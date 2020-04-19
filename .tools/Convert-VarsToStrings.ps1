<# 
    Converts variable values to specific strings

#>
function Convert-WpCliConfigCreateSkipCheck {
    [CmdletBinding()]
    param (
        # True for skipping db check
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [bool]$SkipCheck
    )

    if ($SkipCheck) {
        return "--skip-check"
    }
    else {
        return ""
    }
}

function Convert-WpCliConfigCreateAccessibleHosts {
    [CmdletBinding()]
    param (
        # Object Array
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [System.Object[]] $AccessibleHosts
    )

    return $AccessibleHosts -join ","    
}

function Convert-WpCliConfigCreateAutoUpdateCore {
    [CmdletBinding()]
    param (
        # true, false or minor
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        $AutoUpdateCore
    )

    if ($AutoUpdateCore -eq "minor") {
        return $AutoUpdateCore
    }
    else {
        return "$AutoUpdateCore --raw"
    }
}
