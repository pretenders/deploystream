from zope import interface


class IPlanningPlugin(interface.Interface):

    def get_features(**filters):
        """
        Get all features from this provider

        :param filters:
            Filtering parameters, such as owner, state, project...

        :returns:
            A list of features that follow the specified criteria
        """
        pass

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
                - description

            ``None`` otherwise
        """
        pass
