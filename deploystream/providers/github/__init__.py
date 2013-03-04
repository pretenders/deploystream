import github3
from zope import interface

from deploystream.apps.feature.models import Feature, PlanningInfo
from deploystream.providers.interfaces import IPlanningPlugin


class GithubIssuesProvider(object):
    """
    An implementation of the planning plugin that gets issues from GitHub
    """
    interface.implements(IPlanningPlugin)

    def __init__(self, user, password, repositories, **kwargs):
        """
        Initialise the plugin by giving it GitHub credentials and repos.

        :param repositories:
            A list of tuples containing (<owner>, <name>) that identify
            a repository in GitHub
        """
        self.github = github3.login(user, password=password)
        self.repositories = repositories

    def get_features(self, **filters):
        """
        Get a list of all features.
        """
        features = []

        for owner, repo in self.repositories:
            ghrepo = self.github.repository(owner, repo)
            for issue in ghrepo.iter_issues(**filters):
                feature = Feature(self, issue.number)
                issue_info = issue.__dict__
                issue_info['feature_type'] = 'defect'
                issue_info['description'] = issue_info['body_html']
                issue_info['owner'] = issue_info['assignee']
                feature.planning_info = PlanningInfo(self, **issue_info)
                features.append(feature)

        return features
