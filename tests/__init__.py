import os
import os.path

import deploystream
from deploystream.apps.users.models import User


TEST_DATA = os.path.join(os.path.dirname(__file__), 'data')
MAIN_USER_ID = None


def load_fixture(filename):
    with file(os.path.join(TEST_DATA, filename)) as f:
        contents = f.read()
    return contents


def setup():
    recreate_db()


def recreate_db():
    if os.path.exists(deploystream.app.config['TEST_DB_LOCATION']):
        os.remove(deploystream.app.config['TEST_DB_LOCATION'])
    deploystream.db.create_all()


def create_main_user():
    global MAIN_USER_ID
    user = User.create_user("main_test_user", "main@test.com", "123")
    MAIN_USER_ID = user.id
