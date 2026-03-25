#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_common.sh"

REPO_ROOT="$(repo_root)"
SSH_HOST=""
SSH_PORT="22"
SSH_USER=""
SSH_IDENTITY_FILE=""
REMOTE_REPO_DIR=""
ENV_FILE=""
IMAGE_TAG="wordloom-backend:cloud-dev"
KNOWN_GOOD_IMAGE_TAG=""
CONTAINER_NAME="wordloom-api-cloud-dev"
HOST_PORT="30021"
VERIFY_API_HOST="127.0.0.1"
VERIFY_API_PORT="30021"
VERIFY_MAX_WAIT_SECONDS="45"
VERIFY_POLL_INTERVAL_SECONDS="3"
ROLLBACK_ON_VERIFY_FAIL="0"
ARTIFACT_DIR=""

usage() {
  cat <<'EOF'
Usage:
  bash scripts/ops/cloud_release_workflow.sh \
    --ssh-host <host> \
    --ssh-user <user> \
    --remote-repo-dir <path> \
    --env-file <path> \
    [--ssh-port <port>] \
    [--ssh-identity-file <path>] \
    [--image-tag <tag>] \
    [--known-good-image-tag <tag>] \
    [--container-name <name>] \
    [--host-port <port>] \
    [--api-host <host>] \
    [--api-port <port>] \
    [--verify-max-wait-seconds <n>] \
    [--verify-poll-interval-seconds <n>] \
    [--rollback-on-verify-fail] \
    [--artifact-dir <path>]

Examples:
  bash scripts/ops/cloud_release_workflow.sh \
    --ssh-host 127.0.0.1 \
    --ssh-port 22022 \
    --ssh-user ubuntu \
    --remote-repo-dir /home/ubuntu/wordloom-v3 \
    --env-file /etc/wordloom/.env.cloud.dev

  bash scripts/ops/cloud_release_workflow.sh \
    --ssh-host 127.0.0.1 \
    --ssh-port 22022 \
    --ssh-user ubuntu \
    --remote-repo-dir /home/ubuntu/wordloom-v3 \
    --env-file /etc/wordloom/.env.cloud.dev \
    --known-good-image-tag wordloom-backend:cloud-dev-known-good-20260325-pass \
    --rollback-on-verify-fail
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ssh-host)
      SSH_HOST="$2"
      shift 2
      ;;
    --ssh-port)
      SSH_PORT="$2"
      shift 2
      ;;
    --ssh-user)
      SSH_USER="$2"
      shift 2
      ;;
    --ssh-identity-file)
      SSH_IDENTITY_FILE="$2"
      shift 2
      ;;
    --remote-repo-dir)
      REMOTE_REPO_DIR="$2"
      shift 2
      ;;
    --env-file)
      ENV_FILE="$2"
      shift 2
      ;;
    --image-tag)
      IMAGE_TAG="$2"
      shift 2
      ;;
    --known-good-image-tag)
      KNOWN_GOOD_IMAGE_TAG="$2"
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
    --rollback-on-verify-fail)
      ROLLBACK_ON_VERIFY_FAIL="1"
      shift
      ;;
    --artifact-dir)
      ARTIFACT_DIR="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[cloud_release_workflow] unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$SSH_HOST" || -z "$SSH_USER" || -z "$REMOTE_REPO_DIR" || -z "$ENV_FILE" ]]; then
  echo "[cloud_release_workflow] --ssh-host, --ssh-user, --remote-repo-dir, and --env-file are required" >&2
  usage >&2
  exit 2
fi

require_cmd ssh
require_cmd git

LOCAL_HEAD_SHA="$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
TIMESTAMP_UTC="$(date -u +%Y%m%dT%H%M%SZ)"

if [[ -z "$ARTIFACT_DIR" ]]; then
  ARTIFACT_DIR="$REPO_ROOT/artifacts/_tmp_s4d4a_cloud_release_workflow/$TIMESTAMP_UTC"
fi

mkdir -p "$ARTIFACT_DIR"

PREFLIGHT_LOG="$ARTIFACT_DIR/preflight.log"
DEPLOY_LOG="$ARTIFACT_DIR/deploy.log"
VERIFY_LOG="$ARTIFACT_DIR/verify.log"
ROLLBACK_LOG="$ARTIFACT_DIR/rollback.log"
SUMMARY_JSON="$ARTIFACT_DIR/summary.json"

TARGET_HOST_KIND="Ubuntu Server VM via SSH (${SSH_USER}@${SSH_HOST}:${SSH_PORT})"
WORKFLOW_COMMAND_SUMMARY="bash scripts/ops/cloud_release_workflow.sh --ssh-host ${SSH_HOST} --ssh-port ${SSH_PORT} --ssh-user ${SSH_USER} --remote-repo-dir ${REMOTE_REPO_DIR} --env-file ${ENV_FILE} --image-tag ${IMAGE_TAG} --container-name ${CONTAINER_NAME} --host-port ${HOST_PORT}"

