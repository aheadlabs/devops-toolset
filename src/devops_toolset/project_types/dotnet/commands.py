"""dotnet module commands"""

from devops_toolset.core.ValueDictsBase import ValueDictsBase
from devops_toolset.core.app import App

app: App = App()


class Commands(ValueDictsBase):
    """ Commands for the dotnet module."""

    # Add your dotnet commands dictionaries here
    _commands = {
        "dotnet_build": "dotnet build {force} {with_restore} --configuration={configuration} --framework={framework} "
                        "--runtime={runtime} {debug} {output} {path}",
        "dotnet_ef_migrations_list": "dotnet ef migrations list --startup-project {path} --json -- --environment {env}",
        "dotnet_ef_migrations_script": "dotnet ef migrations script {migration_from} --startup-project {path} "
                                       "--output {script_path} {idempotent}",
        "dotnet_restore": "dotnet restore {force} {debug} {path}",
    }

