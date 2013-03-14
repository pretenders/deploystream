#!/usr/bin/env python
import os


with open('requirements/nodeenv.txt', 'r') as f:
    for line in f.readlines():
        os.system('npm install -g {0}'.format(line))
