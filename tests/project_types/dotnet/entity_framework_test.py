""" Unit tests for the dotnet/entity_framework.py module"""


import devops_toolset.project_types.dotnet.entity_framework as sut
from devops_toolset.core.app import App
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.dotnet.commands import Commands as DotnetCommands
from devops_toolset.project_types.dotnet.Literals import Literals as DotnetLiterals
from devops_toolset.tools import cli
import json
from unittest import mock
from unittest.mock import patch

app: App = App()
literals = LiteralsCore([DotnetLiterals])
commands = CommandsCore([DotnetCommands])


# region __generate_sql_script()

@mock.patch.object(cli, "call_subprocess")
@patch("logging.info")
def test_generate_sql_script_calls_subprocess(log_info_mock, call_subprocess_mock):
    """ Calls subprocess once."""

    # Arrange
    startup_project_path: str = ""
    script_path: str = ""

    # Act
    sut.__generate_sql_script(startup_project_path, script_path)

    # Assert
    call_subprocess_mock.assert_called_once()

# endregion __generate_sql_script()

# region __get_migrations_list()


@mock.patch.object(cli, "call_subprocess_with_result")
@patch("logging.info")
def test_get_migrations_list_calls_subprocess(log_info_mock, call_subprocess_with_result_mock, migrationsdata):
    """ Calls subprocess once."""

    # Arrange
    startup_project_path: str = ""
    environment: str = ""
    call_subprocess_with_result_mock.return_value = migrationsdata.migrations_list_command_result

    # Act
    result = sut.__get_migrations_list(startup_project_path, environment)

    # Assert
    call_subprocess_with_result_mock.assert_called_once()
    assert type(result) is list

# endregion __get_migrations_list()

# region __parse_data_from_migrations_json_array()


def test_parse_data_from_migrations_json_array_given_migrations_list_returns_parsed_data(migrationsdata):
    """ Given migrations list, returns parsed data."""

    # Arrange
    migrations_list: list = json.loads(migrationsdata.one_migration_and_applied)

    # Act
    migrations, applied_migrations, last_migration_applied = \
        sut.__parse_data_from_migrations_json_array(migrations_list)

    # Assert
    assert migrations == 2
    assert applied_migrations == 1
    assert last_migration_applied == migrations_list[0]["id"]

# endregion __parse_data_from_migrations_json_array()
