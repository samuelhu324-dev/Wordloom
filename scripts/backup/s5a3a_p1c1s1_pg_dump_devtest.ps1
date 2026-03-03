param(
  [Parameter(Mandatory = $false)]
  [string]$ComposeFile = "docker-compose.devtest-db.yml",

  [Parameter(Mandatory = $false)]
  [string]$Service = "db_devtest",

  [Parameter(Mandatory = $false)]
  [string]$Database = "wordloom_dev",

  [Parameter(Mandatory = $false)]
  [string]$User = "wordloom",

  [Parameter(Mandatory = $false)]
  [string]$Password = "wordloom",

  [Parameter(Mandatory = $true)]
  [string]$OutFile
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-RepoRoot {
  $scriptDir = Split-Path -Parent $PSCommandPath
  return (Resolve-Path (Join-Path $scriptDir "..\.." )).Path
}

$repoRoot = Resolve-RepoRoot
$composePath = Join-Path $repoRoot $ComposeFile
if (-not (Test-Path $composePath)) {
  throw "Compose file not found: $composePath"
}

$outDir = Split-Path -Parent $OutFile
if ($outDir -and -not (Test-Path $outDir)) {
  New-Item -ItemType Directory -Force -Path $outDir | Out-Null
}

$containerId = (docker compose -f $composePath ps -q $Service).Trim()
if (-not $containerId) {
  throw "No container found for service '$Service'. Start it with: docker compose -f $composePath up -d"
}

$tmpDumpPath = "/tmp/wordloom_${Database}.dump"

# Create dump inside container (custom format), then copy out.
docker exec -e "PGPASSWORD=$Password" $containerId pg_dump -U $User -d $Database -Fc -f $tmpDumpPath | Out-Null

try {
  docker cp "${containerId}:${tmpDumpPath}" "$OutFile" | Out-Null
}
finally {
  docker exec $containerId rm -f $tmpDumpPath | Out-Null
}

Write-Host "OK"
Write-Host "CONTAINER_ID=$containerId"
Write-Host "OUT_FILE=$OutFile"
