param(
  [Parameter(Mandatory=$false)] [string]$ComposeFile = "docker-compose.infra.yml",
  [Parameter(Mandatory=$false)] [string]$MinioService = "minio",
  [Parameter(Mandatory=$false)] [string]$McService = "minio_mc",

  [Parameter(Mandatory=$false)] [string]$MinioUrl = "http://minio:9000",
  [Parameter(Mandatory=$false)] [string]$AccessKey = "wordloom",
  [Parameter(Mandatory=$false)] [string]$SecretKey = "wordloomwordloom",

  [Parameter(Mandatory=$false)] [string]$Bucket = "wordloom-backups-devtest",
  [Parameter(Mandatory=$false)] [string]$Prefix = "s5a3a",
  [Parameter(Mandatory=$true)]  [string]$DumpFile,
  [Parameter(Mandatory=$false)] [string]$DbName = "wordloom_dev",

  [Parameter(Mandatory=$false)] [int]$ExpiryDays = 7,
  [Parameter(Mandatory=$false)] [string]$ManifestFile
)

$ErrorActionPreference = "Stop"

function Repo-Root {
  $here = $PSScriptRoot
  if (-not $here -or $here.Trim() -eq "") {
    $here = Split-Path -Parent $MyInvocation.MyCommand.Definition
  }
  $p = Resolve-Path (Join-Path $here "..\..")
  return $p.Path
}

function Run($cmdArgs) {
  $proc = Start-Process -FilePath $cmdArgs[0] -ArgumentList ($cmdArgs | Select-Object -Skip 1) -NoNewWindow -PassThru -Wait -RedirectStandardOutput "$env:TEMP\_s5a3b_out.txt" -RedirectStandardError "$env:TEMP\_s5a3b_err.txt"
  $stdout = Get-Content "$env:TEMP\_s5a3b_out.txt" -Raw
  $stderr = Get-Content "$env:TEMP\_s5a3b_err.txt" -Raw

  if ($null -eq $stdout) { $stdout = "" }
  if ($null -eq $stderr) { $stderr = "" }
  return [pscustomobject]@{ ExitCode=$proc.ExitCode; Stdout=$stdout; Stderr=$stderr }
}

function Require-Ok($r, $ctx) {
  if ($r.ExitCode -eq 0) { return }
  throw "$ctx failed (exit=$($r.ExitCode))`nSTDOUT:`n$($r.Stdout)`nSTDERR:`n$($r.Stderr)"
}

$repoRoot = Repo-Root
Set-Location $repoRoot

$dumpCandidate = Join-Path $repoRoot $DumpFile
if (-not (Test-Path -LiteralPath $dumpCandidate)) {
  throw "DumpFile not found: $dumpCandidate"
}

$dumpPath = (Resolve-Path -LiteralPath $dumpCandidate).Path
$dumpInfo = Get-Item -LiteralPath $dumpPath
$sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $dumpPath).Hash.ToLowerInvariant()
$size = [int64]$dumpInfo.Length

$repoRootNorm = (Resolve-Path -LiteralPath $repoRoot).Path
if (-not $dumpPath.StartsWith($repoRootNorm, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "DumpFile must be under repo root for container upload. dumpPath=$dumpPath repoRoot=$repoRootNorm"
}

$dumpRelForContainer = $dumpPath.Substring($repoRootNorm.Length).TrimStart("\", "/")
$dumpPathInContainer = "/workspace/" + ($dumpRelForContainer -replace "\\", "/")

$today = (Get-Date).ToString("yyyy-MM-dd")
$ts = [int][double]::Parse((Get-Date -UFormat %s))

if (-not $ManifestFile -or $ManifestFile.Trim() -eq "") {
  $ManifestFile = "artifacts/_tmp_s5a3b_p1c1s2/manifest_$ts.json"
}

$manifestAbsDir = Split-Path -Parent (Join-Path $repoRoot $ManifestFile)
New-Item -ItemType Directory -Force -Path $manifestAbsDir | Out-Null

$objectKeyDump = "$Prefix/$today/$DbName/$ts.dump"
$objectKeyManifest = "$Prefix/$today/$DbName/$ts.manifest.json"

$manifest = [ordered]@{
  kind = "s5a3b_dump_manifest"
  created_at = (Get-Date).ToUniversalTime().ToString("o")
  bucket = $Bucket
  db_name = $DbName
  dump = [ordered]@{
    object_key = $objectKeyDump
    sha256 = $sha256
    size_bytes = $size
  }
  manifest_object_key = $objectKeyManifest
}
$manifestJson = ($manifest | ConvertTo-Json -Depth 10)
Set-Content -Path (Join-Path $repoRoot $ManifestFile) -Value $manifestJson -Encoding UTF8

$manifestAbs = (Resolve-Path -LiteralPath (Join-Path $repoRoot $ManifestFile)).Path
if (-not $manifestAbs.StartsWith($repoRootNorm, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "ManifestFile must be under repo root for container upload. manifest=$manifestAbs repoRoot=$repoRootNorm"
}

$manifestRelForContainer = $manifestAbs.Substring($repoRootNorm.Length).TrimStart("\", "/")
$manifestPathInContainer = "/workspace/" + ($manifestRelForContainer -replace "\\", "/")

# Ensure MinIO is up.
$rUp = Run @("docker","compose","-f",$ComposeFile,"up","-d",$MinioService,$McService)
Require-Ok $rUp "docker compose up (minio)"

# Configure mc alias, bucket, lifecycle and upload.
$mcBase = @("docker","compose","-f",$ComposeFile,"run","--rm",$McService)

$rAlias = Run ($mcBase + @("alias","set","s5a3b",$MinioUrl,$AccessKey,$SecretKey))
Require-Ok $rAlias "mc alias set"

$rMb = Run ($mcBase + @("mb","-p","s5a3b/$Bucket"))
# mb is idempotent-ish; allow non-zero if already exists.

$rIlm = Run ($mcBase + @("ilm","add","--expiry-days",$ExpiryDays.ToString(),"s5a3b/$Bucket"))
# ilm add may fail if already exists; allow non-zero.

$rPutDump = Run ($mcBase + @("cp",$dumpPathInContainer,"s5a3b/$Bucket/$objectKeyDump"))
Require-Ok $rPutDump "mc cp dump"

$rPutManifest = Run ($mcBase + @("cp",$manifestPathInContainer,"s5a3b/$Bucket/$objectKeyManifest"))
Require-Ok $rPutManifest "mc cp manifest"

$rStatDump = Run ($mcBase + @("stat","--json","s5a3b/$Bucket/$objectKeyDump"))
Require-Ok $rStatDump "mc stat dump"

$result = [ordered]@{
  ok = $true
  bucket = $Bucket
  dump_object_key = $objectKeyDump
  manifest_object_key = $objectKeyManifest
  sha256 = $sha256
  size_bytes = $size
  manifest_file = $ManifestFile
  mc = [ordered]@{
    alias_stdout = $rAlias.Stdout.Trim()
    put_dump_stdout = $rPutDump.Stdout.Trim()
    put_manifest_stdout = $rPutManifest.Stdout.Trim()
    stat_dump_json = $rStatDump.Stdout.Trim()
  }
}

Write-Output (ConvertTo-Json $result -Depth 10)
