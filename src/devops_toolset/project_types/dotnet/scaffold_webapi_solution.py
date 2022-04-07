""" This script will scaffold a DDDD WebAPI solution in .NET """

import argparse
from typing import List

import devops_toolset.core.log_setup
import devops_toolset.tools.argument_validators
import devops_toolset.tools.cli
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
# TODO Use global template_config everywhere to remove parameters in functions

def main(root_path: str, solution_name: str, template_name: str, relational_db_engine: str, minimal_api: bool,
         skip_unit_tests: bool, flat_structure: bool):
    """ Scaffolds a .NET WebAPI solution based on DDDD

    Args:
        root_path: Path to the solution root.
        solution_name: Name of the solution to scaffold.
        template_name: Name of the scaffolding template.
    """

    root_path_obj = pathlib.Path(root_path)

    # Create solution
    create_solution(solution_name, root_path)

    # Read configuration template
    with open(get_configuration(template_name), "r") as config_file:
        global template_config
        template_config = json.load(config_file)

    # Get a list of projects-layers key-value pairs
    project_layers: dict = get_project_layers(template_config, solution_name)

    # Create projects
    for layer in template_config["layers"]:
        logging.info(literals.get('dotnet_cli_starting_layer').format(layer=layer["name"]))
        layer_path = pathlib.Path.joinpath(root_path_obj, layer["name"])
        os.makedirs(layer_path)

        for project in layer["projects"]:
            project["solution_path"] = root_path
            project["solution_name"] = solution_name
            project["solution_folder"] = layer["name"]
            project["project_path"] = layer_path
            project["project_name"] = f"{project['solution_name']}{project['name']}"
            if "framework" not in project:
                project["framework"] = template_config["default_frameworks"][project["template"]]
            create_project(project, str(layer_path), project_layers)


def add_nuget_package(project_path: str, package_name: str, source: str = "https://api.nuget.org/v3/index.json"):
    """Adds a package to a project.

    Args:
        project_path: Path to the project that adds the reference.
        package_name: NuGet package name.
        source: Source feed to get the package from.
    """

    package_info: list[str] = package_name.split("|")

    command: str = commands.get("dotnet_add_package").format(
        project_path=project_path,
        package=package_info[0],
        version=package_info[1],
        nuget_feed=source
    )
    result: str = devops_toolset.tools.cli.call_subprocess_with_result(command)

    # TODO Refactor logging to a function and apply everywhere
    if result is not None:
        logging.debug(command)
        logging.info(literals.get('dotnet_cli_log').format(log=result))
        logging.info(literals.get('dotnet_cli_project_package_added').format(
            project=project_path,
            package=package_name
        ))
    else:
        logging.info(literals.get('dotnet_cli_project_package_exists').format(
            package=package_name,
            project=project_path
        ))


def add_project_to_solution(solution_path: str, solution_name: str, project_path: str, project_name: str,
                            solution_folder: str = None):
    """Adds a project to the solution

    Args:
        solution_path: Path to the solution file
        solution_name: Name of the solution without extension
        project_path: Path to the project file
        project_name: Name of the project file without extension
        solution_folder: Solution folder (virtual) name
    """

    # TODO Move all dotnet commands to functions outside from this script
    command: str = commands.get('dotnet_sln_add').format(
        solution_path=solution_path,
        solution_folder=solution_folder,
        project_path=pathlib.Path.joinpath(pathlib.Path(project_path), project_name)
    )

    result: str = devops_toolset.tools.cli.call_subprocess_with_result(command)

    if result is not None:
        logging.debug(command)
        logging.info(literals.get('dotnet_cli_log').format(log=result))
        logging.info(literals.get('dotnet_cli_solution_project_added').format(
            project=project_name,
            solution=solution_name
        ))
    else:
        logging.info(literals.get('dotnet_cli_solution_project_not_added').format(
            project=project_name,
            solution=solution_name
        ))


def add_project_reference(project_path: str, reference_path: str):
    """Adds a reference to a project.

    Args:
        project_path: Path to the project that adds the reference.
        reference_path: Path to the project to be added as a reference.
    """

    command: str = commands.get("dotnet_add_reference").format(
        project_path=project_path,
        reference_path=reference_path
    )
    result: str = devops_toolset.tools.cli.call_subprocess_with_result(command)

    if result is not None:
        logging.debug(command)
        logging.info(literals.get('dotnet_cli_log').format(log=result))
        logging.info(literals.get('dotnet_cli_project_reference_added').format(
            project=project_path,
            referenced=reference_path
        ))
    else:
        logging.info(literals.get('dotnet_cli_project_exists').format(
            project=project_path,
            referenced=reference_path
        ))


