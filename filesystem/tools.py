"""Tools for editing files"""

import xml.etree.ElementTree as ElementTree

from core.app import App
from core.LiteralsCore import LiteralsCore
from filesystem.Literals import Literals as FileSystemLiterals
from project_types.wordpress.Literals import Literals as WordpressLiterals


app: App = App()
platform_specific = app.load_platform_specific("environment")
literals = LiteralsCore([FileSystemLiterals])
wp_literals = LiteralsCore([WordpressLiterals])


def update_xml_file_entity_text(entity_xpath: str, entity_value: str, xml_file_path: str):
    """Updates an XML file with the given value.

    Supported XPath syntax is documented here:
    https://docs.python.org/3/library/xml.etree.elementtree.html#supported-xpath-syntax

    Args:
        entity_xpath: Path to the node or attribute to be updated.
        entity_value: Value to be set.
        xml_file_path: Path to the XML file.
    """

    xml_tree = ElementTree.parse(xml_file_path)
    entity = xml_tree.find(entity_xpath)
    entity.text = entity_value
    xml_tree.write(xml_file_path)


if __name__ == "__main__":
    help(__name__)
