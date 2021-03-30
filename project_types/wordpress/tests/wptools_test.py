"""Unit tests for the wordpress.tools file"""
import os
import stat
import pytest
import json
import pathlib
import project_types.wordpress.wptools as sut
from project_types.wordpress.basic_structure_starter import BasicStructureStarter
from devops_platforms import constants as devops_platform_constants
from core.LiteralsCore import LiteralsCore
from project_types.wordpress.Literals import Literals as WordpressLiterals
from unittest.mock import patch, mock_open, call
from project_types.wordpress.tests.conftest import WordPressData, mocked_requests_get, \
    mocked_requests_get_json_content, PluginsData

literals = LiteralsCore([WordpressLiterals])


# region convert_wp_config_token


def test_convert_wp_config_token_given_token_when_no_match_then_return_bare_token(wordpressdata):
    """Given token, when no matches, then returns bare token without changes"""
    # Arrange
    token = "no_matching_token"
    wordpress_path = wordpressdata.wordpress_path
    # Act
    result = sut.convert_wp_config_token(token, wordpress_path)
    # Assert
    assert result == token


@patch("project_types.wordpress.wp_cli.eval_code")
def test_convert_wp_config_token_given_token_when_date_match_then_calls_wp_cli_eval_code(
        eval_code_mock, wordpressdata):
    """Given token, when match "date|", then parses and calls wp_cli.eval_code with necessary data"""
    # Arrange
    token = "some-data-[date|Y.m.d-Hisve]"
    date_formatted = "some-formatted-date"
    eval_code_mock.return_value = date_formatted
    expected_result = f"some-data-{date_formatted}"
    wordpress_path = wordpressdata.wordpress_path
    # Act
    result = sut.convert_wp_config_token(token, wordpress_path)
    # Assert
    assert result == expected_result


# endregion

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
    environment_config = json.loads(wordpressdata.site_config_content)["environments"][0]
    wordpress_path = wordpressdata.wordpress_path
    database_user_pass = "my-password"
    # Act
    sut.create_configuration_file(environment_config, wordpress_path, database_user_pass)
    # Assert
    create_conf_file_mock.assert_called_once_with(
        wordpress_path=wordpress_path,
        db_host=environment_config["database"]["host"],
        db_name=environment_config["database"]["db_name"],
        db_user=environment_config["database"]["db_user"],
        db_pass=database_user_pass,
        db_prefix=environment_config["database"]["table_prefix"],
        db_charset=environment_config["database"]["charset"],
        db_collate=environment_config["database"]["collate"],
        skip_check=environment_config["database"]["skip_check"],
        debug=environment_config["wp_cli_debug"])


# endregion

# region download_wordpress()


@patch("project_types.wordpress.wp_cli.download_wordpress")
def test_download_wordpress_given_invalid_path_raises_valueerror(download_wordpress_mock, wordpressdata):
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

# region export_database()


@patch("project_types.wordpress.wp_cli.export_database")
def test_export_database_calls_wp_cli_export_database(export_database_mock, wordpressdata):
    """Given site configuration, should call wp_cli.export_database"""
    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    site_config = json.loads(wordpressdata.site_config_content)
    dump_file_path = wordpressdata.dump_file_path
    # Act
    sut.export_database(site_config, wordpress_path, dump_file_path)
    # Assert
    export_database_mock.assert_called_once_with(wordpress_path, dump_file_path, site_config["wp_cli"]["debug"])


# endregion


# region get_constants()

# endregion

# region get_project_structure()


def test_get_project_structure_given_resource_reads_and_parses_content(wordpressdata, mocks):
    """Given a path, reads the file obtained from the resource and parses the JSON content."""

    # Arrange
    url_resource = wordpressdata.url_resource
    mocks.requests_get_mock.side_effect = mocked_requests_get_json_content

    # Act
    result = sut.get_project_structure(url_resource)

    # Assert
    assert result == WordPressData.structure_file_content


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

# region import_content_from_configuration_file()


@patch("project_types.wordpress.wp_cli.import_wxr_content")
@patch("project_types.wordpress.wp_cli.delete_post_type_content")
@patch("project_types.wordpress.wptools.get_constants")
def test_import_content_from_configuration_file_given_args_then_call_delete_post_type_content(get_constants_mock,
    delete_content_mock, import_wxr_content, wordpressdata):
    """ Given args, for every content type present, should call delete_post_type_content with required data """
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    get_constants_mock.return_value = json.loads(wordpressdata.constants_file_content)
    wordpress_path = wordpressdata.wordpress_path
    expected_content_imported = ["page", "nav_menu_item"]
    # Act
    sut.import_content_from_configuration_file(site_config, wordpress_path)
    expected_calls = [call(wordpress_path, expected_content_imported[0], False),
                      call(wordpress_path, expected_content_imported[1], False)]

    # Assert
    delete_content_mock.assert_has_calls(expected_calls)

