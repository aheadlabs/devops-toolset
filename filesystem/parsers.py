"""Parses files for getting information from them"""

import logging
import pathlib
import xml.etree.ElementTree as ElementTree
from core.app import App
from core.LiteralsCore import LiteralsCore
from filesystem.Literals import Literals as FileSystemLiterals

app: App = App()
platform_specific = app.load_platform_specific("environment")
literals = LiteralsCore([FileSystemLiterals])


def parse_project_xml_data(add_environment_variables: bool = True, project_xml_path: str = None) -> dict:
    """Reads the /project.xml file and returns a dict with its data.

    XML elements are upper cased, underscored and prepended with parent name.

    Args:
        add_environment_variables: If True it adds every element of the dict as
            an environment variable.
        project_xml_path: Path to the project.xml file.
    """

    if project_xml_path is None:
        project_xml_path = pathlib.Path.joinpath(app.settings.root_path, "project.xml")
    else:
        project_xml_path = pathlib.Path(project_xml_path)
    logging.info(literals.get("fs_project_path_is").format(path=project_xml_path))
    xml = ElementTree.parse(str(project_xml_path)).getroot()

    environment_variables = {}
    for e in xml:
        environment_variables[f"{xml.tag}_{e.tag}".upper()] = e.text

    if add_environment_variables:
        platform_specific.create_environment_variables(environment_variables)

    return environment_variables
