# Platform specific scripts
In the subdirectories, like `azure-devops`, you can find scripts that are designed specifically for a determined DevOps platform.<br>
Feel free to add your platform's directory and specific scripts.

## Settings
In order to use platform-specific scripts you should set the platform value at `/core/settings.json` file. Azure Devops is the default platform.

## Naming policy
Please, use lowered non-spaced notation for directories and the same script and function names for all platforms.

\<platformname\><br>  
e.g.:
* azuredevops
    * /environment.py => create_environment_variables()
* jenkins
    * /environment.py => create_environment_variables()
* travisci
    * /environment.py => create_environment_variables()

If it is not possible to create any functionality in the new platform, please create the related functions anyway and log to the stdout why it can't be implemented.
