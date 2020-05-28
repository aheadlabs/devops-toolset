"""sonarcloud.io / SonarQube tools"""

from core.app import App
import sys
import requests
import configparser
import logging
from tools.xcoding64 import encode
from devops.constants import Urls
from tools.git import simplify_branch_name

app: App = App()
platform_specific = app.load_platform_specific("environment")


def get_quality_gate_status(properties_file_path: str, token: str, branch: str = None, pull_request: bool = False):
    """Gets the status of the quality gate of a project

    Args:
        properties_file_path: Path to sonar-project.properties file. Keys
            sonar.projectKey and sonar.organization are mandatory.
        token: SonarCloud token used for authentication
        branch: Git branch name to get the quality gate for. If None, master
            will be assumed.
        pull_request: True if the analysis was originated by a pull request.
    """

    token_base64 = encode(f"{token}:")
    basic_auth_token = f"Basic {token_base64}"
    headers = {"Authorization": basic_auth_token}

    message = _("Getting quality gate for branch {branch} (original name).")
    logging.info(str(message).format(branch=branch))
    message = _("Pull request mode: {pull_request}")
    logging.info(str(message).format(pull_request=pull_request))
    branch_segment = generate_branch_segment(branch, pull_request)

    message = _("Using {file} as the Sonar* configuration file.")
    logging.info(str(message).format(file=properties_file_path))
    sonar_url, sonar_project_key, sonar_organization = read_sonar_properties_file(properties_file_path)

    url = f"{sonar_url}{Urls.SONAR_QUALITY_GATE_PARTIAL_URL}{sonar_project_key}{branch_segment}"

    response = requests.get(url, headers=headers)
    quality_gate_data = response.json()

    if quality_gate_data["projectStatus"]["status"] == "OK":
        print(_("Quality gate succeeded"))
    else:
        for condition in quality_gate_data["projectStatus"]["conditions"]:

            if condition["status"] == "ERROR":
                error = _("Invalid metric value for {metricKey}: {actualValue} {comparator} {errorThreshold}")
                sys.stdout.write(str(error + "\n").format(
                    metricKey=condition["metricKey"],
                    actualValue=condition["actualValue"],
                    comparator=condition["comparator"],
                    errorThreshold=condition["errorThreshold"]))

        platform_specific.end_task(platform_specific.ResultType.fail)


def read_sonar_properties_file(path: str):
    """Reads a sonar-project.properties file

    It adds a temporary dummy section to be correctly parsed by configParser

    Args:
        path: Path to the sonar-project.properties file

    Returns:
        Tuple containing url, projectKey, organization
    """

    with open(path, "r") as file:
        data = f"[temp]\n{file.read()}"

    properties_file_parser = configparser.ConfigParser()
    properties_file_parser.read_string(data)

    sonar_url = properties_file_parser.get("temp", "sonar.host.url")
    sonar_project_key = properties_file_parser.get("temp", "sonar.projectKey")
    sonar_organization = properties_file_parser.get("temp", "sonar.organization")

    return sonar_url, sonar_project_key, sonar_organization


def generate_branch_segment(branch: str = None, pull_request: bool = False):
    """Generates the branch segment or the URL used to request the quality gate
    status

    Args:
        branch: Git branch. If None, master will be assumed.
        pull_request: True if the analysis was originated by a pull request
    """

    if branch is None:
        branch = "master"

    if pull_request:
        branch = simplify_branch_name(branch)
        return f"&pullRequest={branch}"
    else:
        return f"&branch={branch}"


if __name__ == "__main__":
    help(__name__)
