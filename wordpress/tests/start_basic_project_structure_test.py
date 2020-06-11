""" Unit tests for the start_basic_structure_test file """
import os
from unittest.mock import patch, call, mock_open
from core.LiteralsCore import LiteralsCore
from wordpress.Literals import Literals as WordpressLiterals

import filesystem.paths as path_tools
import pathlib
import pytest
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

# region condition_met()


@pytest.mark.parametrize('item, expected', [
    ({"condition": "foo_value"}, True),
    ({"foo_condition": "when-parent-not-empty"}, True)])
def test_condition_met_should_return_true_when_cond_not_in_item_or_condition_not_when_parent_not_empty(item,
                                                                                                       expected,
                                                                                                       wordpressdata):
    """ Given item and base_path parameters, should return True if "condition" is not
    part of item keys """
    # Arrange
    base_path = wordpressdata.wordpress_path
    # Act
    result = sut.condition_met(item, base_path)
    # Assert
    assert result == expected


@patch.object(path_tools, "is_empty_dir")
def test_condition_met_given_parameters_should_call_is_empty_dir_result(is_empty_dir_mock, wordpressdata):
    """ Given item and base_path parameters, should call is empty dir method """
    # Arrange
    item = {"condition": "when-parent-not-empty"}
    base_path = wordpressdata.wordpress_path
    # Act
    sut.condition_met(item, base_path)
    # Assert
    is_empty_dir_mock.assert_called_once_with(base_path)

# endregion condition_met()

# region add_item()


@patch.object(sut, "condition_met", return_value=False)
def test_add_item_given_parameters_should_call_condition_met_when_item_has_children_object(condition_met_mock
                                                                                           ,wordpressdata):
    """ Given an item and base_path should call condition_met when has children inside item """
    # Arrange
    item = {"type": "directory", "name": "foo_directory"}
    base_path = wordpressdata.wordpress_path
    with patch.object(path_tools, "is_valid_path", return_value=False):
        # Act
        sut.add_item(item, base_path)
        # Assert
        condition_met_mock.assert_not_called


@patch.object(sut, "condition_met", return_value=False)
def test_add_item_given_parameters_when_child_condition_is_false_and_have_children_then_calls_recursive_add_item(
        condition_met_mock
        , wordpressdata):
    """ Given an item and base_path should call add-item recursively
     when the item has children inside"""
    # Arrange
    item = {"type": "directory", "name": "foo_directory", "children": [{"name": "foo_file"}]}
    base_path = wordpressdata.wordpress_path
    expected_path_1 = str(pathlib.Path.joinpath(pathlib.Path(base_path), "foo_directory"))
    expected_path_2 = str(pathlib.Path.joinpath(pathlib.Path(expected_path_1), "foo_file"))
    with patch.object(path_tools, "is_valid_path", return_value=False) as is_valid_path_mock:
        # Act
        sut.add_item(item, base_path)
        # Assert
        calls = [call(expected_path_1),
                 call(expected_path_2)]
        is_valid_path_mock.assert_has_calls(calls, any_order=True)


@patch.object(sut, "condition_met", return_value=True)
@patch.object(os, "mkdir")
def test_add_item_given_parameters_when_child_condition_and_type_is_directory_should_call_os_mkdir(
        os_mkdir_mock
        , condition_met_mock
        , wordpressdata):
    """ Given an item and base_path should call os.mkdir with the destination path
     when the item has type directory """
    # Arrange
    expected_directory = "foo_directory"
    item = {"type": "directory", "name": expected_directory, "children": [{"name": "foo_file"}]}
    base_path = wordpressdata.wordpress_path
    expected_final_path = pathlib.Path.joinpath(pathlib.Path(base_path), "foo_directory")
    with patch.object(path_tools, "is_valid_path", return_value=False):
        # Act
        sut.add_item(item, base_path)
        # Assert
        os_mkdir_mock.assert_called_once_with(expected_final_path)


@patch.object(sut, "condition_met", return_value=True)
@patch("builtins.open", new_callable=mock_open)
@patch.object(sut, "get_default_content")
def test_add_item_given_parameters_when_child_condition_and_type_is_file_should_create_empty_file(
        get_default_content_mock
        , file_mock
        , condition_met_mock
        , wordpressdata):
    """ Given an item and base_path should create a file with the destination path
     when the item has type file and no default content is present """
    # Arrange
    expected_file = "foo_file"
    item = {"type": "file", "name": expected_file, "children": [{"name": expected_file}]}
    base_path = wordpressdata.wordpress_path
    expected_final_path = pathlib.Path.joinpath(pathlib.Path(base_path), expected_file)
    with patch.object(path_tools, "is_valid_path", return_value=False):
        # Act
        sut.add_item(item, base_path)
        # Assert
        get_default_content_mock.assert_not_called()


@patch.object(sut, "condition_met", return_value=True)
@patch.object(sut, "get_default_content", return_value="")
def test_add_item_given_parameters_when_child_condition_and_type_is_file_should_create_content_file(
        get_default_content_mock
        , condition_met_mock
        , wordpressdata):
    """ Given an item and base_path should write default content
     when the item has type file and default content is present """

    # Arrange
    expected_file = "foo_file"
    item = {"type": "file", "name": expected_file,
            "default_content": "foo_content",
            "children": [{"name": expected_file}]}
    base_path = wordpressdata.wordpress_path
    m = mock_open()
    with patch(wordpressdata.builtins_open, m, create=True):
        with patch.object(path_tools, "is_valid_path", return_value=False):
        # Act
            sut.add_item(item, base_path)
        # Assert
        handler = m()
        handler.write.assert_called_once_with("")


# endregion add_item()

# region get_default_content()


def test_get_default_content_given_item_when_source_is_raw_then_return_value():
    """Given item when source has value raw, then return value content"""
    # Arrange
    # Act
    # Assert
    pass


def test_get_default_content_given_item_when_source_is_from_file_then_return_content_file_read():
    """Given item when source has value from file then should call content file read()"""
    # Arrange
    # Act
    # Assert
    pass


def test_get_default_content_given_item_when_source_is_from_url_then_return_requests_get_item_value():
    """Given item when source has value from url then should call requests get at value """
    # Arrange
    # Act
    # Assert
    pass

# endregion get_default_content()
