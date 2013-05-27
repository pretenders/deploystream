import os
from os.path import join, exists, dirname

from nose.tools import assert_equal, assert_true, with_setup

from deploystream.providers.git_provider import GitProvider

DUMMY_CODE_DIR = join(dirname(__file__), 'data')


def ensure_dummy_clone_available():
    """
    Check that we have access to pretenders' dummyrepo
    """
    if not os.path.exists(DUMMY_CODE_DIR):
        os.mkdir(DUMMY_CODE_DIR)
    folder_name = join(DUMMY_CODE_DIR, 'dummyrepo')
    if not exists(folder_name):
        os.system('git clone git://github.com/pretenders/dummyrepo.git {0}'
                  .format(folder_name))
    else:
        cmd = 'git --git-dir={0}/.git fetch'.format(folder_name)
        ans = os.system(cmd)
        if ans != 0:
            raise Exception("Git fetch failed")


@with_setup(ensure_dummy_clone_available)
def test_git_provider_finds_branches_across_repos():
    """
    Test that the GitProvider finds branches in repos in the dir given.

    Clone the dummyrepo into the data folder if not already there.

    The data in this test is found by looking at the dummyrepo and getting
    the branch names and latest commit of any branches that match "feature-99".
    """
    provider = GitProvider(code_dir=DUMMY_CODE_DIR)
    branches = provider.get_repo_branches_involved(
        'feature-99',
        hierarchy_regexes=["master", "[a-z]*/{FEATURE_ID}"],
    )

    assert_equal(2, len(branches))
    assert_true({
        'name': 'master',
        'commit_id': "0f6eefefc14f362a2c6f804df69aa83bac48c20b",
        'parent_name': None,
        'repository': 'dummyrepo'} in branches)
    assert_true({
        'name': 'my/feature-99',
        'commit_id': "7098fa31bf9663343c723d9d155c0dc6e6e28174",
        'parent_name': 'master',
        'repository': 'dummyrepo'} in branches)
