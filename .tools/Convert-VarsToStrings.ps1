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

function Convert-WpCliCoreInstallAdminPassword {
    [CmdletBinding()]
    param (
        # E-mail
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$AdminPwd
    )

    if ($AdminPwd) {
        return "--admin_password=`"$AdminPwd`""
    }
    else {
        return ""
    }
}

function Convert-WpCliCoreInstallSkipEmail {
    [CmdletBinding()]
    param (
        # E-mail
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [bool]$SkipEmail
    )

    if ($SkipEmail) {
        return "--skip-email"
    }
    else {
        return ""
    }
}

function Get-WpCliCoreDownloadVersion {
    [CmdletBinding()]
    param (
        # Version
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$Version,

        # Default version
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$DefaultVersion
    )
    
    if ($Version) {
        return "$Version"
    }
    else {
        return "$DefaultVersion"
    }
}

function Get-WpCliCoreDownloadLocale {
    [CmdletBinding()]
    param (
        # Locale
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$Locale,

        # Default locale
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$DefaultLocale
    )
    
    if ($Locale) {
        return "$Locale"
    }
    else {
        return "$DefaultLocale"
    }
}

function Convert-WpCliCoreDownloadSkipContent {
    [CmdletBinding()]
    param (
        # Content
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [bool]$SkipContent
    )

    if ($SkipContent) {
        return "--skip-content"
    }
    else {
        return ""
    }
}