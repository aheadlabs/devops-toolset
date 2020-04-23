<#
    Downloads last version of WordPress core files
#>

[CmdletBinding()]
Param(
    # Root project path
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [String] $RootPath,

    # Path to the WordPress site JSON config file
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [String] $SiteConfigPath
)

# Get project root
$ProjectRoot = ((Get-Item $PSScriptRoot).Parent).FullName

# Add tools
."$ProjectRoot\.tools\Import-Files.ps1"
."$ProjectRoot\.tools\Convert-VarsToStrings.ps1"

# Add constants
$Constants = Get-Content "$ProjectRoot\wordpress\wordpress-constants.json" | ConvertFrom-Json

# Parse site configuration
$SiteConfigJson = Import-JsonFile $SiteConfigPath

# Set/expand variables before using WP CLI
$_wordpress_path = $RootPath + $Constants.paths.wordpress
$_version = Get-WpCliCoreDownloadVersion $SiteConfigJson.settings.version $Constants.defaults.version
$_locale = Get-WpCliCoreDownloadLocale $SiteConfigJson.settings.locale $Constants.defaults.locale

# Download WordPress without the default themes and plugins and delete .gitkeep file
wp core download --version=$_version --locale=$_locale --path=$_wordpress_path --skip-content
if (Test-Path "$_wordpress_path/.gitkeep") { Remove-Item "$_wordpress_path/.gitkeep" -Force }
