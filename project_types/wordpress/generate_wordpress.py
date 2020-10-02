""" This scripts will generate and configure a Wordpress based on the required configuration files"""


import argparse
import logging
import os
import pathlib
import requests
import core
import filesystem.paths as paths
import project_types.wordpress.constants as constants
import project_types.wordpress.wptools
import tools.argument_validators
import tools.cli
import tools.devops_toolset
from clint.textui import prompt
from core.LiteralsCore import LiteralsCore
from core.app import App
from devops_platforms.constants import Urls
from project_types import wordpress
from project_types.wordpress.Literals import Literals as WordpressLiterals

#! python


app: App = App()
literals = LiteralsCore([WordpressLiterals])


# TODO (alberto.carbonell) Check .gitkeep not deleted on /database
def main(root_path: str, db_user_password: str = None, db_admin_password: str = None, environment: str = "localhost"):
    """ Generates a new Wordpress based on the required configuration files"""

    # Look for *site.json, *site-environments.json and *project-structure.json files in the project path
    required_files_pattern_suffixes = list(map(lambda x: f"*{x[1]}", constants.required_files_suffixes.items()))
    required_files_not_present = paths.files_exist_filtered(root_path, False, required_files_pattern_suffixes)

    # If there are missing required files, ask for using the default ones from GitHub if quiet flag is activated
    if len(required_files_not_present) > 0:
        core.log_tools.log_indented_list(literals.get("wp_required_files_not_found_detail").format(path=root_path),
                                         required_files_not_present, core.log_tools.LogLevel.warning)

        core.log_tools.log_indented_list(literals.get("wp_default_files"), [
            Urls.DEFAULT_WORDPRESS_PROJECT_STRUCTURE, Urls.DEFAULT_SITE_ENVIRONMENTS, Urls.DEFAULT_SITE_CONFIG],
                                         core.log_tools.LogLevel.info)

        # NOTE: Devops engine won't call this script with "localhost" environment.
        if environment == "localhost":
            # Ask to use defaults
            use_defaults = prompt.yn(literals.get("wp_use_default_files"))
            # If not using defaults, exit
            if not use_defaults:
                logging.critical(literals.get("wp_required_files_mandatory"))
                raise ValueError(literals.get("wp_required_files_not_found").format(path=root_path))
        else:
            logging.critical(literals.get("wp_required_files_mandatory"))
            raise ValueError(literals.get("wp_required_files_not_found").format(path=root_path))

        # Download defaults from GitHub
        for file in required_files_not_present:
            url = Urls.bootstrap_required_files[file]
            file_name = paths.get_file_name_from_url(url)
            file_path = pathlib.Path.joinpath(pathlib.Path(root_path), file_name)

            response = requests.get(url)
            with open(file_path, "wb") as fw:
                fw.write(response.content)

    # Determine required file paths
    required_file_paths = project_types.wordpress.wptools.get_required_file_paths(
        root_path, required_files_pattern_suffixes)

    # Parsing site configuration file
    site_config = wordpress.wptools.get_site_configuration_from_environment(required_file_paths[1], environment)

    # Get wordpress future path (from the constants.json file)
    wordpress_path = wordpress.wptools.get_wordpress_path_from_root_path(root_path)

    # Create project structure
    wordpress.wptools.start_basic_project_structure(root_path, required_file_paths[2])

    # Update / Download devops-toolset
    setup_devops_toolset(root_path)

    # Download WordPress core files
    wordpress.wptools.download_wordpress(site_config, wordpress_path)

    # Configure WordPress site
    wordpress.wptools.set_wordpress_config_from_configuration_file(site_config, wordpress_path, db_user_password)

    # Install WordPress site
    wordpress.wptools.install_wordpress_site(site_config, root_path, db_admin_password)

    # Install site theme
    wordpress.wptools.install_theme_from_configuration_file(site_config, root_path)

    # Install site plugins
    wordpress.wptools.install_plugins_from_configuration_file(site_config, root_path)


def setup_devops_toolset(root_path: str):
    """ Checks if devops toolset is present and up to date. In case not, it will be downloaded
    Args:
        root_path: Project's root path
    """
    devops_path_constant = wordpress.wptools.get_constants()["paths"]["devops"]
    devops_path = os.path.join(root_path + devops_path_constant, "devops-toolset")
    logging.info(literals.get("wp_checking_devops_toolset").format(path=devops_path))
    tools.devops_toolset.update_devops_toolset(devops_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project-path", action=tools.argument_validators.PathValidator)
    parser.add_argument("--db-user-password", required=True)
    parser.add_argument("--db-admin-password", required=True)
    parser.add_argument("--environment", default="localhost")
    args, args_unknown = parser.parse_known_args()

    tools.cli.print_title(literals.get("wp_title_generate_wordpress"))
    main(args.project_path, args.db_user_password, args.db_admin_password, args.environment)