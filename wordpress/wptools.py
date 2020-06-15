"""Contains several tools for WordPress"""

import filesystem.paths as paths
import json
import pathlib
import wordpress.constants
from wordpress.BasicStructureStarter import BasicStructureStarter
from core.app import App
from core.LiteralsCore import LiteralsCore
from typing import List, Tuple
from wordpress.Literals import Literals as WordpressLiterals

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
    start_basic_project_structure("D:/temp", "default-wordpress-project-structure.json")
    help(__name__)
