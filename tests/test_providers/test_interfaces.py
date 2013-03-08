from nose.tools import assert_true, assert_false

from deploystream.providers.interfaces import (
    is_implementation,
    IBuildInfoPlugin, IPlanningPlugin, ISourceCodeControlPlugin,
)


class TestSourceCodeControlPluginInterface(object):

    def test_implements_source_control_plugin(self):
        class MyPlugin(object):
            def get_repo_branches_involved(self, feature_id):
                pass

            def set_merged_status(self, repo_name, hierarchy_tree):
                pass

        assert_true(is_implementation(MyPlugin, ISourceCodeControlPlugin))

    def test_does_not_implement_source_control_plugin(self):
        class MyPlugin(object):
            def get_repo_branches_involved(self, feature_id):
                pass

            def set_merged_status(self, repo_name):
                pass

        assert_false(is_implementation(MyPlugin, ISourceCodeControlPlugin))


class TestBuildInfoPluginInterface(object):

    def test_implements_build_info_plugin(self):
        class MyPlugin(object):
            def get_build_information(self, repo, branch, commit):
                pass

        assert_true(is_implementation(MyPlugin, IBuildInfoPlugin))

    def test_does_not_implement_build_info_plugin(self):
        class MyPlugin(object):
            pass

        assert_false(is_implementation(MyPlugin, IBuildInfoPlugin))


class TestPlanningPluginInterface(object):

    def test_implements_planning_plugin(self):
        class MyPlugin(object):
            def get_features(self, **filters):
                pass

            def get_feature_info(self, feature_id):
                pass

        assert_true(is_implementation(MyPlugin, IPlanningPlugin))

    def test_does_not_implement_planning_plugin(self):
        class MyPlugin(object):
            pass

        assert_false(is_implementation(MyPlugin, IPlanningPlugin))
