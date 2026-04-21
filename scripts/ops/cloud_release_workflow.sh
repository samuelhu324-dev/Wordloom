#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_common.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/cloud_release_workflow_helpers.sh"

REPO_ROOT="$(repo_root)"
SSH_HOST=""
SSH_PORT="22"
SSH_USER=""
SSH_IDENTITY_FILE=""
REMOTE_REPO_DIR=""
REMOTE_BRANCH=""
EXPECTED_HEAD_SHA=""
ENV_FILE=""
IMAGE_TAG="wordloom-backend:cloud-dev"
KNOWN_GOOD_IMAGE_TAG=""
CONTAINER_NAME="wordloom-api-cloud-dev"
HOST_PORT="30021"
VERIFY_API_HOST="127.0.0.1"
VERIFY_API_PORT="30021"
VERIFY_MAX_WAIT_SECONDS="180"
VERIFY_POLL_INTERVAL_SECONDS="3"
ROLLBACK_ON_VERIFY_FAIL="0"
ARTIFACT_DIR=""
ROLLBACK_TRIGGER="manual_only"
SIMULATE_EVIDENCE_FAILURE=""
ACCESS_VERIFY_OVERLAY="0"

IDENTITY_AUTH_GATE="NOT_RUN"
TARGET_REACHABILITY_GATE="NOT_RUN"
DEPENDENCY_CONNECTIVITY_GATE="NOT_RUN"
RELEASE_CONTRACT_GATE="NOT_RUN"
DEPLOY_EXECUTION_GATE="NOT_RUN"
POST_CHANGE_VERIFY_GATE="NOT_RUN"
ACCESS_AWARE_VERIFY_GATE="NOT_RUN"
ROLLBACK_READINESS_GATE="NOT_RUN"

ACCESS_VERIFY_RESULT="NOT_RUN"
MEMBER_READ_RESULT_JSON="null"
ADMIN_READ_RESULT_JSON="null"
LIFECYCLE_MUTATION_RESULT_JSON="null"
RERENDERED_STATE_RESULT_JSON="null"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/ops/cloud_release_workflow.sh \
    --ssh-host <host> \
    --ssh-user <user> \
    --remote-repo-dir <path> \
    --remote-branch <branch> \
    --expected-head-sha <sha> \
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
    [--access-verify-overlay] \
    [--rollback-on-verify-fail] \
    [--simulate-evidence-failure <operator-guidance-missing>] \
    [--artifact-dir <path>]

Examples:
  bash scripts/ops/cloud_release_workflow.sh \
    --ssh-host 127.0.0.1 \
    --ssh-port 22022 \
    --ssh-user ubuntu \
    --remote-repo-dir /home/ubuntu/wordloom-v3 \
    --remote-branch main \
    --expected-head-sha <sha> \
    --env-file /etc/wordloom/.env.cloud.dev

  bash scripts/ops/cloud_release_workflow.sh \
    --ssh-host 127.0.0.1 \
    --ssh-port 22022 \
    --ssh-user ubuntu \
    --remote-repo-dir /home/ubuntu/wordloom-v3 \
    --remote-branch main \
    --expected-head-sha <sha> \
    --env-file /etc/wordloom/.env.cloud.dev \
    --known-good-image-tag wordloom-backend:cloud-dev-known-good-20260325-pass \
    --access-verify-overlay \
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
    --remote-branch)
      REMOTE_BRANCH="$2"
      shift 2
      ;;
    --expected-head-sha)
      EXPECTED_HEAD_SHA="$2"
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
    --access-verify-overlay)
      ACCESS_VERIFY_OVERLAY="1"
      shift
      ;;
    --simulate-evidence-failure)
      SIMULATE_EVIDENCE_FAILURE="$2"
      shift 2
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

if [[ "$ROLLBACK_ON_VERIFY_FAIL" == "1" && -z "$KNOWN_GOOD_IMAGE_TAG" ]]; then
  echo "[cloud_release_workflow] --known-good-image-tag is required when --rollback-on-verify-fail is set" >&2
  usage >&2
  exit 2
fi

