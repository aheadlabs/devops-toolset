"""Microsoft Entity Framework utilities"""

from devops_toolset.core.app import App
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.dotnet.Literals import Literals as DotnetLiterals
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.project_types.dotnet.commands import Commands as DotnetCommands

import devops_toolset.project_types.dotnet.utils as utils
import devops_toolset.tools.cli as cli
import json
import logging
import pathlib
import re


app: App = App()
platform_specific = app.load_platform_specific("environment")
literals = LiteralsCore([DotnetLiterals])
commands = CommandsCore([DotnetCommands])


def drop_database(startup_project_path: str, environment: str, no_build: bool = False):
    """ Drops the database

    Args:
        startup_project_path: Path to the startup project
        environment: Name for the environment to get the migrations for
        no_build: Skips build if True
    """
    logging.info(literals.get("dotnet_ef_database_drop"))

    result: str = cli.call_subprocess_with_result(commands.get("dotnet_ef_database_drop").format(
        path=startup_project_path,
        no_build="--no-build" if no_build else "",
        env=environment
    ))
    logging.info(result)


def generate_migration_sql_script(startup_project_path: str, environment: str, script_path: str):
    """ Generates SQL migration script for a specific environment

    Args:
        startup_project_path: Path to the startup project.
        environment: Name for the environment to get the migrations for.
        script_path: Path to the SQL script to be generated.
    """

    migrations_list: list = __get_migrations_list(startup_project_path, environment)
    migration_name, migration_date = __get_first_migration_not_applied(migrations_list)
    migrations, applied_migrations, last_migration_applied = __parse_data_from_migrations_json_array(migrations_list)

    if migration_name is not None and migrations != applied_migrations:
        __generate_sql_script(
            startup_project_path, script_path.replace("#date#", migration_date), environment, last_migration_applied)


def generate_migration_sql_scripts_for_all_environments(
        startup_project_path: str, scripts_base_path: str, include_development: bool = False):
    """ Generates a SQL migration script for every environment configured in
    the appsettings.*.json files.

    Args:
        startup_project_path: Path to the startup project.
        scripts_base_path: Path to the directory where all scripts will be
            created at.
        include_development: If True, Development/Dev is included in the list.
    """

    environments = utils.get_appsettings_environments(startup_project_path, include_development)
    base_path_obj = pathlib.Path(scripts_base_path)

    for environment in environments:
        script_path = pathlib.Path.joinpath(base_path_obj, f"database-migration-{environment.lower()}-from-#date#.sql")
        generate_migration_sql_script(startup_project_path, environment, str(script_path))


def reset_database(startup_project_path: str, environment: str, no_build: bool = False):
    """ Reverts all migrations applied, dropping all tables and truncating
    __efmigrationshistory database

    Args:
        startup_project_path: Path to the startup project.
        environment: Name for the environment to get the migrations for.
        no_build: Skips build if True.
    """
    logging.info(literals.get("dotnet_ef_database_reset"))

    result: str = cli.call_subprocess_with_result(commands.get("dotnet_ef_database_reset").format(
        path=startup_project_path,
        no_build="--no-build" if no_build else "",
        env=environment
    ))
    logging.info(result)


def __generate_sql_script(startup_project_path: str, script_path: str, environment: str,
                          migration_from: str = "0", no_build: bool = False, idempotent: bool = True):
    """ Generates a SQL script to apply ad hoc migrations to DBMS

    Args:
        startup_project_path: Path to the startup project.
        script_path: Path where the script will be generated at.
        environment: Name for the environment to generate the script for.
        migration_from: ID / name of the last migration applied, defaults to 0.
        no_build: Skips build if True.
        idempotent: Creates an idempotent SQL script if True.
    """

    logging.info(literals.get("dotnet_ef_migrations_script"))

    cli.call_subprocess(commands.get("dotnet_ef_migrations_script").format(
        migration_from=migration_from,
        path=startup_project_path,
        script_path=script_path,
        no_build="--no-build" if no_build else "",
        idempotent="--idempotent" if idempotent else "",
        env=environment
    ))


def __get_first_migration_not_applied(migrations_list: list) -> ([str, None], [str, None]):
    """ Returns the first migration in the list that has not been applied.

    Args:
        migrations_list: List of migrations

    Returns:
        Tuple with migration name and migration date (migration format) or None
        and None if no migration is found.
    """

    regex_pattern = r"^(\d+)_[\w-]+$"

    for migration in migrations_list:
        if migration["applied"] is False:
            match = re.search(regex_pattern, migration["id"])
            return migration["name"], match.groups()[0]

    return None, None


def __get_migrations_list(startup_project_path: str, environment: str, no_build: bool = False) -> list:
    """ Gets a list of the migrations applied for a specific environment

    Args:
        startup_project_path: Path to the startup project
        environment: Name for the environment to get the migrations for
        no_build: Skips build if True

    Returns:
        Migrations JSON array
    """

    logging.info(literals.get("dotnet_ef_migrations_list"))

    result: str = cli.call_subprocess_with_result(commands.get("dotnet_ef_migrations_list").format(
        path=startup_project_path,
        no_build="--no-build" if no_build else "",
        env=environment
    ))
    logging.info(result)

    migrations: str = ""
    json_lure: bool = False
    for line in result.splitlines():
        if line.startswith("[") and not json_lure:
            json_lure = True
        if json_lure:
            migrations += line

    return json.loads(migrations)


def __parse_data_from_migrations_json_array(migrations_json_array: list) -> (int, int, str):
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
