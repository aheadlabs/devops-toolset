<#
    Creates a pre-configured WordPress site locally
#>

[CmdletBinding()]
Param(
    # Root project path
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $DevopsToolsetPath,

    # Root project path
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $RootPath,

    # Environment configuration
    #   - Environment JSON configuration file path
    #   - Environment to be applied
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [array] $EnvironmentConfig,

    # WordPress database user password (better pass this value from an environment variable)
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $DbUserPwd,

    # WordPress admin password (better pass this value from an environment variable)
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $AdminPwd
)

# Get project root
$ProjectRoot = ((Get-Item $PSScriptRoot).Parent).FullName

# Add constants
$Constants = Get-Content "$DevopsToolsetPath\wordpress\wordpress-constants.json" | ConvertFrom-Json

# Set/expand variables
$_wordpress_path = $RootPath + $Constants.paths.wordpress

# Delete all existing files
Remove-Item "$_wordpress_path\*" -Recurse -Force

# Download WordPress
Invoke-Expression -Command "$DevopsToolsetPath\wordpress\Get-WordPressCoreFiles.ps1 -RootPath $RootPath -EnvironmentConfig $EnvironmentConfig"

# Set configuration (wp-config.php)
Invoke-Expression -Command "$DevopsToolsetPath\wordpress\Set-WordPressConfig.ps1 -RootPath $RootPath -EnvironmentConfig $EnvironmentConfig -DbUserPwd $DbUserPwd"

# Install WordPress
Invoke-Expression -Command "$DevopsToolsetPath\wordpress\Install-WordPress.ps1 -RootPath $RootPath -EnvironmentConfig $EnvironmentConfig -AdminPwd $AdminPwd"

# Install WordPress theme
Invoke-Expression -Command "$DevopsToolsetPath\wordpress\Install-WordPressTheme.ps1 -RootPath $RootPath -EnvironmentConfig $EnvironmentConfig"
