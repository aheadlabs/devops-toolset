"""Unit tests for the parsers file"""

import filesystem.parsers as sut
import pathlib
import json
from unittest.mock import patch, mock_open
from core.app import App
from core.LiteralsCore import LiteralsCore
from project_types.wordpress.Literals import Literals as WordpressLiterals

app: App = App()
platform_specific = app.load_platform_specific("environment")
wp_literals = LiteralsCore([WordpressLiterals])

# region parse_project_xml_data()


def test_parse_project_xml_data_when_add_environment_variables_is_false_then_return_dict_with_env_variables(paths):
    """When add_environment_variables is false, then return dict with xml data"""

    # Arrange
    expected_result = {"PROJECT_FOO1": "foo1", "PROJECT_FOO2": "foo2", "PROJECT_FOO3": "foo3"}
    with patch.object(pathlib.Path, "joinpath") as joinpath_mock:
        joinpath_mock.return_value = paths.file_foo_xml_project_path
        # Act
        result = sut.parse_project_xml_data(False)
        # Assert
        assert expected_result == result


def test_parse_project_xml_data_when_add_environment_variables_is_true_then_call_create_env_variables(paths):
    """When add_environment_variables is false, then return dict with xml data"""

    # Arrange
    expected_result = {"PROJECT_FOO1": "foo1", "PROJECT_FOO2": "foo2", "PROJECT_FOO3": "foo3"}
    with patch.object(pathlib.Path, "joinpath") as joinpath_mock:
        joinpath_mock.return_value = paths.file_foo_xml_project_path
        with patch.object(sut, "platform_specific") as platform_specific_mock:
            with patch.object(platform_specific_mock, "create_environment_variables") as create_env_vars_mock:
                # Act
                sut.parse_project_xml_data(True)
                # Assert
                create_env_vars_mock.assert_called_once_with(expected_result)


# endregion

# region parse_theme_metadata()

@patch("logging.info")
def test_parse_theme_metadata_when_no_tokens_then_return_empty_dict(logging_mock):
    """ Given theme metadata, when no tokens to match, then return empty dict """
    # Arrange
    tokens = []
    css_file_data = b""
    # Act
    result = sut.parse_theme_metadata(css_file_data, tokens)
    # Assert
    assert len(result) == 0


@patch("logging.info")
@patch("logging.debug")
def test_parse_theme_metadata_when_tokens_matched_then_return_matches_dict(logging_info_mock, logging_debug_mock):
    """ Given theme metadata, when tokens to match, then return matches as a dict"""
    # Arrange
    token1, value1, token2, value2 = "Sometoken1", "Somevalue1", "Sometoken2", "Somevalue2"
    tokens = [token1, token2]
    css_file_data = b"Sometoken1: Somevalue1\nSometoken2: Somevalue2\n"
    # Act
    result = sut.parse_theme_metadata(css_file_data, tokens)
    # Assert
    assert result[token1] == value1 and result[token2] == value2


@patch("logging.warning")
@patch("logging.info")
@patch("logging.debug")
def test_parse_theme_metadata_when_token_and_not_matched_then_warns(
        logging_info_mock, logging_debug_mock, logging_warning_mock):
    """ Given theme metadata, when token present and doest match, then return matches as a dict"""
    # Arrange
    token1, value1 = "Sometoken1", "Somevalue1"
    tokens = [token1]
    css_file_data = b"Sometoken2: Somevalue2\n"
    literal_expected = wp_literals.get("wp_parsing_theme_no_matches_found").format(token=token1)
    # Act
    sut.parse_theme_metadata(css_file_data, tokens)
    # Assert
    logging_warning_mock.assert_called_once_with(literal_expected)


@patch("logging.info")
@patch("logging.debug")
def test_parse_theme_metadata_when_tokens_matched_and_add_environment_variables_then_call_create_env_variables\
                (logging_info_mock, logging_debug_mock):
    """ Given theme metadata, when tokens to match, then return matches as a dict"""
    # Arrange
    tokens, env_variable = dict(), dict()
    token, value = "Sometoken", "Somevalue"
    tokens[token] = value
    css_file_data = b"Sometoken: Somevalue\n"
    env_variable[f"theme_{token}".upper()] = value
    # Act
    with patch.object(sut, "platform_specific") as platform_specific_mock:
        with patch.object(platform_specific_mock, "create_environment_variables") as create_env_vars_mock:
            sut.parse_theme_metadata(css_file_data, tokens, True)
            # Assert
            create_env_vars_mock.assert_called_once_with(env_variable)

# endregion


# region Parse_json_file()


@patch("builtins.open", new_callable=mock_open, read_data="{}")
def test_parse_json_file_load_json(builtins_open):
    """Given a JSON file path, returns dict with JSON content"""

    # Arrange

    # Act
    result = sut.parse_json_file("file.json")

    # Assert
    assert result == json.loads("{}")

# endregion
