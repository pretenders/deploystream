from deploystream import app
from deploystream.providers import (
    PLANNING_PLUGINS, SOURCE_CODE_PLUGINS, BUILD_INFO_PLUGINS
)

from .models import Branch, BuildInfo, Feature


def get_all_features():
    """
    Collect all features from the configured providers.
    """
    all_features = []

    for provider in PLANNING_PLUGINS:
        for feature in provider.get_features():
            all_features.append(Feature(provider, **feature))

    return all_features


def get_feature_info(feature_id):
    # TODO: since features may come from various origins, we need
    # at this stage to either use a feature id that is a string such as
    # "github:pretenders/deploystream:15" or to have additional arguments
    # for plugin and project. In any case we probably need providers to
    # have an identifying string such as "github", "jira", "sprintly"...

    # First get feature info from the management providers
    # This needs rewriting according to previous paragraph. For now:
    # Only one management provider should know about this feature,
    # so we stop on first success
    for plugin in PLANNING_PLUGINS:
        feature = Feature(plugin, None, **plugin.get_feature_info(feature_id))
        if feature:
            break

    # Then get any branch info from any source control providers
    for plugin in SOURCE_CODE_PLUGINS:
        for branch_data in plugin.get_repo_branches_involved(feature_id):
            feature.add_branch(Branch(*branch_data, plugin=plugin))

    # Use that branch info, along with configuration regexes to create a
    # hierarchy of the branches involved in the feature.
    feature.create_hierarchy_trees(app.config['HIERARCHY_REGEXES'])

    # Ask source control providers for merging information at this point.
    for plugin in SOURCE_CODE_PLUGINS:
        for tree in feature.trees:
            plugin.set_merged_status(tree.repo, tree)

    # Finally get any build information from any BuildInfo providers.
    for plugin in BUILD_INFO_PLUGINS:
        for branch in feature.branches:
            branch.build_info = BuildInfo(plugin=plugin,
                                          **plugin.get_build_information(
                                              branch.repo_name,
                                              branch.branch_name,
                                              branch.latest_commit)
                                          )
    return feature
