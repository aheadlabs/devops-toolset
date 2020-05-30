"""Bootstraps everything
Args:
    --skip-i18n: If present it will skip loading gettext
"""

import argparse
import importlib.util
import pathlib
from core.settings import Settings
import i18n.loader
from core.log_setup import configure

parser = argparse.ArgumentParser()
parser.add_argument("--skip-i18n", action="store_true")
args, args_unknown = parser.parse_known_args()


class App(object):
    """App object"""

    # Initialize settings
    settings: Settings = Settings()

    def __init__(self):
        # Load gettext
        i18n.loader.setup(self.settings)

        # Configure logging
        configure(self.settings.log_config_file_path)

    def load_platform_specific(self, name: str):
        module_path = pathlib.Path.joinpath(self.settings.platform_specific_path, f"{name}.py")
        spec = importlib.util.spec_from_file_location(name, module_path)
        platform_specific = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(platform_specific)
        return platform_specific


if __name__ == "__main__":
    help(__name__)
