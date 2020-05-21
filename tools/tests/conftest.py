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
