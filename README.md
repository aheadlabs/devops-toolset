# DevOps Toolset
![Build status](https://img.shields.io/azure-devops/build/aheadlabs/DevOps-toolset/6)
![Repo size](https://img.shields.io/github/repo-size/aheadlabs/devops-toolset)
![Top language](https://img.shields.io/github/languages/top/aheadlabs/devops-toolset)
![License](https://img.shields.io/github/license/aheadlabs/devops-toolset)  
![Last commit](https://img.shields.io/github/last-commit/aheadlabs/devops-toolset/dev)
![Release date](https://img.shields.io/github/release-date/aheadlabs/devops-toolset)
![GitHub SemVer tag](https://img.shields.io/github/v/tag/aheadlabs/devops-toolset)
<br>

General purpose DevOps-related scripts and tools.<br><br>
![Logo](.media/devops-toolset-logo.png)

# Getting Started
Reference the package in your pipeline to have these tools available:<br>
1. Download the package from the [feed](https://dev.azure.com/aheadlabs/DevOps-toolset/_packaging?_a=feed&feed=devops-toolset). Click on "Connect to feed" for more information<br>
![Connect to feed](.media/connect-to-feed.png)
2. Unzip the package to a directory<br>
e.g.: /devops-toolset
3. Call the scripts taking /code as the base path.<br>
i.e.: /wordpress/SetConfigValues.ps1 for /code/wordpress/SetConfigValues.ps1

# File structure
| Directory / file | Description |
| -- | -- |
| /.devops | Contains pipeline definitions for the project |
| /.media | Contains media files |
| /code | Contains scripts and tools in different formats, grouped by categories |
| /project.xml | Project description and project version |

# Troubleshooting
| Problem | Solution |
| -- | -- |
| Can't execute PowerShell script because of the policy | Take a look at https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies
| Can't execute PowerShell script in Linux | Make sure you installed or have access to PowerShell Core distribution |
| PowerSHell execution policy related problems **in development** | Execute this command as admin (not for production use):<br>`Set-ExecutionPolicy -ExecutionPolicy Bypass` |
