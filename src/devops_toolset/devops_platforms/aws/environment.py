"""Environment-related functionality for Aws"""

from devops_toolset.core.app import App
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.devops_platforms.aws.Literals import Literals as AwsLiterals
from devops_toolset.project_types.linux.commands import Commands as LinuxCommands
import devops_toolset.tools.cli as cli
import logging

app: App = App()
literals = LiteralsCore([AwsLiterals])
linux_commands = CommandsCore([LinuxCommands])


def create_environment_variables(key_value_pairs: dict):
    """Creates environment variables

    Args:
        key_value_pairs: Key-value pair dictionary
    """

    for key, value in key_value_pairs.items():
        logging.info(literals.get("platform_created_ev").format(key=key, value=value))
        cli.call_subprocess(linux_commands.get("create_env_variable").format(variable_name=key, variable_value=value))


if __name__ == "__main__":
    help(__name__)
