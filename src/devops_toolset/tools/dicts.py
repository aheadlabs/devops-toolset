"""Tools for working with dict objects"""

import re


def filter_keys(key_list: dict, regex: str) -> list:
    """Filters keys in a dictionary

    Args:
        key_list: dict object that contains the keys to be filtered.
        regex: Regular expression used to filter the keys.

    Returns:
        list with the filtered keys.
    """

    filtered_keys = filter(lambda x: re.search(regex, x) is not None, key_list)
    return list(filtered_keys)


if __name__ == "__main__":
    help(__name__)
