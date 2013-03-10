import github3
from zope import interface

from deploystream.apps.feature.models import Feature, PlanningInfo
from deploystream.providers.interfaces import IPlanningPlugin
from deploystream.lib import transforms


FEATURE_MAP = {
    'body_html': 'description',
    'assignee': 'owner',
}


class GithubProvider(object):
    """
    An implementation of the planning plugin that gets issues from GitHub
    """
    interface.implements(IPlanningPlugin)

    def __init__(self, token, repositories, **kwargs):
        """
        Initialise the plugin by giving it GitHub credentials and repos.

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
                feature = Feature(self, issue.number, project=project)
                issue_info = transforms.remap(issue.__dict__, FEATURE_MAP)
                issue_info['feature_type'] = 'defect'
                feature.planning_info = PlanningInfo(self, **issue_info)
                features.append(feature)

        return features

    def get_feature_info(self, feature_id):
        pass
