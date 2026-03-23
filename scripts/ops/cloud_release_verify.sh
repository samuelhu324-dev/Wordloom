#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_common.sh"

ENV_FILE="${ENV_FILE:-}"
CONTAINER_NAME="${CONTAINER_NAME:-wordloom-api-cloud-dev}"
API_HOST="${API_HOST:-127.0.0.1}"
API_PORT="${API_PORT:-30021}"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/ops/cloud_release_verify.sh [--env-file <path>] [--container-name <name>] [--api-host <host>] [--api-port <port>]

Examples:
  bash scripts/ops/cloud_release_verify.sh --env-file .env.cloud.dev
  bash scripts/ops/cloud_release_verify.sh --container-name wordloom-api-cloud-dev --api-port 30021
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env-file)
      ENV_FILE="$2"
      shift 2
      ;;
    --container-name)
      CONTAINER_NAME="$2"
      shift 2
      ;;
    --api-host)
      API_HOST="$2"
      shift 2
      ;;
    --api-port)
      API_PORT="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[cloud_release_verify] unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -n "$ENV_FILE" ]]; then
  source_env_file "$ENV_FILE"
fi

require_cmd curl
docker_cmd="$(docker_bin)"

HEAD_SHA="$(git rev-parse HEAD 2>/dev/null || echo unknown)"
API_BASE_URL="http://${API_HOST}:${API_PORT}/api/v1"

echo "[cloud_release_verify] phase=S4D-1A target_head_sha=$HEAD_SHA container_name=$CONTAINER_NAME api_base_url=$API_BASE_URL"

container_rc=0
if ! "$docker_cmd" inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
  echo "[cloud_release_verify] container not found: $CONTAINER_NAME" >&2
  container_rc=1
else
  running_state="$($docker_cmd inspect -f '{{.State.Running}}' "$CONTAINER_NAME" 2>/dev/null | tr -d '\r')"
  if [[ "$running_state" == "true" ]]; then
    echo "[cloud_release_verify] container_running OK"
  else
    echo "[cloud_release_verify] container_running FAIL (running=$running_state)" >&2
    container_rc=1
  fi
fi

migration_rc=0
container_logs="$($docker_cmd logs "$CONTAINER_NAME" 2>&1 | tail -n 200 || true)"
if [[ -z "$container_logs" ]]; then
  echo "[cloud_release_verify] migration/log summary unavailable" >&2
  migration_rc=1
elif grep -q '\[entrypoint\] Starting application' <<<"$container_logs"; then
  echo "[cloud_release_verify] migration_ok OK"
else
  echo "[cloud_release_verify] migration_ok FAIL (entrypoint start marker missing)" >&2
  migration_rc=1
fi

health_rc=0
health_code="$(curl -s -o /dev/null -w '%{http_code}' "$API_BASE_URL/health" 2>/dev/null || true)"
if [[ "$health_code" == "200" ]]; then
  echo "[cloud_release_verify] health_ok OK (200)"
else
  echo "[cloud_release_verify] health_ok FAIL ($health_code)" >&2
  health_rc=1
fi

read_rc=0
libraries_tmp="$(mktemp)"
trap 'rm -f "$libraries_tmp"' EXIT
libraries_code="$(curl -s -o "$libraries_tmp" -w '%{http_code}' "$API_BASE_URL/libraries" 2>/dev/null || true)"
libraries_body="$(cat "$libraries_tmp" 2>/dev/null || true)"
if [[ "$libraries_code" == "200" ]] && grep -qE '^\s*\[' <<<"$libraries_body"; then
  echo "[cloud_release_verify] read_smoke_ok OK (200 list payload)"
else
  echo "[cloud_release_verify] read_smoke_ok FAIL (code=$libraries_code)" >&2
  read_rc=1
fi

env_guard_rc=0
if grep -qE 'environment mismatch|InFailedSqlTransaction' <<<"$container_logs"; then
  echo "[cloud_release_verify] env_guard_ok FAIL (startup log contains env-guard-related error)" >&2
  env_guard_rc=1
else
  echo "[cloud_release_verify] env_guard_ok OK"
fi

if [[ "$container_rc" -eq 0 && "$migration_rc" -eq 0 && "$health_rc" -eq 0 && "$read_rc" -eq 0 && "$env_guard_rc" -eq 0 ]]; then
  echo "[cloud_release_verify] CLOUD_RELEASE_VERIFY_RESULT=PASS"
  exit 0
fi

echo "[cloud_release_verify] CLOUD_RELEASE_VERIFY_RESULT=FAIL container_rc=$container_rc migration_rc=$migration_rc health_rc=$health_rc read_rc=$read_rc env_guard_rc=$env_guard_rc" >&2
exit 1