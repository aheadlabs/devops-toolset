"""wordpress module literals"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the wordpress module."""

    _titles = {
        "wp_title_generate_wordpress": _("Generate WordPress site"),
        "wp_title_wordpress_files": _("WordPress core"),
        "wp_title_wordpress_new_repo": _("WordPress\nexisting repo"),
        "wp_title_wordpress_rollback_db": _("WordPress\ndatabase rollback"),
    }
    _info = {
        "wp_default_files": _("These are the default files from the GitHub repository:"),
        "wp_environment_file_used": _("The following environment file will be used: {file}"),
        "wp_init_git_repo": _("Do you want me to initialize a local Git repository for you?"),
        "wp_required_file_paths_not_found": _("No required file paths were found"),
        "wp_required_file_paths_found": _("The following file paths were found:"),
        "wp_use_default_files": _("Do you want me to use the default ones instead for those missing files?"),
        "wp_wpcli_add_ev": _("Remember to add the path to the PATH or BIN, depending on your operating system."),
        "wp_wpcli_backup_create_before": _("Creating database backup..."),
        "wp_wpcli_config_created_ok": _("File wp-config.php created successfully."),
        "wp_wpcli_core_install_before": _("Preparing wordpress core files to install..."),
        "wp_wpcli_creating_config": _("Creating wp-config.php..."),
        "wp_wpcli_db_create_before":
            _("Creating Wordpress database (by default, user_name and host will be taken from wp_config)"),
        "wp_wpcli_db_import_before": _("Importing database dump from file:"),
        "wp_wpcli_db_export_before": _("Exporting database dump to: {path}"),
        "wp_wpcli_db_query_user_creating": _("Creating database user {user} for host {host}"),
        "wp_wpcli_db_query_user_granting": _("Granting database user {user} for host {host} the following privileges "
                                             "on schema {schema}: {privileges}"),
        "wp_wpcli_db_reset_before": _("Resetting the database (drop and create)..."),
        "wp_wpcli_delete_transients": _("Transients are going to be deleted"),
        "wp_wpcli_downloading": _("Downloading WP-CLI from {url}"),
        "wp_wpcli_downloading_content": _("Downloading WordPress content (default themes and plugins): {content}"),
        "wp_wpcli_downloading_path": _("WordPress core destination path: {path}"),
        "wp_wpcli_downloading_wordpress": _("Downloading WordPress core files version {version}, locale {locale}"),
        "wp_wpcli_downloading_wordpress_ok": _("WordPress core files were successfully downloaded."),
        "wp_wpcli_export": _("Exporting WordPress content to {path}"),
        "wp_wpcli_info": _("Here is the WP-CLI information:"),
        "wp_wpcli_install_ok": _("WP-CLI installation was successful."),
        "wp_wpcli_option_update_before": _("Updating database option {option_name}..."),
        "wp_wpcli_plugin_install_before": _("Installing plugin {plugin_name}..."),
        "wp_wpcli_setting_value_ok": _("Config value {name} set as {value}"),
        "wp_wpcli_theme_install_before": _("Installing wordpress theme {theme_name}"),
        "wp_gulp_build_before": _("Gulp build task has launched for theme {theme_slug}."),
        "wp_gulp_build_after": _("Gulp build task has completed successfully for theme {theme_slug}.")
    }
    _errors = {
        "wp_checking_devops_toolset": _("Checking for devops-toolset in: {path}"),
        "wp_current_version": _("Current version: {version}"),
        "wp_devops_toolset_needs_update": _("devops-toolset needs to be updated."),
        "wp_devops_toolset_not_found": _("devops-toolset not found in required path: {path} "),
        "wp_devops_toolset_obtained": _("devops-toolset has been successfully downloaded on: {path}"),
        "wp_devops_toolset_obtaining": _("Obtaining latest version of devops-toolset from: {resource}"),
        "wp_devops_toolset_up_to_date": _("devops-toolset is up to date."),
        "wp_env_gt1": _("There are more than 1 matching environments in the environments JSON file."),
        "wp_env_not_found": _("Environment not found in the environments JSON file."),
        "wp_environment_name_mandatory": _("environment-name is a mandatory parameter. I cannot continue."),
        "wp_environment_path_mandatory": _("environment-path is a mandatory parameter. I cannot continue."),
        "wp_environment_name_not_found": _("Environment name was not found. I cannot continue."),
        "wp_environment_path_not_found": _("Environment file path was not found. I cannot continue."),
        "wp_file_not_found": _("The following file was not found: {file}"),
        "wp_latest_version": _("Latest version: {version}"),
        "wp_not_dir": _("Path must be a dir, not a file."),
        "wp_non_valid_dir_path": _("Path must be an existent dir."),
        "wp_required_files_mandatory": _("Required files are mandatory. I cannot continue."),
        "wp_required_files_not_found": _("The required files where not found at {path}."),
        "wp_required_files_not_found_detail": _("The following required files where not found at {path}:"),
        "wp_theme_path_not_exist": _("The following theme path does not exist: {path}"),
        "wp_wordpress_path_mandatory": _("wordpress-path is a mandatory parameter. I cannot continue."),
        "wp_wpcli_config_create_err": _("File wp-config.php cannot be created."),
        "wp_wpcli_config_set_value_err": _("Cannot set {name} property as {value}"),
        "wp_wpcli_core_install_error": _("Wordpress installation could not be done."),
        "wp_wpcli_db_export_error": _("Database dump could not be exported due to an error."),
        "wp_wpcli_db_import_error": _("Dump file could not be imported due to an error."),
        "wp_wpcli_db_query_user_creating_err": _("Database user {user} for host {host} could not be created"),
        "wp_wpcli_db_query_user_granting_err": _("Privileges could not be granted to database user {user} for host "
                                                 "{host} on schema {schema}"),
        "wp_wpcli_db_reset_error": _("Database could not be reset due to an error."),
        "wp_wpcli_delete_transients_err": _("Transients could not be deleted"),
        "wp_wpcli_downloading_wordpress_err": _("WordPress core files could not be downloaded."),
        "wp_wpcli_export_err": _("WordPress content could not be exported to {path}"),
        "wp_wpcli_option_update_error":
            _("Database option {option_name} cannot be set to {option_value} due to an error."),
        "wp_wpcli_plugin_install_error": _("Plugin {plugin_name} could not be installed due to an error."),
        "wp_wpcli_theme_install_error": _("Theme {theme_name} could not be installed."),
        "wp_gulp_build_error":
            _("Gulp build task has encountered an error for theme {theme_slug}. "
              "Please check above logs for more details.")
    }
