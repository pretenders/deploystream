from nose.tools import assert_true, assert_false

from deploystream.providers import (
    is_source_control_plugin, is_build_info_plugin, is_planning_plugin)


class TestSourceCodeControlPluginInterface(object):

    def test_implements_source_control_plugin(self):
        class MyPlugin(object):
            def get_repo_branches_involved(self, feature_id, **kwargs):
                pass
            def set_merged_status(self, repo_name, hierarchy_tree, **kwargs):
                pass

        assert_true(is_source_control_plugin(MyPlugin))

    def test_does_not_implement_source_control_plugin(self):
        class MyPlugin(object):
            def get_repo_branches_involved(self, feature_id, **kwargs):
                pass
            def set_merged_status(self, repo_name, hierarchy_tree):
                pass

        assert_false(is_source_control_plugin(MyPlugin))


class TestBuildInfoPluginInterface(object):

    def test_implements_build_info_plugin(self):
        class MyPlugin(object):
            def get_build_information(self, repo, branch, commit, **kwargs):
                pass
        assert_true(is_build_info_plugin(MyPlugin))

    def test_does_not_implement_build_info_plugin(self):
        class MyPlugin(object):
            pass
        assert_false(is_build_info_plugin(MyPlugin))


class TestPlanningPluginInterface(object):

    def test_implements_planning_plugin(self):
        class MyPlugin(object):
            def get_feature_info(self, feature_id, **kwargs):
                pass
        assert_true(is_planning_plugin(MyPlugin))

    def test_does_not_implement_planning_plugin(self):
        class MyPlugin(object):
            pass
        assert_false(is_planning_plugin(MyPlugin))
