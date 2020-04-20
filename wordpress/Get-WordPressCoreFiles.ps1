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

# Set/expand variables before using WP CLI
$_version = $SiteConfigJson.settings.version
$_locale = $SiteConfigJson.settings.locale

# Set latest version if not provided
if ([String]::IsNullOrEmpty($_version)) {
    $_version = 'latest'
}

# Set en_US locale if not provided
if ([String]::IsNullOrEmpty($_locale)) {
    $_locale = 'en_US'
}

# Download WordPress without the default themes and plugins
wp core download --version=$_version --locale=$_locale --path=$Path --skip-content
