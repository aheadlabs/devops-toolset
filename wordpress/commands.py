"""wordpress module commands"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Commands(ValueDictsBase):
    """Commands for the wordpress module."""

    # Add your core literal dictionaries here
    _commands = {
        "wpcli_info": "wp --info",
        "wpcli_core_download": "wp core download --version={version} --locale={locale} --path={path} "
                               "{skip_content} {debug_info}",
        "wpcli_db_reset": "wp db reset --path={path} {yes}",
        "wpcli_db_import": "wp db import {file} --path={path}",
        "wpcli_db_delete_transient": "wp transient delete --all --path={path}",
        # "wp_backup_create" pending review when PHP export database method will be done
        "wp_backup_create": "wp backup create --path={path}"
    }
