"""Constants for the devops module"""


class Urls(object):
    """URL constants"""
    GITHUB_RAW_CONTENT = "https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/"
    DEVOPS_TOOLSET_MASTER = GITHUB_RAW_CONTENT + "wordpress/default-project.xml"
    SONAR_QUALITY_GATE_PARTIAL_URL = "/api/qualitygates/project_status?projectKey="
    DEFAULT_PROJECT_XML = GITHUB_RAW_CONTENT + "wordpress/default-project.xml"
    DEFAULT_README = GITHUB_RAW_CONTENT + "wordpress/default-README.md"
    DEFAULT_GITIGNORE = GITHUB_RAW_CONTENT + "wordpress/default.gitignore"
    DEFAULT_SITE_CONFIG = GITHUB_RAW_CONTENT + "wordpress/default-localhost-site.json"
    DEFAULT_SITE_ENVIRONMENTS = GITHUB_RAW_CONTENT + "wordpress/default-site-environments.json"
    DEFAULT_WORDPRESS_PROJECT_STRUCTURE = GITHUB_RAW_CONTENT + "wordpress/default-wordpress-project-structure.json"

    bootstrap_required_files = {
        "*site.json": DEFAULT_SITE_CONFIG,
        "*site-environments.json": DEFAULT_SITE_ENVIRONMENTS,
        "*project-structure.json": DEFAULT_WORDPRESS_PROJECT_STRUCTURE
    }
