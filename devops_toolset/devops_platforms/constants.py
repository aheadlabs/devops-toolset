"""Constants for the devops_platforms module"""


class Urls(object):
    """URL constants"""
    GITHUB_RAW_CONTENT = "https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/"
    DEVOPS_TOOLSET_MASTER = GITHUB_RAW_CONTENT + \
                            "devops_toolset/project_types/wordpress/default-files/default-project.xml"
    SONAR_QUALITY_GATE_PARTIAL_URL = "/api/qualitygates/project_status?projectKey="
    DEFAULT_PROJECT_XML = GITHUB_RAW_CONTENT + \
                          "devops_toolset/project_types/wordpress/default-files/default-project.xml"
    DEFAULT_README = GITHUB_RAW_CONTENT + "devops_toolset/project_types/wordpress/default-files/default-README.md"
    DEFAULT_GITIGNORE = GITHUB_RAW_CONTENT + "devops_toolset/project_types/wordpress/default-files/default.gitignore"
    DEFAULT_SITE_CONFIG = GITHUB_RAW_CONTENT + \
                          "devops_toolset/project_types/wordpress/default-files/default-localhost-site.json"
    DEFAULT_SITE_ENVIRONMENTS = GITHUB_RAW_CONTENT + \
                                "devops_toolset/project_types/wordpress/default-files/default-site-environments.json"
    DEFAULT_WORDPRESS_PROJECT_STRUCTURE = \
        GITHUB_RAW_CONTENT + \
        "devops_toolset/project_types/wordpress/default-files/default-wordpress-project-structure.json"
    DEFAULT_WORDPRESS_DEVELOPMENT_THEME_STRUCTURE = \
        GITHUB_RAW_CONTENT + \
        "devops_toolset/project_types/wordpress/default-files/default-wordpress-development-theme-structure.json"

    bootstrap_required_files = {
        "*site.json": DEFAULT_SITE_CONFIG,
        "*site-environments.json": DEFAULT_SITE_ENVIRONMENTS,
        "*project-structure.json": DEFAULT_WORDPRESS_PROJECT_STRUCTURE
    }