if [[ "$ROLLBACK_ON_VERIFY_FAIL" == "1" ]]; then
  ROLLBACK_TRIGGER="verify_fail_auto"
fi

if [[ -n "$SIMULATE_EVIDENCE_FAILURE" && "$SIMULATE_EVIDENCE_FAILURE" != "operator-guidance-missing" ]]; then
  echo "[cloud_release_workflow] unsupported --simulate-evidence-failure value: $SIMULATE_EVIDENCE_FAILURE" >&2
  usage >&2
  exit 2
fi

require_cmd git
ssh_cmd="$(ssh_bin)"

LOCAL_HEAD_SHA="$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
LOCAL_BRANCH_NAME="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo HEAD)"
TIMESTAMP_UTC="$(date -u +%Y%m%dT%H%M%SZ)"

if [[ -z "$REMOTE_BRANCH" ]]; then
  if [[ "$LOCAL_BRANCH_NAME" == "HEAD" || "$LOCAL_BRANCH_NAME" == "unknown" ]]; then
    echo "[cloud_release_workflow] --remote-branch is required when the local repo is detached" >&2
    exit 2
  fi
  REMOTE_BRANCH="$LOCAL_BRANCH_NAME"
fi

if [[ -z "$EXPECTED_HEAD_SHA" || "$EXPECTED_HEAD_SHA" == "unknown" ]]; then
  EXPECTED_HEAD_SHA="$LOCAL_HEAD_SHA"
fi

if [[ -z "$ARTIFACT_DIR" ]]; then
  ARTIFACT_DIR="$REPO_ROOT/artifacts/_tmp_s4d4a_cloud_release_workflow/$TIMESTAMP_UTC"
fi

mkdir -p "$ARTIFACT_DIR"

PREFLIGHT_LOG="$ARTIFACT_DIR/preflight.log"
DEPLOY_LOG="$ARTIFACT_DIR/deploy.log"
VERIFY_LOG="$ARTIFACT_DIR/verify.log"
ROLLBACK_LOG="$ARTIFACT_DIR/rollback.log"
SUMMARY_JSON="$ARTIFACT_DIR/summary.json"
OPERATOR_GUIDANCE_TXT="$ARTIFACT_DIR/operator_guidance.txt"
ACCESS_VERIFY_RESULT_JSON="$ARTIFACT_DIR/access_verify_result.json"

TARGET_HOST_KIND="Ubuntu Server VM via SSH (${SSH_USER}@${SSH_HOST}:${SSH_PORT})"
WORKFLOW_COMMAND_BASE="bash scripts/ops/cloud_release_workflow.sh --ssh-host ${SSH_HOST} --ssh-port ${SSH_PORT} --ssh-user ${SSH_USER} --remote-repo-dir ${REMOTE_REPO_DIR} --remote-branch ${REMOTE_BRANCH} --expected-head-sha ${EXPECTED_HEAD_SHA} --env-file ${ENV_FILE} --image-tag ${IMAGE_TAG} --container-name ${CONTAINER_NAME} --host-port ${HOST_PORT}"
WORKFLOW_COMMAND_SUMMARY="$WORKFLOW_COMMAND_BASE"
ROLLBACK_WORKFLOW_COMMAND="$WORKFLOW_COMMAND_BASE"

if [[ -n "$KNOWN_GOOD_IMAGE_TAG" ]]; then
  WORKFLOW_COMMAND_SUMMARY+=" --known-good-image-tag ${KNOWN_GOOD_IMAGE_TAG}"
  ROLLBACK_WORKFLOW_COMMAND+=" --known-good-image-tag ${KNOWN_GOOD_IMAGE_TAG}"
fi
if [[ "$ROLLBACK_ON_VERIFY_FAIL" == "1" ]]; then
  WORKFLOW_COMMAND_SUMMARY+=" --rollback-on-verify-fail"
fi
if [[ "$ACCESS_VERIFY_OVERLAY" == "1" ]]; then
  WORKFLOW_COMMAND_SUMMARY+=" --access-verify-overlay"
fi
ROLLBACK_WORKFLOW_COMMAND+=" --rollback-on-verify-fail"

