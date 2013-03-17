from zope import interface


class ISourceCodeControlProvider(interface.Interface):

    name = interface.Attribute(
                "The name the provider will be referred to in configs etc.")
    oauth_token_required = interface.Attribute(
                "If an oauth token is required, the name of it as defined by "
                "the oauth provider.")

    def get_repo_branches_involved(feature_id):
        """
        Get the set of repo, branches involved in the given feature.

        :param feature_id:
            The id of the feature to look for in this all repos and branches.

        :param **kwargs:
            Additional configuration for the provider. If this provider was written
            by you then this will only be information you have added in the
            configuration of it. See :ref:`<configure_provider>` for more
            information about configuring providers.

        :returns:
            A list of iterables containing at position:

                0: repo name
                1: branch name
                2: latest commit
        """
        pass

    def set_merged_status(repo_name, hierarchy_tree):
        """
        Set the merged status of the given tree in the repo.

        :param repo_name:
            The name of the repository to search for branches.

        :param hierarchy_tree:
            A tree-like object.

            TODO:
                more definition here... (traversing, etc)

        """
        pass
