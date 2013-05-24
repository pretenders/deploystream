from mock import Mock, patch
from nose.tools import assert_equal, assert_true

from deploystream.providers.github import GithubProvider
from deploystream.providers.interfaces import (
        IPlanningProvider, IOAuthProvider, is_implementation)
from tests import DEFAULT_HIERARCHY_REGEXES
from deploystream import app


def test_get_repo_branches_involved():
    "Test ``get_repo_branches_involved`` using ``pretenders/dummyrepo`` repo."
    github_provider = GithubProvider(
        token=None,
        username=app.config['GITHUB_CONFIG']['username'],
        password=app.config['GITHUB_CONFIG']['password'],
        repositories=[('pretenders', 'dummyrepo')]
    )
    branches = github_provider.get_repo_branches_involved(101,
        hierarchy_regexes=DEFAULT_HIERARCHY_REGEXES)

    assert_equal(2, len(branches))
    assert_true({
        "repo_name": "dummyrepo",
        "branch_name": "master",
        "latest_commit": '0f6eefefc14f362a2c6f804df69aa83bac48c20b',
        "parent_branch_name": None} in branches)
    assert_true({
        "repo_name": "dummyrepo",
        "branch_name": "story/101/fred",
        "latest_commit": "0f6eefefc14f362a2c6f804df69aa83bac48c20b",
        "parent_branch_name": "master"} in branches)
