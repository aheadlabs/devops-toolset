<#
    Generates a WordPress Git repository for local development
#>

[CmdletBinding()]
param (
    # Repository root path
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $RepositoryRoot,

    # WordPress database user password (better pass this value from an environment variable)
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $DbUserPwd
)

# Check for JSON files in /.devops
Write-Host -ForegroundColor DarkYellow "Looking for the necessary JSON files in /.devops"
$local:project_structure_path = (Get-Item "$RepositoryRoot/.devops/*project-structure.json").FullName
$local:site_environments_path = (Get-Item "$RepositoryRoot/.devops/*-site-environments.json").FullName
$local:site_config_path = (Get-Item "$RepositoryRoot/.devops/*-site.json").FullName
if (!$local:project_structure_path -or !$local:site_environments_path -or !$local:site_config_path) {
    Write-Host -ForegroundColor Red "Either *project-structure.json, *site-environments.json or *site.json files are missing in the /.devops directory. Please, fix it before continuing."
    Exit
}
else {
    $local:project_structure_path_filename = [IO.Path]::GetFileName($local:project_structure_path)
    $local:site_environments_path_filename = [IO.Path]::GetFileName($local:site_environments_path)
    $local:site_config_path_filename = [IO.Path]::GetFileName($local:site_config_path)
    Write-Host -ForegroundColor Green "$local:project_structure_path_filename, $local:site_environments_path_filename and $local:site_config_path_filename files are present in the /.devops directory."
}

# Delete /Bootstrap-WordPressRepository.ps1
$local:file_to_remove = "Bootstrap-WordPressRepository.ps1"
if (Test-Path -Path "$RepositoryRoot/$local:file_to_remove") {
    Remove-Item -Path "$RepositoryRoot/$local:file_to_remove"
    Write-Host -ForegroundColor DarkYellow "$local:file_to_remove deleted from /"
}

# Update devops-toolset
if (Test-Path "$RepositoryRoot/.devops/devops-toolset") {
    Write-Host -ForegroundColor DarkYellow "Updating devops-toolset to the latest version..."
    ."$RepositoryRoot/.devops/devops-tools/.tools/Use-DevOpsToolset.ps1"
    Update-DevOpsToolset "$RepositoryRoot/.devops/devops-toolset"    
}
else {
    Write-Host -ForegroundColor DarkYellow "Downloading and expanding devops-toolset from GitHub..."
    (New-Object System.Net.WebClient).DownloadFile("https://github.com/aheadlabs/devops-toolset/archive/master.zip", "$RepositoryRoot/devops-toolset-master.zip")
    [IO.Compression.ZipFile]::ExtractToDirectory("$RepositoryRoot/devops-toolset-master.zip", $RepositoryRoot)
    Move-Item "$RepositoryRoot/devops-toolset-master" "$RepositoryRoot/.devops/devops-toolset"
    Remove-Item "$RepositoryRoot/devops-toolset-master.zip"
    Write-Host -ForegroundColor DarkGreen "devops-toolset downloaded and expanded correctly."
}

# Check project structure
Write-Host -ForegroundColor DarkYellow "Checking project basic structure..."
Invoke-Expression -Command "$RepositoryRoot/.devops/devops-toolset/wordpress/Start-BasicProjectStructure.ps1 -RootPath $RepositoryRoot -ProjectStructurePath $local:project_structure_path"
Write-Host -ForegroundColor DarkGreen "Project structure checked out."

# Check WordPress core files and download them if necessary
Write-Host -ForegroundColor DarkYellow "Checking WordPress core files in the local repository"
if (Test-Path "$RepositoryRoot/wordpress/*.php") {
    # Contains files
    Write-Host -ForegroundColor DarkGreen "WordPress core files are already downloaded. Check them out yourself."
}
else {
    # Does not contain files
    Write-Host -ForegroundColor DarkYellow "Downloading WordPress core files..."
    Invoke-Expression -Command "$RepositoryRoot/.devops/devops-toolset/wordpress/Get-WordPressCoreFiles.ps1 -RootPath '$RepositoryRoot' -EnvironmentConfig '$local:site_environments_path','localhost'"
    Write-Host -ForegroundColor DarkGreen "WordPress core files donloaded."
}

# Create configuration file
Write-Host -ForegroundColor DarkYellow "Creating wp-config.php..."
Invoke-Expression -Command "$RepositoryRoot/.devops/devops-toolset/wordpress/Set-WordPressConfig.ps1 -RootPath $RepositoryRoot -EnvironmentConfig '$local:site_environments_path','localhost' -DbUserPwd $DbUserPwd"
Write-Host -ForegroundColor DarkGreen "wp-config.php file created and set up."

# Done
Write-Host -BackgroundColor DarkGreen -ForegroundColor Black "DONE!!"
