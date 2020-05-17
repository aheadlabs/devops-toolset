"""Unit tests for the git file"""

import pathlib
import pytest
from unittest.mock import patch
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
