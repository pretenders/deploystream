def get_feature_info(feature_id, **kwargs):
    """
    :param feature_id:
        The identifier of a feature to be looked up.

    :param **kwargs:
        Additional configuration for the plugin. If this plugin was written
        by you then this will only be information you have added in the
        configuration of it. See :ref:`<configure_provider>` for more
        information about configuring plugins.

    :returns:
        If found, a dictionary containing keys for at least:
            - title
            - id
            - url
            - feature_type
            - owner

        ``None`` otherwise
    """
    pass


def default_config():
    """
    Optional function. Return the default configuration for the plugin.

    The return value from this function will be passed in to calls of
    ``get_feature_info`` by default. These can be overwritten by configuration.

    :returns:
        A dictionary containing only string keys and values.
    """
    pass
