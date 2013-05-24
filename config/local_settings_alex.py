
GITHUB_CONFIG = {
    'organization': 'pretenders',
}


# GIT_CONFIG = {
#     'feature_breakup_regex': "(?P<project>[a-zA-Z]+)-?(?P<id>[0-9]+)",
#     'branch_finder_template': ".*(?i){project}.*"
# }

HIERARCHY_REGEXES = [
        'master',
        'develop',
        'story/{FEATURE_ID}',
        'story/{FEATURE_ID}/[a-z_]*',
        '{PARENT}[/_][a-z]*',
        'dev/{FEATURE_ID}/[a-z]*',
        '{PARENT}[/_][a-z]*',
]

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
