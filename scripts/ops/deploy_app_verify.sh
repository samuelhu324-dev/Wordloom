#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_common.sh"

ENV_NAME="$(resolve_env_name "${1:-dev}")"
REPO_ROOT="$(repo_root)"

cd "$REPO_ROOT"

HEAD_SHA="$(git rev-parse HEAD 2>/dev/null || echo unknown)"

echo "[deploy_app_verify] phase=S4A-2A env=$ENV_NAME target_head_sha=$HEAD_SHA"

echo "[deploy_app_verify] running status.sh ($ENV_NAME)"
status_rc=0
"$SCRIPT_DIR/status.sh" "$ENV_NAME" || status_rc=$?

echo "[deploy_app_verify] running health.sh ($ENV_NAME)"
health_rc=0
"$SCRIPT_DIR/health.sh" "$ENV_NAME" || health_rc=$?

if [[ "$status_rc" -eq 0 && "$health_rc" -eq 0 ]]; then
  echo "[deploy_app_verify] POST_DEPLOY_RESULT=PASS"
  exit 0
fi

echo "[deploy_app_verify] POST_DEPLOY_RESULT=FAIL status_rc=$status_rc health_rc=$health_rc" >&2
exit 1
