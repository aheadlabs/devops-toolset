"""Unit core for the environment file"""
import os

import pytest

from devops_toolset.core.CommandsCore import CommandsCore
from unittest.mock import patch, call
from devops_toolset.project_types.linux.commands import Commands as LinuxCommands
import devops_toolset.devops_platforms.aws.environment as sut

linux_commands = CommandsCore([LinuxCommands])


# region create_environment_variables()


@patch("logging.info")
def test_create_environment_variables_given_dict_when_not_empty_calls_to_create_env_variables_command(
        logger_mock, platformdata):
    """Given a dictionary, when it is not empty, creates environment variables"""

    # Arrange
    environment_variables = platformdata.environment_variables_dict

    # Act
    sut.create_environment_variables(environment_variables)

    # Assert
    for key in environment_variables.keys():
        assert key in os.environ
        # Cleanup: We need to remove the example values from the env variables.
        del os.environ[key]


# endregion

# region end_task()


def test_end_task_given_result_when_fail_then_raises_error():
    """ Given result type, when fail, then should raise an EnvironmentError """
    # Arrange
    result_type = sut.ResultType.fail
    # Act and Assert
    with pytest.raises(EnvironmentError):
        sut.end_task(result_type)


def test_end_task_given_result_when_success_then_do_nothing():
    """ Given result type, when success, then should not raise anything """
    # Arrange
    result_type = sut.ResultType.success
    # Act and Assert
    sut.end_task(result_type)

# endregion
