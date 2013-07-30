from nose.tools import assert_true, assert_equal

from deploystream.apps.users.models import User
from tests.test_users import UserTest


class TestRegister(UserTest):

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


class TestLogin(UserTest):

    def test_login_to_existing_user_account(self):
        response = self.send_register_post('phil', 'test_login@test.com')
        self.client.get('/logout')
        response = self.send_login_post('phil', '123')
        assert_equal(response.status_code, 302)
        assert_true("/#/profile" in response.location)
