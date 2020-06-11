""" Creates an opinionated basic structure for a WordPress project. """

import argparse
import wordpress.wptools as wp_tools
import pathlib
import filesystem.paths as path_tools
import os
import requests


def main(root_path, project_structure_path):
    """ Parses the project structure json and creates the whole structure of the wordpress project """
    # Parse project structure configuration
    project_structure = wp_tools.get_project_structure(project_structure_path)
    # Iterate through every item recursively
    for item in project_structure["items"]:
        add_item(item, root_path)


def condition_met(item, base_path):
    """ Returns the result (True of False) of the condition contained on the item

    Args:
        item: the item inspected for conditions
        base_path: parent dir to check
    """
    if "condition" in item and item["condition"] == "when-parent-not-empty":
        return path_tools.is_empty_dir(base_path)
    # Default behaviour
    return True


def add_item(item, base_path_str):
    """ Creates the item (file or dir) in the current filesystem

     Args:
            item: the object containing the type and the value of the content.
            base_path_str: the path which from the structure will be built

    """
    # Set paths
    base_path = pathlib.Path(base_path_str)
    final_path = pathlib.Path.joinpath(base_path, item["name"])
    has_children = "children" in item
    child_condition = has_children and condition_met(item["children"][0], base_path_str)
    # Only if the item DOES NOT exist and child condition is met
    if not path_tools.is_valid_path(str(final_path)) and child_condition:
        # Create item
        if item["type"] == "directory":
            os.mkdir(final_path)
        elif item["type"] == "file":
            with open(final_path, "a") as new_file:
                # Add default content if applies
                if "default_content" in item:
                    new_file.write(get_default_content(item["default_content"]))

    # Iterate through children if any
    if has_children:
        for child in item["children"]:
            add_item(child, final_path)


def get_default_content(item):
    """ Parses the default content of the files based on the json item passed

        Args:
            item : the object containing the type and the value of the default content
    """
    if item["source"] == "raw":
        return item["value"]
    elif item["source"] == "from_file":
        with open(item["value"], "r") as default_content_file:
            return default_content_file.read()
    elif item["source"] == "from_url":
        response = requests.get(item["value"])

        return response.text


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--root-path", required=True)
    argparser.add_argument("--project-structure-path", required=True)
    args, args_unknown = argparser.parse_known_args()
    main(args.root_path, args.project_structure_path)
