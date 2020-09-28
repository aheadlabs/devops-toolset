"""Contains several tools for WordPress"""
import os
import requests
import filesystem.paths as paths
import json
import pathlib
import shutil
import stat
import logging
from project_types.wordpress.constants import wordpress_constants_json_resource
from project_types.wordpress.basic_structure_starter import BasicStructureStarter
import project_types.wordpress.wp_cli as wp_cli
import sys
import tools.git as git_tools
from core.app import App
from core.LiteralsCore import LiteralsCore
from typing import List, Tuple
from project_types.wordpress.Literals import Literals as WordpressLiterals

app: App = App()
literals = LiteralsCore([WordpressLiterals])


def convert_wp_config_token(token: str, wordpress_path: str) -> str:
    """ Replaces [] tokens inside configuration parameters using php syntax

    Args:
        token: The token to replace (for example: [date|Y.m.d-Hisve])
        wordpress_path: Wordpress installation path
    """
    result = token
    # parse token [date|Y.m.d-Hisve]
    if token.find("[date|") != -1:
        date_format = token[token.find("[date|") + 1:token.find("]")]
        date_token = date_format.split("|")[1]
        result = result.replace(
            "[" + date_format + "]", wp_cli.eval_code("echo date('" + date_token + "');", wordpress_path))
    if token.find("[commit]") != -1:
        commit_token = token[token.find("[commit") + 1:token.rfind("]")]
        # TODO (alberto.carbonell): Set latest commit id
        commit_id = "123456"
        result = result.replace("[" + commit_token + "]", commit_id)
    # Add more tokens if needed
    return result


def create_wp_cli_bat_file(phar_path: str):
    """Creates a .bat file for WP-CLI.

    Args:
        phar_path: Path to the .phar file.
    """

    path = pathlib.Path(phar_path)
    bat_path = pathlib.Path.joinpath(path.parent, "wp.bat")

    with open(bat_path, "w") as bat:
        bat.write("@ECHO OFF\n")
        bat.write(f"php \"{phar_path}\" %*")


def create_configuration_file(site_configuration: dict, wordpress_path: str, database_user_password: str):
    """Creates the wp-config-php WordPress configuration file using WP-CLI.

    All parameters are obtained from a site configuration file.

    For more information see:
        https://developer.wordpress.org/cli/commands/config/create/

    Args:
        site_configuration: parsed site configuration.
        wordpress_path: Path to WordPress files.
        database_user_password: Password for the database user configured in at the wp-config.php file.
    """
    database_props = site_configuration["database"]
    wp_cli.create_configuration_file(wordpress_path=wordpress_path,
                                     db_host=database_props["host"],
                                     db_name=database_props["name"],
                                     db_user=database_props["user"],
                                     db_pass=database_user_password,
                                     db_prefix=database_props["prefix"],
                                     db_charset=database_props["charset"],
                                     db_collate=database_props["collate"],
                                     skip_check=database_props["skip_check"],
                                     debug=site_configuration["wp_cli"]["debug"]
                                     )


def download_wordpress(site_configuration: dict, destination_path: str):
    """ Downloads the latest version of the WordPress core files using a site configuration file.

    For more information see:
        https://developer.wordpress.org/cli/commands/core/download/

    Args:
        site_configuration: parsed site configuration.
        destination_path: Path where WP-CLI will be downloaded.
    """
    if not paths.is_valid_path(destination_path):
        raise ValueError(literals.get("wp_non_valid_dir_path"))

    version = site_configuration["settings"]["version"]
    locale = site_configuration["settings"]["locale"]
    skip_content = site_configuration["settings"]["skip_content_download"]
    debug = site_configuration["wp_cli"]["debug"]
    wp_cli.download_wordpress(destination_path, version, locale, skip_content, debug)
    git_tools.purge_gitkeep(destination_path)


def export_database(site_configuration: dict, wordpress_path: str, dump_file_path: str):
    """Exports a WordPress database to a dump file using a site configuration file.

    All parameters are obtained from a site configuration file.

    For more information see:
        https://developer.wordpress.org/cli/commands/db/export/

    Args:
        site_configuration: parsed site configuration.
        wordpress_path: Path to WordPress files.
        dump_file_path: Path to the destination dump file.
    """
    wp_cli.export_database(wordpress_path, dump_file_path, site_configuration["wp_cli"]["debug"])


def get_constants() -> dict:
    """Gets all the constants from a WordPress constants resource.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-constants-schema.json


    Returns:
        All the constants in a dict object.
    """

    response = requests.get(wordpress_constants_json_resource)
    data = json.loads(response.content)

    return data


