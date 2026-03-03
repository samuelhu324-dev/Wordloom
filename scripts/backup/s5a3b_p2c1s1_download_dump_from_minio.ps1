param(
  [Parameter(Mandatory=$false)] [string]$ComposeFile = "docker-compose.infra.yml",
  [Parameter(Mandatory=$false)] [string]$MinioService = "minio",
  [Parameter(Mandatory=$false)] [string]$McService = "minio_mc",

  [Parameter(Mandatory=$false)] [string]$MinioUrl = "http://minio:9000",
  [Parameter(Mandatory=$false)] [string]$AccessKey = "wordloom",
  [Parameter(Mandatory=$false)] [string]$SecretKey = "wordloomwordloom",

  [Parameter(Mandatory=$false)] [string]$Bucket = "wordloom-backups-devtest",
  [Parameter(Mandatory=$true)]  [string]$ObjectKey,

  [Parameter(Mandatory=$false)] [string]$OutputFile,
  [Parameter(Mandatory=$false)] [string]$ExpectedSha256,
  [Parameter(Mandatory=$false)] [Int64]$ExpectedSizeBytes
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

$ts = [int][double]::Parse((Get-Date -UFormat %s))

if (-not $OutputFile -or $OutputFile.Trim() -eq "") {
  $OutputFile = "artifacts/_tmp_s5a3b_p2c1s1/download_$ts.dump"
}

$outputAbs = [System.IO.Path]::GetFullPath((Join-Path $repoRoot $OutputFile))
$outputAbsDir = Split-Path -Parent $outputAbs
New-Item -ItemType Directory -Force -Path $outputAbsDir | Out-Null

# Ensure MinIO/mc are up.
$rUp = Run @("docker","compose","-f",$ComposeFile,"up","-d",$MinioService,$McService)
Require-Ok $rUp "docker compose up (minio)"

# Configure mc alias.
$mcBase = @("docker","compose","-f",$ComposeFile,"run","--rm",$McService)
$rAlias = Run ($mcBase + @("alias","set","s5a3b",$MinioUrl,$AccessKey,$SecretKey))
Require-Ok $rAlias "mc alias set"

# Download to /workspace/... (container sees repo at /workspace; artifacts is mounted rw).
$repoRootNorm = (Resolve-Path -LiteralPath $repoRoot).Path
if (-not $outputAbs.StartsWith($repoRootNorm, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "OutputFile must be under repo root. output=$outputAbs repoRoot=$repoRootNorm"
}

$outputRelForContainer = $outputAbs.Substring($repoRootNorm.Length).TrimStart('\','/')
$outputPathInContainer = "/workspace/" + ($outputRelForContainer -replace "\\", "/")

$rCp = Run ($mcBase + @("cp","s5a3b/$Bucket/$ObjectKey",$outputPathInContainer))
Require-Ok $rCp "mc cp download"

# Verify on host.
if (-not (Test-Path -LiteralPath $outputAbs)) {
  throw "Download output missing on host: $outputAbs"
}

$downloadInfo = Get-Item -LiteralPath $outputAbs
$size = [Int64]$downloadInfo.Length
$sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $outputAbs).Hash.ToLowerInvariant()

$sha_ok = $true
if ($ExpectedSha256 -and $ExpectedSha256.Trim() -ne "") {
  $sha_ok = ($sha256 -eq $ExpectedSha256.Trim().ToLowerInvariant())
}

$size_ok = $true
if ($ExpectedSizeBytes -and $ExpectedSizeBytes -gt 0) {
  $size_ok = ($size -eq $ExpectedSizeBytes)
}

if (-not $sha_ok) {
  throw "SHA256 mismatch. expected=$ExpectedSha256 actual=$sha256"
}

if (-not $size_ok) {
  throw "Size mismatch. expected=$ExpectedSizeBytes actual=$size"
}

$result = [ordered]@{
  ok = $true
  bucket = $Bucket
  object_key = $ObjectKey
  output_file = $OutputFile
  sha256 = $sha256
  size_bytes = $size
  verification = [ordered]@{
    sha256_ok = $sha_ok
    size_ok = $size_ok
  }
  mc = [ordered]@{
    alias_stdout = $rAlias.Stdout.Trim()
    cp_stdout = $rCp.Stdout.Trim()
  }
}

Write-Output (ConvertTo-Json $result -Depth 10)
