""" Unit-core for the dotnet/cli.py module"""

import pytest

import project_types as sut
from core.CommandsCore import CommandsCore
from core.LiteralsCore import LiteralsCore
from project_types.dotnet import Commands as DotnetCommands
from project_types.dotnet import Literals as DotnetLiterals
from core.app import App

app: App = App()
literals = LiteralsCore([DotnetLiterals])
commands = CommandsCore([DotnetCommands])


# region convert_debug_parameter()

@pytest.mark.parametrize("value,expected", [(False, ""), (True, "--verbosity=diagnostic")])
def test_convert_debug_parameter_returns_conversion_argument(value, expected):
    """ Given value argument, should test the two possibilities and return desired value """
    # Arrange
    # Act
    result = sut.convert_debug_parameter(value)
    # Assert
    assert result == expected

# endregion convert_debug_parameter()

# region convert_force_parameter()


@pytest.mark.parametrize("value,expected", [(False, ""), (True, "--force")])
def test_convert_force_parameter_returns_conversion_argument(value, expected):
    """ Given value argument, should test the two possibilities and return desired value """
    # Arrange
    # Act
    result = sut.convert_force_parameter(value)
    # Assert
    assert result == expected

# endregion convert_force_parameter()

# region convert_with_restore_parameter()


@pytest.mark.parametrize("value,expected", [(False, "--no-restore"), (True, "")])
def test_convert_with_restore_parameter_returns_conversion_argument(value, expected):
    """ Given value argument, should test the two possibilities and return desired value """
    # Arrange
    # Act
    result = sut.convert_with_restore_parameter(value)
    # Assert
    assert result == expected

# endregion convert_with_restore_parameter()

# region restore()

# endregion restore()

# region build()

# endregion build()
