"""Unit tests for the wordpress.tools file"""
import os
import stat
import pytest
import json
import pathlib
import project_types.wordpress.wptools as sut
from project_types.wordpress.basic_structure_starter import BasicStructureStarter
from core.LiteralsCore import LiteralsCore
from project_types.wordpress.Literals import Literals as WordpressLiterals
from unittest.mock import patch, mock_open, call
from project_types.wordpress.tests.conftest import WordPressData, mocked_requests_get

literals = LiteralsCore([WordpressLiterals])


# region create_wp_cli_bat_file()


def test_create_wp_cli_bat_file_given_phar_path_creates_bat_file_with_specific_content(tmp_path):
    """Given a .phar path, then creates a .bat file with specific content"""

    # Arrange
    phar_path = str(pathlib.Path.joinpath(tmp_path, "wp-cli.phar"))
    bat_path = str(pathlib.Path.joinpath(tmp_path, "wp.bat"))
    expected_content = f"@ECHO OFF\nphp \"{phar_path}\" %*"

    # Act
    sut.create_wp_cli_bat_file(phar_path)

    # Assert
    with open(bat_path, "r") as bat:
        file_content = bat.read()
    assert file_content == expected_content


# endregion

# region create_configuration_file()


@patch("project_types.wordpress.wp_cli.create_configuration_file")
def test_create_configuration_file_then_calls_wp_cli_create_configuration_with_database_parameters(
        create_conf_file_mock, wordpressdata):
    """ Given database parameters, calls wp.cli.create_configuration_file """
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    database_props = site_config["database"]
    wordpress_path = wordpressdata.wordpress_path
    database_user_pass = "my-password"
    # Act
    sut.create_configuration_file(site_config, wordpress_path, database_user_pass)
    # Assert
    create_conf_file_mock.assert_called_once_with(
        wordpress_path=wordpress_path,
        db_host=database_props["host"],
        db_name=database_props["name"],
        db_user=database_props["user"],
        db_pass=database_user_pass,
        db_prefix=database_props["prefix"],
        db_charset=database_props["charset"],
        db_collate=database_props["collate"],
        skip_check=database_props["skip_check"],
        debug=site_config["wp_cli"]["debug"])


# endregion

# region download_wordpress()


@patch("project_types.wordpress.wp_cli.download_wordpress")
def test_download_wordpress_given_invalid_path_raises_valueerror(wordpressdata):
    """Given an invalid path, raises ValueError"""

    # Arrange
    site_configuration = json.loads(wordpressdata.site_config_content)
    path = wordpressdata.wordpress_path_err

    # Act
    with pytest.raises(ValueError):
        # Assert
        sut.download_wordpress(site_configuration, path)


@patch("tools.git.purge_gitkeep")
@patch("project_types.wordpress.wp_cli.download_wordpress")
def test_download_wordpress_given_valid_arguments_calls_subprocess(
        download_wordpress_mock, purge_gitkeep, wordpressdata):
    """Given valid arguments, calls subprocess"""

    # Arrange
    site_configuration = json.loads(wordpressdata.site_config_content)
    path = wordpressdata.wordpress_path

    # Act
    sut.download_wordpress(site_configuration, path)

    # Assert
    download_wordpress_mock.assert_called_once()
    purge_gitkeep.assert_called_once()


# endregion

# region import_database()


@patch("project_types.wordpress.wp_cli.import_database")
def test_import_database_given_config_then_call_cli_import_database(import_database_mock, wordpressdata):
    """ Given site configuration, then calls wp_cli.import database """
    # Arrange
    site_configuration = json.loads(wordpressdata.site_config_content)
    wordpress_path = wordpressdata.wordpress_path
    dump_file_path = wordpressdata.dump_file_path
    # Act
    sut.import_database(site_configuration, wordpress_path, dump_file_path)
    # Assert
    import_database_mock.assert_called_once_with(
        wordpress_path, dump_file_path, site_configuration["wp_cli"]["debug"])


# endregion

# region install_wp_cli()


@patch("pathlib.Path")
def test_install_wp_cli_given_path_when_not_dir_then_raise_value_error(pathlib_mock, wordpressdata):
    """Given a file path, raises ValueError when install_path is not a dir."""

    # Arrange
    install_path = wordpressdata.wp_cli_install_path
    pathlib_mock.return_value = install_path
    expected_exception_message = literals.get("wp_not_dir")
    with patch.object(pathlib.Path, "is_dir", return_value=False):
        # Act
        with pytest.raises(ValueError) as exceptionInfo:
            sut.install_wp_cli(install_path)
        # Assert
        assert expected_exception_message == str(exceptionInfo.value)


