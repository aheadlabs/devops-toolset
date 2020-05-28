"""devops.azuredevops module literals."""

from core.LiteralsBase import LiteralsBase
from core.app import App

app: App = App()


class Literals(LiteralsBase):
    """Literals for the devops.azuredevops module."""

    # Add your core literal dictionaries here
    _info = {
        "platform_created_ev": _("Created environment variable {key} with value {value}")
    }
    _errors = {}
