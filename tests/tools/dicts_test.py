"""Unit core for the dicts file"""

import devops_toolset.tools.dicts as sut


# region filter_keys()


def test_filter_keys():
    """Given a dictionary and a regular expression, then return a list with
    the filtered keys."""
    # Arrange
    key_list = {"key_1": "value_1", "key_2": "value_2"}
    regex = "2"
    expected_result = ["key_2"]

    # Act
    result = sut.filter_keys(key_list, regex)

    # Assert
    assert result == expected_result


# endregion
