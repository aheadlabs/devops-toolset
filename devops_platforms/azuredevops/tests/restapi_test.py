"""Unit tests for the restapi file"""

from unittest.mock import patch

import pytest

from core.app import App
import devops_platforms.azuredevops.restapi as sut
from tools.xcoding64 import encode
from devops_platforms.azuredevops.tests.conftest import mocked_requests_get, mocked_requests_get_ko
from core.CommandsCore import CommandsCore
from devops_platforms.azuredevops.commands import Commands as PlatformSpecificCommands

app: App = App()
commands = CommandsCore([PlatformSpecificCommands])


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
    with pytest.raises(ValueError):
        sut.call_api(command, platformdata.user_name, platformdata.access_token)
        # Assert
        request_get_mock.assert_called_once_with(command, headers=headers)

# endregion call_api

# region get_build_list


@patch("devops_platforms.azuredevops.restapi.call_api")
def test_get_build_list_given_args_call_api_with_command_and_credentials(call_api_mock, platformdata):
    """ Given organization and credentials, then retrieves command and calls api """
    # Arrange
    organization = platformdata.organization
    project = platformdata.project
    user_name = platformdata.user_name
    access_token = platformdata.access_token
    command = commands.get("azdevops_rest_get_build_list").format(organization=organization, project=project)
    # Act
    sut.get_build_list(organization, project, user_name, access_token)
    # Assert
    call_api_mock.assert_called_once_with(command, user_name, access_token)

# endregion get_build_list

# region get_build


@patch("devops_platforms.azuredevops.restapi.call_api")
def test_get_build_given_args_call_api_with_args(call_api_mock, platformdata, artifactsdata):
    """ Given parameters, then retrieves command and calls api """
    # Arrange
    organization = platformdata.organization
    project = platformdata.project
    user_name = platformdata.user_name
    access_token = platformdata.access_token
    artifact_name = artifactsdata.artifact_name
    build_id = artifactsdata.build_id
    command = commands.get("azdevops_rest_get_build").format(
        organization=organization, project=project, build_id=build_id, artifact_name=artifact_name)
    # Act
    sut.get_build(organization, project, build_id, artifact_name, user_name, access_token)
    # Assert
    call_api_mock.assert_called_once_with(command, user_name, access_token)

# endregion get_build

