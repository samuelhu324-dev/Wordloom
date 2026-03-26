#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_common.sh"

ENV_FILE="${ENV_FILE:-}"
CONTAINER_NAME="${CONTAINER_NAME:-wordloom-api-cloud-dev}"
VERIFY_API_HOST="${VERIFY_API_HOST:-127.0.0.1}"
VERIFY_API_PORT="${VERIFY_API_PORT:-30021}"
MAX_WAIT_SECONDS="${MAX_WAIT_SECONDS:-180}"
POLL_INTERVAL_SECONDS="${POLL_INTERVAL_SECONDS:-3}"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/ops/cloud_release_verify.sh [--env-file <path>] [--container-name <name>] [--api-host <host>] [--api-port <port>] [--max-wait-seconds <n>] [--poll-interval-seconds <n>]

Examples:
  bash scripts/ops/cloud_release_verify.sh --env-file .env.cloud.dev
  bash scripts/ops/cloud_release_verify.sh --container-name wordloom-api-cloud-dev --api-port 30021
  bash scripts/ops/cloud_release_verify.sh --env-file /etc/wordloom/.env.cloud.dev --max-wait-seconds 180
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
      VERIFY_API_HOST="$2"
      shift 2
      ;;
    --api-port)
      VERIFY_API_PORT="$2"
      shift 2
      ;;
    --max-wait-seconds)
      MAX_WAIT_SECONDS="$2"
      shift 2
      ;;
    --poll-interval-seconds)
      POLL_INTERVAL_SECONDS="$2"
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
API_BASE_URL="http://${VERIFY_API_HOST}:${VERIFY_API_PORT}/api/v1"
deadline_epoch="$(( $(date +%s) + MAX_WAIT_SECONDS ))"

echo "[cloud_release_verify] phase=S4D-2A target_head_sha=$HEAD_SHA container_name=$CONTAINER_NAME api_base_url=$API_BASE_URL max_wait_seconds=$MAX_WAIT_SECONDS poll_interval_seconds=$POLL_INTERVAL_SECONDS"

container_rc=1
migration_rc=1
health_rc=1
read_rc=1
env_guard_rc=0
health_code="000"
libraries_code="000"
container_logs=""
container_exit_code="unknown"
readiness_waited=0
libraries_tmp="$(mktemp)"
trap 'rm -f "$libraries_tmp"' EXIT

while true; do
  if ! "$docker_cmd" inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
    container_rc=1
    running_state="missing"
    container_logs=""
    container_exit_code="unknown"
  else
    running_state="$($docker_cmd inspect -f '{{.State.Running}}' "$CONTAINER_NAME" 2>/dev/null | tr -d '\r')"
    container_exit_code="$($docker_cmd inspect -f '{{.State.ExitCode}}' "$CONTAINER_NAME" 2>/dev/null | tr -d '\r')"
    if [[ "$running_state" == "true" ]]; then
      container_rc=0
    else
      container_rc=1
    fi
    container_logs="$($docker_cmd logs "$CONTAINER_NAME" 2>&1 | tail -n 200 || true)"
  fi

  if [[ -z "$container_logs" ]]; then
    migration_rc=1
  elif grep -q '\[entrypoint\] Starting application' <<<"$container_logs"; then
    migration_rc=0
  else
    migration_rc=1
  fi

  health_code="$(curl -s -o /dev/null -w '%{http_code}' "$API_BASE_URL/health" 2>/dev/null || true)"
  if [[ "$health_code" == "200" ]]; then
    health_rc=0
  else
    health_rc=1
  fi

  : >"$libraries_tmp"
  libraries_code="$(curl -s -o "$libraries_tmp" -w '%{http_code}' "$API_BASE_URL/libraries" 2>/dev/null || true)"
  libraries_body="$(cat "$libraries_tmp" 2>/dev/null || true)"
  if [[ "$libraries_code" == "200" ]] && grep -qE '^\s*\[' <<<"$libraries_body"; then
    read_rc=0
  else
    read_rc=1
  fi

  if grep -qE 'environment mismatch|InFailedSqlTransaction' <<<"$container_logs"; then
    env_guard_rc=1
  else
    env_guard_rc=0
  fi

  if [[ "$container_rc" -eq 0 && "$migration_rc" -eq 0 && "$health_rc" -eq 0 && "$read_rc" -eq 0 && "$env_guard_rc" -eq 0 ]]; then
    break
  fi

  now_epoch="$(date +%s)"
  if (( now_epoch >= deadline_epoch )); then
    break
  fi

  readiness_waited=1
  sleep "$POLL_INTERVAL_SECONDS"
done

if [[ "$readiness_waited" -eq 1 ]]; then
  echo "[cloud_release_verify] readiness_wait_applied max_wait_seconds=$MAX_WAIT_SECONDS"
fi

if [[ "$container_rc" -eq 0 ]]; then
  echo "[cloud_release_verify] container_running OK"
else
  if [[ "$running_state" == "missing" ]]; then
    echo "[cloud_release_verify] container not found: $CONTAINER_NAME" >&2
  else
    echo "[cloud_release_verify] container_running FAIL (running=$running_state exit_code=$container_exit_code)" >&2
  fi
fi

if [[ "$migration_rc" -eq 0 ]]; then
  echo "[cloud_release_verify] migration_ok OK"
elif [[ -z "$container_logs" ]]; then
  echo "[cloud_release_verify] migration/log summary unavailable" >&2
else
  echo "[cloud_release_verify] migration_ok FAIL (entrypoint start marker missing)" >&2
fi

if [[ "$health_rc" -eq 0 ]]; then
  echo "[cloud_release_verify] health_ok OK (200)"
else
  echo "[cloud_release_verify] health_ok FAIL ($health_code)" >&2
fi

if [[ "$read_rc" -eq 0 ]]; then
  echo "[cloud_release_verify] read_smoke_ok OK (200 list payload)"
else
  echo "[cloud_release_verify] read_smoke_ok FAIL (code=$libraries_code)" >&2
fi

if [[ "$env_guard_rc" -eq 0 ]]; then
  echo "[cloud_release_verify] env_guard_ok OK"
else
  echo "[cloud_release_verify] env_guard_ok FAIL (startup log contains env-guard-related error)" >&2
fi

if [[ "$container_rc" -ne 0 || "$migration_rc" -ne 0 || "$health_rc" -ne 0 || "$read_rc" -ne 0 || "$env_guard_rc" -ne 0 ]]; then
  if [[ -n "$container_logs" ]]; then
    echo "[cloud_release_verify] recent_log_tail_begin" >&2
    printf '%s\n' "$container_logs" >&2
    echo "[cloud_release_verify] recent_log_tail_end" >&2
  fi
fi

if [[ "$container_rc" -eq 0 && "$migration_rc" -eq 0 && "$health_rc" -eq 0 && "$read_rc" -eq 0 && "$env_guard_rc" -eq 0 ]]; then
  echo "[cloud_release_verify] CLOUD_RELEASE_VERIFY_RESULT=PASS"
  exit 0
fi

echo "[cloud_release_verify] CLOUD_RELEASE_VERIFY_RESULT=FAIL container_rc=$container_rc migration_rc=$migration_rc health_rc=$health_rc read_rc=$read_rc env_guard_rc=$env_guard_rc" >&2
exit 1