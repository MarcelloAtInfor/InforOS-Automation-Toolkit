[CmdletBinding()]
param(
    [string]$ProjectRoot = '',
    [switch]$IncludeMainPageOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
    $scriptRoot = if (-not [string]::IsNullOrWhiteSpace($PSScriptRoot)) {
        $PSScriptRoot
    }
    else {
        Split-Path -Parent $MyInvocation.MyCommand.Path
    }

    $ProjectRoot = Split-Path -Parent $scriptRoot
}

Add-Type -AssemblyName System.Activities

$projectJsonPath = Join-Path $ProjectRoot 'project.json'
if (-not (Test-Path $projectJsonPath)) {
    throw "project.json not found at '$projectJsonPath'."
}

$project = Get-Content -Raw $projectJsonPath | ConvertFrom-Json
$files = @()

if ($IncludeMainPageOnly) {
    $files = @((Join-Path $ProjectRoot $project.main))
}
else {
    $sourceFiles = @($project.sourceFiles | ForEach-Object { Join-Path $_.filePath $_.fileName })
    $mainPage = Join-Path $ProjectRoot $project.main
    $files = @($mainPage) + $sourceFiles | Select-Object -Unique
}

$results = foreach ($file in $files) {
    try {
        [xml](Get-Content -Raw $file) | Out-Null
        $null = [System.Activities.XamlIntegration.ActivityXamlServices]::Load($file)
        [pscustomobject]@{
            File = $file
            Status = 'SUCCESS'
            Error = ''
        }
    }
    catch {
        [pscustomobject]@{
            File = $file
            Status = 'FAILED'
            Error = $_.Exception.Message
        }
    }
}

$failed = @($results | Where-Object { $_.Status -eq 'FAILED' })

if ($failed.Count -gt 0) {
    $message = ($failed | ForEach-Object { "- $($_.File): $($_.Error)" }) -join [Environment]::NewLine
    throw "XAML validation failed:`n$message"
}

$results
