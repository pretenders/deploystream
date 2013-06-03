from mock import Mock, patch
from nose.tools import assert_true, assert_equal

import deploystream
from deploystream.apps.users.models import User


class UserTestMixin(object):

    def setup(self):
        self.client = deploystream.app.test_client()

    def send_register_post(self, username, email="a@a.com", password='123',
                           confirm_password='123'):
        return self.client.post('/users/register/',
            data={'username': username, 'email': email, 'password': password,
                  'confirm': confirm_password, 'accept_tos': True})

    def send_login_post(self, username, password):
        return self.client.post('/users/login/',
            data={'username': username, 'password': password})


class TestRegister(UserTestMixin):

    def test_adds_user_to_the_database(self):
        response = self.send_register_post(
            email='test@test.com', username='test1')
        assert_equal(response.status_code, 302)
        assert_true("/users/me" in response.location)
        u = User.query.filter_by(username="test1").first()
        assert_equal(u.email, 'test@test.com')

    def test_incomplete_when_username_already_exists(self):
        response = self.send_register_post(username='fred')
        assert_true("/users/me" in response.location)

        response = self.send_register_post(username='fred')
        assert_true("This username is already in use." in response.data)

    def test_incomplete_when_passwords_do_not_match(self):
        response = self.send_register_post("james",
            'test3@test.com', '123', '111')

        assert_true("Passwords must match" in response.data)


class TestLogin(UserTestMixin):

    def test_login_to_existing_user_account(self):
        response = self.send_register_post('phil', 'test_login@test.com')
        self.client.get('/logout')
        response = self.send_login_post('phil', '123')
        assert_equal(response.status_code, 302)
        assert_true("/users/me" in response.location)


class TestProfile(UserTestMixin):

    # TODO:
    #    This needs a fix. We need to get the ``resp`` content back in to the
    #    oauth_authorized view. It'll almost certainly involve more involved
    #    mocking of the underlying flask_oauth class so that we can pass it in.

    def mock_github_oauth(self):
        def fake_authorize_call(callback):
            # Fakes an authorize call by calling the callback with some fake
            # github data.
            resp = self.client.get(
                "github-oauth-authorized/?islogin=True&oauth_name=github",
                data={'access_token': '999'})
            return resp

        github_mock = Mock()
        github_mock.authorize = fake_authorize_call
        github_mock.get.return_value = {'id': '101', 'login': 'fred'}
        return github_mock

    def test_add_oauth_link_to_account(self):
        deploystream.apps.oauth.views.OAUTH_OBJECTS = {
            'github': self.mock_github_oauth()
        }
        # Register
        self.send_register_post('jeff')
        # Link to a github account
        self.client.get('/oauth/github')
        u = User.query.filter_by(username="jeff").first()
        assert_equal(1, len(u.oauth_keys))
        assert_equal(u.auth_keys[0].service, 'github')
        # Need to mock the github provider and call ``oauth_authorized``
