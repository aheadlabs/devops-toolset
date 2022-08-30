"""Contains several tools and utils for WordPress Plugins"""
import devops_toolset.tools.svn as svn
import logging
import pathlib

from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.core.app import App
from devops_toolset.devops_platforms.azuredevops.Literals import Literals as PlatformLiterals
from devops_toolset.project_types.wordpress.Literals import Literals as WordpressLiterals
from devops_toolset.project_types.wordpress.commands import Commands as WordpressCommands

app: App = App()
platform_specific_restapi = app.load_platform_specific("restapi")
literals = LiteralsCore([WordpressLiterals])
platform_literals = LiteralsCore([PlatformLiterals])
commands = CommandsCore([WordpressCommands])


def create_release_tag(plugin_root_path: str, tag_name: str, copy_trunk: bool = True):
    """ Creates the structure for a new tag in a plugin structure

        Args:
            :param plugin_root_path: Source path which contains the plugin code.
            :param tag_name: Tag name to be created. Must not exist
            :param copy_trunk: If True, then the current content on /trunk will be copied
    """

    try:
        # Check plugin root exist
        __check_plugin_path_exists(plugin_root_path)

        # Check tag structure does not exist yet
        plugin_tag_path = pathlib.Path(plugin_root_path).joinpath('tags', tag_name)
        if pathlib.Path.exists(plugin_tag_path):
            logging.warning(literals.get("wp_plugin_tag_already_exists").format(tag_name=tag_name))
            return

        # Create the structure under the plugin root path
        pathlib.Path.mkdir(plugin_tag_path)

        logging.info(literals.get("wp_plugin_tag_path_created").format(plugin_tag_path=plugin_tag_path))

        # If copy_trunk, then copy the content on tag folder using svn_copy
        if copy_trunk:
            plugin_trunk_path: str = str(pathlib.Path(plugin_root_path).joinpath('trunk'))
            __check_plugin_path_exists(plugin_trunk_path)
            svn.svn_copy(plugin_trunk_path + "/*", str(plugin_tag_path))
            logging.info(literals.get("wp_plugin_trunk_copied").format(plugin_trunk_path=plugin_tag_path))

        return

    except FileNotFoundError as exception:
        logging.exception(exception)
        return


def deploy_current_trunk(plugin_root_path: str, commit_message: str, username: str, password: str):
    """ Deploys the current trunk to the SVN central repository

        Args:
            :param plugin_root_path: Source path which contains the plugin code.
            :param commit_message: Comment for the commit that will be created
            :param username: Username of the owner of the repository who will perform the operation
            :param password: Password of the owner of the repository who will perform the operation
    """

    try:
        # Check plugin root exist
        __check_plugin_path_exists(plugin_root_path)

        # Check commit comment, username & password are not empty
        __check_parameters(commit_message, username, password)

        # Call svn_add
        plugin_trunk_path: str = str(pathlib.Path(plugin_root_path).joinpath('trunk'))
        __check_plugin_path_exists(plugin_trunk_path)
        logging.info(literals.get("wp_plugin_add").format(plugin_path=plugin_trunk_path))
        svn.svn_add(f'{plugin_trunk_path}/*')

        # Call svn_checkin
        logging.info(literals.get("wp_plugin_checkin").format(plugin_path=plugin_trunk_path))
        svn.svn_checkin(commit_message, username, password)

    except (FileNotFoundError, ValueError) as exception:
        logging.exception(exception)
        return


def deploy_release_tag(plugin_root_path: str, tag_name: str, commit_message: str, username: str, password: str):
    """ Creates and deploys the current trunk to the SVN central repository as a new tag

        Args:
            :param plugin_root_path: Source path which contains the plugin code.
            :param tag_name: Tag name to be created. Must not exist.
            :param commit_message: Comment for the commit that will be created.
            :param username: Username of the owner of the repository who will perform the operation
            :param password: Password of the owner of the repository who will perform the operation
    """

    try:
        # Check commit comment, username & password are not empty
        __check_parameters(commit_message, username, password)

        # Check plugin root exist
        __check_plugin_path_exists(plugin_root_path)

        # Create release tag if not exist
        create_release_tag(plugin_root_path, tag_name)

        # Add and checkin the new tag created (it will be created on the current trunk)
        plugin_tag_path = pathlib.Path(plugin_root_path).joinpath('tags', tag_name)
        logging.info(literals.get("wp_plugin_add").format(plugin_path=plugin_tag_path))
        svn.svn_add(f'{plugin_tag_path}/*')
        logging.info(literals.get("wp_plugin_checkin").format(plugin_path=plugin_tag_path))
        svn.svn_checkin(commit_message, username, password)

    except (FileNotFoundError, ValueError) as exception:
        logging.exception(exception)
        return


def __check_parameters(commit_message: str, username: str, password: str):
    """ Checks parameters passed and raises an exception if they don't fit the spec

        Args:
            :param commit_message: Comment for the commit that will be created.
            :param username: Username of the owner of the repository who will perform the operation.
            :param password: Password of the owner of the repository who will perform the operation.
    """
    if commit_message is None or commit_message == '':
        raise ValueError(literals.get("wp_mandatory_parameter").format(parameter_name=commit_message))
    if username is None or username == '':
        raise ValueError(literals.get("wp_mandatory_parameter").format(parameter_name=username))
    if password is None or password == '':
        raise ValueError(literals.get("wp_mandatory_parameter").format(parameter_name=password))


def __check_plugin_path_exists(plugin_path: str):
    """ Checks if a plugin relative path exists or not. If not, an exception will be raised.

        Args:
            :param plugin_path: Plugin's relative path to check.
    """
    if not pathlib.Path.exists(pathlib.Path(plugin_path)):
        raise FileNotFoundError(literals.get("wp_non_valid_dir_path"))


if __name__ == "__main__":
    help(__name__)
