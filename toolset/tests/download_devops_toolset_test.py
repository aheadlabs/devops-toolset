""" Unit tests for the download_devops_toolset_file """
from unittest.mock import patch, call
import toolset.download_devops_toolset as sut

# region cleanup()


@patch("os.remove")
@patch("os.rmdir")
@patch("toolset.download_devops_toolset.logger.info")
def test_cleanup_given_args_then_should_call_os_rmdir(logging_mock, rm_dir_mock, remove_mock, pathsdata):
    """ Given argument paths, should always call os.rmdir() and os.remove() """
    # Arrange
    internal_directory_full_path = pathsdata.internal_directory
    temporary_extraction_path = pathsdata.temporary_extraction_path
    full_destination_path = pathsdata.full_destination_path
    # Act
    sut.cleanup(full_destination_path, internal_directory_full_path, temporary_extraction_path)
    # Assert
    calls = [call(internal_directory_full_path),
             call(temporary_extraction_path)]
    rm_dir_mock.assert_has_calls(calls, any_order=True)


@patch("os.remove")
@patch("os.rmdir")
@patch("toolset.download_devops_toolset.logger.info")
def test_cleanup_given_args_then_should_call_os_remove(logging_mock, rm_dir_mock, remove_mock, pathsdata):
    """ Given argument paths, should always call os.rmdir() and os.remove() """
    # Arrange
    internal_directory_full_path = pathsdata.internal_directory
    temporary_extraction_path = pathsdata.temporary_extraction_path
    full_destination_path = pathsdata.full_destination_path
    # Act
    sut.cleanup(full_destination_path, internal_directory_full_path, temporary_extraction_path)
    # Assert
    remove_mock.assert_called_once_with(full_destination_path)

# endregion

# region decompress_toolset()


@patch("toolset.download_devops_toolset.zipfile.ZipFile")
@patch("os.listdir")
@patch("shutil.move")
@patch("toolset.download_devops_toolset.logger.info")
def test_decompress_toolset_given_paths_should_call_zip_extract_all_to_temp_path(
        logging_mock, shutil_mock, listdir_mock, zipfile_mock, pathsdata):
    """ Given paths as args, should compose the temp path and call extract all to that path """
    # Arrange
    temp_extraction_path = pathsdata.temporary_extraction_path
    destination_path = pathsdata.destination_path
    full_destination_path = pathsdata.full_destination_path
    internal_directory = pathsdata.internal_directory
    # Act
    with patch("pathlib.Path.joinpath") as joinpath_mock:
        joinpath_mock.return_value = temp_extraction_path
        sut.decompress_toolset(destination_path, full_destination_path, internal_directory)
        # Assert
        zipfile_mock.assert_called_once_with(full_destination_path, "r")


@patch("toolset.download_devops_toolset.zipfile.ZipFile")
@patch("os.listdir")
@patch("shutil.move")
@patch("pathlib.Path.joinpath")
@patch("toolset.download_devops_toolset.logger.info")
def test_decompress_toolset_given_paths_should_move_items_to_destination_path(
    logging_mock, joinpath_mock, shutil_mock, listdir_mock, zipfile_mock, pathsdata):
    """ Given paths as args, should call shutil.move items on internal path to destination path """
    destination_path = pathsdata.destination_path
    temp_extraction_path = destination_path + "__temp"
    full_destination_path = pathsdata.full_destination_path
    internal_directory = pathsdata.internal_directory
    joinpath_mock.side_effect = my_joinpath
    internal_directory_full_path = temp_extraction_path + internal_directory
    item1 = "item1"
    item2 = "item2"
    listdir_mock.return_value = [item1, item2]
    frompath1 = internal_directory_full_path + item1
    frompath2 = internal_directory_full_path + item2
    topath1 = destination_path + item1
    topath2 = destination_path + item2
    # Act
    sut.decompress_toolset(destination_path, full_destination_path, internal_directory)
    # Assert
    calls = [call(frompath1, topath1),
             call(frompath2, topath2)]
    shutil_mock.assert_has_calls(calls, any_order=True)


@patch("toolset.download_devops_toolset.zipfile.ZipFile")
@patch("os.listdir")
@patch("shutil.move")
@patch("pathlib.Path.joinpath")
@patch("toolset.download_devops_toolset.logger.info")
def test_decompress_toolset_given_paths_should_return_internal_full_path_and_temporary_extraction_path(
    logging_mock, joinpath_mock, shutil_mock, listdir_mock, zipfile_mock, pathsdata
):
    """ Given paths as args, should return the internal path and the temporary path """
    # Arrange
    joinpath_mock.side_effect = my_joinpath
    destination_path = pathsdata.destination_path
    temp_extraction_path = destination_path + "__temp"
    full_destination_path = pathsdata.full_destination_path
    internal_directory = pathsdata.internal_directory
    internal_directory_full_path = temp_extraction_path + internal_directory
    # Act
    result_internal_directory_full_path, result_temporary_extraction_path = \
        sut.decompress_toolset(destination_path, full_destination_path, internal_directory)
    # Assert
    assert internal_directory_full_path == result_internal_directory_full_path
    assert temp_extraction_path == result_temporary_extraction_path