@patch("pathlib.Path")
@patch("project_types.wordpress.wptools.create_wp_cli_bat_file")
@patch("project_types.wordpress.wp_cli.wp_cli_info")
def test_install_wp_cli_given_path_when_is_dir_then_downloads_from_request_resource(
        wp_cli_info, create_wp_cli_bat_file, pathlib_mock, wordpressdata):
    """ Given a file path, when path is a dir, then downloads from download url """
    # Arrange
    install_path = wordpressdata.wp_cli_install_path
    pathlib_mock.return_value = install_path
    wordpressdata.requests_get_mock.side_effect = mocked_requests_get
    wp_cli_phar = "wp-cli.phar"
    wp_cli_download_url = f"https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/{wp_cli_phar}"
    with patch(wordpressdata.builtins_open, mock_open()):
        with patch.object(os, "stat"):
            with patch.object(os, "chmod"):
                # Act
                sut.install_wp_cli(install_path)
    # Assert
    calls = [call(wp_cli_download_url)]
    wordpressdata.requests_get_mock.assert_has_calls(calls, any_order=True)


@patch("pathlib.Path")
@patch("project_types.wordpress.wptools.create_wp_cli_bat_file")
@patch("project_types.wordpress.wp_cli.wp_cli_info")
def test_install_wp_cli_given_path_when_is_dir_then_writes_response_content(
        wp_cli_info, create_wp_cli_bat_file, pathlib_mock, wordpressdata):
    """ Given a file path, when path is a dir, then writes response content to file_path """
    # Arrange
    install_path = wordpressdata.wp_cli_install_path
    pathlib_mock.return_value = install_path
    wordpressdata.requests_get_mock.side_effect = mocked_requests_get
    expected_content = b"sample response in bytes"
    m = mock_open()
    with patch(wordpressdata.builtins_open, m, create=True):
        with patch.object(os, "stat"):
            with patch.object(os, "chmod"):
                # Act
                sut.install_wp_cli(install_path)
                # Assert
                handler = m()
                handler.write.assert_called_once_with(expected_content)


@patch("project_types.wordpress.wp_cli.wp_cli_info")
def test_install_wp_cli_given_path_when_is_dir_then_chmods_written_file_path(wp_cli_info, wordpressdata):
    """ Given a file path, when path is a dir, then does chmod with S_IEXEC """
    # Arrange
    install_path = wordpressdata.wp_cli_install_path
    wordpressdata.requests_get_mock.side_effect = mocked_requests_get

    with patch.object(pathlib.Path, "is_dir", return_value=True):
        with patch(wordpressdata.builtins_open, mock_open()):
            with patch.object(os, "stat") as file_stat_mock:
                file_stat_mock.return_value = os.stat(install_path)
                with patch.object(os, "chmod") as chmod_mock:
                    # Act
                    sut.install_wp_cli(install_path)
                    # Assert
                    chmod_mock.assert_called_once_with(wordpressdata.wp_cli_file_path,
                                                       file_stat_mock.return_value.st_mode | stat.S_IEXEC)


@patch("project_types.wordpress.wp_cli.wp_cli_info")
def test_install_wp_cli_given_path_when_is_dir_then_calls_subprocess_wpcli_info_command(wp_cli_info, wordpressdata):
    """ Given a file path, when path is a dir, then calls wp_cli_info() from wp_cli module """
    # Arrange
    install_path = wordpressdata.wp_cli_install_path
    wordpressdata.requests_get_mock.side_effect = mocked_requests_get

    with patch.object(pathlib.Path, "is_dir", return_value=True):
        with patch(wordpressdata.builtins_open, mock_open()):
            with patch.object(os, "stat") as file_stat_mock:
                file_stat_mock.return_value = os.stat(install_path)
                with patch.object(os, "chmod"):
                    # Act
                    sut.install_wp_cli(install_path)
                    # Assert
                    wp_cli_info.assert_called_once()


# endregion

# region get_constants()

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


@patch("filesystem.paths.get_file_path_from_pattern")
def test_get_required_file_paths(get_file_path_from_pattern, wordpressdata):
    """Given, when, then"""

    # Arrange
    path = wordpressdata.path
    required_file_patterns = ["*site.json"]
    get_file_path_from_pattern.return_value = wordpressdata.site_config_path

    # Act
    result = sut.get_required_file_paths(path, required_file_patterns)

    # Assert
    assert result == (wordpressdata.site_config_path,)


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

# region get_site_configuration_from_environment()


@patch("project_types.wordpress.wptools.get_site_configuration")
@patch("project_types.wordpress.wptools.get_site_configuration_path_from_environment")
def test_get_site_configuration_from_environment(
        get_site_configuration_path_from_environment, get_site_configuration, wordpressdata):
    """Given environment data, calls get_site_configuration with the correct
    path."""

    # Arrange
    environment_path = wordpressdata.environment_path
    environment_name = wordpressdata.environment_name
    get_site_configuration_path_from_environment.return_value = json.loads(wordpressdata.site_config_content)

    # Act
    sut.get_site_configuration_from_environment(environment_path, environment_name)

    # Assert
    get_site_configuration.assert_called_with(get_site_configuration_path_from_environment.return_value)


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

