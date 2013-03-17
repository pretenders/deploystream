from deploystream import app
from deploystream.providers.interfaces import (
    is_planning_provider, is_build_info_provider, is_source_code_provider)
from .models import Branch, BuildInfo, Feature


def get_all_features(providers):
    """
    Collect all features from the configured providers.
    """
    all_features = []

    for provider in providers:
        if is_planning_provider(provider):
            for feature in provider.get_features():
                all_features.append(Feature(provider, **feature))

    return all_features


def get_feature_info(feature_id, providers):
    """
    Get the information associated with the given feature from the providers
    given.

    ``planning``, ``source_code`` and ``build_info`` are relevant providers to
    be called.
    """
    # TODO: since features may come from various origins, we need
    # at this stage to either use a feature id that is a string such as
    # "github:pretenders/deploystream:15" or to have additional arguments
    # for provider and project. In any case we probably need providers to
    # have an identifying string such as "github", "jira", "sprintly"...

    # First get feature info from the management providers
    # This needs rewriting according to previous paragraph. For now:
    # Only one management provider should know about this feature,
    # so we stop on first success
    feature = None
    for provider in providers:
        if is_planning_provider(provider):
            feature = Feature(provider, None,
                              **provider.get_feature_info(feature_id))
            if feature:
                break

    if not feature:
        return

    # Then get any branch info from any source control providers
    for provider in providers:
        if is_source_code_provider(provider):
            for branch_data in provider.get_repo_branches_involved(feature_id):
                feature.add_branch(Branch(*branch_data, provider=provider))

    # Use that branch info, along with configuration regexes to create a
    # hierarchy of the branches involved in the feature.
    feature.create_hierarchy_trees(app.config['HIERARCHY_REGEXES'])

    # Ask source control providers for merging information at this point.
    for provider in providers:
        if is_source_code_provider(provider):
            for tree in feature.trees:
                provider.set_merged_status(tree.repo, tree)

    # Finally get any build information from any BuildInfo providers.
    for provider in providers:
        if is_build_info_provider(provider):
            for branch in feature.branches:
                branch.build_info = BuildInfo(
                                        provider=provider,
                                        **provider.get_build_information(
                                            branch.repo_name,
                                            branch.branch_name,
                                            branch.latest_commit)
                                        )
    return feature
