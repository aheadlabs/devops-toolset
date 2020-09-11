"""Contains wrappers for WP CLI commands"""

import logging
import requests
import os
import stat
import pathlib
import tools.cli as cli
import project_types.wordpress.wptools as wptools
import tools.xcoding64 as base64tools
import filesystem.paths
import sys
import tools.git
from core.app import App
from core.LiteralsCore import LiteralsCore
from project_types.wordpress.Literals import Literals as WordpressLiterals
from core.CommandsCore import CommandsCore
from project_types.wordpress.commands import Commands as WordpressCommands
from enum import Enum

app: App = App()
literals = LiteralsCore([WordpressLiterals])
commands = CommandsCore([WordpressCommands])


class ValueType(Enum):
    """Defines value types for values at the wp-config.php file"""

    CONSTANT = 1,
    VARIABLE = 2


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
    database_props = site_configuration["database"]
    skip_check = wptools.convert_wp_parameter_skip_check(database_props["skip_check"])
    debug_info = wptools.convert_wp_parameter_debug(site_configuration["wp_cli"]["debug"])
    tools.cli.call_subprocess(commands.get("wpcli_config_create").format(
        path=wordpress_path,
        db_host=database_props["host"],
        db_name=database_props["name"],
        db_user=database_props["user"],
        db_pass=database_user_password,
        db_prefix=database_props["prefix"],
        db_charset=database_props["charset"],
        db_collate=database_props["collate"],
        skip_check=skip_check,
        debug_info=debug_info
    ), log_before_process=[literals.get("wp_wpcli_creating_config")],
        log_after_out=[literals.get("wp_wpcli_config_created_ok")],
        log_after_err=[literals.get("wp_wpcli_config_create_err")]
    )


def create_wp_cli_bat_file(phar_path: str):
    """Creates a .bat file for WP-CLI.

    Args:
        phar_path: Path to the .phar file.
    """

    path = pathlib.Path(phar_path)
    bat_path = pathlib.Path.joinpath(path.parent, "wp.bat")

    with open(bat_path, "w") as bat:
        bat.write("@ECHO OFF\n")
        bat.write(f"php \"{phar_path}\" %*")


def download_wordpress(site_configuration: dict, destination_path: str):
    """ Downloads the latest version of the WordPress core files using WP-CLI.

    For more information see:
        https://developer.wordpress.org/cli/commands/core/download/

    Args:
        site_configuration: parsed site configuration.
        destination_path: Path where WP-CLI will be downloaded.
    """

    if not filesystem.paths.is_valid_path(destination_path):
        raise ValueError(literals.get("wp_non_valid_dir_path"))

    version = site_configuration["settings"]["version"]
    locale = site_configuration["settings"]["locale"]
    skip_content = wptools.convert_wp_parameter_skip_content(site_configuration["settings"]["skip_content_download"])
    debug_info = wptools.convert_wp_parameter_debug(site_configuration["wp_cli"]["debug"])
    content = wptools.convert_wp_parameter_content(skip_content)

    cli.call_subprocess(commands.get("wpcli_core_download").format(
        version=version,
        locale=locale,
        path=destination_path,
        skip_content=skip_content,
        debug_info=debug_info
    ), log_before_process=[
        literals.get("wp_wpcli_downloading_wordpress").format(version=version, locale=locale, content=content),
        literals.get("wp_wpcli_downloading_path").format(path=destination_path),
        literals.get("wp_wpcli_downloading_content").format(content=content)],
        log_after_out=[
            literals.get("wp_wpcli_downloading_wordpress_ok")],
        log_after_err=[
            literals.get("wp_wpcli_downloading_wordpress_err")]
    )

    tools.git.purge_gitkeep(destination_path)


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
    debug_info = wptools.convert_wp_parameter_debug(site_configuration["wp_cli"]["debug"])
    cli.call_subprocess(commands.get("wpcli_db_export").format(
        core_dump_path=dump_file_path,
        path=wordpress_path,
        debug_info=debug_info),
        log_before_out=[literals.get("wp_wpcli_db_export_before")],
        log_after_err=[literals.get("wp_wpcli_db_export_error")])


def import_database(wordpress_path: str, dump_file_path: str):
    """Imports a WordPress database from a dump file using WP-CLI.

    All parameters are obtained from a site configuration file.

    Args:
        wordpress_path: Path to WordPress files.
        dump_file_path: Path to dump file to be imported.
    """
    dump_file_path_as_posix = str(pathlib.Path(dump_file_path).as_posix())
    wordpress_path_as_posix = str(pathlib.Path(wordpress_path).as_posix())

    cli.call_subprocess(commands.get("wpcli_db_import").format(
        file=dump_file_path_as_posix, path=wordpress_path_as_posix),
                        log_before_process=[literals.get("wp_wpcli_db_import_before"), dump_file_path],
                        log_after_err=[literals.get("wp_wpcli_db_import_error")])


