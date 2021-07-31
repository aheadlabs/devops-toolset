"""dotnet module literals"""

from devops_toolset.core.app import App
from devops_toolset.core.ValueDictsBase import ValueDictsBase

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the Angular module."""

    _info = {
        "angular_project_version": "The project version is {version}",
    }
    _errors = {}
