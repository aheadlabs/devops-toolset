"""Defines constants for the module."""

required_files_suffixes = {
    "site_configuration_file_path": "site.json",
    "site_environments_file_path": "site-environments.json"
}

theme_metadata_parse_regex = ":\s([\w\d\sáéíóú'-.]+)\r\n"

wordpress_constants_json_resource = \
    "https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/project_types/wordpress/wordpress-constants.json"
