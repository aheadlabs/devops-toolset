"""Unit tests for the wordpress.tools file"""

import pytest
import json
import pathlib
import wordpress.wptools as sut
from core.LiteralsCore import LiteralsCore
from wordpress.Literals import Literals as WordpressLiterals
from unittest.mock import patch, mock_open
from wordpress.tests.conftest import WordPressData

literals = LiteralsCore([WordpressLiterals])

# region convert_wp_parameter_content


@pytest.mark.parametrize("value, expected", [(True, "no"), (False, "yes")])
def test_convert_wp_parameter_content(value, expected):
    """When True, returns a "no" string.
    When False, returns a "yes" string."""

    # Arrange

    # Act
    result = sut.convert_wp_parameter_content(value)

    # Assert
    assert result == expected

# endregion

# region convert_wp_parameter_debug


@pytest.mark.parametrize("value, expected", [(True, "--debug"), (False, "")])
def test_convert_wp_parameter_debug(value, expected):
    """When True, returns a --debug string.
    When False, returns an empty string."""

    # Arrange

    # Act
    result = sut.convert_wp_parameter_debug(value)

    # Assert
    assert result == expected

# endregion

# region convert_wp_parameter_skip_content


@pytest.mark.parametrize("value, expected", [(True, "--skip-content"), (False, "")])
def test_convert_wp_parameter_skip_content(value, expected):
    """When True, returns a --skip-content string.
    When False, returns an empty string."""

    # Arrange

    # Act
    result = sut.convert_wp_parameter_skip_content(value)

    # Assert
    assert result == expected

# endregion

# region get_constants()


def test_get_constants_given_path_returns_data(tmp_path, wordpressdata):
    """Given a file path, returns data in a dict"""

    # Arrange
    constants_file_path = str(pathlib.Path.joinpath(tmp_path, wordpressdata.constants_file_name))
    with open(constants_file_path, "w") as constants_file:
        constants_file.write(wordpressdata.constants_file_content)

    # Act
    result = sut.get_constants(constants_file_path)

    # Assert
    assert result == json.loads(wordpressdata.constants_file_content)

# endregion

# region get_site_configuration()


@patch("builtins.open", new_callable=mock_open, read_data=WordPressData.site_config_content)
def test_get_site_configuration_reads_json(builtins_open, wordpressdata):
    """Given a JSON file path, returns dict with JSON content"""

    # Arrange
    path = wordpressdata.site_config_path

    # Act
    result = sut.get_site_configuration(path)

    # Assert
    assert result == json.loads(wordpressdata.site_config_content)

# endregion

# region get_site_configuration_path_from_environment()


@patch("builtins.open", new_callable=mock_open, read_data=WordPressData.environment_file_content)
def test_get_site_configuration_path_from_environment_when_environment_found_returns_config_path(
        builtins_open, wordpressdata):
    """Given arguments, when the environment is found in the JSON file, returns
    the site configuration file path"""

    # Arrange
    environment_path = wordpressdata.environment_path
    environment_name = wordpressdata.environment_name
    expected_path = wordpressdata.site_config_path_from_json

    # Act
    result = sut.get_site_configuration_path_from_environment(environment_path, environment_name)

    # Assert
    assert pathlib.Path(result).as_posix() == expected_path


@patch("builtins.open", new_callable=mock_open, read_data=WordPressData.environment_file_content)
def test_get_site_configuration_path_from_environment_when_environment_not_found_raises_valuerror(
        builtins_open, wordpressdata):
    """Given arguments, when the environment is not found in the JSON file,
    raises Value error with message"""

    # Arrange
    environment_path = wordpressdata.environment_path
    environment_name = wordpressdata.environment_name_fake

    # Act
    with pytest.raises(ValueError) as value_error:
        sut.get_site_configuration_path_from_environment(environment_path, environment_name)

    # Assert
    assert str(value_error.value) == literals.get("wp_env_not_found")


@patch("builtins.open", new_callable=mock_open,
       read_data=WordPressData.environment_file_content_duplicated_environment)
def test_get_site_configuration_path_from_environment_when_more_than_1_environment_found_raises_valuerror(
        builtins_open, wordpressdata):
    """Given arguments, when more than one environment is found in the JSON
    file, raises Value error with message"""

    # Arrange
    environment_path = wordpressdata.environment_path
    environment_name = wordpressdata.environment_name

    # Act
    with pytest.raises(ValueError) as value_error:
        sut.get_site_configuration_path_from_environment(environment_path, environment_name)

    # Assert
    assert str(value_error.value) == literals.get("wp_env_gt1")

# endregion convert_wp_parameter_skip_content()
