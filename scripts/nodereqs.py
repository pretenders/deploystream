#!/usr/bin/env python
import os
from os.path import join, dirname


THIS_DIR = dirname(__file__)
npm_dependencies = join(THIS_DIR, '..', 'requirements', 'nodeenv.txt')

with open(npm_dependencies, 'r') as f:
    for line in f.readlines():
        os.system('npm install -g {0}'.format(line))
