"""wordpress module literals"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the wordpress module."""

    # Add your core literal dictionaries here
    _info = {
        "wp_wpcli_downloading": _("Downloading WP-CLI from {url}"),
        "wp_wpcli_install_ok": _("WP-CLI installation was successful."),
        "wp_wpcli_info": _("Here is the WP-CLI information:"),
        "wp_wpcli_add_ev": _("Remember to add the path to the PATH or BIN, depending on your operating system."),
        "wp_wpcli_downloading_wordpress": _("Downloading WordPress core files version {version}, locale {locale}"),
        "wp_wpcli_downloading_content": _("Downloading WordPress content (default themes and plugins): {content}"),
        "wp_wpcli_downloading_path": _("WordPress core destination path: {path}"),
        "wp_wpcli_downloading_wordpress_ok": _("WordPress core files were successfully downloaded.")
    }
    _errors = {
        "wp_wordpress_path_mandatory": _("wordpress-path is a mandatory parameter. I cannot continue."),
        "wp_environment_path_mandatory": _("environment-path is a mandatory parameter. I cannot continue."),
        "wp_environment_name_mandatory": _("environment-name is a mandatory parameter. I cannot continue."),
        "wp_not_dir": _("Path must be a dir, not a file."),
        "wp_env_not_found": _("Environment not found in the environments JSON file."),
        "wp_env_gt1": _("There are more than 1 matching environments in the environments JSON file."),
        "wp_wpcli_downloading_wordpress_err": _("WordPress core files could not be downloaded.")
    }
