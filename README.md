# VirtuAlias

**VirtuAlias** is a minimal wrapper for **virtualenv**. It will simply create a new alias (actually, a ***function***) everytime you create a new environment, allowing you to switch between them. Functions are appended to your `~/.bashrc` or `~/.zshrc` configuration file.

**Note** that this is a pretty basic script. If you are looking for something more, then you are probably looking for [**virtualenvwrapper**](https://virtualenvwrapper.readthedocs.org/en/latest/).

Please feel free to make new **Pull Requests** and provide suggestions: the main reason why I created **VirtuAlias** is to learn something new, so I will be grateful for every suggestion I will receive.


The function
------------

**VirtuAlias** writes a function at the bottom of your favourite shell configuration file (depending on the `$SHELL` variable).

| Shell    | $SHELL      | Config file |
| -------- | ----------- | ----------- |
| **Bash** | `/bin/bash` | `~/.bashrc` |
| **Zsh**  | `/bin/zsh`  | `~/.zshrc`  |

The function is as simple as follows:

```bash
your_alias() {
    cd your/environment/folder;
    source your/environment/folder/bin/activate;
    }
```


Usage
----------

**VirtuAlias** can be used as you would use **virtualenv**, with an additional parameter `-a` (`--alias`). E.g.:

`./virtualias.py -a="your_alias" your_env_dir`

In the above case, your new environment will be created in `your_env_dir` and you will be able to activate it using the alias you specified (`your_alias` in the example above).


Is VirtuAlias an alternative to virtualenvwrapper?
---------------------------------------------------

**VirtuAlias** is just a personal experiment.

The reason why I wrote this script is that, as far as I know, **virtualenvwrapper** only allows you to switch between different environments created inside a pre-specified directory (`WORKON_HOME` variable). On the contrary, I needed to create my environments in several locations on my disk, so I decided to create this script that does not require any specific location. As stated above, if you are looking for something more, then you are probably looking for [**virtualenvwrapper**](https://virtualenvwrapper.readthedocs.org/en/latest/).

Improvements
------------

Some improvements are auspicable or necessary:

- [x] If the `virtualenv` call fails, we should not write the function in the shell configuration file.

- [ ] `source` the configuration file after having written the function.

- [ ] Adding a specific file to store all aliases/functions (so that we do not mess too much with the shell configuration file). We could do this by adding the following in the shell configuration file:

```bash
# Add VirtuAlias functions.
if [ -f ~/.virtualias_functions ]; then
    source ~/.virtualias_functions
fi
```

This entails that we would need to check for duplicate alias/function names in both the shell configuration file ***and*** the new `~/.virtualias_functions` file.

- [ ] Providing a method to **remove** aliases when we delete an environment.

- [ ] Automatically detecting shell (e.g. **bash**, **zsh**).

- [ ] Providing a parameter to manually specify the shell configuration file (e.g. `~/.bashrc`, `~/.zshrc`, etc.).

- [ ] Creating a wrapper around **VirtuAlias** so that the script is only executed when your Python version is `>= 3`.
    (A wrapper is needed in order to avoid `SyntaxError` problems. See [this SO question](http://stackoverflow.com/questions/446052/how-can-i-check-for-python-version-in-a-program-that-uses-new-language-features))

- [ ] Packaging (`setup.py`, etc.). Since this is a very small project, it may be not necessary.
