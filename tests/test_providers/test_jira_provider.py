from nose.tools import assert_true

from deploystream.providers.jira import JiraProvider
from deploystream.providers.interfaces import (
        IPlanningProvider, is_implementation)


def test_is_planning_provider():
    assert_true(is_implementation(JiraProvider, IPlanningProvider))
