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
import requests
import shutil
import stat
import sys
import tools.git as git_tools
from project_types.wordpress.constants import wordpress_constants_json_resource
from project_types.wordpress.basic_structure_starter import BasicStructureStarter
from core.app import App
from core.CommandsCore import CommandsCore
from core.LiteralsCore import LiteralsCore
from project_types.wordpress.Literals import Literals as WordpressLiterals
from project_types.wordpress.commands import Commands as WordpressCommands
from tools import cli
from typing import List, Tuple


app: App = App()
platform_specific = app.load_platform_specific("artifacts")
literals = LiteralsCore([WordpressLiterals])
commands = CommandsCore([WordpressCommands])


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
        platform_specific.download_artifact_from_feed(theme_config["feed"], destination_path, **kwargs)
    elif source_type == "url":
        destination_file_path = pathlib.Path.joinpath(pathlib.Path(destination_path), f"{theme_config['name']}.zip")
        with open(destination_file_path, "wb") as file:
            response = requests.get(theme_config["source"])
            file.write(response.content)
    # TODO(ivan.sainz) Unit tests


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
        path: Full path of the project
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
    wordpress_path = pathlib.Path.joinpath(pathlib.Path(root_path), constants["paths"]["wordpress"]).as_posix()
    # For each plugin in config, invoke the command
    for plugin in site_configuration["plugins"]:
        plugin_name = plugin["name"]
        plugin_source = plugin["source"]
        plugins_path = pathlib.Path.joinpath(
            pathlib.Path(root_path), constants["paths"]["content"]["plugins"]).as_posix()
        wp_cli.install_plugin(plugin_name, wordpress_path,  plugin["force"], plugin_source,
                              site_configuration["wp_cli"]["debug"])
        # When source is zipped, move source to the plugins content path
        if plugin["source_type"] == "zip":
            shutil.move(plugin_source, plugins_path)
            # Clean up
            git_tools.purge_gitkeep(plugins_path)


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
def install_themes_from_configuration_file(site_configuration: dict, root_path: str, **kwargs):
    """Installs WordPress's theme files (and child themes also) using a site configuration file

    For more information see:
        https://developer.wordpress.org/cli/commands/theme/install/

    Args:
        site_configuration: parsed site configuration.
        root_path: Path to project root.
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
        theme["source"] = theme_path

        # Download theme if needed
        if theme["source_type"] in ["url", "feed"]:
            download_wordpress_theme(theme, theme_path, **kwargs)

        # Get template for the theme if it has one
        style_content: bytes = filesystem.zip.read_text_file_in_zip(theme_path, "style.css")
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

    # Backup database after theme install
    database_path = pathlib.Path.joinpath(root_path_obj, constants["paths"]["database"])
    core_dump_path_converted = convert_wp_config_token(
        site_configuration["database"]["dumps"]["theme"], wordpress_path)
    database_core_dump_path = pathlib.Path.joinpath(database_path, core_dump_path_converted)
    export_database(site_configuration, wordpress_path, database_core_dump_path.as_posix())


def build_theme(site_configuration: dict, theme_path: str):
    """ Builds a theme source into a packaged theme distribution using npm tasks

    Args:
        site_configuration: Parsed site configuration
        theme_path: Path to the wordpress installation
        wordpress_theme_path: Path to the theme in the WordPress installation
    """
    logging.info(literals.get("wp_looking_for_src_themes"))

    # Get configuration data and paths
    src_theme = list(filter(lambda elem: elem["source_type"] == "src", site_configuration["themes"]))

    if len(src_theme) == 0:
        # Src theme not present
        logging.info(literals.get("wp_no_src_themes"))
        return

    theme_path_src = pathlib.Path.joinpath(pathlib.Path(theme_path), src_theme[0]["source"])
    theme_path_dist = pathlib.Path.joinpath(theme_path_src, "dist")

    if os.path.exists(theme_path_src):

        theme_slug = src_theme[0]["name"]

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


def install_wordpress_site(site_configuration: dict, root_path: str, admin_password: str):
    """Installs WordPress core files using WP-CLI.

    This operation requires cleaning the db and doing a backup after the process.

    For more information see:
        https://developer.wordpress.org/cli/commands/core/install/

    Args:
        site_configuration: parsed site configuration.
        root_path: Path to site installation.
        admin_password: Password for the WordPress administrator user
        is_devops: True if devops engine launched this, False otherwise
    """
    # Add constants
    constants = get_constants()

    database_path = constants["paths"]["database"]
    wordpress_path = pathlib.Path.joinpath(pathlib.Path(root_path), constants["paths"]["wordpress"])
    wordpress_path_as_posix = str(pathlib.Path(wordpress_path).as_posix())

    # Reset database
    wp_cli.reset_database(wordpress_path_as_posix, True, site_configuration["wp_cli"]["debug"])

    # Install wordpress
    install_wordpress_core(site_configuration, wordpress_path_as_posix, admin_password)

    # Update description option
    description = site_configuration["settings"]["description"]
    wp_cli.update_database_option(
        "blogdescription", description, wordpress_path_as_posix, site_configuration["wp_cli"]["debug"])

    # Backup database
    core_dump_path_converted = \
        convert_wp_config_token(site_configuration["database"]["dumps"]["core"], wordpress_path)
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
    wp_cli.create_database(wordpress_path, site_config["wp_cli"]["debug"], admin_db_user, admin_db_password)

    db_user = site_config["database"]["user"]
    schema = site_config["database"]["name"]
    db_host = site_config["database"]["host"]

    wp_cli.create_wordpress_database_user(
        wordpress_path, admin_db_user, admin_db_password, db_user, db_user_password, schema, db_host)


def start_basic_project_structure(root_path: str, project_structure_path: str) -> None:
    """ Creates a basic structure of a wordpress project based on the project-structure.json

    Args:
        root_path: Full path where the structure will be created
        project_structure_path: Full path to the json containing the structure
    """

    logging.info(literals.get("wp_creating_project_structure"))

    # Parse project structure configuration
    project_structure = get_project_structure(project_structure_path)
    project_starter = BasicStructureStarter()

    # Iterate through every item recursively
    for item in project_structure["items"]:
        project_starter.add_item(item, root_path)

    logging.info(literals.get("wp_created_project_structure"))


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

    # site_config = get_site_configuration_from_environment(
    #     r"D:\Source\_david-diaz-fernandez\atipico-santiago\default-site-environments.json", "localhost")
    # install_themes_from_configuration_file(
    #     site_config,
    #     r"D:\Source\_david-diaz-fernandez\atipico-santiago",
    #     azdevops_token="ysi4dwqwbq5lfnqolhmbet5kfxd6s3adh236257dlsx3iztmvmja"
    # )
