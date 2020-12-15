"""Unit tests for the zip file"""

from unittest.mock import patch
import filesystem.zip as sut


# region download_an_unzip_file

@patch("filesystem.paths.download_file")
@patch("pathlib.Path.joinpath")
@patch("zipfile.ZipFile")
def test_download_an_unzip_file_given_parameters_then_calls_extract_all(zipfile_mock, joinpath_mock,
                                                                        download_file_mock, paths):
    """ Given parameters, then calls zip.extractall """
    # Arrange
    url = paths.url
    destination = paths.current_path
    temp_extraction_path = paths.test_path
    download_file_mock.return_value = paths.file_name, paths.test_path
    joinpath_mock.return_value = temp_extraction_path
    # Act
    sut.download_an_unzip_file(url, destination, False)
    # Assert
    zipfile_mock.assert_called_once_with(paths.test_path, 'r')


@patch("filesystem.paths.download_file")
@patch("pathlib.Path.joinpath")
@patch("zipfile.ZipFile")
@patch("os.walk")
@patch("shutil.move")
@patch("os.rmdir")
def test_download_an_unzip_file_given_parameters_when_unzip_root_is_present_then_move_files(rmdir_mock, move_mock,
    walk_mock, zipfile_mock, joinpath_mock, download_file_mock, paths):
    """ Given parameters, when unzip_root is present then walk and move files """
    # Arrange
    url = paths.url
    destination = paths.current_path
    temp_extraction_path = paths.test_path
    download_file_mock.return_value = paths.file_name, paths.test_path
    joinpath_mock.return_value = temp_extraction_path
    walk_mock.return_value = [(paths.test_path, paths.directory_path, paths.file_name)]
    # Act
    sut.download_an_unzip_file(url, destination, False, paths.test_path)
    # Assert
    move_mock.assert_called()
    rmdir_mock.assert_called()


@patch("filesystem.paths.download_file")
@patch("pathlib.Path.joinpath")
@patch("zipfile.ZipFile")
@patch("os.remove")
def test_download_an_unzip_file_given_parameters_when_delete_after_unzip_is_present_then_remove_file_path(remove_mock,
    zipfile_mock, joinpath_mock, download_file_mock, paths):
    """ Given parameters, when delete_after_unzip is present then call os.remove """
    # Arrange
    url = paths.url
    destination = paths.current_path
    temp_extraction_path = paths.test_path
    download_file_mock.return_value = paths.file_name, paths.test_path
    joinpath_mock.return_value = temp_extraction_path
    # Act
    sut.download_an_unzip_file(url, destination, True)
    # Assert
    remove_mock.assert_called_once_with(paths.test_path)


# endregion download_an_unzip_file

# region zip_directory

# endregion zip_directory

# region read_text_file_in_zip

# endregion read_text_file_in_zip