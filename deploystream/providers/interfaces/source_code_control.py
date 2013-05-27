from deploystream.providers.interfaces.base import ProviderInterface


class ISourceCodeControlProvider(ProviderInterface):

    def get_repo_branches_involved(feature_id, hierarchy_tree):
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
