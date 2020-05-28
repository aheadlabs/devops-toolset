"""Base class for Literals"""

import inspect
from typing import List


class LiteralsBase(object):
    """Base class for Literals"""

    def __init__(self, literals_list: List = None):
        """Plains all literals from all the dictionaries passed as a parameter
        plus the ones defined in the instanced class.

        Args:
            literals_list: List of class types where literals should be found.
        """

        self._all_dictionaries = self.get_dicts()

        if literals_list:
            for literals in literals_list:
                _external = literals()
                self._all_dictionaries += _external.get_dicts()

        self.all = {}
        for dictionary in self._all_dictionaries:
            self.all.update(dictionary[1])

    def get(self, key: str) -> str:
        """Gets a literal from a given key.

        Args:
            key: used for getting the message
        """

        return str(self.all[key])

    def get_dicts(self):
        """Gets all dict objects of the class."""

        return inspect.getmembers(self, lambda m: type(m) is dict and len(m) > 0)
