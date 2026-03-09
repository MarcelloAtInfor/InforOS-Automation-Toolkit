[CmdletBinding()]
param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

$templateFolder = Join-Path $ProjectRoot 'samples\batch'
$runtimeRoot = Join-Path $ProjectRoot 'samples\runtime_batch'
$inputFolder = Join-Path $runtimeRoot 'Input'
$inProgressFolder = Join-Path $runtimeRoot 'InProgress'
$successFolder = Join-Path $runtimeRoot 'Success'
$failureFolder = Join-Path $runtimeRoot 'Failure'

foreach ($folder in @($inputFolder, $inProgressFolder, $successFolder, $failureFolder)) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
}

Get-ChildItem -Path $inputFolder -File -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem -Path $inProgressFolder -File -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem -Path $successFolder -Recurse -File -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem -Path $failureFolder -Recurse -File -ErrorAction SilentlyContinue | Remove-Item -Force

Get-ChildItem -Path $successFolder -Directory -Recurse -ErrorAction SilentlyContinue |
    Sort-Object FullName -Descending |
    Remove-Item -Force -Recurse -ErrorAction SilentlyContinue

Get-ChildItem -Path $failureFolder -Directory -Recurse -ErrorAction SilentlyContinue |
    Sort-Object FullName -Descending |
    Remove-Item -Force -Recurse -ErrorAction SilentlyContinue

Copy-Item -Path (Join-Path $templateFolder '*.json') -Destination $inputFolder -Force

[pscustomobject]@{
    TemplateFolder = $templateFolder
    InputFolder = $inputFolder
    SeededFiles = (Get-ChildItem -Path $inputFolder -File -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name)
}
