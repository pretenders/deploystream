from mock import Mock, patch
from nose.tools import assert_equal, assert_true

from deploystream.providers.github import GithubProvider
from deploystream.providers.interfaces import (
        IPlanningProvider, IOAuthProvider, is_implementation)
from tests import DEFAULT_HIERARCHY_REGEXES


def mock_github3(github3):
    mock_repo = Mock()
    mock_repo.has_issues = True
    mock_repo.name = 'repo_1'
    mock_repo.iter_commits.return_value = [Mock(sha="CoMmItHaSh-MaStEr")]

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

    branch1 = {
        'name': 'master',
        'commit': Mock(sha='CoMmItHaSh-MaStEr'),
    }
    branch2 = {
        'name': 'story/5/alex',
        'commit': Mock(sha='CoMmItHaSh-5'),
    }
    branch3 = {
        'name': 'story/23/alex',
        'commit': Mock(sha='CoMmItHaSh-23'),
    }
    mock_branch1, mock_branch2, mock_branch3 = Mock(), Mock(), Mock()
    mock_branch1.__dict__ = branch1
    mock_branch2.__dict__ = branch2
    mock_branch3.__dict__ = branch3
    mock_repo.iter_branches.return_value = [
        mock_branch1, mock_branch2, mock_branch3
    ]
    github3.login.return_value = github3
    github3.iter_repos.return_value = [mock_repo]


@patch('deploystream.providers.github.github3')
def test_get_features(github3):
    mock_github3(github3)
    github_provider = GithubProvider('token')
    features = github_provider.get_features()

    assert_equal(len(features), 2)
    assert_equal(features[0]['id'], '1')
    assert_equal(features[0]['type'], 'PR')
    assert_equal(features[0]['owner'], 'txels')
    assert_equal(features[1]['id'], '2')
    assert_equal(features[1]['type'], 'story')
    assert_equal(features[1]['owner'], '')


@patch('deploystream.providers.github.github3')
def test_implements_expected_interfaces(_):
    assert_true(is_implementation(GithubProvider('token'), IPlanningProvider))
    assert_true(is_implementation(GithubProvider('token'), IOAuthProvider))


@patch('deploystream.providers.github.github3')
def test_get_repo_branches_involved(github3):
    mock_github3(github3)
    github_provider = GithubProvider('token')
    branches = github_provider.get_repo_branches_involved("5",
                                                    DEFAULT_HIERARCHY_REGEXES)
    assert_equal(2, len(branches))
    assert_true({
        "repo_name": "repo_1",
        "branch_name": "master",
        "parent_branch_name": None,
        "latest_commit": 'CoMmItHaSh-MaStEr',
        "has_parent": None,
        "in_parent": None,
    } in branches)
    assert_true({
        "repo_name": "repo_1",
        "branch_name": "story/5/alex",
        "parent_branch_name": "master",
        "latest_commit": "CoMmItHaSh-5",
        "has_parent": True,
        "in_parent": False,
    } in branches)
