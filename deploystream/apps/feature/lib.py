from deploystream import app
from deploystream.providers import (
    PLANNING_PLUGINS, SOURCE_CODE_PLUGINS, CI_PLUGINS
)

from models import Feature, Branch, PlanningInfo, CIInfo


def get_feature_info(feature_id):
    feature = Feature(feature_id)
    # First get any feature info from any management providers
    for plugin in PLANNING_PLUGINS:
        feature.planning_info = PlanningInfo(
                                **plugin.get_feature_info(feature_id))

    # Then get any branch info from any source control providers
    for plugin in SOURCE_CODE_PLUGINS:
        for branch_data in plugin.get_repo_branches_involved(feature_id):
            feature.branches.append(Branch(*branch_data))

    # Use that branch info, along with configuration regexes to create a
    # hierarchy of the branches involved in the feature.
    feature.create_hierarchy_trees(app.config['HIERARCHY_REGEXES'])

    # Ask source control providers for merging information at this point.
    for plugin in SOURCE_CODE_PLUGINS:
        for tree in feature.trees:
            plugin.set_merged_status(tree.repo, tree)

    # Finally get any build information from any CI providers.
    for plugin in CI_PLUGINS:
        for branch in feature.branches:
            branch.ci_info = CIInfo(**plugin.get_build_information(
                                                    branch.repo_name,
                                                    branch.branch_name,
                                                    branch.latest_commit))
    return feature
