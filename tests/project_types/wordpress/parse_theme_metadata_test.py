""" Unit core for the parse_theme_metadata script """

from unittest.mock import mock_open, patch
import devops_toolset.project_types.wordpress.parse_theme_metadata as sut


# region main()


@patch("devops_toolset.filesystem.parsers.parse_theme_metadata")
def test_parse_theme_metadata_from_path_when_path_exists_then_calls_parse_theme_metadata(parse_theme_metadata_mock):
    """ Given path to theme metadata and tokens, then should read the file and call parse_theme_metadata """
    # Arrange
    css_file_path = "/pathto/cssfile"
    token1, value1, token2, value2 = "Sometoken1", "Somevalue1", "Sometoken2", "Somevalue2"
    tokens = dict()
    tokens[token1], tokens[token2] = value1, value2
    css_file_data = b"Sometoken1: Somevalue1\r\nSometoken2: Somevalue2\r\n"
    # Act
    with patch("builtins.open", new_callable=mock_open, read_data=css_file_data):
        sut.main(css_file_path, tokens)
        # Assert
        parse_theme_metadata_mock.assert_called_once_with(css_file_data, tokens, True)


# endregion
