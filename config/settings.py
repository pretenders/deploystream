from os import path, environ

APP_PACKAGE = path.basename(path.dirname(__file__))

# The following is the programmatic equivalent of
# from deploystream.local_settings_<CONFIG> import *
GITHUB_CONFIG = GIT_CONFIG = SPRINTLY_CONFIG = None

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
except (AttributeError, ImportError):
    import sys
    print("ERROR: could not import {0}.{1}".format(APP_PACKAGE,
                                                   LOCAL_SETTINGS))
    print("Try running with 'CONFIG=<name> runserver'")
    print("...where you have a {0}.local_settings_<name> file'".format(
        APP_PACKAGE))
    sys.exit(-1)


PROVIDERS = [
    'deploystream.providers.git_provider.GitProvider',
    'deploystream.providers.github.GithubProvider',
    'deploystream.providers.sprintly.SprintlyProvider',
]
"System wide providers"

USER_SPECIFIC_INFO = {
    'provider_config': [
        ('git', GIT_CONFIG),
        ('github', GITHUB_CONFIG),
        ('sprintly', SPRINTLY_CONFIG),
    ]
}
"""Some User specific information that will end up in a db.

provider_config - a dictionary of provider name to config required.
"""

HIERARCHY_REGEXES = []
