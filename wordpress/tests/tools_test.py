"""Unit tests for the sonarx file"""

import pytest
from unittest.mock import patch
import json
import pathlib
from core.LiteralsCore import LiteralsCore
from wordpress.Literals import Literals as WordpressLiterals
import wordpress.tools as sut

literals = LiteralsCore([WordpressLiterals])

# region get_constants()


def test_get_constants_given_path_returns_data(tmp_path, wordpressdata):
    """Given a file path, returns data in a dict"""

    # Arrange
    constants_file_path = pathlib.Path.joinpath(tmp_path, wordpressdata.constants_file_name)
    with open(constants_file_path, "w") as constants_file:
        constants_file.write(wordpressdata.constants_file_content)

    # Act
    result = sut.get_constants(constants_file_path)

    # Assert
    assert result == json.loads(wordpressdata.constants_file_content)

# endregion
