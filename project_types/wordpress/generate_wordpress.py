""" This script will generate and configure a Wordpress site based on the
required configuration files"""


import argparse
import logging
import pathlib
import requests
import core
import core.log_tools
import filesystem.paths as paths
import os
import project_types.wordpress.constants as constants
import project_types.wordpress.wptools
import shutil
import tools.argument_validators
import tools.cli
import tools.devops_toolset
import tools.git as git_tools
from clint.textui import prompt
from core.LiteralsCore import LiteralsCore
from core.app import App
from devops_platforms.constants import Urls
from project_types import wordpress
from project_types.wordpress.Literals import Literals as WordpressLiterals

#! python


app: App = App()
literals = LiteralsCore([WordpressLiterals])


def main(root_path: str, db_user_password: str, db_admin_password: str, wp_admin_password: str,
         environment: str, additional_environments: list, additional_environment_db_user_passwords: list,
         create_db: bool, skip_partial_dumps: bool, **kwargs):
    """Generates a new Wordpress site based on the required configuration files

    Args:
        root_path: Path to the repository root.
        db_user_password: Password for the database user.
        db_admin_password: Password for the database admin user.
        wp_admin_password: Password for the WordPress admin user.
        environment: Name of the environment to be processed.
        additional_environments: Additional environments to create additional
            wp-config.php files.
        additional_environment_db_user_passwords: Additional environment db
            user passwords.
        create_db: If True it creates the database and the user.
        skip_partial_dumps: If True skips partial database dumps
            (after installing WordPress, themes and plugins).
        kwargs: Platform-specific arguments
    """
    global_constants = wordpress.wptools.get_constants()
    root_path_obj = pathlib.Path(root_path)
    database_path = global_constants["paths"]["database"]

    # Look for *site.json and *site-environments.json files in the project path
    required_files_pattern_suffixes = list(map(lambda x: f"*{ x[1]}", constants.required_files_suffixes.items()))
    required_files_not_present = paths.files_exist_filtered(root_path, False, required_files_pattern_suffixes)

    # If there are missing required files, ask for using the default ones from GitHub if quiet flag is activated
    if len(required_files_not_present) > 0:
        core.log_tools.log_indented_list(literals.get("wp_required_files_not_found_detail").format(path=root_path),
                                         required_files_not_present, core.log_tools.LogLevel.warning)

        core.log_tools.log_indented_list(literals.get("wp_default_files"), [
            Urls.DEFAULT_WORDPRESS_PROJECT_STRUCTURE, Urls.DEFAULT_SITE_ENVIRONMENTS, Urls.DEFAULT_SITE_CONFIG],
                                         core.log_tools.LogLevel.info)

        # Ask to use defaults
        use_defaults = prompt.yn(literals.get("wp_use_default_files"))
        # If not using defaults, exit
        if not use_defaults:
            logging.critical(literals.get("wp_required_files_mandatory"))
            raise ValueError(literals.get("wp_required_files_not_found").format(path=root_path))

        # Download defaults from GitHub
        for file in required_files_not_present:
            url = Urls.bootstrap_required_files[file]
            file_name = paths.get_file_name_from_url(url)
            file_path = pathlib.Path.joinpath(root_path_obj, file_name)

            response = requests.get(url)
            with open(file_path, "wb") as fw:
                fw.write(response.content)

    # Determine required file paths
    required_file_paths = wordpress.wptools.get_required_file_paths(
        root_path, required_files_pattern_suffixes)
    environment_file_path = required_file_paths[1]

    # Get database admin user from environment
    db_admin_user = wordpress.wptools.get_db_admin_from_environment(environment_file_path, environment)

    # Parsing site configuration file
    site_config = wordpress.wptools.get_site_configuration_from_environment(environment_file_path, environment)

    # Get future paths (from the constants.json file)
    wordpress_path = wordpress.wptools.get_wordpress_path_from_root_path(root_path)
    wordpress_path_as_posix = pathlib.Path(wordpress_path).as_posix()
    themes_path = wordpress.wptools.get_themes_path_from_root_path(root_path)

    # Create project structure & prepare devops-toolset
    wordpress.wptools.start_basic_project_structure(root_path)

    # Check for updates / download devops-toolset
    setup_devops_toolset(root_path)

    # Download WordPress core files
    wordpress.wptools.download_wordpress(site_config, wordpress_path)

    # Set development themes / plugins ready
    wordpress.wptools.build_theme(site_config["themes"], themes_path)

    # Configure WordPress site
    wordpress.wptools.set_wordpress_config_from_configuration_file(site_config, wordpress_path, db_user_password)

    # Create database and users
    if create_db:
        wordpress.wptools.setup_database(
            site_config, wordpress_path, db_user_password, db_admin_user, db_admin_password)

    # Install WordPress site
    wordpress.wptools.install_wordpress_site(site_config, root_path, wp_admin_password, skip_partial_dumps)

    # Add / update WordPress options
    wordpress.wptools.add_wp_options(site_config["settings"]["options"], wordpress_path, site_config["wp_cli"]["debug"])

    # Install site theme
    wordpress.wptools.install_themes_from_configuration_file(site_config, root_path, skip_partial_dumps, **kwargs)

    # Install site plugins
    wordpress.wptools.install_plugins_from_configuration_file(site_config, root_path, skip_partial_dumps)

    # Import wxr content
    wordpress.wptools.import_content_from_configuration_file(site_config, wordpress_path)

    # Generate additional wp-config.php files
    generate_additional_wpconfig_files(environment_file_path, additional_environments,
                                       additional_environment_db_user_passwords, wordpress_path)

    # Delete sample configuration file
    delete_sample_wp_config_file(wordpress_path)

    # Backup database
    core_dump_path_converted = wordpress.wptools.convert_wp_config_token(
        site_config["database"]["dumps"]["core"], wordpress_path)
    database_core_dump_directory_path = pathlib.Path.joinpath(root_path_obj, database_path)
    database_core_dump_path = pathlib.Path.joinpath(database_core_dump_directory_path, core_dump_path_converted)
    wordpress.wptools.export_database(
        site_config, wordpress_path_as_posix, database_core_dump_path.as_posix())
    git_tools.purge_gitkeep(database_core_dump_directory_path.as_posix())