# endregion

# region download_toolset()

# TODO (alberto.carbonell) Implement this tests
def test_download_toolset_given_args_when_not_exist_destination_path_then_create_it():
    """ Given destination path when it doesn't exist then use os.mkdir to create it """
    pass


def test_download_toolset_given_args_then_write_response_content_to_full_destination_path():
    """  """
    pass


def test_download_toolset_given_args_then_returns_destination_path_and_full_destination_path():
    """  """
    pass

# endregion

# region is_valid_path()


def test_is_valid_path_given_path_when_path_is_none_then_return_false():
    """ Given path, when its None, then return false """
    # Arrange
    path = None
    # Act
    result = sut.is_valid_path(path)
    # Assert
    assert not result


def test_is_valid_path_given_path_when_path_strip_is_empty_then_return_false():
    """ Given path, when its None, then return false """
    # Arrange
    path = ""
    # Act
    result = sut.is_valid_path(path)
    # Assert
    assert not result


def test_is_valid_path_given_path_when_path_is_valid_then_return_true():
    """ Given path, when its None, then return false """
    # Arrange
    path = "somepath/that/is/valid/"
    # Act
    result = sut.is_valid_path(path)
    # Assert
    assert result

# endregion

# region main()


@patch("os.remove")
@patch("toolset.download_devops_toolset.cleanup")
@patch("toolset.download_devops_toolset.download_toolset")
@patch("toolset.download_devops_toolset.decompress_toolset")
def test_main_given_args_then_call_download_toolset(
        decompress_toolset_mock, download_toolset_mock, cleanup_mock, os_remove_mock, pathsdata):
    """ Given destination path and branch then compose required paths and call download_toolset() """
    # Arrange
    toolset_name = pathsdata.toolset_name
    branch = pathsdata.branch
    destination_path = pathsdata.destination_path
    download_toolset_mock.return_value = ("result1", "result2")
    decompress_toolset_mock.return_value = ("result1", "result2")
    # Act
    sut.main(destination_path, branch)
    # Assert
    download_toolset_mock.assert_called_once_with(branch, destination_path, toolset_name)


@patch("os.remove")
@patch("toolset.download_devops_toolset.cleanup")
@patch("toolset.download_devops_toolset.download_toolset")
@patch("toolset.download_devops_toolset.decompress_toolset")
def test_main_given_args_then_call_decompress_toolset(
        decompress_toolset_mock, download_toolset_mock, cleanup_mock, os_remove_mock, pathsdata):
    """ Given destination path and branch then compose required paths and call decompress_toolset() """
    # Arrange
    destination_path = pathsdata.destination_path
    destination_path_object = destination_path
    full_destination_path = pathsdata.full_destination_path
    download_toolset_mock.return_value = (destination_path_object, full_destination_path)
    decompress_toolset_mock.return_value = ("result1", "result2")
    dashed_branch = pathsdata.branch.replace("/", "-")
    internal_directory = f"{pathsdata.toolset_name}-{dashed_branch}"
    # Act
    sut.main(destination_path, pathsdata.branch)
    # Assert
    decompress_toolset_mock.assert_called_once_with(destination_path_object, full_destination_path, internal_directory)


@patch("os.remove")
@patch("toolset.download_devops_toolset.cleanup")
@patch("toolset.download_devops_toolset.download_toolset")
@patch("toolset.download_devops_toolset.decompress_toolset")
def test_main_given_args_then_call_cleanup(
        decompress_toolset_mock, download_toolset_mock, cleanup_mock, os_remove_mock, pathsdata):
    """  Given destination path and branch then compose required paths and call cleanup() """
    # Arrange
    destination_path = pathsdata.destination_path
    full_destination_path = pathsdata.full_destination_path
    download_toolset_mock.return_value = (destination_path, full_destination_path)
    internal_directory = f"{pathsdata.toolset_name}-{pathsdata.branch}"
    internal_directory_full_path = destination_path + internal_directory
    temporary_extraction_path = pathsdata.temporary_extraction_path
    decompress_toolset_mock.return_value = (internal_directory_full_path, temporary_extraction_path)
    # Act
    sut.main(destination_path, pathsdata.branch)
    # Assert
    cleanup_mock.assert_called_once_with(full_destination_path, internal_directory_full_path, temporary_extraction_path)

# endregion


def my_joinpath(*args):
    """ Just a side effect function to replace the real os.joinpath() """
    return args[0] + args[1]
