param(
    [string]$RunnerHost = "3.27.164.166",
    [int]$RunnerSshPort = 22,
    [string]$RunnerUser = "ubuntu",
    [string]$IdentityFile = "$HOME\.ssh\id_ed25519",
    [string]$LocalTargetHost = "127.0.0.1",
    [int]$LocalTargetPort = 22022,
    [string]$RemoteBindHost = "127.0.0.1",
    [int]$RemoteBindPort = 22022
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $IdentityFile)) {
    throw "Identity file not found: $IdentityFile"
}

$sshArgs = @(
    "-N",
    "-T",
    "-o", "ExitOnForwardFailure=yes",
    "-o", "ServerAliveInterval=30",
    "-o", "ServerAliveCountMax=3",
    "-o", "StrictHostKeyChecking=accept-new",
    "-i", $IdentityFile,
    "-p", $RunnerSshPort,
    "-R", "${RemoteBindHost}:${RemoteBindPort}:${LocalTargetHost}:${LocalTargetPort}",
    "${RunnerUser}@${RunnerHost}"
)

Write-Host "[S4D-4C] reverse tunnel start"
Write-Host "[S4D-4C] local_target=${LocalTargetHost}:${LocalTargetPort}"
Write-Host "[S4D-4C] remote_bind=${RemoteBindHost}:${RemoteBindPort} on ${RunnerUser}@${RunnerHost}:${RunnerSshPort}"

& ssh @sshArgs