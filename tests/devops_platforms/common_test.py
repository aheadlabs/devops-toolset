"""Unit tests for the common file"""

from unittest.mock import patch
import devops_toolset.devops_platforms.common as sut


# region log_environment_variables()

@patch("logging.info")
def test_log_environment_variables_calls_common_code(logging_mock):
    """Returns a list of strings"""

    # Arrange
    platform_keys: list = ["key1", "key2"]

    # Act
    sut.log_environment_variables(platform_keys)

    # Assert
    logging_mock.assert_called()

# endregion
