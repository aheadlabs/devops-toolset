<#
    Gets the name of the active WordPress theme
#>
function Get-ActiveWordPressThemeName {
    param (
        # Root path of the WordPress site
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string] $RootPath
    )
    
    $local:theme_list_json = (wp theme list --format=json --path=$RootPath) | ConvertFrom-Json
    $local:active_theme = $local:theme_list_json | Where-Object { $_.status -eq "active" }
    $local:active_theme_name = $local:active_theme.name

    return $local:active_theme_name
}

<#
    Gets the name of the parent theme if this is a child one or the same string otherwise
#>
function Get-ParentWordPressThemeName {
    param (
        # Theme slug (parent or child)
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string] $ThemeSlug
    )
    
    return $ThemeSlug.Replace("-child", "")
}

<#
    Gets the relative path to the themes directory from the WordPress installation path
#>
function Get-ThemesDirectoryRelativePath {
    [CmdletBinding()]
    param (
        # Root path of the WordPress site
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string] $RootPath,

        # Root path of the WordPress site
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [psobject] $Constants,

        # Root path of the WordPress site
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [psobject] $SiteConfig,

        # Theme slug
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string] $ThemeSlug
    )
    
    $local:wordpress_path = $Constants.paths.wordpress
    if ("$local:wordpress_path".StartsWith("/")) {
        $local:wordpress_path = "$local:wordpress_path".Remove(0, 1)
    }

    $local:site_url = $SiteConfig.settings.site_url

    $local:content_url = $SiteConfig.settings.content_url

    if ("$local:content_url".Contains($local:site_url)) {
        $local:content_path = "$local:content_url".Replace($local:site_url, [string]::Empty)
    }
    else {
        $local:content_path = $local:content_url
    }
    if ("$local:content_path".StartsWith("/")) {
        $local:content_path = "$local:content_path".Remove(0, 1)
    }

    $local:themes_directory_relative_path = [IO.Path]::Combine("$local:wordpress_path", "$local:content_path", "themes", "$ThemeSlug/")
    $local:themes_directory_relative_path = "$local:themes_directory_relative_path".Replace("\","/")
    $local:themes_directory_relative_path = "$local:themes_directory_relative_path".Replace("//","/")
    return $local:themes_directory_relative_path    
}

$_constants = Get-Content "D:\Source\_aheadlabs\devops-toolset\wordpress\wordpress-constants.json" | ConvertFrom-Json
$_config = Get-Content "D:\Source\_tecdev\tecdev.es\.devops\localhost-tecdev-site.json" | ConvertFrom-Json
Get-ThemesDirectoryRelativePath "D:\Source\_tecdev\tecdev.es\wordpress" $_constants $_config "theblogger"
