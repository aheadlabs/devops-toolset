"""Test configuration file for filesystem module.

Add here whatever you want to pass as a fixture in your texts.

    ie: (see FileNames example)
        - Add a class that contains what you want to pass as a fixture in your tests.
        - Create a fixture with that same lowered name that returns an instance to that class."""

import pytest

class FileNames(object):
    """Class used to create the filenames fixture"""
    test_file = "test.py"
    path = "/pathto"
    deep_path = "/deep/pathto"
    paths = ["/pathto/file1", "/pathto/file2"]
    no_paths = []
    file = ".gitignore"
    file__path = "filesystem.paths.__file__"

@pytest.fixture
def filenames():
    """Sample file names for testing file system related functionality"""
    return FileNames()
