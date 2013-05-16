from nose.tools import assert_equals

from deploystream.apps.feature.models import HierarchyNode, RootHierarchyNode


def test_hierarchy_tree_simple_case():
    repo = 'r1'
    root_node = RootHierarchyNode(repo=repo)
    for branch, level in [
            ('master', 0),
            ('develop', 1),
            ('story/1', 2),
            ('dev/1/alex', 3),
        ]:
        root_node.add_node(level=level, repo=repo, branch=branch)

    assert_equals(root_node.as_tree_string(),
        "- master\n"
        "    - develop\n"
        "        - story/1\n"
        "            - dev/1/alex\n"
    )


def test_hierarchy_tree_multiple_parent_options():
    """Test node assignment when there are multiple parents available.

    If there is more than one parental option available, the first node at
    the appropriate level should be selected as parent.
    """
    repo = 'r1'
    root_node = RootHierarchyNode(repo=repo)
    for branch, level in [
            ('master', 0),
            ('develop', 1),
            ('story/1', 2),
            ('story/1/alex', 2),
            ('dev/1/alex', 3),
        ]:
        root_node.add_node(level=level, repo=repo, branch=branch)

    assert_equals(root_node.as_tree_string(),
        "- master\n"
        "    - develop\n"
        "        - story/1\n"
        "            - dev/1/alex\n"
        "        - story/1/alex\n"
    )


def test_hierarchy_tree_nodes_find_correct_position():
    root_node = RootHierarchyNode(repo='r1')

    node_s1 = root_node.add_node(level=2, repo='r1', branch="story/1/alex")
    assert_equals(root_node.children, [node_s1])

    # Higher level nodes slot in and are considered parents of lower level
    # branches even if the levels are not sequential.
    node_master = node_s1.add_node(level=0, repo='r1', branch='master')

    assert_equals(node_master.children, [node_s1])
    assert_equals(node_s1.parent, node_master)
