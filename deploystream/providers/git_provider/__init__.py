import os
from os.path import join, exists
import re

import git


class GitProvider(object):

    name = 'git'
    oauth_token_name = None

    def __init__(self, code_dir='.',
                 feature_breakup_regex='',
                 branch_finder_template=''):
        """
        Create a GitProvider.

        :param code_dir:
            The filesystem path to the directory within which all repositories
            live that are to be queried.

        :param feature_breakup_regex:
            A regular expression to be used to breakup feature ids into
            understandable parts. The regex should use named groups to be
            of use to the ``branch_finder_template``.

            eg. "(?P<project>[a-zA-Z]+)-?(?P<id>[0-9]+)"

        :param branch_finder_template:
            A template regular expression with named gaps to be filled by the
            outcome of breaking up the feature.

            eg. ".*{id}.*"

        """
        self.code_dir = code_dir
        self.feature_breakup_regex = feature_breakup_regex
        self.branch_finder_template = branch_finder_template

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
        # Every folder inside self.code_dir that is a git repo will be looked
        # at
        repo_branches = []
        for repo_name in os.listdir(self.code_dir):
            repo_location = join(self.code_dir, repo_name)
            if exists(join(repo_location, ".git")):
                branches = self.get_branches_involved(repo_location,
                                                      feature_id)
                repo_branches.extend([
                    (repo_name, ) + branch for branch in branches])
        return repo_branches

    def _get_feature_breakdown(self, feature_id):
        """
        Break up the feature_id using the regex in configuration.
        """
        match = re.search(self.feature_breakup_regex, feature_id)
        if match:
            return match.groupdict()

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
        feature_breakup = self._get_feature_breakdown(feature_id)
        regex = self.branch_finder_template.format(**feature_breakup)
        for remote_ref in remote.refs:
            if re.search(regex, remote_ref.remote_head):
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
