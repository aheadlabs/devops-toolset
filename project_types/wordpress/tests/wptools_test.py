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
from project_types.wordpress.tests.conftest import WordPressData, ThemesData, mocked_requests_get, MockResponse
from conftest import Mocks

literals = LiteralsCore([WordpressLiterals])


# region check_themes_configuration()


@patch("logging.warning")
@patch("logging.error")
@pytest.mark.parametrize("themes, expected",
                         [("[]", False),
                          (ThemesData.themes_content_with_three_themes_no_activate, False)])
def test_check_themes_configuration_given_themes_when_wrong_number_of_themes_then_return_false(
        error_mock, warning_mock, themes, expected):
    """ Given themes dict, when wrong number of themes, then return False """
    # Arrange
    themes_dict_content = json.loads(themes)
    # Act
    result = sut.check_themes_configuration(themes_dict_content)
    # Assert
    assert result == expected


@patch("logging.warning")
@patch("logging.error")
@pytest.mark.parametrize("themes, expected",
                         [(ThemesData.themes_content_with_two_activated_themes, False),
                          (ThemesData.themes_content_with_two_themes_none_activated, False)])
def test_check_themes_configuration_given_themes_when_wrong_number_of_activated_themes_then_return_false(
        error_mock, warning_mock, themes, expected):
    """ Given themes dict, when wrong number of activated themes, then return False """
    # Arrange
    themes_dict_content = json.loads(themes)
    # Act
    result = sut.check_themes_configuration(themes_dict_content)
    # Assert
    assert result == expected


@patch("logging.warning")
@patch("logging.error")
def test_check_themes_configuration_given_themes_when_correct_then_return_true(error_mock, warning_mock):
    """ Given themes dict, when correct setup of the themes, then return True """
    # Arrange
    themes_dict_content = json.loads(ThemesData.themes_content_with_two_themes_one_activated)
    expected = True
    # Act
    result = sut.check_themes_configuration(themes_dict_content)
    # Assert
    assert result == expected


# endregion

# region check_theme_configuration()


@patch("logging.warning")
@patch("logging.error")
@pytest.mark.parametrize("theme, expected",
                         [(ThemesData.theme_single_content_with_wrong_feed, False),
                          (ThemesData.theme_single_content_with_correct_feed, True)])
def test_check_theme_configuration_given_theme_when_feed_expected_and_not_source_type_feed_then_returns_false(
        error_mock, warning_mock, theme, expected):
    """ Given single theme dict, when source_type = feed and no feed node, then returns False """
    # Arrange
    theme_dict_content = json.loads(theme)
    # Act
    result = sut.check_theme_configuration(theme_dict_content)
    # Assert
    assert result == expected


# endregion

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

# region download_wordpress_theme()


def test_download_wordpress_theme_given_theme_config_when_source_type_is_feed_then_calls_download_artifact_from_feed(
        themesdata):
    """ Given theme config, when source type is feed, then should call download_artifact_from_feed"""
    # Arrange
    theme_config = json.loads(themesdata.theme_single_content_with_correct_feed)
    destination_path = "path/to/destination"
    # Act
    with patch.object(sut, "platform_specific") as platform_specific_mock:
        with patch.object(platform_specific_mock, "download_artifact_from_feed") as download_artifact_mock:
            sut.download_wordpress_theme(theme_config, destination_path)
            # Assert
            download_artifact_mock.called_once_with(theme_config["feed"], destination_path)


def test_download_wordpress_theme_given_theme_config_when_source_type_is_url_then_gets_and_writes_the_content(
        wordpressdata, themesdata, mocks):
    """ Given theme config, when source type is url, then downloads content to the destination path"""
    # Arrange
    theme_config = json.loads(themesdata.theme_single_content_with_url)
    destination_path = "path/to/destination"
    mocks.requests_get_mock.side_effect = mocked_requests_get
    m = mock_open()
    # Act
    with patch(wordpressdata.builtins_open, m, create=True):
        sut.download_wordpress_theme(theme_config, destination_path)
        # Assert
        handler = m()
        handler.write.assert_called_once_with(b"sample response in bytes")


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

# region get_db_admin_from_environment


