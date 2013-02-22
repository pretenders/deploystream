def get_branches_involved(repo_name, feature_id, **kwargs):
    """
    Get the set of brances involved in the given repo and feature.

    :param repo_name:
        The name of the repository to search for branches.

    :param feature_id:
        The id of the feature to look for in branches.

    :param **kwargs:
        Additional configuration for the plugin. If this plugin was written
        by you then this will only be information you have added in the
        configuration of it. See :ref:`<configure_provider>` for more
        information about configuring plugins.

    :returns:
        A list of iterables containing at position:

            0: branch name
            1: latest commit
            2: url to branch (or ``None`` if not applicable)
    """
    pass


def get_merged_status(repo_name, hierarchy_tree, **kwargs):
    """
    Optional function. Get the merged status of the given tree in the repo.

    :param repo_name:
        The name of the repository to search for branches.

    :param hierarchy_tree:
        A tree-like object.

        TODO:
            more definition here... (traversing, etc)

    """
    pass


def default_config():
    """
    Optional function. Return the default configuration for the plugin.

    The return value from this function will be passed in to calls of
    ``get_feature_info`` by default. These can be overwritten by configuration.

    :returns:
        A dictionary containing only string keys and values.
    """
    pass
