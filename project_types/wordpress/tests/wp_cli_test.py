"""Unit tests for the wordpress.wp_cli file"""
import pytest
import project_types.wordpress.wp_cli as sut
from core.app import App
from unittest.mock import patch, ANY
from core.LiteralsCore import LiteralsCore
from project_types.wordpress.Literals import Literals as WordpressLiterals
from core.CommandsCore import CommandsCore
from project_types.wordpress.commands import Commands as WordpressCommands

app: App = App()
literals = LiteralsCore([WordpressLiterals])
commands = CommandsCore([WordpressCommands])

# region convert_wp_parameter_activate


@pytest.mark.parametrize("value, expected", [(True, "--activate"), (False, "")])
def test_convert_wp_parameter_activate(value, expected):
    """When True, returns a --activate string.
    When False, returns an empty string."""

    # Arrange

    # Act
    result = sut.convert_wp_parameter_activate(value)

    # Assert
    assert result == expected

# endregion

# region convert_wp_parameter_admin_password


@pytest.mark.parametrize(
    "value, expected",
    [("my-admin-password", "--admin_password=" + "\"" + "my-admin-password" + "\""),
     ("", "")])
def test_convert_wp_parameter_admin_password_when_admin_pass_then_return_admin_pass_parameter(
        value, expected):
    """ Given admin_password str, when it has content, then return --admin_password token"""

    # Arrange

    # Act
    result = sut.convert_wp_parameter_admin_password(value)

    # Assert
    assert result == expected

# endregion

# region convert_wp_parameter_content


@pytest.mark.parametrize("value, expected", [(True, "no"), (False, "yes")])
def test_convert_wp_parameter_content(value, expected):
    """When True, returns a "no" string.
    When False, returns a "yes" string."""

    # Arrange

    # Act
    result = sut.convert_wp_parameter_content(value)

    # Assert
    assert result == expected

# endregion

# region convert_wp_parameter_debug


@pytest.mark.parametrize("value, expected", [(True, "--debug"), (False, "")])
def test_convert_wp_parameter_debug(value, expected):
    """When True, returns a --debug string.
    When False, returns an empty string."""

    # Arrange

    # Act
    result = sut.convert_wp_parameter_debug(value)

    # Assert
    assert result == expected

# endregion

# region convert_wp_parameter_force


@pytest.mark.parametrize("value, expected", [(True, "--force"), (False, "")])
def test_convert_wp_parameter_force(value, expected):
    """When True, returns a --force string.
    When False, returns an empty string."""

    # Arrange

    # Act
    result = sut.convert_wp_parameter_force(value)

    # Assert
    assert result == expected

# endregion

# region convert_wp_parameter_raw


@pytest.mark.parametrize("value, expected", [(True, "--raw"), (False, "")])
def test_convert_wp_parameter_raw(value, expected):
    """When True, returns a --raw string.
    When False, returns an empty string."""

    # Arrange

    # Act
    result = sut.convert_wp_parameter_raw(value)

    # Assert
    assert result == expected

# endregion

# region convert_wp_parameter_skip_check


@pytest.mark.parametrize("value, expected", [(True, "--skip-check"), (False, "")])
def test_convert_wp_parameter_skip_check(value, expected):
    """When True, returns a --skip-content string.
    When False, returns an empty string."""

    # Arrange

    # Act
    result = sut.convert_wp_parameter_skip_check(value)

    # Assert
    assert result == expected

# endregion

# region convert_wp_parameter_skip_content


@pytest.mark.parametrize("value, expected", [(True, "--skip-content"), (False, "")])
def test_convert_wp_parameter_skip_content(value, expected):
    """When True, returns a --skip-content string.
    When False, returns an empty string."""

    # Arrange

    # Act
    result = sut.convert_wp_parameter_skip_content(value)

    # Assert
    assert result == expected

# endregion

# region convert_wp_parameter_skip_email


@pytest.mark.parametrize("value, expected", [(True, "--skip-email"), (False, "")])
def test_convert_wp_parameter_skip_email(value, expected):
    """When True, returns a --skip-content string.
    When False, returns an empty string."""

    # Arrange

    # Act
    result = sut.convert_wp_parameter_skip_email(value)

    # Assert
    assert result == expected

# endregion

# region convert_wp_parameter_yes


@pytest.mark.parametrize("value, expected", [(True, "--yes"), (False, "")])
def test_convert_wp_parameter_yes(value, expected):
    """When True, returns a --yes string.
    When False, returns an empty string."""

    # Arrange

    # Act
    result = sut.convert_wp_parameter_yes(value)

    # Assert
    assert result == expected

# endregion

# region import_database()


@patch("tools.cli.call_subprocess")
def test_import_database(call_subprocess, wordpressdata):
    """Given arguments, calls subprocess"""

    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    dump_file_path = wordpressdata.dump_file_path
    debug = False

    # Act
    sut.import_database(wordpress_path, dump_file_path, debug)

    # Assert
    call_subprocess.assert_called_once_with(commands.get("wpcli_db_import").format(
        file=dump_file_path, path=wordpress_path, debug_info=sut.convert_wp_parameter_debug(debug)),
        log_before_process=ANY, log_after_err=ANY)

# endregion

# region reset_database()


@patch("tools.cli.call_subprocess")
def test_reset_database(call_subprocess, wordpressdata):
    """Given arguments, calls subprocess"""

    # Arrange
    wordpress_path = wordpressdata.wordpress_path
    quiet = True
    debug = False

    # Act
    sut.reset_database(wordpress_path, quiet, debug)

    # Assert
    call_subprocess.assert_called_once_with(commands.get("wpcli_db_reset").format(
        path=wordpress_path, yes=sut.convert_wp_parameter_yes(quiet), debug_info=sut.convert_wp_parameter_debug(debug)),
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

# region wp_cli_info()

@patch("tools.cli.call_subprocess")
def test_wp_cli_info(call_subprocess):
    """Calls subprocess with the required command"""
    # Arrange
    info_command = "wpcli_info"
    log_before_literals = [literals.get("wp_wpcli_install_ok"), literals.get("wp_wpcli_info")]
    log_after_literals = [literals.get("wp_wpcli_add_ev")]
    # Act
    sut.wp_cli_info()
    # Assert
    call_subprocess.assert_called_once_with(
        commands.get(info_command), log_before_out=log_before_literals, log_after_out=log_after_literals)

# endregion

# region create_wordpress_database_user()


@patch("tools.cli.call_subprocess")
@pytest.mark.skip(reason="Need to fix this test")
def test_create_wordpress_database_user(call_subprocess):
    """Given arguments, when the method is called, then creates a db user"""

    # Arrange
    wordpress_path = ""
    user_name = "user1"
    user_p = "pass"
    schema = "db1"
    host = "localhost"
    privileges = "create, alter, select, insert, update, delete"

    # Act
    sut.create_wordpress_database_user(wordpress_path, user_name, user_p, schema, host, privileges)

    # Assert
    call_subprocess.assert_called()

# endregion

# region create_wordpress_database_user()


@patch("tools.cli.call_subprocess")
def test_export_content_to_wxr(call_subprocess):
    """Given arguments, when the method is called, then exports WordPress
    content"""

    # Arrange
    wordpress_path = ""
    destination_path = ""
    wxr_file_suffix = "suffix"

    # Act
    sut.export_content_to_wxr(wordpress_path, destination_path, wxr_file_suffix)

    # Assert
    call_subprocess.assert_called()

# endregion
