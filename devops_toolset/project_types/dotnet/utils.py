""" Contains dotnet utilities """

from core.app import App
from core.LiteralsCore import LiteralsCore
from project_types.dotnet.Literals import Literals as DotnetLiterals
from core.CommandsCore import CommandsCore
from project_types.dotnet.commands import Commands as DotnetCommands

import filesystem.parsers
import logging

app: App = App()
platform_specific = app.load_platform_specific("environment")
literals = LiteralsCore([DotnetLiterals])
commands = CommandsCore([DotnetCommands])


def get_csproj_project_version(csproj_path: str) -> str:
    """ Gets the version number from a .csproj files

    Arguments:
        csproj_path: Path to the .csproj file

    Returns:
        The version number defined in the .csproj file.
    """

    version = filesystem.parsers.get_xml_file_entity_text("./PropertyGroup/Version", csproj_path)
    version_environment_variable = {"PROJECT_VERSION": version["Version"]}
    platform_specific.create_environment_variables(version_environment_variable)

    logging.info(literals.get("dotnet_project_version").format(version=version["Version"]))


if __name__ == "__main__":
    help(__name__)
