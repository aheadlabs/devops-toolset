""" Unit tests for the dotnet/ci_pipeline_kickoff.py module"""


from unittest.mock import patch
import devops_toolset.project_types.dotnet.ci_pipeline_kickoff as sut
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.dotnet.commands import Commands as DotnetCommands
from devops_toolset.project_types.dotnet.Literals import Literals as DotnetLiterals
from devops_toolset.core.app import App

app: App = App()
literals = LiteralsCore([DotnetLiterals])
commands = CommandsCore([DotnetCommands])


# region main()

@patch("devops_toolset.configure.main")
def test_main_calls_devops_toolset_configure_main(configure_main_mock):
    """ Given devops_platform argument, calls configure.main method """
    # Arrange
    devops_platform = 'platform1'
    language = 'en'

    # Act
    sut.main(devops_platform, None, True)

    # Assert
    configure_main_mock.assert_called_with(devops_platform, language)


@patch("devops_toolset.configure.main")
@patch("devops_toolset.tools.http_protocol.get_public_ip_address")
def test_main_calls_get_public_ip_address(get_public_ip_address, main_mock):
    """ Given skip_get_public_ip_address argument, should call get_public_ip_method when false method """
    # Arrange
    # Act
    sut.main(any, None, False)

    # Assert
    get_public_ip_address.assert_called()


@patch("devops_toolset.configure.main")
@patch("devops_toolset.tools.git.set_current_branch_simplified")
def test_main_calls_get_public_ip_address(set_current_branch_mock, main_mock):
    """ Given skip_get_public_ip_address argument, should call get_public_ip_method when false method """
    # Arrange
    current_branch = 'branch1'
    current_branch_variable_name = 'CURRENT_BRANCH'
    # Act
    sut.main(any, current_branch, True)

    # Assert
    set_current_branch_mock.assert_called_with(current_branch, current_branch_variable_name)

# endregion main()
