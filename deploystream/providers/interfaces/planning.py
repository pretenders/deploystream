from zope.interface import Interface


class IPlanningPlugin(Interface):

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
