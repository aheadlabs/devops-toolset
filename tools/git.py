"""Helper functions for Git-related task automation."""

#! python

import pathlib
from filesystem.constants import FileNames, Directions
from filesystem.paths import get_project_root, get_filepath_in_tree

def get_gitignore_path(path: str = None, direction: Directions = Directions.ASCENDING) -> str:
    """Gets the path to the .gitignore file.

    If no path parameter is passed to the function it returns the path to the
    .gitignore file in the project root.
    If a path is passed it returns the path to the .gitignore file that is
    closer to the given path in the specified direction.

    Args:
        path: Optional path to start looking for a .gitignore file.
        direction: The direction of the seek (ascending by default).

    Returns:
        The path to the closest/root .gitignore file
    """
    if path == None:
        gitignore_path = pathlib.Path.joinpath(get_project_root(), FileNames.GITIGNORE_FILE)
        if not pathlib.Path(gitignore_path).exists():
            raise FileNotFoundError
        return gitignore_path
    else:
        return get_filepath_in_tree(FileNames.GITIGNORE_FILE, direction)


def add_gitignore_exclusion(path: str, exclusion: str):
    """Adds an excusion in a .gitignore file.

    It adds the exclusion at the end of the file.

    Args:
        path: Path to the .gitignore file.
        exclusion: Exclusion to be added (whole line must be passed).
    """

    with open(path,"a") as gitignore:
        gitignore.write(f"\n{exclusion}\n")


def find_gitignore_exclusion(path: str, exclusion: str) -> bool:
    """Finds if an excusion exisits in a .gitignore file.

    It tries to find the exclusion.

    Args:
        path: Path to the .gitignore file.
        exclusion: Exclusion to find (whole line must be passed).

    Returns:
        True if the exclusion is found, False otherwise.
    """

    # Open .gitignore for reading, read the file

    # Find exclusion and return True, otherwise False
    pass


def update_gitignore_exclusion(path: str, regex: str, value: str):
    """Updates an existing excusion in a .gitignore file.

    It updates the exclusion in the .gitignore file replacing the passed value using the RegEx.

    Args:
        path: Path to the .gitignore file.
        regex: RegEx with only 1 capturing group, whose content will be replaced.
        value: String that will replace the RegEx capture group.
    """

    # Check if the RegEx has more than 1 capture group and throw an exception (update docstring then)

    # Open .gitignore for reading/writing, read the file

    # Try to match RegEx and replace capture group it in that case
    pass


if __name__ == "__main__":
    get_gitignore_path()
