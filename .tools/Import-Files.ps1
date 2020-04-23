<#
    Imports a JSON file to a one-line string
#>
function Import-JsonFileToOneLine {
    param (        
        # Path to site.json file
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [String] $Path
    )

    # Parse JSON file
    [string]$JsonContent = Get-Content -Path $Path -Raw
    $JsonContent = $JsonContent | ConvertTo-Json -Compress

    # Return JSON
    return $JsonContent
}

<#
    Imports a JSON file
#>
function Import-JsonFile {
    param (        
        # Path to site.json file
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [String] $Path
    )

    # Parse JSON file
    $Json = Get-Content -Path $Path -Raw | ConvertFrom-Json

    # Return JSON
    return $Json
}
