import json

from nose.tools import assert_equal

import deploystream
from deploystream.apps.repo.models import Repo
from deploystream.apps.users.models import User
from deploystream import db

import tests
from tests import test_users


class TestGetRepo(test_users.UserTestMixin):

    def setup(self):
        self.client = deploystream.app.test_client()
        repo, created = Repo.get_or_create(
            {'git_url': 'http://testrepo.git'},
            name='test_repo')
        self.repo_id = repo.id
        repo.users = [User.query.get(tests.MAIN_USER_ID)]

        #Alternate user for non-main user access
        User.get_or_create({'email': "other@test.com", 'password': "123"},
            username="other_user")
        db.session.commit()

    def test_api_get_single_repo(self):
        "Test that an auth'd user can get details about a repo."
        self.send_login_post('main_test_user', '123')

        response = self.client.get('/api/repos/{0}'.format(self.repo_id))
        assert_equal(response.status_code, 200)
        repo_data = json.loads(response.data)

        assert_equal(repo_data['name'], 'test_repo')
        assert_equal(repo_data['git_url'], 'http://testrepo.git')

    def test_api_get_single_rejects_anonymous_user(self):
        "Test that the api rejects an anonymous user"
        response = self.client.get('/api/repos/{0}'.format(self.repo_id))

        assert_equal(response.status_code, 401)

    def test_api_get_single_rejects_unauthorized_users(self):
        "Test that the api rejects an unauthorized user's requests"
        self.send_login_post('other_user', '123')

        response = self.client.get('/api/repos/{0}'.format(self.repo_id))

        assert_equal(response.status_code, 401)

    def test_api_get_all_repos_for_user(self):
        "Test that an auth'd user can get details about all repos"
        self.send_login_post('main_test_user', '123')

        response = self.client.get('/api/repos'.format(self.repo_id))
        assert_equal(response.status_code, 200)
        repo_data = json.loads(response.data)

        assert_equal(len(repo_data['objects']), 1)
        assert_equal(repo_data['objects'][0]['name'], 'test_repo')
        assert_equal(repo_data['objects'][0]['git_url'], 'http://testrepo.git')

    def test_api_get_many_rejects_anonymous_user(self):
        "Test that the api rejects an anonymous user"
        response = self.client.get('/api/repos')

        assert_equal(response.status_code, 401)

    def test_api_get_many_rejects_unauthorized_users(self):
        "Test that the api rejects an unauthorized user's requests"
        self.send_login_post('other_user', '123')

        response = self.client.get('/api/repos')

        assert_equal(response.status_code, 401)
