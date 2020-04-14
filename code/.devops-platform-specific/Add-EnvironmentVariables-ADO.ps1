<#
    Receives JSON key-value pairs as Object[] and adds then as environment variables in Azure DevOps
#>
function CreateEnvironmentVariables {
    param (
        # Environment variables as key-value pair objects
        [System.Object[]]$EnvironmentVariables
    )

    # Create environment variables
    $EnvironmentVariables | ForEach-Object {
        $key = $_.key
        $value = $_.value
        Write-Host "##vso[task.setvariable variable=$key]$value"
    }
}

<#
    Receives JSON key-value pairs as Object[] and logs them to the console
#>
function LogEnvironmentVariables {
    param (
        # Environment variables as key-value pair objects
        [System.Object[]]$EnvironmentVariables
    )

    # Log data
    Write-Output "Environment variables created"
    Write-Output "============================="
    $EnvironmentVariables | ForEach-Object {
        $key = $_.key
        $value = $_.value
        Write-Host $key "=" $value
    }
}
