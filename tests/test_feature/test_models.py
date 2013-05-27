from nose.tools import assert_equals

from deploystream.apps.feature.models import Feature, Branch


def test_feature_branches():
    f = Feature(provider=None, project=None, id=None, title=None)
    for branch_name, parent_name in [('alex', 'master'), ('master', None),
                                     ('something', 'alex'), ('sthg2', 'alex')]:
        b = Branch(provider="test",
            repository="repo1",
            name=branch_name,
            commit_id="commit",
            parent_name=parent_name
        )

        f.add_branch(b)

    f.create_hierarchy_trees()
    assert_equals(b.as_tree_string(),
        "- master\n"
        "    - alex\n"
        "        - something\n"
        "        - sthg2\n"
    )
