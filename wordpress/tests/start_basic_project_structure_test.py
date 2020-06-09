"""Unit tests for the sonarx file"""

from unittest.mock import patch
from core.LiteralsCore import LiteralsCore
from wordpress.Literals import Literals as WordpressLiterals
import wordpress.wptools as wp_tools
import wordpress.start_basic_project_structure as sut

literals = LiteralsCore([WordpressLiterals])

# region main


@patch.object(wp_tools, "get_project_structure")
def test_main_given_parameters_must_call_wptools_get_project_structure(get_project_structure_mock, wordpressdata):
    """Given arguments, must call get_project_structure with passed project_path"""
    # Arrange
    project_structure_path = wordpressdata.project_structure_path
    root_path = wordpressdata.wordpress_path
    get_project_structure_mock.return_value = {"items": {}}
    # Act
    sut.main(root_path, project_structure_path)
    # Assert
    get_project_structure_mock.assert_called_once_with(project_structure_path)


@patch.object(wp_tools, "get_project_structure")
@patch.object(sut, "add_item")
def test_main_given_parameters_must_call_wptools_get_project_structure(add_item_mock,
                                                                       get_project_structure_mock,
                                                                       wordpressdata):
    """Given arguments, must call get_project_structure with passed project_path"""
    # Arrange
    project_structure_path = wordpressdata.project_structure_path
    root_path = wordpressdata.wordpress_path
    items_data = {"items": {'foo_item': 'foo_value'}}
    get_project_structure_mock.return_value = items_data
    # Act
    sut.main(root_path, project_structure_path)
    # Assert
    add_item_mock.assert_called_once_with('foo_item', root_path)

# endregion main
