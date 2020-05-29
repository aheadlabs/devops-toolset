"""devops module literals."""

from core.LiteralsBase import LiteralsBase
from core.app import App

app: App = App()


class Literals(LiteralsBase):
    """Literals for the devops module."""

    # Add your core literal dictionaries here
    _info = {
        "sonar_getting_qg": _("Getting quality gate for branch {branch} (original name)."),
        "sonar_pr_mode": _("Pull request mode: {pull_request}"),
        "sonar_config_file": _("Using {file} as the Sonar* configuration file."),
        "sonar_qg_ok": _("Quality gate succeeded")
    }
    _errors = {
        "sonar_invalid_metric": _("Invalid metric value for {metricKey}: {actualValue} {comparator} {errorThreshold}")
    }