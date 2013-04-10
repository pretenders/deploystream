from mock import patch, Mock
from nose.tools import assert_equal, assert_true

import deploystream
from deploystream.apps import oauth
from deploystream.apps.oauth.views import configure_oauth_routes


class OAuthProvider(object):
    name = 'api'
    oauth_token_required = None

    @classmethod
    def get_oauth_data(cls):
        return {
            'base_url': 'https://api.github.com/',
            'request_token_url': None,
            'access_token_url': 'http://access_token_url',
            'authorize_url': 'http://auth_url',
            'request_token_params': {
                'scope': 'user,repo'
            },
        }


class PlanningProvider(object):
    name = 'prov101'
    oauth_token_required = 'api'

    def __init__(self, token):
        pass

    def get_features(self, **filters):
        return []

    def get_feature_info(self, feature_id, **kwargs):
        return {
            "title": "Amazing feature that will blow your mind",
            "id": feature_id,
            "url": "http://planning_site/{0}".format(feature_id),
            "feature_type": "story",
            "owner": "Bob",
            "description": "Too good for words..."
        }


DummyOAuth = Mock()


class TestAutoGetToken(object):

    def setUp(self):
        deploystream.app.config['TESTING'] = True
        deploystream.app.config['api_APP_ID'] = "some-key"
        deploystream.app.config['api_APP_SECRET'] = "some-secret"
        deploystream.app.config['USER_SPECIFIC_INFO'] = {
            'provider_config': [
                ('prov101', {}),
                ('api', {}),
            ]
        }
        self.client = deploystream.app.test_client()

    @patch("deploystream.providers.ALL_PROVIDER_CLASSES",
           {'prov101': PlanningProvider,
            'api': OAuthProvider})
    def test_providers_requiring_oauth_token_force_redirect(self):
        "Test that the site attempts to get tokens for providers"

        configure_oauth_routes(deploystream.providers.ALL_PROVIDER_CLASSES)

        response = self.client.get('/features/FT101')
        assert_equal(response.status_code, 302)
        assert_true("http://auth_url" in response.location)

    @patch("deploystream.providers.ALL_PROVIDER_CLASSES",
           {'prov101': PlanningProvider,
            'api': OAuthProvider})
    def test_if_got_token_no_redirect_required(self):
        "Test that the site doesn't go to get the token if it already has it"
        with self.client.session_transaction() as sess:
            oauth.set_token(
                sess, PlanningProvider.oauth_token_required, "FRED")
        response = self.client.get('/features/FT101')
        assert_equal(response.status_code, 200)
        assert_true("Amazing feature" in response.data)