def get_project_structure(path: str) -> dict:
    """Gets the project structure from a WordPress project structure file.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/project-structure-schema.json

    Args:
        path: Full path to the WordPress project structure file.

    Returns:
        Project structure in a dict object.
    """
    with open(path, "r") as project_structure_file:
        data = project_structure_file.read()
        return json.loads(data)


def get_required_file_paths(path: str, required_file_patterns: List[str]) -> Tuple:
    """Returns file paths in a tuple from the file name patterns.

    Args:
        path: Where to look for the files.
        required_file_patterns: glob patterns of the file names to be found.

    Returns:
        Tuple with the file paths in the following order:
        - site configuration JSON file
        - site environments JSON file
        - project structure JSON file
    """

    # required_file_patterns = wordpress.constants.required_files_suffixes
    #
    # for required_file_pattern in required_file_patterns:
    #     if required_file_pattern.endswith()

    result = []
    for required_file_pattern in required_file_patterns:
        result.append(paths.get_file_path_from_pattern(path, required_file_pattern))

    return tuple(result)


def get_site_configuration(path: str) -> dict:
    """Gets the WordPress site configuration from a site configuration file.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-site-schema.json

    Args:
        path: Full path to the WordPress project structure file.

    Returns:
        Site configuration in a dict object.
    """

    with open(path, "r") as config_file:
        data = config_file.read()
        return json.loads(data)


def get_site_configuration_from_environment(environment_path: str, environment_name: str = None) -> dict:
    """Gets the WordPress site configuration from a environment.

    Args:
        environment_path: Path to the environments file.
        environment_name: Name of the environment.

    Returns:
        A dict with the site's configuration.
    """

    site_configuration_path = get_site_configuration_path_from_environment(environment_path, environment_name)

    return get_site_configuration(site_configuration_path)


def get_site_configuration_path_from_environment(environment_path: str, environment_name: str = None) -> str:
    """Gets the path to the WordPress site configuration from a environment.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-site-schema.json
        http://dev.aheadlabs.com/schemas/json/wordpress-site-environments-schema.json

    Args:
        environment_path: Full path to the WordPress site environment file.
        environment_name: Name of the environment to be got. If no name is
            given, default environment is obtained.

    Returns:
        Site configuration path.
    """

    with open(environment_path, "r") as environment_file:
        json_data = json.loads(environment_file.read())

    matching_environments = list(filter(lambda e: e["name"] == environment_name, json_data["environments"]))

    if len(matching_environments) == 0:
        raise ValueError(literals.get("wp_env_not_found"))

    if len(matching_environments) > 1:
        raise ValueError(literals.get("wp_env_gt1"))

    directory = pathlib.Path(environment_path).parent
    file_path = pathlib.Path.joinpath(directory, matching_environments[0]["configuration_file"])

    return str(file_path)


def get_site_environments(path: str) -> dict:
    """Gets the site environments from a WordPress site environment file.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-site-environments-schema.json

    Args:
        path: Full path to the WordPress project structure file.

    Returns:
        Site environments in a dict object.
    """
    pass


def get_wordpress_path_from_root_path(path) -> str:
    """ Gets the wordpress path based on the constants.json from a desired root path

    Args:
        path: Full path of the project
    """
    # Add constants
    wp_constants = get_constants()
    # Get wordpress path from the constants
    wordpress_relative_path = wp_constants["paths"]["wordpress"].split('/')[1]
    wordpress_path = os.path.join(path, wordpress_relative_path)
    return wordpress_path


def import_database(site_configuration: dict, wordpress_path: str, dump_file_path: str):
    """Imports a WordPress database from a dump file based on a site_configuration file.

    For more information see:
           https://developer.wordpress.org/cli/commands/db/import/
    Args:
        site_configuration: parsed site configuration.
        wordpress_path: Path to WordPress files.
        dump_file_path: Path to dump file to be imported.
    """
    dump_file_path_as_posix = str(pathlib.Path(dump_file_path).as_posix())
    wordpress_path_as_posix = str(pathlib.Path(wordpress_path).as_posix())
    wp_cli.import_database(wordpress_path_as_posix, dump_file_path_as_posix, site_configuration["wp_cli"]["debug"])


