"""Unit core for the tools file"""

import devops_toolset.filesystem.tools as sut
from unittest.mock import patch
import pytest



# region update_xml_file_entity_text()


@patch("xml.etree.ElementTree.parse")
def test_update_xml_file_entity_text_parse_file(parse_mock):
    """Given an XML file path parse its content."""

    # Act
    sut.update_xml_file_entity_text("", "", "file.xml")

    # Assert
    parse_mock.assert_called_once_with("file.xml")


# endregion

# region is_file_empty


@patch("os.path.getsize")
@pytest.mark.parametrize("getsize_result, expected_result", [(0, True), (5, False)])
def test_is_file_empty_given_path_when_empty_then_return_true(getsize_mock, getsize_result, expected_result, paths):
    """Given an empty file return True."""

    # Arrange
    path = paths.test_path
    getsize_mock.return_value = getsize_result
    # Act
    result = sut.is_file_empty(path)

    # Assert
    assert result == expected_result

# endregion
