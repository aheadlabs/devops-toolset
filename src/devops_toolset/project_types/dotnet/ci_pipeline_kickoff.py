"""This script kicks off a CI pipeline for .NET projects"""

import argparse
import devops_toolset.configure
import devops_toolset.tools.cli

from devops_toolset.core.app import App
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.dotnet.Literals import Literals as DotnetLiterals
from devops_toolset.project_types.dotnet.utils import get_csproj_project_version
from devops_toolset.tools.git import get_current_branch_simplified
from devops_toolset.tools.http_protocol import get_public_ip_address

app: App = App()
literals = LiteralsCore([DotnetLiterals])


def main(devops_platform: [str, None],
         csproj_path: [str, None],
         current_branch: [str, None],
         skip_get_public_ip_address: bool):
    """Kick off the CI pipeline

    Args:
        devops_platform: Name of the DevOps platform to be set.
        csproj_path: Path to the .csproj file.
        current_branch: Name of the current branch
        skip_get_public_ip_address: Skips getting public IP address if present.
            simplified if present.
    """

    # Set DevOps current platform
    if devops_platform is not None:
        devops_toolset.configure.main(devops_platform, "en")

    # Get project version from .csproj file
    if csproj_path is not None:
        _ = devops_toolset.project_types.dotnet.utils.get_csproj_project_version(csproj_path)

    # Get current branch simplified
    if current_branch is not None:
        _ = devops_toolset.tools.git.get_current_branch_simplified(current_branch)

    # Get public IP address
    if not skip_get_public_ip_address:
        _ = devops_toolset.tools.http_protocol.get_public_ip_address()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("devops_platform", default=None)
    parser.add_argument("--csproj-path", default=None)
    parser.add_argument("--current-branch", default=None)
    parser.add_argument("--skip-get-public-ip-address", action="store_true", default=False)
    args, args_unknown = parser.parse_known_args()

    devops_toolset.tools.cli.print_title(literals.get("dotnet_ci_title_pipeline_kickoff"))
    main(args.devops_platform,
         args.csproj_path,
         args.current_branch,
         args.skip_get_public_ip_address)