# endregion import_content_from_configuration_file

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
    sut.install_plugins_from_configuration_file(site_config, root_path, True)
    # Assert
    install_plugin_mock.assert_not_called()


@patch("logging.info")
@patch("project_types.wordpress.wptools.get_constants")
@patch("project_types.wordpress.wp_cli.install_plugin")
@patch("project_types.wordpress.wptools.download_wordpress_plugin")
@patch("project_types.wordpress.wptools.convert_wp_config_token")
@patch("project_types.wordpress.wptools.export_database")
@pytest.mark.parametrize(
    "plugins_content", [json.loads(PluginsData.plugins_content_single_url_source),
                        json.loads(PluginsData.plugins_content_single_zip_source),
                        json.loads(PluginsData.plugins_content_two_plugins_with_url_and_zip_sources)])
def test_install_plugins_given_configuration_file_when_plugins_then_then_downloads_wordpress_plugin(
        export_mock, convert_token_mock, download_wordpress_plugin_mock, install_plugin_mock, get_constants_mock,
        logging_mock, plugins_content, wordpressdata, pluginsdata):
    """ Given the configuration values, when url plugin present, then calls download_wordpress_plugin"""
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    site_config["plugins"] = plugins_content
    constants = json.loads(wordpressdata.constants_file_content)
    get_constants_mock.return_value = constants
    root_path = pathlib.Path(wordpressdata.root_path)
    wordpress_path = pathlib.Path.joinpath(root_path, constants["paths"]["wordpress"])
    plugins_path = pathlib.Path.joinpath(root_path, constants["paths"]["content"]["plugins"])
    # Act
    sut.install_plugins_from_configuration_file(site_config, root_path, True)
    # Assert
    calls = []
    for plugin in site_config["plugins"]:
        plugin_path = pathlib.Path.joinpath(plugins_path, f"{plugin['name']}.zip")
        plugin_call = call(plugin["name"],
                           wordpress_path,
                           plugin["activate"],
                           plugin["force"],
                           plugin_path,
                           site_config["wp_cli"]["debug"])
        calls.append(plugin_call)
    install_plugin_mock.assert_has_calls(calls)

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
@patch("logging.info")
def test_install_wp_cli_given_path_when_is_dir_then_downloads_from_request_resource(
        log_info_mock, wp_cli_info, create_wp_cli_bat_file, pathlib_mock, wordpressdata, mocks):
    """ Given a file path, when path is a dir, then downloads from download url """
    # Arrange
    install_path = wordpressdata.wp_cli_install_path
    pathlib_mock.return_value = install_path
    mocks.requests_get_mock.side_effect = mocked_requests_get
    wp_cli_phar = "wp-cli.phar"
    wp_cli_download_url = f"https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/{wp_cli_phar}"
    with patch(wordpressdata.builtins_open, mock_open()):
        with patch.object(os, "stat"):
            with patch.object(os, "chmod"):
                # Act
                sut.install_wp_cli(install_path)
                # Assert
                calls = [call(wp_cli_download_url)]
                mocks.requests_get_mock.assert_has_calls(calls, any_order=True)


@patch("pathlib.Path")
@patch("project_types.wordpress.wptools.create_wp_cli_bat_file")
@patch("project_types.wordpress.wp_cli.wp_cli_info")
@patch("logging.info")
def test_install_wp_cli_given_path_when_is_dir_then_writes_response_content(
        log_info_mock, wp_cli_info, create_wp_cli_bat_file, pathlib_mock, wordpressdata, mocks):
    """ Given a file path, when path is a dir, then writes response content to file_path """
    # Arrange
    install_path = wordpressdata.wp_cli_install_path
    pathlib_mock.return_value = install_path
    mocks.requests_get_mock.side_effect = mocked_requests_get
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
def test_install_wp_cli_given_path_when_is_dir_then_chmods_written_file_path(wp_cli_info, wordpressdata, mocks):
    """ Given a file path, when path is a dir, then does chmod with S_IEXEC """
    # Arrange
    install_path = wordpressdata.wp_cli_install_path
    mocks.requests_get_mock.side_effect = mocked_requests_get

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
def test_install_wp_cli_given_path_when_is_dir_then_calls_subprocess_wpcli_info_command(
        wp_cli_info, wordpressdata, mocks):
    """ Given a file path, when path is a dir, then calls wp_cli_info() from wp_cli module """
    # Arrange
    install_path = wordpressdata.wp_cli_install_path
    mocks.requests_get_mock.side_effect = mocked_requests_get

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

# region install_wordpress_core()


@patch("project_types.wordpress.wp_cli.install_wordpress_core")
def test_install_wordpress_core_then_calls_cli_install_wordpress_core(install_wordpress_mock, wordpressdata):
    """ Given configuration file, then calls install_wordpress_core from cli """
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    wordpress_path = wordpressdata.wordpress_path
    admin_pass = "root"
    # Act
    sut.install_wordpress_core(site_config, wordpress_path, admin_pass)
    # Assert
    install_wordpress_mock.assert_called_once()


