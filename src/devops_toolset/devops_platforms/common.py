"""This file contains common code for all the platforms"""

from devops_toolset.core.app import App
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.devops_platforms.commands import Commands as CommonCommands
from devops_toolset.devops_platforms.Literals import Literals as CommonLiterals
from devops_toolset.devops_platforms.azuredevops.Literals import Literals as AzureDevOpsLiterals
import devops_toolset.tools.cli as cli

app: App = App()
commands = CommandsCore([CommonCommands])
literals = LiteralsCore([CommonLiterals, AzureDevOpsLiterals])


def echo_environment_variable(environment_variable_name: str) -> str:
    """Echoes an environment variable. This function is common to all and
    limited to operating systems that support the echo command.

    Args:
        environment_variable_name: Name of the environment variable to echo.

    Returns:
        The environment variable value.
    """
    return cli.call_subprocess_with_result(commands.get("echo").format(
        variable=environment_variable_name
    ))


if __name__ == "__main__":
    help(__name__)
