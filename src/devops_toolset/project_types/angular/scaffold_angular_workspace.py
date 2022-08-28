""" This script will scaffold an Angular workspace """

import argparse
import devops_toolset.core.log_setup
import devops_toolset.tools.argument_validators
import devops_toolset.tools.cli
import devops_toolset.tools.git
import json
import logging
import os
import pathlib
from devops_toolset.core.app import App
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.dotnet.commands import Commands as DotnetCommands
from devops_toolset.project_types.dotnet.Literals import Literals as DotnetLiterals

app: App = App()
literals = LiteralsCore([DotnetLiterals])
commands = CommandsCore([DotnetCommands])
template_config: dict = {}


def main(root_path: str, project_name: str, template_name: str, update_global_cli: bool):
    """ Scaffolds a .NET WebAPI solution based on DDDD

    Args:
        root_path: Path to the solution root.
        project_name: Name of the project to scaffold.
        template_name: Name of the scaffolding template.
        update_global_cli: Updates Angular CLI globally before starting the process.
    """

    root_path_obj = pathlib.Path(root_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project-path", action=devops_toolset.tools.argument_validators.PathValidator)
    parser.add_argument("name")
    parser.add_argument("template_name")
    parser.add_argument("--update-global-cli", action="store_true", default=False)
    args, args_unknown = parser.parse_known_args()
    main(args.project_path, args.name, args.template_name, args.update_global_cli)
