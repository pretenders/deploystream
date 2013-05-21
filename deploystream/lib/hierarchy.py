from collections import defaultdict
import re


def create_single_regex(feature_id, hierarchical_regexes):
    """
    Create a single regex to be used to find which level a branch is on.

    :param feature_id:
        The id of the feature. This is substituted into the
        ``hierarchical_regexes`` if they use {FEATURE_ID} anywhere.

    :param hierarchical_regexes:
        A list of regexes to be joined into one single regex.

    :returns:
        A single regex for easier matching.
    """
    subs = []
    for index, regex in enumerate(hierarchical_regexes):
        subs.append("(?P<level_{0}>^{1}$)".format(index, regex))
    full_regex = "|".join(subs)
    full_regex = full_regex.format(FEATURE_ID=feature_id)
    return full_regex


def match_with_levels(feature_id, branch, hierarchical_regexes):
    """
    Filter and return the branches in appropriate levels.

    :param feature_id:
        The feature to filter the branch names on.

    :param branches:
        A list of branch names to filter.

    :param hierarchical_regexes:
        A list of regexes assumed to be in descending order of branch status.

    :returns:
        The positional index that the branch should be found in. Or None if it
        does not match.
    """
    regex = create_single_regex(feature_id, hierarchical_regexes)

    result = re.match(regex, branch)
    if not result:
        return None

    for level, match in result.groupdict().items():
        if match:
            index = int(level.split('level_')[1])
            return index


def match_with_geneology(feature_id, branches, hierarchical_regexes):
    matched_branches = defaultdict(list)
    hierarchy = []
    for index, regex in enumerate(hierarchical_regexes):
        print "- REGEX:", regex, "INDEX:", index
        try:
            parent_regex = hierarchical_regexes[max(index - 1, 0)]
        except IndexError:
            parent_regex = None

        possible_parents = matched_branches[index - 1]
        fake_parent = False
        if not possible_parents:
            fake_parent = True
            possible_parents = [parent_regex]

        for branch in branches[:]:
            print "  - BRANCH:", branch
            for parent in possible_parents:
                print "    - PARENT?:", parent

                full_regex = regex.format(FEATURE_ID=feature_id,
                                          PARENT=parent)
                print "    - REGEX:", full_regex, "BRANCH:", branch
                result = re.match(full_regex, branch)
                if result:
                    print "  ---MATCHED---"
                    matched_branches[index].append(branch)
                    branches.remove(branch)
                    if fake_parent:
                        parent = None
                    hierarchy.append((branch, parent))
                    break
                else:
                    print "  ---FAILED---"

    print "hierarchy", hierarchy
    return hierarchy