# region import_database()


@patch("project_types.wordpress.wp_cli.import_database")
def test_import_database_given_config_then_call_cli_import_database(import_database_mock, wordpressdata):
    """ Given site configuration, then calls wp_cli.import database """
    # Arrange
    site_configuration = json.loads(wordpressdata.site_config_content)
    wordpress_path = wordpressdata.wordpress_path
    dump_file_path = wordpressdata.dump_file_path
    # Act
    sut.import_database(site_configuration, wordpress_path, dump_file_path)
    # Assert
    import_database_mock.assert_called_once_with(
        wordpress_path, dump_file_path, site_configuration["wp_cli"]["debug"])


# endregion

# region install_plugins_from_configuration_file()


@patch("project_types.wordpress.wptools.get_constants")
@patch("project_types.wordpress.wp_cli.install_plugin")
def test_install_plugins_given_configuration_file_when_no_plugins_then_no_install(
        install_plugin_mock, get_constants_mock, wordpressdata):
    """ Given the configuration values, when no plugins present, the no installation calls
     should be made """
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    site_config["plugins"] = {}
    get_constants_mock.return_value = json.loads(wordpressdata.constants_file_content)
    root_path = wordpressdata.root_path
    # Act
    sut.install_plugins_from_configuration_file(site_config, root_path)
    # Assert
    install_plugin_mock.assert_not_called()


@patch("project_types.wordpress.wptools.get_constants")
@patch("project_types.wordpress.wp_cli.install_plugin")
@patch("pathlib.Path.as_posix")
def test_install_plugins_given_configuration_file_when_plugins_then_calls_wp_cli_install_plugin(
        path_mock, install_plugin_mock, get_constants_mock, wordpressdata):
    """ Given the configuration values, when no plugins present, the no installation calls
     should be made """
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    site_config["plugins"] = json.loads(wordpressdata.plugins_content)
    get_constants_mock.return_value = json.loads(wordpressdata.constants_file_content)
    root_path = wordpressdata.root_path
    path_mock.return_value = wordpressdata.wordpress_path
    # Act
    sut.install_plugins_from_configuration_file(site_config, root_path)
    # Assert
    calls = []
    for plugin in site_config["plugins"]:
        plugin_call = call(plugin["name"],
                           wordpressdata.wordpress_path,
                           plugin["force"],
                           plugin["source"],
                           site_config["wp_cli"]["debug"])
        calls.append(plugin_call)
    install_plugin_mock.assert_has_calls(calls)


@patch("project_types.wordpress.wptools.get_constants")
@patch("project_types.wordpress.wp_cli.install_plugin")
@patch("pathlib.Path.as_posix")
@patch("shutil.move")
@patch("tools.git.purge_gitkeep")
def test_install_plugins_given_configuration_file_when_zip_plugins_then_calls_shutil_move(
        purge_gitkeep_mock, move_mock, path_mock, install_plugin_mock, get_constants_mock, wordpressdata):
    """ Given the configuration values, when no plugins present, the no installation calls
     should be made """
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    site_config["plugins"] = json.loads(wordpressdata.plugins_content)
    site_config["plugins"][0]["source_type"] = "zip"
    site_config["plugins"][1]["source_type"] = "zip"
    get_constants_mock.return_value = json.loads(wordpressdata.constants_file_content)
    root_path = wordpressdata.root_path
    path_mock.return_value = wordpressdata.wordpress_path
    # Act
    sut.install_plugins_from_configuration_file(site_config, root_path)
    # Assert
    calls = []
    for plugin in site_config["plugins"]:
        move_call = call(plugin["source"],
                         wordpressdata.wordpress_path)
        calls.append(move_call)
    move_mock.assert_has_calls(calls, any_order=True)


@patch("project_types.wordpress.wptools.get_constants")
@patch("project_types.wordpress.wp_cli.install_plugin")
@patch("pathlib.Path.as_posix")
@patch("shutil.move")
@patch("tools.git.purge_gitkeep")
def test_install_plugins_given_configuration_file_when_zip_plugins_then_calls_shutil_move(
        purge_gitkeep_mock, move_mock, path_mock, install_plugin_mock, get_constants_mock, wordpressdata):
    """ Given the configuration values, when no plugins present, the no installation calls
     should be made """
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    site_config["plugins"] = json.loads(wordpressdata.plugins_content)
    site_config["plugins"][0]["source_type"] = "zip"
    site_config["plugins"][1]["source_type"] = "zip"
    get_constants_mock.return_value = json.loads(wordpressdata.constants_file_content)
    root_path = wordpressdata.root_path
    path_mock.return_value = wordpressdata.wordpress_path
    # Act
    sut.install_plugins_from_configuration_file(site_config, root_path)
    # Assert
    calls = []
    purge_gitkeep_mock.assert_called()

# endregion


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
