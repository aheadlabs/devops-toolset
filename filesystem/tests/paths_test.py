"""Unit tests for the paths file"""

import filesystem.paths as sut
import pathlib
import pytest
from conftest import FileNames as FileNameFixtures
from filesystem.constants import Directions, FileNames
from unittest.mock import patch

# region files_exist()


def test_files_exist_given_empty_list_returns_empty_list(paths):
    """Given an empty list, returns an empty list"""

    # Arrange
    path = paths.directory_path
    file_names = []

    # Act
    result = sut.files_exist(path, file_names)

    # Assert
    assert result == []


@patch("pathlib.Path.rglob")
@pytest.mark.parametrize("rglob_response, expected", [
    ([], [("file1.txt", False), ("file2.txt", False)]),
    (["file1.txt"], [("file1.txt", True), ("file1.txt", True)])
])
def test_files_exist_given_list_returns_list_tuple(rglob_mock, rglob_response, expected, paths):
    """Given a list, returns a list of tuples with boolean values"""

    # Arrange
    path = paths.directory_path
    file_names = ["file1.txt", "file2.txt"]
    rglob_mock.return_value = rglob_response

    # Act
    result = sut.files_exist(path, file_names)

    # Assert
    assert result == expected

# endregion

# region files_exist_filtered()


@patch("filesystem.paths.files_exist")
@pytest.mark.parametrize("filter_by, expected", [(True, ["file1.txt"]), (False, ["file2.txt"])])
def test_files_exist_filtered(files_exist, filter_by, expected, paths):
    """Given, when, then"""

    # Arrange
    path = paths.directory_path
    file_names = []
    file_list_tuple = [("file1.txt", True), ("file2.txt", False)]
    files_exist.return_value = file_list_tuple

    # Act
    result = sut.files_exist_filtered(path, filter_by, file_names)

    # Assert
    assert result == expected


# endregion

# region get_file_name_from_url()


def test_get_file_name_from_url_given_url_returns_file_name(paths):
    """Given a URL, returns the file name"""

    # Arrange
    url = paths.url

    # Act
    result = sut.get_file_name_from_url(url)

    # Assert
    assert result == paths.file_name

# endregion

# region get_file_paths_in_tree()

def test_get_filepaths_in_tree_given_starting_path_glob_when_no_paths_then_returns_empty_list(filenames):
    """Given a starting path and a glob, when there are no matching paths, it
    returns an empty list."""

    # Arrange
    with patch.object(pathlib.Path, "rglob") as rglob:
        rglob.return_value = filenames.no_paths

    # Act
        result = sut.get_file_paths_in_tree(filenames.path, filenames.glob_no_match)

    # Assert
    assert result == []


def test_get_filepaths_in_tree_given_starting_path_glob_when_paths_then_returns_list(filenames):
    """Given a starting path and a glob, when there are matching paths, it
    returns a list with those paths."""

    # Arrange
    with patch.object(pathlib.Path, "rglob") as rglob:
        rglob.return_value = filenames.paths

    # Act
        result = sut.get_file_paths_in_tree(filenames.path, filenames.glob_no_match)

    # Assert
    assert result == filenames.paths

# endregion

# region get_filepath_in_tree() ASCENDING


def test_get_filepath_in_tree_ascending_given_file_name_when_exists_then_returns_path(filenames):
    """Given a file, when it exists in a child directory, should return its
    path"""

    # Arrange
    with patch.object(pathlib.Path, "exists") as exits:
        exits.return_value = True
        with patch(filenames.file__path, f"{filenames.path}/{filenames.test_file}"):

            # Act
            result = sut.get_filepath_in_tree(filenames.file)

    # Assert
    assert result.as_posix() == filenames.path


def test_get_filepath_in_tree_ascending_given_file_name_when_not_exist_then_returns_none(filenames):
    """Given a file, when does not exist in a parent directory, should return
    None"""

    # Arrange
    with patch.object(pathlib.Path, "exists") as exits:
        exits.return_value = False
        with patch(filenames.file__path, f"{filenames.path}/{filenames.test_file}"):

            # Act
            result = sut.get_filepath_in_tree(filenames.file)

    # Assert
    assert result is None

