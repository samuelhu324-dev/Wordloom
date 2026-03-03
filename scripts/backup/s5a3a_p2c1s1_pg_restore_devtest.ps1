param(
  [Parameter(Mandatory = $false)]
  [string]$ComposeFile = "docker-compose.devtest-db.yml",

  [Parameter(Mandatory = $false)]
  [string]$Service = "db_devtest",

  [Parameter(Mandatory = $true)]
  [string]$DumpFile,

  [Parameter(Mandatory = $false)]
  [string]$TargetDatabase = "wordloom_restore_dev",

  [Parameter(Mandatory = $false)]
  [string]$User = "wordloom",

  [Parameter(Mandatory = $false)]
  [string]$Password = "wordloom",

  [Parameter(Mandatory = $false)]
  [switch]$DropIfExists
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

$dumpPath = Resolve-Path -Path (Join-Path $repoRoot $DumpFile) -ErrorAction Stop
if (-not (Test-Path $dumpPath)) {
  throw "Dump file not found: $dumpPath"
}

$containerId = (docker compose -f $composePath ps -q $Service).Trim()
if (-not $containerId) {
  throw "No container found for service '$Service'. Start it with: docker compose -f $composePath up -d"
}

$tmpDumpPath = "/tmp/wordloom_restore.dump"

# Copy dump into container

docker cp "$dumpPath" "${containerId}:${tmpDumpPath}" | Out-Null

try {
  if ($DropIfExists) {
    $terminateSql = "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$TargetDatabase' AND pid <> pg_backend_pid();"
    docker exec -e "PGPASSWORD=$Password" $containerId psql -U $User -d postgres -v ON_ERROR_STOP=1 -c $terminateSql | Out-Null
    docker exec -e "PGPASSWORD=$Password" $containerId dropdb -U $User --if-exists $TargetDatabase | Out-Null
  }

  docker exec -e "PGPASSWORD=$Password" $containerId createdb -U $User $TargetDatabase | Out-Null

  # Restore into target db (custom format). Avoid ownership/privileges to keep dev/test simple.
  docker exec -e "PGPASSWORD=$Password" $containerId pg_restore -U $User -d $TargetDatabase --no-owner --no-privileges $tmpDumpPath | Out-Null
}
finally {
  docker exec $containerId rm -f $tmpDumpPath | Out-Null
}

Write-Host "OK"
Write-Host "CONTAINER_ID=$containerId"
Write-Host "TARGET_DB=$TargetDatabase"
Write-Host "DUMP_FILE=$dumpPath"
