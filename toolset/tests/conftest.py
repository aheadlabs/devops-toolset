"""Test configuration file for wordpress module.

Add here whatever you want to pass as a fixture in your texts."""
import json

import pytest
import requests
from unittest import mock


class PathsData:
    """Class used to create the pathsdata fixture"""

    full_destination_path = "/pathto/devops-toolset/"
    internal_directory = "devops_toolset-branch/"
    temporary_extraction_path = "/pathto/temporary_extraction/"
    destination_path = "/pathto/destination/"
    toolset_name = "devops-toolset"
    branch = "main/branch"
    builtins_open = "builtins.open"


@pytest.fixture
def pathsdata():
    """Sample data for testing"""
    yield PathsData()
    # Below code is executed as a TearDown
    print("Teardown finished.")

# Mocks


def mocked_requests_get(url: str, *args, **kwargs):
    """Mock to replace requests.get()"""

    # Default values
    bytes_content = b"sample response in bytes"
    text_content = "sample text response"

    # Return instance
    return MockResponse(bytes_content, text_content)


class MockResponse:
    """This is the mocked Response object returned by requests.get()"""
    def __init__(self, b_content, text_content):
        self.content = b_content
        self.text = text_content
