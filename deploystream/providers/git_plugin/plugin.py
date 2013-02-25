import git


class GitPlugin(object):

    def get_repo_branches_involved(self, feature_id, **kwargs):
        pass

    def get_branches_involved(self, repo_name, feature_id, **kwargs):
        """
        Get the set of brances involved in the given repo and feature.

        :param repo_name:
            The name of the repository to search for branches.

        :param feature_id:
            The id of the feature to look for in branches.

        :param kwargs:
            Expected to contain keys for:

                - CODE_DIR: The directory in which repo ``repo_name`` can be
                  found.

        :returns:
            A list of iterables containing at position:

                0: branch name
                1: latest commit
        """
        code_dir = kwargs['CODE_DIR']
        repo = git.Repo("{CODE_DIR}/{REPO_NAME}/.git".format(
                                                    CODE_DIR=code_dir,
                                                    REPO_NAME=repo_name,))
        remote = git.remote.Remote(repo, 'origin')
        affected = []
        for remote_ref in remote.refs:
            if feature_id in remote_ref.remote_head:
                affected.append((remote_ref.remote_head,
                                 str(remote_ref.commit)))

        return affected

    def set_merged_status(self, repo_name, hierarchy_tree, **kwargs):
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
