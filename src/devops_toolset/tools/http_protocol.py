"""Helper functions fot HTTP-related tasks."""

import re
import requests
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.tools.commands import Commands as ToolsCommands
from devops_toolset.tools.Literals import Literals as ToolsLiterals

literals = LiteralsCore([ToolsLiterals])
commands = CommandsCore([ToolsCommands])


def get_public_ip_address(public_service_url: str = commands.get("public_ip_address_service_url")):
    """Gets the machine public IP address using an external service.

    Args:
        public_service_url: URL of the public service to be requested. Defaults
            to checkip.dyndns.com

    Returns:
        Public IP address of the endpoint that calls this function.
    """

    regex = r"((?:\d{1,3}\.?){4})"
    response = requests.get(public_service_url)
    match = re.search(regex, response.content.decode("utf-8"))
    return match.groups()[0]


if __name__ == "__main__":
    help(__name__)
