""" Unit tests for the generate wordpress script """

import json
import pathlib
from unittest.mock import patch, mock_open, call

import pytest

import project_types.wordpress.generate_wordpress as sut
from project_types.wordpress import constants
from project_types.wordpress.tests.conftest import mocked_requests_get

# region main


@patch("clint.textui.prompt.yn")
@patch("logging.critical")
@patch("core.log_tools.log_indented_list")
@patch("filesystem.paths.files_exist_filtered")
@patch("project_types.wordpress.wptools.get_constants")
def test_main_given_required_files_when_not_present_and_localhost_and_no_defaults_then_raise_error(
        constants_mock, files_exist_mock, log_indented_mock, logging_mock, prompt_mock, wordpressdata):
    """ Given required files filter, when not present in root_path and not localhost environment, then raise error"""
    # Arrange
    required_files = ["file1", "file2", "file3"]
    files_exist_mock.return_value = required_files
    environment = "localhost"
    root_path = wordpressdata.root_path
    prompt_mock.return_value = False
    # Act
    with pytest.raises(ValueError) as value_error:
        sut.main(root_path, "root", "root", "root", environment, [''], [''], False, True, False)
    # Assert
    assert str(value_error.value) == sut.literals.get("wp_required_files_not_found").format(path=root_path)


@patch("tools.git.purge_gitkeep")
@patch("project_types.wordpress.wptools.export_database")
@patch("project_types.wordpress.generate_wordpress.delete_sample_wp_config_file")
@patch("project_types.wordpress.generate_wordpress.generate_additional_wpconfig_files")
@patch("logging.info")
@patch("core.log_tools.log_indented_list")
@patch("project_types.wordpress.wptools.get_db_admin_from_environment")
@patch("project_types.wordpress.wptools.build_theme")
@patch("project_types.wordpress.wptools.install_plugins_from_configuration_file")
@patch("project_types.wordpress.wptools.install_themes_from_configuration_file")
@patch("project_types.wordpress.wptools.install_wordpress_site")
@patch("project_types.wordpress.wptools.set_wordpress_config_from_configuration_file")
@patch("project_types.wordpress.wptools.download_wordpress")
@patch("project_types.wordpress.generate_wordpress.setup_devops_toolset")
@patch("project_types.wordpress.wptools.start_basic_project_structure")
@patch("project_types.wordpress.wptools.get_wordpress_path_from_root_path")
@patch("project_types.wordpress.wptools.get_site_configuration_from_environment")
@patch("project_types.wordpress.wptools.get_required_file_paths")
@patch("project_types.wordpress.wptools.get_themes_path_from_root_path")
@patch("filesystem.paths.files_exist_filtered")
@patch("project_types.wordpress.wptools.get_constants")
def test_main_given_required_files_when_present_then_calls_wptools_get_required_file_paths(
        constants_mock, files_exist_mock, get_themes_path_mock, get_required_files_mock, get_site_config_mock,
        get_wordpress_path, start_basic_structure_mock, setup_devops_toolset_mock, download_wordpress_mock,
        set_wordpress_config_mock, install_wordpress_site_mock, install_theme_mock,
        install_plugins_mock, build_theme_mock, get_db_admin_mock, log_indented_mock, logging_mock,
        generate_environments_mock, delete_sample_mock, export_database_mock, purge_gitkeep_mock, wordpressdata):
    """ Given root_path, when required files present in root_path, then calls get_required_file_paths"""
    # Arrange
    required_files = []
    files_exist_mock.return_value = required_files
    environment = "any"
    root_path = wordpressdata.root_path
    required_files_pattern_suffixes = list(map(lambda x: f"*{x[1]}", constants.required_files_suffixes.items()))
    # Act
    sut.main(root_path, "root", "root", "root", environment, [''], [''], False, True, False)
    # Assert
    get_required_files_mock.assert_called_with(root_path, required_files_pattern_suffixes)


