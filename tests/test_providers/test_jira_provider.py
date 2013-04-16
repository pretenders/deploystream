from nose.tools import assert_true

from deploystream.providers.jira import JiraProvider
from deploystream.providers.interfaces import (
        IPlanningProvider, is_implementation)

ISSUES = []


def test_is_planning_provider():
    assert_true(is_implementation(JiraProvider, IPlanningProvider))


def test_jira_provider_features():
    """
    Patch requests to use the response in ISSUES.

    Check that we get expected data out from ``get_features`` for jira.
    """
    raise Exception("Not implemented yet")
