import github3
from zope import interface

from deploystream.providers.interfaces import IPlanningProvider
from deploystream.lib import transforms


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
    oauth_token_required = name

    def __init__(self, token, repositories, **kwargs):
        """
        Initialise the provider by giving it GitHub credentials and repos.

        :param repositories:
            A list of tuples containing (<owner>, <name>) that identify
            a repository in GitHub
        """
        self.github = github3.login(token=token)
        self.repositories = repositories

    def get_features(self, **filters):
        """
        Get a list of all features.
        """
        features = []

        for owner, repo in self.repositories:
            ghrepo = self.github.repository(owner, repo)
            project = '{0}/{1}'.format(owner, repo)
            for issue in ghrepo.iter_issues(**filters):
                issue_info = transforms.remap(issue.__dict__, FEATURE_MAP)
                issue_info['type'] = 'story'
                issue_info['project'] = project
                owner = issue_info['assignee']
                if owner is None:
                    issue_info['owner'] = ''
                else:
                    # take only login name from User object
                    issue_info['owner'] = owner.login
                features.append(issue_info)

        return features

    def get_feature_info(self, feature_id):
        pass
