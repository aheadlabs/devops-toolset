<#
    This script parses the project.xml file and creates environment variables with its content
#>

[CmdletBinding()]
Param(
    # DevOps platform code (see \.devops-platform-specific\README.md)
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [String] $DevOpsPlatformCode,

    # Project root (defaults to this project's root path if $null)
    [String] $ProjectRootPath
)

# Set variables
$ProjectFile = "project.xml"

# Get project root
if ($ProjectRootPath) {
    $ProjectRoot = $ProjectRootPath
}
else {
    $ProjectRoot = ((Get-Item $PSScriptRoot).Parent).FullName
}

# Add tools
."$ProjectRoot\.tools\Convert-ToJson.ps1"

# Add platform specific logic
."$ProjectRoot\.devops-platform-specific\Add-EnvironmentVariables-$DevOpsPlatformCode.ps1"

# Read the project file
[XML]$Content = (Get-Content -Path "$ProjectRoot\$ProjectFile" -Raw)

# Convert to JSON key-value pairs
$EnvironmentVariables = (Convert-XmlToJsonKeyValuePairs -XmlDocument $Content) | ConvertFrom-Json

# Create environment variables
CreateEnvironmentVariables $EnvironmentVariables
LogEnvironmentVariables $EnvironmentVariables
