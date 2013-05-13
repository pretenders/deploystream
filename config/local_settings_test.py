GITHUB_CONFIG = {
    'organization': 'pretenders'
}

SPRINTLY_CONFIG = {
    'user': 'carles.barrobes@rockaboxmedia.com',
    'token': 'iwonttell',
    'current': [
        {'status': 'in-progress', 'limit': 100},
        {'status': 'backlog', 'limit': 100},
    ],
}

GIT_CONFIG = {
}

try:
    from non_github_settings import GITHUB_USERNAME, GITHUB_PASSWORD
    GITHUB_CONFIG['username'] = GITHUB_USERNAME
    GITHUB_CONFIG['password'] = GITHUB_PASSWORD
except ImportError:
    print ("Failed to import from non_github_settings. \n"
        "You need GITHUB_PASSWORD and GITHUB_USERNAME defined in a module "
        "named ``non_github_settings`` in order to run the tests."
        )
    raise
