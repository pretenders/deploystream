from nose.tools import assert_true, assert_false

from deploystream.providers.interfaces import (
    is_implementation,
    IBuildInfoProvider, IPlanningProvider, ISourceCodeControlProvider,
    IOAuthProvider
)


class TestSourceCodeControlProviderInterface(object):

    def test_implements_source_control_provider(self):
        class MyProvider(object):
            name = "provider"
            oauth_token_required = "oauth"
            def get_repo_branches_involved(self, feature_id):
                pass

            def set_merged_status(self, repo_name, hierarchy_tree):
                pass

        assert_true(is_implementation(MyProvider(), ISourceCodeControlProvider))

    def test_does_not_implement_source_control_provider(self):
        class MyProvider(object):
            def get_repo_branches_involved(self, feature_id):
                pass

            def set_merged_status(self, repo_name):
                pass

        assert_false(is_implementation(MyProvider(), ISourceCodeControlProvider))


class TestBuildInfoProviderInterface(object):

    def test_implements_build_info_provider(self):
        class MyProvider(object):
            name = "provider"
            oauth_token_required = "oauth"

            def get_build_information(self, repo, branch, commit):
                pass

        assert_true(is_implementation(MyProvider(), IBuildInfoProvider))

    def test_does_not_implement_build_info_provider(self):
        class MyProvider(object):
            pass

        assert_false(is_implementation(MyProvider(), IBuildInfoProvider))


class TestPlanningProviderInterface(object):

    def test_implements_planning_provider(self):
        class MyProvider(object):
            name = "provider"
            oauth_token_required = "oauth"

            def get_features(self, **filters):
                pass

            def get_feature_info(self, feature_id):
                pass

        assert_true(is_implementation(MyProvider(), IPlanningProvider))

    def test_does_not_implement_planning_provider(self):
        class MyProvider(object):
            pass

        assert_false(is_implementation(MyProvider(), IPlanningProvider))


class TestOAuthProviderInterface(object):

    def test_implements_oauth(self):
        class MyProvider(object):
            name = "provider"
            oauth_token_required = "oauth"

            def get_oauth_data(self):
                pass
        assert_true(is_implementation(MyProvider(), IOAuthProvider))

    def test_does_not_implement_oauth(self):
        class MyProvider(object):
            pass

        assert_false(is_implementation(MyProvider(), IOAuthProvider))
