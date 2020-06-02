"""wordpress module literals"""

from core.LiteralsBase import LiteralsBase
from core.app import App

app: App = App()


class Literals(LiteralsBase):
    """Literals for the wordpress module."""

    # Add your core literal dictionaries here
    _info = {
        "wp_wpcli_downloading": _("Downloading WP-CLI from {url}")
    }
    _errors = {
        "wp_wordpress_path_mandatory": _("wordpress-path is a mandatory parameter. I cannot continue."),
        "wp_environment_path_mandatory": _("environment-path is a mandatory parameter. I cannot continue."),
        "wp_environment_name_mandatory": _("environment-name is a mandatory parameter. I cannot continue."),
        "wp_not_dir": _("Path must be a dir, not a file.")
    }
