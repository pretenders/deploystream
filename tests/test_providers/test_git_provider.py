import os
from os.path import join, exists, dirname

from nose.tools import assert_equal, with_setup

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
        os.system('git clone git+ssh://git@github.com/pretenders/dummyrepo {0}'
                  .format(folder_name))
    else:
        os.system('git --git-dir={0} fetch'.format(folder_name))


@with_setup(ensure_dummy_clone_available)
def test_git_plugin_finds_branches_across_repos():
    """
    Test that the GitPlugin finds branches in repos in the dir given.

    Clone the dummyrepo into the data folder if not already there.

    The data in this test is found by looking at the dummyrepo and getting
    the branch names and latest commit of any branches that match "FeAtUrE".
    """
    provider = GitProvider(code_dir=DUMMY_CODE_DIR,
            feature_breakup_regex="(?P<project>[a-zA-Z]+)-?(?P<id>[0-9]+)",
            branch_finder_template=".*(?i){project}.*")
    branches = provider.get_repo_branches_involved('FeAtUrE-99')

    assert_equal([
        ('dummyrepo', 'my/feature_branch',
         'cf9130d3c07b061a88569153f10a7c7779338cfa'),
        ], branches)


def test_git_plugin_feature_breakup_regex():
    """
    Test that GitPlugin breaks up feature ids into appropriate parts.
    """
    provider = GitProvider(
                 feature_breakup_regex="(?P<project>[a-zA-Z]+)-?(?P<id>[0-9]+)")
    for feature, expected in [
        ('DD-334', {'id': '334', 'project':'DD'}),
        ('DD334', {'id': '334', 'project':'DD'}),
        ]:
        assert_equal(provider._get_feature_breakdown('DD-334'), expected)
