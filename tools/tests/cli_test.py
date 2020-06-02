"""Unit tests for the tools file"""
import unittest.mock as mock
import tools.cli as sut
import subprocess
import logging

# region call_subprocess(str)


@mock.patch.object(subprocess, "Popen")
def test_call_subprocess_given_command_srt_then_calls_popens_with_command(subprocess_mock, clidata):
    """ Given an str command, then calls subprocess. Popen with that command"""

    # Arrange
    foo_command = clidata.sample_command
    expected_out = clidata.sample_log_message_info
    shell = True
    stdout = subprocess.PIPE
    stderr = subprocess.PIPE
    subprocess_mock.return_value.return_code = 0
    subprocess_mock.return_value.communicate.return_value = (expected_out, expected_out)

    # Act
    sut.call_subprocess(foo_command)

    # Assert
    subprocess_mock.assert_called_once_with(foo_command, shell=shell, stdout=stdout, stderr=stderr)


@mock.patch.object(subprocess, "Popen")
def test_call_subprocess_given_command_srt_when_stdout_has_lines_then_log_info(subprocess_mock, clidata):
    """ Given an str command, then calls subprocess.Popen and must log stdout as info"""

    # Arrange
    foo_command = clidata.sample_command
    expected_log_message = clidata.sample_log_message_info
    subprocess_mock.return_value.return_code = 0
    subprocess_mock.return_value.communicate.return_value = (expected_log_message, "")

    # Act
    with mock.patch.object(logging, "info") as logging_mock:
        sut.call_subprocess(foo_command)
        # Assert
        logging_mock.assert_called_once_with(expected_log_message)


@mock.patch.object(subprocess, "Popen")
def test_call_subprocess_given_command_srt_when_stderr_has_lines_then_log_error(subprocess_mock, clidata):
    """ Given an str command, then calls subprocess.Popen and must log stderr as error"""

    # Arrange
    foo_command = clidata.sample_command
    expected_log_message = clidata.sample_log_message_error
    subprocess_mock.return_value.return_code = 0
    subprocess_mock.return_value.communicate.return_value = ("", expected_log_message)

    # Act
    with mock.patch.object(logging, "error") as logging_mock:
        sut.call_subprocess(foo_command)

        # Assert
        logging_mock.assert_called_once_with(expected_log_message)

# endregion call_subprocess(str)
