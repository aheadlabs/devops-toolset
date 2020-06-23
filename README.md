# DevOps Toolset
[![Last commit](https://img.shields.io/github/last-commit/aheadlabs/devops-toolset)](https://github.com/aheadlabs/devops-toolset/commits/)
[![Build status](https://img.shields.io/azure-devops/build/aheadlabs/DevOps-toolset/6)](https://dev.azure.com/aheadlabs/DevOps-toolset/_build?definitionId=6&_a=summary)
[![Release](https://img.shields.io/azure-devops/release/aheadlabs/1485b494-712b-4941-9b9a-d177484d1727/1/1)](https://dev.azure.com/aheadlabs/DevOps-toolset/_release?_a=releases&view=mine&definitionId=1)  
[![Sonar quality gate](https://img.shields.io/sonar/quality_gate/devops-toolset?server=https%3A%2F%2Fsonarcloud.io)](https://sonarcloud.io/dashboard?id=devops-toolset)
[![Sonar coverage](https://img.shields.io/sonar/coverage/devops-toolset?server=https%3A%2F%2Fsonarcloud.io)](https://img.shields.io/sonar/coverage/devops-toolset?server=https%3A%2F%2Fsonarcloud.io)
[![Sonar tech debt](https://img.shields.io/sonar/tech_debt/devops-toolset?server=https%3A%2F%2Fsonarcloud.io)](https://sonarcloud.io/component_measures?id=devops-toolset&metric=sqale_index&view=list)
[![Sonar violations](https://img.shields.io/sonar/violations/devops-toolset?format=long&server=https%3A%2F%2Fsonarcloud.io)](https://sonarcloud.io/dashboard?id=devops-toolset)<!--[![Sonar documented API density](https://img.shields.io/sonar/public_documented_api_density/devops-toolset?server=https%3A%2F%2Fsonarcloud.io)]()-->  
[![GitHub SemVer tag](https://img.shields.io/github/v/tag/aheadlabs/devops-toolset)](https://github.com/aheadlabs/devops-toolset/tags)
[![Repo size](https://img.shields.io/github/repo-size/aheadlabs/devops-toolset)](https://github.com/aheadlabs/devops-toolset)
[![Top language](https://img.shields.io/github/languages/top/aheadlabs/devops-toolset)](https://github.com/aheadlabs/devops-toolset)
[![License](https://img.shields.io/github/license/aheadlabs/devops-toolset)](https://github.com/aheadlabs/devops-toolset/blob/master/LICENSE)  
[![Liberapay](https://img.shields.io/liberapay/receives/ahead-labs?logo=liberapay)](https://es.liberapay.com/ahead-labs/)
[![Donate Liberapay](https://img.shields.io/badge/donate-Liberapay-yellow)](https://liberapay.com/ahead-labs/donate)
[![Donate PayPal](https://img.shields.io/badge/donate-PayPal-yellow.svg)](https://www.paypal.me/aheadlabs)  

Everything than can be automated, must be automated!<br><br>
![Logo](.media/devops-toolset-logo-216x100px.png)

# Getting Started

## Description

This project contains general purpose, DevOps-related, scripts and tools.

## Prerequisites

You need Python 3.8.2+ installed on your machine. Please follow the instructions on the [Python web site](https://www.python.org/downloads/).

## How to use

Reference the package in your pipeline to have these tools available:<br>
1. Download the package from the [feed](https://dev.azure.com/aheadlabs/DevOps-toolset/_packaging?_a=feed&feed=devops-toolset). Click on "Connect to feed" for more information<br>
![Connect to feed](.media/connect-to-feed.png)
2. Unzip the package to a directory<br>
e.g.: /devops-toolset
3. Add this directory to the PYTHONPATH environment variable.

## Running the tests

### Unit tests

To run the unit tests you need to install [pytest from PyPI](https://pypi.org/project/pytest/). You can do so by executing the following command:

```
pip install pytest
```

Then, run the tests using the following command at the project's root path:
```
pytest
```

# File structure
| Directory / file | Description |
| -- | -- |
| /.devops | Contains pipeline definitions for the project |
| /.devops-platform-specific | Contains platform-specific code |
| /.media | Contains media files |
| /.tools | Contains helpers and tools used in scripts |
| /\<category\> | Contains scripts and tools in different formats, grouped by categories |
| /project.xml | Project description and project version |

# WordPress tools
This repository relies on WP CLI for WordPress automation. Please refer to [WP-CLI handbook](https://make.wordpress.org/cli/handbook/) for more information and installation instructions.

# Troubleshooting
| Problem | Solution |
| -- | -- |
| Can't execute PowerShell script because of the policy | Take a look at https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies
| Can't execute PowerShell script in Linux | Make sure you installed or have access to PowerShell Core distribution |
| PowerSHell execution policy related problems **in development** | Execute this command as admin (not for production use):<br>`Set-ExecutionPolicy -ExecutionPolicy Bypass` |
