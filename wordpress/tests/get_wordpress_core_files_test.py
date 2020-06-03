"""Unit tests for the sonarx file"""

import pytest
from unittest.mock import patch
import json
from core.LiteralsCore import LiteralsCore
from wordpress.Literals import Literals as WordpressLiterals
import wordpress.get_wordpress_core_files as sut

literals = LiteralsCore([WordpressLiterals])


@pytest.mark.parametrize("wordpress_path", [None, "", " "])
def test_main_given_no_wordpress_path_raises_valueerror(wordpress_path, wordpressdata):
    """Given no wordpress-path parameter, it raises a value error."""

    # Arrange
    environment_path = wordpressdata.environment_path
    environment_name = wordpressdata.environment_name

    # Act
    with pytest.raises(ValueError) as value_error:
        sut.main(wordpress_path, environment_path, environment_name)

    # Assert
    assert str(value_error.value) == literals.get("wp_wordpress_path_mandatory")


@pytest.mark.parametrize("environment_path", [None, "", " "])
def test_main_given_no_environment_path_raises_valueerror(environment_path, wordpressdata):
    """Given no environment-path parameter, it raises a value error."""

    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    environment_name = wordpressdata.environment_name

    # Act
    with pytest.raises(ValueError) as value_error:
        sut.main(wordpress_path, environment_path, environment_name)

    # Assert
    assert str(value_error.value) == literals.get("wp_environment_path_mandatory")


@pytest.mark.parametrize("environment_name", [None, "", " "])
def test_main_given_no_environment_name_raises_valueerror(environment_name, wordpressdata):
    """Given no environment-name parameter, it raises a value error."""

    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    environment_path = wordpressdata.environment_path

    # Act
    with pytest.raises(ValueError) as value_error:
        sut.main(wordpress_path, environment_path, environment_name)

    # Assert
    assert str(value_error.value) == literals.get("wp_environment_name_mandatory")


@patch("wordpress.wp_cli.download_wordpress")
@patch("wordpress.wptools.get_site_configuration")
@patch("wordpress.wptools.get_site_configuration_path_from_environment")
def test_main_given_parameters_must_call_get_site_configuration_path_from_environment(
        get_site_config_path, get_site_config, download_wordpress, wordpressdata):
    """Given arguments, must call get_site_configuration_path_from_environment
    with appropriate parameters"""

    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    environment_path = wordpressdata.environment_path
    environment_name = wordpressdata.environment_name
    get_site_config_path.return_value = wordpressdata.site_config_path

    # Act
    sut.main(wordpress_path, environment_path, environment_name)

    # Assert
    get_site_config_path.assert_called_with(environment_path, environment_name)


@patch("wordpress.wp_cli.download_wordpress")
@patch("wordpress.wptools.get_site_configuration")
@patch("wordpress.wptools.get_site_configuration_path_from_environment")
def test_main_given_parameters_must_call_get_site_configuration(
        get_site_config_path, get_site_config, download_wordpress, wordpressdata):
    """Given arguments, must call get_site_configuration_path_from_environment
    with appropriate parameters"""

    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    environment_path = wordpressdata.environment_path
    environment_name = wordpressdata.environment_name
    get_site_config.return_value = json.loads(wordpressdata.site_config_content)

    # Act
    sut.main(wordpress_path, environment_path, environment_name)

    # Assert
    get_site_config.assert_called()


@patch("wordpress.wp_cli.download_wordpress")
@patch("wordpress.wptools.get_site_configuration")
@patch("wordpress.wptools.get_site_configuration_path_from_environment")
def test_main_given_parameters_must_call_download_wordpress(
        get_site_config_path, get_site_config, download_wordpress, wordpressdata):
    """Given arguments, must call get_site_configuration_path_from_environment
    with appropriate parameters"""

    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    environment_path = wordpressdata.environment_path
    environment_name = wordpressdata.environment_name
    get_site_config.return_value = json.loads(wordpressdata.site_config_content)

    # Act
    sut.main(wordpress_path, environment_path, environment_name)

    # Assert
    get_site_config.assert_called()
