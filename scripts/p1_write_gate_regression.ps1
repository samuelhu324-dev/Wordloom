param(
  # GitHub repo in OWNER/REPO format.
  [string]$Repo = "samuelhu324-dev/wordloom-v3",

  # Git ref to dispatch the workflow from (branch or tag). Default: current git branch.
  [string]$Ref = "",

  # Commit SHA to select runs for. Default: current HEAD.
  [string]$Sha = "",

  # Optional data scope forwarded to the workflow.
  [string]$LibraryId = "",

  # Evidence window convenience: run multiple rounds of the fixed pack.
  [int]$Rounds = 1,

  # Optional jitter inserted between rounds (seconds).
  [int]$JitterSecondsMin = 0,
  [int]$JitterSecondsMax = 0,

  # Optional worker scope forwarded to the workflow.
  [string]$WorkerLibraryAllowlist = "",

  # Optional [window only] overrides forwarded to the workflow.
  [int]$WindowDurationSeconds = 0,
  [int]$WindowIntervalSeconds = 0,
  [int]$WindowEnqueueBatchSize = 0,
  [int]$WindowMaxTotalEvents = 0,
  [int]$WindowDrainTimeoutSeconds = 0,
  [int]$WindowWorkerMaxRuntimeSeconds = 0,

  # Poll timeout for runs to reach completed.
  [int]$TimeoutMinutes = 25,

  # Output mapping file (SoT pointer to find GH runs).
  [string]$OutPath = "artifacts/write_gate_runs.latest.json",

  # If set, only dispatch workflows (no collection).
  [switch]$DispatchOnly,

  # If set, only collect existing runs (no dispatch).
  [switch]$CollectOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Ensure file redirections write UTF-8 (Windows PowerShell defaults to UTF-16LE).
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
$PSDefaultParameterValues['Add-Content:Encoding'] = 'utf8'
$PSDefaultParameterValues['Set-Content:Encoding'] = 'utf8'

function Write-Utf8NoBom([string]$Path, [string]$Content) {
  $encoding = New-Object System.Text.UTF8Encoding($false)
  $fullPath = [System.IO.Path]::GetFullPath($Path)
  [System.IO.File]::WriteAllText($fullPath, $Content, $encoding)
}

if ($DispatchOnly -and $CollectOnly) {
  throw "Use at most one of -DispatchOnly or -CollectOnly."
}

if ($Rounds -lt 1) {
  throw "Rounds must be >= 1."
}
if ($JitterSecondsMin -lt 0 -or $JitterSecondsMax -lt 0) {
  throw "JitterSecondsMin/Max must be >= 0."
}
if ($JitterSecondsMax -lt $JitterSecondsMin) {
  throw "JitterSecondsMax must be >= JitterSecondsMin."
}

function Require-Command([string]$cmd) {
  $c = Get-Command $cmd -ErrorAction SilentlyContinue
  if (-not $c) {
    throw "Missing required command '$cmd'. Install it and ensure it's on PATH."
  }
}

function Get-GitValue([string[]]$gitArgs) {
  $v = (& git @gitArgs).Trim()
  if (-not $v) { throw "git @($gitArgs -join ' ') returned empty" }
  return $v
}

function Parse-ScenarioIdFromLog([string]$log) {
  if (-not $log) { return $null }
  $m = [regex]::Match($log, 'scenario_id:\s*([A-Za-z0-9_\-/]+)')
  if ($m.Success) { return $m.Groups[1].Value.Trim() }
  return $null
}

Require-Command "git"
Require-Command "gh"

if (-not $Ref) {
  $Ref = Get-GitValue @("branch", "--show-current")
}
if (-not $Sha) {
  $Sha = Get-GitValue @("rev-parse", "HEAD")
}

$expected = @(
  'shadow_verify_search_index_write_gate',
  'shadow_verify_search_index_paging_stability',
  'shadow_verify_shared_keys',
  'shadow_verify_dual_run_window',
  'shadow_verify_canary_dual_write',
  'shadow_verify_dual_write_sampling'
)

function New-WorkflowInputs([string]$ScenarioId) {
  $pairs = @(
    "scenario_id=$ScenarioId",
    "library_id=$LibraryId"
  )

  if ($WorkerLibraryAllowlist) {
    $pairs += "worker_library_allowlist=$WorkerLibraryAllowlist"
  }

  # These inputs are only meaningful for the window scenario, but passing them for other
  # scenarios is harmless (the runner ignores unused env variables).
  if ($WindowDurationSeconds -gt 0) { $pairs += "window_duration_seconds=$WindowDurationSeconds" }
  if ($WindowIntervalSeconds -gt 0) { $pairs += "window_interval_seconds=$WindowIntervalSeconds" }
  if ($WindowEnqueueBatchSize -gt 0) { $pairs += "window_enqueue_batch_size=$WindowEnqueueBatchSize" }
  if ($WindowMaxTotalEvents -gt 0) { $pairs += "window_max_total_events=$WindowMaxTotalEvents" }
  if ($WindowDrainTimeoutSeconds -gt 0) { $pairs += "window_drain_timeout_seconds=$WindowDrainTimeoutSeconds" }
  if ($WindowWorkerMaxRuntimeSeconds -gt 0) { $pairs += "window_worker_max_runtime_seconds=$WindowWorkerMaxRuntimeSeconds" }

  return $pairs
}

for ($round = 1; $round -le $Rounds; $round++) {
  $minCreatedAtUtc = $null
  if (-not $CollectOnly) {
    $minCreatedAtUtc = (Get-Date).ToUniversalTime().AddMinutes(-1)
    foreach ($scenario in $expected) {
      $args = @(
        "workflow", "run", "drill-write-gate.yml",
        "--repo", $Repo,
        "--ref", $Ref
      )

      foreach ($p in (New-WorkflowInputs -ScenarioId $scenario)) {
        $args += @("-f", $p)
      }

      # Avoid noisy output; the run URL is captured later.
      & gh @args | Out-Null
    }

    if ($DispatchOnly) {
      Write-Host "Dispatched round $round/$Rounds ($($expected.Count) scenarios) on ref '$Ref' (sha=$Sha)."
      if ($round -lt $Rounds) {
        $sleepS = if ($JitterSecondsMax -gt 0) { Get-Random -Minimum $JitterSecondsMin -Maximum ($JitterSecondsMax + 1) } else { 0 }
        if ($sleepS -gt 0) {
          Write-Host "Sleeping ${sleepS}s (jitter) before next round dispatch."
          Start-Sleep -Seconds $sleepS
        }
      }
      continue
    }
  }

  $deadline = (Get-Date).ToUniversalTime().AddMinutes($TimeoutMinutes)

  while ($true) {
    if ((Get-Date).ToUniversalTime() -gt $deadline) {
      throw "Timeout waiting for drill runs to complete (round $round/$Rounds)."
    }

    $runs = & gh run list --repo $Repo --workflow drill-write-gate.yml --branch $Ref --limit 80 --json databaseId,status,conclusion,headSha,url,createdAt | ConvertFrom-Json

    $runs = @($runs | Where-Object {
      $_.headSha -eq $Sha -and (
        $null -eq $minCreatedAtUtc -or ([datetime]$_.createdAt).ToUniversalTime() -ge $minCreatedAtUtc
      )
    } | Sort-Object createdAt -Descending)

    $chosen = @{}
    foreach ($run in $runs) {
      if ($chosen.Count -ge $expected.Count) { break }

      $runId = [int64]$run.databaseId
      $log = $null
      try {
        $log = (gh run view $runId --repo $Repo --log 2>$null)
      } catch {
        $log = $null
      }
      $scenarioId = Parse-ScenarioIdFromLog -log $log
      if (-not $scenarioId) { continue }
      if (($expected -notcontains $scenarioId) -or $chosen.ContainsKey($scenarioId)) { continue }

      $chosen[$scenarioId] = [pscustomobject]@{
        scenario_id = $scenarioId
        run_id = $runId
        url = $run.url
        status = $run.status
        conclusion = $run.conclusion
        headSha = $run.headSha
        createdAt = $run.createdAt
      }
    }

    $selected = @()
    foreach ($s in $expected) {
      if ($chosen.ContainsKey($s)) { $selected += $chosen[$s] }
    }

    if ($selected.Count -ne $expected.Count) {
      Start-Sleep -Seconds 15
      continue
    }

    $incomplete = @($selected | Where-Object { $_.status -ne 'completed' })
    if ($incomplete.Count -ne 0) {
      Start-Sleep -Seconds 15
      continue
    }

    $outDir = Split-Path -Parent $OutPath
    if ($outDir -and (-not (Test-Path $outDir))) {
      New-Item -ItemType Directory -Force $outDir | Out-Null
    }

    $json = $selected | ConvertTo-Json -Depth 6
    Write-Utf8NoBom -Path $OutPath -Content ($json + "`n")

    Write-Host ("[round {0}/{1}] Selected runs: {2}/{3}" -f $round, $Rounds, $selected.Count, $expected.Count)
    ($selected | Format-Table -AutoSize scenario_id,run_id,status,conclusion,url | Out-String) | Write-Host

    Write-Host ("[round {0}/{1}] Evidence snippet (paste into log):" -f $round, $Rounds)
    foreach ($row in $selected) {
      Write-Host ("- Drill: drill-write-gate | scenario_id: {0} | Run URL: {1} | status/conclusion: {2} / {3}" -f $row.scenario_id, $row.url, $row.status, $row.conclusion)
    }

    break
  }

  if ($round -lt $Rounds) {
    $sleepS = if ($JitterSecondsMax -gt 0) { Get-Random -Minimum $JitterSecondsMin -Maximum ($JitterSecondsMax + 1) } else { 0 }
    if ($sleepS -gt 0) {
      Write-Host "Sleeping ${sleepS}s (jitter) before next round."
      Start-Sleep -Seconds $sleepS
    }
  }
}
