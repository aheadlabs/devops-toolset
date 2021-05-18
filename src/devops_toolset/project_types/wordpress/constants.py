"""Defines constants for the module."""

required_files_suffixes = {
    "site_configuration_file_path": "site.json"
}

theme_metadata_parse_regex = ": (.+)"
functions_php_mytheme_regex = "(mytheme)(?=_[\w\d\sáéíóú'-.])"

wordpress_constants_json_resource = \
    "https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/" \
    "devops_toolset/project_types/wordpress/wordpress-constants.json"
