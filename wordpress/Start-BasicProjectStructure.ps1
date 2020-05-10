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

    if ($Item.source -eq "raw") {
        return $Item.value
    }

    if ($Item.source -eq "from_file") {
        return Get-Content -Path $Item.value
    }

    if ($Item.source -eq "from_url") {
        return (Invoke-WebRequest $Item.value).Content
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

    # Check if condition is met
    if (Get-Member -InputObject $Item -Name "condition" -MemberType NoteProperty) {
        if ($Item.condition -eq "when-parent-not-empty") {
            if (-Not (Test-Path "$BasePath\*")) {
                $local:condition = $true
            }
            else {
                $local:condition = $false
            }
        }
    }
    else {
        $local:condition = $true # by default
    }

    # Only if the item DOES NOT exist and condition is met
    if (-Not (Test-Path -Path $local:Path) -and $local:condition) {
        # Create item
        New-Item -Path $local:Path -ItemType $Item.type | Out-Null

        # Add default content if applies
        if ($Item.type -eq "file" -AND (Get-Member -InputObject $Item -Name "default_content" -MemberType NoteProperty)) {
            Get-DefaultContent $Item.default_content | Where-Object { $_ -ne $null } | Set-Content -Path $local:Path
        }        
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