REMOTE_HEAD_SHA="unknown"
PREFLIGHT_RESULT="NOT_RUN"
DEPLOY_RESULT="NOT_RUN"
VERIFY_RESULT="NOT_RUN"
ROLLBACK_RESULT="SKIPPED"
FAILURE_CLASS="none"
FINAL_RESULT="FAIL"
TERMINAL_STAGE="init"
OPERATOR_ACTION="inspect_artifacts"

echo "[cloud_release_workflow] phase=S4D-4A target_head_sha=$LOCAL_HEAD_SHA remote_branch=$REMOTE_BRANCH expected_head_sha=$EXPECTED_HEAD_SHA ssh_target=${SSH_USER}@${SSH_HOST}:${SSH_PORT} artifact_dir=$(artifact_relpath "$ARTIFACT_DIR")"

PREFLIGHT_REMOTE_SCRIPT=$(cat <<EOF
printf '[preflight] remote_repo_dir=%s\n' "$REMOTE_REPO_DIR"
if ! test -d "$REMOTE_REPO_DIR"; then
  printf '[preflight] remote_repo_dir_missing=%s\n' "$REMOTE_REPO_DIR"
  exit 1
fi
if ! test -f "$ENV_FILE"; then
  printf '[preflight] env_file_missing=%s\n' "$ENV_FILE"
  exit 1
fi
printf '[preflight] env_file_ok=%s\n' "$ENV_FILE"
if ! git diff --quiet --ignore-submodules -- || ! git diff --cached --quiet --ignore-submodules --; then
  printf '[preflight] remote_repo_dirty=1\n'
  exit 1
fi
printf '[preflight] remote_branch=%s\n' "$REMOTE_BRANCH"
printf '[preflight] expected_head_sha=%s\n' "$EXPECTED_HEAD_SHA"
git fetch --quiet origin "$REMOTE_BRANCH"
if ! git rev-parse --verify "$EXPECTED_HEAD_SHA^{commit}" >/dev/null 2>&1; then
  printf '[preflight] expected_head_missing=%s\n' "$EXPECTED_HEAD_SHA"
  exit 1
fi
if ! git merge-base --is-ancestor "$EXPECTED_HEAD_SHA" "origin/$REMOTE_BRANCH"; then
  printf '[preflight] expected_head_not_on_origin_branch=%s\n' "$EXPECTED_HEAD_SHA"
  exit 1
fi
current_branch="\$(git symbolic-ref --short -q HEAD || true)"
if [[ "\$current_branch" != "$REMOTE_BRANCH" ]]; then
  if git show-ref --verify --quiet "refs/heads/$REMOTE_BRANCH"; then
    git checkout "$REMOTE_BRANCH"
  else
    git checkout -b "$REMOTE_BRANCH" "origin/$REMOTE_BRANCH"
  fi
fi
git reset --hard "$EXPECTED_HEAD_SHA"
printf '[preflight] remote_head_sha=%s\n' "\$(git rev-parse HEAD)"
EOF
)

if run_remote_step "$PREFLIGHT_LOG" "$PREFLIGHT_REMOTE_SCRIPT"; then
  PREFLIGHT_RESULT="PASS"
  IDENTITY_AUTH_GATE="PASS"
  TARGET_REACHABILITY_GATE="PASS"
  RELEASE_CONTRACT_GATE="PASS"
  REMOTE_HEAD_SHA="$(sed -n 's/^\[preflight\] remote_head_sha=//p' "$PREFLIGHT_LOG" | tail -n 1)"
else
  PREFLIGHT_RESULT="FAIL"
  TERMINAL_STAGE="preflight"
  OPERATOR_ACTION="stop_and_fix_preflight"
  FAILURE_CLASS="$(classify_failure preflight "$PREFLIGHT_LOG")"
  write_operator_guidance "$OPERATOR_ACTION" "$TERMINAL_STAGE" "$FAILURE_CLASS" "$FINAL_RESULT"
  if [[ "$FAILURE_CLASS" == "contract_validation_failure" ]]; then
    IDENTITY_AUTH_GATE="PASS"
    TARGET_REACHABILITY_GATE="PASS"
  fi
  mark_failure_gate "$FAILURE_CLASS"
  promote_evidence_failure_if_incomplete "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT"
  write_summary_json "$REMOTE_HEAD_SHA" "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT" "$FAILURE_CLASS" "$FINAL_RESULT" "$OPERATOR_ACTION" "$TERMINAL_STAGE"
  echo "[cloud_release_workflow] preflight_result=FAIL failure_class=$FAILURE_CLASS summary=$(artifact_relpath "$SUMMARY_JSON")" >&2
  exit 1
