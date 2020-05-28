"""Test configuration file for core module.

    contains:
        - Class CoreTestsFixture: contains some static values used in tests"""

import pytest
import logging
import pathlib
import os


class CoreTestsFixture(object):
    """Class used to create the test constants fixture"""
    default_loglevel = logging.INFO
    default_handler = logging.StreamHandler()
    current_path = os.path.dirname(os.path.realpath(__file__))
    root_path = pathlib.Path(current_path).absolute()
    fake_config_file_path = pathlib.Path.joinpath(root_path, 'logging_config.json').__str__()
    fake_error_exception_message = "Exception error message"
    cannot_config_message = f"Cannot configure logger: {fake_error_exception_message}"
    default_configure_success = "Default configuration loaded successfully."
    fake_config_data_file_content = r'{"logging": {"foo": "foo"}}'
    file_open_patch = "builtins.open"
    default_backup_count = 10
    default_filepath = "./core/tests/foo_log.log"
    default_when = "midnight"


@pytest.fixture
def coretestsfixture():
    """Sample file names for testing file system related functionality"""
    return CoreTestsFixture()
