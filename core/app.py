"""Bootstraps everything
Args:
    --skip-i18n: If present it will skip loading gettext
"""

import argparse
from core.settings import Settings
import i18n.loader

parser = argparse.ArgumentParser()
parser.add_argument("--skip-i18n", action="store_true")
args, args_unknown = parser.parse_known_args()


class App(object):
    """App object"""

    # Initialize settings
    settings: Settings = Settings()

    def __init__(self):
        # Load gettext
        if not args.skip_i18n:
            i18n.loader.setup(self.settings)
