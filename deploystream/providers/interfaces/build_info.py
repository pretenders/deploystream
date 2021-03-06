from deploystream.providers.interfaces.base import ProviderInterface


class IBuildInfoProvider(ProviderInterface):

    def get_build_information(repo, branch, commit):
        """
        Get build information for the given repo, branch and commit.

        :param repo_name:
            The name of the repository to get build info for.

        :param branch:
            The name of the branch to get build info for.

        :param commit:
            The commit of specific interest. This will be the commit that is at
            the head of the given branch and repo_name. If there is no build
            information for this commit it is acceptable to return build
            information for the latest build - but it is important to include
            the new commit in the return data.

        :returns:
            A dictionary containing keys and values for at least:
                - timestamp (of the build - a datetime object)
                - result (one of "success", "failure", "unstable", "partial")
                - commit (of the build)
                - url
        """
        pass
