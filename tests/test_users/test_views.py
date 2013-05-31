from nose.tools import assert_true, assert_equal, assert_false

import deploystream


class TestRegister(object):

    def setup(self):
        self.client = deploystream.app.test_client()

    def send_register_post(self, email, password='123',
                           confirm_password='123'):
        return self.client.post('/users/register',
            {'name': 'testuser', 'email': email, 'password': password,
             'confirm': confirm_password, 'accept_tos': True})

    def test_adds_user_to_the_database(self):
        response = self.send_register_post('test@test.com')

        assert_equal(response.status_code, 302)
        assert_true("/users/me" in response.location)
        assert_false("NEED TO CHECK IN THE DB FOR THE OBJECT HERE")

    def test_incomplete_when_email_already_exists(self):
        response = self.send_register_post('test@test.com')
        assert_true("/users/me" in response.location)

        response = self.send_register_post('test@test.com')
        assert_true("This user already exists" in response.data)

    def test_incomplete_when_passwords_do_not_match(self):
        response = self.send_register_post('test@test.com', '123', '111')

        assert_true("Passwords must match" in response.data)


class TestLogin(object):

    def test_login_to_existing_user_account():
        raise NotImplementedError()
