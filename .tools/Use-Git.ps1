function Add-GitExclusion {
    param (
        # Path to .gitignore directory
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string] $RootPath,

        # Exclusion to add to the .gitignore file
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string] $Exclusion
    )

    $local:git_path = [IO.Path]::Combine($RootPath, ".gitignore")
    
    Add-Content $local:git_path $Exclusion
}

function Find-GitExclusion {
    param (
        # Path to .gitignore directory
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string] $RootPath,

        # Exclusion to find in the .gitignore file
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string] $Exclusion
    )
    
    $local:git_path = [IO.Path]::Combine($RootPath, ".gitignore")

    $local:gitignore = (Get-Content $local:git_path )
    if ($local:gitignore | Where-Object { $_ -eq $Exclusion }) {
        return $true
    }
    
    return $false
}

function Update-GitExclusion {
    param (
        # Path to .gitignore directory
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string] $RootPath,

        # Exclusion to find in the .gitignore file (1 capturing group)
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string] $RegEx1CG,

        # Exclusion to find in the .gitignore file
        [Parameter (Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string] $Value
    )
    
    $local:git_path = [IO.Path]::Combine($RootPath, ".gitignore")

    $local:gitignore = (Get-Content $local:git_path )

    for ($i = 0; $i -lt $local:gitignore.Length; $i++) {
        if ($local:gitignore[$i] -match $RegEx1CG) {
            $local:gitignore[$i] = $local:gitignore[$i] -replace $matches[1], $Value
        }        
    }
    
    Set-Content $local:git_path $local:gitignore
}
