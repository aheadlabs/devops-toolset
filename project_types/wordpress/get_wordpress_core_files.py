"""Downloads the last version of WordPress core files.

Args:
    wordpress-path: Path to the WordPress installation.
    environment-path: Path to the environment JSON file.
    environment-name: Environment name.
"""

#! python

import argparse
import tools.argument_validators
import tools.cli
import project_types.wordpress.wptools
import project_types.wordpress.wp_cli
from core.app import App
from core.LiteralsCore import LiteralsCore
from project_types.wordpress.Literals import Literals as WordpressLiterals

app: App = App()
literals = LiteralsCore([WordpressLiterals])


def main(wordpress_path, environment_path, environment_name):
    """Downloads the last version of WordPress core files"""

    # Get path to site configuration file from the environment file
    site_configuration_path: str = \
        project_types.wordpress.wptools.get_site_configuration_path_from_environment(
            environment_path, environment_name)

    # Get site configuration from file
    site_configuration: dict = project_types.wordpress.wptools.get_site_configuration(site_configuration_path)

    # Download WordPress core files based on site configuration
    project_types.wordpress.wp_cli.download_wordpress(site_configuration, wordpress_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("wordpress-path", action=tools.argument_validators.PathValidator)
    parser.add_argument("environment-path", action=tools.argument_validators.PathValidator)
    parser.add_argument("environment_name")
    args, args_unknown = parser.parse_known_args()

    tools.cli.print_title(literals.get("wp_title_wordpress_files"))
    main(args.wordpress_path, args.environment_path, args.environment_name)