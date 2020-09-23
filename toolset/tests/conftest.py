"""Test configuration file for wordpress module.

Add here whatever you want to pass as a fixture in your texts."""

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


@pytest.fixture
def pathsdata():
    """Sample data for testing"""
    yield PathsData()
    # Below code is executed as a TearDown
    print("Teardown finished.")
