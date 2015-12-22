#!/usr/bin/env python3

"""Minimal virtualenv wrapper to add an "alias" for each environment."""

import argparse # We do not use optparse because it is deprecated since python 2.7
import os
import re
import subprocess
import sys

from os.path import expanduser


# Valid command line answers
VALID_CHOICES = {"yes": True, "y": True, "no": False, "n": False}

# Function components
STARTING_LINE = '\n# Start of virtualias function: {0}'
CLOSING_LINE = '# End of virtualias function: {0}'
FUNCTION_BODY = """\n{0}() {{
    cd {1}
    source {1}/{2}/bin/activate
}}\n"""
FUNCTION_TEXT = STARTING_LINE + FUNCTION_BODY + CLOSING_LINE
FUNCTION_REGEXP = '{}\\(\\)\\s{{\n.*}}'

# Function reference to be written in the shell configuration file
FUNCTIONS_REFERENCE_START = '\n# VirtuAlias functions reference.'
FUNCTIONS_REFERENCE_BODY = """\nif [ -f ~/.virtualias_functions ]; then
    source ~/.virtualias_functions
fi"""
FUNCTIONS_REFERENCE = FUNCTIONS_REFERENCE_START + FUNCTIONS_REFERENCE_BODY

# Supported shells and relative configuration files:
SUPPORTED_SHELLS = {
    '/bin/bash': '~/.bashrc',
    '/usr/bin/bash': '~/.bashrc',
    '/bin/zsh': '~/.zshrc',
    '/usr/bin/zsh': '~/.zshrc'
}


class AliasExistsException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


def alias_exists(alias, alias_stream):
    """Check if alias already exists in the configuration file."""

    alias_re = r"\b{}()\b".format(alias)
    for line in alias_stream:
        if re.match(alias_re, line):
            return True
    return False

def call_virtualenv(virtualenv_args):
    popen = subprocess.Popen(["virtualenv"] + virtualenv_args, stdout=subprocess.PIPE)
    lines_iterator = iter(popen.stdout.readline, b"")
    for line in lines_iterator:
        print(line.decode('utf-8'), end='') # Decode the byte object
    # Wait for process to terminate before retrieving the return code
    stream = popen.communicate()[0]
    if popen.returncode != 0:
        raise RuntimeError("Virtualenv call failed.")

def delete_alias(alias, filename):
    """Remove the alias function from the configuration file.
    NOTE: this method requries function comments to be present in the configuration
    file, as defined by the `STARTING_LINE` and `CLOSING_LINE` constants.
    """

    filepath = expanduser(filename)
    with open(filepath, 'r+') as alias_stream:
        text = ''
        for line in alias_stream:
            if line.strip() == STARTING_LINE.format(alias).strip():
                # Skip lines until we reach the end of the function.
                found_closing_line = False
                for function_line in alias_stream:
                    if function_line.strip() == CLOSING_LINE.format(alias).strip():
                        found_closing_line = True
                        break
                if not found_closing_line:
                    print("VirtuAlias cannot delete the alias.")
                    return False
            else:
                text += line

        alias_stream.seek(0)
        alias_stream.truncate()
        alias_stream.write(text)

def destination_specified(virtualenv_args):
    """Check if a parameter to define the destination folder for the virtualenv
    command has been specified.
    """
    if virtualenv_args:
        for arg in virtualenv_args:
            if not arg.startswith("-"):
                # This argument represents the virtualenv destination folder
                return arg
    return None

def detect_shell_config():
    """Detect the default shell and outputs its configuration file path."""

    shell_var = subprocess.check_output('echo $SHELL', shell=True)
    if shell_var:
        shell_var = shell_var.decode('utf-8').strip()
        if shell_var in SUPPORTED_SHELLS:
            return SUPPORTED_SHELLS[shell_var]

    return None

def edit_alias_file(alias, virtualenv_args, filename):
    dest_dir = destination_specified(virtualenv_args)
    if not dest_dir:
        print("You did not specify a folder for your virtualenv. Quitting.") # subsitute this with an exception
        sys.exit()

    filepath = expanduser(filename)
    with open(filepath, 'a+') as alias_stream:
        # a+ opens the file at its end. So we need to go back to the top
        alias_stream.seek(0)
        try:
            write_alias(alias_stream, alias, dest_dir)
        except AliasExistsException as e:
            raise

def edit_config_file(filepath):
    """Modify the shell configuration file, adding a reference to the VirtuAlias
    functions file (if it is not already present).
    """
    filepath = expanduser(filepath)
    with open(filepath, 'a+') as config_stream:
        # a+ opens the file at its end. So we need to go back to the top
        config_stream.seek(0)
        if not reference_exists(config_stream):
            print("Writing reference to VirtuAlias functions file in " + filepath + ".")
            config_stream.write(FUNCTIONS_REFERENCE)

def reference_exists(config_stream):
    for line in config_stream:
        if line.strip() == FUNCTIONS_REFERENCE_START.strip():
            return True
    return False

def write_alias(alias_stream, alias, dest_dir):
    """Write the alias (actually a function with the alias name) in the configuration
    file. Function behaviour: change directory to the new virtualenv directory
    (`dest_dir`), then activate the environment.
    """

    if alias_exists(alias, alias_stream):
        raise AliasExistsException("Alias '{}' already defined. ".format(alias) +
                "Please choose another alias for your virtual environment.")

    CURRENT_DIR = os.getcwd()
    function_text = FUNCTION_TEXT.format(alias, CURRENT_DIR, dest_dir)

    alias_stream.write(function_text + '\n')

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


def main():
    parser = argparse.ArgumentParser(
        description="Wraps virtualenv command adding aliases for the environments. \
        Similar to virtualenvwrapper, but without the WORKING_HOME variable.")

    # dest is the name that the variable will take. I.e. args.alias in this case.
    parser.add_argument(
        '-a', '--alias',
        dest='alias',
        action='store',
        help='Add specified alias to your shell configuration file.')

    parser.add_argument('virtualenv_args', nargs='*')
    args = parser.parse_args()
    # If an alias is specified, create the alias and call virtualenv
    if not len(sys.argv) > 1:
        print('You must provide some arguments.')
        parser.print_help()
        sys.exit(2)
    elif args.alias:
        shell_config_file = detect_shell_config()
        edit_config_file(shell_config_file)
        edit_alias_file(args.alias, args.virtualenv_args, filename='~/.virtualias_functions')
        try:
            call_virtualenv(args.virtualenv_args)
        except RuntimeError as e:
            delete_alias(args.alias, filename='~/.virtualias_functions')

    # If an alias is NOT specified, ask user and eventually call virtualenv
    else:
        old_ve_question = ("You did not specify an alias for your environment. Do "
            "you want to create it anyway using the virtualenv command?")
        use_old_ve = user_yes_no(old_ve_question)
        if use_old_ve:
            print("Calling virtualenv.")
            call_virtualenv(args.virtualenv_args)
        else:
            print("Exiting.")
            sys.exit(2)

if __name__ == '__main__':
    main()
