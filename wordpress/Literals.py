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
        "wp_wpcli_add_ev": _("Remember to add the path to the PATH or BIN, depending on your operating system.")
    }
    _errors = {
        "wp_wordpress_path_mandatory": _("wordpress-path is a mandatory parameter. I cannot continue."),
        "wp_environment_path_mandatory": _("environment-path is a mandatory parameter. I cannot continue."),
        "wp_environment_name_mandatory": _("environment-name is a mandatory parameter. I cannot continue."),
        "wp_not_dir": _("Path must be a dir, not a file.")
    }
