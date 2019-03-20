# Contributing

This document describes how to contribute to this repository. Pull
requests containing bug fixes, updates, and extensions to the existing
tools in this repository will be considered for inclusion.

To maximize the likelihood your contribution will be accepted, it is a
good practice to file an
[issue](https://github.com/peterjc/galaxy_blast/issues) first and
discuss potential solution before proceeding with development.

## How to Contribute

* Make sure you have a [GitHub account](https://github.com/signup/free)
* Make sure you have git [installed](https://help.github.com/articles/set-up-git)
* Fork the repository on [GitHub](https://github.com/peterjc/galaxy_blast/fork)
* Make the desired modifications - consider using a [feature branch](https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches).
* Make sure you have added the necessary tests for your changes and they pass. See [TESTING](https://github.com/peterjc/galaxy_blast#testing) for more information.
* Open a [pull request](https://help.github.com/articles/using-pull-requests) with these changes.

## Coding style

Via the Travis continuous integration testing we enforce various style
checks, including running ``flake8`` on the Python code with this set
of plugins:

```
$ pip install flake8 flake8-blind-except flake8-docstrings flake8-rst-docstrings
```

Additionally, we have adopted the command line tool ``black`` for the
Python coding style - must this must be installed under Python 3, try:

```
$ pip install black
```

Or:

```
$ python3 -m pip install black
```

If you are using Python 3, then we also recommand:

```
$ pip install flake8-black
```

The reStructuredText markup is tested with ``restructuredtext-lint``:

```
$ pip install restructuredtext-lint
```
