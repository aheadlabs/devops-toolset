<#
    Installs a theme and its child theme if it is available.

    Possible sources for the theme are:
    - zip: local zipped file (child theme must be in the same directory)
    - wordpress: installed from wordpress.org/themes
    - url: installed from a custom url (must be publicly accessible)
#>

[CmdletBinding()]
Param(
    # Root path of the WordPress implementation
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $RootPath,
    
    # WordPress site config in JSON string format
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $SiteConfigPath
)

# Get project root
$ProjectRoot = ((Get-Item $PSScriptRoot).Parent).FullName

# Add tools
."$ProjectRoot\.tools\Import-Files.ps1"

# Parse site configuration
$SiteConfigJson = Import-JsonFile $SiteConfigPath

# Add constants
$Constants = Get-Content "$ProjectRoot\wordpress\wordpress-constants.json" | ConvertFrom-Json

# Set/expand variables before using WP CLI
$_themes_source_type = $SiteConfigJson.themes.source_type
$_themes_source = $SiteConfigJson.themes.source
$_themes_has_child = $SiteConfigJson.themes.has_child
$_wordpress_path = $RootPath + $Constants.paths.wordpress
$_database_path = $RootPath + $Constants.paths.database
$_themes_path = $RootPath + $Constants.paths.content.themes + "/" + $_themes_source
$_database_theme_dump_path = $_database_path + "/" + $SiteConfigJson.database.dumps.theme

# Install and activate WordPress theme
wp theme install $_themes_path --path=$_wordpress_path --activate
if ($_themes_has_child) {
    $_child_theme_path = [IO.Path]::GetDirectoryName($_themes_path) + "/" + [IO.Path]::GetFileNameWithoutExtension($_themes_path) + "-child" + [IO.Path]::GetExtension($_themes_path)
    wp theme install $_child_theme_path --path=$_wordpress_path --activate
}

# Backup database
wp db export $_database_theme_dump_path --extended-insert --path=$_wordpress_path
