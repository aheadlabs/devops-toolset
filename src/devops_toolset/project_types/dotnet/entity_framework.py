"""Entity Framework utilities"""
import json

from devops_toolset.core.app import App
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.dotnet.Literals import Literals as DotnetLiterals
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.project_types.dotnet.commands import Commands as DotnetCommands

import devops_toolset.filesystem.parsers as parsers
import devops_toolset.tools.cli as cli
import logging

app: App = App()
platform_specific = app.load_platform_specific("environment")
literals = LiteralsCore([DotnetLiterals])
commands = CommandsCore([DotnetCommands])


def generate_migration_sql_script(startup_project_path: str, environment: str, script_path: str):
    """ Gets a list of the migrations applied for a specific environment

    Args:
        startup_project_path: Path to the startup project
        environment: Name for the environment to get the migrations for
        script_path: Path to the SQL script to be generated

    Returns:
        Migrations JSON array
    """
    migrations_list: list = get_migrations_list(startup_project_path, environment)
    migrations, applied_migrations, last_migration_applied = parse_data_from_migrations_json_array(migrations_list)
    generate_sql_script(startup_project_path, script_path, last_migration_applied)


def generate_sql_script(
        startup_project_path: str, script_path: str, migration_from: str = "0", idempotent: bool = True):
    """ Generates a SQL script to apply ad hoc migrations to DBMS

    Args:
        startup_project_path: Path to the startup project
        script_path: Path where the script will be generated at
        migration_from: ID or name of the last migration applied, defaults to 0
        idempotent: Creates an idempotent SQL script if True
    """

    logging.info(literals.get("dotnet_ef_migrations_script"))

    cli.call_subprocess(commands.get("dotnet_ef_migrations_script").format(
        migration_from=migration_from,
        path=startup_project_path,
        script_path=script_path,
        idempotent="--idempotent" if idempotent else ""
    ))


def get_migrations_list(startup_project_path: str, environment: str) -> list:
    """ Gets a list of the migrations applied for a specific environment

    Args:
        startup_project_path: Path to the startup project
        environment: Name for the environment to get the migrations for

    Returns:
        Migrations JSON array
    """

    logging.info(literals.get("dotnet_ef_migrations_list"))

    result: str = cli.call_subprocess_with_result(commands.get("dotnet_ef_migrations_list").format(
        path=startup_project_path,
        env=environment
    ))

    migrations: str = ""
    json_lure: bool = False
    for line in result.splitlines():
        if line.startswith("[") and not json_lure:
            json_lure = True
        if json_lure:
            migrations += line

    return json.loads(migrations)


def parse_data_from_migrations_json_array(migrations_json_array: list) -> (int, int, str):
    """ Parses data from the migrations JSON array

    Arguments:
        migrations_json_array: Migrations JSON array

    Returns:
        Number of migrations, number of applied migrations, last applied
        migration name
    """

    last_applied_migration: str = "0"
    applied_migrations: int = 0
    for migration in migrations_json_array:
        if migration["applied"]:
            last_applied_migration = migration["id"]
            applied_migrations += 1

    return len(migrations_json_array), applied_migrations, last_applied_migration


if __name__ == "__main__":
    help(__name__)
    generate_migration_sql_script(
        r"D:\Source\_aheadlabs\signatus\0.DistributedServicesLayer\SignatusApi\SignatusApi.csproj",
        "Development",
        r"D:\Source\_aheadlabs\signatus\0.DistributedServicesLayer\SignatusApi\migration.sql")
