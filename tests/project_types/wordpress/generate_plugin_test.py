""" Unit core for the generate plugin script """

import json
import pathlib
from unittest.mock import patch, mock_open, ANY

import pytest

import devops_toolset.project_types.wordpress.generate_plugin as sut
from tests.project_types.wordpress.conftest import mocked_requests_get

# region main


@patch("os.path.exists")
def test_main_given_path_when_not_exist_then_raise_error(exists_mock, wordpressdata):
    """ Given plugin root path, when not exists, then raise error """
    # Arrange
    exists_mock.return_value = False
    # Act
    with pytest.raises(NotADirectoryError) as error:
        sut.main(wordpressdata.root_path)
    # Assert
    assert str(error.value) == sut.literals.get("wp_non_valid_dir_path")


@patch("devops_toolset.filesystem.paths.move_files")
@patch("devops_toolset.tools.git.purge_gitkeep")
@patch("devops_toolset.project_types.wordpress.generate_plugin.teardown")
@patch("logging.info")
@patch("devops_toolset.core.log_tools.log_indented_list")
@patch("devops_toolset.filesystem.paths.files_exist_filtered")
@patch("os.path.exists")
@patch("devops_toolset.project_types.wordpress.generate_plugin.get_and_parse_required_plugin_file")
@patch("devops_toolset.project_types.wordpress.generate_plugin.create_plugin")
def test_main_given_required_files_when_present_then_calls_create_plugin_with_files_content(
       create_plugin, parse_required_file_mock, path_exist_mock, files_exist_mock, log_indented_mock,
        logging_mock, teardown_mock, purge_gitkeep_mock, move_files_mock, pluginsdata):
    """ Given root_path, when required files present in root_path, then calls create_plugin with files content """
    # Arrange
    path_exist_mock.return_value = True
    files_exist_mock.return_value = []
    parse_required_file_mock.return_value = pluginsdata.plugin_config
    # Act
    sut.main(pluginsdata.plugin_root_path)
    # Assert
    create_plugin.assert_called_with(pluginsdata.plugin_config, pluginsdata.plugin_config, pluginsdata.plugin_root_path)


@patch("devops_toolset.filesystem.paths.move_files")
@patch("devops_toolset.tools.git.purge_gitkeep")
@patch("devops_toolset.project_types.wordpress.generate_plugin.teardown")
@patch("logging.info")
@patch("devops_toolset.core.log_tools.log_indented_list")
@patch("devops_toolset.filesystem.paths.files_exist_filtered")
@patch("os.path.exists")
@patch("devops_toolset.project_types.wordpress.generate_plugin.get_and_parse_required_plugin_file")
@patch("devops_toolset.project_types.wordpress.generate_plugin.create_plugin")
def test_main_given_required_files_when_present_then_calls_teardown(
       create_plugin, parse_required_file_mock, path_exist_mock, files_exist_mock, log_indented_mock,
        logging_mock, teardown_mock, purge_gitkeep_mock, move_files_mock, pluginsdata):
    """ Given root_path, when required files present in root_path, then calls teardown """
    # Arrange
    path_exist_mock.return_value = True
    files_exist_mock.return_value = []
    parse_required_file_mock.return_value = pluginsdata.plugin_config
    # Act
    sut.main(pluginsdata.plugin_root_path)
    # Assert
    teardown_mock.assert_called_with(pluginsdata.plugin_root_path)


@patch("devops_toolset.filesystem.paths.move_files")
@patch("devops_toolset.tools.git.purge_gitkeep")
@patch("devops_toolset.project_types.wordpress.generate_plugin.teardown")
@patch("logging.info")
@patch("devops_toolset.core.log_tools.log_indented_list")
@patch("devops_toolset.filesystem.paths.files_exist_filtered")
@patch("os.path.exists")
@patch("devops_toolset.project_types.wordpress.generate_plugin.get_and_parse_required_plugin_file")
@patch("devops_toolset.project_types.wordpress.generate_plugin.create_plugin")
@patch("clint.textui.prompt.yn")
def test_main_given_required_files_when_not_present_and_use_defaults_then_download_defaults(
       prompt_yn_mock, create_plugin, parse_required_file_mock, path_exist_mock, files_exist_mock,
        log_indented_mock, logging_mock, teardown_mock, purge_gitkeep_mock, move_files_mock, pluginsdata, wordpressdata,
        mocks):
    """ Given root_path, when required files not present in root_path and using defaults,
    then downlaods default files """
    # Arrange
    path_exist_mock.return_value = True
    prompt_yn_mock.return_value = True
    files_exist_mock.return_value = ["*plugin-config.json", "*plugin-structure.json"]
    mocks.requests_get_mock.side_effect = mocked_requests_get
    parse_required_file_mock.return_value = pluginsdata.plugin_config
    m = mock_open()
    expected_content = b"sample response in bytes"
    # Act
    with patch(wordpressdata.builtins_open, m, create=True):
        sut.main(pluginsdata.plugin_root_path)
        # Assert
        handler = m()
        handler.write.assert_called_with(expected_content)


