"""tools module literals."""

from devops_toolset.core.ValueDictsBase import ValueDictsBase
from devops_toolset.core.app import App

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the tools module."""

    # Add your core literal dictionaries here
    _info = {
        "cli_return_code": _("Process terminated with return code {code}"),
        "git_purging_gitkeep": _("Purging .gitkeep file at {path}"),
        "git_repo_to_be_created": _("The repository is going to be created"),
        "git_repo_created": _("The repository has been created"),
        "val_path_argument_not_valid": _("The path specified in the {argument} argument is invalid or does not exist."),
        "git_init_repo": _("Do you want me to initialize a local Git repository for you?"),
        "git_before_adding_project_structure_files_to_stage": _("Adding files to the stage"),
        "git_after_adding_project_structure_files_to_stage": _("Added files to the stage"),
        "git_add_project_structure_message": _("File project structure created"),
        "git_before_project_structure_commit": _("Creating file project structure commit"),
        "git_after_project_structure_commit": _("Committed project structure files"),
        "git_before_change_branch": _("Changing branch to master"),
        "git_after_change_branch": _("Changed branch to master successfully"),
    }

    _errors = {
        "git_err_create_repo": _("Git error: repository couldn't be created"),
        "git_non_valid_dir_path": _("Path must be an existent dir."),
        "git_regex1cg": _("RegEx must have 1 capture group. No less, no more."),
        "git_err_commit_project_structure": _("Git error: project structure files couldn't be committed"),
        "git_err_adding_project_structure_files_to_stage": _("Files couldn't be staged"),
        "git_err_changing_branch": _("Changing to master branch couldn't be done"),
    }
