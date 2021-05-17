"""dotnet module commands"""

from devops_toolset.core.ValueDictsBase import ValueDictsBase
from devops_toolset.core.app import App

app: App = App()


class Commands(ValueDictsBase):
    """ Commands for the dotnet module."""

    # Add your dotnet commands dictionaries here
    _commands = {
        "dotnet_restore": "dotnet restore {force} {debug} {path}",
        "dotnet_build": "dotnet build {force} {with_restore} --configuration={configuration} --framework={framework} "
                        "--runtime={runtime} {debug} {output} {path}"
    }

