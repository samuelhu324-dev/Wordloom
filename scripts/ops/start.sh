#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

ENV_NAME="${1:-dev}"
shift || true

TARGET="${1:-all}"
if [[ $# -gt 0 ]]; then
  shift
fi

case "$TARGET" in
  env_prep)
    exec "$SCRIPT_DIR/env_prep.sh" "$ENV_NAME"
    ;;
  infra)
    MODE="${1:-es}"
    exec "$REPO_ROOT/scripts/infra_up.sh" "$MODE"
    ;;
  db)
    exec "$REPO_ROOT/scripts/db_up.sh"
    ;;
  app)
    exec "$REPO_ROOT/scripts/app_up.sh" "$ENV_NAME" "$@"
    ;;
  all)
    exec "$REPO_ROOT/scripts/up.sh" "$ENV_NAME" "$@"
    ;;
  *)
    cat >&2 <<'EOF'
[ops/start] Unknown target.

Usage:
  ./scripts/ops/start.sh dev env_prep
  ./scripts/ops/start.sh dev infra [es|monitoring]
  ./scripts/ops/start.sh dev db
  ./scripts/ops/start.sh dev app [--no-worker]
  ./scripts/ops/start.sh dev all [--no-worker]
EOF
    exit 2
    ;;
esac