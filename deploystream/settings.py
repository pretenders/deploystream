from local_settings import GITHUB_CONFIG, GIT_CONFIG, SPRINTLY_CONFIG

PROVIDERS = [
    'deploystream.providers.git_provider.GitProvider',
    'deploystream.providers.github.GithubProvider',
    'deploystream.providers.sprintly.SprintlyProvider',
]
"System wide providers"

USER_SPECIFIC_INFO = {
    'provider_config': {
        'git': GIT_CONFIG,
        'github': GITHUB_CONFIG,
        'sprintly': SPRINTLY_CONFIG,
    }
}
"""Some User specific information that will end up in a db.

provider_config - a dictionary of provider name to config required.
"""

HIERARCHY_REGEXES = []
