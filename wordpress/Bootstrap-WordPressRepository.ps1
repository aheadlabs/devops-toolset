<#
    Generates a WordPress Git repository for local development
#>

[CmdletBinding()]
param (
    # WordPress database user password (better pass this value from an environment variable)
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $DbUserPwd,

    # WordPress admin password (better pass this value from an environment variable)
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $AdminPwd
)

# Reminders. Press any key.
Read-Host "Please place your *site.json, *site-environments.json and *project-structure.json files in the root path before continuing (localhost environment must be present). Press any key..."
Read-Host "Please install MySql and create the database specified in the config file. Press any key..."

# Ask for using the default ones defined in devops-toolset instead => yes/no
Write-Host "Do you want me to use the default ones instead? (y or n)"
$local:key_pressed = $Host.UI.RawUI.ReadKey()
Write-Host ""

# Get repository root
$RepositoryRoot = (Get-Item $PSScriptRoot).FullName

# Download devops-toolset
Write-Host "Downloading and expanding devops-toolset from GitHub..."
(New-Object System.Net.WebClient).DownloadFile("https://github.com/aheadlabs/devops-toolset/archive/master.zip", "$RepositoryRoot/devops-toolset-master.zip")
[IO.Compression.ZipFile]::ExtractToDirectory("$RepositoryRoot/devops-toolset-master.zip", $RepositoryRoot)
Rename-Item "$RepositoryRoot/devops-toolset-master" "$RepositoryRoot/devops-toolset"
Remove-Item "$RepositoryRoot/devops-toolset-master.zip"

# Download default site.json and site-environments.json if needed
if ($local:key_pressed.Character -eq "y"){
    Write-Host "Getting default config files from GitHub..."

    $local:site_environments_path = "$RepositoryRoot/default-site-environments.json"
    $local:site_environments_request = Invoke-WebRequest "https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/wordpress/default-site-environments.json"
    Set-Content $local:site_environments_path $local:site_environments_request.Content

    $local:site_config_path = "$RepositoryRoot/default-localhost-site.json"
    $local:site_config_request = Invoke-WebRequest "https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/wordpress/default-localhost-site.json"
    Set-Content $local:site_config_path $local:site_config_request.Content

    $local:project_structure_path = "$RepositoryRoot/default-wordpress-project-structure.json"
    $local:project_structure_request = Invoke-WebRequest "https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/wordpress/default-wordpress-project-structure.json"
    Set-Content $local:project_structure_path $local:project_structure_request.Content
}

# Set JSON file paths
$local:site_environments_path = (Get-Item "$RepositoryRoot/*-site-environments.json").FullName
$local:site_config_path = (Get-Item "$RepositoryRoot/*-site.json").FullName
$local:project_structure_path = (Get-Item "$RepositoryRoot/*project-structure.json").FullName

# Get *site.json
$local:site_config_json = Get-Content -Path $local:site_config_path -Raw | ConvertFrom-Json

# Create basic project structure
Write-Host "Creating project basic structure..."
Invoke-Expression -Command "$RepositoryRoot/devops-toolset/wordpress/Start-BasicProjectStructure.ps1 -RootPath $RepositoryRoot -ProjectStructurePath $local:project_structure_path"

# Move devops-toolset to /.devops
Write-Host "Moving devops-toolset inside /.devops..."
Move-Item "$RepositoryRoot/devops-toolset" "$RepositoryRoot/.devops/devops-toolset"
Remove-Item "$RepositoryRoot/.devops/.gitkeep"

# Moving themes to /content/themes
Write-Host "Moving themes (<theme>*.zip) to /content/themes..."
if ($local:site_config_json.themes.source_type -eq "zip") {
    $local:theme_with_no_extension = [IO.Path]::GetFileNameWithoutExtension($local:site_config_json.themes.source)
    Move-Item "$RepositoryRoot/$local:theme_with_no_extension*.zip" "$RepositoryRoot/content/themes"
    Remove-Item "$RepositoryRoot/content/themes/.gitkeep"
}

# Download core files, configure site, install site, install theme and install plugins
Write-Host "Downloading WordPress core files..."
Invoke-Expression -Command "$RepositoryRoot/.devops/devops-toolset/wordpress/Get-WordPressCoreFiles.ps1 -RootPath $RepositoryRoot -EnvironmentConfig '$local:site_environments_path','localhost'"
Write-Host "Creating wp-config.php..."
Invoke-Expression -Command "$RepositoryRoot/.devops/devops-toolset/wordpress/Set-WordPressConfig.ps1 -RootPath $RepositoryRoot -EnvironmentConfig '$local:site_environments_path','localhost' -DbUserPwd $DbUserPwd"
Write-Host "Installing WordPress..."
Invoke-Expression -Command "$RepositoryRoot/.devops/devops-toolset/wordpress/Install-WordPress.ps1 -RootPath $RepositoryRoot -EnvironmentConfig '$local:site_environments_path','localhost' -AdminPwd $AdminPwd"
Remove-Item "$RepositoryRoot/database/.gitkeep"
Write-Host "Installing WordPress theme..."
Invoke-Expression -Command "$RepositoryRoot/.devops/devops-toolset/wordpress/Install-WordPressTheme.ps1 -RootPath $RepositoryRoot -EnvironmentConfig '$local:site_environments_path','localhost'"

# Moved *site.json and *site-environments.json and *project-structure.json files to /.devops
Write-Host "Moving configuration (*site*.json and *project-structure.json) files inside /.devops..."
Move-Item "$RepositoryRoot/*site*.json" "$RepositoryRoot/.devops"
Move-Item "$RepositoryRoot/*project-structure.json" "$RepositoryRoot/.devops"

# Delete this script or remind to delete it manually
Read-Host "Remember to delete this script manually. Press any key to finish..."
