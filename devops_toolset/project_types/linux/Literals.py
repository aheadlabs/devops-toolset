"""linux module literals"""

from core.app import App
from core.ValueDictsBase import ValueDictsBase

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the linux module."""

    _info = {
        "deb_package_install_pre": "Preparing to install: {package}. Please wait...",
        "deb_package_install_post": "Package {package} has been succesfully installed."
    }
    _errors = {
        "deb_package_install_err": "An error occurred when trying to install {package}. Please check the logs."
    }
