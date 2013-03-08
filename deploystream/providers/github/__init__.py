import github3
from zope import interface

from deploystream.apps.feature.models import Feature, PlanningInfo
from deploystream.providers.interfaces import IPlanningPlugin
from deploystream.lib import transforms


FEATURE_MAP = {
    'body_html': 'description',
    'assignee': 'owner',
}
BUILD_MAP = {
    'created_at': 'timestamp',
    'result': ('state', {
                'success': 'success',
                'pending': 'pending',
                'failed': 'failure',
                'error': 'unstable',
              }),
    'target_url': 'url',
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
            for issue in ghrepo.iter_issues(**filters):
                feature = Feature(self, issue.number)
                issue_info = transforms.remap(issue.__dict__, FEATURE_MAP)
                issue_info['feature_type'] = 'defect'
                feature.planning_info = PlanningInfo(self, **issue_info)
                features.append(feature)

        return features

    def get_feature_info(self, feature_id):
        pass

    def get_build_information(self, repo, owner, branch, commit):
        ghrepo = self.github.repository(owner, repo)
        for status in ghrepo.iter_statuses(commit):
            build_info = transforms.remap(status.__dict__, BUILD_MAP)
            build_info['commit'] = commit
