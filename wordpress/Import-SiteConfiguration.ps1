<#
    Imports the site.json file
#>

[CmdletBinding()]
Param(
    # Path to site.json file
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [String] $Path
)

# Log the purpose of this script
Write-Host "######## NOTE ########"
Write-Host "This script imports the configuration of the site from a JSON file that matches the WordPress site schema at http://dev.aheadlabs.com/schemas/json/wordpress-site-schema.json"
Write-Host "Make sure your path meets this requirement."
Write-Host "######################"

# Get project root
$ProjectRoot = ((Get-Item $PSScriptRoot).Parent).FullName

# Add platform specific logic
."$ProjectRoot\.devops-platform-specific\Add-EnvironmentVariables-$DevOpsPlatformCode.ps1"

# Parse site configuration
$SiteConfigJson = Get-Content -Path $Path -Raw

# Create key-value pairs
$EnvironmentVariables = [System.Collections.Generic.List[hashtable]]::new()
$EnvironmentVariables.Add(@{key="SiteConfigJson";value=$SiteConfigJson})

# Create environment variables
CreateEnvironmentVariables $EnvironmentVariables
LogEnvironmentVariables $EnvironmentVariables
