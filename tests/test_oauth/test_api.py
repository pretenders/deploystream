import json

from nose.tools import assert_equals

import deploystream


def test_list_oauths_available():
    client = deploystream.app.test_client()
    response = client.get('/oauth/')
    assert_equals(200, response.status_code)
    assert_equals(['github'], json.loads(response.data))
