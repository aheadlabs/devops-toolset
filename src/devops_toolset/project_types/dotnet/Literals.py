"""dotnet module literals"""

from devops_toolset.core.app import App
from devops_toolset.core.ValueDictsBase import ValueDictsBase

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the dotnet module."""

    _info = {
        "dotnet_build_before": "Launching dotnet build inside {path}. Please wait..",
        "dotnet_cli_log": ".NET CLI => {log}",
        "dotnet_cli_project_created": "Project '{name}.csproj' created.",
        "dotnet_cli_project_exists": "Solution '{name}.csproj' already exists. Skipping.",
        "dotnet_cli_project_package_added": "Project \"{project}\" added \"{package}\" as a dependency.",
        "dotnet_cli_project_package_exists": "Project package \"{package}\" exists for project \"{project}\" as a "
                                             "dependency. Skipping.",
        "dotnet_cli_project_reference_added": "Project \"{project}\" added \"{referenced}\" as a reference.",
        "dotnet_cli_project_reference_exists": "Project reference \"{referenced}\" exists for project \"{project}\"."
                                               "Skipping.",
        "dotnet_cli_solution_created": "Solution '{name}.sln' created.",
        "dotnet_cli_solution_exists": "Solution '{name}.sln' already exists. Skipping.",
        "dotnet_cli_solution_project_added": "Project '{project}.csproj' added to solution '{solution}.sln'.",
        "dotnet_cli_solution_project_not_added": "Project '{project}.csproj' already added to solution '{solution}.sln'"
                                                 ". Skipping.",
        "dotnet_project_version": "The project version is {version}",
        "dotnet_restore_before": "Launching dotnet restore inside {path}. Please wait..",
        "dotnet_cli_starting_layer": "Starting layer '{layer}'.",
    }
    _errors = {
        "dotnet_restore_err": "Something went wrong while restoring {path}. Please check the logs and try again.",
        "dotnet_build_err": "Something went wrong while building {path}. Please check the logs and try again.",
    }
