# A module for doing all the things.
# Bares a vague resemblance to django's manage.py
#
# You can use it to access the shell, create the db and run the server.

import os
import readline
from pprint import pprint
from flask import *
from deploystream import *
from deploystream import __version__

USAGE = """
deploystream {version}: manage.py

Do things with the application from the command line.

Use this to create the database, access the shell and run the server in debug
mode. When deploying to a server you should use the .wsgi file.

TODO: create the .wsgi file.

Usage:
    manage.py runserver <host_port>
    manage.py syncdb
    manage.py shell
    manage.py -h | --help
    manage.py --version

Options:
    -h --help   Show this screen.
    --version   Show version.
""".format(version=__version__)


def runserver(**kwargs):
    app.run(debug=True, **kwargs)


def syncdb():
    db.create_all()


def shell():
    os.environ['PYTHONINSPECT'] = 'True'

if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(USAGE, version=__version__)
    kwargs = {}
    if arguments['runserver']:
        host, port = arguments['<host_port>'].split(':')
        kwargs['host'] = host
        kwargs['port'] = int(port)
        runserver(**kwargs)
    elif arguments['syncdb']:
        syncdb()
    elif arguments['shell']:
        shell()
