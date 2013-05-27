from nose.tools import assert_items_equal

from deploystream.lib.hierarchy import match_with_genealogy


def test_genealogy():
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

    results = match_with_genealogy(12, branches, regexes)
    assert_items_equal(results, expected)


def test_genealogy_unordered_list():
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

    results = match_with_genealogy(12, branches, regexes)
    results.sort()
    assert_items_equal(results, expected)


def test_genealogy_missing_steps():
    regexes = ['master', 'develop', 'story/{FEATURE_ID}',
               'story/{FEATURE_ID}/[a-z]*',
               '{PARENT}/[a-z]*']

    branches = ['master',
                'story/12/bill']

    expected = [('master', None),
                ('story/12/bill', 'master')]

    results = match_with_genealogy(12, branches, regexes)
    assert_items_equal(results, expected)


def test_gets_underscores():
    regexes = [
        'master',
        'develop',
        'story/{FEATURE_ID}',
        'story/{FEATURE_ID}/[a-z_]*',
        '{PARENT}[/_][a-z]*',
        'dev/{FEATURE_ID}/[a-z]*',
        '{PARENT}[/_][a-z]*',
    ]

    branches = [
        'alex/19',
        'dev/70/alex',
        'dev/70/alex_hierarchy',
        'dev_alex',
        'develop',
        'master',
        'story/23/carles',
        'story/43/carles',
        'story/53/carles',
        'story/58/carles',
        'story/70/alex',
        'story/72/carles',
    ]
    expected = [
        ('master', None),
        ('develop', 'master'),
        ('story/70/alex', 'develop'),
        ('dev/70/alex', 'story/70/alex'),
        ('dev/70/alex_hierarchy', 'dev/70/alex'),
    ]

    results = match_with_genealogy(70, branches, regexes)
    assert_items_equal(results, expected)
