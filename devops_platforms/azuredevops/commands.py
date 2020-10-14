"""Azure DevOps module commands"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Commands(ValueDictsBase):
    """Commands for the wordpress module."""

    # Add your wordpress literal dictionaries here
    _commands = {
        "azdevops_login": "{token} | az devops login --organization {organization}",
        "azdevops_universal_download": "az artifacts universal download --feed {feed} --name {name} --path {path} "
                                       "--version {version} --organization {organization}",
    }
