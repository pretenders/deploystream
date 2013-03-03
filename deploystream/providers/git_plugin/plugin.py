import os
from os.path import join, exists

import git


class GitPlugin(object):

    def __init__(self, code_dir='.'):
        self.code_dir = code_dir

    def get_repo_branches_involved(self, feature_id):
        """
        Get all the repo branches involved.

        For each repository in each repo location defined in configuration,
        call ``get_branches_involved`` and return a list of tuples.

        :returns:
            A list of iterables containing at position:

                0: repo name
                1: branch name
                2: latest commit
        """
        # Every folder in side self.code_dir that is a git repo will be looked
        # at
        repo_branches = []
        for repo_name in os.listdir(self.code_dir):
            repo_location = join(self.code_dir, repo_name)
            if exists(join(repo_location, ".git")):
                branches = self.get_branches_involved(repo_location,
                                                      feature_id)
                repo_branches.extend([(repo_name, ) + branch
                                            for branch in branches])
        return repo_branches

    def get_branches_involved(self, repo_location, feature_id):
        """
        Get the set of brances involved in the given repo and feature.

        :param repo_location:
            The location of the repository to search for branches.

        :param feature_id:
            The id of the feature to look for in branches.

        :returns:
            A list of iterables containing at position:

                0: branch name
                1: latest commit
        """
        repo = git.Repo("{repo_location}/.git"
                        .format(repo_location=repo_location))
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
