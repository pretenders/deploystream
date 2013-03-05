from local_settings import GITHUB_CONFIG


SOURCE_CODE_PLUGINS = [
    ('deploystream.providers.git_plugin.plugin.GitPlugin', {}),
]

PLANNING_PLUGINS = [
    ('deploystream.providers.github.GithubProvider', GITHUB_CONFIG),
]

BUILD_INFO_PLUGINS = []

HIERARCHY_REGEXES = []
