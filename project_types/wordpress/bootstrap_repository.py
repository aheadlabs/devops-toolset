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
import os
import tools.argument_validators
import tools.cli
import tools.devops_toolset
from core.LiteralsCore import LiteralsCore
from core.app import App
from project_types.wordpress import generate_wordpress
from project_types.wordpress.Literals import Literals as WordpressLiterals
from tools import git

app: App = App()
literals = LiteralsCore([WordpressLiterals])


# TODO (alberto.carbonell) Check if database and db users exist and if not, prompt to create them
def main(project_path: str, db_user_password: str = None, db_admin_password: str = None):
    """Generates a WordPress Git repository for local development."""

    # Change the working directory
    os.chdir(project_path)

    # Initialize a local Git repository?
    git.git_init(project_path, args.skip_git)

    # Generate wordpress with the required data
    generate_wordpress.main(project_path, db_user_password, db_admin_password)

    # Move initial required files to .devops
    # TODO(ivan.sainz) Move initial required files to .devops

    # Commit git repository
    git.git_commit(args.skip_git)

    # TODO(ivan.sainz) Remove this script from SonarCloud exclusions


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project-path", action=tools.argument_validators.PathValidator)
    parser.add_argument("--db-user-password", required=True)
    parser.add_argument("--db-admin-password", required=True)
    parser.add_argument("--skip-git", action="store_true", default=False)
    args, args_unknown = parser.parse_known_args()

    tools.cli.print_title(literals.get("wp_title_wordpress_new_repo"))
    main(args.project_path, args.db_user_password, args.db_admin_password)
