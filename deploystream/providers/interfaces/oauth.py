from deploystream.providers.interfaces.base import ProviderInterface


class IOAuthProvider(ProviderInterface):

    def start_token_processing():
        """Class method. Get a session token for OAuth of a service.

        The token should end up being stored in the session.
        """