@patch("logging.info")
@patch("project_types.wordpress.wptools.get_site_environments")
def test_get_db_admin_from_environment_return_db_admin_user_from_environment_file_path(
        get_site_environments_mock, logging_mock, wordpressdata):
    """Given environment_file path and name, should parse the db_admin_user property and return it"""
    # Arrange
    env_file = json.loads(wordpressdata.environment_file_content)
    get_site_environments_mock.return_value = env_file["environments"][0]
    environment_path = wordpressdata.environment_path
    environment_name = wordpressdata.environment_name
    expected_result = "root"
    # Act
    result = sut.get_db_admin_from_environment(environment_path, environment_name)
    # Assert
    assert result == expected_result


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


@pytest.mark.parametrize("env_path, env_name, literal",
                         [("path", None, "wp_environment_path_not_found"),
                          (None, "localhost", "wp_environment_name_not_found")])
def test_get_site_configuration_path_from_environment_when_environment_path_is_none_raises_error(
        env_path, env_name, literal):
    """Given arguments, when the environment is found in the JSON file, returns
    the site configuration file path"""
    # Arrange
    expected_error = literals.get(literal)
    # Act
    with pytest.raises(ValueError) as error:
        sut.get_site_configuration_path_from_environment(env_path, env_name)

        # Assert
        assert error.value == expected_error


