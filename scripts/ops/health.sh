#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_common.sh"

ENV_NAME="$(resolve_env_name "${1:-dev}")"
ENV_FILE="$(env_file_for "$ENV_NAME")"
REPO_ROOT="$(repo_root)"

require_cmd curl
source_env_file "$ENV_FILE"

API_PORT="${API_PORT:-30001}"
OUTBOX_METRICS_PORT="${OUTBOX_METRICS_PORT:-9108}"
UI_PORT="30002"
ES_PORT="19200"
SEARCH_OUTBOX_WORKER_ENABLED="${SEARCH_OUTBOX_WORKER_ENABLED:-0}"

db_cid="$(container_id_for "$REPO_ROOT/docker-compose.devtest-db.yml" "wordloom-devtest" "db_devtest")"
if [[ -z "$db_cid" ]]; then
  echo "[ops] db_devtest container not found" >&2
  exit 1
fi

db_health="$(container_health_for "$db_cid" || echo unknown)"
if [[ "$db_health" != "healthy" ]]; then
  echo "[ops] db_devtest unhealthy ($db_health)" >&2
  exit 1
fi
echo "[ops] db_devtest OK ($db_health)"

check_http_ok "api_health" "http://127.0.0.1:${API_PORT}/api/v1/health" 200
check_http_ok "ui_http" "http://127.0.0.1:${UI_PORT}" 200 307 308
check_http_ok "es_http" "http://127.0.0.1:${ES_PORT}" 200

if [[ "$SEARCH_OUTBOX_WORKER_ENABLED" == "0" ]]; then
  echo "[ops] worker runtime skipped (SEARCH_OUTBOX_WORKER_ENABLED=0)"
  exit 0
fi

check_http_ok "worker_healthz" "http://127.0.0.1:${OUTBOX_METRICS_PORT}/healthz" 200
check_http_ok "worker_readyz" "http://127.0.0.1:${OUTBOX_METRICS_PORT}/readyz" 200