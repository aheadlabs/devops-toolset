"""Unit tests for the common file"""

from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.devops_platforms.commands import Commands as CommonCommands
from unittest.mock import patch
import devops_toolset.devops_platforms.common as sut
import devops_toolset.tools.cli as cli

commands = CommandsCore([CommonCommands])


# region echo_environment_variable()

@patch("devops_toolset.tools.cli.call_subprocess_with_result")
def test_echo_environment_variable_calls_subprocess(subprocess_mock):
    """Calls"""

    # Arrange
    variable_name: str = "variable1"

    # Act
    _ = sut.echo_environment_variable(variable_name)

    # Assert
    subprocess_mock.assert_called_with(commands.get("echo").format(
        variable=variable_name
    ))

# endregion
