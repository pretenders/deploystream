from mock import MagicMock, Mock, patch
from nose.tools import assert_equal

from deploystream.providers.sprintly import SprintlyProvider
from supermutes.dot import dotify


# Real data sample from sprint.ly, anonimised
ISSUES = [dotify(x) for x in [
 {u'assigned_to': None,
  u'created_at': u'2013-02-13T10:28:30+00:00',
  u'created_by': {u'created_at': u'2013-02-05T14:53:33+00:00',
                  u'email': u'someone@example.com',
                  u'first_name': u'Some',
                  u'id': 11037,
                  u'last_login': u'2013-03-22T13:35:24+00:00',
                  u'last_name': u'One'},
  u'description': u'see http://marteau.readthedocs.org/en/latest/',
  u'email': {u'discussion': u'discussion-290500@items.sprint.ly',
             u'files': u'files-290500@items.sprint.ly'},
  u'last_modified': u'2013-03-30T05:52:09+00:00',
  u'number': 873,
  u'product': {u'archived': 0, u'id': 9134, u'name': u'RBX'},
  u'progress': {u'started_at': u'2013-02-19T12:55:14+00:00'},
  u'score': u'XL',
  u'short_url': u'http://sprint.ly/i/9134/873/',
  u'status': u'in-progress',
  u'tags': [u'adstats', u'sprint1'],
  u'title': u"As a developer, I want the real-time ad stats aggregation...",
  u'type': u'story',
  u'what': u'the real-time ad stats aggregation to be thoroughly load-tested',
  u'who': u'developer',
  u'why': u"it doesn't break when we go live with a big ad campaign"},
 {u'assigned_to': {u'created_at': u'2013-02-04T15:34:18+00:00',
                   u'email': u'someone@example.com',
                   u'first_name': u'Some',
                   u'id': 10999,
                   u'last_login': u'2013-03-07T11:01:14+00:00',
                   u'last_name': u'One'},
  u'created_at': u'2013-03-08T08:50:55+00:00',
  u'created_by': {u'created_at': u'2013-02-04T15:34:18+00:00',
                  u'email': u'someone@example.com',
                  u'first_name': u'Some',
                  u'id': 10999,
                  u'last_login': u'2013-03-07T11:01:14+00:00',
                  u'last_name': u'One'},
  u'description': u'',
  u'email': {u'discussion': u'discussion-314208@items.sprint.ly',
             u'files': u'files-314208@items.sprint.ly'},
  u'last_modified': u'2013-03-30T05:52:09+00:00',
  u'number': 1096,
  u'product': {u'archived': 0, u'id': 9134, u'name': u'RBX'},
  u'progress': {u'started_at': u'2013-03-08T08:51:05+00:00'},
  u'score': u'L',
  u'short_url': u'http://sprint.ly/i/9134/1096/',
  u'status': u'in-progress',
  u'tags': [u'sprint1'],
  u'title': u'As a user, I want extensive help and support from manuals...',
  u'type': u'story',
  u'what': u'extensive help and support from manuals, screencasts and FAQs',
  u'who': u'user',
  u'why': u'I can understand how to use the system'}
]]


@patch('deploystream.providers.sprintly.Api')
def test_get_features(Api):
    mock_api = Mock()
    Api.return_value = mock_api
    mock_project = Mock()
    mock_project.id = 123
    endpoint = Mock()
    endpoint.return_value = ISSUES
    mock_api.products = MagicMock()
    mock_api.products.return_value = [mock_project]
    mock_api.products[123].items = endpoint

    sprintly_provider = SprintlyProvider('user', 'token',
                                         [{'status': 'in-progress'}])
    features = sprintly_provider.get_features()

    assert_equal(len(features), 2)
    assert_equal(features[0]['id'], 873)
    assert_equal(features[0]['type'], 'story')
    assert_equal(features[0]['owner'], '')
    assert_equal(features[1]['id'], 1096)
    assert_equal(features[1]['type'], 'story')
    assert_equal(features[1]['owner'], 'Some One')