def install_plugins_from_configuration_file(site_configuration: dict, root_path: str):
    """Installs WordPress's plugin files (and child themes also) using WP-CLI.

       For more information see:
           https://developer.wordpress.org/cli/commands/plugin/install/

       Args:
           site_configuration: parsed site configuration.
           root_path: Path to project root.
       """
    # Add constants
    constants = get_constants()

    # Set/expand variables before using WP CLI
    wordpress_path = root_path + constants["paths"]["wordpress"]
    wordpress_path_as_posix = str(pathlib.Path(wordpress_path).as_posix())
    # For each plugin in config, invoke the command
    for plugin in site_configuration["plugins"]:
        plugin_name = plugin["name"]
        plugin_source = plugin["source"]
        plugins_path = root_path + constants["paths"]["content"]["plugins"]
        plugins_path_as_posix = str(pathlib.Path(plugins_path).as_posix())
        wp_cli.install_plugin(plugin_name, wordpress_path_as_posix,  plugin["force"], plugin_source,
                              site_configuration["wp_cli"]["debug"])
        # When source is zipped, move source to the plugins content path
        if plugin["source_type"] == "zip":
            shutil.move(plugin_source, plugins_path_as_posix)
            # Clean up
            git_tools.purge_gitkeep(plugins_path_as_posix)


def install_recommended_plugins():
    """ Uses TGMPA core to decide and install automatically the recommended plugins.

    See Also: http://tgmpluginactivation.com/
    See Also: https://github.com/itspriddle/wp-cli-tgmpa-plugin
    Args:

    """
    # TODO(alberto.carbonell) Develop an WP-cli extension.
    pass


def install_wordpress_core(site_config: dict, wordpress_path: str, admin_password: str):
    """Installs WordPress core files using a site configuration file.

        For more information see:
            https://developer.wordpress.org/cli/commands/core/install/

        Args:
            site_config: parsed site configuration.
            wordpress_path: Path to WordPress files.
            admin_password: Password for the WordPress administrator user
        """
    # Set/expand variables before using WP CLI
    debug_info = site_config["wp_cli"]["debug"]
    admin_user = site_config["settings"]["admin"]["user"]
    admin_email = site_config["settings"]["admin"]["email"]
    url = site_config["settings"]["wp_config"]["site_url"]["value"]
    title = site_config["settings"]["title"]
    skip_email = site_config["settings"]["admin"]["skip_email"]
    wp_cli.install_wordpress_core(wordpress_path, url, title, admin_user, admin_email, admin_password,
                                  skip_email, debug_info)


# TODO: (alberto.carbonell) Set child theme name using styles.css's Template property (in comments).
# See https://developer.wordpress.org/themes/advanced-topics/child-themes/
def install_theme_from_configuration_file(site_configuration: dict, root_path: str):
    """Installs WordPress's theme files (and child themes also) using a site configuration file

    For more information see:
        https://developer.wordpress.org/cli/commands/theme/install/

    Args:
        site_configuration: parsed site configuration.
        root_path: Path to project root.
    """
    if not site_configuration["themes"]:
        logging.info("No themes configured to install")
        return

    # Add constants
    constants = get_constants()

    # Set/expand variables before using WP CLI
    debug_info = site_configuration["wp_cli"]["debug"]
    theme_name = site_configuration["themes"]["name"]
    theme_source = site_configuration["themes"]["source"]
    wordpress_path = root_path + constants["paths"]["wordpress"]
    themes_path = os.path.join(root_path + constants["paths"]["content"]["themes"], theme_name)
    wordpress_path_as_posix = str(pathlib.Path(wordpress_path).as_posix())
    themes_path_as_posix = str(pathlib.Path(themes_path).as_posix())
    # TODO: (alberto.carbonell) Unused feature (regex): investigate why
    # wordpress_theme_regex_filter = filter(lambda elem: elem["key"] == "wordpress-theme", constants["regex_base64"])
    # wordpress_theme_regex = next(wordpress_theme_regex_filter)["value"]
    # regex_wordpress_theme = base64tools.decode(wordpress_theme_regex)

    # Install and activate WordPress theme
    wp_cli.install_theme(wordpress_path, theme_source, True, debug_info, theme_name)
    # Clean up the theme by moving to the content folder
    shutil.move(theme_source, themes_path_as_posix)
    if site_configuration["themes"]["has_child"] and site_configuration["themes"]["source_type"] == "zip":
        # This operation should take from a theme named <theme>.zip, a <theme>-child.zip path
        child_theme_path = theme_source.replace(
            pathlib.Path(theme_source).suffixes[0], "-child" + pathlib.Path(theme_source).suffixes[0])
        child_theme_path_as_posix = str(pathlib.Path(child_theme_path).as_posix())
        # Install and activate WordPress child theme
        wp_cli.install_theme(wordpress_path, child_theme_path_as_posix, True, debug_info, theme_name)
        # Clean up the theme by moving to the content folder
        shutil.move(child_theme_path_as_posix, themes_path_as_posix)
    git_tools.purge_gitkeep(themes_path_as_posix)
    # Backup database after theme install
    database_path = root_path + constants["paths"]["database"]
    core_dump_path_converted = convert_wp_config_token(site_configuration["database"]["dumps"]["theme"], wordpress_path)
    database_core_dump_path = os.path.join(database_path, core_dump_path_converted)
    database_core_dump_path_as_posix = str(pathlib.Path(database_core_dump_path).as_posix())
    export_database(site_configuration, wordpress_path_as_posix, database_core_dump_path_as_posix)


