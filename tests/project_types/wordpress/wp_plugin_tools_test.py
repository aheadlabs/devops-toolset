"""Unit tests for the wp_plugin_tools file"""
import pathlib

import pytest
from unittest.mock import patch, ANY

import devops_toolset.project_types.wordpress.wp_plugin_tools as sut

# region create_release_tag


@patch("logging.exception")
def test_create_release_tag_logs_exception_when_exception_raised(logging_mock, pluginsdata):
    # Arrange
    plugin_root_path = pluginsdata.plugin_root_path
    tag_name = pluginsdata.tag_name

    # Act
    sut.create_release_tag(plugin_root_path, tag_name, False)

    # Assert
    logging_mock.assert_called_once()


@patch("devops_toolset.project_types.wordpress.wp_plugin_tools.__check_plugin_path_exists")
@patch("pathlib.Path.mkdir")
def test_create_release_tag_creates_structure_when_path_not_already_exist(
        mkdir_mock, _, pluginsdata):
    # Arrange
    plugin_root_path = pluginsdata.plugin_root_path
    tag_name = pluginsdata.tag_name
    plugin_tag_path = pathlib.Path(plugin_root_path).joinpath(tag_name)

    # Act
    sut.create_release_tag(plugin_root_path, tag_name, False)

    # Assert
    mkdir_mock.assert_called_once_with(plugin_tag_path)


@patch("devops_toolset.project_types.wordpress.wp_plugin_tools.__check_plugin_path_exists")
@patch("pathlib.Path.mkdir")
@patch("pathlib.Path.exists")
@patch("logging.warning")
def test_create_release_tag_warns_when_path_already_exist(
        logging_mock, exists_mock, mkdir_mock, _, pluginsdata):
    # Arrange
    plugin_root_path = pluginsdata.plugin_root_path
    tag_name = pluginsdata.tag_name
    exists_mock.return_value = True

    # Act
    sut.create_release_tag(plugin_root_path, tag_name, False)

    # Assert
    logging_mock.assert_called_once()


def test_create_release_tag_copies_trunk_when_copy_trunk_is_true():
    pass

# endregion create_release_tag

# region deploy_current_trunk


@patch("logging.exception")
def test_deploy_current_trunk_logs_exception_when_exception_raised(logging_mock, pluginsdata):
    # Arrange
    plugin_root_path = pluginsdata.plugin_root_path
    commit_message = pluginsdata.commit_message
    username = pluginsdata.username
    password = pluginsdata.password

    # Act
    sut.deploy_current_trunk(plugin_root_path, commit_message, username, password)

    # Assert
    logging_mock.assert_called_once()


def test_deploy_current_trunk_calls_svn_add():
    pass


def test_deploy_current_trunk_calls_svn_checkin():
    pass


def test_deploy_current_trunk_raises_error_when_trunk_path_is_not_present():
    pass

# endregion deploy_current_trunk


# region deploy_release_tag


@patch("logging.exception")
def test_deploy_release_tag_logs_exception_when_exception_raised(logging_mock, pluginsdata):
    # Arrange
    plugin_root_path = pluginsdata.plugin_root_path
    commit_message = pluginsdata.commit_message
    username = pluginsdata.username
    password = pluginsdata.password
    tag_name = pluginsdata.tag_name

    # Act
    sut.deploy_release_tag(plugin_root_path, tag_name, commit_message, username, password)

    # Assert
    logging_mock.assert_called_once()


def test_deploy_release_tag_calls_create_release_tag():
    pass


def test_deploy_release_tag_calls_svn_add():
    pass


def test_deploy_release_tag_calls_svn_checkin():
    pass

# endregion deploy_release_tag


# region __check_parameters

def test__check_parameters_raises_error_when_commit_message_is_none():
    pass


def test__check_parameters_raises_error_when_username_is_none():
    pass


def test__check_parameters_returns_doing_noting_when_parameters_are_present():
    pass

# endregion __check_parameters


# region __check_plugin_path_exists

def test__check_plugin_path_exists_raises_error_when_path_exists():
    pass


def test__check_plugin_path_exists_returns_when_path_not_exists():
    pass

# endregion __check_plugin_path_exists
