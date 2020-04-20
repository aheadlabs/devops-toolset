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

# Set/expand variables before using WP CLI
$_version = Get-WpCliCoreDownloadVersion $SiteConfigJson.settings.version
$_locale = Get-WpCliCoreDownloadLocale $SiteConfigJson.settings.locale

# Download WordPress without the default themes and plugins
wp core download --version=$_version --locale=$_locale --path=$Path --skip-content
