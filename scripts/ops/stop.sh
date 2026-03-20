#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_common.sh"

REPO_ROOT="$(repo_root)"
TARGET="${1:-all}"
DOCKER_CMD="$(docker_bin)"

stop_db() {
  (
    cd "$REPO_ROOT"
    "$DOCKER_CMD" compose -f docker-compose.devtest-db.yml -p wordloom-devtest down --remove-orphans
  )
}

stop_infra() {
  (
    cd "$REPO_ROOT"
    "$DOCKER_CMD" compose -f docker-compose.infra.yml down --remove-orphans
  )
}

case "$TARGET" in
  db)
    stop_db
    ;;
  infra)
    stop_infra
    ;;
  all)
    stop_db
    stop_infra
    echo "[ops/stop] Docker-managed db + infra stopped."
    echo "[ops/stop] App processes started via scripts/app_up.sh remain foreground-managed; stop them with Ctrl+C in their terminal."
    ;;
  *)
    cat >&2 <<'EOF'
[ops/stop] Unknown target.

Usage:
  ./scripts/ops/stop.sh db
  ./scripts/ops/stop.sh infra
  ./scripts/ops/stop.sh all
EOF
    exit 2
    ;;
esac