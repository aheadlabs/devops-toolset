"""Contains wrappers for WP CLI commands"""

from core.app import App
import logging
from enum import Enum

app: App = App()


class ValueType(Enum):
    """Defines value types for values at the wp-config.php file"""

    CONSTANT = 1,
    VARIABLE = 2


def install_wp_cli(install_path: str = "/usr/local/bin/wp"):
    """Downloads and installs the latest version of WP-CLI.

    For more information see:
        https://make.wordpress.org/cli/handbook/installing/

    Args:
        install_path: Path where WP-CLI will be installed. It must be in the
            PATH/BIN of the operating system.
    """
    pass


def download_wordpress(site_configuration: dict, destination_path: str):
    """Downloads the latest version of the WordPress core files using WP-CLI.

    All parameters are obtained from a site configuration file.

    For more information see:
        https://developer.wordpress.org/cli/commands/core/download/

    Args:
        site_configuration: parsed site configuration.
        destination_path: Path where WP-CLI will be downloaded.
    """
    pass


def install_wordpress(site_configuration: dict, wordpress_path: str, wordpress_admin_password: str):
    """Installs WordPress core files using WP-CLI.

    All parameters are obtained from a site configuration file.

    For more information see:
        https://developer.wordpress.org/cli/commands/core/install/

    Args:
        site_configuration: parsed site configuration.
        wordpress_path: Path to WordPress files.
        wordpress_admin_password: Password for the WordPress administrator user
    """
    pass


def reset_database(site_configuration: dict, wordpress_path: str):
    """Removes all WordPress core tables from the database using WP-CLI.

    All parameters are obtained from a site configuration file.

    For more information see:
        https://developer.wordpress.org/cli/commands/db/reset/

    Args:
        site_configuration: parsed site configuration.
        wordpress_path: Path to WordPress files.
    """
    pass


def import_database(site_configuration: dict, wordpress_path: str, dump_file_path: str):
    """Imports a WordPress database from a dump file using WP-CLI.

    All parameters are obtained from a site configuration file.

    For more information see:
        https://developer.wordpress.org/cli/commands/db/import/

    Args:
        site_configuration: parsed site configuration.
        wordpress_path: Path to WordPress files.
        dump_file_path: Path to dump file to be imported.
    """
    pass


def set_database_configuration(site_configuration: dict, wordpress_path: str, database_user_password: str):
    """Sets all WordPress database configuration parameters in wp-config.php
    using WP-CLI.

    All parameters are obtained from a site configuration file.

    For more information see:
        https://developer.wordpress.org/cli/commands/config/set/

    Args:
        site_configuration: parsed site configuration.
        wordpress_path: Path to WordPress files.
        database_user_password: Password for the database user configured in at
            the wp-config.php file.
    """
    pass


def export_database(site_configuration: dict, wordpress_path: str, dump_file_path: str):
    """Exports a WordPress database to a dump file using WP-CLI.

    All parameters are obtained from a site configuration file.

    For more information see:
        https://developer.wordpress.org/cli/commands/db/export/

    Args:
        site_configuration: parsed site configuration.
        wordpress_path: Path to WordPress files.
        dump_file_path: Path to the destination dump file.
    """
    pass


def create_configuration_file(site_configuration: dict, wordpress_path: str, database_user_password: str):
    """Creates the wp-config-php WordPress configuration file using WP-CLI.

    All parameters are obtained from a site configuration file.

    For more information see:
        https://developer.wordpress.org/cli/commands/config/create/

    Args:
        site_configuration: parsed site configuration.
        wordpress_path: Path to WordPress files.
        database_user_password: Password for the database user configured in at
            the wp-config.php file.
    """
    pass


def set_configuration_value(name: str, value: str, value_type: ValueType, wordpress_path: str):
    """Creates or updates a value (constant or variable) at the wp-config-php
    WordPress configuration file using WP-CLI.

    For more information see:
        https://developer.wordpress.org/cli/commands/config/set/

    Args:
        name: Name for the constant or variable.
        value: Value for the constant or variable.
        value_type: Type to be created (constant or value).
        wordpress_path: Path to WordPress files.
    """
    pass


def update_database_option(option_name: str, option_value: str, wordpress_path: str):
    """Updates an option at the wp_options (*) table in the WordPress
    database using WP-CLI.

    (*) wp_ prefix could change, but this function will work anyway because
        its value is obtained from the wp-config.php configuration file.
    For more information see:
        https://developer.wordpress.org/cli/commands/option/update/

    Args:
        option_name: Name for the option.
        option_value: Value for the option.
        wordpress_path: Path to WordPress files.
    """
    pass


def install_theme_from_configuration_file(site_configuration: dict, wordpress_path: str):
    """Creates the wp-config-php WordPress configuration file using WP-CLI.

    All parameters are obtained from a site configuration file.

    For more information see:
        https://developer.wordpress.org/cli/commands/theme/install/

    Args:
        site_configuration: parsed site configuration.
        wordpress_path: Path to WordPress files.
    """
    pass


if __name__ == "__main__":
    help(__name__)