def install_theme_from_configuration_file(site_configuration: dict, root_path: str):
    """Installs WordPress's theme files (and child themes also) using WP-CLI.

    All parameters are obtained from a site configuration file.

    For more information see:
        https://developer.wordpress.org/cli/commands/theme/install/

    Args:
        site_configuration: parsed site configuration.
        root_path: Path to project root.
    """
    # Add constants
    constants = wptools.get_constants()

    # Set/expand variables before using WP CLI
    debug_info = wptools.convert_wp_parameter_debug(site_configuration["wp_cli"]["debug"])
    theme_name = site_configuration["themes"]["name"]
    theme_source = site_configuration["themes"]["source"]
    database_path = root_path + constants["paths"]["database"]
    wordpress_path = root_path + constants["paths"]["wordpress"]
    database_core_dump_path = os.path.join(database_path, site_configuration["database"]["dumps"]["core"])
    themes_path = os.path.join(root_path + constants["paths"]["content"]["themes"], theme_name)
    wordpress_path_as_posix = str(pathlib.Path(wordpress_path).as_posix())
    database_core_dump_path_as_posix = str(pathlib.Path(database_core_dump_path).as_posix())
    themes_path_as_posix = str(pathlib.Path(themes_path).as_posix())
    wordpress_theme_regex_filter = filter(lambda elem: elem["key"] == "wordpress-theme", constants["regex_base64"])
    wordpress_theme_regex = next(wordpress_theme_regex_filter)["value"]
    regex_wordpress_theme = base64tools.decode(wordpress_theme_regex)

    # Install and activate WordPress theme
    cli.call_subprocess(commands.get("wpcli_theme_install").format(
        path=wordpress_path_as_posix,
        source=theme_source,
        activate="--activate",
        debug_info=debug_info),
        log_before_process=[literals.get("wp_wpcli_theme_install_before").format(theme_name=theme_name)],
        log_after_err=[literals.get("wp_wpcli_theme_install_error").format(theme_name=theme_name)])
    if site_configuration["themes"]["has_child"]:
        # This operation should take from a theme named <theme>.zip, a <theme>-child.zip path
        child_theme_path = themes_path_as_posix.replace(pathlib.Path(themes_path_as_posix).suffixes,
                                                        "-child" + pathlib.Path(themes_path_as_posix).suffixes)
        child_theme_path_as_posix = str(pathlib.Path(child_theme_path).as_posix())
        cli.call_subprocess(commands.get("wpcli_theme_install").format(
            path=wordpress_path_as_posix,
            activate="--activate",
            source=child_theme_path_as_posix,
            debug_info=debug_info),
            log_before_process=[literals.get("wp_wpcli_theme_install_before").format(theme_name=theme_name)],
            log_after_err=[literals.get("wp_wpcli_theme_install_error").format(theme_name=theme_name)])
    export_database(site_configuration, wordpress_path_as_posix, database_core_dump_path_as_posix)


def install_wordpress_core(site_config: dict, wordpress_path: str, admin_password: str):
    """Installs WordPress core files using WP-CLI.

        All parameters are obtained from a site configuration file.

        For more information see:
            https://developer.wordpress.org/cli/commands/core/install/

        Args:
            site_config: parsed site configuration.
            wordpress_path: Path to WordPress files.
            admin_password: Password for the WordPress administrator user
        """
    # Set/expand variables before using WP CLI
    debug_info = wptools.convert_wp_parameter_debug(site_config["wp_cli"]["debug"])
    admin_password_converted = wptools.convert_wp_parameter_admin_password(admin_password)
    skip_email = wptools.convert_wp_parameter_skip_email(site_config["settings"]["admin"]["skip_email"])
    cli.call_subprocess(commands.get("wpcli_core_install").format(
        path=wordpress_path,
        url=site_config["settings"]["wp_config"]["site_url"]["value"],
        title=site_config["settings"]["title"],
        admin_user=site_config["settings"]["admin"]["user"],
        admin_email=site_config["settings"]["admin"]["email"],
        admin_password=admin_password_converted,
        skip_email=skip_email,
        debug_info=debug_info),
        log_before_process=[literals.get("wp_wpcli_core_install_before")],
        log_after_err=[literals.get("wp_wpcli_core_install_error")]
    )