fi

if run_remote_step "$DEPLOY_LOG" "bash scripts/ops/cloud_release_run_container.sh --env-file \"$ENV_FILE\" --image-tag \"$IMAGE_TAG\" --container-name \"$CONTAINER_NAME\" --host-port \"$HOST_PORT\""; then
  DEPLOY_RESULT="PASS"
  DEPLOY_EXECUTION_GATE="PASS"
else
  DEPLOY_RESULT="FAIL"
  TERMINAL_STAGE="deploy"
  OPERATOR_ACTION="stop_and_fix_deploy"
  FAILURE_CLASS="$(classify_failure deploy "$DEPLOY_LOG")"
  write_operator_guidance "$OPERATOR_ACTION" "$TERMINAL_STAGE" "$FAILURE_CLASS" "$FINAL_RESULT"
  mark_failure_gate "$FAILURE_CLASS"
  promote_evidence_failure_if_incomplete "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT"
  write_summary_json "$REMOTE_HEAD_SHA" "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT" "$FAILURE_CLASS" "$FINAL_RESULT" "$OPERATOR_ACTION" "$TERMINAL_STAGE"
  echo "[cloud_release_workflow] deploy_result=FAIL failure_class=$FAILURE_CLASS summary=$(artifact_relpath "$SUMMARY_JSON")" >&2
  exit 1
fi

VERIFY_REMOTE_COMMAND="bash scripts/ops/cloud_release_verify.sh --env-file \"$ENV_FILE\" --container-name \"$CONTAINER_NAME\" --api-host \"$VERIFY_API_HOST\" --api-port \"$VERIFY_API_PORT\" --max-wait-seconds \"$VERIFY_MAX_WAIT_SECONDS\" --poll-interval-seconds \"$VERIFY_POLL_INTERVAL_SECONDS\""
if [[ "$ACCESS_VERIFY_OVERLAY" == "1" ]]; then
  VERIFY_REMOTE_COMMAND+=" && bash scripts/ops/cloud_release_access_verify.sh --env-file \"$ENV_FILE\" --container-name \"$CONTAINER_NAME\" --api-host \"$VERIFY_API_HOST\" --api-port \"$VERIFY_API_PORT\" --run-id \"$TIMESTAMP_UTC\""
fi

if run_remote_step "$VERIFY_LOG" "$VERIFY_REMOTE_COMMAND"; then
  VERIFY_RESULT="PASS"
  DEPENDENCY_CONNECTIVITY_GATE="PASS"
  POST_CHANGE_VERIFY_GATE="PASS"
  if [[ "$ACCESS_VERIFY_OVERLAY" == "1" ]]; then
    extract_access_verify_result_from_log "$VERIFY_LOG" "$ACCESS_VERIFY_RESULT_JSON"
    load_access_verify_result_fields "$ACCESS_VERIFY_RESULT_JSON"
    ACCESS_AWARE_VERIFY_GATE="PASS"
  fi
  FINAL_RESULT="PASS"
  TERMINAL_STAGE="verify"
  OPERATOR_ACTION="release_complete"
  write_operator_guidance "$OPERATOR_ACTION" "$TERMINAL_STAGE" "$FAILURE_CLASS" "$FINAL_RESULT"
  promote_evidence_failure_if_incomplete "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT"
  write_summary_json "$REMOTE_HEAD_SHA" "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT" "$FAILURE_CLASS" "$FINAL_RESULT" "$OPERATOR_ACTION" "$TERMINAL_STAGE"
    echo "[cloud_release_workflow] result=$FINAL_RESULT failure_class=$FAILURE_CLASS summary=$(artifact_relpath "$SUMMARY_JSON")"
  if [[ "$FAILURE_CLASS" == "evidence_capture_failure" ]]; then
    exit 1
  fi
  exit 0
