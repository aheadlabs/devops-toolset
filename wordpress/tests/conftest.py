"""Test configuration file for wordpress module.

Add here whatever you want to pass as a fixture in your texts."""

import pytest


class WordPressData(object):
    """Class used to create the wordpressdata fixture"""
    wordpress_path = "/pathto/wordpress"
    environment_path = "/pathto/environment"
    environment_name = "environment1"
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


@pytest.fixture
def wordpressdata():
    """Sample data for testing"""
    return WordPressData()
