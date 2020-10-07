"""wordpress module commands"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Commands(ValueDictsBase):
    """Commands for the wordpress module."""

    # Add your wordpress literal dictionaries here
    _commands = {
        "npm_install": "npm install {folder}",
        "npm_run": "npm run {command} {silent} {if_present} {extra_args}"
    }
