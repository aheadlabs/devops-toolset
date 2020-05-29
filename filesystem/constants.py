"""Defines constants for the module."""

from enum import Enum

class FileNames(object):
    """Defines constants for file names.

    Attributes:
        GITIGNORE_FILE: .gitignore file.
        PROJECT_FILE: Project definition file.
    """

    GITIGNORE_FILE = ".gitignore"
    PROJECT_FILE = "project.xml"

class Directions(Enum):
    """Defines sorting and finding directions"""

    ASCENDING = 1,
    DESCENDING = 2
