#!/usr/bin/env bash
set -euo pipefail

# One-command app runner (WSL)
# Starts: API + outbox worker + Next.js
# Usage:
#   ./scripts/app_up.sh dev
#   ./scripts/app_up.sh test
#   ./scripts/app_up.sh test --no-worker

ENV_NAME="${1:-dev}"
shift || true

NO_WORKER=0
NO_UI=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-worker)
      NO_WORKER=1
      shift
      ;;
    --no-ui)
      NO_UI=1
      shift
      ;;
    *)
      echo "[app_up] Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

case "$ENV_NAME" in
  dev)
    ENV_FILE="$REPO_ROOT/.env.dev"
    PROCFILE="$REPO_ROOT/Procfile.dev"
    ;;
  test)
    ENV_FILE="$REPO_ROOT/.env.test"
    PROCFILE="$REPO_ROOT/Procfile.test"
    ;;
  *)
    echo "[app_up] Unknown env '$ENV_NAME' (expected: dev|test)" >&2
    exit 2
    ;;
 esac

if [[ ! -f "$ENV_FILE" ]]; then
  echo "[app_up] env file not found: $ENV_FILE" >&2
  exit 1
fi

source_env_file() {
  local env_file="$1"
  set -a
  # shellcheck disable=SC1090
  source <(sed 's/\r$//' "$env_file")
  set +a
}

if [[ ! -f "$PROCFILE" ]]; then
  echo "[app_up] Procfile not found: $PROCFILE" >&2
  exit 1
fi

HONCHO=(honcho)
if ! command -v honcho >/dev/null 2>&1; then
  if python3 -m honcho --help >/dev/null 2>&1; then
    HONCHO=(python3 -m honcho)
  else
    cat >&2 <<'EOF'
[app_up] 'honcho' not found.

Install in WSL (recommended):
  python3 -m pip install --user honcho

Or via pipx:
  sudo apt-get update && sudo apt-get install -y pipx
  pipx install honcho
EOF
    exit 1
  fi
fi

# Export env vars to all Procfile processes.
source_env_file "$ENV_FILE"

worker_enabled_raw="${SEARCH_OUTBOX_WORKER_ENABLED:-}"
worker_enabled_normalized="$(printf '%s' "$worker_enabled_raw" | tr '[:upper:]' '[:lower:]')"
if [[ "$NO_WORKER" != "1" ]]; then
  case "$worker_enabled_normalized" in
    ""|1|true|yes|y|on)
      ;;
    0|false|no|n|off)
      echo "[app_up] SEARCH_OUTBOX_WORKER_ENABLED=$worker_enabled_raw -> starting only api + ui"
      NO_WORKER=1
      ;;
    *)
      echo "[app_up] invalid SEARCH_OUTBOX_WORKER_ENABLED='$worker_enabled_raw' in $ENV_FILE" >&2
      exit 2
      ;;
  esac
fi

cd "$REPO_ROOT"
echo "[app_up] Starting app processes ($ENV_NAME) via $(basename "$PROCFILE")"

FRONTEND_DIR="$REPO_ROOT/frontend"
if [[ ! -d "$FRONTEND_DIR" ]]; then
  echo "[app_up] frontend directory not found: $FRONTEND_DIR" >&2
  exit 1
fi

install_frontend_deps_posix() {
  if ! command -v npm >/dev/null 2>&1; then
    echo "[app_up] npm not found; please install Node.js/npm in WSL" >&2
    exit 1
  fi

  echo "[app_up] frontend dependencies missing for POSIX runtime -> installing in frontend/"
  if [[ -f "$FRONTEND_DIR/package-lock.json" ]]; then
    (cd "$FRONTEND_DIR" && npm ci)
  else
    (cd "$FRONTEND_DIR" && npm install)
  fi
}

install_frontend_deps_windows() {
  if ! command -v powershell.exe >/dev/null 2>&1; then
    echo "[app_up] powershell.exe not found; cannot prepare Windows-side frontend dependencies from WSL" >&2
    exit 1
  fi

  local frontend_dir_win
  frontend_dir_win="$(wslpath -w "$FRONTEND_DIR")"
  echo "[app_up] frontend dependencies missing for Windows npm fallback -> installing in frontend/"
  powershell.exe -NoProfile -Command "\$ErrorActionPreference='Stop'; Set-Location '$frontend_dir_win'; if (Test-Path package-lock.json) { npm.cmd ci } else { npm.cmd install }"
}

if [[ "$NO_UI" != "1" ]]; then
  if [[ -n "${WSL_DISTRO_NAME:-}" || -n "${WSL_INTEROP:-}" ]]; then
    if [[ ! -f "$FRONTEND_DIR/node_modules/.bin/cross-env.cmd" || ! -f "$FRONTEND_DIR/node_modules/.bin/next.cmd" ]]; then
      install_frontend_deps_windows
    fi
  elif [[ ! -x "$FRONTEND_DIR/node_modules/.bin/cross-env" || ! -x "$FRONTEND_DIR/node_modules/.bin/next" ]]; then
    install_frontend_deps_posix
  fi
fi

if [[ "$NO_UI" == "1" ]]; then
  echo "[app_up] --no-ui: starting only api$( [[ "$NO_WORKER" != "1" ]] && printf ' + worker' )"
  if [[ "$NO_WORKER" == "1" ]]; then
    exec "${HONCHO[@]}" start -f "$PROCFILE" api
  fi

  exec "${HONCHO[@]}" start -f "$PROCFILE" api worker_search
fi

if [[ "$NO_WORKER" == "1" ]]; then
  echo "[app_up] --no-worker: starting only api + ui"
  exec "${HONCHO[@]}" start -f "$PROCFILE" api ui
fi

exec "${HONCHO[@]}" start -f "$PROCFILE"
