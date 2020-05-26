# This script gets the current Git branch and sets the $CurrentBranch variable

# Note: In case of execution policy related problems while development please execute this command as admin
# Set-ExecutionPolicy -ExecutionPolicy Bypass

[CmdletBinding()]
Param(
    # Build source branch
    # $(Build.SourceBranch)
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [String] $BuildSourceBranch
)

$CurrentBranch = "$BuildSourceBranch".Replace("refs/heads/","").Replace("refs/","")
Write-Host "##vso[task.setvariable variable=CurrentBranch]$CurrentBranch"
Write-Host "Current branch is $CurrentBranch ($BuildSourceBranch)"
