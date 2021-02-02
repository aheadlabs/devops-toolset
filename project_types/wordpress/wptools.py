"""Contains several tools for WordPress"""
import core.log_tools
import filesystem.parsers as parsers
import filesystem.paths as paths
import filesystem.zip
import json
import logging
import os
import pathlib
import project_types.wordpress.wp_cli as wp_cli
import project_types.node.npm as npm
import re
import requests
import stat
import sys
import tools.git as git_tools
from project_types.wordpress.constants import wordpress_constants_json_resource
from project_types.wordpress.basic_structure_starter import BasicStructureStarter
from core.app import App
from core.CommandsCore import CommandsCore
from core.LiteralsCore import LiteralsCore
from project_types.wordpress.Literals import Literals as WordpressLiterals
from devops_platforms.azuredevops.Literals import Literals as PlatformLiterals
from devops_platforms import constants as devops_platforms_constants
from project_types.wordpress.commands import Commands as WordpressCommands
from tools import cli
from typing import List, Tuple


app: App = App()
platform_specific_restapi = app.load_platform_specific("restapi")
literals = LiteralsCore([WordpressLiterals])
platform_literals = LiteralsCore([PlatformLiterals])
commands = CommandsCore([WordpressCommands])


def add_wp_options(wp_options: dict, wordpress_path: str, debug: bool = False):
    """Adds or updates WordPress options in the wp_options table

    Args:
        wp_options: WordPress options.
        wordpress_path: Path to the WordPress installation.
        debug: If True logs debug information.
    """
    for option in wp_options:
        wp_cli.add_update_option(option, wordpress_path, debug)


def check_themes_configuration(themes: dict) -> bool:
    """Checks that the themes configuration is correct.

    Args:
        themes: Themes configuration.

    Returns:
        True if the configuration is correct, False if incorrect.
    """

    # Check if the number of themes is correct
    themes_number = len(themes)
    if themes_number == 0 or themes_number > 2:
        logging.error(literals.get("wp_config_file_bad_themes_number").format(number=themes_number))
        logging.warning(literals.get("wp_themes_install_manually"))
        return False

    # Check if the number of themes to be activated is more or less than one
    themes_to_activate: int = 0
    for theme in themes:
        if theme["activate"]:
            themes_to_activate += 1
    if themes_to_activate == 0 or themes_to_activate > 1:
        logging.error(literals.get("wp_config_file_only_one_activated_theme").format(number=themes_to_activate))
        logging.warning(literals.get("wp_themes_install_manually"))
        return False

    return True


def check_theme_configuration(theme: dict) -> bool:
    """Checks that the themes configuration is correct.

    Args:
        theme: Themes configuration.

    Returns:
        True if the configuration is correct, False if incorrect.
    """

    # Check if feed-based themes contain feed information
    if theme["source_type"] == "feed" and "feed" not in theme:
        logging.error(literals.get("wp_theme_feed_no_info").format(theme=theme["name"]))
        logging.warning(literals.get("wp_themes_install_manually"))
        return False

    return True


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
    # NOTE: Add more tokens if needed
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


def create_development_theme(theme_configuration: dict, root_path: str):
    """ Creates the structure of a development theme.

    Args:
        theme_configuration: The themes configuration node
        root_path: The desired destination path of the theme
    """

    constants = get_constants()
    root_path = pathlib.Path(root_path)
    destination_path = pathlib.Path.joinpath(root_path, constants["paths"]["content"]["themes"])
    # Extract theme name from the themes configuration dict
    src_theme = list(filter(lambda t: t["source_type"] == "src", theme_configuration))
    theme_slug = src_theme[0]["source"]
    # Determine if we have a theme structure file available (should be named as [theme-slug]-wordpress-theme-structure
    structure_file_name = f'{theme_slug}-wordpress-theme-structure.json'
    structure_file_path = pathlib.Path.joinpath(root_path, structure_file_name)
    # Create the structure based on the theme_name
    start_basic_theme_structure(destination_path, theme_slug, structure_file_path)
    # Replace necessary theme files with the theme name.


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


def download_wordpress_plugin(plugin_config: dict, destination_path: str):
    """Downloads a WordPress plugin from an URL.

    NOTE: The URL must download a zip file that contains the plugin. If the ZIP
        contains a non-standard inner structure, the calling process will
        produce side-effects.

    Args:
        plugin_config: Plugin configuration.
        destination_path: Path where the plugin will be downloaded.
    """
    with open(destination_path, "wb") as file:
        response = requests.get(plugin_config["source"])
        file.write(response.content)


