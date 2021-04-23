""" Unit-core for the linux/utils.py module"""

from unittest.mock import patch, call
import pytest

import project_types.linux.utils as sut
from core.CommandsCore import CommandsCore
from core.LiteralsCore import LiteralsCore
from project_types.linux.commands import Commands as LinuxCommands
from project_types.linux.Literals import Literals as LinuxLiterals
from core.app import App

app: App = App()
literals = LiteralsCore([LinuxLiterals])
commands = CommandsCore([LinuxCommands])

# region edit_in_place


@patch("logging.error")
def test_edit_in_place_given_arguments_when_file_path_not_exist_then_raises_error(
    logging_mock):
    """ Given arguments, when file_path does not exist, should raise FileNotFound error """
    # Arrange
    file_path = "path/to/file"
    search_for = "replace this string"
    replace_with = "with this string"
    error_message = literals.get("file_not_exist_err").format(path=file_path)

    # Act
    with pytest.raises(FileNotFoundError):
        sut.edit_in_place(search_for, replace_with, file_path)

        # Assert
        logging_mock.assert_called_once_with(error_message)


@patch("tools.cli.call_subprocess")
@patch("pathlib.Path.exists")
def test_edit_in_place_given_arguments_then_calls_subprocess_with_arguments(
    path_exists_mock, call_subprocess_mock):
    """ Given arguments, should call subprocess with command edit_in_place and its arguments """
    # Arrange
    file_path = "path/to/file"
    search_for = "replace this string"
    replace_with = "with this string"
    path_exists_mock.return_value = True
    log_before_messages = [literals.get("edit_in_place_post").format(
        search_for=search_for, replace_with=replace_with, path=file_path)]
    log_after_err_messages = [literals.get("edit_in_place_err").format(
         search_for=search_for, replace_with=replace_with, path=file_path)]
    expected_command = commands.get("edit_in_place").format(
        search_for=search_for,
        replace_with=replace_with,
        file_path=file_path
    )

    # Act
    sut.edit_in_place(search_for, replace_with, file_path)

    # Assert
    call_subprocess_mock.assert_called_once_with(expected_command,
                                                 log_before_out=log_before_messages,
                                                 log_after_err=log_after_err_messages)


# endregion edit_in_place

# region edit_multiple_in_place

@patch("project_types.linux.utils.edit_in_place")
@patch("pathlib.Path.exists")
def test_edit_multiple_in_place_given_replacements_should_call_edit_in_place(
        path_exists_mock, edit_in_place_mock):
    """ Given replacements dict, should call edit_in_place with every replacement """
    # Arrange
    file_path = "path/to/file"
    replacements = {"key": "value", "key2": "value2"}

    # Act
    sut.edit_multiple_in_place(replacements, file_path)
    calls = []
    for key, value in replacements.items():
        calls.append(call(key, value, file_path))

    # Assert
    edit_in_place_mock.assert_has_calls(calls)

# endregion edit_multiple_in_place
