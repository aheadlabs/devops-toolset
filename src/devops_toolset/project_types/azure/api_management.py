"""Provides support for deployment operations in Azure API Management service."""
import json
import logging

from devops_toolset.core import log_tools
from devops_toolset.core.app import App
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.azure.commands import Commands as AzureCommands
from devops_toolset.project_types.azure.Literals import Literals as AzureLiterals
from devops_toolset.tools import cli

app: App = App()
literals = LiteralsCore([AzureLiterals])
commands = CommandsCore([AzureCommands])


def check_apim_exists(resource_group_name, apim_name):
    """Checks if an API Management service exists."""

    logging.info(literals.get("azure_cli_apim_checking").format(name=apim_name))
    result = cli.call_subprocess_with_result(commands.get("azure_cli_apim_exists")
                                             .format(resource_group_name=resource_group_name, name=apim_name))

    if isinstance(result, str) and 'ResourceNotFound' not in result:
        logging.info(literals.get("azure_cli_apim_exists").format(name=apim_name))
        return True
    elif isinstance(result, tuple) and 'ResourceNotFound' in result[1]:
        logging.info(literals.get("azure_cli_apim_not_exists").format(name=apim_name))
        return False
    else:
        logging.error(literals.get("azure_cli_apim_check_failed").format(name=apim_name))
        return False
