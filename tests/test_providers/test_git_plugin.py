from os.path import join, basename
import shutil
import tempfile

import git
from nose.tools import assert_equal

import deploystream
from deploystream.providers.git_plugin import GitPlugin


def create_git_repos(repo_names, branches):
    """
    Create a couple of repos each with ``branches``.

    In each branch add and commit an additional file.

    :returns:
        a tuple of the path to the folder where all the repos exist,
        a dictionary of repo: branch: commit hash
    """
    def add_file_and_commit(repo, dir):
        _, filename = tempfile.mkstemp(dir=dir)
        print filename
        repo.index.add([basename(filename)])
        commit = repo.index.commit("A commit")
        return str(commit)

    commit_hashes = {}
    # Create a test directory
    code_dir = tempfile.mkdtemp()
    # Inside that directory create 2 repos
    for repo_name in ['r1', 'r2']:
        folder_name = join(code_dir, repo_name)
        repo = git.Repo.init("{0}".format(folder_name))

        commit_hash = add_file_and_commit(repo, folder_name)
        commit_hashes[repo_name] = {'master': commit_hash}
        # Create branches of different names in those repos.
        for branch in branches:
            repo.create_head(branch)
            getattr(repo.heads, branch).checkout()
            commit_hash = add_file_and_commit(repo, folder_name)
            commit_hashes[repo_name][branch] = commit_hash

    return code_dir, commit_hashes


def remove_git_repos(path):
    shutil.rmtree(path)


def test_git_plugin_finds_branches_across_repos():
    """
    Test that the GitPlugin finds branches in mutiple repos in the dir given.

    Creates 2 repositories with branches inside a temp directory.
    """
    location, hashes = create_git_repos(repo_names=["r1", "r2"],
                                branches=['something', 'FeAtUrE'])
    plugin = GitPlugin(code_dir=location)
    branches = plugin.get_repo_branches_involved('FeAtUrE')

    try:
        assert_equal([
            ('r1', 'FeAtUrE', hashes['r1']['FeAtUrE']),
            ('r2', 'FeAtUrE', hashes['r2']['FeAtUrE']),
            ], branches)
    finally:
        remove_git_repos(location)
