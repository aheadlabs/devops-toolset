"""wordpress module literals"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the wordpress module."""

    _info = {
        "npm_run_before": _("Running npm task: {task}..."),
        "npm_run_after": _("npm task: {task} has completed successfully."),
        "npm_install_before": _("Npm install launched. This may take a while..."),
        "npm_install_after": _("Npm install completed successfully."),
        "gulp_build_before": _("Gulp build task has launched for theme {theme_slug}."),
        "gulp_build_after": _("Gulp build task has completed successfully for theme {theme_slug}.")
    }
    _errors = {
        "npm_run_error": _("An error has occurred while running task {task}. See above log for more details."),
        "npm_install_error": _("Npm install has encountered an error. Please check above logs for more details."),
        "gulp_build_error":
            _("Gulp build task has encountered an error for theme {theme_slug}. "
              "Please check above logs for more details.")
    }
