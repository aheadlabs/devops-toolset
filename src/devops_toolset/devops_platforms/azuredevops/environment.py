"""Environment-related functionality for Azure DevOps"""

from devops_toolset.core.app import App
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.devops_platforms.Literals import Literals as CommonLiterals
from devops_toolset.devops_platforms.azuredevops.Literals import Literals as AzureDevOpsLiterals
from enum import Enum
import devops_toolset.devops_platforms.common
import logging
import sys

app: App = App()
literals = LiteralsCore([CommonLiterals, AzureDevOpsLiterals])


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
        sys.stdout.write(f"##vso[task.setvariable variable={key}]{value}\n")


def end_task(result_type: ResultType):
    """Ends the current task

    Args:
        result_type: Result type of the task
        description: Explanation for task ending
    """

    sys.stdout.write(f"##vso[task.complete result={result_type.value};]DONE\n")


def get_platform_variable_keys() -> list:
    """Gets all keys for the environment variables defined by default in the
    platform. More info at:
    https://docs.microsoft.com/en-us/azure/devops/pipelines/build/variables

    Returns
        List with all variables
    """

    return [
        "System.AccessToken", "System.Debug", "Agent.BuildDirectory", "Agent.ContainerMapping", "Agent.HomeDirectory",
        "Agent.Id", "Agent.JobName", "Agent.JobStatus", "Agent.MachineName", "Agent.Name", "Agent.OS",
        "Agent.OSArchitecture", "Agent.TempDirectory", "Agent.ToolsDirectory", "Agent.WorkFolder",
        "Build.ArtifactStagingDirectory", "Build.BuildId", "Build.BuildNumber", "Build.BuildUri",
        "Build.BinariesDirectory", "Build.ContainerId", "Build.DefinitionName", "Build.DefinitionVersion",
        "Build.QueuedBy", "Build.QueuedById", "Build.Reason", "Build.Repository.Clean", "Build.Repository.LocalPath",
        "Build.Repository.ID", "Build.Repository.Name", "Build.Repository.Provider", "Build.Repository.Tfvc.Workspace",
        "Build.Repository.Uri", "Build.RequestedFor", "Build.RequestedForEmail", "Build.RequestedForId",
        "Build.SourceBranch", "Build.SourceBranchName", "Build.SourcesDirectory", "Build.SourceVersion",
        "Build.SourceVersionMessage", "Build.StagingDirectory", "Build.Repository.Git.SubmoduleCheckout",
        "Build.SourceTfvcShelveset", "Build.TriggeredBy.BuildId", "Build.TriggeredBy.DefinitionId",
        "Build.TriggeredBy.DefinitionName", "Build.TriggeredBy.BuildNumber", "Build.TriggeredBy.ProjectID",
        "Common.TestResultsDirectory", "Pipeline.Workspace", "Environment.Name", "Environment.Id",
        "Environment.ResourceName", "Environment.ResourceId", "Strategy.Name", "Strategy.CycleName",
        "System.CollectionId", "System.CollectionUri", "System.DefaultWorkingDirectory", "System.DefinitionId",
        "System.HostType", "System.JobAttempt", "System.JobDisplayName", "System.JobId", "System.JobName",
        "System.PhaseAttempt", "System.PhaseDisplayName", "System.PhaseName", "System.StageAttempt",
        "System.StageDisplayName", "System.StageName", "System.PullRequest.IsFork", "System.PullRequest.PullRequestId",
        "System.PullRequest.PullRequestNumber", "System.PullRequest.SourceBranch",
        "System.PullRequest.SourceRepositoryURI", "System.PullRequest.TargetBranch",
        "System.TeamFoundationCollectionUri", "System.TeamProject", "System.TeamProjectId", "TF_BUILD",
        "Checks.StageAttempt"
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
            value=devops_toolset.devops_platforms.common.echo_environment_variable(f"$(\"{environment_variable}\")")
        ))


if __name__ == "__main__":
    help(__name__)
