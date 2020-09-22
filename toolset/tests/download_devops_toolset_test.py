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

# endregion

# region is_valid_path()

# endregion

# region main()

# endregion


def my_joinpath(*args):
    return args[0] + args[1]
