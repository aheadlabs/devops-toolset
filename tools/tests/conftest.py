"""Test configuration file for filesystem module.

Add here whatever you want to pass as a fixture in your texts."""

import pytest


class GitignoreData(object):
    """Class used to create the gitignoredata fixture"""
    file_contents = "wordpress/wp-content/themes/oldtheme/"
    regex = r"wordpress/wp-content/themes/([\w\-]+)/"
    replace_value = "mytheme"


@pytest.fixture
def gitignoredata():
    """Sample file names for testing file system related functionality"""
    return GitignoreData()


class BranchesData(object):
    """Class used to create the branchesdata fixture"""
    long_master_branch = "refs/heads/master"
    simple_master_branch = "master"
    long_feature_branch = "refs/heads/feature/name"
    simple_feature_branch = "feature/name"
    long_pr_branch = "refs/pull/1/merge"
    simple_pr_branch = "pull/1"
    other_branch = "dev"
    environment_variable_name = "env_variable"


@pytest.fixture
def branchesdata():
    """Sample branch names for testing"""
    return BranchesData()


class CliData(object):
    """ Class used to create CliData fixture containing test data"""
    sample_command = "sample command"
    sample_log_message_info = "Operation completed successfully."
    sample_log_message_error = "Something went wrong."


@pytest.fixture()
def clidata():
    """ Sample command line interface data """
    return CliData()
