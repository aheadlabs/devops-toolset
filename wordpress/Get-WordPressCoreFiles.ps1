<#
    Downloads last version of WordPress core files
#>

[CmdletBinding()]
Param(
    # Path where WordPress will be downloaded
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [String] $Path,

    # WordPress site config in JSON string format
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [String] $SiteConfig
)

# Parse site configuration
$SiteConfigJson = ConvertFrom-Json $SiteConfig

# Get project root
$ProjectRoot = ((Get-Item $PSScriptRoot).Parent).FullName

# Add tools
."$ProjectRoot\.tools\Convert-VarsToStrings.ps1"

# Add constants
$Constants = Get-Content "$ProjectRoot\wordpress\wordpress-constants.json" | ConvertFrom-Json

# Set/expand variables before using WP CLI
$_wordpress_path = $Path + $Constants.paths.wordpress
$_version = Get-WpCliCoreDownloadVersion $SiteConfigJson.settings.version $Constants.defaults.version
$_locale = Get-WpCliCoreDownloadLocale $SiteConfigJson.settings.locale $Constants.defaults.locale

# Download WordPress without the default themes and plugins
wp core download --version=$_version --locale=$_locale --path=$_wordpress_path --skip-content
