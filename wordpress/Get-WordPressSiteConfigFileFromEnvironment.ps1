<#
    Gets the site configuration based on the environment
#>

function Get-WordPressSiteConfigFileFromEnvironment {
    [CmdletBinding()]
    Param(
        # Environment configuration
        #   - Environment JSON configuration file path
        #   - Environment to be applied
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [array] $EnvironmentConfig
    )

    # Get project root
    $ProjectRoot = ((Get-Item $PSScriptRoot).Parent).FullName

    # Add tools
    ."$ProjectRoot\.tools\Import-Files.ps1"

    # Parse environments configuration
    $EnvironmentsConfigJson = Import-JsonFile $EnvironmentConfig[0]

    # Get environment
    $_environment = $EnvironmentsConfigJson.environments | Where-Object { $_.name -eq $EnvironmentConfig[1] }

    # Parse environment configuration file
    $_config_file_path = [IO.Path]::Combine([IO.Path]::GetDirectoryName($EnvironmentConfig[0]), $_environment.configuration_file)
    return Import-JsonFile $_config_file_path
}
