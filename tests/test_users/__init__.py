import deploystream

import tests


def setup():
    tests.recreate_db()
    tests.create_main_user()


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
