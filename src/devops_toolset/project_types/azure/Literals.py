"""Azure module literals"""

from devops_toolset.core.app import App
from devops_toolset.core.ValueDictsBase import ValueDictsBase

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the Azure module."""

    _info = {
        "azure_cli_command_output": _("I got this output from the Azure CLI command:\n{output}"),
        "azure_cli_executing_command": _("Executing command => {command}"),
    }
    _errors = {
        "azure_cli_db_mysql_flexible_server_execute_file_query_parameters_error":
            _("You must either pass a SQL file path or SQL query text to be executed.")
    }
