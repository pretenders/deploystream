from zope import interface


class ProviderInterface(interface.Interface):

    name = interface.Attribute(
                "The name the provider will be referred to in configs etc.")
    oauth_token_required = interface.Attribute(
                "If an oauth token is required, the name of it as defined by "
                "the oauth provider.")
