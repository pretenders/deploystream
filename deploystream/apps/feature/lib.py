#!/usr/bin/env python
#-*- coding: utf-8 -*-

from deploystream import app
from deploystream.exceptions import UnknownProviderException
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
            print("INFO: found " + feature['title'])
            all_features.append(Feature(provider, **feature))

    return all_features


def get_feature_info(feature_provider, feature_id, providers):
    """
    Get the information associated with the given feature from the providers
    given.

    :param feature_provider:
        The name of the planning provider who knows of this feature.

    :param feature_id:
        The planning-provider specific id for the feature.

    :param providers:
        A dictionary of all providers.

    :raises:
        UnknownProviderException - if no such name found.
    """
    if feature_provider not in providers:
        raise UnknownProviderException(feature_provider)

    # First get feature info from the management provider
    planning_provider = providers[feature_provider]

    feature = Feature(planning_provider,
                      **planning_provider.get_feature_info(feature_id))
    print providers[ISourceCodeControlProvider]
    # Then get any branch info from any source control providers
    for provider in providers[ISourceCodeControlProvider]:
        print provider
        for branch_data in provider.get_repo_branches_involved(
            feature_id, app.config['HIERARCHY_REGEXES']):
            print branch_data
            feature.add_branch(Branch(provider=provider, **branch_data))

    feature.create_hierarchy_trees()

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
