<#
    Runs the standard WordPress installation process and dumps the database to a file:
    - Creates the database and tables (specified at wp-config.php)
    - Sets site's title and description
    - Dumps the database to a SQL file
#>

[CmdletBinding()]
Param(
    # Root path of the WordPress implementation
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $RootPath,
    
    # Environment configuration
    #   - Environment JSON configuration file path
    #   - Environment to be applied
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [array] $EnvironmentConfig,
    
    # WordPress admin password (better pass this value from an environment variable)
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $AdminPwd
)

# Get project root
$ProjectRoot = ((Get-Item $PSScriptRoot).Parent).FullName

# Add tools
."$ProjectRoot\.tools\Import-Files.ps1"
."$ProjectRoot\wordpress\Get-WordPressSiteConfigFileFromEnvironment.ps1"

# Parse site configuration
$SiteConfigJson = Get-WordPressSiteConfigFileFromEnvironment -EnvironmentConfig $EnvironmentConfig

# Get project root
$ProjectRoot = ((Get-Item $PSScriptRoot).Parent).FullName

# Add tools
."$ProjectRoot\.tools\Convert-VarsToStrings.ps1"

# Add constants
$Constants = Get-Content "$ProjectRoot\wordpress\wordpress-constants.json" | ConvertFrom-Json

# Set/expand variables before using WP CLI
$_debug_info = Convert-WpCliDebug -DebugInfo $SiteConfigJson.wp_cli.debug
$_wordpress_path = $RootPath + $Constants.paths.wordpress
$_database_path = $RootPath + $Constants.paths.database
$_database_core_dump_path = $_database_path + "/" + $SiteConfigJson.database.dumps.core
$_title = $SiteConfigJson.settings.title
$_description = $SiteConfigJson.settings.description
$_site_url = $SiteConfigJson.settings.site_url
$_admin_user = $SiteConfigJson.settings.admin.user
$_admin_email = $SiteConfigJson.settings.admin.email
$_admin_password = Convert-WpCliCoreInstallAdminPassword $AdminPwd
$_skip_email = Convert-WpCliCoreInstallSkipEmail $SiteConfigJson.settings.admin.skip_email

# Install WordPress
wp db drop --yes --path=$_wordpress_path $_debug_info
wp db create --path=$_wordpress_path $_debug_info
wp core install --path=$_wordpress_path --url=$_site_url --title=$_title --admin_user=$_admin_user --admin_email=$_admin_email $_admin_password $_skip_email $_debug_info
wp option update blogdescription $_description --path=$_wordpress_path $_debug_info

# Backup database
wp db export $_database_core_dump_path --extended-insert=false --path=$_wordpress_path $_debug_info
