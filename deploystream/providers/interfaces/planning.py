from zope import interface


class IPlanningProvider(interface.Interface):

    name = interface.Attribute(
                "The name the provider will be referred to in configs etc.")
    oauth_token_required = interface.Attribute(
                "If an oauth token is required, the name of it as defined by "
                "the oauth provider.")

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
