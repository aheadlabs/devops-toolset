"""Angular module commands"""

from devops_toolset.core.ValueDictsBase import ValueDictsBase
from devops_toolset.core.app import App

app: App = App()


class Commands(ValueDictsBase):
    """ Commands for the Angular module."""

    # Add your Angular commands dictionaries here
    _commands = {
        "ng_install_cli": "npm install {global_scope} @angular/cli@latest",
        "ng_uninstall_cli": "npm uninstall {global_scope} @angular/cli",
        "ng_update_cli": "npm update {global_scope} @angular/cli@latest",
    }
