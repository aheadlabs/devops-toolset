"""devops_platforms.azuredevops module literals."""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the devops_platforms.azuredevops module."""

    # Add your core literal dictionaries here
    _info = {
        "azdevops_command": _("Command: {command}"),
        "azdevops_download_package_manually": _("Please, download the packages from the Azure DevOps feed manually."),
        "platform_created_ev": _("Created environment variable {key} with value {value}"),
    }
    _errors = {
        "azdevops_status_code": _("Status code for the request: {status_code}"),
        "azdevops_token_not_found": _("Azure DevOps token was not found in the **kwargs parameter."),
    }
