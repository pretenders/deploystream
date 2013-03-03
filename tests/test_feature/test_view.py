from datetime import datetime
from mock import patch

import deploystream


class SourceCodePlugin(object):
    def get_repo_branches_involved(self, feature_id, **kwargs):
        return [('repo_01', "{0}_branch".format(feature_id), "232323")]

    def get_merged_status(self, repo_name, hierarchy_tree, **kwargs):
        return {}


class PlanningPlugin(object):
    def get_feature_info(self, feature_id, **kwargs):
        return {
            "title": "Amazing feature that will blow your mind",
            "id": feature_id,
            "url": "http://planning_site/{0}".format(feature_id),
            "feature_type": "interesting",
            "owner": "Bob"
        }


class BuildInfoPlugin(object):
    def get_build_information(self, repo, branch, commit, **kwargs):
        return {
            "timestamp": datetime.now(),
            "result": "success",
            "commit": "242424",
            "url": "http://ci.box/{0}-{1}".format(repo, branch)
        }


class TestEndToEndWithDummyPlugins(object):
    "A test case for checking that the site uses and displays plugins info."

    def setUp(self):
        deploystream.app.config['TESTING'] = True
        self.client = deploystream.app.test_client()

    @patch("deploystream.apps.feature.lib.PLANNING_PLUGINS",
            [PlanningPlugin()])
    @patch("deploystream.apps.feature.lib.SOURCE_CODE_PLUGINS",
            [SourceCodePlugin()])
    @patch("deploystream.apps.feature.lib.BUILD_INFO_PLUGINS",
            [BuildInfoPlugin()])
    def test_feature_view_shows_details(self):
        response = self.client.get('/feature/FT101')
        assert "Amazing feature that will blow your mind" in response.data
        # TODO: Add further assertions here to do with links etc. Probably
        # with the use of beautiful soup.
