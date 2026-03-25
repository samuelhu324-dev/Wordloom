#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

ENV_FILE=""
ROLLBACK_IMAGE_TAG=""
CONTAINER_NAME="wordloom-api-cloud-dev"
HOST_PORT="30021"
VERIFY_AFTER_ROLLBACK="1"
VERIFY_API_HOST="127.0.0.1"
VERIFY_API_PORT="30021"
VERIFY_MAX_WAIT_SECONDS="45"
VERIFY_POLL_INTERVAL_SECONDS="3"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/ops/cloud_release_rollback.sh --env-file <path> --rollback-image-tag <tag> [--container-name <name>] [--host-port <port>] [--skip-verify] [--api-host <host>] [--api-port <port>] [--verify-max-wait-seconds <n>] [--verify-poll-interval-seconds <n>]

Examples:
  bash scripts/ops/cloud_release_rollback.sh --env-file /etc/wordloom/.env.cloud.dev --rollback-image-tag wordloom-backend:cloud-dev-known-good-20260324
  bash scripts/ops/cloud_release_rollback.sh --env-file /etc/wordloom/.env.cloud.dev --rollback-image-tag wordloom-backend:cloud-dev-known-good --skip-verify
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env-file)
      ENV_FILE="$2"
      shift 2
      ;;
    --rollback-image-tag)
      ROLLBACK_IMAGE_TAG="$2"
      shift 2
      ;;
    --container-name)
      CONTAINER_NAME="$2"
      shift 2
      ;;
    --host-port)
      HOST_PORT="$2"
      VERIFY_API_PORT="$2"
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
    --verify-max-wait-seconds)
      VERIFY_MAX_WAIT_SECONDS="$2"
      shift 2
      ;;
    --verify-poll-interval-seconds)
      VERIFY_POLL_INTERVAL_SECONDS="$2"
      shift 2
      ;;
    --skip-verify)
      VERIFY_AFTER_ROLLBACK="0"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[cloud_release_rollback] unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$ENV_FILE" || -z "$ROLLBACK_IMAGE_TAG" ]]; then
  echo "[cloud_release_rollback] --env-file and --rollback-image-tag are required" >&2
  usage >&2
  exit 2
fi

HEAD_SHA="$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"

echo "[cloud_release_rollback] phase=S4D-3A target_head_sha=$HEAD_SHA rollback_image_tag=$ROLLBACK_IMAGE_TAG container_name=$CONTAINER_NAME host_port=$HOST_PORT"

bash "$SCRIPT_DIR/cloud_release_run_container.sh" \
  --env-file "$ENV_FILE" \
  --image-tag "$ROLLBACK_IMAGE_TAG" \
  --container-name "$CONTAINER_NAME" \
  --host-port "$HOST_PORT" \
  --skip-build

if [[ "$VERIFY_AFTER_ROLLBACK" == "0" ]]; then
  echo "[cloud_release_rollback] CLOUD_RELEASE_ROLLBACK_RESULT=PASS verify_skipped=1"
  exit 0
fi

if bash "$SCRIPT_DIR/cloud_release_verify.sh" \
  --env-file "$ENV_FILE" \
  --container-name "$CONTAINER_NAME" \
  --api-host "$VERIFY_API_HOST" \
  --api-port "$VERIFY_API_PORT" \
  --max-wait-seconds "$VERIFY_MAX_WAIT_SECONDS" \
  --poll-interval-seconds "$VERIFY_POLL_INTERVAL_SECONDS"; then
  echo "[cloud_release_rollback] CLOUD_RELEASE_ROLLBACK_RESULT=PASS"
  exit 0
fi

echo "[cloud_release_rollback] CLOUD_RELEASE_ROLLBACK_RESULT=FAIL" >&2
exit 1