"""wordpress module literals"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the wordpress module."""

    _titles = {
        "wp_title_wordpress_files": _("WordPress core"),
        "wp_title_wordpress_new_repo": _("WordPress\nexisting repo"),
        "wp_title_wordpress_rollback_db": _("WordPress\ndatabase rollback"),
    }
    _info = {
        "wp_wpcli_db_reset_before": _("Resetting the database (drop and create)..."),
        "wp_wpcli_db_reset_error": _("Database could not be reset due to an error."),
        "wp_wpcli_db_import_before": _("Importing database dump from file:"),
        "wp_wpcli_db_import_error": _("Dump file could not be imported due to an error."),
        "wp_wpcli_downloading": _("Downloading WP-CLI from {url}"),
        "wp_wpcli_install_ok": _("WP-CLI installation was successful."),
        "wp_wpcli_info": _("Here is the WP-CLI information:"),
        "wp_wpcli_add_ev": _("Remember to add the path to the PATH or BIN, depending on your operating system."),
        "wp_wpcli_downloading_wordpress": _("Downloading WordPress core files version {version}, locale {locale}"),
        "wp_wpcli_downloading_content": _("Downloading WordPress content (default themes and plugins): {content}"),
        "wp_wpcli_downloading_path": _("WordPress core destination path: {path}"),
        "wp_wpcli_downloading_wordpress_ok": _("WordPress core files were successfully downloaded."),
        "wp_default_files": _("These are the default files from the GitHub repository:"),
        "wp_use_default_files": _("Do you want me to use the default ones instead for those missing files?"),
        "wp_wpcli_delete_transients": _("Transients are going to be deleted"),
        "wp_backup_create": _("Dump done successfully"),
        "wp_init_git_repo": _("Do you want me to initialize a local Git repository for you?"),
        "wp_wpcli_creating_config": _("Creating wp-config.php..."),
        "wp_wpcli_config_created_ok": _("File wp-config.php created successfully."),
        "wp_wpcli_setting_value_ok": _("Config value {name} set as {value}"),
    }
    _errors = {
        "wp_wordpress_path_mandatory": _("wordpress-path is a mandatory parameter. I cannot continue."),
        "wp_environment_path_mandatory": _("environment-path is a mandatory parameter. I cannot continue."),
        "wp_environment_name_mandatory": _("environment-name is a mandatory parameter. I cannot continue."),
        "wp_required_files_mandatory": _("Required files are mandatory. I cannot continue."),
        "wp_not_dir": _("Path must be a dir, not a file."),
        "wp_non_valid_dir_path": _("Path must be an existent dir."),
        "wp_env_not_found": _("Environment not found in the environments JSON file."),
        "wp_env_gt1": _("There are more than 1 matching environments in the environments JSON file."),
        "wp_wpcli_downloading_wordpress_err": _("WordPress core files could not be downloaded."),
        "wp_required_files_not_found_detail": _("The following required files where not found at {path}:"),
        "wp_required_files_not_found": _("The required files where not found at {path}."),
        "wp_wpcli_delete_transients_err": _("Transients could not be deleted"),
        "wp_err_backup_create": _("Dump could not be done"),
        "wp_wpcli_config_create_err": _("File wp-config.php cannot be created."),
        "wp_wpcli_config_set_value_err": _("Cannot set {name} property as {value}")
    }