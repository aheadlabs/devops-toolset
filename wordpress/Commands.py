"""wordpress module commands"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Commands(ValueDictsBase):
    """Commands for the wordpress module."""

    # Add your core literal dictionaries here
    _commands = {
        "wpcli_info": "wp --info"
    }
