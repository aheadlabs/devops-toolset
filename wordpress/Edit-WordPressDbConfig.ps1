<#
    Sets all database configuration parameters in wp-config.php
#>

[CmdletBinding()]
Param(
    # Root project
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
    [string] $DbUserPwd
)

# Get project root
$ProjectRoot = ((Get-Item $PSScriptRoot).Parent).FullName

# Add tools
."$ProjectRoot\.tools\Convert-VarsToStrings.ps1"
."$ProjectRoot\wordpress\Get-WordPressSiteConfigFileFromEnvironment.ps1"

# Add constants
$Constants = Get-Content "$ProjectRoot\wordpress\wordpress-constants.json" | ConvertFrom-Json

# Parse site configuration
$SiteConfigJson = Get-WordPressSiteConfigFileFromEnvironment -EnvironmentConfig $EnvironmentConfig

# Set/expand variables before using WP CLI
$_debug_info = Convert-WpCliDebug -DebugInfo $SiteConfigJson.wp_cli.debug
$_wordpress_path = $RootPath + $Constants.paths.wordpress
$_host = $SiteConfigJson.database.host
$_name = $SiteConfigJson.database.name
$_user = $SiteConfigJson.database.user
$_prefix = $SiteConfigJson.database.prefix
$_charset = $SiteConfigJson.database.charset
$_collate = $SiteConfigJson.database.collate

# Edit database parameters
# More info at https://wordpress.org/support/article/editing-wp-config-php/
wp config set DB_HOST $_host --type=constant --path=$_wordpress_path $_debug_info
wp config set DB_NAME $_name --type=constant --path=$_wordpress_path $_debug_info
wp config set DB_USER $_user --type=constant --path=$_wordpress_path $_debug_info
wp config set DB_PASSWORD $DbUserPwd --type=constant --path=$_wordpress_path $_debug_info
wp config set DB_CHARSET $_charset --type=constant --path=$_wordpress_path $_debug_info
wp config set DB_COLLATE $_collate --type=constant --path=$_wordpress_path $_debug_info
wp config set table_prefix $_prefix --type=variable --path=$_wordpress_path $_debug_info
