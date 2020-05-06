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
Read-Host "Please place your localhost-site.json and site-environments.json files in the root path before continuing (localhost environment must be present). Press any key..."
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

# Create basic project structure
Write-Host "Creating project basic structure..."
Invoke-Expression -Command "$RepositoryRoot/devops-toolset/wordpress/Start-BasicProjectStructure.ps1 -RootPath $RepositoryRoot -ProjectStructurePath $RepositoryRoot/devops-toolset/wordpress/wordpress-project-structure.json"

# Move devops-toolset to /.devops
Write-Host "Moving devops-toolset inside /.devops..."
Move-Item "$RepositoryRoot/devops-toolset" "$RepositoryRoot/.devops/devops-toolset"
Remove-Item "$RepositoryRoot/.devops/.gitkeep"

# Download default site.json and site-environments.json if needed
if ($local:key_pressed.Character -eq "y"){
    Write-Host "Getting default config files from GitHub..."

    $local:site_environments_path = "$RepositoryRoot/default-site-environments.json"
    $local:site_environments_request = Invoke-WebRequest "https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/wordpress/default-site-environments.json"
    Set-Content $local:site_environments_path $local:site_environments_request.Content

    $local:site_config_path = "$RepositoryRoot/default-localhost-site.json"
    $local:site_config_request = Invoke-WebRequest "https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/wordpress/default-localhost-site.json"
    Set-Content $local:site_config_path $local:site_config_request.Content
}

# Moved site.json and site-environments.json to /.devops
Write-Host "Moving configuration (*site*.json) files inside /.devops..."
Move-Item "$RepositoryRoot/*site*.json" "$RepositoryRoot/.devops"

# set JSON file paths
$local:site_environments_path = (Get-Item "$RepositoryRoot/.devops/*-site-environments.json").FullName
$local:site_config_path = (Get-Item "$RepositoryRoot/.devops/*-site.json").FullName

# Download core files, configure site, install site, install theme and install plugins
Write-Host "Downloading WordPress core files..."
Invoke-Expression -Command "$RepositoryRoot/.devops/devops-toolset/wordpress/Get-WordPressCoreFiles.ps1 -RootPath $RepositoryRoot -EnvironmentConfig '$local:site_environments_path','localhost'"
Write-Host "Creating wp-config.php..."
Invoke-Expression -Command "$RepositoryRoot/.devops/devops-toolset/wordpress/Set-WordPressConfig.ps1 -RootPath $RepositoryRoot -EnvironmentConfig '$local:site_environments_path','localhost' -DbUserPwd $DbUserPwd"
Write-Host "Installing WordPress..."
Invoke-Expression -Command "$RepositoryRoot/.devops/devops-toolset/wordpress/Install-WordPress.ps1 -RootPath $RepositoryRoot -EnvironmentConfig '$local:site_environments_path','localhost' -AdminPwd $AdminPwd"

# Delete this script or remind to delete it manually
Read-Host "Remember to delete this script manually. Press any key to finish..."