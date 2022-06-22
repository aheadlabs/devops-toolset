"""This script kicks off a CI pipeline for .NET projects"""

import argparse
import devops_toolset.configure
import devops_toolset.tools.cli
import devops_toolset.tools.git
import devops_toolset.tools.http_protocol

from devops_toolset.core.app import App
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.dotnet.Literals import Literals as DotnetLiterals

app: App = App()
literals = LiteralsCore([DotnetLiterals])


def main(devops_platform: [str, None],
         current_branch: [str, None],
         skip_get_public_ip_address: bool,
         **kwargs):
    """Kick off the CI pipeline

    Args:
        devops_platform: Name of the DevOps platform to be set.
        current_branch: Name of the current branch
        skip_get_public_ip_address: Skips getting pulic IP address if present.
            simplified if present.
        kwargs: Platform specific arguments
    """

    # Set DevOps current platform
    if devops_toolset is not None:
        devops_toolset.configure.main(devops_platform, "en")

    # Get public IP address
    if not skip_get_public_ip_address:
        devops_toolset.tools.http_protocol.get_public_ip_address()

    # Get current branch simplified
    if current_branch is not None:
        devops_toolset.tools.git.set_current_branch_simplified(current_branch, "CURRENT_BRANCH")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("devops-platform", default=None)
    parser.add_argument("--current-branch", action="store_true", default=False)
    parser.add_argument("--skip-get-public-ip-address", action="store_true", default=False)
    args, args_unknown = parser.parse_known_args()
    kwargs = {}
    for kwarg in args_unknown:
        splited = str(kwarg).split("=")
        kwargs[splited[0]] = splited[1]

    devops_toolset.tools.cli.print_title(literals.get("dotnet_ci_title_pipeline_kickoff"))
    main(args.devops_platform,
         args.current_branch,
         args.skip_get_public_ip_address,
         **kwargs)
