#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_common.sh"

REPO_ROOT="$(repo_root)"
TARGET="${1:-db}"
TAIL_LINES="${2:-150}"
DOCKER_CMD="$(docker_bin)"

run_logs() {
  local compose_file="$1"
  local project_name="$2"
  local service_name="$3"

  (
    cd "$REPO_ROOT"
    exec "$DOCKER_CMD" compose -f "$compose_file" -p "$project_name" logs -f --tail "$TAIL_LINES" "$service_name"
  )
}

case "$TARGET" in
  db)
    run_logs "docker-compose.devtest-db.yml" "wordloom-devtest" "db_devtest"
    ;;
  es|jaeger|minio|minio_mc|prometheus|grafana)
    run_logs "docker-compose.infra.yml" "wordloom-v3" "$TARGET"
    ;;
  infra)
    (
      cd "$REPO_ROOT"
      exec "$DOCKER_CMD" compose -f docker-compose.infra.yml -p wordloom-v3 logs -f --tail "$TAIL_LINES"
    )
    ;;
  app)
    echo "[ops/logs] App processes are started in the foreground via honcho from scripts/app_up.sh." >&2
    echo "[ops/logs] Use the original app terminal for live logs, or rerun scripts/ops/start.sh <env> app in a dedicated terminal." >&2
    exit 2
    ;;
  *)
    cat >&2 <<'EOF'
[ops/logs] Unknown target.

Usage:
  ./scripts/ops/logs.sh db [tail]
  ./scripts/ops/logs.sh es [tail]
  ./scripts/ops/logs.sh infra [tail]
  ./scripts/ops/logs.sh minio [tail]
  ./scripts/ops/logs.sh app
EOF
    exit 2
    ;;
esac