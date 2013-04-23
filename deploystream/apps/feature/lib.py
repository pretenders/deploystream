from deploystream import app
from deploystream.providers.interfaces import (
    IBuildInfoProvider, IPlanningProvider, ISourceCodeControlProvider)
from .models import Branch, BuildInfo, Feature


def get_all_features(providers):
    """
    Collect all features from the configured providers.
    """
    all_features = []

    for provider in providers[IPlanningProvider]:
        print("INFO: getting features from {0}".format(provider.name))
        for feature in provider.get_features():
            print("INFO: found {0}".format(feature['title']))
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
    for provider in providers[IPlanningProvider]:
        feature = Feature(provider, None,
                          **provider.get_feature_info(feature_id))
        if feature:
            break

    if not feature:
        return

    # Then get any branch info from any source control providers
    for provider in providers[ISourceCodeControlProvider]:
        for branch_data in provider.get_repo_branches_involved(feature_id):
            feature.add_branch(Branch(*branch_data, provider=provider))

    # Use that branch info, along with configuration regexes to create a
    # hierarchy of the branches involved in the feature.
    feature.create_hierarchy_trees(app.config['HIERARCHY_REGEXES'])

    # Ask source control providers for merging information at this point.
    for provider in providers[ISourceCodeControlProvider]:
        for tree in feature.trees:
            provider.set_merged_status(tree.repo, tree)

    # Finally get any build information from any BuildInfo providers.
    for provider in providers[IBuildInfoProvider]:
        for branch in feature.branches:
            build_info = provider.get_build_information(
                branch.repo_name,
                branch.branch_name,
                branch.latest_commit
            )
            branch.build_info = BuildInfo(provider=provider, **build_info)
    return feature
