<# 
    Converts 1-level-depth XML to JSON key-value pairs

    Input:
    ------

    <project>
        <name>devops-toolset</name>
        <version>0.1.0</version>
    </project>

    Hashtable sample needed for the conversion:
    -------------------------------------------
    $HashTable = @{
        project = @(
            @{
                key = "ProjectName"
                value = "devops-toolset"
            },
            @{
                key = "ProjectVersion"
                value = "1.6.0"
            }
        )
    }

    Output:
    -------

    [
        {
            "key":"name",
            "value":"devops-toolset"
        },
        {
            "key":"version",
            "value":"1.6.0"
        }
    ]
#>
function Convert-XmlToJsonKeyValuePairs {
    [CmdletBinding()]
    param (
        # XML document to be converted
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [XML]$XmlDocument
    )

    # Get TextInfo for capitalizing strings
    $TextInfo = (Get-Culture).TextInfo

    # Set everything up at root level
    $DocumentElement = $XmlDocument.DocumentElement
    $TrailingName = $TextInfo.ToTitleCase($DocumentElement.LocalName)
    
    if ($DocumentElement.HasChildNodes) {
        # Create a hashtable list to generate all children-based key-value pairs
        $ChildrenHashtableArray = [System.Collections.Generic.List[hashtable]]::new()

        # Iterate through all children
        $DocumentElement.ChildNodes | ForEach-Object {
            $ChildElement = $_

            # Add key-value pair hashtable
            $ChildrenHashtableArray.Add(@{
                key = $TrailingName + $TextInfo.ToTitleCase($ChildElement.LocalName)
                value = $ChildElement.InnerText
            })
        }
    } 

    # Convert to JSON
    return $ChildrenHashtableArray | ConvertTo-Json -Compress
}