@patch("tools.git.purge_gitkeep")
@patch("project_types.wordpress.wptools.convert_wp_config_token")
@patch("project_types.wordpress.wptools.export_database")
@patch("project_types.wordpress.generate_wordpress.delete_sample_wp_config_file")
@patch("project_types.wordpress.generate_wordpress.generate_additional_wpconfig_files")
@patch("logging.info")
@patch("core.log_tools.log_indented_list")
@patch("project_types.wordpress.wptools.get_db_admin_from_environment")
@patch("project_types.wordpress.wptools.build_theme")
@patch("project_types.wordpress.wptools.install_plugins_from_configuration_file")
@patch("project_types.wordpress.wptools.install_themes_from_configuration_file")
@patch("project_types.wordpress.wptools.setup_database")
@patch("project_types.wordpress.wptools.install_wordpress_site")
@patch("project_types.wordpress.wptools.set_wordpress_config_from_configuration_file")
@patch("project_types.wordpress.wptools.download_wordpress")
@patch("project_types.wordpress.generate_wordpress.setup_devops_toolset")
@patch("project_types.wordpress.wptools.start_basic_project_structure")
@patch("project_types.wordpress.wptools.get_wordpress_path_from_root_path")
@patch("project_types.wordpress.wptools.get_site_configuration_from_environment")
@patch("project_types.wordpress.wptools.get_required_file_paths")
@patch("project_types.wordpress.wptools.get_themes_path_from_root_path")
@patch("filesystem.paths.files_exist_filtered")
@patch("project_types.wordpress.wptools.get_constants")
def test_main_given_required_files_when_present_and_create_db_then_calls_setup_database(
        constants_mock, files_exist_mock, get_themes_path_mock, get_required_files_mock, get_site_config_mock,
        get_wordpress_path, start_basic_structure_mock, setup_devops_toolset_mock, download_wordpress_mock,
        set_wordpress_config_mock, install_wordpress_site_mock, setup_database_mock, install_theme_mock,
        install_plugins_mock, build_theme_mock, get_db_admin_mock, log_indented_mock, logging_mock,
        generate_environments_mock, delete_sample_mock, export_database_mock, convert_wp_config_token_mock,
        purge_gitkeep_mock, wordpressdata):
    """ Given root_path, when required files present in root_path, then calls get_required_file_paths"""
    # Arrange
    required_files = []
    files_exist_mock.return_value = required_files
    environment = "any"
    root_path = wordpressdata.root_path
    get_site_config_mock.return_value = json.loads(wordpressdata.site_config_content)
    get_wordpress_path.return_value = wordpressdata.wordpress_path
    get_db_admin_mock.return_value = "root"
    create_db = True
    site_config = json.loads(wordpressdata.site_config_content)
    # Act
    sut.main(root_path, "root", "root", "root", environment, [''], [''], create_db, True, False)
    # Assert
    setup_database_mock.assert_called_with(site_config, wordpressdata.wordpress_path, "root", "root", "root")


