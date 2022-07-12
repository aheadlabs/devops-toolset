"""Test configuration file for dotnet package.

This code is executed once per unit test session.
Add here whatever you want to pass as a fixture in your core.

    ie: (see FileNames example)
        - Add a class that contains what you want to pass as a fixture in your core.
        - Create a fixture with that same lowered name that returns an instance to that class."""
import typing

import pytest


class DotNetData(object):
    """Class used to create the dotnetdata fixture"""

    csproj_file_content = "<Project><PropertyGroup><Version>6.6.6</Version></PropertyGroup></Project>"

    @staticmethod
    def get_appsettings_files() -> typing.Generator:
        for file in ["appsettings.Development.json", "appsettings.Staging.json", "appsettings.Production.json"]:
            yield file

    @staticmethod
    def get_wrong_appsettings_files() -> typing.Generator:
        for file in ["appsettings.1.json", "appsettings.2.json"]:
            yield file


class GitData(object):
    """ Class used to create the gitdata fixture """

    branch = "heads/refs/dev"
    tag = "v1.0.0"
    commit = "fdr564"
    auth_header = "bearer 1234"


class MigrationsData(object):
    """Class used to create the migrationsdata fixture"""

    one_migration_and_applied = \
        "[{\"id\":\"20220529212511_Init-V1\",\"name\":\"Init-V1\",\"safeName\":\"Init-V1\",\"applied\":true}," \
        "{\"id\":\"20220529212512_Second-V2\",\"name\":\"Second-V2\",\"safeName\":\"Second-V2\",\"applied\":false}]"

    migrations_list_command_result = \
        "info: Microsoft.EntityFrameworkCore.Infrastructure[10403]\n" \
        "      Executed DbCommand (22ms) [Parameters=[], CommandType='Text', CommandTimeout='30']\n" \
        "[{\"id\":\"20220529212511_Init-V1\",\"name\":\"Init-V1\",\"safeName\":\"Init-V1\",\"applied\":true}]"


@pytest.fixture
def dotnetdata():
    """Sample data for testing .NET related functionality"""
    return DotNetData()


@pytest.fixture
def gitdata():
    """Sample data for testing Git functionality"""
    return GitData()


@pytest.fixture
def migrationsdata():
    """Sample data for testing Entity Framework functionality"""
    return MigrationsData()
