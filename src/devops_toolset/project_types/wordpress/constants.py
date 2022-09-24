"""Defines constants for the WordPress module."""
from enum import Enum


class DefaultValues(object):
    """Default value constants"""
    WORDPRESS_DEFAULT_LOCALE = "en_US"


class Expressions(object):
    """Expressions constants"""
    WORDPRESS_REGEX_FUNCTIONS_PHP_MYTHEME = "(mytheme)(?=_[\w\d\sáéíóú'-.])"
    WORDPRESS_REGEX_THEME_METADATA_PARSE = ": (.+)"
    WORDPRESS_REGEX_VERSION_LOCAL_PACKAGE = r"\$wp_local_package\s=\s'([a-z]{2}_[A-Z]{2})'"
    WORDPRESS_FILTER_PLUGIN_NAME = "([a-z-]+)(?:\.php)?"


class FileNames(object):
    """File names constants"""

    DEFAULT_CLOUDFRONT_FORWARDED_PROTO_PHP = "default-cloudfront-forwarded-proto.php"
    DEFAULT_FILES_PATH_FROM_PACKAGE_ROOT = "devops_toolset/project_types/wordpress/default-files/"
    DEFAULT_GITIGNORE = "default.gitignore"
    DEFAULT_PROJECT_XML = "default-project.xml"
    DEFAULT_README = "default-README.md"
    DEFAULT_SITE_CONFIG = "default-site.json"
    DEFAULT_SITE_ENVIRONMENTS = "default-site-environments.json"
    DEFAULT_WORDPRESS_DEV_THEME_STRUCTURE = "default-wordpress-development-theme-structure.json"
    DEFAULT_WORDPRESS_PROJECT_STRUCTURE = "default-wordpress-project-structure.json"
    REQUIRED_FILE_SUFFIXES = {
        "site_configuration_file_path": "site.json"
    }
    WORDPRESS_CONSTANTS_JSON = "wordpress-constants.json"
    WORDPRESS_CONTENT = "wp-content/"
    WORDPRESS_DEVELOPMENT_THEME_STRUCTURE_FILE = "{theme_slug}-wordpress-theme-structure.json"
    WORDPRESS_LANGUAGES = "wp-content/languages/"
    WORDPRESS_VERSION = "wp-includes/version.php"
    WORDPRESS_ZIP_FILE_NAME_FORMAT = "wordpress*.zip"
    WORDPRESS_ZIP_FILE_NAME_REGEX = r"^wordpress-([0-9]\.[0-9]\.[0-9]).*\.zip$"


class ProjectStructureType(Enum):
    """Types of projects based on its file structure."""
    WORDPRESS = 1
    THEME = 2


class ProjectEnvironmentType(Enum):
    """Types of environments."""
    DEVELOPMENT = 1
    DEVOPS = 2
    INTEGRATION = 3
    QA = 4
    STAGING = 5
    PRODUCTION = 6


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
        FileNames.DEFAULT_WORDPRESS_DEV_THEME_STRUCTURE
    DEFAULT_WORDPRESS_PROJECT_STRUCTURE = \
        GITHUB_RAW_CONTENT + FileNames.DEFAULT_FILES_PATH_FROM_PACKAGE_ROOT + \
        FileNames.DEFAULT_WORDPRESS_PROJECT_STRUCTURE

    BOOTSTRAP_REQUIRED_FILES = {
        "*site.json": DEFAULT_SITE_CONFIG,
        "*site-environments.json": DEFAULT_SITE_ENVIRONMENTS,
        "*project-structure.json": DEFAULT_WORDPRESS_PROJECT_STRUCTURE
    }
