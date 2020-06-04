"""tools module literals."""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the tools module."""

    # Add your core literal dictionaries here
    _info = {
        "git_purging_gitkeep": _("Purging .gitkeep file at {path}")
    }

    _errors = {
        "git_regex1cg": _("RegEx must have 1 capture group. No less, no more."),
        "git_non_valid_dir_path": _("Path must be an existent dir.")
    }
