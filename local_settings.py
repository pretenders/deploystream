# Run ./get_github_token.py once to generate github_auth.py with your TOKEN
from github_auth import TOKEN

GITHUB_CONFIG = {
    'repositories': [('pretenders', 'deploystream')],
    'token': TOKEN,
}
