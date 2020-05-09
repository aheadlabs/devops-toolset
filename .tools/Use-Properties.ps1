<#
    Returns true if any of the properties are present in the given object
#>
function Find-ObjectProperties {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true)]
        [psobject] $Item,

        [Parameter(Mandatory=$true)]
        [array] $Properties
    )
    
    # Look for each property in the object
    $Properties | ForEach-Object {
        if (Get-Member -InputObject $Item -Name $_ -MemberType NoteProperty) {
            return $true
        }
        return $false
    }    
}