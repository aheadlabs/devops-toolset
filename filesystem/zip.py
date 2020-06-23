"""Supports al compression / decompression operations in the file system."""

import filesystem.constants as constants
import filesystem.paths
import os
import pathlib
import shutil
import zipfile
from core.app import App

app: App = App()


def download_an_unzip_file(url: str, destination: str, delete_after_unzip: bool = True, unzip_root: str = None):
    """Downloads and unzips a file from a URL.

    Args:
        url: Where to download the file from.
        destination: Where to download and unzip the file.
        delete_after_unzip: If True it deletes the file after unzipping it.
        unzip_root: Determines which directory inside the zip file is the root
            directory.
    """

    file_name, file_path = filesystem.paths.download_file(url, destination, constants.FileType.BINARY)
    destination_path = pathlib.Path(destination)
    temp_extraction_path = pathlib.Path.joinpath(destination_path, constants.FileNames.TEMP_DIRECTORY)

    with zipfile.ZipFile(file_path, "r") as zip_file:
        zip_file.extractall(temp_extraction_path)

    if unzip_root is not None:
        temp_rooted_extraction_path = pathlib.Path.joinpath(temp_extraction_path, unzip_root)
        for path, directories, files in os.walk(temp_rooted_extraction_path):
            path_object = pathlib.Path(path)
            for file in files:
                shutil.move(str(pathlib.Path.joinpath(path_object, file)), destination)
            for directory in directories:
                shutil.move(str(pathlib.Path.joinpath(path_object, directory)), destination)
        os.rmdir(temp_rooted_extraction_path)
        os.rmdir(temp_extraction_path)

    if delete_after_unzip:
        os.remove(file_path)
    # TODO(ivan.sainz) Unit tests


if __name__ == "__main__":
    help(__name__)
