from flask import Flask
from deploystream import VERSION

app = Flask(__name__)

USAGE = """
deploystream {version}

Run the application from the command line. For debugging purposes
only. When deploying to a server you should use the .wsgi file.

TODO: create the .wsgi file.

Usage:
    app.py
    app.py <host_port>
    app.py -h | --help
    app.py --version

Options:
    -h --help   Show this screen.
    --version   Show version.
""".format(version=VERSION)

if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(USAGE, version=VERSION)
    kwargs = {}
    if arguments['<host_port>']:
        host, port = arguments['<host_port>'].split(':')
        kwargs['host'] = host
        kwargs['port'] = int(port)

    app.run(**kwargs)
