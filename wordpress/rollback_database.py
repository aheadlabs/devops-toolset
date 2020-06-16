"""Rollbacks a database using a dump, removing first all existing tables."""

import argparse
import tools.argument_validators
import tools.cli
import wordpress.wptools as wptools
from core.app import App
from core.CommandsCore import CommandsCore
from core.LiteralsCore import LiteralsCore
from tools.commands import Commands as ToolsCommands
from tools.Literals import Literals as ToolsLiterals
from wordpress.Literals import Literals as WordpressLiterals
from wordpress import wp_cli

app: App = App()
literals = LiteralsCore([WordpressLiterals, ToolsLiterals])
commands = CommandsCore([ToolsCommands])


def main(environment_path: str, environment_name: str, wordpress_path: str, database_dump_path: str, quiet: bool):
    """Rollbacks a database using a dump, dropping and re-creating the database

    Args:
        environment_path: Path to the environment file
        environment_name: Environment name
        wordpress_path: Path to WordPress directory.
        database_dump_path: Path to the database dump file to be restored.
        quiet: If True, no questions are asked and defaults are assumed.
    """

    # Get WordPress site configuration from the environment
    site_configuration = wptools.get_site_configuration_from_environment(environment_path, environment_name)

    # Drop the database and create an empty one
    wp_cli.reset_database(site_configuration, wordpress_path, quiet)

    # Imports a dump in the newly created database
    wp_cli.import_database(site_configuration, wordpress_path, database_dump_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("environment-path", action=tools.argument_validators.PathValidator)
    parser.add_argument("environment_name")
    parser.add_argument("wordpress-path", action=tools.argument_validators.PathValidator)
    parser.add_argument("database-dump-path", action=tools.argument_validators.PathValidator)
    parser.add_argument("--quiet", action="store_true", default=False)
    args, args_unknown = parser.parse_known_args()

    tools.cli.print_title(literals.get("wp_title_wordpress_rollback_db"))
    main(args.environment_path, args.environment_name, args.wordpress_path, args.database_dump_path, args.quiet)
