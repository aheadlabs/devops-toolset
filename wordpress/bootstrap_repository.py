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
import requests
import tools.argument_validators
import tools.cli
import wordpress.wptools
from clint.textui import prompt
from core.CommandsCore import CommandsCore
from core.LiteralsCore import LiteralsCore
from core.app import App
from devops.constants import Urls
from tools.commands import Commands as ToolsCommands
from wordpress.Literals import Literals as WordpressLiterals
from tools.Literals import Literals as ToolsLiterals

app: App = App()
#Cambiar literals por wp_literals ?? ccruz
literals = LiteralsCore([WordpressLiterals])
commands = CommandsCore([ToolsCommands])
#nombrarlo tools_literals // entiendo que está asociado a LiteralsCore ?? ccruz
toolsLiterals = LiteralsCore([ToolsLiterals])


def main(project_path: str = None, db_user_password: str = None, db_admin_password: str = None):
    """Generates a WordPress Git repository for local development."""

    # Initialize a local Git repository?
    init_git = prompt.yn(literals.get("wp_init_git_repo"))
    if init_git:
        tools.cli.call_subprocess(commands.get("git_init").format(path=project_path),
                                  log_before_process=[toolsLiterals.get("log_before_process")],
                                  log_after_err=[toolsLiterals.get("log_after_err")],
                                  log_after_out=[toolsLiterals.get("log_after_out")])

    # Look for *site.json, *site-environments.json and *project-structure.json files in the project path
    required_file_patterns = ["*site.json", "*site-environments.json", "*project-structure.json"]
    required_files_not_present = paths.files_exist_filtered(project_path, False, required_file_patterns)

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
    required_file_paths = wordpress.wptools.get_required_file_paths(project_path, required_file_patterns)

    # Create project structure
    # TODO(ivan.sainz) Create project structure

    # Move devops-toolset to .devops
    # TODO(ivan.sainz) Move devops-toolset to .devops

    # Move themes to content/themes
    # TODO(ivan.sainz) Move themes to content/themes

    # Download WordPress core files
    # TODO(ivan.sainz) Download WordPress core files

    # Configure WordPress site
    # TODO(ivan.sainz) Configure WordPress site

    # Install WordPress site
    # TODO(ivan.sainz) Install WordPress site

    # Install site theme
    # TODO(ivan.sainz) Install site theme

    # Install site plugins
    # TODO(ivan.sainz) Install site plugins

    # Move initial required files to .devops
    # TODO(ivan.sainz) Move initial required files to .devops

    # Commit git repository
    # TODO(ccruz) Commit git repository

    # TODO(ivan.sainz) Remove this script from SonarCloud exclusions


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project-path", action=tools.argument_validators.PathValidator)
    parser.add_argument("--db-user-password", required=True)
    parser.add_argument("--db-admin-password", required=True)
    args, args_unknown = parser.parse_known_args()

    tools.cli.print_title(literals.get("wp_title_wordpress_new_repo"))
    main(args.project_path, args.db_user_password, args.db_admin_password)
