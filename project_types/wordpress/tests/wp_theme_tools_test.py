"""Unit tests for the wp_theme_tools file"""
import json
import pathlib
import project_types.wordpress.wp_theme_tools as sut
import pytest
from core.LiteralsCore import LiteralsCore
from project_types.wordpress.Literals import Literals as WordpressLiterals
from project_types.wordpress.tests.conftest import ThemesData
from unittest.mock import patch, call

literals = LiteralsCore([WordpressLiterals])

# region build_theme


@patch("logging.info")
@patch("os.path.exists")
def test_build_theme_given_site_config_when_no_src_themes_then_logs\
                (path_exists_mock, logging_mock, wordpressdata, themesdata):
    """ Given site configuration, when no src themes present, then logs info """
    # Arrange
    theme_path = wordpressdata.theme_path
    no_src_theme_config = json.loads(themesdata.theme_single_no_src)
    path_exists_mock.return_value = False
    literal1 = literals.get("wp_looking_for_src_themes")
    literal2 = literals.get("wp_no_src_themes")

    # Act
    sut.build_theme(no_src_theme_config, theme_path)
    # Assert
    calls = [call(literal1), call(literal2)]
    logging_mock.assert_has_calls(calls)


@patch("logging.info")
@patch("os.path.exists")
@patch("os.chdir")
@patch("project_types.node.npm.install")
@patch("tools.cli.call_subprocess")
@patch("filesystem.zip.zip_directory")
def test_build_theme_given_site_config_when_src_themes_then_calls_npm_install(
        zip_directory_mock, subprocess_mock, npm_install_mock, chdir_mock, path_exists_mock,
        logging_mock, wordpressdata, themesdata):
    """ Given site configuration, when src theme present, then calls npm install wrapper """
    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    path_exists_mock.return_value = True
    src_theme_config = json.loads(themesdata.theme_single_src)
    # Act
    sut.build_theme(src_theme_config, wordpress_path)
    # Assert
    npm_install_mock.assert_called_once()


@patch("logging.info")
@patch("os.path.exists")
@patch("os.chdir")
@patch("project_types.node.npm.install")
@patch("tools.cli.call_subprocess")
@patch("filesystem.zip.zip_directory")
def test_build_theme_given_site_config_when_src_themes_then_chdir_to_source(
        zip_directory_mock, subprocess_mock, npm_install_mock, chdir_mock, path_exists_mock,
        logging_mock, wordpressdata, themesdata):
    """ Given site configuration, when src theme present, then calls npm install wrapper """
    # Arrange
    theme_path = wordpressdata.theme_path
    path_exists_mock.return_value = True
    src_theme_config = json.loads(themesdata.theme_single_src)
    src_theme_path = pathlib.Path.joinpath(pathlib.Path(theme_path), src_theme_config[0]["source"])
    # Act
    sut.build_theme(src_theme_config, theme_path)
    # Assert
    chdir_mock.assert_called_once_with(src_theme_path)


@patch("logging.info")
@patch("os.path.exists")
@patch("os.chdir")
@patch("project_types.node.npm.install")
@patch("tools.cli.call_subprocess")
@patch("filesystem.zip.zip_directory")
def test_build_theme_given_site_config_when_src_themes_then_calls_subprocess_with_build_command(
        zip_directory_mock, subprocess_mock, npm_install_mock, chdir_mock, path_exists_mock,
        logging_mock, wordpressdata, themesdata):
    """ Given site configuration, when src theme present, then calls subprocess with gulp_build command """
    # Arrange
    theme_path = wordpressdata.theme_path
    path_exists_mock.return_value = True
    src_theme_config = json.loads(themesdata.theme_single_src)
    theme_slug = src_theme_config[0]["name"]
    theme_path_src = pathlib.Path.joinpath(pathlib.Path(theme_path), src_theme_config[0]["source"])
    theme_path_dist = pathlib.Path.joinpath(theme_path_src, "dist")
    command = sut.commands.get("wp_theme_src_build").format(
        theme_slug=theme_slug,
        path=theme_path_dist)
    literal_before = literals.get("wp_gulp_build_before").format(theme_slug=theme_slug)
    literal_after = literals.get("wp_gulp_build_after").format(theme_slug=theme_slug)
    literal_error = literals.get("wp_gulp_build_error").format(theme_slug=theme_slug)
    # Act
    sut.build_theme(src_theme_config, theme_path)
    # Assert
    subprocess_mock.assert_called_once_with(command,
                                            log_before_out=[literal_before],
                                            log_after_out=[literal_after],
                                            log_after_err=[literal_error])


