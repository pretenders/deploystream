from datetime import datetime
from mock import patch

import deploystream


class SourceCodeProvider(object):
    name = 'source'
    oauth_token_required = None

    def get_repo_branches_involved(self, feature_id, **kwargs):
        return [('repo_01', "{0}_branch".format(feature_id), "232323")]

    def get_merged_status(self, repo_name, hierarchy_tree, **kwargs):
        return {}


class PlanningProvider(object):
    name = 'plan'
    oauth_token_required = None

    def get_features(self, **filters):
        return []

    def get_feature_info(self, feature_id, **kwargs):
        return {
            "title": "Amazing feature that will blow your mind",
            "id": feature_id,
            "url": "http://planning_site/{0}".format(feature_id),
            "feature_type": "story",
            "owner": "Bob",
            "description": "Too good for words..."
        }


class BuildInfoProvider(object):
    name = 'build'
    oauth_token_required = None

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
        response = self.client.get('/features/FT101')
        assert "Amazing feature that will blow your mind" in response.data

    @patch("deploystream.providers.ALL_PROVIDER_CLASSES",
           {'testplan': PlanningProvider,
            'testsource': SourceCodeProvider,
            'testbuild': BuildInfoProvider})
    def test_only_uses_providers_user_specifies(self):
        conf = deploystream.app.config
        del conf['USER_SPECIFIC_INFO']['provider_config'][0]

        response = self.client.get('/features/FT101')
        assert "Amazing feature that will blow your mind" not in response.data
