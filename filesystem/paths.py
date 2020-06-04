"""Gets different paths needed in the execution of the different scripts in the project."""

#! python

import pathlib
import xml.etree.ElementTree as ElementTree
from typing import List
from core.app import App
from filesystem.constants import FileNames, Directions

app: App = App()
platform_specific = app.load_platform_specific("environment")


def get_filepath_in_tree(file: str, direction: Directions = Directions.ASCENDING) -> pathlib.PurePath:
    """Gets path to the directory containing the file.

    Args:
        file: File name (not path to file) that should be found.
        direction: The direction of the seek (ascending by default).

    Returns:
        Path to the directory or None if path not found.
    """

    current_path = pathlib.Path(__file__)
    path_to_file = None

    if direction == Directions.ASCENDING:
        for i in range(len(current_path.parents)):
            guess_path = pathlib.Path.joinpath(current_path.parents[i], file)
            if pathlib.Path(guess_path).exists():
                path_to_file = pathlib.Path(guess_path).parent
                break
    else:
        for guess_path in current_path.parent.rglob(file):
            if pathlib.Path(guess_path).exists():
                path_to_file = pathlib.Path(guess_path).parent
                break
            else:
                path_to_file = None

    return path_to_file


def get_file_paths_in_tree(starting_path: str, glob: str) -> List[pathlib.Path]:
    """Gets a list with the paths to the descendant files that match the glob pattern.

    Args:
        starting_path: Path to start the seek from.
        glob: glob pattern to match the files that should be found.

    Returns:
        List with the paths to the files that match.
    """

    paths = []

    for guess_path in pathlib.Path(starting_path).rglob(glob):
        paths.append(guess_path)

    return paths


def get_project_root() -> str:
    """Gets the project root directory path.

    Returns:
        Path to the project root directory or None if path not found."""

    return get_filepath_in_tree(FileNames.PROJECT_FILE)


def get_project_xml_data(add_environment_variables: bool = True) -> dict:
    """Reads the /project.xml file and returns a dict with its data.

    XML elements are uppercased, underscored and prepended with parent name.

    Args:
        add_environment_variables: If True it adds every element of the dict as
            an environment variable.
    """

    project_xml_path = pathlib.Path.joinpath(app.settings.root_path, "project.xml")
    xml = ElementTree.parse(str(project_xml_path)).getroot()

    environment_variables = {}
    for e in xml:
        environment_variables[f"{xml.tag}_{e.tag}".upper()] = e.text

    if add_environment_variables:
        platform_specific.create_environment_variables(environment_variables)

    return environment_variables


def is_valid_path(path: str = None) -> bool:
    """Checks if it is a valid path.

    Args:
        path: Path string to be analyzed

    Returns:
        True if path is valid an exists.
    """

    if path is None or path.strip() == "":
        return False

    path_object = pathlib.Path(path)
    # Exception for unit tests
    if not path.startswith("/pathto") \
            and not pathlib.Path.exists(path_object):
        return False

    return True


if __name__ == "__main__":
    help(__name__)
    get_project_xml_data()
