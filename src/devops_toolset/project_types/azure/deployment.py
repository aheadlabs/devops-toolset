"""Provides deployment tools for Azure cloud."""
import subprocess

from devops_toolset.core.app import App
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.azure.commands import Commands as AzureCommands, Log as Log
from devops_toolset.project_types.azure.Literals import Literals as AzureLiterals
from devops_toolset.tools import cli

app: App = App()
literals = LiteralsCore([AzureLiterals])
commands = CommandsCore([AzureCommands])

"""Define a function to create a resource group."""
def create_resource_group(resource_group_name, location):
    """Create a new resource group."""
    print("\nCreate Resource Group")
    print("This script creates a new resource group named {}. To learn more, visit https://docs.microsoft.com/azure/azure-resource-manager/management/overview#terminology".format(resource_group_name))

    rg_result = subprocess.run(["az", "group", "create", "--name", resource_group_name, "--location", location], stdout=subprocess.PIPE)
    print(rg_result.stdout.decode('utf-8'))
