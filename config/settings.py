from os import path, environ
import traceback

_basedir = path.abspath(path.dirname(__file__))

APP_PACKAGE = path.basename(_basedir)

# Default settings, overridden by the python file pointed to by CONFIG variable
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(_basedir, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# THREADS_PER_PAGE = 8

# CSRF_ENABLED = True
# CSRF_SESSION_KEY = "somethingimpossibletoguess"

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = 'blahblahblahblahblahblahblahblahblah'
RECAPTCHA_PRIVATE_KEY = 'blahblahblahblahblahblahprivate'
RECAPTCHA_OPTIONS = {'theme': 'white'}

GITHUB_CONFIG = GIT_CONFIG = SPRINTLY_CONFIG = JIRA_CONFIG = None

# The following is the programmatic equivalent of
# from deploystream.local_settings_<CONFIG> import *

try:
    CONFIG = environ.get('CONFIG', 'sample')
    LOCAL_SETTINGS = 'local_settings_{0}'.format(CONFIG)
    mod = __import__(APP_PACKAGE, globals(), locals(), [LOCAL_SETTINGS], -1)
    submod = getattr(mod, LOCAL_SETTINGS)
    where = globals()
    for attr in dir(submod):
        if not attr.startswith('__'):
            where[attr] = getattr(submod, attr)
            print("imported " + attr + " from {0}".format(LOCAL_SETTINGS))
except (AttributeError, ImportError) as e:
    import sys
    print("ERROR: could not import {0}.{1}".format(APP_PACKAGE,
                                                   LOCAL_SETTINGS))
    print("Try running with 'CONFIG=<name> runserver'")
    print("...where you have a {0}.local_settings_<name> file'".format(
        APP_PACKAGE))
    print("Original error was: {0}".format(str(e)))
    traceback.print_exc()
    sys.exit(-1)


PROVIDERS = [
    'deploystream.providers.git_provider.GitProvider',
    'deploystream.providers.github.GithubProvider',
    'deploystream.providers.sprintly.SprintlyProvider',
    'deploystream.providers.jira.JiraProvider',
]
"System wide providers"

USER_SPECIFIC_INFO = {
    'provider_config': [
        ('git', GIT_CONFIG),
        ('github', GITHUB_CONFIG),
        ('sprintly', SPRINTLY_CONFIG),
        ('jira', JIRA_CONFIG),
    ]
}
"""Some User specific information that will end up in a db.

provider_config - a dictionary of provider name to config required.
"""

HIERARCHY_REGEXES = []
