#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_common.sh"

ENV_FILE="${ENV_FILE:-}"
CONTAINER_NAME="${CONTAINER_NAME:-wordloom-api-cloud-dev}"
VERIFY_API_HOST="${VERIFY_API_HOST:-127.0.0.1}"
VERIFY_API_PORT="${VERIFY_API_PORT:-30021}"
RUN_ID="${RUN_ID:-}"
OUTPUT_PATH="${OUTPUT_PATH:-}"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/ops/cloud_release_access_verify.sh \
    [--env-file <path>] \
    [--container-name <name>] \
    [--api-host <host>] \
    [--api-port <port>] \
    [--run-id <id>] \
    [--output-path <path>]
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
    --run-id)
      RUN_ID="$2"
      shift 2
      ;;
    --output-path)
      OUTPUT_PATH="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[cloud_release_access_verify] unknown argument: $1" >&2
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

if ! "$docker_cmd" inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
  echo "[cloud_release_access_verify] container not found: $CONTAINER_NAME" >&2
  echo "[cloud_release_access_verify] ACCESS_VERIFY_RESULT=FAIL" >&2
  exit 1
fi

if [[ -z "$RUN_ID" ]]; then
  RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$(cat /proc/sys/kernel/random/uuid | cut -c1-8)"
fi

API_BASE_URL="http://${VERIFY_API_HOST}:${VERIFY_API_PORT}/api/v1"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

create_body="$TMP_DIR/create_library.json"
member_body="$TMP_DIR/member_read.json"
member_admin_deny_body="$TMP_DIR/member_admin_deny.json"
admin_body="$TMP_DIR/admin_read.json"
admin_memberships_body="$TMP_DIR/admin_memberships.json"
lifecycle_body="$TMP_DIR/lifecycle.json"
rerender_body="$TMP_DIR/rerender.json"
history_body="$TMP_DIR/history.json"

library_name="s4f2a-${RUN_ID:0:16}"
create_code="$(curl -sS -o "$create_body" -w '%{http_code}' -H 'Content-Type: application/json' -X POST -d "{\"name\":\"${library_name}\",\"description\":\"S4F-2A cloud target access verify\"}" "$API_BASE_URL/libraries")"

if [[ "$create_code" != "201" ]]; then
  echo "[cloud_release_access_verify] create_library_status=$create_code" >&2
  cat "$create_body" >&2 || true
  echo "[cloud_release_access_verify] ACCESS_VERIFY_RESULT=FAIL" >&2
  exit 1
fi

library_id="$(cat "$create_body" | $docker_cmd exec -i "$CONTAINER_NAME" python -c "import json, sys; payload = json.load(sys.stdin); library_id = str(payload.get('id') or '');
if not library_id:
    raise SystemExit('create_library_missing_id')
print(library_id)")"

member_user_id="11111111-1111-4111-8111-111111111111"
admin_user_id="22222222-2222-4222-8222-222222222222"

"$docker_cmd" exec -i -e LIBRARY_ID="$library_id" -e MEMBER_USER_ID="$member_user_id" -e ADMIN_USER_ID="$admin_user_id" "$CONTAINER_NAME" python - <<'PY'
from __future__ import annotations

import os
import uuid
from sqlalchemy import create_engine, text


def convert_to_psycopg(url: str) -> str:
    if url.startswith("postgresql+psycopg://"):
        return url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql+"):
        parts = url.split("://", 1)
        if len(parts) == 2:
            return f"postgresql+psycopg://{parts[1]}"
    return url


database_url = (os.getenv("DATABASE_URL") or "").strip()
if not database_url:
    raise SystemExit("DATABASE_URL missing")

library_id = str(uuid.UUID(os.environ["LIBRARY_ID"]))
member_user_id = str(uuid.UUID(os.environ["MEMBER_USER_ID"]))
admin_user_id = str(uuid.UUID(os.environ["ADMIN_USER_ID"]))

engine = create_engine(convert_to_psycopg(database_url), future=True)
try:
    with engine.begin() as conn:
        for user_id, role in ((member_user_id, "member"), (admin_user_id, "admin")):
            conn.execute(
                text(
                    """
                    INSERT INTO library_memberships (id, library_id, user_id, role, created_at, updated_at)
                    VALUES (:id, :library_id, :user_id, :role, TIMEZONE('utc', NOW()), TIMEZONE('utc', NOW()))
                    """
                ),
                {
                    "id": str(uuid.uuid4()),
                    "library_id": library_id,
                    "user_id": user_id,
                    "role": role,
                },
            )
        conn.execute(
            text(
                """
                INSERT INTO subscriptions (id, library_id, plan_code, state, created_at, updated_at)
                VALUES (:id, :library_id, 'trial', 'trialing', TIMEZONE('utc', NOW()), TIMEZONE('utc', NOW()))
                """
            ),
            {"id": str(uuid.uuid4()), "library_id": library_id},
        )
        conn.execute(
            text(
                """
                INSERT INTO entitlement_snapshots (id, library_id, plan_code, subscription_state, entitlements, created_at, updated_at)
                VALUES (:id, :library_id, 'trial', 'trialing', 'read_library', TIMEZONE('utc', NOW()), TIMEZONE('utc', NOW()))
                """
            ),
            {"id": str(uuid.uuid4()), "library_id": library_id},
        )
