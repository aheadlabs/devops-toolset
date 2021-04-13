"""Unit tests for the tools file"""

import filesystem.tools as sut
from unittest.mock import patch



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


def test_is_file_empty_on_empty_file(tmp_path):
    """Given an empty file return True."""

    # Act
    result = sut.is_file_empty(tmp_path)

    # Assert
    assert result


# endregion
