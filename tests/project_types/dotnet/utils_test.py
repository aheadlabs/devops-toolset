""" Unit-core for the dotnet/cli.py module"""

import pathlib
import devops_toolset.project_types.dotnet.utils as sut
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.dotnet.commands import Commands as DotnetCommands
from devops_toolset.project_types.dotnet.Literals import Literals as DotnetLiterals
from devops_toolset.core.app import App

app: App = App()
literals = LiteralsCore([DotnetLiterals])
commands = CommandsCore([DotnetCommands])


# region get_csproj_project_version()

def test_get_csproj_project_version_given_path_returns_version_number(dotnetdata, tmp_path):
    """ Given the .csproj file path , returns the version number."""

    # Arrange
    csproj_file_content = dotnetdata.csproj_file_content
    csproj_file_path = pathlib.Path.joinpath(tmp_path, "my_project.csproj")
    with open(str(csproj_file_path), "w") as properties_file:
        properties_file.write(csproj_file_content)

    # Act
    result = sut.get_csproj_project_version(str(csproj_file_path))

    # Assert
    assert result == "6.6.6"

# endregion get_csproj_project_version()
