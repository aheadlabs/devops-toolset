"""tools module commands"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Commands(ValueDictsBase):
    """Commands for the tools module."""

    # Add your core literal dictionaries here
    _commands = {
        "git_init": "git init {path}"
    }
