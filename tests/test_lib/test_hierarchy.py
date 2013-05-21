from nose.tools import assert_equals

from deploystream.lib.hierarchy import match_with_levels, match_with_geneology
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


def test_geneology():
    regexes = ['^master$', '^develop$', '^story/{FEATURE_ID}$',
               '^story/{FEATURE_ID}/[a-z]*$',
               '^{PARENT}/[a-z]*$']

    branches = ['master', 'develop', 'story/12', 'story/12/alex',
                'story/12/bill',
                'story/12/bill/something']

    expected = [('master', None),
                ('develop', 'master'),
                ('story/12', 'develop'),
                ('story/12/alex', 'story/12'),
                ('story/12/bill', 'story/12'),
                ('story/12/bill/something', 'story/12/bill')]

    results = match_with_geneology(12, branches, regexes)
    assert_equals(results, expected)
