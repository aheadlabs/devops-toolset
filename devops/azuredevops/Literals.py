"""devops.azuredevops module literals."""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the devops.azuredevops module."""

    # Add your core literal dictionaries here
    _info = {
        "platform_created_ev": _("Created environment variable {key} with value {value}")
    }
    _errors = {}
