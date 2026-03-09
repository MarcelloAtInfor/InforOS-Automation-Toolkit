[CmdletBinding()]
param(
    [string]$ProjectRoot = '',
    [string]$WindowTitleContains = 'Infor RPA Studio',
    [string]$RuntimeLogRoot = 'C:\ProgramData\Infor\RPA\Runtime\Logs',
    [int]$PollIntervalMs = 10000,
    [int]$TimeoutSeconds = 90,
    [int]$TailLines = 80,
    [switch]$ReseedSampleBatch
)

$projectRoot = if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
    Split-Path -Parent $PSScriptRoot
}
else {
    $ProjectRoot
}
$sampleRuntimeInput = Join-Path $projectRoot 'samples\runtime_batch\Input'
$sampleTemplateFolder = Join-Path $projectRoot 'samples\batch'

if ($ReseedSampleBatch -or ((Test-Path $sampleRuntimeInput) -and (Test-Path $sampleTemplateFolder) -and -not (Get-ChildItem -Path $sampleRuntimeInput -File -ErrorAction SilentlyContinue | Select-Object -First 1))) {
    powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'reset_runtime_batch.ps1') -ProjectRoot $projectRoot | Out-Null
}

powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'validate_project_xaml.ps1') -ProjectRoot $projectRoot | Out-Null

$before = Get-ChildItem $RuntimeLogRoot -Directory -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

$beforePath = if ($before) { $before.FullName } else { '' }
$beforeTime = if ($before) { $before.LastWriteTime } else { [datetime]::MinValue }
$beforeFile = $null
$beforeFilePath = ''
$beforeFileTime = [datetime]::MinValue

if ($before) {
    $beforeFile = Get-ChildItem $before.FullName -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1

    if ($beforeFile) {
        $beforeFilePath = $beforeFile.FullName
        $beforeFileTime = $beforeFile.LastWriteTime
    }
}

$triggerResult = powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'trigger_studio_run.ps1') -WindowTitleContains $WindowTitleContains -PassThru | Out-String

$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
$latestDir = $null
$latestFile = $null

while ((Get-Date) -lt $deadline) {
    $candidate = Get-ChildItem $RuntimeLogRoot -Directory -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1

    if ($candidate) {
        $candidateFile = Get-ChildItem $candidate.FullName -File -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 1

        $dirChanged = $candidate.FullName -ne $beforePath -or $candidate.LastWriteTime -gt $beforeTime
        $fileChanged = $candidateFile -and (
            $candidateFile.FullName -ne $beforeFilePath -or
            $candidateFile.LastWriteTime -gt $beforeFileTime
        )

        if ($dirChanged -or $fileChanged) {
            $latestDir = $candidate
            $latestFile = $candidateFile
            break
        }
    }

    Start-Sleep -Milliseconds $PollIntervalMs
}

if (-not $latestDir) {
    $triggerText = if (-not [string]::IsNullOrWhiteSpace($triggerResult)) { $triggerResult } else { 'Trigger result unavailable.' }
    throw "Timed out after $TimeoutSeconds seconds waiting for a new or updated runtime log after triggering Studio run. Studio may have failed before runtime log creation.`nTrigger diagnostics:`n$triggerText"
}

while ((Get-Date) -lt $deadline) {
    $latestFile = Get-ChildItem $latestDir.FullName -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1

    if ($latestFile) {
        $text = Get-Content -Path $latestFile.FullName -Raw -ErrorAction SilentlyContinue
        if ($text -match 'Workflow Finished' -or $text -match 'Workflow Terminated' -or $text -match 'Activity State: Faulted') {
            break
        }
    }

    Start-Sleep -Milliseconds $PollIntervalMs
}

if (-not $latestFile) {
    throw "A new runtime log directory was created but no log file was found in '$($latestDir.FullName)'."
}

[pscustomobject]@{
    Directory = $latestDir.FullName
    File = $latestFile.FullName
    LastWriteTime = $latestFile.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss')
}

Get-Content -Path $latestFile.FullName -Tail $TailLines
