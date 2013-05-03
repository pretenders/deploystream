from mock import Mock, patch
from nose.tools import assert_true, assert_equals

from deploystream.providers.jira import JiraProvider
from deploystream.providers.interfaces import (
        IPlanningProvider, is_implementation)
from tests import load_fixture

ISSUE_RESPONSE_JSON = load_fixture('jira_issues.json')


def test_is_planning_provider():
    assert_true(is_implementation(JiraProvider, IPlanningProvider))


@patch('jira.client.requests')
def test_jira_provider_features(requests):
    """
    Patch requests to use the response in ISSUES.

    Check that we get expected data out from ``get_features`` for jira.
    """
    mock_session_get = Mock()
    mock_session_get.text = ISSUE_RESPONSE_JSON
    mock_session_get.status_code = 200

    requests.Session().get.return_value = mock_session_get

    jira_provider = JiraProvider('user', 'token', 'url',)

    features = jira_provider.get_features()

    assert_equals(features[0]['title'], "Perform update")
    assert_equals(features[0]['id'], "TD-193")
    assert_equals(features[0]['url'],
        "https://something.atlassian.net/rest/api/2/issue/46385")
    assert_equals(features[0]['type'], "Sub-task")
    assert_equals(features[0]['owner'], "alex.couper")
    assert_equals(features[0]['project'], "Superior Project")
