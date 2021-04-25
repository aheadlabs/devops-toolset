"""devops_platforms.aws module literals."""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the devops_platforms.aws module."""

    # Add your core literal dictionaries here
    _info = {
        "aws_command": _("Command: {command}"),
        "platform_created_ev": _("Created environment variable {key} with value {value}"),
    }
    _errors = {}