finally:
    engine.dispose()
PY

member_status="$(curl -sS -o "$member_body" -w '%{http_code}' -H "X-Dev-User-Id: $member_user_id" -H "X-Library-Id: $library_id" "$API_BASE_URL/access-context/me")"
member_admin_deny_status="$(curl -sS -o "$member_admin_deny_body" -w '%{http_code}' -H "X-Dev-User-Id: $member_user_id" -H "X-Library-Id: $library_id" "$API_BASE_URL/admin/subscriptions/$library_id")"
admin_status="$(curl -sS -o "$admin_body" -w '%{http_code}' -H "X-Dev-User-Id: $admin_user_id" -H "X-Library-Id: $library_id" "$API_BASE_URL/admin/subscriptions/$library_id")"
admin_memberships_status="$(curl -sS -o "$admin_memberships_body" -w '%{http_code}' -H "X-Dev-User-Id: $admin_user_id" -H "X-Library-Id: $library_id" "$API_BASE_URL/libraries/$library_id/memberships")"
lifecycle_status="$(curl -sS -o "$lifecycle_body" -w '%{http_code}' -H 'Content-Type: application/json' -H "X-Dev-User-Id: $admin_user_id" -H "X-Library-Id: $library_id" -X POST -d '{"event_type":"upgrade_success"}' "$API_BASE_URL/admin/subscriptions/$library_id/events")"
rerender_status="$(curl -sS -o "$rerender_body" -w '%{http_code}' -H "X-Dev-User-Id: $admin_user_id" -H "X-Library-Id: $library_id" "$API_BASE_URL/admin/subscriptions/$library_id")"
history_status="$(curl -sS -o "$history_body" -w '%{http_code}' -H "X-Dev-User-Id: $admin_user_id" -H "X-Library-Id: $library_id" "$API_BASE_URL/admin/subscriptions/$library_id/history")"

result_json="$($docker_cmd exec -i \
  -e RUN_ID="$RUN_ID" \
  -e API_BASE_URL="$API_BASE_URL" \
  -e LIBRARY_ID="$library_id" \
    -e MEMBER_USER_ID="$member_user_id" \
    -e ADMIN_USER_ID="$admin_user_id" \
  -e MEMBER_STATUS="$member_status" \
    -e MEMBER_ADMIN_DENY_STATUS="$member_admin_deny_status" \
  -e ADMIN_STATUS="$admin_status" \
    -e ADMIN_MEMBERSHIPS_STATUS="$admin_memberships_status" \
  -e LIFECYCLE_STATUS="$lifecycle_status" \
  -e RERENDER_STATUS="$rerender_status" \
  -e HISTORY_STATUS="$history_status" \
  -e MEMBER_BODY_B64="$(base64 -w0 < "$member_body")" \
    -e MEMBER_ADMIN_DENY_BODY_B64="$(base64 -w0 < "$member_admin_deny_body")" \
  -e ADMIN_BODY_B64="$(base64 -w0 < "$admin_body")" \
    -e ADMIN_MEMBERSHIPS_BODY_B64="$(base64 -w0 < "$admin_memberships_body")" \
  -e LIFECYCLE_BODY_B64="$(base64 -w0 < "$lifecycle_body")" \
  -e RERENDER_BODY_B64="$(base64 -w0 < "$rerender_body")" \
  -e HISTORY_BODY_B64="$(base64 -w0 < "$history_body")" \
  "$CONTAINER_NAME" python - <<'PY'
from __future__ import annotations

import base64
import json
import os
from datetime import datetime, timezone


def decode_payload(name: str):
    raw = os.getenv(name, "")
    if not raw:
        return {}
    try:
        return json.loads(base64.b64decode(raw).decode("utf-8"))
    except Exception:
        return {}


def normalize_roles(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def normalize_history_items(value: object) -> list[dict]:
    if not isinstance(value, dict):
        return []
    items = value.get("items")
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, dict)]


member_body = decode_payload("MEMBER_BODY_B64")
member_admin_deny_body = decode_payload("MEMBER_ADMIN_DENY_BODY_B64")
admin_body = decode_payload("ADMIN_BODY_B64")
admin_memberships_body = decode_payload("ADMIN_MEMBERSHIPS_BODY_B64")
lifecycle_body = decode_payload("LIFECYCLE_BODY_B64")
rerender_body = decode_payload("RERENDER_BODY_B64")
history_body = decode_payload("HISTORY_BODY_B64")
history_items = normalize_history_items(history_body)
membership_items = normalize_history_items(admin_memberships_body)
library_id = os.environ["LIBRARY_ID"]
member_user_id = os.environ["MEMBER_USER_ID"]
admin_user_id = os.environ["ADMIN_USER_ID"]

