#!/usr/bin/env python3

"""Minimal virtualenv wrapper to add an "alias" for each environment."""

import argparse # We do not use optparse because it is deprecated since python 2.7
import os
import pdb
import re
import subprocess
import sys

from os.path import expanduser

VALID_CHOICES = {"yes": True, "y": True, "no": False, "n": False}

class AliasExistsException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


def write_alias(config_file, alias, dest_dir):
    """Write the alias (actually a function with the alias name) in the configuration
    file. Function behaviour: change directory to the new virtualenv directory
    (`dest_dir`), then activate the environment.
    """

    if alias_exists(alias, config_file):
        raise AliasExistsException("Alias '{}' already defined. ".format(alias) +
                "Please choose another alias for your virtual environment.")

    CURRENT_DIR = os.getcwd()
    function_text = """\n{0}() {{
            cd {1}
            source {1}/{2}/bin/activate
    }}""".format(alias, CURRENT_DIR, dest_dir)

    config_file.write(function_text + '\n')

def alias_exists(alias, config_file):
    """Check if alias already exists in the configuration file."""

    alias_re = r"\b{}()\b".format(alias)
    for line in config_file:
        if re.match(alias_re, line):
            return True
    return False

def destination_specified(virtualenv_args):
    """Check if a parameter to define the destination folder for the virtualenv
    has been specified.
    """

    if virtualenv_args:
        for arg in virtualenv_args:
            if not arg.startswith("-"):
                # This argument represents the virtualenv destination folder
                return arg
    return None

def edit_config_file(alias, virtualenv_args, filename='~/.zshrc'):
    dest_dir = destination_specified(virtualenv_args)
    if not dest_dir:
        print("You did not specify a folder for your virtualenv. Quitting") # subsitute this with an exception
        sys.exit()

    filepath = expanduser(filename)
    with open(filepath, 'a+') as config_file:
        # a+ opens the file at its end. So we need to go back to the top
        config_file.seek(0)
        try:
            write_alias(config_file, alias, dest_dir)
        except AliasExistsException as e:
            raise

def user_yes_no(question, default='yes'):
    while True:
        print(question, end='')

        if default is None:
            print(" [y/n]")
        elif default=='yes':
            print(" [Y/n]")
        elif default=='no':
            print(" [y/N]")
        else:
            raise ValueError("Invalid default answer {}".format(default))

        choice = input().lower()
        if default is not None and choice == '':
            return VALID_CHOICES[default]
        elif choice in VALID_CHOICES:
            return VALID_CHOICES[choice]
        else:
            print("Please answer 'yes' or 'no' ('y' or 'n')")

def call_virtualenv(virtualenv_args):
    popen = subprocess.Popen(["virtualenv"] + virtualenv_args, stdout=subprocess.PIPE)
    lines_iterator = iter(popen.stdout.readline, b"")
    for line in lines_iterator:
        print(line.decode('utf-8'), end='') # Decode the byte object


def main():
    parser = argparse.ArgumentParser(
        description="Wraps virtualenv command adding alias to ~/.zshrc. Similar \
        to virtualenvwrapper, but without the WORKING_HOME variable.")

    # dest is the name that the variable will take. I.e. args.alias in this case.
    parser.add_argument('-a', '--alias', dest='alias', action='store',
        help='Add specified alias to .zshrc file.')

    args, virtualenv_args = parser.parse_known_args()

    # If an alias is specified, create the alias and call virtualenv
    if args.alias:
        edit_config_file(args.alias, virtualenv_args, filename='~/.zshrc')
        call_virtualenv(virtualenv_args)

    # If an alias is NOT specified, ask user and eventually call virtualenv
    else:
        old_ve_question = ("You did not specify an alias for your environment. Do "
            "you want to create it anyway using the good old virtualenv command?")
        use_old_ve = user_yes_no(old_ve_question)
        if use_old_ve:
            print("Use old virtualenv")
            call_virtualenv(virtualenv_args)
        else:
            print("Exiting")
            sys.exit()

if __name__ == '__main__':
    main()
