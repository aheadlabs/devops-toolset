"""Unit tests for the sonarx file"""

from unittest.mock import patch
import json
from core.LiteralsCore import LiteralsCore
from project_types.wordpress.Literals import Literals as WordpressLiterals
import project_types.wordpress.get_wordpress_core_files as sut

import pytest

literals = LiteralsCore([WordpressLiterals])


@patch("project_types.wordpress.wp_cli.download_wordpress")
@patch("project_types.wordpress.wptools.get_site_configuration")
@patch("project_types.wordpress.wptools.get_site_configuration_path_from_environment")
@pytest.mark.skip(reason="Need to fix this test")
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


@patch("project_types.wordpress.wp_cli.download_wordpress")
@patch("project_types.wordpress.wptools.get_site_configuration")
@patch("project_types.wordpress.wptools.get_site_configuration_path_from_environment")
@pytest.mark.skip(reason="Need to fix this test")
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


@patch("project_types.wordpress.wp_cli.download_wordpress")
@patch("project_types.wordpress.wptools.get_site_configuration")
@patch("project_types.wordpress.wptools.get_site_configuration_path_from_environment")
@pytest.mark.skip(reason="Need to fix this test")
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