def setup_devops_toolset(root_path: str):
    """ Checks if devops toolset is present and up to date. In case not, it will be downloaded
    Args:
        root_path: Project's root path
    """
    devops_path_constant = wordpress.wptools.get_constants()["paths"]["devops"]
    devops_path = pathlib.Path.joinpath(pathlib.Path(root_path), devops_path_constant, "devops-toolset")
    logging.info(literals.get("wp_checking_devops_toolset").format(path=devops_path))
    tools.devops_toolset.update_devops_toolset(devops_path)


def generate_additional_wpconfig_files(environments_file_path: str, environments: list,
                                       additional_environment_db_user_passwords: list,
                                       wordpress_path: str):
    """Generates additional wp-config.php files for different environments.

    Args:
        environments_file_path: Path to the environments file.
        environments: List of environment configuration files to be generated.
        additional_environment_db_user_passwords: Additional environment db
            user passwords.
        wordpress_path: Path to the WordPress installation.
    """
    wordpress_path_obj = pathlib.Path(wordpress_path)
    wp_config_path = pathlib.Path.joinpath(wordpress_path_obj, "wp-config.php")
    wp_config_path_temp = pathlib.Path.joinpath(wordpress_path_obj, "wp-config-temp.php")

    # Rename original file
    if paths.is_valid_path(wp_config_path.as_posix(), True):
        shutil.move(wp_config_path, wp_config_path_temp)

    i = 0
    while i < len(environments) and environments[i]:
        site_config = wordpress.wptools.get_site_configuration_from_environment(environments_file_path, environments[i])
        wordpress.wptools.set_wordpress_config_from_configuration_file(site_config, wordpress_path,
                                                                       additional_environment_db_user_passwords[i])
        shutil.move(wp_config_path, pathlib.Path.joinpath(wordpress_path_obj, f"wp-config-{environments[i]}.php"))
        i += 1

    # Rename original file
    if paths.is_valid_path(str(wp_config_path_temp), True):
        shutil.move(wp_config_path_temp, wp_config_path)


def delete_sample_wp_config_file(wordpress_path: str):
    """Deletes the wp-config-sample.php file.

    Args:
        wordpress_path: Path to WordPress.
    """
    file_path = pathlib.Path.joinpath(pathlib.Path(wordpress_path), "wp-config-sample.php")
    if file_path.exists():
        os.remove(str(file_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project-path", action=tools.argument_validators.PathValidator)
    parser.add_argument("--db-user-password", required=True)
    parser.add_argument("--db-admin-password", required=True)
    parser.add_argument("--wp-admin-password", required=True)
    parser.add_argument("--environment", default="localhost")
    parser.add_argument("--additional-environments", default="")
    parser.add_argument("--additional-environment-db-user-passwords", default="")
    parser.add_argument("--create-db", action="store_true", default=False)
    parser.add_argument("--skip-partial-dumps", action="store_true", default=False)
    args, args_unknown = parser.parse_known_args()
    kwargs = {}
    for kwarg in args_unknown:
        splited = str(kwarg).split("=")
        kwargs[splited[0]] = splited[1]

    tools.cli.print_title(literals.get("wp_title_generate_wordpress"))
    main(args.project_path, args.db_user_password, args.db_admin_password, args.wp_admin_password,
         args.environment,
         args.additional_environments.split(","),
         args.additional_environment_db_user_passwords.split(","),
         args.create_db, args.skip_partial_dumps, **kwargs)
