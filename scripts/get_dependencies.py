#!/usr/bin/env python
import os
from os.path import join, dirname


THIS_DIR = dirname(__file__)


def install_from_file(command, filename, version_separator):
    """
    Install requirement from a file with the given command.

    The files use the standard version separator '==' which will get
    replaced with whatever you pass in here in `version_separator`.
    """
    dependencies = join(THIS_DIR, '..', 'requirements', filename + '.txt')
    with open(dependencies, 'r') as f:
        for dependency in f.readlines():
            dependency = version_separator.join(dependency.split('=='))
            os.system('{0} {1}'.format(command, dependency))


install_from_file('npm install -g', 'npm-modules', '@')
install_from_file('bower install', 'bower-components', '#')
