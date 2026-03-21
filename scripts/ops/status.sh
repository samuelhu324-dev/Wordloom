#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_common.sh"

ENV_NAME="$(resolve_env_name "${1:-dev}")"
ENV_FILE="$(env_file_for "$ENV_NAME")"
REPO_ROOT="$(repo_root)"

source_env_file "$ENV_FILE"

API_PORT="${API_PORT:-30001}"
OUTBOX_METRICS_PORT="${OUTBOX_METRICS_PORT:-9108}"
UI_PORT="30002"
ES_PORT="19200"

DB_STATUS="not-running"
INFRA_ES_STATUS="not-running"

db_cid="$(container_id_for "$REPO_ROOT/docker-compose.devtest-db.yml" "wordloom-devtest" "db_devtest" || true)"
if [[ -n "$db_cid" ]]; then
  DB_STATUS="$(container_health_for "$db_cid" || echo unknown)"
fi

es_cid="$(container_id_for "$REPO_ROOT/docker-compose.infra.yml" "wordloom-v3" "es" || true)"
if [[ -n "$es_cid" ]]; then
  INFRA_ES_STATUS="$(container_health_for "$es_cid" || echo unknown)"
fi

api_code="$(http_code "http://127.0.0.1:${API_PORT}/api/v1/health" || true)"
worker_health_code="$(http_code "http://127.0.0.1:${OUTBOX_METRICS_PORT}/healthz" || true)"
worker_ready_code="$(http_code "http://127.0.0.1:${OUTBOX_METRICS_PORT}/readyz" || true)"
ui_code="$(http_code "http://127.0.0.1:${UI_PORT}" || true)"
es_code="$(http_code "http://127.0.0.1:${ES_PORT}" || true)"

echo "[ops/status] env=$ENV_NAME"
print_kv "env_file" "$ENV_FILE"
print_kv "db_container" "$DB_STATUS"
print_kv "infra_es" "$INFRA_ES_STATUS"
print_kv "api_health" "${api_code:-000}"
print_kv "worker_healthz" "${worker_health_code:-000}"
print_kv "worker_readyz" "${worker_ready_code:-000}"
print_kv "ui_http" "${ui_code:-000}"
print_kv "es_http" "${es_code:-000}"

if [[ "${SEARCH_OUTBOX_WORKER_ENABLED:-0}" == "0" ]]; then
  echo "[ops/status] worker runtime is disabled by env (SEARCH_OUTBOX_WORKER_ENABLED=0)"
fi