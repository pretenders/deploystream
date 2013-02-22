from deploystream.providers.base import ProviderPluginReader


class SourceCodeControlPlugin(ProviderPluginReader):

    required = {
        'get_branches_involved': [
            'repo_name',
            'feature_id',
            '**kwargs',
        ]
    }

    optional = {
        'get_merged_status': [
            'repo_name',
            'hierarchy_tree',
            '**kwargs',
            ],
        'default_config': [],
    }
