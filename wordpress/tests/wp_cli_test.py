"""Unit tests for the wordpress.wp_cli file"""

import pytest
from unittest.mock import patch
import json
import pathlib
from core.LiteralsCore import LiteralsCore
from wordpress.Literals import Literals as WordpressLiterals
import wordpress.wp_cli as sut

literals = LiteralsCore([WordpressLiterals])

# region get_constants()


def test_install_wp_cli_given_path_downloads_files(wordpressdata):
    """Given a file path, downloads WP-CLI files."""

    # Arrange

    # Act
    # TODO(alberto_carbonell) Complete this test
    # sut.install_wp_cli(wordpressdata.wp_cli_install_path)

    # Assert
    assert True

# endregion