if [[ -n "$KNOWN_GOOD_IMAGE_TAG" ]]; then
  WORKFLOW_COMMAND_SUMMARY+=" --known-good-image-tag ${KNOWN_GOOD_IMAGE_TAG}"
fi
if [[ "$ROLLBACK_ON_VERIFY_FAIL" == "1" ]]; then
  WORKFLOW_COMMAND_SUMMARY+=" --rollback-on-verify-fail"
fi

json_escape() {
  local raw="${1-}"
  raw="${raw//\\/\\\\}"
  raw="${raw//\"/\\\"}"
  raw="${raw//$'\n'/\\n}"
  raw="${raw//$'\r'/\\r}"
  raw="${raw//$'\t'/\\t}"
  printf '%s' "$raw"
}

artifact_relpath() {
  local path="$1"
  path="${path#"$REPO_ROOT"/}"
  printf '%s' "$path"
}

ssh_base_args() {
  local args=( -p "$SSH_PORT" -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new )
  if [[ -n "$SSH_IDENTITY_FILE" ]]; then
    args+=( -i "$SSH_IDENTITY_FILE" )
  fi
  printf '%s\n' "${args[@]}"
}

run_remote_step() {
  local log_file="$1"
  local remote_script="$2"
  local remote_command
  local ssh_target="${SSH_USER}@${SSH_HOST}"
  local ssh_args=()
  mapfile -t ssh_args < <(ssh_base_args)

  printf -v remote_command 'cd %q && %s' "$REMOTE_REPO_DIR" "$remote_script"
  if ssh "${ssh_args[@]}" "$ssh_target" "bash -lc $(printf '%q' "$remote_command")" >"$log_file" 2>&1; then
    return 0
  fi

  return $?
}

classify_failure() {
  local stage="$1"
  local log_file="$2"
  local content=""
  if [[ -f "$log_file" ]]; then
    content="$(cat "$log_file" 2>/dev/null || true)"
  fi

  if grep -qiE 'permission denied|connection refused|could not resolve hostname|no route to host|host key verification failed|operation timed out|connection timed out|connection closed by remote host' <<<"$content"; then
    printf 'ssh_connectivity\n'
    return 0
  fi

  if [[ "$stage" == "preflight" ]]; then
    printf 'preflight_contract\n'
    return 0
  fi

  if [[ "$stage" == "deploy" ]] && grep -qiE 'image not found|pull access denied|failed to solve|build failed|manifest unknown' <<<"$content"; then
    printf 'image_build_or_lookup\n'
    return 0
  fi

  if grep -qiE 'OperationalError|could not connect|connection unexpectedly|temporary failure in name resolution|name or service not known|server closed the connection unexpectedly|timeout expired' <<<"$content"; then
    printf 'dependency_connectivity\n'
    return 0
  fi

  if [[ "$stage" == "rollback" ]]; then
    printf 'rollback_recovery\n'
    return 0
  fi

  if [[ "$stage" == "verify" ]]; then
    printf 'verify_gate\n'
    return 0
  fi

  printf 'container_startup\n'
}

write_summary_json() {
  local remote_head_sha="$1"
  local preflight_result="$2"
  local deploy_result="$3"
  local verify_result="$4"
  local rollback_result="$5"
  local failure_class="$6"
  local result="$7"

  cat >"$SUMMARY_JSON" <<EOF
{
  "headSha": "$(json_escape "$LOCAL_HEAD_SHA")",
  "remoteHeadSha": "$(json_escape "$remote_head_sha")",
  "workflowCommandSummary": "$(json_escape "$WORKFLOW_COMMAND_SUMMARY")",
  "targetHostKind": "$(json_escape "$TARGET_HOST_KIND")",
  "envFilePath": "$(json_escape "$ENV_FILE")",
  "imageTag": "$(json_escape "$IMAGE_TAG")",
  "knownGoodImageTag": "$(json_escape "$KNOWN_GOOD_IMAGE_TAG")",
  "deployResult": "$(json_escape "$deploy_result")",
  "verifyResult": "$(json_escape "$verify_result")",
  "rollbackResult": "$(json_escape "$rollback_result")",
  "preflightResult": "$(json_escape "$preflight_result")",
  "failureClass": "$(json_escape "$failure_class")",
  "artifacts": {
    "preflightLog": "$(json_escape "$(artifact_relpath "$PREFLIGHT_LOG")")",
    "deployLog": "$(json_escape "$(artifact_relpath "$DEPLOY_LOG")")",
    "verifyLog": "$(json_escape "$(artifact_relpath "$VERIFY_LOG")")",
    "rollbackLog": "$(json_escape "$(artifact_relpath "$ROLLBACK_LOG")")",
    "summaryJson": "$(json_escape "$(artifact_relpath "$SUMMARY_JSON")")"
  },
  "result": "$(json_escape "$result")"
}
EOF
}

REMOTE_HEAD_SHA="unknown"
PREFLIGHT_RESULT="NOT_RUN"
DEPLOY_RESULT="NOT_RUN"
VERIFY_RESULT="NOT_RUN"
ROLLBACK_RESULT="SKIPPED"
FAILURE_CLASS="none"
FINAL_RESULT="FAIL"

