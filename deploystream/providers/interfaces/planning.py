from zope import interface


class IPlanningPlugin(interface.Interface):

    def get_feature_info(feature_id):
        """
        :param feature_id:
            The identifier of a feature to be looked up.

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
