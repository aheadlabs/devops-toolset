"""Helper functions fot HTTP-related tasks."""

import re
import requests
from devops_toolset.core.app import App
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.tools.commands import Commands as ToolsCommands
from devops_toolset.tools.Literals import Literals as ToolsLiterals

app: App = App()
platform_specific = app.load_platform_specific("environment")
literals = LiteralsCore([ToolsLiterals])
commands = CommandsCore([ToolsCommands])


def get_public_ip_address(
        public_service_url: str = commands.get("public_ip_address_service_url"),
        environment_variable_name: str = "DT_PUBLIC_IP_ADDRESS") -> str:
    """Gets the machine public IP address using an external service.

    Args:
        public_service_url: URL of the public service to be requested. Defaults
            to checkip.dyndns.com
        environment_variable_name: Name of the environment variable to be
            created. Defaults to "DT_PUBLIC_IP_ADDRESS".

    Returns:
        Public IP address of the endpoint that calls this function.
    """

    regex = r"((?:\d{1,3}\.?){4})"
    response = requests.get(public_service_url)
    match = re.search(regex, response.content.decode("utf-8"))
    ip_address = match.groups()[0]

    platform_specific.create_environment_variables({environment_variable_name: ip_address})

    return ip_address


if __name__ == "__main__":
    help(__name__)
