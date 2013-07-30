import os
import os.path

import deploystream


TEST_DATA = os.path.join(os.path.dirname(__file__), 'data')


def load_fixture(filename):
    with file(os.path.join(TEST_DATA, filename)) as f:
        contents = f.read()
    return contents


def setup():
    if os.path.exists(deploystream.app.config['TEST_DB_LOCATION']):
        os.remove(deploystream.app.config['TEST_DB_LOCATION'])
    deploystream.db.create_all()
