#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_common.sh"

REPO_ROOT="$(repo_root)"
ENV_FILE=""
IMAGE_TAG="wordloom-backend:cloud-dev"
CONTAINER_NAME="wordloom-api-cloud-dev"
HOST_PORT="30021"
CONTAINER_PORT="8000"
DETACH="1"
SKIP_BUILD="0"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/ops/cloud_release_run_container.sh --env-file <path> [--image-tag <tag>] [--container-name <name>] [--host-port <port>] [--foreground] [--skip-build]

Examples:
  bash scripts/ops/cloud_release_run_container.sh --env-file .env.cloud.dev
  bash scripts/ops/cloud_release_run_container.sh --env-file /etc/wordloom/.env.cloud.dev --image-tag wordloom-backend:sha-1234567
  bash scripts/ops/cloud_release_run_container.sh --env-file /etc/wordloom/.env.cloud.dev --image-tag wordloom-backend:cloud-dev-known-good --skip-build
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env-file)
      ENV_FILE="$2"
      shift 2
      ;;
    --image-tag)
      IMAGE_TAG="$2"
      shift 2
      ;;
    --container-name)
      CONTAINER_NAME="$2"
      shift 2
      ;;
    --host-port)
      HOST_PORT="$2"
      shift 2
      ;;
    --foreground)
      DETACH="0"
      shift
      ;;
    --skip-build)
      SKIP_BUILD="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[cloud_release_run_container] unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$ENV_FILE" ]]; then
  echo "[cloud_release_run_container] --env-file is required" >&2
  usage >&2
  exit 2
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "[cloud_release_run_container] env file not found: $ENV_FILE" >&2
  exit 1
fi

docker_cmd="$(docker_bin)"

echo "[cloud_release_run_container] repo_root=$REPO_ROOT"
echo "[cloud_release_run_container] image_tag=$IMAGE_TAG container_name=$CONTAINER_NAME host_port=$HOST_PORT"

cd "$REPO_ROOT"

if [[ "$SKIP_BUILD" == "1" ]]; then
  echo "[cloud_release_run_container] skip_build=1 using existing image"
  if ! "$docker_cmd" image inspect "$IMAGE_TAG" >/dev/null 2>&1; then
    echo "[cloud_release_run_container] image not found for --skip-build: $IMAGE_TAG" >&2
    exit 1
  fi
else
  echo "[cloud_release_run_container] building backend image"
  "$docker_cmd" build -t "$IMAGE_TAG" "$REPO_ROOT/backend"
fi

if "$docker_cmd" inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
  echo "[cloud_release_run_container] removing existing container: $CONTAINER_NAME"
  "$docker_cmd" rm -f "$CONTAINER_NAME" >/dev/null
fi

run_args=(run)
if [[ "$DETACH" == "1" ]]; then
  run_args+=( -d )
fi
run_args+=( --name "$CONTAINER_NAME" --env-file "$ENV_FILE" -p "${HOST_PORT}:${CONTAINER_PORT}" )

echo "[cloud_release_run_container] starting container"
"$docker_cmd" "${run_args[@]}" "$IMAGE_TAG"

echo "[cloud_release_run_container] container started"