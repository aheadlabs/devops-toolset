"""linux module commands"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Commands(ValueDictsBase):
    """Commands for the linux module."""

    # Add your linux literal dictionaries here
    _commands = {
        "deb_which": "which {package}",
        "deb_package_install": "sudo apt install -y {package} {version}"
    }