@patch("logging.info")
@patch("os.path.exists")
@patch("os.chdir")
@patch("project_types.node.npm.install")
@patch("tools.cli.call_subprocess")
@patch("filesystem.zip.zip_directory")
def test_build_theme_given_site_config_when_src_themes_then_zips_dist(
        zip_directory_mock, subprocess_mock, npm_install_mock, chdir_mock, path_exists_mock,
        logging_mock, wordpressdata, themesdata):
    """ Given site configuration, when src theme present, then calls zip_directory """
    # Arrange
    theme_path = wordpressdata.theme_path
    path_exists_mock.return_value = True
    src_theme_config = json.loads(themesdata.theme_single_src)
    src_theme_path_obj = pathlib.Path.joinpath(pathlib.Path(theme_path), src_theme_config[0]["source"])
    theme_slug = src_theme_config[0]['name']
    theme_path_dist = pathlib.Path.joinpath(src_theme_path_obj, "dist")
    theme_path_zip = pathlib.Path.joinpath(pathlib.Path(theme_path), f"{theme_slug}.zip")
    # Act
    sut.build_theme(src_theme_config, theme_path)
    # Assert
    zip_directory_mock.assert_called_once_with(
        theme_path_dist.as_posix(), theme_path_zip.as_posix(), f"{theme_slug}/")

# endregion

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

# region download_wordpress_theme()

def test_download_wordpress_theme_given_theme_config_when_source_type_is_feed_then_calls_get_last_artifact(
        themesdata):
    """ Given theme config, when source type is feed, then should call get_last_artifact"""
    # Arrange
    theme_config = json.loads(themesdata.theme_single_content_with_correct_feed)
    destination_path = "path/to/destination"
    azdevops_user = "user"
    azdevops_token = "my_token"
    feed_config = theme_config["feed"]
    # Act
    with patch.object(sut, "platform_specific_restapi") as platform_specific_mock:
        with patch.object(platform_specific_mock, "get_last_artifact") as get_last_artifact_mock:
            sut.download_wordpress_theme(theme_config, destination_path,
                                         azdevops_user=azdevops_user, azdevops_token=azdevops_token)
            # Assert
            get_last_artifact_mock.called_once_with("organization", feed_config["name"], feed_config["package"],
                                                    destination_path, azdevops_user, azdevops_token)


@patch("logging.warning")
def test_download_wordpress_theme_given_theme_config_when_source_type_is_feed_and_not_kwargs_then_warns(
        log_warning_mock, themesdata):
    """ Given theme config, when source type is feed, then should call get_last_artifact"""
    # Arrange
    theme_config = json.loads(themesdata.theme_single_content_with_correct_feed)
    destination_path = "path/to/destination"
    # Act
    sut.download_wordpress_theme(theme_config, destination_path)
    # Assert
    log_warning_mock.assert_called()


@patch("filesystem.paths.download_file")
def test_download_wordpress_theme_given_theme_config_when_source_type_is_url_then_calls_paths_download_file(
        download_file_mock, themesdata):
    """ Given theme config, when source type is url, then downloads content to the destination path"""
    # Arrange
    theme_config = json.loads(themesdata.theme_single_content_with_url)
    destination_path = "path/to/destination/"
    # Act
    sut.download_wordpress_theme(theme_config, destination_path)
    # Assert
    download_file_mock.assert_called_once_with(theme_config["source"], destination_path, f"{theme_config['name']}.zip")

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
    sut.install_themes_from_configuration_file(site_config, root_path, True)
    # Assert
    install_theme_mock.assert_not_called()


@patch("project_types.wordpress.wp_theme_tools.check_themes_configuration")
@patch("project_types.wordpress.wp_theme_tools.check_theme_configuration")
@patch("project_types.wordpress.wp_theme_tools.download_wordpress_theme")
@patch("filesystem.zip.read_text_file_in_zip")
@patch("filesystem.parsers.parse_theme_metadata")
@patch("project_types.wordpress.wp_theme_tools.triage_themes")
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
    sut.install_themes_from_configuration_file(site_config, root_path, True)
    # Assert
    install_theme_mock.assert_called_once_with(wordpress_path, themesdata.child_url_source, True,
                                               site_config["wp_cli"]["debug"], themesdata.child_name)


# endregion


