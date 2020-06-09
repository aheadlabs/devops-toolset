"""Unit tests for the git file"""

import io
import pathlib
import pytest
import tools.git as sut
import filesystem.paths as path_tools
from unittest.mock import patch, mock_open
from filesystem.constants import Directions, FileNames
from tools.tests.conftest import GitignoreData
from tools.tests.conftest import BranchesData


# region get_gitignore_path()

@patch("filesystem.paths.get_project_root")
def test_get_gitignore_path_given_none_when_exists_then_returns_root_gitignore_path(target, filenames):
    """Given no file, when it exists, should return path to root .gitignore"""

    # Arrange
    target.return_value = pathlib.Path(f"{filenames.path}")
    with patch.object(pathlib.Path, "exists") as exits:
        exits.return_value = True

    # Act
        result = sut.get_gitignore_path()

    # Assert
    assert result == pathlib.Path(f"{filenames.path}/{FileNames.GITIGNORE_FILE}")


@patch("filesystem.paths.get_project_root")
def test_get_gitignore_path_given_none_when_not_exist_then_raises_filenotfounderror(target, filenames):
    """Given no file, when it doesn't exist, should raise FileNotFoundError"""

    # Arrange
    target.return_value = pathlib.Path(f"{filenames.path}")
    with patch.object(pathlib.Path, "exists") as exits:
        exits.return_value = False

    # Act
        with pytest.raises(FileNotFoundError):

            # Assert
            sut.get_gitignore_path()


@patch("filesystem.paths.get_filepath_in_tree")
def test_get_gitignore_path_given_file_then_calls_get_filepath_in_tree(target, filenames):
    """Given a file, should call get_filepath_in_tree(FileNames.GITIGNORE_FILE, direction)"""

    # Arrange

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


@patch("builtins.open", new_callable=mock_open, read_data=GitignoreData.file_contents)
def test_update_gitignore_exclusion_given_regex_when_1_capture_group_reads_gitignore(mocked_open, filenames):
    """Given a RegEx, when it has 1 capture group, it reads the .gitignore file
    passed in path"""

    # Arrange
    regex = GitignoreData.regex
    value = GitignoreData.replace_value

    # Act
    sut.update_gitignore_exclusion(filenames.path, regex, value)

    # Assert
    mocked_open.assert_any_call(filenames.path, "r+")


@patch("builtins.open", new_callable=mock_open, read_data=GitignoreData.file_contents)
def test_update_gitignore_exclusion_given_regex_when_1_capture_group_writes_gitignore(mocked_open, filenames):
    """Given a RegEx, when it has 1 capture group, it writes the .gitignore
    file after editing it"""

    # Arrange
    regex = GitignoreData.regex
    value = GitignoreData.replace_value

    # Act
    sut.update_gitignore_exclusion(filenames.path, regex, value)

    # Assert
    mocked_open.assert_any_call(filenames.path, "w")

# endregion

# region simplify_branch_name()


@pytest.mark.parametrize("long_branch, expected", [
    (BranchesData.long_master_branch, BranchesData.simple_master_branch),
    (BranchesData.long_pr_branch, BranchesData.simple_pr_branch)])
def test_simplify_branch_name_given_branch_when_root_then_returns_simplified(long_branch, expected):
    """Given a branch name, when it is a root branch, then it is returned
    simplified"""

    # Arrange

    # Act
    result = sut.simplify_branch_name(long_branch)

    # Assert
    assert result == expected


def test_simplify_branch_name_given_branch_when_feature_then_returns_simplified(branchesdata):
    """Given a branch name, when it is a feature branch, then it is returned
    simplified"""

    # Arrange
    long_branch = branchesdata.long_feature_branch
    expected = branchesdata.simple_feature_branch

    # Act
    result = sut.simplify_branch_name(long_branch)

    # Assert
    assert result == expected


def test_simplify_branch_name_given_branch_when_other_then_returns_original(branchesdata):
    """Given a branch name, when it is non-defined branch, then it is returned
    simplified"""

    # Arrange
    long_branch = branchesdata.other_branch
    expected = branchesdata.other_branch

    # Act
    result = sut.simplify_branch_name(long_branch)

    # Assert
    assert result == expected

# endregion

# region set_current_branch_simplified()


def test_set_current_branch_simplified_given_branch_and_environment_variable_creates_environment_variable(branchesdata):
    """Given a branch name and a environment variable, calls platform_specific's create_
    environment_variables method"""

    # Arrange
    branch = branchesdata.other_branch
    environment_variable_name = branchesdata.environment_variable_name

    # Act
    with patch.object(sut, "platform_specific") as platform_specific_mock:
        with patch.object(platform_specific_mock, "create_environment_variables") as create_env_vars_mock:
            sut.set_current_branch_simplified(branch, environment_variable_name)
            # Assert
            create_env_vars_mock.assert_called_once_with({environment_variable_name: branch})

# endregion

# region purge_gitkeep()


def test_purge_gitkeep_when_invalid_path_raises_valueerror(paths):
    """Given an invalid path, raises ValueError"""

    # Arrange
    path = paths.invalid_path

    # Act
    with pytest.raises(ValueError):

        # Assert
        sut.purge_gitkeep(path)


@patch("logging.info")
@patch("os.remove")
@patch.object(path_tools, "is_empty_dir", return_value=True)
def test_purge_gitkeep_when_no_additional_files_remove_not_called(is_empty_dir_mock,
                                                                  os_remove,
                                                                  logging_info,
                                                                  tmp_path):
    """Given a directory with a .gitkeep file, when directory is empty, do
    nothing"""

    # Arrange
    guess_gitkeep_file = pathlib.Path.joinpath(tmp_path, ".gitkeep")
    with open(str(guess_gitkeep_file), "w") as gitkeep:
        gitkeep.write("")

    # Act
    sut.purge_gitkeep(str(tmp_path))

    # Assert
    os_remove.assert_not_called()


@patch("logging.info")
@patch("os.remove")
def test_purge_gitkeep_when_directory_not_empty_remove_called(os_remove, logging_info, tmp_path):
    """Given a directory with a .gitkeep file, when directory not empty, call
    os.remove()"""

    # Arrange
    guess_gitkeep_file = pathlib.Path.joinpath(tmp_path, ".gitkeep")
    other_file = pathlib.Path.joinpath(tmp_path, "other_file.txt")
    with open(str(guess_gitkeep_file), "w") as gitkeep:
        gitkeep.write("")
    with open(str(other_file), "w") as file:
        file.write("hello world!")

    # Act
    sut.purge_gitkeep(str(tmp_path))

    # Assert
    os_remove.assert_called_once_with(guess_gitkeep_file)

# endregion
