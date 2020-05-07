<#
    Creates an opinionated basic structure for a WordPress project.
#>

[CmdletBinding()]
Param(
    # Root project path where the structure should be generated
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $RootPath,

    # Project structure file path
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string] $ProjectStructurePath
)

function Get-DefaultContent {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true)]
        [psobject] $Item
    )

    if (Get-Member -InputObject $Item -Name "default_content" -MemberType NoteProperty) {
        return $Item.default_content
    }

    if (Get-Member -InputObject $Item -Name "default_content_from_file" -MemberType NoteProperty) {
        return Get-Content -Path $Item.default_content_from_file
    }

    if (Get-Member -InputObject $Item -Name "default_content_from_url" -MemberType NoteProperty) {
        return (Invoke-WebRequest $Item.default_content_from_url).Content
    }

    return $null
}
function Add-Item {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true)]
        [psobject] $Item,

        [Parameter(Mandatory=$true)]
        [string] $BasePath
    )

    # Set paths
    $Item | Add-Member -MemberType NoteProperty -Name "path" -Value "$BasePath"
    $local:Path = [IO.Path]::Combine($Item.path, $Item.name)

    # Create item
    New-Item -Path $local:Path -ItemType $Item.type | Out-Null
    
    # Add default content if applies
    if ($Item.type -eq "file") {
        Get-DefaultContent $Item | Where-Object { $_ -ne $null } | Set-Content -Path $local:Path
    }
    
    # Iterate through children if any
    if (Get-Member -InputObject $Item -Name "children" -MemberType NoteProperty){
        $Item.children | ForEach-Object  {
            Add-Item -Item $_ -BasePath $local:Path     
        }
    }
}

# Get project root
$ProjectRoot = ((Get-Item $PSScriptRoot).Parent).FullName

# Add tools
."$ProjectRoot\.tools\Import-Files.ps1"

# Parse project structure configuration
$ProjectStructure = Import-JsonFile $ProjectStructurePath

# Iterate through every item recursively
$ProjectStructure.items | ForEach-Object {
    Add-Item -Item $_ -BasePath $RootPath
}
