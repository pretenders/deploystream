from collections import defaultdict
import re


def match_with_geneology(feature_id, branches, hierarchical_regexes):
    """
    Filter and return the branches in order with parents attached.

    :param feature_id:
        The feature to filter the branch names on.

    :param branches:
        A list of branch names to filter.

    :param hierarchical_regexes:
        A list of regexes assumed to be in descending order of branch status.

    :returns:
        A list of tuples containing:
            - Branch name
            - Parent name

    Go through the hierarchy regexes in sequence.
    Attempt to match each one against all the branches. When a match occurs
    remove the branch from the list to be matched against and continue.
    Also add parental information as we go along.
    """
    matched_branches = defaultdict(list)
    hierarchy = []
    for index, regex in enumerate(hierarchical_regexes):
        try:
            parent_regex = hierarchical_regexes[max(index - 1, 0)]
        except IndexError:
            parent_regex = None

        # Find the possible parents for any branches found at this level.
        # Simply look at the level above, and if not there then keep going back
        parent_index = index - 1
        fake_parent = False
        possible_parents = matched_branches[parent_index]
        while not possible_parents:
            parent_index -= 1
            if parent_index < 0:
                fake_parent = True
                possible_parents = [parent_regex]
                break
            possible_parents = matched_branches[parent_index]

        # Look through all the branches (that are left to look at) and see
        # if any match this regex.
        for branch in branches[:]:
            for parent in possible_parents:
                full_regex = regex.format(FEATURE_ID=feature_id,
                                          PARENT=parent)
                result = re.match("^{0}$".format(full_regex), branch)
                if result:
                    matched_branches[index].append(branch)
                    branches.remove(branch)
                    if fake_parent:
                        parent = None
                    hierarchy.append((branch, parent))
                    break

    return hierarchy
