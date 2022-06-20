"""Helper functions fot HTTP-related tasks."""
import re
import requests
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.tools.commands import Commands as ToolsCommands
from devops_toolset.tools.Literals import Literals as ToolsLiterals
literals = LiteralsCore([ToolsLiterals])
commands = CommandsCore([ToolsCommands])


def get_public_ip_address():
    """Gets the machine public IP address using an external service."""
    regex = r"((?:\d{1,3}\.?){4})"
    response = requests.get(commands.get("public_ip_address_service_url"))
    match = re.search(regex, response.content.decode("utf-8"))
    return match.groups()[0]


if __name__ == "__main__":
    help(__name__)
    print(get_public_ip_address())
