"""Contains several tools for WordPress"""

from core.app import App
import logging

app: App = App()


def get_constants(path: str) -> dict:
    """Gets all the constants from a WordPress constants file.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-constants-schema.json

    Args:
        path: Full path to the WordPress constants file.
    """
    pass


def get_project_structure(path: str) -> dict:
    """Gets the project structure from a WordPress project structure file.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/project-structure-schema.json

    Args:
        path: Full path to the WordPress project structure file.
    """
    pass


def get_site_environments(path: str) -> dict:
    """Gets the project structure from a WordPress site environment file.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-site-environments-schema.json

    Args:
        path: Full path to the WordPress project structure file.
    """
    pass


def get_site_configuration(path: str) -> dict:
    """Gets the WordPress site configuration from a site configuration file.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-site-schema.json

    Args:
        path: Full path to the WordPress project structure file.
    """
    pass


def get_site_configuration_path_from_environment(environment_path: str, environment_name: str) -> str:
    """Gets the path to the WordPress site configuration from a environment.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-site-schema.json
        http://dev.aheadlabs.com/schemas/json/wordpress-site-environments-schema.json

    Args:
        environment_path: Full path to the WordPress site environment file.
        environment_name: Name of the environment to be got.
    """
    pass


def create_project_structure(project_structure: dict) -> bool:
    """Creates the project structure from a site configuration file.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-site-schema.json

    Args:
        project_structure: Parsed WordPress project structure file.
    """
    pass


if __name__ == "__main__":
    help(__name__)
