param(
  [Parameter(Mandatory = $true)]
  [string[]]$RequestedIdPrefix,

  [string]$Repo = '',
  [string]$LogsDir = '',
  [string[]]$WrapperNotes = @(),
  [string]$RunId = '',
  [string]$ArtifactRoot = '',
  [string]$PythonExe = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
$PSDefaultParameterValues['Add-Content:Encoding'] = 'utf8'
$PSDefaultParameterValues['Set-Content:Encoding'] = 'utf8'

function Resolve-RepoRoot {
  return [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
}

function Resolve-AbsolutePath([string]$BasePath, [string]$Value) {
  if ([string]::IsNullOrWhiteSpace($Value)) {
    return ''
  }

  if ([System.IO.Path]::IsPathRooted($Value)) {
    return [System.IO.Path]::GetFullPath($Value)
  }

  return [System.IO.Path]::GetFullPath((Join-Path $BasePath $Value))
}

function Resolve-PythonExe([string]$BasePath, [string]$RequestedPythonExe) {
  if (-not [string]::IsNullOrWhiteSpace($RequestedPythonExe)) {
    return (Resolve-AbsolutePath -BasePath $BasePath -Value $RequestedPythonExe)
  }

  $venvPython = Join-Path $BasePath '.venv\Scripts\python.exe'
  if (Test-Path $venvPython) {
    return [System.IO.Path]::GetFullPath($venvPython)
  }

  $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
  if ($pythonCmd) {
    return $pythonCmd.Source
  }

  throw "Missing Python interpreter. Pass -PythonExe explicitly or ensure 'python' is on PATH."
}

function Ensure-Directory([string]$Path) {
  New-Item -ItemType Directory -Force -Path $Path | Out-Null
}

function Get-Slug([string[]]$Prefixes) {
  $joined = ($Prefixes | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }) -join '-'
  if ([string]::IsNullOrWhiteSpace($joined)) {
    $joined = 'review'
  }
  return ($joined -replace '[^A-Za-z0-9._-]', '-')
}

$repoRoot = Resolve-RepoRoot
$pythonExe = Resolve-PythonExe -BasePath $repoRoot -RequestedPythonExe $PythonExe

if (-not $RunId) {
  $RunId = Get-Date -Format 'yyyyMMddTHHmmss'
}

if (-not $ArtifactRoot) {
  $slug = Get-Slug -Prefixes $RequestedIdPrefix
  $ArtifactRoot = Join-Path $repoRoot "artifacts/operator-facing/pr-body-completeness-check/$RunId-$slug"
} else {
  $ArtifactRoot = Resolve-AbsolutePath -BasePath $repoRoot -Value $ArtifactRoot
}

Ensure-Directory -Path $ArtifactRoot

$wrapperResultPath = Join-Path $ArtifactRoot 'wrapper-result.json'
$wrapperSummaryPath = Join-Path $ArtifactRoot 'workflow-summary.md'
$artifactManifestPath = Join-Path $ArtifactRoot 'artifact-manifest.json'
$reviewResultPath = Join-Path $ArtifactRoot 'review-result.json'
$reviewArtifactDir = Join-Path $ArtifactRoot 'review-files'

$pythonArgs = @(
  'scripts/issues/plan_pr_body_completeness_check_wrapper.py',
  '--wrapper-result-path', $wrapperResultPath,
  '--wrapper-summary-path', $wrapperSummaryPath,
  '--artifact-manifest-path', $artifactManifestPath,
  '--review-result-path', $reviewResultPath,
  '--review-artifact-dir', $reviewArtifactDir,
  '--trigger-surface', 'local-operator-facing'
)

foreach ($prefix in $RequestedIdPrefix) {
  if (-not [string]::IsNullOrWhiteSpace($prefix)) {
    $pythonArgs += @('--requested-id-prefix', $prefix)
  }
}
if ($Repo) {
  $pythonArgs += @('--repo', $Repo)
}
if ($LogsDir) {
  $pythonArgs += @('--logs-dir', (Resolve-AbsolutePath -BasePath $repoRoot -Value $LogsDir))
}
foreach ($note in $WrapperNotes) {
  if (-not [string]::IsNullOrWhiteSpace($note)) {
    $pythonArgs += @('--wrapper-notes', $note)
  }
}

Push-Location $repoRoot
try {
  & $pythonExe @pythonArgs
  $exitCode = $LASTEXITCODE
} finally {
  Pop-Location
}

if (Test-Path $wrapperResultPath) {
  $payload = Get-Content -Path $wrapperResultPath -Raw -Encoding utf8 | ConvertFrom-Json
  Write-Host ("result={0}" -f $payload.result)
  Write-Host ("total_logs_reviewed={0}" -f $payload.total_logs_reviewed)
  Write-Host ("wrapper_result_path={0}" -f $payload.wrapper_result_path)
  Write-Host ("wrapper_summary_path={0}" -f $payload.wrapper_summary_path)
  Write-Host ("artifact_manifest_path={0}" -f $payload.artifact_manifest_path)
  Write-Host ("review_result_path={0}" -f $payload.review_result_path)
  if ($payload.stop_reason) {
    Write-Host ("stop_reason={0}" -f $payload.stop_reason)
  }
}

Write-Host ("artifact_root={0}" -f $ArtifactRoot)
exit $exitCode