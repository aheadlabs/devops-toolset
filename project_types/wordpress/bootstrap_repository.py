"""Generates a WordPress Git repository for local development.

Git repositories should not contain downloadable or third-party files, but you need them for your site to work.
These are the type of files that won't be pushed to the repository and we will download/generate here:
  - WordPress core files
  - This toolset's
  - WordPress themes (parent themes)

Args:
    --project-path: Path to the WordPress installation.
    --environment-path: Path to the environment JSON file.
    --environment-name: Environment name.
    --db-user-password: Password for the database user.
    --db-admin-password: Password for the WordPress admin user.
"""

#! python

import argparse
import core.log_tools
import filesystem.paths as paths
import logging
import pathlib
import os
import requests
import shutil
import tools.argument_validators
import tools.cli
import tools.devops_toolset
import project_types.wordpress.constants as constants
import project_types.wordpress.wptools
from clint.textui import prompt
from core.LiteralsCore import LiteralsCore
from core.app import App
from devops_platforms.constants import Urls
from project_types import wordpress
from project_types.wordpress import wp_cli
from tools import git
from project_types.wordpress.Literals import Literals as WordpressLiterals

app: App = App()
literals = LiteralsCore([WordpressLiterals])


def main(project_path: str, db_user_password: str = None, db_admin_password: str = None):
    """Generates a WordPress Git repository for local development."""

    # Change the working directory
    os.chdir(project_path)

    # Initialize a local Git repository?
    git.git_init(project_path, args.skip_git)

    # Look for *site.json, *site-environments.json and *project-structure.json files in the project path
    required_files_pattern_suffixes = list(map(lambda x: f"*{x[1]}", constants.required_files_suffixes.items()))
    required_files_not_present = paths.files_exist_filtered(project_path, False, required_files_pattern_suffixes)

    # If there are missing required files, ask for using the default ones from GitHub
    if len(required_files_not_present) > 0:
        core.log_tools.log_indented_list(literals.get("wp_required_files_not_found_detail").format(path=project_path),
                                         required_files_not_present, core.log_tools.LogLevel.warning)

        core.log_tools.log_indented_list(literals.get("wp_default_files"), [
            Urls.DEFAULT_WORDPRESS_PROJECT_STRUCTURE, Urls.DEFAULT_SITE_ENVIRONMENTS, Urls.DEFAULT_SITE_CONFIG],
                                         core.log_tools.LogLevel.info)

        # Ask to use defaults
        use_defaults = prompt.yn(literals.get("wp_use_default_files"))

        # If not using defaults, exit
        if not use_defaults:
            logging.critical(literals.get("wp_required_files_mandatory"))
            raise ValueError(literals.get("wp_required_files_not_found").format(project_path))

    # Download defaults from GitHub
    for file in required_files_not_present:
        url = Urls.bootstrap_required_files[file]
        file_name = paths.get_file_name_from_url(url)
        file_path = pathlib.Path.joinpath(pathlib.Path(project_path), file_name)

        response = requests.get(url)
        with open(file_path, "wb") as fw:
            fw.write(response.content)

    # Determine required file paths
    required_file_paths = project_types.wordpress.wptools.get_required_file_paths(
        project_path, required_files_pattern_suffixes)

    # Parsing site configuration file
    site_config = wordpress.wptools.get_site_configuration_from_environment(required_file_paths[1], "localhost")

    # Get wordpress future path (from the constants.json file)
    wordpress_path = wordpress.wptools.get_wordpress_path_from_root_path(project_path)

    # Create project structure
    wordpress.wptools.start_basic_project_structure(project_path, required_file_paths[2])

    # Update / Download devops-toolset
    setup_devops_toolset(project_path)

    # Move themes to content/themes
    move_themes(project_path, site_config["themes"])

    # Download WordPress core files
    wp_cli.download_wordpress(site_config, wordpress_path)

    # Configure WordPress site
    wordpress.wptools.set_wordpress_config(site_config, wordpress_path, db_user_password)

    # Install WordPress site
    wp_cli.install_wordpress_site(site_config, project_path, db_admin_password)

    # Install site theme
    wp_cli.install_theme_from_configuration_file(site_config, project_path)

    # Install site plugins
    wordpress.wptools.install_plugins_from_configuration_file(site_config, project_path)

    # Move initial required files to .devops
    # TODO(ivan.sainz) Move initial required files to .devops

    # Commit git repository
    git.git_commit(args.skip_git)

    # TODO(ivan.sainz) Remove this script from SonarCloud exclusions


def setup_devops_toolset(root_path: str):
    """ Checks if devops toolset is present and up to date. In case not, it will be downloaded
    Args:
        root_path: Project's root path
    """
    devops_path_constant = wordpress.wptools.get_constants()["paths"]["devops"]
    devops_path = os.path.join(root_path + devops_path_constant, "devops-toolset")
    logging.info(literals.get("wp_checking_devops_toolset").format(path=devops_path))
    tools.devops_toolset.update_devops_toolset(devops_path)


def move_themes(root_path: str, theme: dict):
    """ Moves the themes files (<theme>*.zip) to the folder defined under constants themes path
        Args:
            root_path: Project's root path
            theme: Dict node content of the theme object inside site_config
    """
    themes_path_constant = wordpress.wptools.get_constants()["paths"]["content"]["themes"]
    themes_path = os.path.join(root_path + themes_path_constant)
    if theme["source_type"] == "zip":
        shutil.move(theme["source"], themes_path)
        os.remove(os.path.join(themes_path, ".gitkeep"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project-path", action=tools.argument_validators.PathValidator)
    parser.add_argument("--db-user-password", required=True)
    parser.add_argument("--db-admin-password", required=True)
    parser.add_argument("--skip-git", action="store_true", default=False)
    args, args_unknown = parser.parse_known_args()

    tools.cli.print_title(literals.get("wp_title_wordpress_new_repo"))
    main(args.project_path, args.db_user_password, args.db_admin_password)
