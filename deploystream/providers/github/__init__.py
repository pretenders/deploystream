import github3
import re
from zope import interface

from deploystream.providers.interfaces import IPlanningProvider
from deploystream.lib import transforms, hierarchy


__all__ = ['GithubProvider']


# Map fields from the Github API to deploystream names
FEATURE_MAP = {
    'body_html': 'description',
    'html_url': 'url',
    'number': 'id',
    'id': 'github_id',
}


class GithubProvider(object):
    """
    An implementation of the planning provider that gets issues from GitHub
    """
    interface.implements(IPlanningProvider)
    name = 'github'
    oauth_token_name = name

    def __init__(self, token, organization=None, repositories=None, **kwargs):
        """
        Initialise the provider by giving it GitHub credentials and repos.

        :param organization:
            The name of the organization who's repository issues should be
            identified in GitHub. If ``None`` and no ``repositories`` given,
            then the authenticated user's issues will be tracked.

        :param repositories:
            A list of tuples containing (<owner>, <name>) that identify
            a repository in GitHub. This is only looked at if ``organization``
            is ``None``.
        """

        if token is None and "username" in kwargs and "password" in kwargs:
            # We can login using username and password for testing purposes
            self.github = github3.login(
                kwargs['username'],
                password=kwargs['password']
            )
        else:
            self.github = github3.login(token=token)

        if organization:
            org = self.github.organization(organization)
            self.repositories = list(org.iter_repos())
        elif repositories:
            self.repositories = []
            for owner, repo in repositories:
                self.repositories.append(self.github.repository(owner, repo))
        else:
            self.repositories = list(self.github.iter_repos())

    def get_features(self, **filters):
        """
        Get a list of all features.
        """
        features = []
        for repository in self.repositories:
            project = '{0}/{1}'.format(repository.owner.login,
                                       repository.name)
            if repository.has_issues:
                for issue in repository.iter_issues(**filters):
                    issue_info = transforms.remap(issue.__dict__, FEATURE_MAP)
                    if issue.pull_request:
                        issue_type = 'PR'
                    else:
                        issue_type = 'story'
                    issue_info['type'] = issue_type
                    issue_info['project'] = project
                    owner = issue_info['assignee']
                    if owner is None:
                        issue_info['owner'] = ''
                    else:
                        # take only login name from User object
                        issue_info['owner'] = owner.login
                    features.append(issue_info)

        # sort by putting PRs first, stories second
        features = sorted(features, key=lambda f: f['type'] == 'story')

        return features

    def get_feature_info(self, feature_id):
        pass

    @classmethod
    def get_oauth_data(self):
        return {
            'base_url': 'https://api.github.com/',
            'request_token_url': None,
            'access_token_url': 'https://github.com/login/oauth/access_token',
            'authorize_url': 'https://github.com/login/oauth/authorize',
            'request_token_params': {
                'scope': 'repo'
            },
        }

    def get_repo_branches_involved(self, feature_id, hierarchy_regexes):
        """
        Get the list of branches involved for the given ``feature_id``.

        :returns:
            A list of dictionaries containing keys for:
                - repo_name
                - branch_name
                - parent_branch_name
                - latest_commit
        """
        branch_list = []

        for repo in self.repositories:
            repo_branches = {}
            for branch in repo.iter_branches():
                repo_branches[branch.name] = {'sha': branch.commit.sha}

            geneology = hierarchy.match_with_geneology(
                feature_id, repo_branches.keys(), hierarchy_regexes)

            for branch, parent in geneology:

                branch_list.append({
                    "repo_name": repo.name,
                    "branch_name": branch,
                    "latest_commit": repo_branches[branch]['sha'],
                    "parent_branch_name": parent,
                })
        return branch_list

# def iter_commits(repo, branch):
# from github3.repos.commit import RepoCommit
#     def iter_parents(commit_sha):
#         url = repo._build_url('commits', commit_sha, base_url=repo._api)
#         json = repo._json(repo._get(url), 200)
#         commit = RepoCommit(json)
#         yield commit
#         for parent in commit.parents:
#             for commit in iter_parents(RepoCommit(parent).sha):
#                 yield commit

#     return iter_parents(branch.commit.sha)
