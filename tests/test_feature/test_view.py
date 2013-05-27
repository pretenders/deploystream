from datetime import datetime
import json

from mock import patch
from nose.tools import assert_equal, assert_true

import deploystream


class SourceCodeProvider(object):
    name = 'source'
    oauth_token_name = None

    def get_repo_branches_involved(self, feature_id, hierarchy_tree, **kwargs):
        return [
            {
                'repository': 'repo_01',
                'name': '{0}_branch'.format(feature_id),
                'parent_name': 'master',
                'commit_id': '222222',
            },
            {
                'repository': 'repo_01',
                'name': 'master',
                'parent_name': None,
                'commit_id': '222223',
            },
        ]

    def get_merged_status(self, repo_name, hierarchy_tree, **kwargs):
        return {}


class PlanningProvider(object):
    name = 'plan'
    oauth_token_name = None

    def get_features(self, **filters):
        return []

    def get_feature_info(self, feature_id, **kwargs):
        return {
            "title": "Amazing feature that will blow your mind",
            "id": feature_id,
            "url": "http://planning_site/{0}".format(feature_id),
            "feature_type": "story",
            "owner": "Bob",
            "project": "P1",
            "description": "Too good for words..."
        }


class BuildInfoProvider(object):
    name = 'build'
    oauth_token_name = None

    def get_build_information(self, repo, branch, commit, **kwargs):
        return {
            "timestamp": datetime.now(),
            "result": "success",
            "commit": "242424",
            "url": "http://ci.box/{0}-{1}".format(repo, branch)
        }


class TestViewFeatureEndToEndWithDummyProviders(object):
    "A test case for checking that the site uses and displays providers info."

    def setUp(self):
        deploystream.app.config['TESTING'] = True
        deploystream.app.config['USER_SPECIFIC_INFO'] = {
            'provider_config': [
                ('testplan', {}),
                ('testsource', {}),
            ]
        }
        self.client = deploystream.app.test_client()

    @patch("deploystream.providers.ALL_PROVIDER_CLASSES",
           {'testplan': PlanningProvider,
            'testsource': SourceCodeProvider,
            'testbuild': BuildInfoProvider})
    def test_feature_view_shows_details(self):
        response = self.client.get('/features/plan/FT101')
        print response.__dict__
        feature_dict = json.loads(response.data)
        assert_true("Amazing feature that will blow your mind" in
            feature_dict['title'])

        ft101_branch_output = (
            feature_dict['branches']['repo_01']['FT101_branch'])
        assert_equal(ft101_branch_output['parent_name'], 'master')
        assert_equal(ft101_branch_output['children'], [])

        master_branch_output = (
            feature_dict['branches']['repo_01']['master'])
        assert_equal(master_branch_output['parent_name'], None)
        assert_equal(master_branch_output['children'][0]['name'],
                     "FT101_branch")

    @patch("deploystream.providers.ALL_PROVIDER_CLASSES",
           {'testplan': PlanningProvider,
            'testsource': SourceCodeProvider,
            'testbuild': BuildInfoProvider})
    def test_returns_404_on_unknown_provider(self):
        response = self.client.get('/features/planmissing/FT101')
        assert 404 == response.status_code
