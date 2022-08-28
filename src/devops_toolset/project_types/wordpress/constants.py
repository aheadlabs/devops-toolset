"""Defines constants for the WordPress module."""

# TODO Move these classless constants
required_files_suffixes = {
    "site_configuration_file_path": "site.json"
}

theme_metadata_parse_regex = ": (.+)"
functions_php_mytheme_regex = "(mytheme)(?=_[\w\d\sáéíóú'-.])"

github_raw_path = "https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/src/devops_toolset/"


class FileNames(object):
    """File names constants"""

    DEFAULT_CLOUDFRONT_FORWARDED_PROTO_PHP = "default-cloudfront-forwarded-proto.php"
    DEFAULT_FILES_PATH_FROM_PACKAGE_ROOT = "devops_toolset/project_types/wordpress/default-files/"
    DEFAULT_GITIGNORE = "default.gitignore"
    DEFAULT_PROJECT_XML = "default-project.xml"
    DEFAULT_README = "default-README.md"
    DEFAULT_SITE_CONFIG = "default-localhost-site.json"
    DEFAULT_SITE_ENVIRONMENTS = "default-site-environments.json"
    DEFAULT_WORDPRESS_DEVELOPMENT_THEME_STRUCTURE = "default-wordpress-development-theme-structure.json"
    DEFAULT_WORDPRESS_PROJECT_STRUCTURE = "default-wordpress-project-structure.json"
    WORDPRESS_CONSTANTS_JSON = "wordpress-constants.json"
    WORDPRESS_ZIP_FILE_NAME_FORMAT = "wordpress*.zip"
    WORDPRESS_ZIP_FILE_NAME_REGEX = r"^wordpress-([0-9]\.[0-9]\.[0-9])\.zip$"


class Urls(object):
    """URL constants"""

    GITHUB_RAW_CONTENT = "https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/src/"

    DEFAULT_GITIGNORE = \
        GITHUB_RAW_CONTENT + FileNames.DEFAULT_FILES_PATH_FROM_PACKAGE_ROOT + FileNames.DEFAULT_GITIGNORE
    DEFAULT_PROJECT_XML = \
        GITHUB_RAW_CONTENT + FileNames.DEFAULT_FILES_PATH_FROM_PACKAGE_ROOT + FileNames.DEFAULT_PROJECT_XML
    DEFAULT_README = GITHUB_RAW_CONTENT + FileNames.DEFAULT_FILES_PATH_FROM_PACKAGE_ROOT + FileNames.DEFAULT_README
    DEFAULT_SITE_CONFIG = \
        GITHUB_RAW_CONTENT + FileNames.DEFAULT_FILES_PATH_FROM_PACKAGE_ROOT + FileNames.DEFAULT_SITE_CONFIG
    DEFAULT_SITE_ENVIRONMENTS = \
        GITHUB_RAW_CONTENT + FileNames.DEFAULT_FILES_PATH_FROM_PACKAGE_ROOT + FileNames.DEFAULT_SITE_ENVIRONMENTS
    DEFAULT_WORDPRESS_DEVELOPMENT_THEME_STRUCTURE = \
        GITHUB_RAW_CONTENT + FileNames.DEFAULT_FILES_PATH_FROM_PACKAGE_ROOT + \
        FileNames.DEFAULT_WORDPRESS_DEVELOPMENT_THEME_STRUCTURE
    DEFAULT_WORDPRESS_PROJECT_STRUCTURE = \
        GITHUB_RAW_CONTENT + FileNames.DEFAULT_FILES_PATH_FROM_PACKAGE_ROOT + \
        FileNames.DEFAULT_WORDPRESS_PROJECT_STRUCTURE

    BOOTSTRAP_REQUIRED_FILES = {
        "*site.json": DEFAULT_SITE_CONFIG,
        "*site-environments.json": DEFAULT_SITE_ENVIRONMENTS,
        "*project-structure.json": DEFAULT_WORDPRESS_PROJECT_STRUCTURE
    }
