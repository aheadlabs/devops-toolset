"""wordpress module literals"""

from core.LiteralsBase import LiteralsBase
from core.app import App

app: App = App()


class Literals(LiteralsBase):
    """Literals for the wordpress module."""

    # Add your core literal dictionaries here
    _info = {}
    _errors = {}
