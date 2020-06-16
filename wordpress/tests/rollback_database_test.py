"""Unit tests for the rollback_database file"""

from unittest.mock import patch
import wordpress.rollback_database as sut


@patch("wordpress.wp_cli.import_database")
@patch("wordpress.wp_cli.reset_database")
@patch("wordpress.wptools.get_site_configuration_from_environment")
def test_main(get_site_configuration_from_environment, reset_database, import_database):
    """Given arguments, then calls all needed WP CLI commands."""

    # Arrange
    environment_path = ""
    environment_name = ""
    wordpress_path = ""
    database_dump_path = ""
    quiet = True

    # Act
    sut.main(environment_path, environment_name, wordpress_path, database_dump_path, quiet)

    # Assert
    reset_database.assert_called()
    import_database.assert_called()
