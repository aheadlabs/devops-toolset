""" Unit tests for the project_types/azure/api_management.py module"""

from unittest.mock import patch
from devops_toolset.project_types.azure import api_management

# region check_apim_exists()


@patch('devops_toolset.project_types.azure.api_management.cli')
@patch('devops_toolset.project_types.azure.api_management.logging')
def test_check_apim_exists_when_resource_found(logging_mock, cli_mock):
    """Should return True when the resource is found."""

    # Arrange
    cli_mock.call_subprocess_with_result.return_value = '{}'

    # Act
    result = api_management.check_apim_exists('resource_group_name', 'apim_name')

    # Assert
    assert result is True


@patch('devops_toolset.project_types.azure.api_management.cli')
@patch('devops_toolset.project_types.azure.api_management.logging')
def test_check_apim_exists_when_resource_not_found_in_tuple(logging_mock, cli_mock):
    """Should return False when the resource is not found and result is a tuple."""

    # Arrange
    cli_mock.call_subprocess_with_result.return_value = (None, 'ResourceNotFound')

    # Act
    result = api_management.check_apim_exists('resource_group_name', 'apim_name')

    # Assert
    assert result is False


@patch('devops_toolset.project_types.azure.api_management.cli')
@patch('devops_toolset.project_types.azure.api_management.logging')
def test_check_apim_exists_when_resource_not_found_in_string(logging_mock, cli_mock):
    """Should return False when the resource is not found and result is a string."""

    # Arrange
    cli_mock.call_subprocess_with_result.return_value = 'ResourceNotFound'

    # Act
    result = api_management.check_apim_exists('resource_group_name', 'apim_name')

    # Assert
    assert result is False

# endregion
