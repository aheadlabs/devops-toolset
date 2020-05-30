"""Test configuration file for sonarx module.

Add here whatever you want to pass as a fixture in your texts."""

import pytest
import json


class SonarxData(object):
    """Class used to create the sonarxdata fixture"""
    properties_file_path = "/pathto/sonar-project.properties"
    token = "0123456789abcdef0123456789abcdef01234567"
    branch_feature = "/feature/branch"
    sonar_url = "https://sonarcloud.io"
    sonar_project_key = "devops-toolset"
    sonar_organization = "ahead-labs"
    quality_gate_json_ok = "{\"projectStatus\":{\"status\":\"OK\"}}"
    quality_gate_json_ok_object = json.loads(quality_gate_json_ok)


@pytest.fixture
def sonarxdata():
    """Sample sonarx data for testing sonarx related functionality"""
    return SonarxData()


# Mocks


def mocked_requests_get(*args, **kwargs):
    """Mock to replace requests.get()"""
    class MockResponse(object):
        """Mock response"""
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(SonarxData.quality_gate_json_ok_object, 200)
