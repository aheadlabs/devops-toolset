<#
    This script parses the artifact file name to get the version information
#>

[CmdletBinding()]
Param(
    # Artifact file path
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [String] $ArtifactPath,

    # DevOps platform code (see \.devops-platform-specific\README.md)
    [Parameter (Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [String] $DevOpsPlatformCode
)

# Get project root
$ProjectRoot = ((Get-Item $PSScriptRoot).Parent).FullName

# Add tools
."$ProjectRoot\.tools\Convert-ToJson.ps1"

# Add platform specific logic
."$ProjectRoot\.devops-platform-specific\Add-EnvironmentVariables-$DevOpsPlatformCode.ps1"

# Get full version
$FileNameWithoutExtension = [io.path]::GetFileNameWithoutExtension($ArtifactPath)
$VersionFull = $FileNameWithoutExtension -creplace "^[a-zA-Z-]*", ""

# Get version segments using capture groups
# 1. The whole version string
# 2. MAJOR.MINOR.PATCH-PRE_RELEASE (what you should be evaluating for precendence)
# 3. MAJOR
# 4. MINOR
# 5. PATCH
# 6. PRERELEASE
# 7. BUILD_METADATA
if($VersionFull -match '^((([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)$'){
    $VersionMajorMinorPatchPreRelease = $matches[2]
    $VersionMajor = $matches[3]
    $VersionMinor = $matches[4]
    $VersionPatch = $matches[5]
    $VersionPreRelease = $matches[6]
    $VersionBuildMetadata = $matches[7]
}

# Create key-value pairs with version data
$EnvironmentVariables = [System.Collections.Generic.List[hashtable]]::new()
$EnvironmentVariables.Add(@{key="ArtifactFileName";value=$ArtifactFileName})
$EnvironmentVariables.Add(@{key="VersionFull";value=$VersionFull})
$EnvironmentVariables.Add(@{key="VersionMajorMinorPatchPreRelease";value=$VersionMajorMinorPatchPreRelease})
$EnvironmentVariables.Add(@{key="VersionMajor";value=$VersionMajor})
$EnvironmentVariables.Add(@{key="VersionMinor";value=$VersionMinor})
$EnvironmentVariables.Add(@{key="VersionPatch";value=$VersionPatch})
$EnvironmentVariables.Add(@{key="VersionPreRelease";value=$VersionPreRelease})
$EnvironmentVariables.Add(@{key="VersionBuildMetadata";value=$VersionBuildMetadata})

# Create environment variables
CreateEnvironmentVariables $EnvironmentVariables
LogEnvironmentVariables $EnvironmentVariables