def download_wordpress_theme(theme_config: dict, destination_path: str, **kwargs):
    """Downloads a WordPress theme from a feed or a URL.

    NOTE: The URL must download a zip file that contains the theme. If the ZIP
        contains a non-standard inner structure, the calling process will
        produce side-effects.

    Args:
        theme_config: Theme configuration.
        destination_path: Path where the theme will be downloaded.
        kwargs: Platform-specific arguments
    """
    source_type: str = theme_config["source_type"]

    if source_type == "feed":
        feed_config = theme_config["feed"]
        matches = re.search(r"https:\/\/dev.azure.com\/(\w+)\/", feed_config["organization_url"])
        organization = matches.group(1)
        if "azdevops_user" in kwargs and "azdevops_token" in kwargs:
            platform_specific_restapi.get_last_artifact(organization, feed_config["name"], feed_config["package"],
                                                        destination_path, kwargs["azdevops_user"],
                                                        kwargs["azdevops_token"])
        else:
            logging.warning(platform_literals.get("azdevops_token_not_found"))
            logging.warning(platform_literals.get("azdevops_download_package_manually"))
    elif source_type == "url":
        paths.download_file(theme_config["source"], destination_path, f"{theme_config['name']}.zip")


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


def get_db_admin_from_environment(environment_path: str, environment_name: str = None) -> str:
    """ Gets the db_admin user from the environment path

        Args:
             environment_path: Path to the environments file.
             environment_name: Name of the environment.

    """
    environment_obj = get_site_environments(environment_path, environment_name)
    db_admin_user = environment_obj["db_admin_user"]
    logging.info(literals.get("wp_got_db_admin_user").format(db_admin_user=db_admin_user))

    return db_admin_user


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


