<#
    Gets the id for the latest build for a project or $null if there are no builds
#>
function Get-LastBuildId {
    [CmdletBinding()]
    param (
        # Azure DevOps organization
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$Organization,

        # Azure DevOps project
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$Project
    )
    
    $_builds_json = Invoke-RestMethod -Method Get -Uri "https://dev.azure.com/$Organization/$Project/_apis/build/builds"
    
    # Return the last build id for the project
    if ($_builds_json.value.Count -gt 0) {
        return $_builds_json.value[0].id
    }
    else {
        return $null
    }
}
