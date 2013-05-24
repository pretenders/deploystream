from nose.tools import assert_items_equal

from deploystream.lib.hierarchy import match_with_geneology


def test_geneology():
    regexes = ['master', 'develop', 'story/{FEATURE_ID}',
               'story/{FEATURE_ID}/[a-z]*',
               '{PARENT}/[a-z]*']

    branches = ['master', 'develop', 'story/12', 'story/12/alex',
                'story/12/bill',
                'story/12/bill/something',
                'story/223/bill']

    expected = [('master', None),
                ('develop', 'master'),
                ('story/12', 'develop'),
                ('story/12/alex', 'story/12'),
                ('story/12/bill', 'story/12'),
                ('story/12/bill/something', 'story/12/bill')]

    results = match_with_geneology(12, branches, regexes)
    assert_items_equal(results, expected)


def test_geneology_unordered_list():
    regexes = ['master', 'develop', 'story/{FEATURE_ID}',
               'story/{FEATURE_ID}/[a-z]*',
               '{PARENT}/[a-z]*']

    branches = ['story/12/bill', 'master',  'story/12/bill/something',
                'story/12', 'story/12/alex', 'develop']

    expected = [('master', None),
                ('develop', 'master'),
                ('story/12', 'develop'),
                ('story/12/alex', 'story/12'),
                ('story/12/bill', 'story/12'),
                ('story/12/bill/something', 'story/12/bill')]

    results = match_with_geneology(12, branches, regexes)
    results.sort()
    assert_items_equal(results, expected)


def test_geneology_missing_steps():
    regexes = ['master', 'develop', 'story/{FEATURE_ID}',
               'story/{FEATURE_ID}/[a-z]*',
               '{PARENT}/[a-z]*']

    branches = ['master',
                'story/12/bill']

    expected = [('master', None),
                ('story/12/bill', 'master')]

    results = match_with_geneology(12, branches, regexes)
    assert_items_equal(results, expected)
