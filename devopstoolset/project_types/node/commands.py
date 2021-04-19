"""node module commands"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Commands(ValueDictsBase):
    """Commands for the node module."""

    # Add your node literal dictionaries here
    _commands = {
        "npm_install": "npm install {folder}",
        "npm_run": "npm run {command} {silent} {if_present} {extra_args}"
    }
