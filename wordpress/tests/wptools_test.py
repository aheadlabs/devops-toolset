"""Unit tests for the wordpress.tools file"""

import pytest
import json
import pathlib
import wordpress.wptools as sut
from wordpress.basic_structure_starter import BasicStructureStarter
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

# region get_project_structure()


@patch("builtins.open", new_callable=mock_open, read_data=WordPressData.structure_file_content)
def test_get_project_structure_given_path_reads_and_parses_content(open_file_mock, wordpressdata):
    """Given a path, reads the file and parses the JSON content."""

    # Arrange
    path = wordpressdata.project_structure_path

    # Act
    result = sut.get_project_structure(path)

    # Assert
    assert result == json.loads(WordPressData.structure_file_content)

# endregion

# region get_required_file_paths()


# TODO(team) Finish this test
def test_get_required_file_paths():
    """Given, when, then"""

    # Arrange

    # Act

    # Assert
    assert True

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

# region start_basic_structure

@patch.object(sut, "get_project_structure")
def test_main_given_parameters_must_call_wptools_get_project_structure(get_project_structure_mock, wordpressdata):
    """Given arguments, must call get_project_structure with passed project_path"""
    # Arrange
    project_structure_path = wordpressdata.project_structure_path
    root_path = wordpressdata.wordpress_path
    get_project_structure_mock.return_value = {"items": {}}
    # Act
    sut.start_basic_project_structure(root_path, project_structure_path)
    # Assert
    get_project_structure_mock.assert_called_once_with(project_structure_path)


@patch.object(sut, "get_project_structure")
@patch.object(BasicStructureStarter, "add_item")
def test_main_given_parameters_must_call_add_item(add_item_mock, get_project_structure_mock, wordpressdata):
    """Given arguments, must call get_project_structure with passed project_path"""
    # Arrange
    project_structure_path = wordpressdata.project_structure_path
    root_path = wordpressdata.wordpress_path
    items_data = {"items": {'foo_item': 'foo_value'}}
    get_project_structure_mock.return_value = items_data
    # Act
    sut.start_basic_project_structure(root_path, project_structure_path)
    # Assert
    add_item_mock.assert_called_once_with('foo_item', root_path)

# endregion start_basic_structure
