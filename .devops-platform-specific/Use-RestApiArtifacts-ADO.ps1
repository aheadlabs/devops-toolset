<#
    Gets the id for the latest build for a project or $null if there are no builds
#>
function Get-ArtifactDownloadUrl {
    [CmdletBinding()]
    param (
        # Azure DevOps organization
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$Organization,

        # Azure DevOps project
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$Project,

        # Build id where the artifact has been published
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [int]$BuildId,

        # Artifact name
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$ArtifactName
    )
    
    $_artifact = Invoke-RestMethod -Method Get -Uri "https://dev.azure.com/$Organization/$Project/_apis/build/builds/$BuildId/artifacts?artifactName=$ArtifactName"
    
    # Return the artifact download URL
    return $_artifact.resource.downloadUrl
}

<#
    Gets the file name from the artifact REST API querystring
#>
function Get-ArtifactFileNameFromQuerystring {
    param (
        # REST API URL for downloading the artifact
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$Url
    )

    if ($Url -match 'artifactName=(?<name>[^&]*).*format=(?<extension>[^&]*)') {
        $_file_name = $Matches["name"]
        $_file_extension = $Matches["extension"]
        return "$_file_name.$_file_extension"
    }
    else {
        return $null
    }
}

<#
    Extracts a the real artifact zip file inside the downloaded zip file
#>
function Expand-RealArtifactFile {
    param (
        # Path to the downloaded zip file
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$ZipFilePath
    )
    
    # Get name with no extension (equivalent to project and artifact names)
    $_file_name_without_extension = [IO.Path]::GetFileNameWithoutExtension($ZipFilePath)
    $_file_extension = [IO.Path]::GetExtension($ZipFilePath)
    $_file_directory_path = [IO.Path]::GetDirectoryName($ZipFilePath)
    $_real_artifact_file_name = "$_file_name_without_extension-latest$_file_extension"
    $_real_artifact_file_path = [IO.Path]::Combine($_file_directory_path, $_real_artifact_file_name)
    $_destination_directory = "$_file_directory_path/$_file_name_without_extension"
    
    # Read file and extract real artifact from the inside
    $ZipFile = [IO.Compression.ZipFile]::OpenRead($ZipFilePath)
    $ZipFile.Entries | Where-Object { $_.FullName -like "$_file_name_without_extension/$_file_name_without_extension-*$_file_extension" } | ForEach-Object {
        [IO.Compression.ZipFileExtensions]::ExtractToFile($_, $_real_artifact_file_path, $true)
    }
    $ZipFile.Dispose()

    # Expand real artifact
    [IO.Compression.ZipFile]::ExtractToDirectory($_real_artifact_file_path, $_destination_directory)

    # Delete artifact zip files
    Remove-Item "$_file_directory_path\$_file_name_without_extension*$_file_extension" -Force
}
