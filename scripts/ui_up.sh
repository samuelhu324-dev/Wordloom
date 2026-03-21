#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="${1:-dev}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FRONTEND_DIR="$REPO_ROOT/frontend"

case "$ENV_NAME" in
  dev)
    NPM_SCRIPT="dev:dev"
    ;;
  test)
    NPM_SCRIPT="dev:test"
    ;;
  sandbox)
    NPM_SCRIPT="dev:sandbox"
    ;;
  *)
    echo "[ui_up] Unknown env '$ENV_NAME' (expected: dev|test|sandbox)" >&2
    exit 2
    ;;
esac

node_major_version() {
  if ! command -v node >/dev/null 2>&1; then
    echo 0
    return 0
  fi

  node -p "Number(process.versions.node.split('.')[0])" 2>/dev/null || echo 0
}

npm_path="$(command -v npm 2>/dev/null || true)"
node_major="$(node_major_version)"

if [[ -n "${WSL_DISTRO_NAME:-}" || -n "${WSL_INTEROP:-}" ]]; then
  if command -v powershell.exe >/dev/null 2>&1; then
    frontend_dir_win="$(wslpath -w "$FRONTEND_DIR")"
    exec powershell.exe -NoProfile -Command "\$ErrorActionPreference='Stop'; Set-Location '$frontend_dir_win'; npm.cmd run $NPM_SCRIPT"
  fi

  if [[ -n "$npm_path" && "$node_major" -ge 20 ]]; then
    cd "$FRONTEND_DIR"
    exec npm run "$NPM_SCRIPT"
  fi

  echo "[ui_up] WSL frontend startup requires either powershell.exe for Windows npm fallback or Linux node>=20 + npm inside WSL." >&2
  echo "[ui_up] Current npm=$npm_path node_major=$node_major" >&2
  exit 1
fi

if [[ -z "$npm_path" ]]; then
  echo "[ui_up] npm not found; please install Node.js/npm" >&2
  exit 1
fi

if [[ "$node_major" -lt 20 ]]; then
  echo "[ui_up] Node.js >= 20 is required for frontend dev startup; current major=$node_major" >&2
  exit 1
fi

cd "$FRONTEND_DIR"
exec npm run "$NPM_SCRIPT"