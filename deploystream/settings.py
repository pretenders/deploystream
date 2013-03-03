
SOURCE_CODE_PLUGINS = ['deploystream.providers.git_plugin.GitPlugin']
PLANNING_PLUGINS = []
BUILD_INFO_PLUGINS = []

HIERARCHY_REGEXES = []


PLUGIN_CONFIG = {
    'GitPlugin': {
        'code_dir': None
    }
}
"""A dict of configuration information for the plugins.
Keys are plugin class names, values are dictionaries to be passed in as kwargs
during insantiation.
"""
