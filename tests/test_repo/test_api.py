import json

from nose.tools import assert_equal

import deploystream
from deploystream.apps.repo.models import Repo
from deploystream.apps.users.models import User
from deploystream import db

import tests
from tests import test_users


class TestGetRepo(test_users.UserTest):

    def setup(self):
        self.client = deploystream.app.test_client()
        repo, created = Repo.get_or_create(
            {'url': 'http://testrepo.git',
             'user_id': tests.MAIN_USER_ID},
            name='test_repo')
        self.repo_id = repo.id
        db.session.commit()

    def test_api_get_single_repo(self):
        "Test that an auth'd user can get details about a repo."
        self.send_login_post('main_test_user', '123')

        response = self.client.get('/api/repos/{0}'.format(self.repo_id))
        assert_equal(response.status_code, 200)
        repo_data = json.loads(response.data)

        assert_equal(repo_data['name'], 'test_repo')
        assert_equal(repo_data['url'], 'http://testrepo.git')

    def test_api_get_single_rejects_anonymous_user(self):
        "Test that the api rejects an anonymous user"
        response = self.client.get('/api/repos/{0}'.format(self.repo_id))

        assert_equal(response.status_code, 401)

    def test_api_get_single_rejects_unauthorized_users(self):
        "Test that the api rejects an unauthorized user's requests"
        self.send_register_post('other_user')
        self.send_login_post('other_user', '123')

        response = self.client.get('/api/repos/{0}'.format(self.repo_id))

        assert_equal(response.status_code, 404)

    def test_api_get_all_repos_for_user(self):
        "Test that an auth'd user can get details about all repos"
        self.send_login_post('main_test_user', '123')

        response = self.client.get('/api/repos'.format(self.repo_id))
        assert_equal(response.status_code, 200)
        repo_data = json.loads(response.data)

        assert_equal(len(repo_data['objects']), 1)
        assert_equal(repo_data['objects'][0]['name'], 'test_repo')
        assert_equal(repo_data['objects'][0]['url'], 'http://testrepo.git')

    def test_api_get_many_rejects_anonymous_user(self):
        "Test that the api rejects an anonymous user"
        response = self.client.get('/api/repos')

        assert_equal(response.status_code, 401)

    def test_api_get_many_returns_only_those_for_the_user(self):
        "Test that the api rejects an unauthorized user's requests"
        self.send_register_post('other_user')
        self.send_login_post('other_user', '123')

        response = self.client.get('/api/repos')

        assert_equal(response.status_code, 200)
        repo_data = json.loads(response.data)

        assert_equal(len(repo_data['objects']), 0)


class TestPostRepo(test_users.UserTest):

    def setup(self):
        self.client = deploystream.app.test_client()

    def send_add_repo_post(self, **kwargs):
        payload = {
            'name': 'AwesomeRepo',
            'url': 'http://github.com/me/awesomes',
        }
        payload.update(kwargs)
        return self.client.post('/api/repos', data=json.dumps(payload),
                                content_type='application/json')

    def test_create_repo_against_user(self):
        self.send_login_post('main_test_user', '123')

        response = self.send_add_repo_post()
        assert_equal(response.status_code, 201)
        repo = Repo.query.filter_by(name='AwesomeRepo').first()
        me = User.query.filter_by(username='main_test_user').first()
        assert_equal(repo.user, me)

    def test_post_as_anonymous_fails(self):
        response = self.send_add_repo_post()
        assert_equal(response.status_code, 401)

    def test_post_as_other_user_ignores_user_id(self):
        self.send_register_post('other_user')
        self.send_login_post('other_user', '123')

        self.send_add_repo_post(
            user_id=tests.MAIN_USER_ID,
            url='http://my_sneeky_repo'
        )

        repo = Repo.query.filter_by(url='http://my_sneeky_repo').first()
        assert_equal(repo.user.username, 'other_user')