# endregion

# region get_filepath_in_tree() DESCENDING


def test_get_filepath_descending_in_tree_given_file_name_when_exists_then_returns_path(filenames):
    """Given a file, when it exists in a child directory, should return its
    path"""

    # Arrange
    with patch.object(pathlib.Path, "exists") as exists:
        exists.return_value = True
        with patch.object(pathlib.Path, "rglob") as rglob:
            rglob.return_value = filenames.paths
            with patch(filenames.file__path, f"{filenames.deep_path}/{filenames.test_file}"):

                # Act
                result = sut.get_filepath_in_tree(filenames.file, Directions.DESCENDING)

    # Assert
    assert result.as_posix() == filenames.path


@pytest.mark.parametrize("rglob_return, path", [
    (FileNameFixtures.paths, FileNameFixtures.deep_path), (FileNameFixtures.no_paths, FileNameFixtures.path)])
def test_get_filepath_descending_in_tree_given_file_name_when_not_exist_but_paths_then_returns_path(
        rglob_return, path, filenames):
    """Given a file, when it does not exist in a child directory but paths are
    returned, should return None"""

    # Arrange
    with patch.object(pathlib.Path, "exists") as exists:
        exists.return_value = False
        with patch.object(pathlib.Path, "rglob") as rglob:
            rglob.return_value = rglob_return
            with patch(filenames.file__path, f"{path}/{filenames.test_file}"):

                # Act
                result = sut.get_filepath_in_tree(filenames.file, Directions.DESCENDING)

    # Assert
    assert result is None


# endregion

# region get_project_root()


def test_get_project_root_then_calls_get_file_path_in_tree_with_project_file():
    """Then calls get_filepath_in_tree() with project file as a parameter"""

    # Arrange
    with patch.object(sut, "get_filepath_in_tree") as target:

        # Act
        sut.get_project_root()

        # Assert
        target.assert_called_with(FileNames.PROJECT_FILE)

# endregion

# region get_project_xml_data()


def test_get_project_xml_data_when_add_environment_variables_is_false_then_return_dict_with_env_variables(paths):
    """When add_environment_variables is false, then return dict with xml data"""

    # Arrange
    expected_result = {"PROJECT_FOO1": "foo1", "PROJECT_FOO2": "foo2", "PROJECT_FOO3": "foo3"}
    with patch.object(pathlib.Path, "joinpath") as joinpath_mock:
        joinpath_mock.return_value = paths.file_foo_xml_project_path
        # Act
        result = sut.get_project_xml_data(False)
        # Assert
        assert expected_result == result


def test_get_project_xml_data_when_add_environment_variables_is_true_then_call_create_env_variables(paths):
    """When add_environment_variables is false, then return dict with xml data"""

    # Arrange
    expected_result = {"PROJECT_FOO1": "foo1", "PROJECT_FOO2": "foo2", "PROJECT_FOO3": "foo3"}
    with patch.object(pathlib.Path, "joinpath") as joinpath_mock:
        joinpath_mock.return_value = paths.file_foo_xml_project_path
        with patch.object(sut, "platform_specific") as platform_specific_mock:
            with patch.object(platform_specific_mock, "create_environment_variables") as create_env_vars_mock:
                # Act
                sut.get_project_xml_data(True)
                # Assert
                create_env_vars_mock.assert_called_once_with(expected_result)


def test_is_valid_path_given_test_path_returns_true(paths):
    """Given a test path, returns true"""

    # Arrange
    path = paths.test_path

    # Act
    result = sut.is_valid_path(path)

    # Assert
    assert result


def test_is_valid_path_given_non_existent_path_returns_false(paths):
    """Given a non existent path, returns false"""

    # Arrange
    path = paths.non_existent_path

    # Act
    result = sut.is_valid_path(path)

    # Assert
    assert not result

# endregion
