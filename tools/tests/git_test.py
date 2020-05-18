"""Unit tests for the git file"""

import io
import pathlib
import pytest
from unittest.mock import patch, mock_open
import tools.git as sut
import filesystem.paths as paths
from filesystem.constants import Directions, FileNames

# region get_gitignore_path()
def test_get_gitignore_path_given_none_when_exists_then_returns_root_gitignore_path(filenames):
    """Given no file, when it exists, should return path to root .gitignore"""

    # Arrange
    with patch.object(sut, "get_project_root") as target:
        target.return_value = pathlib.Path(f"{filenames.path}")
        with patch.object(pathlib.Path, "exists") as exits:
            exits.return_value = True

    # Act
            result = sut.get_gitignore_path()

    # Assert
    assert result == pathlib.Path(f"{filenames.path}/{FileNames.GITIGNORE_FILE}")

def test_get_gitignore_path_given_none_when_not_exist_then_raises_filenotfounderror(filenames):
    """Given no file, when it doesn't exist, should raise FileNotFoundError"""

    # Arrange
    with patch.object(sut, "get_project_root") as target:
        target.return_value = pathlib.Path(f"{filenames.path}")
        with patch.object(pathlib.Path, "exists") as exits:
            exits.return_value = False

    # Act, Assert
            with pytest.raises(FileNotFoundError):
                sut.get_gitignore_path()

def test_get_gitignore_path_given_file_then_calls_get_filepath_in_tree(filenames):
    """Given a file, should call get_filepath_in_tree(FileNames.GITIGNORE_FILE, direction)"""

    # Arrange
    with patch.object(sut, "get_filepath_in_tree") as target:

    # Act
        sut.get_gitignore_path(filenames.file, Directions.ASCENDING)

    # Assert
    target.assert_called_with(filenames.file, Directions.ASCENDING)

# endregion

# region add_gitignore_exclusion()

def test_add_gitignore_exclusion_given_path_when_file_opens_then_appends_exclusion(filenames, tmp_path):
    """Given a path, when the file opens, the exclusion is appended"""

    # Arrange
    test_gitignore_path = pathlib.Path.joinpath(tmp_path, FileNames.GITIGNORE_FILE)
    with open(test_gitignore_path, "w") as test_gitignore:
        test_gitignore.write(".pytest/")
    exclusion = "exclusion/"
    expected_gitignore = io.StringIO(f".pytest/\n{exclusion}\n")

    # Act
    sut.add_gitignore_exclusion(test_gitignore_path, exclusion)

    # Assert
    with open(test_gitignore_path, "r") as test_gitignore:
        content = test_gitignore.read()
        assert content == expected_gitignore.read()

# endregion
