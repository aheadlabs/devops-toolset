"""dotnet module literals"""

from devops_toolset.core.app import App
from devops_toolset.core.ValueDictsBase import ValueDictsBase

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the dotnet module."""

    _info = {
        "dotnet_build_before": "Launching dotnet build inside {path}. Please wait..",
        "dotnet_ef_database_drop": "Dropping the database...",
        "dotnet_ef_database_reset": "Reverting all migrations...",
        "dotnet_ef_migrations_list": "Listing migrations (will take a while)...",
        "dotnet_ef_migrations_script": "Generating SQL script (will take a while)...",
        "dotnet_project_version": "The project version is {version}",
        "dotnet_restore_before": "Launching dotnet restore inside {path}. Please wait..",
    }
    _errors = {
        "dotnet_restore_err": "Something went wrong while restoring {path}. Please check the logs and try again.",
        "dotnet_build_err": "Something went wrong while building {path}. Please check the logs and try again.",
    }
