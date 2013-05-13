from nose.tools import assert_equals

from deploystream.apps.feature.models import HierarchyNode


def test_hierarchy_tree_behaviour():
    root_node = HierarchyNode(level=-1, repo='r1')

    node_s1 = root_node.add_node(level=2, repo='r1', branch="story/1/alex")
    assert_equals(root_node.children, [node_s1])

    # Higher level nodes slot in and are considered parents of lower level
    # branches even if the levels are not sequential.
    node_master = node_s1.add_node(level=0, repo='r1', branch='master')

    assert_equals(node_master.children, [node_s1])
    assert_equals(node_s1.parent, node_master)

    # When a missing level is added, children and parents of the branches below
    # and above are corrected accordingly.
    node_devel = node_s1.add_node(level=1, repo='r1', branch="develop")

    assert_equals(node_devel.children, [node_s1])
    assert_equals(node_s1.parent, node_devel)
    assert_equals(node_master.children, [node_devel])
    assert_equals(node_devel.parent, node_master)

    node_s1b = node_devel.add_node(level=2, repo='r1', branch='story/1')

    assert_equals(node_devel.children, [node_s1, node_s1b])
    assert_equals(node_s1.parent, node_devel)
    assert_equals(node_s1b.parent, node_devel)
    assert_equals(node_master.children, [node_devel])
    assert_equals(node_devel.parent, node_master)

    # A level can have more than one child.
    node_d1 = node_s1b.add_node(level=3, repo='r1', branch='dev/1/fred')

    assert_equals(node_d1.parent, node_s1b)
    assert_equals(node_s1b.children, [node_d1])
    assert_equals(node_s1.children, [])

    node_d2 = node_s1b.add_node(level=3, repo='r1', branch='dev/1/alex')

    assert_equals(node_d2.parent, node_s1b)
    assert_equals(node_s1b.children, [node_d1, node_d2])

    # Check the tree looks correct
    print root_node.as_tree_string()
    assert_equals(root_node.as_tree_string(),
        "- master\n"
        "    - develop\n"
        "        - story/1/alex\n"
        "        - story/1\n"
        "            - dev/1/fred\n"
        "            - dev/1/alex\n"
    )
