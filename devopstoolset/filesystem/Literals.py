"""filesystem module literals"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the filesystem module."""

    _titles = {}
    _info = {
        "fs_project_path_is": _("Project path is {path}."),
        "fs_composer_path_is": _("Composer file path is {path}."),
        "fs_zip_added_file": _("[{zip_file_name}] Added file: {added_file}"),
        "fs_file_moving": _("Moving file {origin_file_path} to {destination_file_path}"),
    }
    _errors = {
        "fs_not_dir": _("Path must be a dir, not a file."),
    }
