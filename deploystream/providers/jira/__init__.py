from jira.client import JIRA
from jira.exceptions import JIRAError

from deploystream.lib import transforms

# Map fields from the Jira API to deploystream names
FEATURE_MAP = {
    ('fields', 'summary'): 'title',
    'key': 'id',
    'self': 'url',
    ('fields', 'issuetype', 'name'): 'type',
    'owner': 'owner',
    ('fields', 'project', 'name'): 'project',
}


def _transform(feature):
    """
    Adapt feature to match normalised field names.
    """
    feature = transforms.remap(feature.raw, FEATURE_MAP)
    return feature


class JiraProvider(object):

    name = 'jira'

    def __init__(self, user, password, url, issue_types=None):
        """
        Initialise by passing credentials and issue types to retrieve.
        """
        if not issue_types:
            issue_types = ['Story', 'Bug']
        self.issue_types = issue_types
        options = {'server': url}
        self._conn = JIRA(options, basic_auth=(user, password))

    def get_features(self, **filters):
        """
        Get all features from this provider.

        :param filters:
            Filtering parameters, such as owner, state, project...

        :returns:
            A list of features that follow the specified criteria
        """
        type_list = ', '.join(self.issue_types)
        features = self._conn.search_issues("type in ({0})".format(type_list))
        features = map(_transform, features)
        return features

    def get_feature_info(self, feature_id):
        """
        :param feature_id:
            The identifier of a feature to be looked up.

        :returns:
            If found, a dictionary containing keys for at least:
                - title
                - id
                - url
                - feature_type
                - owner
                - description

            ``None`` otherwise
        """
        pass
