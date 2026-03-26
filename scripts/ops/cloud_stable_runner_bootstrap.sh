#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bash scripts/ops/cloud_stable_runner_bootstrap.sh \
    --ssh-host <host> \
    --ssh-user <user> \
    [--ssh-port <port>] \
    [--ssh-identity-file <path>] \
    [--repo <owner/repo>] \
    [--runner-name <name>] \
    [--runner-labels <csv>] \
    [--runner-version <version>] \
    [--install-dir <dir>] \
    [--service-user <user>] \
    [--artifact-dir <dir>]

Purpose:
  Bootstrap a Linux GitHub Actions self-hosted runner on a stable cloud host
  without baking registration tokens into the repository or Terraform state.
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
REPO=""
RUNNER_NAME="wordloom-cloud-dev-runner"
RUNNER_LABELS="s4d-cloud,cloud-dev,release"
RUNNER_VERSION="2.328.0"
INSTALL_DIR="/opt/actions-runner/s4d-cloud"
SERVICE_USER=""
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
    --repo)
      REPO="$2"
      shift 2
      ;;
    --runner-name)
      RUNNER_NAME="$2"
      shift 2
      ;;
    --runner-labels)
      RUNNER_LABELS="$2"
      shift 2
      ;;
    --runner-version)
      RUNNER_VERSION="$2"
      shift 2
      ;;
    --install-dir)
      INSTALL_DIR="$2"
      shift 2
      ;;
    --service-user)
      SERVICE_USER="$2"
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

if [[ -z "$SERVICE_USER" ]]; then
  SERVICE_USER="$SSH_USER"
fi

if [[ -z "$ARTIFACT_DIR" ]]; then
  ARTIFACT_DIR="artifacts/_tmp_s4d4c_cloud_runner_bootstrap/$(timestamp_utc)"
fi
mkdir -p "$ARTIFACT_DIR"

require_cmd gh
require_cmd ssh
require_cmd tee

if [[ -z "$REPO" ]]; then
  REPO="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"
fi

REGISTRATION_TOKEN="$(gh api -X POST "repos/${REPO}/actions/runners/registration-token" --jq .token)"

SSH_OPTS=(-p "$SSH_PORT" -o BatchMode=yes -o StrictHostKeyChecking=accept-new)
if [[ -n "$SSH_IDENTITY_FILE" ]]; then
  SSH_OPTS+=(-i "$SSH_IDENTITY_FILE")
fi

REMOTE_LOG="$ARTIFACT_DIR/remote-bootstrap.log"

ssh "${SSH_OPTS[@]}" "${SSH_USER}@${SSH_HOST}" \
  "REPO=$(printf '%q' "$REPO") RUNNER_NAME=$(printf '%q' "$RUNNER_NAME") RUNNER_LABELS=$(printf '%q' "$RUNNER_LABELS") RUNNER_VERSION=$(printf '%q' "$RUNNER_VERSION") INSTALL_DIR=$(printf '%q' "$INSTALL_DIR") SERVICE_USER=$(printf '%q' "$SERVICE_USER") REGISTRATION_TOKEN=$(printf '%q' "$REGISTRATION_TOKEN") bash -s" <<'REMOTE' | tee "$REMOTE_LOG"
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl git jq tar unzip docker.io python3 python-is-python3
sudo systemctl enable docker
sudo systemctl start docker

sudo mkdir -p "$INSTALL_DIR"
sudo chown -R "$SERVICE_USER":"$SERVICE_USER" "$INSTALL_DIR"
cd "$INSTALL_DIR"

archive="actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz"
download_url="https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/${archive}"

if [[ ! -x "./config.sh" || "$(cat .runner-version 2>/dev/null || true)" != "$RUNNER_VERSION" ]]; then
  tmp_dir="$(mktemp -d)"
  trap 'rm -rf "$tmp_dir"' EXIT
  curl -fsSL "$download_url" -o "$tmp_dir/$archive"
  tar -xzf "$tmp_dir/$archive" -C "$tmp_dir"
  cp -a "$tmp_dir/." "$INSTALL_DIR/"
  printf '%s\n' "$RUNNER_VERSION" > .runner-version
fi

./config.sh --url "https://github.com/${REPO}" --token "$REGISTRATION_TOKEN" --name "$RUNNER_NAME" --labels "$RUNNER_LABELS" --unattended --replace
sudo ./svc.sh stop || true
sudo ./svc.sh uninstall || true
sudo ./svc.sh install "$SERVICE_USER"
sudo ./svc.sh start
sudo ./svc.sh status || true

echo "runner_name=$RUNNER_NAME"
echo "runner_labels=$RUNNER_LABELS"
echo "install_dir=$INSTALL_DIR"
echo "docker_version=$(docker --version 2>/dev/null || echo missing)"
echo "git_version=$(git --version 2>/dev/null || echo missing)"
REMOTE

cat > "$ARTIFACT_DIR/bootstrap.json" <<EOF
{
  "repo": "${REPO}",
  "sshHost": "${SSH_HOST}",
  "sshPort": "${SSH_PORT}",
  "sshUser": "${SSH_USER}",
  "runnerName": "${RUNNER_NAME}",
  "runnerLabels": "${RUNNER_LABELS}",
  "runnerVersion": "${RUNNER_VERSION}",
  "installDir": "${INSTALL_DIR}",
  "serviceUser": "${SERVICE_USER}",
  "remoteLog": "${REMOTE_LOG}"
}
EOF

echo "[S4D-4C] bootstrap complete"
echo "artifact_dir=$ARTIFACT_DIR"
echo "remote_log=$REMOTE_LOG"