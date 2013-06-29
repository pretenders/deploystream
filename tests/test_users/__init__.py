import os

import deploystream
from deploystream.apps.users.models import User

MAIN_USER_ID = None


def setup():
    global MAIN_USER_ID
    if os.path.exists(deploystream.app.config['TEST_DB_LOCATION']):
        os.remove(deploystream.app.config['TEST_DB_LOCATION'])
    deploystream.db.create_all()
    user = User.create_user("main_test_user", "main@test.com", "123")
    MAIN_USER_ID = user.id


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
