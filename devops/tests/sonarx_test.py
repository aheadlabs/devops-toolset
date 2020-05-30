"""Unit tests for the sonarx file"""

from unittest.mock import patch, MagicMock
import devops.sonarx as sut
from devops.tests.conftest import mocked_requests_get

# region get_quality_gate_status()


@patch("requests.get", side_effect=mocked_requests_get)
@patch("devops.sonarx.logging.info")
def test_get_quality_gate_status_given_branch_then_generates_branch_segment(info, sonarxdata):
    """Given a file, when it exists in a child directory, should return its
    path"""

    # Arrange
    sut.generate_branch_segment = MagicMock(return_value=f"&branch={sonarxdata.branch_feature}")
    sut.read_sonar_properties_file = \
        MagicMock(return_value=(sonarxdata.sonar_url, sonarxdata.sonar_project_key, sonarxdata.sonar_organization))

    # Act
    sut.get_quality_gate_status(sonarxdata.properties_file_path, sonarxdata.token, sonarxdata.branch_feature)

    # Assert
    sut.generate_branch_segment.assert_called_once()

# endregion
