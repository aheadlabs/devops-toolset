"""Unit tests for the log_setup file"""

import logging
from unittest.mock import patch, mock_open
import core.log_setup as sut
from core.tests.conftest import CoreTestsFixture as Fixture

# region configure(filepath)


def test_configure_given_filepath_when_exception_catch_then_logs_error():
    """Given a filepath to configure logging, when exception is catch, then logs
    with error severity"""

    # Arrange
    filepath = Fixture.fake_config_file_path
    expected_message = Fixture.cannot_config_message
    with patch.object(sut, "configure_by_file") as configure_by_file_mock:
        configure_by_file_mock.side_effect = Exception(Fixture.fake_error_exception_message)
        with patch.object(logging, "error") as logger_error_mock:
            # Act
            sut.configure(filepath)
            # Assert
            logger_error_mock.assert_called_once_with(expected_message)


def test_configure_given_filepath_when_exception_catch_then_configure_by_default():
    """Given a filepath to configure logging, when exception is catch, then calls
    configure logger by default"""

    # Arrange
    filepath = Fixture.fake_config_file_path
    with patch.object(sut, "configure_by_file") as configure_by_file_mock:
        configure_by_file_mock.side_effect = Exception(Fixture.fake_error_exception_message)
        with patch.object(sut, "configure_by_default") as configure_by_default_mock:
            # Act
            sut.configure(filepath)
            # Assert
            configure_by_default_mock.assert_called_once()


def test_configure_given_filepath_then_configure_by_file():
    """Given a filepath to configure logging, then calls
    configure logger by file"""

    # Arrange
    filepath = Fixture.fake_config_file_path
    with patch.object(sut, "configure_by_file") as configure_by_file_mock:
        # Act
        sut.configure(filepath)
        # Assert
        configure_by_file_mock.assert_called_once()

# endregion

# region configure_by_default(loglevel)


@patch.object(logging, "getLogger")
def test_configure_by_default_sets_root_logger_level(get_logger_mock):
    """Given a log level, should set loglevel to the root logger."""
    # Arrange
    loglevel = Fixture.default_loglevel
    get_logger_mock.return_value = logging.getLogger(__name__)
    with patch.object(get_logger_mock.return_value, "setLevel") as logging_setlevel_mock:
        # Act
        sut.configure_by_default(loglevel)
        # Assert
        logging_setlevel_mock.assert_called_once_with(loglevel)


@patch.object(logging, "getLogger")
def test_configure_by_default_adds_streamhandler(get_logger_mock):
    """Given a log level, should set the logging.StreamHandler() to the root logger."""
    # Arrange
    loglevel = Fixture.default_loglevel
    get_logger_mock.return_value = logging.getLogger(__name__)
    with patch.object(get_logger_mock.return_value, "addHandler") as logging_addHandler_mock:
        # Act
        sut.configure_by_default(loglevel)
        # Assert
        logging_addHandler_mock.assert_called_once()


@patch.object(logging, "getLogger")
def test_configure_by_default_logs_info(get_logger_mock):
    """Given a log level, should log a message when configuring by default."""
    # Arrange
    loglevel = Fixture.default_loglevel
    expected_message = Fixture.default_configure_success
    get_logger_mock.return_value = logging.getLogger(__name__)
    with patch.object(get_logger_mock.return_value, "info") as logging_info_mock:
        # Act
        sut.configure_by_default(loglevel)
        # Assert
        logging_info_mock.assert_called_once_with(expected_message)
# endregion

# region configure_by_file(filepath)


@patch("builtins.open", new_callable=mock_open, read_data=Fixture.fake_config_data_file_content)
def test_configure_by_file_opens_filepath_in_read_mode(open_file_mock):
    """Given a filepath, should call open with read privileges."""
    # Arrange
    from logging import config
    filepath = Fixture.fake_config_file_path
    with patch.object(config, "dictConfig") as dict_config_mock:
        dict_config_mock.return_value = None
        # Act
        sut.configure_by_file(filepath)
        # Assert
        open_file_mock.assert_called_once_with(filepath, "r")


def test_configure_by_file_calls_dict_config():
    """Given a filepath, should load the config content using json module ."""
    from logging import config
    # Arrange
    filepath = Fixture.fake_config_file_path
    with patch.object(config, "dictConfig") as dict_config_mock:
        # Act
        sut.configure_by_file(filepath)
        # Assert
        dict_config_mock.assert_called_once()
# endregion
