"""Unit tests for the git file"""

import io
import pathlib
import pytest
from unittest.mock import patch, mock_open
from filesystem.constants import Directions, FileNames
from tools.tests.conftest import GitignoreData
import tools.git as sut

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

    # Act
            with pytest.raises(FileNotFoundError):

    # Assert
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

# region find_gitignore_exclusion()

def test_find_gitignore_exclusion_given_path_when_exclusion_exists_then_returns_true(filenames, tmp_path):
    """Given a path, when the exclusion is found on it, then returns True"""

    # Arrange
    test_gitignore_path = pathlib.Path.joinpath(tmp_path, FileNames.GITIGNORE_FILE)
    with open(test_gitignore_path, "w") as test_gitignore:
        test_gitignore.write(".idea\n.vscode\n.vs\n.pytest/")
    exclusion = ".vs"

    # Act
    result = sut.find_gitignore_exclusion(test_gitignore_path, exclusion)

    # Assert
    assert result == True


def test_find_gitignore_exclusion_given_path_when_exclusion_exists_then_returns_false(filenames, tmp_path):
    """Given a path, when the exclusion is not found, then returns False"""

    # Arrange
    test_gitignore_path = pathlib.Path.joinpath(tmp_path, FileNames.GITIGNORE_FILE)
    with open(test_gitignore_path, "w") as test_gitignore:
        test_gitignore.write(".idea\n.vscode\n.vs\n.pytest/")
    exclusion = "notpresent"

    # Act
    result = sut.find_gitignore_exclusion(test_gitignore_path, exclusion)

    # Assert
    assert result == False

# endregion

# region update_gitignore_exclusion()

def test_update_gitignore_exclusion_given_regex_when_more_than_1_capture_group_raises_valueerror():
    """Given a RegEx, when it has more than 1 capture group, then raises
    ValueError"""

    # Arrange
    path = "/pathto"
    regex = "(a-z)(a-z)"
    value = "mytheme"

    # Act
    with pytest.raises(ValueError):

    # Assert
        sut.update_gitignore_exclusion(path, regex, value)


@patch("builtins.open", new_callable=mock_open, read_data = GitignoreData.file_contents)
def test_update_gitignore_exclusion_given_regex_when_1_capture_group_reads_gitignore(open, filenames):
    """Given a RegEx, when it has 1 capture group, it reads the .gitignore file
    passed in path"""

    # Arrange
    regex = GitignoreData.regex
    value = GitignoreData.replace_value

    # Act
    sut.update_gitignore_exclusion(filenames.path, regex, value)

    # Assert
    open.assert_any_call(filenames.path, "r+")


@patch("builtins.open", new_callable=mock_open, read_data = GitignoreData.file_contents)
def test_update_gitignore_exclusion_given_regex_when_1_capture_group_reads_gitignore(open, filenames):
    """Given a RegEx, when it has 1 capture group, it writes the .gitignore
    file after editing it"""

    # Arrange
    regex = GitignoreData.regex
    value = GitignoreData.replace_value

    # Act
    sut.update_gitignore_exclusion(filenames.path, regex, value)

    # Assert
    open.assert_any_call(filenames.path, "w")

# endregion