def add_unit_tests(project_config: dict, path: str, project_layers: dict):
    """Adds unit tests to a project

    Args:
        project_config: Project data configuration
        path: Path where to create the project
        project_layers: List of projects-layers key-value pairs"""

    if project_config["unit-test-eligible"]:
        path_obj = pathlib.Path(path)
        project_name = f'{project_config["project_name"]}.Tests'
        framework = template_config["default_frameworks"]["xunit"]
        dotnet_new('xunit', project_name, str(pathlib.Path.joinpath(path_obj, project_name)), framework)


def create_project(project_config: dict, path: str, project_layers: dict):
    """Creates a project for a specific template

    Args:
        project_config: Project data configuration
        path: Path where to create the project
        project_layers: List of projects-layers key-value pairs
    """

    path_obj = pathlib.Path(path)

    # Create project
    # TODO use dotnet_new()
    if "framework" in project_config:
        command = commands.get('dotnet_new_framework').format(
            template=project_config['template'],
            name=project_config["project_name"],
            path=pathlib.Path.joinpath(path_obj, project_config["project_name"]),
            framework=project_config['framework']
        )
    else:
        command = commands.get('dotnet_new').format(
            template=project_config['template'],
            name=project_config["project_name"],
            path=pathlib.Path.joinpath(path_obj, project_config["project_name"])
        )

    result: str = devops_toolset.tools.cli.call_subprocess_with_result(command)

    if result is not None:
        logging.debug(command)
        logging.info(literals.get('dotnet_cli_log').format(log=result))
        logging.info(literals.get('dotnet_cli_project_created').format(name=project_config["project_name"]))
    else:
        logging.info(literals.get('dotnet_cli_project_exists').format(name=project_config["project_name"]))

    # Add project to solution
    add_project_to_solution(project_config["solution_path"], project_config["solution_name"],
                            project_config["project_path"], project_config["project_name"],
                            project_config["solution_folder"])

    full_project_path: str = pathlib.Path.joinpath(project_config['project_path'], project_config['project_name'])

    # Add references to other projects
    for reference in project_config["references"]:
        reference_project_path = str(pathlib.Path.joinpath(
            pathlib.Path(project_config["solution_path"]),
            project_layers[f"{project_config['solution_name']}{reference}"],
            f"{project_config['solution_name']}{reference}"
        ))
        add_project_reference(full_project_path, reference_project_path)

    # Add NuGet packages
    for package in project_config["packages"]:
        add_nuget_package(full_project_path, package)

    # Add unit tests
    add_unit_tests(project_config, path, project_layers)


def create_solution(name: str, path: str):
    """Creates a solution in the specified path

    Args:
          name: Name of the solution to be created
          path: Path where to create the solution
    """

    result: str = devops_toolset.tools.cli.call_subprocess_with_result(commands.get('dotnet_new').format(
        template='sln',
        name=name,
        path=path
    ))

    if result is not None:
        logging.info(literals.get('dotnet_cli_log').format(log=result))
        logging.info(literals.get('dotnet_cli_solution_created').format(name=name))
    else:
        logging.info(literals.get('dotnet_cli_solution_exists').format(name=name))


def dotnet_new(template: str, name: str, path: str, framework: [str, None]):
    """Creates a new .NET project using .NET CLI.

    Args:
        template: Project template name.
        name: Project name.
        path: Path to the project to be created.
        framework: Framework
    """
    if framework is not None:
        command = commands.get('dotnet_new_framework').format(
            template=template,
            name=name,
            path=path,
            framework=framework
        )
    else:
        command = commands.get('dotnet_new').format(
            template=template,
            name=name,
            path=path,
        )

    result: str = devops_toolset.tools.cli.call_subprocess_with_result(command)

    if result is not None:
        logging.debug(command)
        logging.info(literals.get('dotnet_cli_log').format(log=result))
        logging.info(literals.get('dotnet_cli_project_created').format(name=name))
    else:
        logging.info(literals.get('dotnet_cli_project_exists').format(name=name))


def get_configuration(template_name: str):
    """Gets the configuration file based on the template name.

    Args:
        template_name: Configuration template name.
    """
    return f"./scaffolding_templates/{template_name}-template.json"


def get_project_layers(template_config: dict, solution_name: str):
    """Returns a dict with all project folders.

    Args:
        template_config: Template configuration.
        solution_name: Name of the solution.
    """

    project_layers: dict = {}
    for layer in template_config["layers"]:
        for project in layer["projects"]:
            project_layers[f"{solution_name}{project['name']}"] = layer["name"]

    return project_layers


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project-path", action=devops_toolset.tools.argument_validators.PathValidator)
    parser.add_argument("name")
    parser.add_argument("template_name")
    parser.add_argument("--relational-db-engine", default="mysql")
    parser.add_argument("--minimal-api", action="store_true", default=False)
    parser.add_argument("--skip-unit-tests", action="store_true", default=False)
    parser.add_argument("--flat-structure", action="store_true", default=False)
    args, args_unknown = parser.parse_known_args()
    main(args.project_path, args.name, args.template_name, args.relational_db_engine, args.minimal_api,
         args.skip_unit_tests, args.flat_structure)
