param(
    [string]$ProjectRoot = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
    $ProjectRoot = Split-Path -Parent $PSScriptRoot
}

$extractPath = Join-Path $ProjectRoot "ExtractOCRData.xaml"
if (-not (Test-Path $extractPath)) {
    throw "ExtractOCRData.xaml not found under project root: $ProjectRoot"
}

$extractContent = Get-Content -Raw -Path $extractPath
$documentsDir = Join-Path $ProjectRoot "Documents"
$documentsExists = Test-Path $documentsDir
$documentMetadataFiles = @()
if ($documentsExists) {
    $documentMetadataFiles = Get-ChildItem -Recurse -File -Path $documentsDir -Filter "FlowBasedFields_ToFilter.json" | Select-Object -ExpandProperty FullName
}

$hasExtractDataActivity = $extractContent -match "ExtractDataActivity"
$hasPlaceholder = $extractContent -match "LIVE_ACTIVITY_PENDING"
$hasSidecarMode = $extractContent -match "DOCUMENT_SIDECAR_JSON"

$status = [ordered]@{
    ProjectRoot = $ProjectRoot
    ExtractOCRDataPath = $extractPath
    HasExtractDataActivity = $hasExtractDataActivity
    HasPlaceholderBranch = $hasPlaceholder
    HasSidecarSupport = $hasSidecarMode
    DocumentsDirectoryExists = $documentsExists
    DocumentMetadataFileCount = $documentMetadataFiles.Count
    DocumentMetadataFiles = $documentMetadataFiles
}

$statusJson = $status | ConvertTo-Json -Depth 6
Write-Output $statusJson

if (-not $hasExtractDataActivity -or $hasPlaceholder) {
    Write-Warning "The generated project does not show a clean on-disk live OCR binding yet."
    Write-Warning "If Studio validation is only in-memory, preserve_output_paths will not be enough to keep that OCR seam across regeneration."
}
