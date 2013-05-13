from nose.tools import assert_equals

from deploystream.lib.hierarchy import match_with_levels
from tests import DEFAULT_HIERARCHY_REGEXES


def test_match_with_levels():
    "Test that we get back what we'd expect when matching branches"
    branches_results = [
        ('master', 0),
        ('develop', 1),
        ('story/23', 2),
        ('dev/23/alex', 3),
        ('dev/23/carles', 3),

        ('somestory/234/carles', None),
        ('story/234/carles', None),
        ('story/45/alex', None),
        ('dev/99/carles', None),
    ]

    for branch, expected in branches_results:
        result = match_with_levels('23', branch, DEFAULT_HIERARCHY_REGEXES)
        assert_equals(result, expected)