@patch("builtins.open", new_callable=mock_open, read_data=WordPressData.environment_file_content)
@patch("pathlib.Path.exists")
@patch("pathlib.Path.is_file")
def test_get_site_configuration_path_from_environment_when_environment_found_returns_config_path(
        path_isfile_mock, path_exist_mock, builtins_open, wordpressdata):
    """Given arguments, when the environment is found in the JSON file, returns
    the site configuration file path"""

    # Arrange
    environment_path = wordpressdata.environment_path
    environment_name = wordpressdata.environment_name
    path_exist_mock.return_value = True
    path_isfile_mock.return_value = True
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
def test_install_plugins_given_configuration_file_when_zip_plugins_then_calls_purge_git_keep(
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
    purge_gitkeep_mock.assert_called()


# endregion

# region install_themes_from_configuration_file()


@patch("project_types.wordpress.wptools.get_constants")
@patch("logging.info")
@patch("project_types.wordpress.wp_cli.install_theme")
def test_install_theme_given_configuration_file_when_wrong_themes_configuration_then_return(
        install_theme_mock, logging_mock, get_constants_mock, wordpressdata, themesdata):
    """ Given the configuration values, when wrong configuration of themes given, then no installation calls
     should be made """
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    site_config["themes"] = json.loads(themesdata.themes_content_with_three_themes_no_activate)
    root_path = wordpressdata.root_path
    get_constants_mock.return_value = json.loads(wordpressdata.constants_file_content)
    # Act
    sut.install_themes_from_configuration_file(site_config, root_path)
    # Assert
    install_theme_mock.assert_not_called()


@patch("project_types.wordpress.wptools.check_themes_configuration")
@patch("project_types.wordpress.wptools.check_theme_configuration")
@patch("project_types.wordpress.wptools.download_wordpress_theme")
@patch("filesystem.zip.read_text_file_in_zip")
@patch("filesystem.parsers.parse_theme_metadata")
@patch("project_types.wordpress.wptools.triage_themes")
@patch("project_types.wordpress.wptools.get_constants")
@patch("project_types.wordpress.wptools.convert_wp_config_token")
@patch("project_types.wordpress.wptools.export_database")
@patch("logging.info")
@patch("project_types.wordpress.wp_cli.install_theme")
def test_install_theme_given_configuration_file_when_no_parent_theme_then_install_once(
        install_theme_mock, logging_mock, export_database_mock, convert_token_mock, get_constants_mock,
        triage_themes_mock, parse_theme_metadata, read_text_file_mock, download_wordpress_mock, check_theme_mock,
        check_themes_mock, wordpressdata, themesdata):
    """ Given the configuration values, when wrong single theme configuration found, then the theme is skipped """
    # Arrange
    check_themes_mock.return_value = True
    check_theme_mock.return_value = True
    constants = json.loads(wordpressdata.constants_file_content)
    wordpress_path = pathlib.Path.joinpath(
        pathlib.Path(wordpressdata.root_path, constants["paths"]["wordpress"]))
    site_config = json.loads(wordpressdata.site_config_content)
    site_config["themes"] = json.loads(themesdata.themes_content_with_child_activated)
    root_path = wordpressdata.root_path
    get_constants_mock.return_value = constants
    triage_themes_mock.return_value = None, json.loads(themesdata.themes_content_with_child_activated)[0]
    # Act
    sut.install_themes_from_configuration_file(site_config, root_path)
    # Assert
    install_theme_mock.assert_called_once_with(wordpress_path, themesdata.child_url_source, True,
                                               site_config["wp_cli"]["debug"], themesdata.child_name)


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


@patch("project_types.wordpress.wptools.get_constants")
@patch("project_types.wordpress.wp_cli.reset_database")
@patch("project_types.wordpress.wp_cli.update_database_option")
@patch("project_types.wordpress.wptools.install_wordpress_core")
@patch("project_types.wordpress.wptools.export_database")
@patch("project_types.wordpress.wptools.convert_wp_config_token")
@patch("pathlib.Path.as_posix")
def test_install_wordpress_site_then_calls_cli_reset_database(
        path_mock, convert_wp_config_token, export_database, install_wordpress_core,
        update_database, reset_database_mock, get_constants_mock, wordpressdata):
    """ Given site_configuration, then calls cli's reset database """
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    wordpress_path = wordpressdata.wordpress_path
    path_mock.return_value = wordpress_path
    admin_pass = "root"
    # Act
    sut.install_wordpress_site(site_config, wordpress_path, admin_pass, True)
    # Assert
    reset_database_mock.assert_called_with(wordpress_path, True, site_config["wp_cli"]["debug"])


@patch("project_types.wordpress.wptools.get_constants")
@patch("project_types.wordpress.wp_cli.reset_database")
@patch("project_types.wordpress.wp_cli.update_database_option")
@patch("project_types.wordpress.wptools.install_wordpress_core")
@patch("project_types.wordpress.wptools.export_database")
@patch("project_types.wordpress.wptools.convert_wp_config_token")
@patch("pathlib.Path.as_posix")
def test_install_wordpress_site_then_calls_install_wordpress_core(
        path_mock, convert_wp_config_token, export_database, install_wordpress_core,
        update_database, reset_database_mock, get_constants_mock, wordpressdata):
    """ Given site_configuration, then calls install_wordpress_core """
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    wordpress_path = wordpressdata.wordpress_path
    path_mock.return_value = wordpress_path
    admin_pass = "root"
    # Act
    sut.install_wordpress_site(site_config, wordpress_path, admin_pass, False)
    # Assert
    install_wordpress_core.assert_called_with(site_config, wordpress_path, admin_pass)


@patch("project_types.wordpress.wptools.get_constants")
@patch("project_types.wordpress.wp_cli.reset_database")
@patch("project_types.wordpress.wp_cli.update_database_option")
@patch("project_types.wordpress.wptools.install_wordpress_core")
@patch("project_types.wordpress.wptools.export_database")
@patch("project_types.wordpress.wptools.convert_wp_config_token")
@patch("pathlib.Path.as_posix")
def test_install_wordpress_site_then_calls_cli_update_option(
        path_mock, convert_wp_config_token, export_database, install_wordpress_core,
        update_database, reset_database_mock, get_constants_mock, wordpressdata):
    """ Given site_configuration, then calls cli's update database  option """
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    wordpress_path = wordpressdata.wordpress_path
    path_mock.return_value = str(wordpress_path)
    admin_pass = "root"
    # Act
    sut.install_wordpress_site(site_config, wordpress_path, admin_pass, False)
    # Assert
    update_database.assert_called_with("blogdescription", site_config["settings"]["description"],
                                       wordpress_path, site_config["wp_cli"]["debug"])


@patch("project_types.wordpress.wptools.get_constants")
@patch("project_types.wordpress.wp_cli.reset_database")
@patch("project_types.wordpress.wp_cli.update_database_option")
@patch("project_types.wordpress.wptools.install_wordpress_core")
@patch("project_types.wordpress.wptools.export_database")
@patch("project_types.wordpress.wptools.convert_wp_config_token")
@patch("pathlib.Path.as_posix")
def test_install_wordpress_site_then_calls_cli_export_database(
        path_mock, convert_wp_config_token, export_database, install_wordpress_core,
        update_database, reset_database_mock, get_constants_mock, wordpressdata):
    """ Given site_configuration, then calls cli's export_database"""
    # Arrange
    site_config = json.loads(wordpressdata.site_config_content)
    wordpress_path = wordpressdata.wordpress_path
    path_mock.return_value = wordpress_path
    admin_pass = "root"
    # Act
    sut.install_wordpress_site(site_config, wordpress_path, admin_pass, False)
    # Assert
    export_database.assert_called_with(site_config, wordpress_path, wordpress_path)


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

# region build_theme


@patch("logging.info")
@patch("os.path.exists")
def test_build_theme_given_site_config_when_no_src_themes_then_logs(path_exists_mock, logging_mock, wordpressdata):
    """ Given site configuration, when no src themes present, then logs info """
    # Arrange
    theme_path = wordpressdata.theme_path
    site_config = json.loads(wordpressdata.site_config_content)
    path_exists_mock.return_value = False
    literal1 = literals.get("wp_looking_for_src_themes")
    literal2 = literals.get("wp_no_src_themes")

    # Act
    sut.build_theme(site_config, theme_path)
    # Assert
    calls = [call(literal1), call(literal2)]
    logging_mock.assert_has_calls(calls)


@patch("logging.info")
@patch("os.path.exists")
@patch("os.chdir")
@patch("project_types.node.npm.install")
@patch("tools.cli.call_subprocess")
def test_build_theme_given_site_config_when_src_themes_then_calls_npm_install(
        subprocess_mock, npm_install_mock, chdir_mock, path_exists_mock, logging_mock, wordpressdata, themesdata):
    """ Given site configuration, when src theme present, then calls npm install wrapper """
    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    site_config = json.loads(wordpressdata.site_config_content)
    path_exists_mock.return_value = True
    site_config["themes"] = [json.loads(themesdata.theme_single_content_with_url)]
    site_config["themes"][0]["source_type"] = "src"
    # Act
    sut.build_theme(site_config, wordpress_path)
    # Assert
    npm_install_mock.assert_called_once()


@patch("logging.info")
@patch("os.path.exists")
@patch("os.chdir")
@patch("project_types.node.npm.install")
@patch("tools.cli.call_subprocess")
def test_build_theme_given_site_config_when_src_themes_then_chdir_to_source(
        subprocess_mock, npm_install_mock, chdir_mock, path_exists_mock, logging_mock, wordpressdata, themesdata):
    """ Given site configuration, when src theme present, then calls npm install wrapper """
    # Arrange
    theme_path = wordpressdata.theme_path
    site_config = json.loads(wordpressdata.site_config_content)
    path_exists_mock.return_value = True
    site_config["themes"] = [json.loads(themesdata.theme_single_content_with_url)]
    site_config["themes"][0]["source_type"] = "src"
    src_theme_path = pathlib.Path.joinpath(pathlib.Path(theme_path), site_config["themes"][0]["source"])
    # Act
    sut.build_theme(site_config, theme_path)
    # Assert
    chdir_mock.assert_called_once_with(src_theme_path)


@patch("logging.info")
@patch("os.path.exists")
@patch("os.chdir")
@patch("project_types.node.npm.install")
@patch("tools.cli.call_subprocess")
def test_build_theme_given_site_config_when_src_themes_then_calls_subprocess_with_build_command(
        subprocess_mock, npm_install_mock, chdir_mock, path_exists_mock, logging_mock, wordpressdata, themesdata):
    """ Given site configuration, when src theme present, then calls subprocess with gulp_build command """
    # Arrange
    theme_path = wordpressdata.theme_path
    site_config = json.loads(wordpressdata.site_config_content)
    path_exists_mock.return_value = True
    site_config["themes"] = [json.loads(themesdata.theme_single_content_with_url)]
    site_config["themes"][0]["source_type"] = "src"
    theme_slug = site_config["themes"][0]["name"]
    theme_path_src = pathlib.Path.joinpath(pathlib.Path(theme_path), site_config["themes"][0]["source"])
    theme_path_dist = pathlib.Path.joinpath(theme_path_src, "dist")
    command = sut.commands.get("wp_theme_src_build").format(
        theme_slug=theme_slug,
        path=theme_path_dist)
    literal_before = literals.get("wp_gulp_build_before").format(theme_slug=theme_slug)
    literal_after = literals.get("wp_gulp_build_after").format(theme_slug=theme_slug)
    literal_error = literals.get("wp_gulp_build_error").format(theme_slug=theme_slug)
    # Act
    sut.build_theme(site_config, theme_path)
    # Assert
    subprocess_mock.assert_called_once_with(command,
                                            log_before_out=[literal_before],
                                            log_after_out=[literal_after],
                                            log_after_err=[literal_error])

# endregion
