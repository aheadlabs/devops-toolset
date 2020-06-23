""" Creates an opinionated basic structure for a WordPress project. """

import pathlib
import filesystem.paths as path_tools
import os
import requests


class BasicStructureStarter(object):
    """ Set of methods used to create a basic structure for a Wordpress project """

    def add_item(self, item, base_path_str: str) -> None:
        """ Creates the item (file or dir) in the current filesystem

         Args:
                item: the object containing the type and the value of the content.
                base_path_str: the path which from the structure will be built

        """

        # Set paths
        base_path = pathlib.Path(base_path_str)
        final_path = pathlib.Path.joinpath(base_path, item["name"])
        has_condition = "condition" in item
        if has_condition:
            child_condition = self.condition_met(item, base_path_str)
        else:
            child_condition = True
        # Only if the item DOES NOT exist and condition is met
        if not path_tools.is_valid_path(str(final_path)) and child_condition and "type" in item:
            # Create item
            if item["type"] == "directory":
                os.mkdir(final_path)
            elif item["type"] == "file":
                with open(final_path, "a") as new_file:
                    # Add default content if applies
                    if "default_content" in item:
                        new_file.write(self.get_default_content(item["default_content"]))

        # Iterate through children if any
        if "children" in item:
            for child in item["children"]:
                self.add_item(child, final_path)

    @staticmethod
    def condition_met(item, base_path: str) -> bool:
        """ Returns the result (True of False) of the condition contained on the item

        Args:
            item: the item inspected for conditions
            base_path: parent dir to check
        """

        if "condition" in item and item["condition"] == "when-parent-not-empty":
            return not path_tools.is_empty_dir(str(pathlib.Path(base_path).parent))
        # Default behaviour
        return True

    @staticmethod
    def get_default_content(item) -> str:
        """ Gets the default content of the files based on the json item passed

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
