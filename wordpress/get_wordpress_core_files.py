"""Downloads the last version of WordPress core files"""

import argparse
from core.app import App
import wordpress.tools
import wordpress.wp_cli
from core.LiteralsCore import LiteralsCore
from wordpress.Literals import Literals as WordpressLiterals

parser = argparse.ArgumentParser()
parser.add_argument("--wordpress-path")
parser.add_argument("--environment-path")
parser.add_argument("--environment-name")
args, args_unknown = parser.parse_known_args()

app: App = App()
literals = LiteralsCore([WordpressLiterals])


def main(wordpress_path: str = None, environment_path: str = None, environment_name: str = None):
    """Downloads the last version of WordPress core files"""

    if not wordpress_path or wordpress_path.strip() == "":
        raise ValueError(literals.get("wp_wordpress_path_mandatory"))

    if not environment_path or environment_path.strip() == "":
        raise ValueError(literals.get("wp_environment_path_mandatory"))

    if not environment_name or environment_name.strip() == "":
        raise ValueError(literals.get("wp_environment_name_mandatory"))

    site_configuration_path: str = \
        wordpress.tools.get_site_configuration_path_from_environment(environment_path, environment_name)

    site_configuration: dict = wordpress.tools.get_site_configuration(site_configuration_path)

    wordpress.wp_cli.download_wordpress(site_configuration, wordpress_path)


if __name__ == "__main__":
    main(args.wordpress_path, args.environment_path, args.environment_name)
