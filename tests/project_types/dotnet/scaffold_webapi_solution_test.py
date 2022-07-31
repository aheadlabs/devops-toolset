""" Unit tests for the dotnet/scaffold_webapi_solution.py module"""
import pathlib
from unittest.mock import mock_open, patch

import devops_toolset.project_types.dotnet.scaffold_webapi_solution
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.dotnet.commands import Commands as DotnetCommands
from devops_toolset.project_types.dotnet.Literals import Literals as DotnetLiterals
from devops_toolset.core.app import App

import devops_toolset.project_types.dotnet.scaffold_webapi_solution as sut
from tests.project_types.dotnet.conftest import DotNetData

app: App = App()
literals = LiteralsCore([DotnetLiterals])
commands = CommandsCore([DotnetCommands])

# region main()


@patch("devops_toolset.project_types.dotnet.scaffold_webapi_solution.create_project")
@patch("os.makedirs")
@patch("logging.info")
@patch("devops_toolset.project_types.dotnet.scaffold_webapi_solution.get_project_layers")
@patch("devops_toolset.project_types.dotnet.scaffold_webapi_solution.create_git_repository")
@patch("builtins.open", new_callable=mock_open, read_data=DotNetData.dddd_webapi_template)
@patch("devops_toolset.project_types.dotnet.scaffold_webapi_solution.create_solution")
def test_main_creates_solution(
        create_solution_mock, open_mock, create_git_repository_mock, project_layers_mock,
        logging_mock, makedirs_mock, create_project_mock, dotnetdata):
    """ Given parameters, calls creates a solution """

    # Arrange
    root_path = "pathto/root"
    solution_name = "MySolution"
    template_name = "MyTemplate"
    relational_db_engine = "mysql"

    # Act
    sut.main(root_path, solution_name, template_name, relational_db_engine)

    # Assert
    create_solution_mock.assert_called_with(solution_name, root_path)

# endregion main()

# region add_nuget_package()


@patch("devops_toolset.project_types.dotnet.scaffold_webapi_solution.log")
@patch("devops_toolset.tools.cli.call_subprocess_with_result")
def test_add_nuget_package_calls_subprocess(subprocess_mock, log_mock):
    """ Given parameters, calls subprocess """

    # Arrange
    project_path = "pathto/project"
    package_name = "DotnetRepository|*"

    # Act
    sut.add_nuget_package(project_path, package_name)

    # Assert
    subprocess_mock.assert_called()

# endregion

# region add_project_to_solution()


@patch("devops_toolset.project_types.dotnet.scaffold_webapi_solution.log")
@patch("devops_toolset.tools.cli.call_subprocess_with_result")
def test_add_project_to_solution_calls_subprocess(subprocess_mock, log_mock):
    """ Given parameters, calls subprocess """

    # Arrange
    solution_path = "pathto/solution"
    solution_name = "MySolution"
    project_path = "pathto/project"
    project_name = "MyProject"

    # Act
    sut.add_project_to_solution(solution_path, solution_name, project_path, project_name)

    # Assert
    subprocess_mock.assert_called()

# endregion

# region add_project_reference()


@patch("devops_toolset.project_types.dotnet.scaffold_webapi_solution.log")
@patch("devops_toolset.tools.cli.call_subprocess_with_result")
def test_add_project_reference_calls_subprocess(subprocess_mock, log_mock):
    """ Given parameters, calls subprocess """

    # Arrange
    project_path = "pathto/project"
    reference_path = "pathto/reference"

    # Act
    sut.add_project_reference(project_path, reference_path)

    # Assert
    subprocess_mock.assert_called()

# endregion

# region add_unit_tests()


@patch("devops_toolset.project_types.dotnet.scaffold_webapi_solution.add_project_to_solution")
@patch("devops_toolset.project_types.dotnet.scaffold_webapi_solution.dotnet_new")
def test_add_unit_tests_creates_test_project(dotnet_new_mock, add_project_mock, dotnetdata):
    """ Given pass unit tests, creates new test project """

    # Arrange
    devops_toolset.project_types.dotnet.scaffold_webapi_solution.template_config = \
        dotnetdata.template_config_pass_unit_tests
    project_config = dotnetdata.project_config
    path = "pathto/project"
    project_layers = {}

    # Act
    sut.add_unit_tests(project_config, path, project_layers)

    # Assert
    dotnet_new_mock.assert_called()


@patch("devops_toolset.project_types.dotnet.scaffold_webapi_solution.add_project_to_solution")
@patch("devops_toolset.project_types.dotnet.scaffold_webapi_solution.dotnet_new")
def test_add_unit_tests_adds_created_project_to_solution(dotnet_new_mock, add_project_mock, dotnetdata):
    """ Given pass unit tests, adds new created project to solution """

    # Arrange
    devops_toolset.project_types.dotnet.scaffold_webapi_solution.template_config = \
        dotnetdata.template_config_pass_unit_tests
    project_config = dotnetdata.project_config
    path = "pathto/project"
    project_layers = {}

    # Act
    sut.add_unit_tests(project_config, path, project_layers)

    # Assert
    add_project_mock.assert_called()


@patch("devops_toolset.project_types.dotnet.scaffold_webapi_solution.add_project_to_solution")
@patch("devops_toolset.project_types.dotnet.scaffold_webapi_solution.dotnet_new")
def test_add_unit_tests_does_not_add_test_project(dotnet_new_mock, add_project_mock, dotnetdata):
    """ Given skip_unit_tests, does not create a new test project """

    # Arrange
    devops_toolset.project_types.dotnet.scaffold_webapi_solution.template_config = \
        dotnetdata.template_config_skip_unit_tests
    project_config = dotnetdata.project_config
    path = "pathto/project"
    project_layers = {}

    # Act
    sut.add_unit_tests(project_config, path, project_layers)

    # Assert
    dotnet_new_mock.assert_not_called()
    add_project_mock.assert_not_called()

# endregion

# region create_git_repository()


@patch("devops_toolset.tools.git.add_gitignore_exclusion")
@patch("pathlib.Path.touch")
@patch("devops_toolset.tools.git.git_init")
def test_create_git_repository_initializes_repository_and_adds_exclusions(
        git_init_mock, touch_mock, git_exclusion_mock, dotnetdata):
    """ Given path, initializes repository """

    # Arrange
    devops_toolset.project_types.dotnet.scaffold_webapi_solution.template_config = \
        dotnetdata.template_config_git_exclusions
    path = pathlib.Path("pathto/project")

    # Act
    sut.create_git_repository(path)

    # Assert
    git_init_mock.assert_called()
    touch_mock.assert_called()
    git_exclusion_mock.assert_called()

# endregion

# region create_git_repository()


@patch("devops_toolset.tools.git.add_gitignore_exclusion")
@patch("pathlib.Path.touch")
@patch("devops_toolset.tools.git.git_init")
def test_create_git_repository_initializes_repository_and_adds_exclusions(
        git_init_mock, touch_mock, git_exclusion_mock, dotnetdata):
    """ Given path, initializes repository """

    # Arrange
    devops_toolset.project_types.dotnet.scaffold_webapi_solution.template_config = \
        dotnetdata.template_config_git_exclusions
    path = pathlib.Path("pathto/project")

    # Act
    sut.create_git_repository(path)

    # Assert
    git_init_mock.assert_called()
    touch_mock.assert_called()
    git_exclusion_mock.assert_called()

# endregion
