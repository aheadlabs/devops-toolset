"""tools module literals."""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the tools module."""

    # Add your core literal dictionaries here
    _info = {
        "git_purging_gitkeep": _("Purging .gitkeep file at {path}"),
        "git_repo_to_be_created": _("The repository is going to be created"),
        "git_repo_created": _("The repository has been created"),
        "val_path_argument_not_valid": _("The path specified in the {argument} argument is invalid or does not exist."),
    }

    _errors = {
        "git_err_create_repo": _("Git error: repository couldn't be created"),
        "git_non_valid_dir_path": _("Path must be an existent dir."),
        "git_regex1cg": _("RegEx must have 1 capture group. No less, no more."),
    }
