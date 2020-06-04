"""Test configuration file for filesystem module.

Add here whatever you want to pass as a fixture in your texts."""

import pytest
import os
import pathlib


class Paths(object):
    """Class used to create the paths fixture"""
    current_path = os.path.dirname(os.path.realpath(__file__))
    root_path = pathlib.Path(current_path).absolute()
    file_foo_xml_project_path = pathlib.Path.joinpath(root_path, 'foo_project.xml').__str__()
    test_path = "/pathto/foo"
    non_existent_path = "/nonexistentpath"


@pytest.fixture
def paths():
    """Sample file paths for testing file system related functionality"""
    return Paths()
