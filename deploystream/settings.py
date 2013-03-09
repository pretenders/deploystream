from local_settings import GITHUB_CONFIG, GIT_CONFIG


SOURCE_CODE_PLUGINS = [
    ('deploystream.providers.git_provider.GitProvider', GIT_CONFIG),
]

PLANNING_PLUGINS = [
    ('deploystream.providers.github.GithubProvider', GITHUB_CONFIG),
]

BUILD_INFO_PLUGINS = []

HIERARCHY_REGEXES = []
