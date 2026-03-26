#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bash scripts/ops/cloud_stable_runner_probe.sh \
    --ssh-host <host> \
    --ssh-user <user> \
    [--ssh-port <port>] \
    [--ssh-identity-file <path>] \
    [--dependency-host <host>] \
    [--dependency-port <port>] \
    [--target-ssh-host <host>] \
    [--target-ssh-port <port>] \
    [--artifact-dir <dir>]

Purpose:
  Probe a stable cloud runner host and emit a minimal JSON summary for
  GitHub reachability, dependency TCP reachability, and listener health.
EOF
}

timestamp_utc() {
  date -u +"%Y%m%dT%H%M%SZ"
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 2
  fi
}

SSH_HOST=""
SSH_PORT="22"
SSH_USER=""
SSH_IDENTITY_FILE=""
DEPENDENCY_HOST=""
DEPENDENCY_PORT="5432"
TARGET_SSH_HOST=""
TARGET_SSH_PORT="22"
ARTIFACT_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ssh-host)
      SSH_HOST="$2"
      shift 2
      ;;
    --ssh-port)
      SSH_PORT="$2"
      shift 2
      ;;
    --ssh-user)
      SSH_USER="$2"
      shift 2
      ;;
    --ssh-identity-file)
      SSH_IDENTITY_FILE="$2"
      shift 2
      ;;
    --dependency-host)
      DEPENDENCY_HOST="$2"
      shift 2
      ;;
    --dependency-port)
      DEPENDENCY_PORT="$2"
      shift 2
      ;;
    --target-ssh-host)
      TARGET_SSH_HOST="$2"
      shift 2
      ;;
    --target-ssh-port)
      TARGET_SSH_PORT="$2"
      shift 2
      ;;
    --artifact-dir)
      ARTIFACT_DIR="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$SSH_HOST" || -z "$SSH_USER" ]]; then
  echo "--ssh-host and --ssh-user are required" >&2
  usage >&2
  exit 2
fi

if [[ -z "$ARTIFACT_DIR" ]]; then
  ARTIFACT_DIR="artifacts/_tmp_s4d4c_cloud_runner_probe/$(timestamp_utc)"
fi
mkdir -p "$ARTIFACT_DIR"

require_cmd ssh

SSH_OPTS=(-p "$SSH_PORT" -o BatchMode=yes -o StrictHostKeyChecking=accept-new)
if [[ -n "$SSH_IDENTITY_FILE" ]]; then
  SSH_OPTS+=(-i "$SSH_IDENTITY_FILE")
fi

PROBE_JSON="$ARTIFACT_DIR/probe.json"

ssh "${SSH_OPTS[@]}" "${SSH_USER}@${SSH_HOST}" \
  "DEPENDENCY_HOST=$(printf '%q' "$DEPENDENCY_HOST") DEPENDENCY_PORT=$(printf '%q' "$DEPENDENCY_PORT") TARGET_SSH_HOST=$(printf '%q' "$TARGET_SSH_HOST") TARGET_SSH_PORT=$(printf '%q' "$TARGET_SSH_PORT") bash -s" <<'REMOTE' > "$PROBE_JSON"
set -euo pipefail

tcp_probe() {
  local host="$1"
  local port="$2"
  if [[ -z "$host" ]]; then
    printf 'SKIPPED'
    return 0
  fi

  if timeout 5 bash -lc "</dev/tcp/${host}/${port}" >/dev/null 2>&1; then
    printf 'PASS'
  else
    printf 'FAIL'
  fi
}

cmd_probe() {
  if command -v "$1" >/dev/null 2>&1; then
    printf 'PASS'
  else
    printf 'FAIL'
  fi
}

github_probe='FAIL'
if curl -fsSI https://github.com >/dev/null 2>&1; then
  github_probe='PASS'
fi

listener_probe='FAIL'
if pgrep -f Runner.Listener >/dev/null 2>&1; then
  listener_probe='PASS'
fi

cat <<EOF
{
  "bash": "$(cmd_probe bash)",
  "git": "$(cmd_probe git)",
  "ssh": "$(cmd_probe ssh)",
  "docker": "$(cmd_probe docker)",
  "githubReachability": "${github_probe}",
  "runnerListener": "${listener_probe}",
  "dependencyHost": "${DEPENDENCY_HOST:-}",
  "dependencyTcpReachability": "$(tcp_probe "${DEPENDENCY_HOST}" "${DEPENDENCY_PORT}")",
  "targetSshHost": "${TARGET_SSH_HOST:-}",
  "targetSshReachability": "$(tcp_probe "${TARGET_SSH_HOST}" "${TARGET_SSH_PORT}")"
}
EOF
REMOTE

echo "[S4D-4C] probe complete"
echo "probe_json=$PROBE_JSON"