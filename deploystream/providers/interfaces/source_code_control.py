from deploystream.providers.interfaces.base import ProviderInterface


class ISourceCodeControlProvider(ProviderInterface):

    def get_repo_branches_involved(feature_id):
        """
        Get the set of repo, branches involved in the given feature.

        :param feature_id:
            The id of the feature to look for in this all repos and branches.

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
