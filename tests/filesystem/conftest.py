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


class FileContents(object):
    """Class to create the file contents fixture"""
    json_file_depth_1 = "{\"key1\":\"value1\"}"
    json_file_depth_1_result = "{\"key1\":\"new value\"}"
    json_file_depth_2 = "{\"key1\":{\"key2\":\"value2\"}}"
    json_file_depth_2_result = "{\"key1\":{\"key2\":\"new value\"}}"
    json_file_depth_3 = "{\"key1\":{\"key2\":{\"key3\":\"value3\"}}}"
    json_file_depth_3_result = "{\"key1\":{\"key2\":{\"key3\":\"new value\"}}}"
    json_file_name = "file.json"
    key_value = "new value"


@pytest.fixture
def paths():
    """Sample file paths for testing file system related functionality"""
    return Paths()


@pytest.fixture
def filecontents():
    """Sample file contents for testing file system related functionality"""
    return FileContents()