def get_project_structure(url_resource: str) -> dict:
    """Gets the project structure from a WordPress project structure file located on an url resource.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/project-structure-schema.json

    Args:
        url_resource: Full url resource to the WordPress project structure file.

    Returns:
        Project structure in a dict object.
    """
    request = requests.get(url_resource)
    return request.json()


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

    if len(result) == 0:
        logging.info(literals.get("wp_required_file_paths_not_found"))
    else:
        core.log_tools.log_indented_list(literals.get("wp_required_file_paths_found"),
                                         result,
                                         core.log_tools.LogLevel.info)

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

    with open(path, "r", encoding="utf-8") as config_file:
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
        environment_path: Path to the WordPress environment file.
        environment_name: Environment name that exists in the environment file.

    Returns:
        Site configuration path.
    """

    if environment_path is None:
        raise ValueError(literals.get("wp_environment_path_not_found"))
    if environment_name is None:
        raise ValueError(literals.get("wp_environment_name_not_found"))

    environment_obj = get_site_environments(environment_path, environment_name)

    directory = pathlib.Path(environment_path).parent
    file_path = pathlib.Path.joinpath(directory, environment_obj["configuration_file"])
    if not file_path.exists() or not file_path.is_file():
        raise ValueError(literals.get("wp_file_not_found").format(file=file_path))
    logging.info(literals.get("wp_environment_file_used").format(file=file_path))

    return str(file_path)


def get_site_environments(environment_path: str, environment_name: str = None) -> dict:
    """Gets the site environments from a WordPress site environment file.

    For more information see:
        http://dev.aheadlabs.com/schemas/json/wordpress-site-environments-schema.json

    Args:
        environment_path: Full path to the WordPress site environment file.
        environment_name: Name of the environment to be got. If no name is
            given, default environment is obtained.

    Returns:
        Site environments in a dict object.
    """
    with open(environment_path, "r") as environment_file:
        json_data = json.loads(environment_file.read())

    matching_environments = list(filter(lambda e: e["name"] == environment_name, json_data["environments"]))

    if len(matching_environments) == 0:
        raise ValueError(literals.get("wp_env_not_found"))

    if len(matching_environments) > 1:
        raise ValueError(literals.get("wp_env_gt1"))

    return matching_environments[0]


def get_themes_path_from_root_path(root_path) -> str:
    """ Gets the themes path based on the constants.json from a desired root path

    Args:
        root_path: Full path of the project
    """
    # Add constants
    wp_constants = get_constants()

    # Get wordpress path from the constants
    themes_relative_path = wp_constants["paths"]["content"]["themes"]
    themes_path = pathlib.Path.joinpath(pathlib.Path(root_path), themes_relative_path).as_posix()
    logging.info(literals.get("wp_themes_path").format(path=themes_path))

    return themes_path


def get_wordpress_path_from_root_path(root_path) -> str:
    """ Gets the wordpress path based on the constants.json from a desired root path

    Args:
        root_path: Full path of the project
    """
    logging.info(literals.get("wp_root_path").format(path=root_path))

    # Add constants
    wp_constants = get_constants()

    # Get wordpress path from the constants
    wordpress_relative_path = wp_constants["paths"]["wordpress"]
    wordpress_path = pathlib.Path.joinpath(pathlib.Path(root_path), wordpress_relative_path).as_posix()
    logging.info(literals.get("wp_wordpress_path").format(path=wordpress_path))

    return wordpress_path


def import_content_from_configuration_file(site_configuration: dict, wordpress_path: str):
    """ Imports WordPress posts content specified on a site_configuration file .

    Args:
        site_configuration: parsed site configuration.
        wordpress_path: Path to WordPress files.
    """
    # Add constants
    wp_constants = get_constants()

    # Get wxr path from the constants
    wxr_path = pathlib.Path(wp_constants["paths"]["content"]["wxr"])
    authors = pathlib.Path.joinpath(wxr_path, "mapping.csv")
    if not pathlib.Path.exists(authors):
        authors = "skip"
    debug_info = site_configuration["wp_cli"]["debug"]
    for content_type in site_configuration["content"]:
        # File name will be the {wxr_path}/{content_type}.xml
        content_path = pathlib.Path.joinpath(wxr_path, f"{content_type}.xml")
        # Delete content before importing (to avoid duplicating content)
        wp_cli.delete_post_type_content(wordpress_path, content_type, debug_info)
        # Import new content
        wp_cli.import_wxr_content(wordpress_path, content_path, authors, debug_info)


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


def install_plugins_from_configuration_file(site_configuration: dict, root_path: str, skip_partial_dumps: bool):
    """Installs WordPress's plugin files using WP-CLI.

       For more information see:
           https://developer.wordpress.org/cli/commands/plugin/install/

       Args:
           site_configuration: parsed site configuration.
           root_path: Path to project root.
           skip_partial_dumps: If True skips database dumps.
       """
    # Get data needed in the process
    plugins: dict = site_configuration["plugins"]
    constants = get_constants()
    root_path_obj = pathlib.Path(root_path)
    wordpress_path = pathlib.Path.joinpath(root_path_obj, constants["paths"]["wordpress"])
    plugins_path = pathlib.Path.joinpath(root_path_obj, constants["paths"]["content"]["plugins"])
    debug_info = site_configuration["wp_cli"]["debug"]

    for plugin in plugins:
        # Get plugin path
        plugin_path = pathlib.Path.joinpath(plugins_path, f"{plugin['name']}.zip")
        logging.info(literals.get("wp_plugin_path").format(path=plugin_path))

        # Download theme if needed
        if plugin["source_type"] == "url":
            download_wordpress_plugin(plugin, plugin_path)

            # Once downloaded, should have a .zip under plugins path, so can freely add this source as a .zip one for
            # further installing this plugin as a zip
            plugin["source_type"] = "zip"

        if plugin["source_type"] == "zip":
            plugin["source"] = plugin_path

        wp_cli.install_plugin(plugin["name"], wordpress_path, plugin["activate"], plugin["force"], plugin["source"],
                              debug_info)

        # Backup database after plugin install
        if not skip_partial_dumps:
            database_path = pathlib.Path.joinpath(root_path_obj, constants["paths"]["database"])
            core_dump_path_converted = convert_wp_config_token(
                site_configuration["database"]["dumps"]["plugins"], wordpress_path)
            database_core_dump_path = pathlib.Path.joinpath(database_path, core_dump_path_converted)
            export_database(site_configuration, wordpress_path, database_core_dump_path.as_posix())


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


def install_themes_from_configuration_file(site_configuration: dict, root_path: str,
                                           skip_partial_dumps: bool, **kwargs):
    """Installs WordPress's theme files (and child themes also) using a site configuration file

    For more information see:
        https://developer.wordpress.org/cli/commands/theme/install/

    Args:
        site_configuration: parsed site configuration.
        root_path: Path to project root.
        skip_partial_dumps: If True skips database dumps.
    """

    child_theme_config: dict
    parent_theme_config: dict

    # Get data needed in the process
    themes: dict = site_configuration["themes"]
    constants = get_constants()
    root_path_obj = pathlib.Path(root_path)
    wordpress_path = pathlib.Path.joinpath(root_path_obj, constants["paths"]["wordpress"])
    themes_path = pathlib.Path.joinpath(root_path_obj, constants["paths"]["content"]["themes"])
    debug_info = site_configuration["wp_cli"]["debug"]

    # Check themes configuration
    if not check_themes_configuration(themes):
        return

    for theme in themes:
        # Check theme configuration
        if not check_theme_configuration(theme):
            continue

        # Get theme path
        theme_path = pathlib.Path.joinpath(themes_path, f"{theme['name']}.zip")
        logging.info(literals.get("wp_theme_path").format(path=theme_path))
        theme["source"] = theme_path

        # Download theme if needed
        if theme["source_type"] in ["url", "feed"]:
            download_wordpress_theme(theme, themes_path, **kwargs)

        # Get template for the theme if it has one
        style_content: bytes = filesystem.zip.read_text_file_in_zip(theme_path, f"{theme['name']}/style.css")
        metadata: dict = filesystem.parsers.parse_theme_metadata(style_content, ["Template", "Version"])
        theme["template"] = metadata["Template"] if "Template" in metadata else None
        theme["version"] = metadata["Version"]

    # Set child theme and parent theme, or just child theme (the one to be activated)
    parent_theme_config, child_theme_config = triage_themes(themes)

    # Install parent theme
    if parent_theme_config:
        wp_cli.install_theme(wordpress_path, parent_theme_config["source"], parent_theme_config["activate"],
                             debug_info, parent_theme_config["name"])

    # Install child / single theme
    wp_cli.install_theme(wordpress_path, child_theme_config["source"], child_theme_config["activate"],
                         debug_info, child_theme_config["name"])

    # TODO(anyone) Clean up theme ZIP files for themes which sources are not ZIP

    # Backup database after theme install
    if not skip_partial_dumps:
        database_path = pathlib.Path.joinpath(root_path_obj, constants["paths"]["database"])
        core_dump_path_converted = convert_wp_config_token(
            site_configuration["database"]["dumps"]["theme"], wordpress_path)
        database_core_dump_path = pathlib.Path.joinpath(database_path, core_dump_path_converted)
        export_database(site_configuration, wordpress_path, database_core_dump_path.as_posix())


def build_theme(themes_config: dict, theme_path: str):
    """ Builds a theme source into a packaged theme distribution using npm tasks

    Args:
        themes_config: Themes configuration
        theme_path: Path to the theme in the WordPress repository
    """
    logging.info(literals.get("wp_looking_for_src_themes"))

    # Get configuration data and paths
    src_theme_list = list(filter(lambda elem: elem["source_type"] == "src", themes_config))

    if len(src_theme_list) == 0:
        # Src theme not present
        logging.info(literals.get("wp_no_src_themes"))
        return

    src_theme = src_theme_list[0]
    theme_path_obj = pathlib.Path(theme_path)
    theme_path_src = pathlib.Path.joinpath(theme_path_obj, src_theme["source"])
    theme_path_dist = pathlib.Path.joinpath(theme_path_src, "dist")
    theme_path_zip = pathlib.Path.joinpath(theme_path_obj, f"{src_theme['name']}.zip")

    if os.path.exists(theme_path_src):

        theme_slug = src_theme["name"]

        # Change to the the theme's source directory
        os.chdir(theme_path_src)

        # Run npm install from the package.json path
        npm.install()

        # Run npm run build to execute the task build with the required parameters
        cli.call_subprocess(commands.get("wp_theme_src_build").format(
            theme_slug=theme_slug,
            path=theme_path_dist
        ), log_before_out=[literals.get("wp_gulp_build_before").format(theme_slug=theme_slug)],
            log_after_out=[literals.get("wp_gulp_build_after").format(theme_slug=theme_slug)],
            log_after_err=[literals.get("wp_gulp_build_error").format(theme_slug=theme_slug)])

        # Zip dist
        filesystem.zip.zip_directory(theme_path_dist.as_posix(), theme_path_zip.as_posix(), f"{theme_slug}/")
    else:
        logging.error(literals.get("wp_file_not_found").format(file=theme_path_src))


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


def install_wordpress_site(site_configuration: dict, root_path: str, admin_password: str,
                           skip_partial_dumps: bool = False):
    """Installs WordPress core files using WP-CLI.

    This operation requires cleaning the db and doing a backup after the process.

    For more information see:
        https://developer.wordpress.org/cli/commands/core/install/

    Args:
        site_configuration: parsed site configuration.
        root_path: Path to site installation.
        admin_password: Password for the WordPress administrator user.
        skip_partial_dumps: If True skips database dump.
    """
    # Add constants
    constants = get_constants()

    database_path = constants["paths"]["database"]
    root_path_obj = pathlib.Path(root_path)
    wordpress_path = pathlib.Path.joinpath(root_path_obj, constants["paths"]["wordpress"])
    wordpress_path_as_posix = str(pathlib.Path(wordpress_path).as_posix())

    # Install wordpress
    install_wordpress_core(site_configuration, wordpress_path_as_posix, admin_password)

    # Update description option
    description = site_configuration["settings"]["description"]
    wp_cli.update_database_option(
        "blogdescription", description, wordpress_path_as_posix, site_configuration["wp_cli"]["debug"])

    # Backup database
    if not skip_partial_dumps:
        core_dump_path_converted = \
            convert_wp_config_token(site_configuration["database"]["dumps"]["core"], wordpress_path)
        database_core_dump_directory_path = pathlib.Path.joinpath(root_path_obj, database_path)
        database_core_dump_path = pathlib.Path.joinpath(database_core_dump_directory_path, core_dump_path_converted)
        export_database(site_configuration, wordpress_path_as_posix, database_core_dump_path.as_posix())
        git_tools.purge_gitkeep(database_core_dump_directory_path.as_posix())


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


def setup_database(site_config: dict, wordpress_path: str, db_user_password: str,
                   admin_db_user: str = "", admin_db_password: str = ""):
    """ Uses wp cli create to create a new database from configuration file

    Args:
        site_config: parsed site configuration.
        wordpress_path: Path to WordPress files.
        db_user_password: Password of the database user to be created.
        admin_db_user: Database administrator user name.
        admin_db_password:  Database administrator user password.
    """
    db_user = site_config["database"]["user"]
    schema = site_config["database"]["name"]
    db_host = site_config["database"]["host"]

    wp_cli.create_database(wordpress_path, site_config["wp_cli"]["debug"], admin_db_user, admin_db_password, schema)

    wp_cli.create_wordpress_database_user(
        wordpress_path, admin_db_user, admin_db_password, db_user, db_user_password, schema, db_host)


def start_basic_project_structure(root_path: str) -> None:
    """ Creates a basic structure of a wordpress project based on the project-structure.json

    Args:
        root_path: Full path where the structure will be created
    """

    logging.info(literals.get("wp_creating_project_structure"))

    structure_file_path = pathlib.Path.joinpath(pathlib.Path(root_path), "wordpress-project-structure.json")
    # Parse project structure configuration
    if pathlib.Path.exists(structure_file_path):
        project_structure = get_site_configuration(structure_file_path)
    else:
        project_structure = get_project_structure(devops_platforms_constants.Urls.DEFAULT_WORDPRESS_PROJECT_STRUCTURE)

    project_starter = BasicStructureStarter()

    # Iterate through every item recursively
    for item in project_structure["items"]:
        project_starter.add_item(item, root_path)

    logging.info(literals.get("wp_created_project_structure"))


def start_basic_theme_structure(path: str, theme_name: str, structure_file_path: str = None) -> None:
    """ Creates a basic structure of a wordpress development theme based on its default theme-structure.json

        Args:
            path: Full path where the structure will be created
            theme_name: Name of the theme to be used to create the root folder
            structure_file_path: Optional parameter containing the structure file path to be used. If ignored, the
            default structure file will be used.
        """

    # Parse project structure configuration
    if pathlib.Path.exists(structure_file_path):
        project_structure = get_site_configuration(structure_file_path)
        logging.info(literals.get("wp_theme_structure_creating_from_file").format(theme_name=theme_name,
                                                                                  file_name=structure_file_path))
    else:
        project_structure = get_project_structure(
            devops_platforms_constants.Urls.DEFAULT_WORDPRESS_DEVELOPMENT_THEME_STRUCTURE)
        logging.info(literals.get("wp_theme_structure_creating_from_default_file").format(
            resource=devops_platforms_constants.Urls.DEFAULT_WORDPRESS_DEVELOPMENT_THEME_STRUCTURE))

    project_starter = BasicStructureStarter()

    # Change the main folder's name of the theme to the theme_name
    project_structure["items"][0]["name"] = theme_name

    # Purge .gitkeep
    git_tools.purge_gitkeep(path)

    # Iterate through every item recursively
    for item in project_structure["items"]:
        project_starter.add_item(item, path)

    logging.info(literals.get("wp_created_theme_structure").format(theme_name=theme_name))


def triage_themes(themes: dict) -> (dict, dict):
    """triages themes to determine which must be installed and activated.

    Args:
        themes: Themes configuration.

    Return:
        Tuple with parent and child theme configuration.
    """
    child = None
    parent = None
    parent_guess: str

    for theme in themes:
        if not theme["activate"]:
            parent_guess = theme["name"]
        if theme["activate"]:
            child = theme
            if theme["template"]:
                parent_guess = theme["template"]

        if not theme["activate"] and not theme["template"] and theme["name"] == parent_guess:
            parent = theme

    return parent, child


if __name__ == "__main__":
    help(__name__)
