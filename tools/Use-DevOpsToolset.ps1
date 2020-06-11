function Get-DevOpsToolset {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true)]
        [string] $DestinationPath
    )
    
    $local:save_as = "devops-toolset-master.zip"
    (New-Object System.Net.WebClient).DownloadFile("https://github.com/aheadlabs/devops-toolset/archive/master.zip", "$DestinationPath/$local:save_as")
    [IO.Compression.ZipFile]::ExtractToDirectory("$DestinationPath/$local:save_as", $DestinationPath)
    Rename-Item "$RepositoryRoot/devops-toolset-master" "$RepositoryRoot/devops-toolset"
    Remove-Item "$DestinationPath/$local:save_as"
}

function Update-DevOpsToolset {
    param (
        [Parameter(Mandatory=$true)]
        [string] $ToolsetPath
    )
    
    $local:is_latest_version = Compare-DevOpsToolsetVersion $ToolsetPath

    if (-Not $local:is_latest_version) {
        # Delete current version
        Remove-Item -Path $ToolsetPath -Recurse -Force

        # Download latest version
        Get-DevOpsToolset $ToolsetPath
    }
}

function Compare-DevOpsToolsetVersion {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true)]
        [string] $ToolsetPath
    )
    
    $local:current_version = ([xml](Get-Content "$ToolsetPath/project.xml")).project.version
    $local:latest_version = ([xml]((Invoke-WebRequest "https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/project.xml").Content)).project.version

    return ($local:current_version -eq $local:latest_version)
}