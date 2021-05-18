"""Unit core for the environment file"""

from devops_toolset.core.CommandsCore import CommandsCore
from unittest.mock import patch, call
from devops_toolset.project_types.linux.commands import Commands as LinuxCommands
import devops_toolset.devops_platforms.aws.environment as sut

linux_commands = CommandsCore([LinuxCommands])


# region create_environment_variables()


@patch("logging.info")
@patch("devops_toolset.tools.cli.call_subprocess")
def test_create_environment_variables_given_dict_when_not_empty_calls_to_create_env_variables_command(
        call_subprocess_mock, logger_mock, platformdata):
    """Given a dictionary, when it is not empty, writes environment variables
    to stdout in the Azure DevOps notation"""

    # Arrange
    environment_variables = platformdata.environment_variables_dict
    expected_command_1 = linux_commands.get("create_env_variable").\
        format(variable_name="env_var_1", variable_value="value1")
    expected_command_2 = linux_commands.get("create_env_variable").\
        format(variable_name="env_var_2", variable_value="value2")

    # Act
    sut.create_environment_variables(environment_variables)
    calls = [call(expected_command_1), call(expected_command_2)]

    # Assert
    call_subprocess_mock.assert_has_calls(calls)

# endregion
