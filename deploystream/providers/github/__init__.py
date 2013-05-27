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
                    issue_info = self._convert_to_dict(issue, project)
                    features.append(issue_info)

        # sort by putting PRs first, stories second
        features = sorted(features, key=lambda f: f['type'] == 'story')

        return features

    def _convert_to_dict(self, issue, project):
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
        return issue_info

    def get_feature_info(self, feature_id):
        # Issue with this approach is that we return the first issue with an
        # ID across all repos.
        # Such are the shortcomings of using Git as a planning provider. To
        # get round this we'd need to have the repo in the feature_id, but this
        # seems a bad idea from the POV of matching branch names.
        for repository in self.repositories:
            project = '{0}/{1}'.format(repository.owner.login,
                                       repository.name)
            issue = repository.issue(feature_id)
            if issue:
                return self._convert_to_dict(issue, project)

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
                - repository
                - name
                - parent_name
                - commit_id
                - has_parent
                - in_parent

        Look through each repo and get a set of branches that match the
        ``hierarchy_regexes``.

        Go through matching branches finding their merge status.

        .. note::
            We loop through all the commits for every matching branch exactly
            once. This could be optimized to only check back as far as some
            ancestor's HEAD.

        """
        branch_list = []

        for repo in self.repositories:
            repo_branches = {}
            for branch in repo.iter_branches():
                repo_branches[branch.name] = {
                    'sha': branch.commit.sha,
                }

            genealogy = hierarchy.match_with_genealogy(
                feature_id, repo_branches.keys(), hierarchy_regexes)

            for branch, parent in genealogy:
                has_parent = None
                in_parent = None
                branch_data = repo_branches[branch]

                if parent:
                    for sha in [branch, parent]:
                        # Loop through all the commits for branch and parent if
                        # we haven't already done so and store them in the
                        # temporary ``repo_branches`` dict
                        if repo_branches[sha].get('commits') is None:
                            repo_branches[sha]['commits'] = [
                                c.sha for c in repo.iter_commits(sha=sha)
                            ]
                    # Check if we're merged in
                    parent_data = repo_branches[parent]
                    has_parent = parent_data['sha'] in branch_data['commits']
                    in_parent = branch_data['sha'] in parent_data['commits']

                branch_list.append({
                    "repository": repo.name,
                    "name": branch,
                    "commit_id": branch_data['sha'],
                    "parent_name": parent,
                    "has_parent": has_parent,
                    "in_parent": in_parent,
                })

        return branch_list
