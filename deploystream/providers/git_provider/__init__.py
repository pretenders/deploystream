import os
from os.path import join, exists
import re

import git

from deploystream.lib import hierarchy


class GitProvider(object):

    name = 'git'
    oauth_token_name = None

    def __init__(self, code_dir):
        """
        Create a GitProvider.

        :param code_dir:
            The filesystem path to the directory within which all repositories
            live that are to be queried.
        """
        self.code_dir = code_dir

    def get_repo_branches_involved(self, feature_id, hierarchy_regexes):
        """
        Get all the repo branches involved.

        For each repository in each repo location defined in configuration,
        call ``get_branches_involved`` and return a list of tuples.


        :returns:
            A list of dictionaries containing keys for:
                - repo_name
                - branch_name
                - parent_branch_name
                - latest_commit
        """
        branch_list = []

        for repo_name in os.listdir(self.code_dir):
            repo_location = join(self.code_dir, repo_name)
            if exists(join(repo_location, ".git")):
                repo_branches = {}

                repo = git.Repo("{repo_location}/.git"
                        .format(repo_location=repo_location))
                remote = git.remote.Remote(repo, 'origin')
                for remote_ref in remote.refs:
                    repo_branches[remote_ref.remote_head] = {
                            'sha': str(remote_ref.commit)
                    }

                geneology = hierarchy.match_with_geneology(
                    feature_id, repo_branches.keys(), hierarchy_regexes)

                for branch, parent in geneology:
                    branch_list.append({
                        "repo_name": repo_name,
                        "branch_name": branch,
                        "latest_commit": repo_branches[branch]['sha'],
                        "parent_branch_name": parent,
                    })

        return branch_list
