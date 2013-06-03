from flask import session
from mock import patch, Mock
from nose.tools import assert_equal, assert_true

import deploystream
from deploystream.apps import oauth


class PlanningProvider(object):
    name = 'prov101'
    oauth_token_name = 'prov101'

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

    @classmethod
    def start_token_processing(cls):
        oauth.set_token(session, cls.name, 'some-token')

DummyOAuth = Mock()


class TestAutoGetToken(object):

    def setUp(self):
        deploystream.app.config['TESTING'] = True
        deploystream.app.config['oauth']['api'] = ("some-key", "some-secret")
        deploystream.app.config['OAuthProviders'] = {}
        deploystream.app.config['USER_SPECIFIC_INFO'] = {
            'provider_config': [
                ('prov101', {}),
                ('api', {}),
            ]
        }
        self.client = deploystream.app.test_client()

    @patch("deploystream.providers.ALL_PROVIDER_CLASSES",
           {'prov101': PlanningProvider})
    def test_providers_requiring_oauth_token_force_redirect(self):
        "Test that the site attempts to get tokens for providers"
        response = self.client.get('/features/FT101')
        assert_equal(response.status_code, 302)
        assert_true("http://auth_url" in response.location)

    @patch("deploystream.providers.ALL_PROVIDER_CLASSES",
           {'prov101': PlanningProvider})
    def test_if_got_token_no_redirect_required(self):
        "Test that the site doesn't go to get the token if it already has it"
        with self.client.session_transaction() as sess:
            oauth.set_token(
                sess, PlanningProvider.oauth_token_name, "FRED")
        response = self.client.get('/features/FT101')
        assert_equal(response.status_code, 200)
        assert_true("Amazing feature" in response.data)
