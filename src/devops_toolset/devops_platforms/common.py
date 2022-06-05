"""This file contains common code for all the platforms"""

from devops_toolset.core.app import App
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.devops_platforms.Literals import Literals as CommonLiterals
from devops_toolset.devops_platforms.azuredevops.Literals import Literals as AzureDevOpsLiterals
from enum import Enum
import logging
import os
import sys

app: App = App()
literals = LiteralsCore([CommonLiterals, AzureDevOpsLiterals])


def log_environment_variables(platform_keys: list):
    """Logs all environment variables for this platform and process.

    Args:
        platform_keys: List of platform variables.
    """

    spaces: int = len(max(platform_keys, key=len)) + 5

    for environment_variable in platform_keys:
        logging.info(literals.get("environment_variable_log").format(
            key=str(environment_variable).ljust(spaces, "."),
            value=os.environ.get(environment_variable)
        ))


if __name__ == "__main__":
    help(__name__)
