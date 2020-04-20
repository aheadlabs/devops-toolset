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

function Convert-WpCliCoreInstallSkipEmail {
    [CmdletBinding()]
    param (
        # E-mail
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [bool]$AdminPassword
    )

    if ($AdminPassword) {
        return "--admin-password=`"$AdminPassword`" --skip-email"
    }
    else {
        return ""
    }
}

function Get-WpCliCoreDownloadVersion {
    [CmdletBinding()]
    param (
        # Version (latest by default)
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [bool]$Version
    )
    
    if ($Version) {
        return "$Version"
    }
    else {
        return "latest"
    }
}

function Get-WpCliCoreDownloadLocale {
    [CmdletBinding()]
    param (
        # Locale (en_US by default)
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [bool]$Locale
    )
    
    if ($Locale) {
        return "$Locale"
    }
    else {
        return "en_US"
    }
}