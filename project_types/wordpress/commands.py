"""wordpress module commands"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Commands(ValueDictsBase):
    """Commands for the wordpress module."""

    # Add your wordpress literal dictionaries here
    _commands = {
        "wpcli_info": "wp --info",
        "wpcli_core_download": "wp core download --version={version} --locale={locale} --path={path} "
                               "{skip_content} {debug_info}",
        "wpcli_core_install": "wp core install --path={path} --url={url} --title=\"{title}\" --admin_user={admin_user} "
                              "--admin_email={admin_email} {admin_password} {skip_email} {debug_info}",
        "wpcli_db_export": "wp db export \"{core_dump_path}\" --path={path} --extended-insert=false {debug_info}",
        "wpcli_db_reset": "wp db reset --path={path} {yes} {debug_info}",
        "wpcli_db_import": "wp db import {file} --path={path}",
        "wpcli_db_delete_transient": "wp transient delete --all --path={path}",
        "wpcli_config_create": "wp config create --path={path} --dbhost={db_host} --dbname={db_name} "
                               "--dbuser={db_user} --dbpass={db_pass} --dbprefix={db_prefix} --dbcharset={db_charset} "
                               "--dbcollate={db_collate} --force {skip_check} {debug_info}",
        "wpcli_config_set": "wp config set {name} {value} {raw} --type={type} --path={path} {debug_info}",
        "wpcli_option_update": "wp option update {option_name} \"{option_value}\" --path={path} {debug_info}"
    }