@patch("tools.git.purge_gitkeep")
@patch("project_types.wordpress.wptools.export_database")
@patch("project_types.wordpress.generate_wordpress.delete_sample_wp_config_file")
@patch("project_types.wordpress.generate_wordpress.generate_additional_wpconfig_files")
@patch("core.log_tools.log_indented_list")
@patch("clint.textui.prompt.yn")
@patch("project_types.wordpress.wptools.get_db_admin_from_environment")
@patch("project_types.wordpress.wptools.build_theme")
@patch("project_types.wordpress.wptools.install_plugins_from_configuration_file")
@patch("project_types.wordpress.wptools.install_themes_from_configuration_file")
@patch("project_types.wordpress.wptools.install_wordpress_site")
@patch("project_types.wordpress.wptools.set_wordpress_config_from_configuration_file")
@patch("project_types.wordpress.wptools.download_wordpress")
@patch("project_types.wordpress.generate_wordpress.setup_devops_toolset")
@patch("project_types.wordpress.wptools.start_basic_project_structure")
@patch("project_types.wordpress.wptools.get_wordpress_path_from_root_path")
@patch("project_types.wordpress.wptools.get_site_configuration_from_environment")
@patch("project_types.wordpress.wptools.get_required_file_paths")
@patch("project_types.wordpress.wptools.get_themes_path_from_root_path")
@patch("filesystem.paths.files_exist_filtered")
@patch("project_types.wordpress.wptools.get_constants")
def test_main_given_required_files_when_not_present_and_use_defaults_then_download_required_files(
        constants_mock, files_exist_mock, get_themes_path_mock, get_required_files_mock, get_site_config_mock,
        get_wordpress_path, start_basic_structure_mock, setup_devops_toolset_mock, download_wordpress_mock,
        set_wordpress_config_mock, install_wordpress_site_mock, install_theme_mock, install_plugins_mock,
        build_theme_mock, get_db_admin_mock, prompt_yn_mock, log_indented_mock, generate_environments_mock,
        delete_sample_mock, export_database_mock, purge_gitkeep_mock, wordpressdata, mocks):
    """ Given root_path, when required files present in root_path, then calls get_required_file_paths"""
    # Arrange
    required_files = list(map(lambda x: f"*{x[1]}", constants.required_files_suffixes.items()))
    files_exist_mock.return_value = required_files
    prompt_yn_mock.return_value = True
    environment = "any"
    mocks.requests_get_mock.side_effect = mocked_requests_get
    root_path = wordpressdata.root_path
    m = mock_open()
    expected_content = b"sample response in bytes"
    # Act
    with patch(wordpressdata.builtins_open, m, create=True):
        sut.main(root_path, "root", "root", "root", environment, [''], [''], False, True, False)
        # Assert
        handler = m()
        calls = []
        # Build equal number of calls as required files we have: The content will be the same since we mocked it.
        while len(calls) != len(required_files):
            calls.append(call(expected_content))
        handler.write.assert_has_calls(calls)

# endregion main

# region delete_sample_wp_config_file


@patch("pathlib.Path.exists")
@patch("os.remove")
def test_delete_sample_wp_config_file_when_file_not_exist_then_remove(remove_mock, path_exists_mock, wordpressdata):
    """ Given wordpress_path, when config-sample.php exist, then calls os.remove """
    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    file_path = pathlib.Path.joinpath(pathlib.Path(wordpress_path), "wp-config-sample.php")
    path_exists_mock.return_value = True
    # Act
    sut.delete_sample_wp_config_file(wordpress_path)
    # Assert
    remove_mock.assert_called_once_with((str(file_path)))


@patch("pathlib.Path.exists")
@patch("os.remove")
def test_delete_sample_wp_config_file_when_file_exist_then_remove(remove_mock, path_exists_mock, wordpressdata):
    """ Given wordpress_path, when config-sample.php exist, then calls os.remove """
    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    path_exists_mock.return_value = False
    # Act
    sut.delete_sample_wp_config_file(wordpress_path)
    # Assert
    remove_mock.assert_not_called()


# endregion delete_sample_wp_config_file

# region setup_devops_toolset


@patch("tools.devops_toolset.update_devops_toolset")
@patch("logging.info")
@patch("project_types.wordpress.wptools.get_constants")
def test_setup_devops_toolset_given_root_path_then_call_update_devops_toolset(
        get_constants_mock, logging_mock, update_devops_toolset_mock, wordpressdata):
    """ Given root_path, then calls update_devops_toolset with devops_path """
    # Arrange
    constants_data = json.loads(wordpressdata.constants_file_content)
    get_constants_mock.return_value = constants_data
    devops_path_constant = "/.devops"
    root_path = wordpressdata.root_path
    devops_path = pathlib.Path.joinpath(pathlib.Path(root_path), devops_path_constant, "devops-toolset")
    # Act
    sut.setup_devops_toolset(root_path)
    # Assert
    update_devops_toolset_mock.assert_called_once_with(devops_path)

# endregion
