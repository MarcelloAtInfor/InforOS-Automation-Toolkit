[CmdletBinding()]
param(
    [string]$RuntimeLogRoot = 'C:\ProgramData\Infor\RPA\Runtime\Logs',
    [switch]$OpenTail
)

$latestDir = Get-ChildItem $RuntimeLogRoot -Directory |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $latestDir) {
    throw "No runtime log directories found under '$RuntimeLogRoot'."
}

$latestFile = Get-ChildItem $latestDir.FullName -File |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $latestFile) {
    throw "No runtime log file found in '$($latestDir.FullName)'."
}

if ($OpenTail) {
    Get-Content -Path $latestFile.FullName -Tail 80
} else {
    [pscustomobject]@{
        Directory = $latestDir.FullName
        File = $latestFile.FullName
        LastWriteTime = $latestFile.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss')
    }
}
