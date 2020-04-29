<#
    Downloads last version of WordPress core files
#>

[CmdletBinding()]
Param(
    # Root project path
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $RootPath,

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
."$ProjectRoot\.tools\Convert-VarsToStrings.ps1"
."$ProjectRoot\wordpress\Get-WordPressSiteConfigFileFromEnvironment.ps1"

# Add constants
$Constants = Get-Content "$ProjectRoot\wordpress\wordpress-constants.json" | ConvertFrom-Json

# Parse site configuration
$SiteConfigJson = Get-WordPressSiteConfigFileFromEnvironment -EnvironmentConfig $EnvironmentConfig

# Set/expand variables before using WP CLI
$_wordpress_path = $RootPath + $Constants.paths.wordpress
$_version = Get-WpCliCoreDownloadVersion $SiteConfigJson.settings.version $Constants.defaults.version
$_locale = Get-WpCliCoreDownloadLocale $SiteConfigJson.settings.locale $Constants.defaults.locale
$_skip_content = Convert-WpCliCoreDownloadSkipContent $SiteConfigJson.settings.skip_content_download

# Download WordPress without the default themes and plugins and delete .gitkeep file
wp core download --version=$_version --locale=$_locale --path=$_wordpress_path $_skip_content
if (Test-Path "$_wordpress_path/.gitkeep") { Remove-Item "$_wordpress_path/.gitkeep" -Force }
