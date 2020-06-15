"""Test configuration file for wordpress module.

Add here whatever you want to pass as a fixture in your texts."""
import pathlib

import pytest
import requests

from unittest import mock


class WordPressData:
    """Class used to create the wordpressdata fixture"""
    wordpress_path = "/pathto/wordpress"
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
    site_config_content = "{\"$schema\":\"http://dev.aheadlabs.com/schemas/json/wordpress-site-schema.json\"," \
                          "\"wp_cli\":{\"debug\":false},\"database\":{\"host\":\"localhost\",\"name\":" \
                          "\"my_wordpress_site\",\"user\":\"wp_db_user\",\"prefix\":\"wp_\",\"charset\":\"utf8\"," \
                          "\"collate\":\"utf8_unicode_ci\",\"skip_check\":true,\"dumps\":{\"core\":" \
                          "\"[date]-db.core.sql\",\"theme\":\"[date]-db.theme.sql\",\"plugins\":" \
                          "\"[date]-db.plugins.sql\",\"regular\":\"[date]-db.sql\"}},\"settings\":{\"title\":" \
                          "\"My WordPress site\",\"description\":\"This is my WordPress site\",\"version\":" \
                          "\"latest\",\"locale\":\"en_US\",\"site_url\":\"http://localhost/my-wordpress-site\"," \
                          "\"admin\":{\"user\":\"wp_admin\",\"email\":\"you@example.com\",\"skip_email\":true}," \
                          "\"skip_content_download\":false,\"content_url\":" \
                          "\"http://localhost/my-wordpress-site/wp-content\",\"plugin_url\":" \
                          "\"http://localhost/my-wordpress-site/wp-content/plugins\",\"noblogredirect_url\":" \
                          "\"http://localhost/my-wordpress-site\",\"disable_fatal_error_handler_and_debug_display\":" \
                          "false,\"concatenate_scripts\":true,\"cache\":false,\"save_queries\":false," \
                          "\"empty_trash_days\":5,\"disallow_file_edit\":false,\"disallow_file_mods\":false," \
                          "\"force_ssl_admin\":false,\"http_block_external\":true,\"accessible_hosts\":" \
                          "[\"localhost\"],\"auto_update_core\":\"minor\",\"image_edit_overwrite\":true}," \
                          "\"multisite\":{},\"themes\":{\"source_type\":\"wordpress\",\"source\":\"twentytwenty\"," \
                          "\"has_child\":false},\"plugins\":{}}"
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

    # Mocks
    requests_get_mock = mock.patch.object(requests, "get").start()


@pytest.fixture
def wordpressdata():
    """Sample data for testing"""
    yield WordPressData()
    # Below code is executed as a TearDown
    WordPressData.requests_get_mock.stop()
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
