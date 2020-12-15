"""Test configuration file for parsers module.

Add here whatever you want to pass as a fixture in your tests."""
import json

import pytest


class ParsersData:
    """Class used to create the parsersdata fixture"""
    composer_json_file_path = "path/to/composer/composer.json"
    composer_file_data = \
        "{\"name\":\"project-name\", \"version\":\"0.1\"}"


@pytest.fixture
def parsersdata():
    """ Sample parsers configuration data for testing"""
    yield ParsersData()
    # Below code is executed as a TearDown
    print("Teardown finished.")

