"""Test configuration file for devops-toolset package.

This code is executed once per unit test session.
Add here whatever you want to pass as a fixture in your core.

    ie: (see FileNames example)
        - Add a class that contains what you want to pass as a fixture in your core.
        - Create a fixture with that same lowered name that returns an instance to that class."""

from unittest import mock

import pytest
import requests


class FileNames(object):
    """Class used to create the filenames fixture"""
    test_file = "test.py"
    test_file2 = "test2.py"
    test_pot_file = "test.pot"
    path = "/pathto"
    deep_path = "/deep/pathto"
    paths = ["/pathto/file1", "/pathto/file2"]
    no_paths = []
    file = ".gitignore"
    file__path = "filesystem.paths.__file__"
    glob_no_match = "**/no_match.file"


class Mocks(object):
    """Class used to declare general purpose testing mocks"""
    requests_get_mock = mock.patch.object(requests, "get").start()


@pytest.fixture
def filenames():
    """Sample file names for testing file system related functionality"""
    return FileNames()


@pytest.fixture
def mocks():
    """ General testing mocks """
    yield Mocks()
    Mocks.requests_get_mock.stop()
    print(" Teardown finished.")

