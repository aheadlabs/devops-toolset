"""Unit tests for the tools file"""

import pathlib
from unittest.mock import patch
import i18n.tools as sut
from filesystem.constants import Directions, FileNames

# region compile_po_files()


def test_compile_po_files_given_path_then_calls_get_filepaths_in_tree(filenames):
    """Given a locale path, it should call get_file_paths_in_tree() to get the
    paths"""

    # Arrange
    with patch.object(sut, "get_file_paths_in_tree") as file_paths:
        file_paths.return_value = filenames.paths

    # Act
        sut.compile_po_files(filenames.path)

    # Assert
    file_paths.assert_called()

# endregion
