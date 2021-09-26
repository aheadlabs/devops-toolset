""" This script will build a Wordpress site based on therequired configuration
files"""

import argparse

import devops_toolset.tools.cli as cli
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.core.app import App
from devops_toolset.project_types.wordpress.Literals import Literals as WordpressLiterals

app: App = App()
literals = LiteralsCore([WordpressLiterals])


def main():
    """Builds a WordPress site based on the site configuration file"""

    # TODO Get basic settings and configuration file, parse everything
    # TODO Create or fix project structure
    # TODO Download WordPress core files if version is newer or not present
    # TODO Set / update WordPress options
    # TODO Install theme/s
    # TODO Configure WordPress site and delete sample configuration file if present
    # TODO Import WXR content
    # TODO Synchronize content with other environment?
    # TODO Generate files artifact
    # TODO Generate SQL artifact

    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args, args_unknown = parser.parse_known_args()
    kwargs = {}
    for kwarg in args_unknown:
        splited = str(kwarg).split("=")
        kwargs[splited[0]] = splited[1]

    cli.print_title(literals.get("wp_title_build_wordpress"))
    main()
