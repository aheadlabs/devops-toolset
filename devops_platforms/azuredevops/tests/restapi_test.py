"""Unit tests for the restapi file"""

from unittest.mock import patch

import pytest

import devops_platforms.azuredevops.restapi as sut
from tools.xcoding64 import encode
from devops_platforms.azuredevops.tests.conftest import mocked_requests_get, mocked_requests_get_ko


# region generate_authentication_header


def test_generate_authentication_header_given_name_and_token_then_generate_header(platformdata):
    """ Given user_name and access_token, then encodes and generates authentication code """
    # Arrange
    user_name = platformdata.user_name
    access_token = platformdata.access_token
    token_base_64 = f"{user_name}:{access_token}"
    basic_auth_token = f"Basic {encode(token_base_64)}"
    expected_auth_token = {"Authorization": basic_auth_token}
    # Act
    result = sut.generate_authentication_header(user_name, access_token)
    # Assert
    assert result == expected_auth_token


# endregion generate_authentication_header

# region call_api

@patch("devops_platforms.azuredevops.restapi.generate_authentication_header")
@patch("logging.info")
@patch("requests.get", side_effect=mocked_requests_get)
def test_call_api_given_command_and_credentials_when_status_code_is_200_then_return_response(request_get_mock,
                                                                                             logging_mock,
                                                                                             generate_mock,
                                                                                             platformdata):
    """ Given parameters, when request return status code 200, then return the response """
    # Arrange
    headers = "my_headers"
    generate_mock.return_value = headers
    command = "my_command"
    # Act
    sut.call_api(command, platformdata.user_name, platformdata.access_token)
    # Assert
    request_get_mock.assert_called_once_with(command, headers=headers)


@patch("devops_platforms.azuredevops.restapi.generate_authentication_header")
@patch("logging.info")
@patch("requests.get", side_effect=mocked_requests_get_ko)
def test_call_api_given_command_and_credentials_when_status_code_is_not_200_then_raise_value_error(request_get_mock,
                                                                                             logging_mock,
                                                                                             generate_mock,
                                                                                             platformdata):
    """ Given parameters, when request return status code not 200, then raises a ValueError """
    # Arrange
    headers = "my_headers"
    generate_mock.return_value = headers
    command = "my_command"
    # Act
    with pytest.raises(ValueError) as value_error:
        sut.call_api(command, platformdata.user_name, platformdata.access_token)
        # Assert
        request_get_mock.assert_called_once_with(command, headers=headers)

# endregion call_api
