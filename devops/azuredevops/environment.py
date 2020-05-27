"""Environment-related functionality for Azure DevOps"""

from core.app import App
import sys
from enum import Enum

app: App = App()


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
        sys.stdout.write(f"##vso[task.setvariable variable={key}]{value}\n")


def end_task(result_type: ResultType, description: str):
    """Ends the current task

    Args:
        result_type: Result type of the task
        description: Explanation for task ending
    """

    sys.stdout.write(f"##vso[task.complete result={result_type.value};]{description}\n")


if __name__ == "__main__":
    help(__name__)
