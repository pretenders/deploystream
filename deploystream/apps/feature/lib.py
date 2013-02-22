def get_feature_info(feature_id):
    # First get any feature info from any management providers

    # Then get any branch info from any source control providers

    # Use that branch info, along with configuration regexes to create a
    # hierarchy of the branches involved in the feature.

    # Ask source control providers for merging information at this point.

    # Finally get any build information from any CI providers.
    pass
