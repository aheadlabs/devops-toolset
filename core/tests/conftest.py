"""Test configuration file for core module.

    contains:
        - Class CoreTestsConstants: contains some static values used in tests"""

import pytest
import logging

class CoreTestsFixture(object):
    """Class used to create the test constants fixture"""
    default_loglevel = logging.INFO
    default_handler = logging.StreamHandler()
    fake_config_file_path = "./core/tests/logging_config.json"
    fake_error_exception_message = "Exception error message"
    couldnt_config_file_message = f"Couldn't configure logger: {fake_error_exception_message}"
    default_configure_success = "Default configuration loaded succesfully."
    fake_config_data_file_content = r'{"logging": {"foo": "foo"}}'
    file_open_patch = "builtins.open"

@pytest.fixture
def coretestsfixture():
    """Sample file names for testing file system related functionality"""
    return CoreTestsFixture()
