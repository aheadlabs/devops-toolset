"""Test configuration file for wordpress module.

Add here whatever you want to pass as a fixture in your texts."""
import pathlib

import pytest
import requests

from unittest import mock


class WordPressData:
    """Class used to create the wordpressdata fixture"""
    root_path = "pathto/project"
    wordpress_path = "/pathto/wordpress"
    theme_path = "/pathto/theme"
    wordpress_path_part = "/wordpress"
    wordpress_path_err = "/nonexistentpath"
    environment_path = "/pathto/environment"
    project_structure_path = "/pathto/structure"
    environment_name = "localhost"
    environment_name_fake = "notfoundhost"
    environment_file_content = \
        "{\"$schema\":\"http://dev.aheadlabs.com/schemas/json/wordpress-site-environments-schema.json\"," \
        "\"environments\":[{\"name\":\"localhost\",\"type\":\"development\",\"default\":true,\"configuration_file\":" \
        "\"default-localhost-site.json\"}]}"
    environment_file_content_duplicated_environment = \
        "{\"$schema\":\"http://dev.aheadlabs.com/schemas/json/wordpress-site-environments-schema.json\"," \
        "\"environments\":[{\"name\":\"localhost\",\"type\":\"development\",\"default\":true,\"configuration_file\":" \
        "\"default-localhost-site.json\"},{\"name\":\"localhost\",\"type\":\"development\",\"default\":true," \
        "\"configuration_file\":\"default-localhost-site.json\"}]}"
    site_config_path_from_json = "/pathto/default-localhost-site.json"
    site_config_path = "/pathto/site-config"
    site_config_file_name = "default-localhost-site.json"
    site_config_content = "{\"wp_cli\":{\"debug\":false},\"database\":{\"host\":\"localhost\"," \
                          "\"name\":\"wordpress-playground\",\"user\":\"wp_playground_db_user\",\"prefix\":\"wp_\"," \
                          "\"charset\":\"utf8\",\"collate\":\"utf8_unicode_ci\",\"skip_check\":true," \
                          "\"dumps\":{\"core\":\"[date|Y.m.d-Hisve]-db.core.sql\"," \
                          "\"theme\":\"[date|Y.m.d-Hisve]-db.theme.sql\"," \
                          "\"plugins\":\"[date|Y.m.d-Hisve]-db.plugins.sql\"," \
                          "\"regular\":\"[date|Y.m.d-Hisve]-db-[commit].sql\"}}," \
                          "\"settings\":{\"title\":\"Wordpress Playground\"," \
                          "\"description\":\"This site\",\"version\":\"latest\",\"locale\":\"en_US\"," \
                          "\"admin\":{\"user\":\"wp_admin\",\"email\":\"you@example.com\",\"skip_email\":true}," \
                          "\"wp_config\":{\"site_url\":{\"name\":\"WP_SITEURL\",\"type\":\"constant\"," \
                          "\"value\":\"http://localhost/wordpress-playground\"},\"home_url\":{\"name\":\"WP_HOME\"," \
                          "\"type\":\"constant\",\"value\":\"http://localhost/wordpress-playground\"}," \
                          "\"content_url\":{\"name\":\"WP_CONTENT_URL\",\"type\":\"constant\"," \
                          "\"value\":\"http://localhost/wordpress-playground/wp-content\"}," \
                          "\"plugin_url\":{\"name\":\"WP_PLUGIN_URL\",\"type\":\"constant\"," \
                          "\"value\":\"http://localhost/wordpress-playground/wp-content/plugins\"}," \
                          "\"noblogredirect_url\":{\"name\":\"NOBLOGREDIRECT\",\"type\":\"constant\"," \
                          "\"value\":\"http://localhost/wordpress-playground\"}," \
                          "\"disable_fatal_error_handler\":{\"name\":\"WP_DISABLE_FATAL_ERROR_HANDLER\"," \
                          "\"type\":\"constant\",\"value\":false},\"debug_display\":{\"name\":\"WP_DEBUG_DISPLAY\"," \
                          "\"type\":\"constant\",\"value\":false},\"debug\":{\"name\":\"WP_DEBUG\"," \
                          "\"type\":\"constant\",\"value\":false},\"cache\":{\"name\":\"WP_CACHE\"," \
                          "\"type\":\"constant\",\"value\":false},\"save_queries\":{\"name\":\"SAVEQUERIES\"," \
                          "\"type\":\"constant\",\"value\":false},\"empty_trash_days\":{\"name\":\"EMPTY_TRASH_DAYS\"," \
                          "\"type\":\"constant\",\"value\":5},\"disallow_file_edit\":{\"name\":\"DISALLOW_FILE_EDIT\"," \
                          "\"type\":\"constant\",\"value\":false},\"disallow_file_mods\":{\"name\":\"DISALLOW_FILE_MODS\"," \
                          "\"type\":\"constant\",\"value\":false},\"force_ssl_admin\":{\"name\":\"FORCE_SSL_ADMIN\"," \
                          "\"type\":\"constant\",\"value\":false},\"http_block_external\":" \
                          "{\"name\":\"WP_HTTP_BLOCK_EXTERNAL\",\"type\":\"constant\",\"value\":true}," \
                          "\"accessible_hosts\":{\"name\":\"WP_ACCESIBLE_HOSTS\",\"type\":\"constant\"," \
                          "\"value\":[\"localhost\"]},\"auto_update_core\":{\"name\":\"WP_AUTO_UPDATE_CORE\"," \
                          "\"type\":\"constant\",\"value\":\"minor\"},\"image_edit_overwrite\":" \
                          "{\"name\":\"IMAGE_EDIT_OVERWRITE\",\"type\":\"constant\",\"value\":true}}," \
                          "\"skip_content_download\":false,\"concatenate_scripts\":true},\"multisite\":{}," \
                          "\"themes\":{},\"plugins\":[]}"
    plugins_content = \
        "[{\"name\":\"plugin-1\",\"source_type\":\"wordpress\",\"source\":\"path-to-source1\",\"force\":true}," \
        "{\"name\":\"plugin-2\",\"source_type\":\"wordpress\",\"source\":\"path-to-source2\",\"force\":true}]"
    themes_content = \
        "[{\"name\":\"theme\",\"source_type\":\"zip\",\"source\":\"path-to-source1.zip\"}]"
    themes_content_with_child = \
        "[{\"name\":\"theme\",\"source_type\":\"zip\",\"source\":\"path-to-source1.zip\"," \
        "\"child\":\"\"}]"
    constants_file_name = "wordpress-constants.json"
    constants_file_content = "{\"$schema\":" \
                             "\"http://dev.aheadlabs.com/schemas/json/wordpress-constants-schema.json\"," \
                             "\"defaults\":{\"version\":\"latest\",\"locale\":\"en_US\"},\"paths\":{\"devops\":" \
                             "\"/.devops\",\"database\":\"/database\",\"wordpress\":\"/wordpress\",\"content\":" \
                             "{\"themes\":\"/content/themes\",\"plugins\":\"/content/plugins\"}},\"packages\":" \
                             "{\"devops_toolset\":" \
                             "\"https://github.com/aheadlabs/devops-toolset/archive/master.zip\"},\"regex_base64\":" \
                             "[{\"key\":\"wordpress-theme\",\"value\":" \
                             "\"d29yZHByZXNzL3dwLWNvbnRlbnQvdGhlbWVzLyhbXHdcLV0rKS8=\"}]}"
    structure_file_content = "{\"$schema\":\"http://dev.aheadlabs.com/schemas/json/project-structure-schema.json\"," \
                             "\"items\":[{\"name\":\".devops\",\"type\":\"directory\",\"children\":[{\"name\":" \
                             "\".gitkeep\",\"type\":\"file\",\"condition\":\"when-parent-not-empty\"}]},{\"name\":" \
                             "\".media\",\"type\":\"directory\",\"children\":[{\"name\":\".gitkeep\",\"type\":" \
                             "\"file\",\"condition\":\"when-parent-not-empty\"}]},{\"name\":\"content\",\"type\":" \
                             "\"directory\",\"children\":[{\"name\":\"themes\",\"type\":\"directory\",\"children\":" \
                             "[{\"name\":\".gitkeep\",\"type\":\"file\",\"condition\":\"when-parent-not-empty\"}]}]}" \
                             ",{\"name\":\"database\",\"type\":\"directory\",\"children\":[{\"name\":\".gitkeep\"," \
                             "\"type\":\"file\",\"condition\":\"when-parent-not-empty\"}]},{\"name\":\"wordpress\"," \
                             "\"type\":\"directory\",\"children\":[{\"name\":\".gitkeep\",\"type\":\"file\"," \
                             "\"condition\":\"when-parent-not-empty\"}]},{\"name\":\".gitignore\",\"type\":\"file\"," \
                             "\"default_content\":{\"source\":\"from_url\",\"value\":" \
                             "\"https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/wordpress/" \
                             "default.gitignore\"}},{\"name\":\"project.xml\",\"type\":\"file\",\"default_content\":" \
                             "{\"source\":\"from_url\",\"value\":" \
                             "\"https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/wordpress/" \
                             "default-project.xml\"}},{\"name\":\"README.md\",\"type\":\"file\",\"default_content\":" \
                             "{\"source\":\"from_url\",\"value\":\"https://raw.githubusercontent.com/aheadlabs/" \
                             "devops-toolset/master/wordpress/default-README.md\"}}]}"
    wp_cli_install_path = "/pathto/wp-cli"
    wp_cli_phar = "wp-cli.phar"
    wp_cli_file_path = pathlib.Path.joinpath(pathlib.Path(wp_cli_install_path), wp_cli_phar)
    builtins_open = 'builtins.open'
    parent_not_empty_value = 'when_parent_not_empty'
    condition_key = 'condition'
    dump_file_path = "/pathto/dump_file_1.sql"
    path = "/pathto"


@pytest.fixture
def wordpressdata():
    """Sample data for testing"""
    yield WordPressData()
    # Below code is executed as a TearDown
    print("Teardown finished.")


def mocked_requests_get(url: str, *args, **kwargs):
    """Mock to replace requests.get()"""

    # Default values
    bytes_content = b"sample response in bytes"
    text_content = "sample text response"

    # Return instance
    return MockResponse(bytes_content, text_content)


class MockResponse:
    """This is the mocked Response object returned by requests.get()"""
    def __init__(self, b_content, text_content):
        self.content = b_content
        self.text = text_content
