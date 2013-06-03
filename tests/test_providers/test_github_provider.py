from mock import Mock, patch
from nose.tools import assert_equal, assert_true

from deploystream.apps.github import GithubProvider
from deploystream.providers.interfaces import (
        IPlanningProvider, is_implementation, IOAuthProvider)


@patch('deploystream.apps.github.github3')
def test_get_features(github3):
    mock_repo = Mock()
    mock_repo.has_issues = True

    issue1 = {
        'title': 'Hello',
        'id': '22',
        'number': '1',
        'pull_request': True,
        'assignee': Mock(login='txels'),
    }
    issue2 = {
        'title': 'Goodbye',
        'id': '25',
        'number': '2',
        'pull_request': False,
        'assignee': None,
    }
    mock_issue1, mock_issue2 = Mock(), Mock()
    mock_issue1.__dict__ = issue1
    mock_issue2.__dict__ = issue2
    mock_repo.iter_issues.return_value = [
        mock_issue1, mock_issue2
    ]
    github3.login.return_value = github3
    github3.iter_repos.return_value = [mock_repo]

    github_provider = GithubProvider('token')
    features = github_provider.get_features()

    assert_equal(len(features), 2)
    assert_equal(features[0]['id'], '1')
    assert_equal(features[0]['type'], 'PR')
    assert_equal(features[0]['owner'], 'txels')
    assert_equal(features[1]['id'], '2')
    assert_equal(features[1]['type'], 'story')
    assert_equal(features[1]['owner'], '')


@patch('deploystream.apps.github.github3')
def test_implements_expected_interfaces(_):
    assert_true(is_implementation(GithubProvider('token'), IPlanningProvider))
    assert_true(is_implementation(GithubProvider('token'), IOAuthProvider))
