"""filesystem module literals"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the filesystem module."""

    _titles = {}
    _info = {
        "fs_project_path_is": _("Project path is {path}.")
    }
    _errors = {
        "fs_not_dir": _("Path must be a dir, not a file."),
    }
