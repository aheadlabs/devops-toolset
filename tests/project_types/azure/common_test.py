"""Unit tests for the project_types/azure/common.py module"""

from unittest.mock import patch

import devops_toolset.project_types.azure.common as sut

# region get_installed_cli_extensions()


@patch("devops_toolset.tools.cli.call_subprocess_with_result")
@patch("logging.info")
def test_get_installed_cli_extensions(logging_info_mock, subprocess_result_mock):
    """Calls subprocess with result"""

    # Arrange
    subprocess_result_mock.return_value = "{}"

    # Act
    _ = sut.get_installed_cli_extensions()

    # Assert
    subprocess_result_mock.assert_called()

# endregion get_installed_cli_extensions()

# region is_cli_extension_installed()


@patch("devops_toolset.project_types.azure.common.get_installed_cli_extensions")
def test_is_cli_extension_installed(get_installed_cli_extensions_mock):
    """Calls subprocess with result"""

    # Arrange
    extension_name = "my-extension"
    get_installed_cli_extensions_mock.return_value = [{"name": extension_name}]

    # Act
    result = sut.is_cli_extension_installed(extension_name)

    # Assert
    assert result is True

# endregion is_cli_extension_installed()