@patch("devops_toolset.filesystem.paths.move_files")
@patch("devops_toolset.tools.git.purge_gitkeep")
@patch("devops_toolset.project_types.wordpress.generate_plugin.teardown")
@patch("logging.info")
@patch("devops_toolset.core.log_tools.log_indented_list")
@patch("devops_toolset.filesystem.paths.files_exist_filtered")
@patch("os.path.exists")
@patch("devops_toolset.project_types.wordpress.generate_plugin.get_and_parse_required_plugin_file")
@patch("devops_toolset.project_types.wordpress.generate_plugin.create_plugin")
@patch("clint.textui.prompt.yn")
@patch("logging.critical")
def test_main_given_required_files_when_not_present_and_not_use_defaults_then_raise_error(
       logging_critical_mock, prompt_yn_mock, create_plugin, parse_required_file_mock, path_exist_mock,
        files_exist_mock, log_indented_mock, logging_mock, teardown_mock, purge_gitkeep_mock, move_files_mock,
        pluginsdata):
    """ Given root_path, when required files not present in root_path and using defaults,
    then downlaods default files """
    # Arrange
    path_exist_mock.return_value = True
    prompt_yn_mock.return_value = False
    files_exist_mock.return_value = ["*plugin-config.json", "*plugin-structure.json"]
    parse_required_file_mock.return_value = pluginsdata.plugin_config
    # Act
    with pytest.raises(ValueError) as error:
        sut.main(pluginsdata.plugin_root_path)
        # Assert
        logging_critical_mock.assert_called_with(ANY)
        assert error is not None

# endregion

# region get_and_parse_required_plugin_file()


@patch("os.path.exists")
@patch("devops_toolset.filesystem.paths.get_file_path_from_pattern")
def test_get_and_parse_required_plugin_file_raises_error_when_path_not_exists(get_file_mock, exists_mock, pluginsdata):
    """ Given root path, when not exists, then raises FileNotFoundError """
    # Arrange
    exists_mock.return_value = False
    # Act
    with pytest.raises(FileNotFoundError) as error:
        sut.get_and_parse_required_plugin_file(pluginsdata.plugin_root_path, "")
        # Assert
        assert error is not None


@patch("os.path.exists")
@patch("devops_toolset.filesystem.paths.get_file_path_from_pattern")
def test_get_and_parse_required_plugin_file_reads_and_parses_plugin_file(get_file_mock, exists_mock,
                                                                         wordpressdata, pluginsdata):
    """ Given root path, when not exists, then raises FileNotFoundError """
    # Arrange
    exists_mock.return_value = True
    # Act
    expected_content = json.loads(pluginsdata.plugin_config)
    with patch(wordpressdata.builtins_open, new_callable=mock_open, read_data=pluginsdata.plugin_config):
        result = sut.get_and_parse_required_plugin_file(pluginsdata.plugin_root_path, "")
        # Assert
        assert result == expected_content

# endregion get_and_parse_required_plugin_file()

# region teardown()


@patch("devops_toolset.filesystem.paths.move_files")
@patch("devops_toolset.tools.git.purge_gitkeep")
def test_teardown_move_files_to_devops_path(purge_gitkeep_mock, move_files_mock, pluginsdata):
    """ Given root path, then moves files to devops path """
    # Arrange
    root_path = pluginsdata.plugin_root_path
    devops_path = pathlib.Path.joinpath(pathlib.Path(root_path), '.devops').as_posix()
    # Act
    sut.teardown(root_path)
    # Assert
    move_files_mock.assert_called_with(root_path, devops_path, "*.json", False)


@patch("devops_toolset.filesystem.paths.move_files")
@patch("devops_toolset.tools.git.purge_gitkeep")
def test_teardown_purges_gitkeep_on_devops_path(purge_gitkeep_mock, move_files_mock, pluginsdata):
    """ Given root path, then purges .gitkeep file under devops path """
    # Arrange
    root_path = pluginsdata.plugin_root_path
    devops_path = pathlib.Path.joinpath(pathlib.Path(root_path), '.devops').as_posix()
    # Act
    sut.teardown(root_path)
    # Assert
    purge_gitkeep_mock.assert_called_with(devops_path)

# endregion teardown()

