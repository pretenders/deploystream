
GITHUB_CONFIG = {
    'organization': 'pretenders',
}


GIT_CONFIG = {
    'code_dir': None,
    'feature_breakup_regex': "(?P<project>[a-zA-Z]+)-?(?P<id>[0-9]+)",
    'branch_finder_template': ".*(?i){project}.*"
}


JIRA_CONFIG = {
    'url': '',
    'user': None,
    'password': None,
}


try:
    from non_github_settings import JIRA_CONFIG
except ImportError:
    print "Failed to import from non_github_settings"
    raise
