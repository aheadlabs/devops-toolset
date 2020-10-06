""" Unit tests for the generate wordpress script """

# region main
from unittest.mock import patch

import pytest

import project_types.wordpress.generate_wordpress as sut
from project_types.wordpress import constants


@patch("clint.textui.prompt.yn")
@patch("logging.critical")
@patch("core.log_tools.log_indented_list")
@patch("filesystem.paths.files_exist_filtered")
def test_main_given_required_files_when_not_present_and_localhost_and_no_defaults_then_raise_error(
        files_exist_mock, log_indented_mock, logging_mock, prompt_mock, wordpressdata):
    """ Given required files filter, when not present in root_path and not localhost environment, then raise error"""
    # Arrange
    required_files = ["file1", "file2", "file3"]
    files_exist_mock.return_value = required_files
    environment = "localhost"
    root_path = wordpressdata.root_path
    prompt_mock.return_value = False
    # Act
    with pytest.raises(ValueError) as value_error:
        sut.main(root_path, "root", "root", environment)
    # Assert
    assert str(value_error.value) == sut.literals.get("wp_required_files_not_found").format(path=root_path)


@patch("logging.critical")
@patch("core.log_tools.log_indented_list")
@patch("project_types.wordpress.wptools.get_dbadmin_from_environment")
@patch("project_types.wordpress.wptools.build_theme")
@patch("project_types.wordpress.wptools.install_plugins_from_configuration_file")
@patch("project_types.wordpress.wptools.install_theme_from_configuration_file")
@patch("project_types.wordpress.wptools.install_wordpress_site")
@patch("project_types.wordpress.wptools.set_wordpress_config_from_configuration_file")
@patch("project_types.wordpress.wptools.download_wordpress")
@patch("project_types.wordpress.generate_wordpress.setup_devops_toolset")
@patch("project_types.wordpress.wptools.start_basic_project_structure")
@patch("project_types.wordpress.wptools.get_wordpress_path_from_root_path")
@patch("project_types.wordpress.wptools.get_site_configuration_from_environment")
@patch("project_types.wordpress.wptools.get_required_file_paths")
@patch("filesystem.paths.files_exist_filtered")
def test_main_given_required_files_when_present_then_calls_wptools_get_required_file_paths(
        files_exist_mock, get_required_files_mock, get_site_config_mock, get_wordpress_path, start_basic_structure_mock,
        setup_devops_toolset_mock, download_wordpress_mock, set_wordpress_config_mock, install_wordpress_site_mock,
        install_theme_mock, install_plugins_mock, log_indented_mock, build_theme_mock,
        get_db_admin_mock, logging_mock, wordpressdata):
    """ Given root_path, when required files present in root_path, then calls get_required_file_paths"""
    # Arrange
    required_files = []
    files_exist_mock.return_value = required_files
    environment = "any"
    root_path = wordpressdata.root_path
    required_files_pattern_suffixes = list(map(lambda x: f"*{x[1]}", constants.required_files_suffixes.items()))
    # Act
    sut.main(root_path, "root", "root", "root", environment)
    # Assert
    get_required_files_mock.assert_called_with(root_path, required_files_pattern_suffixes)

# endregion main

# TODO (alberto.carbonell) Finish this tests by covering all possible paths
