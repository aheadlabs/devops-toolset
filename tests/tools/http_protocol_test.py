"""Unit tests for the tools/http_protocol module"""

from tests.tools.conftest import mocked_requests_get_ip
from unittest.mock import patch

import devops_toolset.tools.http_protocol as sut
import pytest

# region get_public_ip_address()


@patch("requests.get")
def test_get_public_ip_address_(requests_get_mock):
    """Given a public service URL, calls it and parses the IP address."""

    # Arrange
    public_service_url: str = "https://myservice.net"
    requests_get_mock.side_effect = mocked_requests_get_ip

    # Act
    result = sut.get_public_ip_address(public_service_url)

    # Assert
    assert result == "1.1.1.1"

# endregion
