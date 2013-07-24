import json

from nose.tools import assert_equal, assert_false, assert_true

from tests import test_users


class TestUserDetails(test_users.UserTestMixin):

    def test_can_get_details_about_myself(self):
        self.send_login_post('main_test_user', '123')

        response = self.client.get('/api/users/{0}'.format(
                        test_users.MAIN_USER_ID))

        assert_equal(response.status_code, 200)
        json_data = json.loads(response.data)
        assert_equal(json_data['username'], 'main_test_user')
        assert_false('password' in json_data)

    def test_permission_denied_for_other_users(self):
        self.send_login_post('main_test_user', '123')
        response = self.client.get('/api/users/100')
        assert_equal(response.status_code, 401)

    def test_permission_denied_when_listing_users(self):
        self.send_login_post('main_test_user', '123')
        response = self.client.get('/api/users')
        assert_equal(response.status_code, 401)

    def test_get_profile_redirects_to_correct_api(self):
        self.send_login_post('main_test_user', '123')

        response = self.client.get('/users/me/')

        assert_equal(response.status_code, 302)
        assert_true("/api/users/{0}".format(test_users.MAIN_USER_ID)
                        in response.location)
