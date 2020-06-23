"""Unit tests for the wordpress.wp_cli file"""
import os
import stat
import pytest
import pathlib
import json
import project_types.wordpress.wp_cli as sut
import project_types.wordpress.wptools as wptools
from core.app import App
from unittest.mock import patch, mock_open, call, ANY
from core.LiteralsCore import LiteralsCore
from project_types.wordpress.Literals import Literals as WordpressLiterals
from core.CommandsCore import CommandsCore
from project_types.wordpress.commands import Commands as WordpressCommands
from project_types.wordpress.tests.conftest import mocked_requests_get

app: App = App()
literals = LiteralsCore([WordpressLiterals])
commands = CommandsCore([WordpressCommands])

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

# region download_wordpress()


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
@patch("tools.cli.call_subprocess")
def test_download_wordpress_given_valid_arguments_calls_subprocess(subprocess, purge_gitkeep, wordpressdata):
    """Given valid arguments, calls subprocess"""

    # Arrange
    site_configuration = json.loads(wordpressdata.site_config_content)
    path = wordpressdata.wordpress_path

    # Act
    sut.download_wordpress(site_configuration, path)

    # Assert
    subprocess.assert_called_once()
    purge_gitkeep.assert_called_once()

# endregion

# region import_database()


@patch("tools.cli.call_subprocess")
def test_import_database(call_subprocess, wordpressdata):
    """Given arguments, calls subprocess"""

    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    dump_file_path = wordpressdata.dump_file_path

    # Act
    sut.import_database(wordpress_path, dump_file_path)

    # Assert
    call_subprocess.assert_called_once_with(commands.get("wpcli_db_import").format(
        file=dump_file_path, path=wordpress_path), log_before_process=ANY, log_after_err=ANY)

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
@patch("project_types.wordpress.wp_cli.create_wp_cli_bat_file")
@patch("tools.cli.call_subprocess")
def test_install_wp_cli_given_path_when_is_dir_then_downloads_from_request_resource(
        subprocess_mock, create_wp_cli_bat_file, pathlib_mock, wordpressdata):
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
@patch("project_types.wordpress.wp_cli.create_wp_cli_bat_file")
@patch("tools.cli.call_subprocess")
def test_install_wp_cli_given_path_when_is_dir_then_writes_response_content(
        subprocess_mock, create_wp_cli_bat_file, pathlib_mock, wordpressdata):
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


@patch("tools.cli.call_subprocess")
def test_install_wp_cli_given_path_when_is_dir_then_chmods_written_file_path(subprocess_mock, wordpressdata):
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


@patch("tools.cli.call_subprocess")
def test_install_wp_cli_given_path_when_is_dir_then_calls_subprocess_wpcli_info_command(subprocess_mock, wordpressdata):
    """ Given a file path, when path is a dir, then calls cli's subprocess with wpcli command """
    # Arrange
    install_path = wordpressdata.wp_cli_install_path
    wordpressdata.requests_get_mock.side_effect = mocked_requests_get
    expected_command = commands.get("wpcli_info")
    expected_before_out_message1 = literals.get("wp_wpcli_install_ok")
    expected_before_out_message2 = literals.get("wp_wpcli_info")
    expected_after_out_message = literals.get("wp_wpcli_add_ev")

    with patch.object(pathlib.Path, "is_dir", return_value=True):
        with patch(wordpressdata.builtins_open, mock_open()):
            with patch.object(os, "stat") as file_stat_mock:
                file_stat_mock.return_value = os.stat(install_path)
                with patch.object(os, "chmod"):
                    # Act
                    sut.install_wp_cli(install_path)
                    # Assert
                    subprocess_mock.assert_called_with(
                        expected_command,
                        log_before_out=[expected_before_out_message1, expected_before_out_message2],
                        log_after_out=[expected_after_out_message]
                    )

# endregion

# region import_database()


@patch("tools.cli.call_subprocess")
def test_reset_database(call_subprocess, wordpressdata):
    """Given arguments, calls subprocess"""

    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    quiet = True

    # Act
    sut.reset_database(wordpress_path, quiet)

    # Assert
    call_subprocess.assert_called_once_with(commands.get("wpcli_db_reset").format(
        path=wordpress_path, yes=wptools.convert_wp_parameter_yes(quiet)),
        log_before_process=ANY, log_after_err=ANY)

# endregion


# region reset_transients()


@patch("tools.cli.call_subprocess")
def test_reset_transients(call_subprocess):
    """Given arguments, when the method is called, then delete transients"""

    # Arrange
    wordpress_path = ""

    # Act
    sut.reset_transients(wordpress_path)

    # Assert
    call_subprocess.assert_called()

# endregion

# TODO (some user)
# region reset_transients()


# def test_export_database():
#     """Given, when, then"""
#
#     # Arrange
#
#     # Act
#
#     # Assert
#     assert False

# endregion
