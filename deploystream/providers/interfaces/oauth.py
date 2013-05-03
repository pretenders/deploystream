from deploystream.providers.interfaces.base import ProviderInterface


class IOAuthProvider(ProviderInterface):

    def get_oauth_data():
        """Class method. Return a dict of items used for getting OAuth data.

        The dictionary should return values for at least::

            "request_token_url": "the URL for requesting new tokens"
            "access_token_url": "the URL for token exchange"
            "authorize_url": "the URL for authorization"

        The return value of this function will be passed into flask_oauth along
        with consumer key and secret. See the Flask-OAuth docs for more
        details http://pythonhosted.org/Flask-OAuth/
        """
