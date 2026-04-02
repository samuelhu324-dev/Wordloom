param(
  [Parameter(Mandatory = $true)]
  [ValidateSet('issue-conclusion', 'issue-relationship', 'pr-body-rewrite', 'pr-create-preflight')]
  [string]$OperationFamily,

  [Parameter(Mandatory = $true)]
  [string]$SelectionInputPath,

  [ValidateSet('manifest', 'audit-plan')]
  [string]$SelectionInputKind = 'manifest',

  [string]$FamilyInputPath = '',

  [ValidateSet('manifest', 'plan', 'result')]
  [string]$FamilyInputKind = 'manifest',

  [string]$Repo = '',
  [string]$TrustedSourceLogPath = '',
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

function Get-Slug([string]$OperationFamilyValue, [string]$SelectionPathValue) {
  $leaf = [System.IO.Path]::GetFileNameWithoutExtension($SelectionPathValue)
  if ([string]::IsNullOrWhiteSpace($leaf)) {
    $leaf = 'selection'
  }

  $safeLeaf = ($leaf -replace '[^A-Za-z0-9._-]', '-')
  return "$OperationFamilyValue-$safeLeaf"
}

function Ensure-Directory([string]$Path) {
  New-Item -ItemType Directory -Force -Path $Path | Out-Null
}

$repoRoot = Resolve-RepoRoot
$pythonExe = Resolve-PythonExe -BasePath $repoRoot -RequestedPythonExe $PythonExe
$selectionInputAbsolutePath = Resolve-AbsolutePath -BasePath $repoRoot -Value $SelectionInputPath

if (-not (Test-Path $selectionInputAbsolutePath)) {
  throw "SelectionInputPath not found: $SelectionInputPath"
}

$familyInputAbsolutePath = ''
if (-not [string]::IsNullOrWhiteSpace($FamilyInputPath)) {
  $familyInputAbsolutePath = Resolve-AbsolutePath -BasePath $repoRoot -Value $FamilyInputPath
  if (-not (Test-Path $familyInputAbsolutePath)) {
    throw "FamilyInputPath not found: $FamilyInputPath"
  }
}

if (-not $RunId) {
  $RunId = Get-Date -Format 'yyyyMMddTHHmmss'
}

if (-not $ArtifactRoot) {
  $slug = Get-Slug -OperationFamilyValue $OperationFamily -SelectionPathValue $selectionInputAbsolutePath
  $ArtifactRoot = Join-Path $repoRoot "artifacts/operator-facing/publish-verify-remediation-gate-read-only-wrapper/$RunId-$slug"
} else {
  $ArtifactRoot = Resolve-AbsolutePath -BasePath $repoRoot -Value $ArtifactRoot
}

Ensure-Directory -Path $ArtifactRoot

$wrapperResultPath = Join-Path $ArtifactRoot 'wrapper-result.json'
$wrapperSummaryPath = Join-Path $ArtifactRoot 'workflow-summary.md'
$artifactManifestPath = Join-Path $ArtifactRoot 'artifact-manifest.json'
$thinGateResultPath = Join-Path $ArtifactRoot 'thin-gate-result.json'

$auditPlanPath = ''
$remediationPlanPath = ''
$decisionPath = ''
$familyPlanPath = ''

if ($SelectionInputKind -eq 'manifest') {
  $auditPlanPath = Join-Path $ArtifactRoot 'lifecycle-audit-plan.json'
  $remediationPlanPath = Join-Path $ArtifactRoot 'lifecycle-remediation-plan.json'
  $decisionPath = Join-Path $ArtifactRoot 'lifecycle-gate-decision.json'
}

if ($OperationFamily -eq 'pr-create-preflight') {
  $familyPlanPath = Join-Path $ArtifactRoot 'family-plan.json'
}

$pythonArgs = @(
  'scripts/issues/plan_publish_verify_remediation_gate_read_only_wrapper.py',
  $OperationFamily,
  $selectionInputAbsolutePath,
  '--selection-input-kind', $SelectionInputKind,
  '--wrapper-result-path', $wrapperResultPath,
  '--wrapper-summary-path', $wrapperSummaryPath,
  '--artifact-manifest-path', $artifactManifestPath,
  '--thin-gate-result-path', $thinGateResultPath,
  '--trigger-surface', 'local-operator-facing'
)

if ($familyInputAbsolutePath) {
  $pythonArgs += @('--family-input-path', $familyInputAbsolutePath, '--family-input-kind', $FamilyInputKind)
}
if ($Repo) {
  $pythonArgs += @('--repo', $Repo)
}
if ($TrustedSourceLogPath) {
  $pythonArgs += @('--trusted-source-log-path', (Resolve-AbsolutePath -BasePath $repoRoot -Value $TrustedSourceLogPath))
}
if ($auditPlanPath) {
  $pythonArgs += @('--audit-plan-path', $auditPlanPath)
}
if ($remediationPlanPath) {
  $pythonArgs += @('--remediation-plan-path', $remediationPlanPath)
}
if ($decisionPath) {
  $pythonArgs += @('--decision-path', $decisionPath)
}
if ($familyPlanPath) {
  $pythonArgs += @('--family-plan-path', $familyPlanPath)
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
  Write-Host ("normalized_decision={0}" -f $payload.normalized_decision)
  Write-Host ("wrapper_result_path={0}" -f $payload.wrapper_result_path)
  Write-Host ("wrapper_summary_path={0}" -f $payload.wrapper_summary_path)
  Write-Host ("artifact_manifest_path={0}" -f $payload.artifact_manifest_path)
  if ($payload.stop_reason) {
    Write-Host ("stop_reason={0}" -f $payload.stop_reason)
  }
}

Write-Host ("artifact_root={0}" -f $ArtifactRoot)
exit $exitCode