"""Downloads the last version of WordPress core files"""

import argparse
import wordpress.wptools
import wordpress.wp_cli
from core.app import App
from core.LiteralsCore import LiteralsCore
from wordpress.Literals import Literals as WordpressLiterals

app: App = App()
literals = LiteralsCore([WordpressLiterals])


def main(wordpress_path, environment_path, environment_name):
    """Downloads the last version of WordPress core files"""

    site_configuration_path: str = \
        wordpress.wptools.get_site_configuration_path_from_environment(environment_path, environment_name)

    site_configuration: dict = wordpress.wptools.get_site_configuration(site_configuration_path)

    wordpress.wp_cli.download_wordpress(site_configuration, wordpress_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wordpress-path", required=True)
    parser.add_argument("--environment-path", required=True)
    parser.add_argument("--environment-name", required=True)
    args, args_unknown = parser.parse_known_args()
    main(args.wordpress_path, args.environment_path, args.environment_name)