def install_wp_cli(install_path: str = "/usr/local/bin/wp"):
    """Downloads and installs the latest version of WP-CLI.

    For more information see:
        https://make.wordpress.org/cli/handbook/installing/

    Args:
        install_path: Path where WP-CLI will be installed. It must be in the
            PATH/BIN of the operating system.
    """

    wp_cli_phar = "wp-cli.phar"
    wp_cli_download_url = f"https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/{wp_cli_phar}"
    install_path = pathlib.Path(install_path)
    file_path = pathlib.Path.joinpath(install_path, wp_cli_phar)

    if not pathlib.Path.is_dir(install_path):
        raise ValueError(literals.get("wp_not_dir"))

    logging.info(literals.get("wp_wpcli_downloading").format(url=wp_cli_download_url))
    response = requests.get(wp_cli_download_url)

    with open(file_path, "wb") as cli:
        cli.write(response.content)

    file_stat = os.stat(file_path)
    os.chmod(file_path, file_stat.st_mode | stat.S_IEXEC)

    if sys.platform == "win32":
        create_wp_cli_bat_file(file_path)

    wp_cli.wp_cli_info()


def install_wordpress_site(site_configuration: dict, root_path: str, admin_password: str):
    """Installs WordPress core files using WP-CLI.

    This operation requires cleaning the db and doing a backup after the process.

    For more information see:
        https://developer.wordpress.org/cli/commands/core/install/

    Args:
        site_configuration: parsed site configuration.
        root_path: Path to site installation.
        admin_password: Password for the WordPress administrator user
    """
    # Add constants
    constants = get_constants()

    database_path = constants["paths"]["database"]
    wordpress_path = pathlib.Path(root_path + constants["paths"]["wordpress"])
    wordpress_path_as_posix = str(pathlib.Path(wordpress_path).as_posix())

    # Reset database
    wp_cli.reset_database(wordpress_path_as_posix, True, site_configuration["wp_cli"]["debug"])

    # Install wordpress
    install_wordpress_core(site_configuration, wordpress_path_as_posix, admin_password)

    # Update description option
    description = site_configuration["settings"]["description"]
    wp_cli.update_database_option("blogdescription", description, wordpress_path_as_posix, site_configuration["wp_cli"]["debug"])

    # Backup database
    core_dump_path_converted = convert_wp_config_token(site_configuration["database"]["dumps"]["core"], wordpress_path)
    database_core_dump_path = os.path.join(root_path + database_path, core_dump_path_converted)
    database_core_dump_path_as_posix = str(pathlib.Path(database_core_dump_path).as_posix())
    export_database(site_configuration, wordpress_path_as_posix, database_core_dump_path_as_posix)


def set_wordpress_config_from_configuration_file(site_config: dict, wordpress_path: str, db_user_password: str) -> None:
    """ Sets all configuration parameters in pristine WordPress core files
    Args:
        site_config: parsed site configuration.
        wordpress_path: Path to wordpress installation.
        db_user_password: Database user password.

    """
    # Create wp-config.php file
    create_configuration_file(site_config, wordpress_path, db_user_password)
    # Get config properties to set from site configuration
    wp_config_properties = site_config["settings"]["wp_config"]
    debug = site_config["wp_cli"]["debug"]

    # Foreach variable to set: execute wp config set
    for prop in wp_config_properties.values():
        # This value will place the value as it gets, without quotes
        value = prop.get("value")
        raw = type(value) != str
        wp_cli.set_configuration_value(
            prop.get("name"), value, prop.get("type"), wordpress_path, raw, debug)


def start_basic_project_structure(root_path: str, project_structure_path: str) -> None:
    """ Creates a basic structure of a wordpress project based on the project-structure.json

    Args:
        root_path: Full path where the structure will be created
        project_structure_path: Full path to the json containing the structure
    """
    # Parse project structure configuration
    project_structure = get_project_structure(project_structure_path)
    project_starter = BasicStructureStarter()
    # Iterate through every item recursively
    for item in project_structure["items"]:
        project_starter.add_item(item, root_path)


if __name__ == "__main__":
    help(__name__)
