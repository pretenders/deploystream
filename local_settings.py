# Run ./get_github_token.py once to generate github_auth.py with your TOKEN
from github_auth import TOKEN

GITHUB_CONFIG = {
    'repositories': [('pretenders', 'deploystream')],
    'token': TOKEN,
}


GIT_CONFIG = {
    'code_dir': None,
    'feature_breakup_regex': "(?P<project>[a-zA-Z]+)-?(?P<id>[0-9]+)",
    'branch_finder_template': ".*(?i){project}.*"
}