# endregion

# region install_wordpress_site()

@patch("tools.git.purge_gitkeep")
@patch("project_types.wordpress.wptools.get_constants")
@patch("project_types.wordpress.wp_cli.reset_database")
@patch("project_types.wordpress.wp_cli.update_database_option")
@patch("project_types.wordpress.wptools.install_wordpress_core")
@patch("project_types.wordpress.wptools.export_database")
@patch("project_types.wordpress.wptools.convert_wp_config_token")
@patch("pathlib.Path.as_posix")
def test_install_wordpress_site_then_calls_install_wordpress_core(
        path_mock, convert_wp_config_token, export_database, install_wordpress_core,
        update_database, reset_database_mock, get_constants_mock, purge_gitkeep_mock, wordpressdata):
    """ Given site_configuration, then calls install_wordpress_core """
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    wordpress_path = wordpressdata.wordpress_path
    path_mock.return_value = wordpress_path
    admin_pass = "root"
    # Act
    sut.install_wordpress_site(site_config, wordpress_path, admin_pass)
    # Assert
    install_wordpress_core.assert_called_with(site_config, wordpress_path, admin_pass)


@patch("tools.git.purge_gitkeep")
@patch("project_types.wordpress.wptools.get_constants")
@patch("project_types.wordpress.wp_cli.reset_database")
@patch("project_types.wordpress.wp_cli.update_database_option")
@patch("project_types.wordpress.wptools.install_wordpress_core")
@patch("project_types.wordpress.wptools.export_database")
@patch("project_types.wordpress.wptools.convert_wp_config_token")
@patch("pathlib.Path.as_posix")
def test_install_wordpress_site_then_calls_cli_update_option(
        path_mock, convert_wp_config_token, export_database, install_wordpress_core,
        update_database, reset_database_mock, get_constants_mock, purge_gitkeep_mock, wordpressdata):
    """ Given site_configuration, then calls cli's update database  option """
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    wordpress_path = wordpressdata.wordpress_path
    path_mock.return_value = str(wordpress_path)
    admin_pass = "root"
    # Act
    sut.install_wordpress_site(site_config, wordpress_path, admin_pass)
    # Assert
    update_database.assert_called_with("blogdescription", site_config["settings"]["description"],
                                       wordpress_path, site_config["wp_cli"]["debug"])


@patch("tools.git.purge_gitkeep")
@patch("project_types.wordpress.wptools.get_constants")
@patch("project_types.wordpress.wp_cli.reset_database")
@patch("project_types.wordpress.wp_cli.update_database_option")
@patch("project_types.wordpress.wptools.install_wordpress_core")
@patch("project_types.wordpress.wptools.export_database")
@patch("project_types.wordpress.wptools.convert_wp_config_token")
@patch("pathlib.Path.as_posix")
def test_install_wordpress_site_then_calls_cli_export_database(
        path_mock, convert_wp_config_token, export_database, install_wordpress_core,
        update_database, reset_database_mock, get_constants_mock, purge_gitkeep_mock, wordpressdata):
    """ Given site_configuration, then calls cli's export_database"""
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    wordpress_path = wordpressdata.wordpress_path
    path_mock.return_value = wordpress_path
    admin_pass = "root"
    # Act
    sut.install_wordpress_site(site_config, wordpress_path, admin_pass)
    # Assert
    export_database.assert_called_with(site_config, wordpress_path, wordpress_path)


# endregion

# region start_basic_structure


@patch.object(sut, "get_project_structure")
def test_main_given_parameters_must_call_wptools_get_project_structure(get_project_structure_mock, wordpressdata):
    """Given arguments, must call get_project_structure with passed project_path"""
    # Arrange
    project_structure_resource = devops_platform_constants.Urls.DEFAULT_WORDPRESS_PROJECT_STRUCTURE
    root_path = wordpressdata.wordpress_path
    get_project_structure_mock.return_value = {"items": {}}
    # Act
    sut.start_basic_project_structure(root_path)
    # Assert
    get_project_structure_mock.assert_called_once_with(project_structure_resource)


@patch.object(sut, "get_project_structure")
@patch.object(BasicStructureStarter, "add_item")
def test_main_given_parameters_must_call_add_item(add_item_mock, get_project_structure_mock, wordpressdata):
    """Given arguments, must call get_project_structure with passed project_path"""
    # Arrange
    root_path = wordpressdata.wordpress_path
    items_data = {"items": {'foo_item': 'foo_value'}}
    get_project_structure_mock.return_value = items_data
    # Act
    sut.start_basic_project_structure(root_path)
    # Assert
    add_item_mock.assert_called_once_with('foo_item', root_path)


# endregion start_basic_structure
