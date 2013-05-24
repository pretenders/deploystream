from nose.tools import assert_equals

from deploystream.apps.feature.models import Feature, Branch


def test_feature_branches():
    f = Feature(provider=None, project=None, id=None, title=None)
    for branch_name, parent_name in [('alex', 'master'), ('master', None),
                                     ('something', 'alex'), ('sthg2', 'alex')]:
        b = Branch("repo1", branch_name, "commit", parent_name, "test")
        f.add_branch(b)

    f.create_hierarchy_trees()
    assert_equals(b.as_tree_string(),
        "- master\n"
        "    - alex\n"
        "        - something\n"
        "        - sthg2\n"
    )
