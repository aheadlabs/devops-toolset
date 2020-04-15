<#
    Downloads last version of WordPress core files
#>

[CmdletBinding()]
Param(
    # Path where WordPress will be downloaded
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [String] $Path,

    # WordPress version to be downloaded. latest (default) and nightly are valid
    [Parameter (Mandatory=$false)]
    [String] $Version,

    # WordPress locale. Default is en_US
    [Parameter (Mandatory=$false)]
    [String] $Locale
)

# Set latest version if not provided
if ([String]::IsNullOrEmpty($Version) {
    $Version = 'latest'
}

# Set en_US locale if not provided
if ([String]::IsNullOrEmpty($Locale) {
    $Version = 'en_US'
}

# Download WordPress without the default themes and plugins
wp core download --version=$Version --locale=$Locale --path=$Path --skip-content
