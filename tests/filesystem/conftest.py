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
    file_name = "filename.txt"
    glob = "*.txt"
    url = f"https://example.com/{file_name}"
    directory_path = "/pathto"
    file_name_list = ["file1.txt", "file2.txt"]
    file_pattern = "*.json"
    path_to_file_1 = f"{directory_path}/file1.json"
    path_to_file_2 = f"{directory_path}/file2.json"
    rglob_result_0 = []
    rglob_result_1 = [path_to_file_1]
    rglob_result_many = [path_to_file_1, path_to_file_2]


@pytest.fixture
def paths():
    """Sample file paths for testing file system related functionality"""
    return Paths()
