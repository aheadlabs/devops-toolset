"""Contains wrappers for WP CLI commands"""

from core.app import App
import logging

app: App = App()


def install_wp_cli() -> bool:
    pass


def download_wordpress() -> bool:
    pass


def install_wordpress() -> bool:
    pass


def reset_database() -> bool:
    pass


def import_database() -> bool:
    pass


def set_database_configuration() -> bool:
    pass


def export_database() -> bool:
    pass


def create_configuration_file() -> bool:
    pass


def set_configuration_constant() -> bool:
    pass


def update_database_option() -> bool:
    pass


def install_theme() -> bool:
    pass


if __name__ == "__main__":
    help(__name__)
