"""Defines constants for the module."""

required_files_suffixes = {
    "site_configuration_file_path": "site.json"
}

theme_metadata_parse_regex = ": (.+)"
functions_php_mytheme_regex = "(mytheme)(?=_[\w\d\sáéíóú'-.])"

github_raw_path = "https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/src/devops_toolset/"
default_cloudfront_forwarded_proto_php = \
    f"{github_raw_path}project_types/wordpress/default-files/default-cloudfront-forwarded-proto.php"
wordpress_constants_json_resource = f"{github_raw_path}project_types/wordpress/wordpress-constants.json"