echo "[cloud_release_workflow] phase=S4D-4A target_head_sha=$LOCAL_HEAD_SHA ssh_target=${SSH_USER}@${SSH_HOST}:${SSH_PORT} artifact_dir=$(artifact_relpath "$ARTIFACT_DIR")"

if run_remote_step "$PREFLIGHT_LOG" "printf '[preflight] remote_repo_dir=%s\\n' \"$REMOTE_REPO_DIR\" && test -d \"$REMOTE_REPO_DIR\" && test -f \"$ENV_FILE\" && printf '[preflight] env_file_ok=%s\\n' \"$ENV_FILE\" && printf '[preflight] remote_head_sha=%s\\n' \"\$(git rev-parse HEAD)\""; then
  PREFLIGHT_RESULT="PASS"
  REMOTE_HEAD_SHA="$(sed -n 's/^\[preflight\] remote_head_sha=//p' "$PREFLIGHT_LOG" | tail -n 1)"
else
  PREFLIGHT_RESULT="FAIL"
  FAILURE_CLASS="$(classify_failure preflight "$PREFLIGHT_LOG")"
  write_summary_json "$REMOTE_HEAD_SHA" "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT" "$FAILURE_CLASS" "$FINAL_RESULT"
  echo "[cloud_release_workflow] preflight_result=FAIL failure_class=$FAILURE_CLASS summary=$(artifact_relpath "$SUMMARY_JSON")" >&2
  exit 1
fi

if run_remote_step "$DEPLOY_LOG" "bash scripts/ops/cloud_release_run_container.sh --env-file \"$ENV_FILE\" --image-tag \"$IMAGE_TAG\" --container-name \"$CONTAINER_NAME\" --host-port \"$HOST_PORT\""; then
  DEPLOY_RESULT="PASS"
else
  DEPLOY_RESULT="FAIL"
  FAILURE_CLASS="$(classify_failure deploy "$DEPLOY_LOG")"
  write_summary_json "$REMOTE_HEAD_SHA" "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT" "$FAILURE_CLASS" "$FINAL_RESULT"
  echo "[cloud_release_workflow] deploy_result=FAIL failure_class=$FAILURE_CLASS summary=$(artifact_relpath "$SUMMARY_JSON")" >&2
  exit 1
fi

if run_remote_step "$VERIFY_LOG" "bash scripts/ops/cloud_release_verify.sh --env-file \"$ENV_FILE\" --container-name \"$CONTAINER_NAME\" --api-host \"$VERIFY_API_HOST\" --api-port \"$VERIFY_API_PORT\" --max-wait-seconds \"$VERIFY_MAX_WAIT_SECONDS\" --poll-interval-seconds \"$VERIFY_POLL_INTERVAL_SECONDS\""; then
  VERIFY_RESULT="PASS"
  FINAL_RESULT="PASS"
  write_summary_json "$REMOTE_HEAD_SHA" "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT" "$FAILURE_CLASS" "$FINAL_RESULT"
  echo "[cloud_release_workflow] result=PASS summary=$(artifact_relpath "$SUMMARY_JSON")"
  exit 0
fi

VERIFY_RESULT="FAIL"
FAILURE_CLASS="$(classify_failure verify "$VERIFY_LOG")"

if [[ "$ROLLBACK_ON_VERIFY_FAIL" == "1" && -n "$KNOWN_GOOD_IMAGE_TAG" ]]; then
  if run_remote_step "$ROLLBACK_LOG" "bash scripts/ops/cloud_release_rollback.sh --env-file \"$ENV_FILE\" --rollback-image-tag \"$KNOWN_GOOD_IMAGE_TAG\" --container-name \"$CONTAINER_NAME\" --host-port \"$HOST_PORT\" --verify-max-wait-seconds \"$VERIFY_MAX_WAIT_SECONDS\" --verify-poll-interval-seconds \"$VERIFY_POLL_INTERVAL_SECONDS\""; then
    ROLLBACK_RESULT="PASS"
    FINAL_RESULT="PASS_AFTER_ROLLBACK"
    FAILURE_CLASS="rollback_recovery"
    write_summary_json "$REMOTE_HEAD_SHA" "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT" "$FAILURE_CLASS" "$FINAL_RESULT"
    echo "[cloud_release_workflow] result=PASS_AFTER_ROLLBACK failure_class=$FAILURE_CLASS summary=$(artifact_relpath "$SUMMARY_JSON")"
    exit 0
  fi

  ROLLBACK_RESULT="FAIL"
  FAILURE_CLASS="$(classify_failure rollback "$ROLLBACK_LOG")"
fi

write_summary_json "$REMOTE_HEAD_SHA" "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT" "$FAILURE_CLASS" "$FINAL_RESULT"
echo "[cloud_release_workflow] result=FAIL failure_class=$FAILURE_CLASS summary=$(artifact_relpath "$SUMMARY_JSON")" >&2
exit 1