def install_wordpress_site(site_configuration: dict, root_path: str, admin_password: str):
    """Installs WordPress core files using WP-CLI.

    This operation requires cleaning the db and doing a backup after the process.

    For more information see:
        https://developer.wordpress.org/cli/commands/core/install/

    Args:
        site_configuration: parsed site configuration.
        root_path: Path to site installation.
        admin_password: Password for the WordPress administrator user
    """
    # Add constants
    constants = wptools.get_constants()

    database_path = constants["paths"]["database"]
    wordpress_path = root_path + constants["paths"]["wordpress"]
    database_core_dump_path = os.path.join(root_path + database_path, site_configuration["database"]["dumps"]["core"])
    database_core_dump_path_as_posix = str(pathlib.Path(database_core_dump_path).as_posix())
    wordpress_path_as_posix = str(pathlib.Path(wordpress_path).as_posix())

    # Reset database
    reset_database(wordpress_path_as_posix, True, site_configuration["wp_cli"]["debug"])

    # Install wordpress
    install_wordpress_core(site_configuration, wordpress_path_as_posix, admin_password)

    # Update description option
    description = site_configuration["settings"]["description"]
    update_database_option("blogdescription", description, wordpress_path, site_configuration["wp_cli"]["debug"])

    # Backup database
    export_database(site_configuration, wordpress_path, database_core_dump_path_as_posix)


def install_wp_cli(install_path: str = "/usr/local/bin/wp"):
    """Downloads and installs the latest version of WP-CLI.

    For more information see:
        https://make.wordpress.org/cli/handbook/installing/

    Args:
        install_path: Path where WP-CLI will be installed. It must be in the
            PATH/BIN of the operating system.
    """

    wp_cli_phar = "wp-cli.phar"
    wp_cli_download_url = f"https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/{wp_cli_phar}"
    install_path = pathlib.Path(install_path)
    file_path = pathlib.Path.joinpath(install_path, wp_cli_phar)

    if not pathlib.Path.is_dir(install_path):
        raise ValueError(literals.get("wp_not_dir"))

    logging.info(literals.get("wp_wpcli_downloading").format(url=wp_cli_download_url))
    response = requests.get(wp_cli_download_url)

    with open(file_path, "wb") as wp_cli:
        wp_cli.write(response.content)

    file_stat = os.stat(file_path)
    os.chmod(file_path, file_stat.st_mode | stat.S_IEXEC)

    if sys.platform == "win32":
        create_wp_cli_bat_file(file_path)

    cli.call_subprocess(commands.get("wpcli_info"),
                        log_before_out=[literals.get("wp_wpcli_install_ok"), literals.get("wp_wpcli_info")],
                        log_after_out=[literals.get("wp_wpcli_add_ev")])


def reset_database(wordpress_path: str, quiet: bool, debug_info: bool):
    """Removes all WordPress core tables from the database using WP-CLI.

    For more information see:
        https://developer.wordpress.org/cli/commands/db/reset/

    Args:
        wordpress_path: Path to WordPress files.
        quiet: If True, no questions are asked.
    """
    cli.call_subprocess(commands.get("wpcli_db_reset").format(
        path=wordpress_path,
        yes=wptools.convert_wp_parameter_yes(quiet),
        debug_info=wptools.convert_wp_parameter_debug(debug_info)),
        log_before_process=[literals.get("wp_wpcli_db_reset_before")],
        log_after_err=[literals.get("wp_wpcli_db_reset_error")])


def reset_transients(wordpress_path: str):
    """Removes all WordPress transients from database using WP-CLI

    Args:
        wordpress_path: Path to WordPress files.
    """

    cli.call_subprocess(commands.get("wpcli_db_delete_transient").format(path=wordpress_path),
                        log_before_out=[literals.get("wp_wpcli_delete_transients")],
                        log_after_err=[literals.get("wp_wpcli_delete_transients_err")])


def set_configuration_value(name: str, value: str, value_type: ValueType, wordpress_path: str, with_debug: bool):
    """Creates or updates a value (constant or variable) at the wp-config-php
    WordPress configuration file using WP-CLI.

    For more information see:
        https://developer.wordpress.org/cli/commands/db/import/

        Args:
            name: Name of the parameter
            value: Value of the parameter
            value_type: CONSTANT or VARIABLE
            wordpress_path: Path to WordPress files.
            with_debug: Toggles --debug_info as a parameter inside the command.
    """
    debug_info = wptools.convert_wp_parameter_debug(with_debug)
    # This value will place the value as it gets, without quotes
    raw = "--raw" if type(value) is not str else ""
    cli.call_subprocess(commands.get("wpcli_config_set").format(
        name=name,
        value=value,
        raw=raw,
        type=value_type,
        path=wordpress_path,
        debug_info=debug_info
    ),  log_after_err=[literals.get("wp_wpcli_config_set_value_err")]
    )


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


def update_database_option(option_name: str, option_value: str, wordpress_path: str, debug_info: bool):
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
        debug_info: Toggles debug info on the command.
    """
    debug_info = wptools.convert_wp_parameter_debug(debug_info)
    cli.call_subprocess(commands.get("wpcli_option_update").format(
        option_name=option_name,
        option_value=option_value,
        path=wordpress_path,
        debug_info=debug_info),
        log_before_process=[literals.get("wp_wpcli_option_update_before").format(
            option_name=option_name,
            option_value=option_value)],
        log_after_err=[literals.get("wp_wpcli_option_update_error").format(
            option_name=option_name,
            option_value=option_value)])


if __name__ == "__main__":
    help(__name__)
