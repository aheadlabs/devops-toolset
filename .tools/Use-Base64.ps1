<#
    Encodes a string to Base64 format
#>
function ConvertTo-Base64 {
    param (
        # Plain text to be encoded to a Base64 string
        [Parameter (Mandatory=$true, ValueFromPipeline=$true)]
        [ValidateNotNullOrEmpty()]
        [string] $Text
    )
    
    return [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Text))
}

<#
    Decodes a string from Base64 format
#>
function ConvertFrom-Base64 {
    param (
        # Base64 string to be decoded to plain text
        [Parameter (Mandatory=$true, ValueFromPipeline=$true)]
        [ValidateNotNullOrEmpty()]
        [string] $Base64Text
    )
    
    return [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($Base64Text))
}