fi

VERIFY_RESULT="FAIL"
TERMINAL_STAGE="verify"
FAILURE_CLASS="$(classify_failure verify "$VERIFY_LOG")"
OPERATOR_ACTION="decide_manual_rollback_or_fix_forward"
POST_CHANGE_VERIFY_GATE="FAIL"
if [[ "$FAILURE_CLASS" == "verify_failure" ]]; then
  DEPENDENCY_CONNECTIVITY_GATE="PASS"
fi
if [[ "$FAILURE_CLASS" == "access_aware_verify_failure" ]]; then
  DEPENDENCY_CONNECTIVITY_GATE="PASS"
  POST_CHANGE_VERIFY_GATE="PASS"
  extract_access_verify_result_from_log "$VERIFY_LOG" "$ACCESS_VERIFY_RESULT_JSON" || true
  if [[ -f "$ACCESS_VERIFY_RESULT_JSON" ]]; then
    load_access_verify_result_fields "$ACCESS_VERIFY_RESULT_JSON"
  fi
fi
mark_failure_gate "$FAILURE_CLASS"

if [[ "$ROLLBACK_ON_VERIFY_FAIL" == "1" && -n "$KNOWN_GOOD_IMAGE_TAG" ]]; then
  if run_remote_step "$ROLLBACK_LOG" "bash scripts/ops/cloud_release_rollback.sh --env-file \"$ENV_FILE\" --rollback-image-tag \"$KNOWN_GOOD_IMAGE_TAG\" --container-name \"$CONTAINER_NAME\" --host-port \"$HOST_PORT\" --verify-max-wait-seconds \"$VERIFY_MAX_WAIT_SECONDS\" --verify-poll-interval-seconds \"$VERIFY_POLL_INTERVAL_SECONDS\""; then
    ROLLBACK_RESULT="PASS"
    ROLLBACK_READINESS_GATE="PASS"
    FINAL_RESULT="PASS_AFTER_ROLLBACK"
    TERMINAL_STAGE="rollback"
    OPERATOR_ACTION="candidate_reverted_to_known_good"
    FAILURE_CLASS="rollback_recovery"
    write_operator_guidance "$OPERATOR_ACTION" "$TERMINAL_STAGE" "$FAILURE_CLASS" "$FINAL_RESULT"
    promote_evidence_failure_if_incomplete "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT"
    write_summary_json "$REMOTE_HEAD_SHA" "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT" "$FAILURE_CLASS" "$FINAL_RESULT" "$OPERATOR_ACTION" "$TERMINAL_STAGE"
    echo "[cloud_release_workflow] result=$FINAL_RESULT failure_class=$FAILURE_CLASS summary=$(artifact_relpath "$SUMMARY_JSON")"
    if [[ "$FAILURE_CLASS" == "evidence_capture_failure" ]]; then
      exit 1
    fi
    exit 0
  fi

  ROLLBACK_RESULT="FAIL"
  TERMINAL_STAGE="rollback"
  OPERATOR_ACTION="manual_recovery_required"
  FAILURE_CLASS="$(classify_failure rollback "$ROLLBACK_LOG")"
  mark_failure_gate "$FAILURE_CLASS"
fi

write_operator_guidance "$OPERATOR_ACTION" "$TERMINAL_STAGE" "$FAILURE_CLASS" "$FINAL_RESULT"
promote_evidence_failure_if_incomplete "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT"
write_summary_json "$REMOTE_HEAD_SHA" "$PREFLIGHT_RESULT" "$DEPLOY_RESULT" "$VERIFY_RESULT" "$ROLLBACK_RESULT" "$FAILURE_CLASS" "$FINAL_RESULT" "$OPERATOR_ACTION" "$TERMINAL_STAGE"
echo "[cloud_release_workflow] result=FAIL failure_class=$FAILURE_CLASS summary=$(artifact_relpath "$SUMMARY_JSON")" >&2
exit 1