import os

import deploystream


def setup():
    if os.path.exists(deploystream.app.config['TEST_DB_LOCATION']):
        os.remove(deploystream.app.config['TEST_DB_LOCATION'])
    deploystream.db.create_all()
