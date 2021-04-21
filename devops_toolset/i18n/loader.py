"""Initializes gettext"""

import gettext
from core.settings import Settings


def setup(settings: Settings):
    """Sets up translations for the selected language"""
    gettext.translation("base", localedir=settings.locales_path, languages=[settings.language]).install()
