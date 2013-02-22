from deploystream import VERSION, app

USAGE = """
deploystream {version}: runserver.py

Run the application from the command line. For debugging purposes
only. When deploying to a server you should use the .wsgi file.

TODO: create the .wsgi file.

Usage:
    runserver.py
    runserver.py <host_port>
    runserver.py -h | --help
    runserver.py --version

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

    app.run(debug=True, **kwargs)
