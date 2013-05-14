from apitopy import Api
from zope import interface

from deploystream.providers.interfaces import IPlanningProvider
from deploystream.lib import transforms


__all__ = ['SprintlyProvider']


# Map fields from the Sprint.ly API to deploystream names
FEATURE_MAP = {
    'number': 'id',
    'short_url': 'url',
    ('product', 'name'): 'project',
}


def _transform(feature):
    """
    Adapt feature to match normalised field names.
    """
    if feature.assigned_to is None:
        feature['owner'] = u''
    else:
        feature['owner'] = u"{first_name} {last_name}".format(
            **feature.assigned_to)
    feature = transforms.remap(feature, FEATURE_MAP)
    return feature


class SprintlyProvider(object):
    """
    An implementation of the planning provider that gets stories from Sprint.ly
    """
    interface.implements(IPlanningProvider)
    name = 'sprintly'
    oauth_token_name = None

    def __init__(self, user, token, current, products=None, **kwargs):
        """
        Initialise by providing credentials and project IDs.

        Load a list of available projects.
        """
        self.api = Api('https://sprint.ly/api/',
                       (user, token), verify_ssl_cert=False, suffix='.json')
        if products:
            self.projects = products
        else:
            self.projects = [p.id for p in self.api.products()]
        self.current = current

    def get_features(self, **filters):
        """
        Get a list of all current features from all projects.
        """
        features = []

        for project_id in self.projects:
            feature_endpoint = self.api.products[project_id].items
            for criterion in self.current:
                features += feature_endpoint(**criterion)

        features = map(_transform, features)
        return features

    def get_feature_info(self, feature_id):
        pass
