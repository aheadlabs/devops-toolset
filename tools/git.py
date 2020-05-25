"""Helper functions for Git-related task automation."""

#! python

import core.app
import pathlib
import re
from filesystem.constants import FileNames, Directions
from filesystem.paths import get_project_root, get_filepath_in_tree

app: core.app.App = core.app.App()

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
    if path is None:
        gitignore_path = pathlib.Path.joinpath(get_project_root(), FileNames.GITIGNORE_FILE)
        if not pathlib.Path(gitignore_path).exists():
            raise FileNotFoundError
        return gitignore_path
    else:
        return get_filepath_in_tree(FileNames.GITIGNORE_FILE, direction)


def add_gitignore_exclusion(path: str, exclusion: str):
    """Adds an exclusion in a .gitignore file.

    It adds the exclusion at the end of the file.

    Args:
        path: Path to the .gitignore file.
        exclusion: Exclusion to be added (whole line must be passed).
    """

    with open(path,"a") as _gitignore:
        _gitignore.write(f"\n{exclusion}\n")


def find_gitignore_exclusion(path: str, exclusion: str) -> bool:
    """Finds if an excusion exisits in a .gitignore file.

    It tries to find the exclusion.

    Args:
        path: Path to the .gitignore file.
        exclusion: Exclusion to find (whole line must be passed not including
            newline).

    Returns:
        True if the exclusion is found, False otherwise.
    """

    with open(path, "r") as _gitignore:
        index = _gitignore.read().find(f"{exclusion}\n")

    return index > -1


def update_gitignore_exclusion(path: str, regex: str, value: str):
    """Updates an existing excusion in a .gitignore file.

    It updates the exclusion in the .gitignore file replacing the passed value using the RegEx.

    Args:
        path: Path to the .gitignore file.
        regex: RegEx with only 1 capturing group, whose content will be replaced.
        value: String that will replace the RegEx capture group.
    Raises:
        ValueError: When regex has no capture groups or more than one
    """

    cregex = re.compile(regex)

    if cregex.groups != 1:
        raise ValueError(_("RegEx must have 1 capture group. No less, no more."))

    with open(path, "r+") as _gitignore:
        content = _gitignore.read()

    from_index = 0
    iterations = len(cregex.findall(content))
    while iterations > 0:
        match = cregex.search(content, from_index)
        content = content[:match.regs[1][0]] + value + content[match.regs[1][1]:]
        from_index = match.regs[1][1]
        iterations -= 1

    with open(path, "w") as _gitignore:
        _gitignore.write(content)


if __name__ == "__main__":
    get_gitignore_path()
