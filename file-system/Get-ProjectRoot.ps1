<# 
    Gets the project root based on the location of a determined file (project.xml by default)
#>
function Get-ProjectRoot {
    param (
        # File to find in order to determine project root
        [Parameter(Mandatory=$false)]
        [String]$File
    )

    # Set variables
    if ([String]::IsNullOrEmpty($File)) {
        $File = "project.xml"
    }    
    $ProjectRoot = $PSScriptRoot

    # Find the project file
    $ProjectFile = "$ProjectRoot\$File"
    while (![System.IO.File]::Exists($ProjectFile)) {
        $ProjectRoot = Split-Path -Path $ProjectRoot -Parent
        $ProjectFile = "$ProjectRoot\$File"
    }

    return $ProjectRoot
}
