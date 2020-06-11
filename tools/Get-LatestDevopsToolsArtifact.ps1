<#
    Downloads the latest artifact of devops-toolset
#>

[CmdletBinding()]
Param(
    # Destination path for the artifact
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $DestinationPath,
    
    # If true the artifact is unzipped
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [bool] $Unzip,

    # DevOps platform code (see \.devops-platform-specific\README.md)
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [String] $DevOpsPlatformCode
)

# Get project root
$ProjectRoot = ((Get-Item $PSScriptRoot).Parent).FullName

# Add tools
."$ProjectRoot\.devops-platform-specific\Use-RestApiBuilds-$DevOpsPlatformCode.ps1"
."$ProjectRoot\.devops-platform-specific\Use-RestApiArtifacts-$DevOpsPlatformCode.ps1"

# Add constants
[xml]$ProjectData = (Get-Content -Path "$ProjectRoot\project.xml" -Raw)

# Get the last build id
[int]$_build_id = Get-LastBuildId -Organization $ProjectData.project.organization -Project $ProjectData.project.name

# Get the artifact download URL
[string]$_artifact_download_url = Get-ArtifactDownloadUrl -Organization $ProjectData.project.organization -Project $ProjectData.project.name -BuildId $_build_id -ArtifactName $ProjectData.project.name

# Set/expand variables
$_artifact_destination_path = $DestinationPath + "/" + (Get-ArtifactFileNameFromQuerystring -Url $_artifact_download_url)

# Download artifact zip file
(New-Object System.Net.WebClient).DownloadFile($_artifact_download_url, $_artifact_destination_path)

# Unzip file
if ($Unzip) {
    Expand-RealArtifactFile -ZipFilePath $_artifact_destination_path
}
