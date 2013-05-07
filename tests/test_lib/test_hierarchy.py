from deploystream.lib.hierarchy import match_with_levels

from nose.tools import assert_equals


def test_match_with_levels():
    "Test that we get back what we'd expect when matching branches"
    branches_results = [
        ('master', 0),
        ('develop', 1),
        ('story/23', 2),
        ('dev/23/alex', 3),
        ('dev/23/carles', 3),

        ('story/45/alex', None),
        ('dev/99/carles', None),
    ]
    regexes = [
        'master',
        'develop',
        'story/{FEATURE_ID}(/[a-z]*)?',
        'dev/{FEATURE_ID}/[a-z]*',
        '[a-zA-Z]*/{FEATURE_ID}/[a-zA-Z]*'
    ]

    for branch, expected in branches_results:
        result = match_with_levels('23', branch, regexes)
        assert_equals(result, expected)