member_ok = (
    os.environ["MEMBER_STATUS"] == "200"
    and str(member_body.get("user_id")) == member_user_id
    and str(member_body.get("tenant_id")) == library_id
    and normalize_roles(member_body.get("roles")) == ["member"]
    and bool(member_body.get("plan_code"))
    and bool(member_body.get("subscription_state"))
    and "read_library" in list(member_body.get("entitlements") or [])
    and os.environ["MEMBER_ADMIN_DENY_STATUS"] == "403"
    and member_admin_deny_body.get("detail", {}).get("reason") == "not_admin"
)
admin_ok = (
    os.environ["ADMIN_STATUS"] == "200"
    and str(admin_body.get("library_id")) == library_id
    and bool(admin_body.get("plan_code"))
    and bool(admin_body.get("subscription_state"))
    and "read_library" in list(admin_body.get("entitlements") or [])
    and os.environ["ADMIN_MEMBERSHIPS_STATUS"] == "200"
    and any(item.get("user_id") == member_user_id and item.get("role") == "member" for item in membership_items)
    and any(item.get("user_id") == admin_user_id and item.get("role") == "admin" for item in membership_items)
)
lifecycle_ok = (
    os.environ["LIFECYCLE_STATUS"] == "200"
    and str(lifecycle_body.get("library_id")) == library_id
    and lifecycle_body.get("subscription_state") == "active"
)
rerender_ok = (
    os.environ["RERENDER_STATUS"] == "200"
    and rerender_body.get("subscription_state") == "active"
    and os.environ["HISTORY_STATUS"] == "200"
    and any(item.get("event_type") == "upgrade_success" for item in history_items)
)
passed = int(member_ok) + int(admin_ok) + int(lifecycle_ok) + int(rerender_ok)

print(json.dumps({
    "schema_version": "s4f-2c.access-verify.v1",
    "run_id": os.environ["RUN_ID"],
    "ok": bool(member_ok and admin_ok and lifecycle_ok and rerender_ok),
    "meta": {
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "api_base_url": os.environ["API_BASE_URL"],
        "library_id": library_id,
        "identityTruthSource": "backend-validated.dev-header",
        "admissionTruthSource": "persistence-backed.library_memberships",
        "membershipTruthSource": "persistence-backed.library_memberships",
        "lifecycleTruthSource": "backend.subscription_access",
    },
    "checks": {
        "memberReadResult": member_ok,
        "adminReadResult": admin_ok,
        "lifecycleMutationResult": lifecycle_ok,
        "rerenderedStateResult": rerender_ok,
    },
    "observed": {
        "memberUserId": member_user_id,
        "adminUserId": admin_user_id,
        "memberReadStatus": int(os.environ["MEMBER_STATUS"]),
        "memberAdminDenyStatus": int(os.environ["MEMBER_ADMIN_DENY_STATUS"]),
        "adminReadStatus": int(os.environ["ADMIN_STATUS"]),
        "adminMembershipsStatus": int(os.environ["ADMIN_MEMBERSHIPS_STATUS"]),
        "lifecycleMutationStatus": int(os.environ["LIFECYCLE_STATUS"]),
        "rerenderedStateStatus": int(os.environ["RERENDER_STATUS"]),
        "historyStatus": int(os.environ["HISTORY_STATUS"]),
        "memberRoles": normalize_roles(member_body.get("roles")),
        "memberAdminDenyReason": member_admin_deny_body.get("detail", {}).get("reason"),
        "adminEntitlements": list(admin_body.get("entitlements") or []),
        "adminMembershipRoles": {
            item.get("user_id"): item.get("role") for item in membership_items if item.get("user_id") in {member_user_id, admin_user_id}
        },
    },
    "summary": {
        "total": 4,
        "passed": passed,
        "failed": 4 - passed,
    },
}, indent=2))
PY
)"

if [[ -n "$OUTPUT_PATH" ]]; then
  mkdir -p "$(dirname "$OUTPUT_PATH")"
  printf '%s\n' "$result_json" > "$OUTPUT_PATH"
fi

echo "[cloud_release_access_verify] ACCESS_VERIFY_RESULT_JSON_BEGIN"
printf '%s\n' "$result_json"
echo "[cloud_release_access_verify] ACCESS_VERIFY_RESULT_JSON_END"

if printf '%s\n' "$result_json" | "$docker_cmd" exec -i "$CONTAINER_NAME" python -c "import json, sys; payload = json.load(sys.stdin); raise SystemExit(0 if payload.get('ok') else 1)"
then
  echo "[cloud_release_access_verify] ACCESS_VERIFY_RESULT=PASS"
  exit 0
fi

echo "[cloud_release_access_verify] ACCESS_VERIFY_RESULT=FAIL" >&2
exit 1