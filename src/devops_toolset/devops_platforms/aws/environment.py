"""Environment-related functionality for Aws"""

from enum import Enum
from devops_toolset.core.app import App
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.devops_platforms.Literals import Literals as CommonLiterals
from devops_toolset.devops_platforms.aws.Literals import Literals as AwsLiterals
from devops_toolset.project_types.linux.commands import Commands as LinuxCommands
import devops_toolset.devops_platforms.common
import logging
import os

app: App = App()
literals = LiteralsCore([CommonLiterals, AwsLiterals])
linux_commands = CommandsCore([LinuxCommands])


class ResultType(Enum):
    """Result types for a task"""
    success = "Succeeded"
    partial_success = "SucceededWithIssues"
    fail = "Failed"


def create_environment_variables(key_value_pairs: dict):
    """Creates environment variables

    Args:
        key_value_pairs: Key-value pair dictionary
    """

    for key, value in key_value_pairs.items():
        logging.info(literals.get("platform_created_ev").format(key=key, value=value))
        os.environ[key] = value


def end_task(result_type: ResultType):
    """Ends the current task

    Args:
        result_type: Result type of the task
    """

    if result_type == ResultType.fail:
        raise EnvironmentError()


def get_platform_variable_keys() -> list:
    """Gets all keys for the environment variables defined by default in the
    platform. More info at:
    https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-variables.html#reference-variables-list

    Returns
        List with all variables
    """

    return [
        "codepipeline.PipelineExecutionId", "SourceVariables.ImageDigest", "SourceVariables.ImageTag",
        "SourceVariables.ImageURI", "SourceVariables.RegistryId", "SourceVariables.RepositoryName",
        "DeployVariables.OperationId", "DeployVariables.StackSetId", "DeployVariables.StackName",
        "SourceVariables.AuthorDate", "SourceVariables.BranchName", "SourceVariables.CommitId",
        "SourceVariables.CommitMessage", "SourceVariables.CommitterDate", "SourceVariables.AuthorDate",
        "SourceVariables.BranchName", "SourceVariables.CommitId", "SourceVariables.CommitMessage",
        "SourceVariables.ConnectionArn", "SourceVariables.FullRepositoryName", "SourceVariables.CommitterDate",
        "SourceVariables.CommitUrl", "SourceVariables.ETag", "SourceVariables.VersionId", "BuildVariables.EnvVar",
        "TestVariables.testRunId"
    ]


def log_environment_variables(platform_keys: list):
    """Logs all environment variables for this platform and process.

    Args:
        platform_keys: List of platform variables.
    """

    spaces: int = len(max(platform_keys, key=len)) + 5

    for environment_variable in platform_keys:
        logging.info(literals.get("environment_variable_log").format(
            key=str(environment_variable).ljust(spaces, "."),
            value=os.environ.get(environment_variable)
        ))


if __name__ == "__main__":
    help(__name__)
