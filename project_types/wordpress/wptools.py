"""Contains several tools for WordPress"""
import os

import filesystem.paths as paths
import json
import pathlib
from project_types.wordpress.basic_structure_starter import BasicStructureStarter
import project_types.wordpress.wp_cli as wp_cli
from core.app import App
from core.LiteralsCore import LiteralsCore
from typing import List, Tuple
from project_types.wordpress.Literals import Literals as WordpressLiterals

app: App = App()
literals = LiteralsCore([WordpressLiterals])


def convert_wp_parameter_content(value: bool):
    """Converts a boolean value to a yes/no string."""
    if not value:
        return "yes"
    return "no"


def convert_wp_parameter_debug(value: bool):
    """Converts a boolean value to a --debug string."""
    if value:
        return "--debug"
    return ""


def convert_wp_parameter_skip_content(value: bool):
    """Converts a boolean value to a --skip-content string."""
    if value:
        return "--skip-content"
    return ""


def convert_wp_parameter_yes(value: bool):
    """Converts a boolean value to a --yes string."""
    if value:
        return "--yes"
    return ""


def convert_wp_parameter_skip_check(value: bool):
    """Converts a boolean value to a --skip-check string."""
    if value:
        return "--skip-check"
    return ""


def get_constants(path: str) -> dict:
    """Gets all the constants from a WordPress constants file.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-constants-schema.json

    Args:
        path: Full path to the WordPress constants file.

    Returns:
        All the constants in a dict object.
    """

    with open(path, "r") as constants:
        data = json.loads(constants.read())

    return data


def get_project_structure(path: str) -> dict:
    """Gets the project structure from a WordPress project structure file.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/project-structure-schema.json

    Args:
        path: Full path to the WordPress project structure file.

    Returns:
        Project structure in a dict object.
    """
    with open(path, "r") as project_structure_file:
        data = project_structure_file.read()
        return json.loads(data)


def get_required_file_paths(path: str, required_file_patterns: List[str]) -> Tuple:
    """Returns file paths in a tuple from the file name patterns.

    Args:
        path: Where to look for the files.
        required_file_patterns: glob patterns of the file names to be found.

    Returns:
        Tuple with the file paths in the following order:
        - site configuration JSON file
        - site environments JSON file
        - project structure JSON file
    """

    # required_file_patterns = wordpress.constants.required_files_suffixes
    #
    # for required_file_pattern in required_file_patterns:
    #     if required_file_pattern.endswith()

    result = []
    for required_file_pattern in required_file_patterns:
        result.append(paths.get_file_path_from_pattern(path, required_file_pattern))

    return tuple(result)


def get_site_configuration(path: str) -> dict:
    """Gets the WordPress site configuration from a site configuration file.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-site-schema.json

    Args:
        path: Full path to the WordPress project structure file.

    Returns:
        Site configuration in a dict object.
    """

    with open(path, "r") as config_file:
        data = config_file.read()
        return json.loads(data)


def get_site_configuration_from_environment(environment_path: str, environment_name: str = None) -> dict:
    """Gets the WordPress site configuration from a environment.

    Args:
        environment_path: Path to the environments file.
        environment_name: Name of the environment.

    Returns:
        A dict with the site's configuration.
    """

    site_configuration_path = get_site_configuration_path_from_environment(environment_path, environment_name)

    return get_site_configuration(site_configuration_path)


def get_site_configuration_path_from_environment(environment_path: str, environment_name: str = None) -> str:
    """Gets the path to the WordPress site configuration from a environment.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-site-schema.json
        http://dev.aheadlabs.com/schemas/json/wordpress-site-environments-schema.json

    Args:
        environment_path: Full path to the WordPress site environment file.
        environment_name: Name of the environment to be got. If no name is
            given, default environment is obtained.

    Returns:
        Site configuration path.
    """

    with open(environment_path, "r") as environment_file:
        json_data = json.loads(environment_file.read())

    matching_environments = list(filter(lambda e: e["name"] == environment_name, json_data["environments"]))

    if len(matching_environments) == 0:
        raise ValueError(literals.get("wp_env_not_found"))

    if len(matching_environments) > 1:
        raise ValueError(literals.get("wp_env_gt1"))

    directory = pathlib.Path(environment_path).parent
    file_path = pathlib.Path.joinpath(directory, matching_environments[0]["configuration_file"])

    return str(file_path)


def get_site_environments(path: str) -> dict:
    """Gets the site environments from a WordPress site environment file.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-site-environments-schema.json

    Args:
        path: Full path to the WordPress project structure file.

    Returns:
        Site environments in a dict object.
    """
    pass


def get_wordpress_path_from_root_path(path) -> str:
    """ Gets the wordpress path based on the constants.json from a desired root path 
    
    Args:
        path: Full path of the project
    """
    # Add constants
    wp_constants = get_constants("wordpress-constants.json")
    # Get wordpress path from the constants
    wordpress_relative_path = wp_constants["paths"]["wordpress"].split('/')[1]
    wordpress_path = os.path.join(path, wordpress_relative_path)
    return wordpress_path


def set_wordpress_config(wordpress_path: str, environment_path: str, environment_name: str, db_user_password: str) -> None:
    """ Sets all configuration parameters in pristine WordPress core files
    Args:
        root-wordpress_path: Wordpress installation path.
        environment-path: Path to the environment JSON file.
        environment-name: Environment name.
        db-user_password: Database user password.

    """
    
    # Parse site configuration
    site_config_path = get_site_configuration_path_from_environment(environment_path, environment_name)
    site_config_data = get_site_configuration(site_config_path)
    # Create wp-config.php file
    wp_cli.create_configuration_file(site_config_data, wordpress_path, db_user_password)
    # Get config properties to set from site configuration
    wp_config_properties = get_site_configuration(site_config_path)["settings"]["wp_config"]
    # Foreach variable to set: execute wp config set
    for prop in wp_config_properties.values():
        wp_cli.set_configuration_value(prop.get("name"), prop.get("value"), prop.get("type"), root_path)


def start_basic_project_structure(root_path: str, project_structure_path: str) -> None:
    """ Creates a basic structure of a wordpress project based on the project-structure.json

    Args:
        root_path: Full path where the structure will be created
        project_structure_path: Full path to the json containing the structure
    """
    # Parse project structure configuration
    project_structure = get_project_structure(project_structure_path)
    project_starter = BasicStructureStarter()
    # Iterate through every item recursively
    for item in project_structure["items"]:
        project_starter.add_item(item, root_path)


if __name__ == "__main__":
    root_path = r"D:\\temp"
    project_structure_path = "default-wordpress-project-structure.json"
    # start_basic_project_structure(root_path, project_structure_path)
    set_wordpress_config(root_path, "default-site-environments.json", "localhost", "root")
    help(__name__)
