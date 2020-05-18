"""Unit tests for the paths file"""

import pathlib
from unittest.mock import patch
import filesystem.paths as sut
from filesystem.constants import Directions, FileNames

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
                result = sut.get_filepath_in_tree(filenames.file, Directions.DESDENDING)

    # Assert
    assert result.as_posix() == filenames.path


def test_get_filepath_descending_in_tree_given_file_name_when_not_exist_but_paths_then_returns_path(filenames):
    """Given a file, when it does not exist in a child directory but paths are
    returned, should return None"""

    # Arrange
    with patch.object(pathlib.Path, "exists") as exists:
        exists.return_value = False
        with patch.object(pathlib.Path, "rglob") as rglob:
            rglob.return_value = filenames.paths
            with patch(filenames.file__path, f"{filenames.deep_path}/{filenames.test_file}"):

    # Act
                result = sut.get_filepath_in_tree(filenames.file, Directions.DESDENDING)

    # Assert
    assert result is None


def test_get_filepath_descending_in_tree_ascending_given_file_name_when_not_exist_no_paths_then_returns_none(filenames):
    """Given a file, when does not exist in a child directory and no paths
    are returned, should return None"""

    # Arrange
    with patch.object(pathlib.Path, "exists") as exits:
        exits.return_value = False
        with patch.object(pathlib.Path, "rglob") as rglob:
            rglob.return_value = filenames.no_paths
            with patch(filenames.file__path, f"{filenames.path}/{filenames.test_file}"):

    # Act
                result = sut.get_filepath_in_tree(filenames.file, Directions.DESDENDING)

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