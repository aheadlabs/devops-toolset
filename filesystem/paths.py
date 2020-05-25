"""Gets different paths needed in the execution of the different scripts in the project."""

#! python

import pathlib
from typing import List
from filesystem.constants import FileNames, Directions


def get_filepath_in_tree(file: str, direction: Directions = Directions.ASCENDING) -> str:
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


if __name__ == "__main__":
    print(f"Project root is {get_project_root()}")
