import pytest


class PlatformData(object):
    """Class used to create the platformdata fixture"""
    environment_variables_dict = {"env_var_1": "value1", "env_var_2": "value2"}
    environment_variables_dict1 = {"env_var_1": "value1"}
    description = "Lorem ipsum dolor sit amet"


class ArtifactsData(object):
    """Class used to create the artifactsdata fixture"""
    artifact_destination_path = "/pathto/artifact/destination"
    feed_content = "{\"name\":\"feed_name\",\"package\":\"package_name\",\"version\":\"1.0.1\"," \
                   "\"organization_url\":\"https://my-organization\"}"

@pytest.fixture
def platformdata():
    """Sample data for testing"""
    return PlatformData()

@pytest.fixture
def artifactsdata():
    """Sample data for testing"""
    return ArtifactsData()
