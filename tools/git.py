"""Helper functions for Git-related task automation."""

#! python

import core.app
import os
import pathlib
import re
import filesystem.paths
import logging
from core.LiteralsCore import LiteralsCore
from tools.Literals import Literals as ToolsLiterals
from filesystem.constants import FileNames, Directions

app: core.app.App = core.app.App()
literals = LiteralsCore([ToolsLiterals])
platform_specific = app.load_platform_specific("environment")


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
        gitignore_path = pathlib.Path.joinpath(
            pathlib.Path(filesystem.paths.get_project_root()), FileNames.GITIGNORE_FILE)
        if not pathlib.Path(gitignore_path).exists():
            raise FileNotFoundError
        return gitignore_path
    else:
        return str(filesystem.paths.get_filepath_in_tree(FileNames.GITIGNORE_FILE, direction))


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

    compiled_regex = re.compile(regex)

    if compiled_regex.groups != 1:
        raise ValueError(literals.get("git_regex1cg"))

    with open(path, "r+") as _gitignore:
        content = _gitignore.read()

    from_index = 0
    iterations = len(compiled_regex.findall(content))
    while iterations > 0:
        match = compiled_regex.search(content, from_index)
        content = content[:match.regs[1][0]] + value + content[match.regs[1][1]:]
        from_index = match.regs[1][1]
        iterations -= 1

    with open(path, "w") as _gitignore:
        _gitignore.write(content)


def simplify_branch_name(branch: str):
    """Simplifies a branch name.

    e.g:
        refs/heads/master => master
        refs/heads/feature/name => feature/name
        refs/pull/1/merge => pull/1

    If none of these cases the original branch name is returned.

    Args:
        branch: Long name of the branch to be simplified
    """

    if branch.startswith("refs/heads/"):
        return branch.replace("refs/heads/", "")
    elif branch.startswith("refs/pull/"):
        return branch.replace("refs/", "").replace("/merge", "")
    else:
        return branch


def set_current_branch_simplified(branch: str, environment_variable_name: str):
    """Creates an environment variable from a branch name (simplified)

    Args:
        branch: Git branch name to be simplified and stored in an environment
            variable
        environment_variable_name: name of the environment variable to be
            created
    """

    simplified_branch_name = simplify_branch_name(branch)
    platform_specific.create_environment_variables({environment_variable_name: simplified_branch_name})


def purge_gitkeep(path: str = None):
    """Deletes .gitkeep file if exists and there are more files in the path."""

    if not filesystem.paths.is_valid_path(path):
        raise ValueError(literals.get("git_non_valid_dir_path"))

    path_object = pathlib.Path(path)
    guess_gitkeep_file = pathlib.Path.joinpath(path_object, ".gitkeep")
    if len(os.listdir(path)) > 1 and guess_gitkeep_file.exists():
        logging.info(literals.get("git_purging_gitkeep").format(path=path))
        os.remove(guess_gitkeep_file)


if __name__ == "__main__":
    help(__name__)
