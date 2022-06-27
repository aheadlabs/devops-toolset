"""dotnet module commands"""

from devops_toolset.core.ValueDictsBase import ValueDictsBase
from devops_toolset.core.app import App

app: App = App()


class Commands(ValueDictsBase):
    """ Commands for the project_types/azure module."""

    # Add your dotnet commands dictionaries here
    _commands = {
        "azure_cli_db_mysql_flexible_server_execute":
            "az mysql flexible-server execute -n {server_name} -u {admin_user} -p {admin_password} "
            "-d {database_name} {file_path} {query}",
        "azure_cli_db_mysql_flexible_server_firewall_rule_create":
            "az mysql flexible-server firewall-rule create -n {server_name} -g {resource_group} "
            "-r {rule_name} --start-ip-address {start_ip_address} --end-ip-address {end_ip_address}",
        "azure_cli_db_mysql_flexible_server_firewall_rule_delete":
            "az mysql flexible-server firewall-rule delete -n {server_name} -g {resource_group} "
            "-r {rule_name} -y",
        "azure_cli_extension_list": "az extension list",
        "azure_cli_extension_add": "az extension add --name {name}",
    }
