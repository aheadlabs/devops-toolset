""" Unit tests for the dotnet/utils.py module"""

import devops_toolset.project_types.dotnet.utils as sut
import pathlib
from devops_toolset.core.app import App
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.dotnet.commands import Commands as DotnetCommands
from devops_toolset.project_types.dotnet.Literals import Literals as DotnetLiterals
from unittest.mock import patch

app: App = App()
literals = LiteralsCore([DotnetLiterals])
commands = CommandsCore([DotnetCommands])


# region get_appsettings_environments()

@patch("logging.info")
@patch("pathlib.Path.glob")
def test_get_appsettings_environments_returns_list(glob_mock, logging_info_mock, dotnetdata):
    """ Given the .csproj file path, returns a list of strings."""

    # Arrange
    csproj_path = "path/to/csproj"
    glob_mock.return_value = dotnetdata.get_appsettings_files()

    # Act
    result = sut.get_appsettings_environments(csproj_path)

    # Assert
    assert type(result) is list


@patch("logging.info")
@patch("pathlib.Path.glob")
def test_get_appsettings_environments_given_unmatched_environments_returns_empty_list(
        glob_mock, logging_info_mock, dotnetdata):
    """ Given the .csproj file path and wrong appsettings files, returns an
    empty list."""

    # Arrange
    csproj_path = "path/to/csproj"
    glob_mock.return_value = dotnetdata.get_wrong_appsettings_files()

    # Act
    result = sut.get_appsettings_environments(csproj_path)

    # Assert
    assert result == []


# endregion

# region get_csproj_project_version()


def test_get_csproj_project_version_given_path_returns_version_number(dotnetdata, tmp_path):
    """ Given the .csproj file path , returns the version number."""

    # Arrange
    csproj_file_content = dotnetdata.csproj_file_content
    csproj_file_path = pathlib.Path.joinpath(tmp_path, "my_project.csproj")
    with open(str(csproj_file_path), "w") as properties_file:
        properties_file.write(csproj_file_content)

    # Act
    result = sut.get_csproj_project_version(str(csproj_file_path))

    # Assert
    assert result == "6.6.6"


# endregion

# region git_tag()


@patch("logging.info")
@patch("devops_toolset.tools.git_flow.is_branch_suitable_for_tagging")
@patch("devops_toolset.tools.git.git_tag_add")
@patch("devops_toolset.tools.git.git_tag_exist")
def test_git_tag_calls_git_tools_tag_add(
        git_tag_exist_mock, git_tag_add_mock, git_flow_suitable_branch_mock, _, gitdata):
    """ Given a commit name, tag name and branch name, calls git.git_tag_add() """
    # Arrange
    branch = gitdata.branch
    commit = gitdata.commit
    tag = gitdata.tag
    auth_header = gitdata.auth_header
    git_flow_suitable_branch_mock.return_value = True
    git_tag_exist_mock.return_value = False

    # Act
    sut.git_tag(commit, tag, branch, auth_header)

    # Assert
    git_tag_add_mock.assert_called_with(tag, commit, auth_header=auth_header)


@patch("logging.info")
@patch("devops_toolset.tools.git_flow.is_branch_suitable_for_tagging")
@patch("devops_toolset.tools.git.git_tag_add")
@patch("devops_toolset.tools.git.git_tag_exist")
def test_git_tag_not_calls_git_tools_tag_add(
        git_tag_exist_mock, git_tag_add_mock, git_flow_suitable_branch_mock, _, gitdata):
    """ Given a commit name, tag name and branch name, calls git.git_tag_add() """
    # Arrange
    branch = gitdata.branch
    commit = gitdata.commit
    tag = gitdata.tag
    auth_header = gitdata.auth_header
    git_flow_suitable_branch_mock.return_value = False
    git_tag_exist_mock.return_value = False

    # Act
    sut.git_tag(commit, tag, branch, auth_header)

    # Assert
    git_tag_add_mock.assert_not_called()


@patch("logging.info")
@patch("logging.warning")
@patch("devops_toolset.tools.git_flow.is_branch_suitable_for_tagging")
@patch("devops_toolset.tools.git.git_tag_add")
@patch("devops_toolset.tools.git.git_tag_exist")
@patch("devops_toolset.tools.git.git_tag_delete")
def test_git_tag_calls_git_tools_tag_delete_when_tag_exists_and_overwrite_tag \
                (git_tag_delete_mock, git_tag_exist_mock, git_tag_add_mock, git_flow_suitable_branch_mock,
                 logging_warning_mock, _, gitdata):
    """ Given a commit name, tag name, branch name and overwrite_tag, calls git.git_tag_delete() """
    # Arrange
    branch = gitdata.branch
    commit = gitdata.commit
    tag = gitdata.tag
    auth_header = gitdata.auth_header
    git_flow_suitable_branch_mock.return_value = True
    git_tag_exist_mock.return_value = True

    # Act
    sut.git_tag(commit, tag, branch, auth_header)

    # Assert
    git_tag_delete_mock.assert_called_with(tag, True, auth_header)


@patch("logging.info")
@patch("logging.warning")
@patch("devops_toolset.tools.git_flow.is_branch_suitable_for_tagging")
@patch("devops_toolset.tools.git.git_tag_add")
@patch("devops_toolset.tools.git.git_tag_exist")
@patch("devops_toolset.tools.git.git_tag_delete")
def test_git_tag_warns_when_tag_exists_and_not_overwrite_tag\
                (git_tag_delete_mock, git_tag_exist_mock, git_tag_add_mock, git_flow_suitable_branch_mock,
                 logging_warning_mock, _, gitdata):
    """ Given a commit name, tag name, branch name and not overwrite_tag, then not tag anything """
    # Arrange
    branch = gitdata.branch
    commit = gitdata.commit
    tag = gitdata.tag
    auth_header = gitdata.auth_header
    git_flow_suitable_branch_mock.return_value = True
    git_tag_exist_mock.return_value = True

    # Act
    sut.git_tag(commit, tag, branch, auth_header, False)

    # Assert
    git_tag_add_mock.assert_not_called()

# endregion git_tag()
