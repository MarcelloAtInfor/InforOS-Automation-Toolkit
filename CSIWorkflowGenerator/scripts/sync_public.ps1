param(
    [string]$ConfigPath = "sync_public.json",
    [switch]$Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-ProjectRoot {
    return (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}

function Normalize-RelPath([string]$base, [string]$fullPath) {
    $basePath = (Resolve-Path $base).Path
    if (-not $basePath.EndsWith("\")) {
        $basePath = "$basePath\"
    }
    $baseUri = New-Object System.Uri($basePath)
    $fullUri = New-Object System.Uri((Resolve-Path $fullPath).Path)
    $relUri = $baseUri.MakeRelativeUri($fullUri).ToString()
    return ($relUri -replace "\\", "/")
}

function Test-DenyMatch([string]$relPath, [string[]]$denyGlobs) {
    foreach ($glob in $denyGlobs) {
        if ($relPath -like $glob) {
            return $true
        }
    }
    return $false
}

function Resolve-AllowFiles([string]$sourceRoot, [string[]]$allowPaths) {
    $results = New-Object System.Collections.Generic.List[string]
    foreach ($allow in $allowPaths) {
        $allowAbs = Join-Path $sourceRoot $allow
        if (-not (Test-Path $allowAbs)) {
            Write-Warning "Allow path not found, skipping: $allow"
            continue
        }
        $item = Get-Item $allowAbs
        if ($item.PSIsContainer) {
            Get-ChildItem $allowAbs -Recurse -File | ForEach-Object {
                $results.Add($_.FullName)
            }
        } else {
            $results.Add($item.FullName)
        }
    }
    return $results
}

$projectRoot = Get-ProjectRoot
$configAbs = Join-Path $projectRoot $ConfigPath
if (-not (Test-Path $configAbs)) {
    throw "Config file not found: $configAbs"
}

$config = Get-Content $configAbs -Raw | ConvertFrom-Json
$targetRoot = $config.public_project_path
if (-not (Test-Path $targetRoot)) {
    throw "Public project path does not exist: $targetRoot"
}

$allowPaths = @($config.allow_paths)
$denyGlobs = @($config.deny_globs)

$allCandidates = Resolve-AllowFiles -sourceRoot $projectRoot -allowPaths $allowPaths
$copied = New-Object System.Collections.Generic.List[string]
$skipped = New-Object System.Collections.Generic.List[string]

foreach ($src in $allCandidates | Sort-Object -Unique) {
    $rel = Normalize-RelPath -base $projectRoot -fullPath $src
    if (Test-DenyMatch -relPath $rel -denyGlobs $denyGlobs) {
        $skipped.Add($rel)
        continue
    }

    $dest = Join-Path $targetRoot $rel
    $destDir = Split-Path -Parent $dest
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    if ($Apply) {
        Copy-Item -Path $src -Destination $dest -Force
    }
    $copied.Add($rel)
}

if ($Apply) {
    Write-Output "Sync mode: APPLY"
} else {
    Write-Output "Sync mode: DRY-RUN"
}
Write-Output "Private source: $projectRoot"
Write-Output "Public target:  $targetRoot"
Write-Output "Allow paths: $($allowPaths.Count)"
Write-Output "Files selected: $($copied.Count)"
Write-Output "Files denied:   $($skipped.Count)"

if ($copied.Count -gt 0) {
    Write-Output ""
    Write-Output "Selected files:"
    $copied | ForEach-Object { Write-Output "  + $_" }
}

if ($skipped.Count -gt 0) {
    Write-Output ""
    Write-Output "Denied files:"
    $skipped | ForEach-Object { Write-Output "  - $_" }
}

if (-not $Apply) {
    Write-Output ""
    Write-Output "No files were copied. Re-run with -Apply to sync."
}
