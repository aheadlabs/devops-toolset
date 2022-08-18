""" Script used on devops flows to parse a theme's style.css metadata """

import argparse
import devops_toolset.filesystem.parsers as parsers


def main(path: str, tokens):
    """ Loads the css file in path and parses theme metadata, creating environment variables
    Args:
        path: Path to style.css file inside the target theme
        tokens: List of tokens to be retrieved from metadata file
    """
    with open(path, "rb") as css_file_content:
        parsers.parse_theme_metadata(css_file_content.read(), tokens, True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", action=tools.argument_validators.PathValidator)
    args, args_unknown = parser.parse_known_args()
    # First parameter should be the path, all next parameters will be the tokens to retrieve
    main(args.path, args_unknown)
