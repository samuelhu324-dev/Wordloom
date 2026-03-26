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
VERIFY_MAX_WAIT_SECONDS="180"
VERIFY_POLL_INTERVAL_SECONDS="3"
ROLLBACK_ON_VERIFY_FAIL="0"
ARTIFACT_DIR=""
ROLLBACK_TRIGGER="manual_only"
SIMULATE_EVIDENCE_FAILURE=""

IDENTITY_AUTH_GATE="NOT_RUN"
TARGET_REACHABILITY_GATE="NOT_RUN"
DEPENDENCY_CONNECTIVITY_GATE="NOT_RUN"
RELEASE_CONTRACT_GATE="NOT_RUN"
DEPLOY_EXECUTION_GATE="NOT_RUN"
POST_CHANGE_VERIFY_GATE="NOT_RUN"
ROLLBACK_READINESS_GATE="NOT_RUN"

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
    [--simulate-evidence-failure <operator-guidance-missing>] \
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
OPERATOR_GUIDANCE_TXT="$ARTIFACT_DIR/operator_guidance.txt"

TARGET_HOST_KIND="Ubuntu Server VM via SSH (${SSH_USER}@${SSH_HOST}:${SSH_PORT})"
WORKFLOW_COMMAND_BASE="bash scripts/ops/cloud_release_workflow.sh --ssh-host ${SSH_HOST} --ssh-port ${SSH_PORT} --ssh-user ${SSH_USER} --remote-repo-dir ${REMOTE_REPO_DIR} --env-file ${ENV_FILE} --image-tag ${IMAGE_TAG} --container-name ${CONTAINER_NAME} --host-port ${HOST_PORT}"
WORKFLOW_COMMAND_SUMMARY="$WORKFLOW_COMMAND_BASE"
ROLLBACK_WORKFLOW_COMMAND="$WORKFLOW_COMMAND_BASE"

if [[ -n "$KNOWN_GOOD_IMAGE_TAG" ]]; then
  WORKFLOW_COMMAND_SUMMARY+=" --known-good-image-tag ${KNOWN_GOOD_IMAGE_TAG}"
  ROLLBACK_WORKFLOW_COMMAND+=" --known-good-image-tag ${KNOWN_GOOD_IMAGE_TAG}"
fi
if [[ "$ROLLBACK_ON_VERIFY_FAIL" == "1" ]]; then
  WORKFLOW_COMMAND_SUMMARY+=" --rollback-on-verify-fail"
fi
ROLLBACK_WORKFLOW_COMMAND+=" --rollback-on-verify-fail"

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
  local args=( -p "$SSH_PORT" -o BatchMode=yes -o ConnectTimeout=30 -o StrictHostKeyChecking=accept-new )
  if [[ -n "$SSH_IDENTITY_FILE" ]]; then
    args+=( -i "$(normalize_ssh_identity_path "$ssh_cmd" "$SSH_IDENTITY_FILE")" )
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
  if "$ssh_cmd" "${ssh_args[@]}" "$ssh_target" "bash -lc $(printf '%q' "$remote_command")" >"$log_file" 2>&1; then
    return 0
  else
    local ssh_status=$?
    return "$ssh_status"
  fi
}

classify_failure() {
  local stage="$1"
  local log_file="$2"
  local content=""
  if [[ -f "$log_file" ]]; then
    content="$(cat "$log_file" 2>/dev/null || true)"
  fi

  if grep -qiE 'permission denied|publickey|host key verification failed|bad permissions|identity file .* not accessible|sign_and_send_pubkey|invalid format' <<<"$content"; then
    printf 'identity_auth_failure\n'
    return 0
  fi

  if [[ "$stage" != "preflight" ]] && grep -qiE 'OperationalError|could not connect|connection unexpectedly|temporary failure in name resolution|name or service not known|server closed the connection unexpectedly|timeout expired|network is unreachable' <<<"$content"; then
    printf 'dependency_connectivity_failure\n'
    return 0
  fi

  if grep -qiE 'connection refused|could not resolve hostname|no route to host|operation timed out|connection timed out|connection closed by remote host|network is unreachable' <<<"$content"; then
    printf 'target_reachability_failure\n'
    return 0
  fi

  if [[ "$stage" == "preflight" ]]; then
    printf 'contract_validation_failure\n'
    return 0
  fi

  if [[ "$stage" == "deploy" ]] && grep -qiE 'image not found|pull access denied|manifest unknown|unknown flag|env file not found|unknown argument|is required' <<<"$content"; then
    printf 'contract_validation_failure\n'
    return 0
  fi

  if [[ "$stage" == "deploy" ]] && grep -qiE 'failed to solve|build failed|error response from daemon|port is already allocated|container .* is not running|container started' <<<"$content"; then
    printf 'deploy_execution_failure\n'
    return 0
  fi

  if [[ "$stage" == "rollback" ]]; then
    printf 'rollback_failure\n'
    return 0
  fi

  if [[ "$stage" == "verify" ]]; then
    printf 'verify_failure\n'
    return 0
  fi

  printf 'deploy_execution_failure\n'
}

terminal_gate_for_failure_class() {
  local failure_class="$1"
  case "$failure_class" in
    identity_auth_failure)
      printf 'identity_auth_gate\n'
      ;;
    target_reachability_failure)
      printf 'target_reachability_gate\n'
      ;;
    dependency_connectivity_failure)
      printf 'dependency_connectivity_gate\n'
      ;;
    contract_validation_failure)
      printf 'release_contract_gate\n'
      ;;
    deploy_execution_failure)
      printf 'deploy_execution_gate\n'
      ;;
    verify_failure)
      printf 'post_change_verify_gate\n'
      ;;
    rollback_recovery)
      printf 'rollback_readiness_gate\n'
      ;;
    rollback_failure)
      printf 'rollback_readiness_gate\n'
      ;;
    evidence_capture_failure)
      printf 'evidence_capture\n'
      ;;
    none)
      printf 'none\n'
      ;;
    *)
      printf 'unknown\n'
      ;;
  esac
}

mark_failure_gate() {
  local failure_class="$1"
  case "$failure_class" in
    identity_auth_failure)
      IDENTITY_AUTH_GATE="FAIL"
      ;;
    target_reachability_failure)
      TARGET_REACHABILITY_GATE="FAIL"
      ;;
    dependency_connectivity_failure)
      DEPENDENCY_CONNECTIVITY_GATE="FAIL"
      ;;
    contract_validation_failure)
      RELEASE_CONTRACT_GATE="FAIL"
      ;;
    deploy_execution_failure)
      DEPLOY_EXECUTION_GATE="FAIL"
      ;;
    verify_failure)
      POST_CHANGE_VERIFY_GATE="FAIL"
      ;;
    rollback_failure)
      ROLLBACK_READINESS_GATE="FAIL"
      ;;
  esac
}

evidence_complete_json() {
  local preflight_result="$1"
  local deploy_result="$2"
  local verify_result="$3"
  local rollback_result="$4"
  local complete="true"

  if [[ ! -f "$OPERATOR_GUIDANCE_TXT" ]]; then
    complete="false"
  fi

  if [[ "$preflight_result" != "NOT_RUN" && ! -f "$PREFLIGHT_LOG" ]]; then
    complete="false"
  fi

  if [[ "$deploy_result" != "NOT_RUN" && ! -f "$DEPLOY_LOG" ]]; then
    complete="false"
  fi

  if [[ "$verify_result" != "NOT_RUN" && ! -f "$VERIFY_LOG" ]]; then
    complete="false"
  fi

  if [[ "$rollback_result" != "NOT_RUN" && "$rollback_result" != "SKIPPED" && ! -f "$ROLLBACK_LOG" ]]; then
    complete="false"
  fi

  printf '%s' "$complete"
}

promote_evidence_failure_if_incomplete() {
  local preflight_result="$1"
  local deploy_result="$2"
  local verify_result="$3"
  local rollback_result="$4"
  local evidence_complete

  evidence_complete="$(evidence_complete_json "$preflight_result" "$deploy_result" "$verify_result" "$rollback_result")"
  if [[ "$evidence_complete" == "true" ]]; then
    return 0
  fi

  FAILURE_CLASS="evidence_capture_failure"
  FINAL_RESULT="FAIL"
  TERMINAL_STAGE="evidence"
  OPERATOR_ACTION="inspect_artifacts"
}

write_summary_json() {
  local remote_head_sha="$1"
  local preflight_result="$2"
  local deploy_result="$3"
  local verify_result="$4"
  local rollback_result="$5"
  local failure_class="$6"
  local result="$7"
  local operator_action="$8"
  local terminal_stage="$9"
  local terminal_gate
  local evidence_complete

  terminal_gate="$(terminal_gate_for_failure_class "$failure_class")"
  evidence_complete="$(evidence_complete_json "$preflight_result" "$deploy_result" "$verify_result" "$rollback_result")"

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
  "rollbackTrigger": "$(json_escape "$ROLLBACK_TRIGGER")",
  "operatorAction": "$(json_escape "$operator_action")",
  "terminalStage": "$(json_escape "$terminal_stage")",
  "terminalGate": "$(json_escape "$terminal_gate")",
  "failureClass": "$(json_escape "$failure_class")",
  "gateResults": {
    "identityAuthGate": "$(json_escape "$IDENTITY_AUTH_GATE")",
    "targetReachabilityGate": "$(json_escape "$TARGET_REACHABILITY_GATE")",
    "dependencyConnectivityGate": "$(json_escape "$DEPENDENCY_CONNECTIVITY_GATE")",
    "releaseContractGate": "$(json_escape "$RELEASE_CONTRACT_GATE")",
    "deployExecutionGate": "$(json_escape "$DEPLOY_EXECUTION_GATE")",
    "postChangeVerifyGate": "$(json_escape "$POST_CHANGE_VERIFY_GATE")",
    "rollbackReadinessGate": "$(json_escape "$ROLLBACK_READINESS_GATE")"
  },
  "evidenceComplete": $evidence_complete,
  "artifacts": {
    "preflightLog": "$(json_escape "$(artifact_relpath "$PREFLIGHT_LOG")")",
    "deployLog": "$(json_escape "$(artifact_relpath "$DEPLOY_LOG")")",
    "verifyLog": "$(json_escape "$(artifact_relpath "$VERIFY_LOG")")",
    "rollbackLog": "$(json_escape "$(artifact_relpath "$ROLLBACK_LOG")")",
    "operatorGuidance": "$(json_escape "$(artifact_relpath "$OPERATOR_GUIDANCE_TXT")")",
    "summaryJson": "$(json_escape "$(artifact_relpath "$SUMMARY_JSON")")"
  },
  "result": "$(json_escape "$result")"
}
EOF
}

write_operator_guidance() {
  local operator_action="$1"
  local terminal_stage="$2"
  local failure_class="$3"
  local result="$4"

  if [[ "$SIMULATE_EVIDENCE_FAILURE" == "operator-guidance-missing" ]]; then
    return 0
  fi

  cat >"$OPERATOR_GUIDANCE_TXT" <<EOF
[cloud_release_workflow] result=$result terminal_stage=$terminal_stage failure_class=$failure_class rollback_trigger=$ROLLBACK_TRIGGER operator_action=$operator_action

summary_json=$(artifact_relpath "$SUMMARY_JSON")
preflight_log=$(artifact_relpath "$PREFLIGHT_LOG")
deploy_log=$(artifact_relpath "$DEPLOY_LOG")
verify_log=$(artifact_relpath "$VERIFY_LOG")
rollback_log=$(artifact_relpath "$ROLLBACK_LOG")

rerun_workflow_command=$WORKFLOW_COMMAND_SUMMARY
rollback_workflow_command=$ROLLBACK_WORKFLOW_COMMAND
EOF

  case "$operator_action" in
    release_complete)
      cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Release verified. Keep the candidate running and retain this artifact bundle as evidence.
EOF
      ;;
    stop_and_fix_preflight)
      if [[ "$failure_class" == "identity_auth_failure" ]]; then
        cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Stop here. Fix SSH identity/auth inputs first, then rerun the same workflow command.
guidance_1=Check ssh-user, identity file path, file permissions, and host trust or known_hosts state.
guidance_2=Use preflight.log to confirm whether the first failure was key access, auth rejection, or host verification.
EOF
      elif [[ "$failure_class" == "target_reachability_failure" ]]; then
        cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Stop here. Fix target reachability first, then rerun the same workflow command.
guidance_1=Check port forwarding, SSH listener availability, port number, and the operator host network path to the target.
guidance_2=Use preflight.log to confirm whether the failure was connection refused, timeout, DNS resolution, or another transport-level error.
EOF
      elif [[ "$failure_class" == "contract_validation_failure" ]]; then
        cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Stop here. Fix remote contract inputs first, then rerun the same workflow command.
guidance_1=Check remote_repo_dir, env_file path, and any required workflow inputs referenced by preflight.
guidance_2=Use preflight.log to confirm which contract check failed before rerunning.
EOF
      else
        cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Stop here. Fix SSH or remote contract issues first, then rerun the same workflow command.
EOF
      fi
      ;;
    stop_and_fix_deploy)
      if [[ "$failure_class" == "deploy_execution_failure" ]]; then
        cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Stop here. Fix deploy execution issues first, then rerun the same workflow command.
guidance_1=Inspect deploy.log for image build errors, docker run failures, host-port bind conflicts, or container startup failures.
guidance_2=If deploy failed after image build succeeded, check whether the target host port, container name, or runtime prerequisites are already in use.
EOF
      else
        cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Stop here. Inspect deploy.log for image/build/container startup issues, fix them, then rerun the same workflow command.
EOF
      fi
      ;;
    decide_manual_rollback_or_fix_forward)
      if [[ "$failure_class" == "dependency_connectivity_failure" ]]; then
        cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Candidate reached runtime but could not reach a required dependency. Do not retry blindly.
guidance_1=Inspect verify.log for DB, registry, DNS, or other upstream connectivity errors before deciding whether to keep the candidate for debugging.
guidance_2=Prioritize dependency reachability, credentials, security rules, and env-target correctness before the next deploy attempt.
EOF
        if [[ -n "$KNOWN_GOOD_IMAGE_TAG" ]]; then
          cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF
guidance_3=If the candidate should be removed, rerun with rollback armed using: $ROLLBACK_WORKFLOW_COMMAND
EOF
        else
          cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF
guidance_3=Before using workflow-driven rollback, provide a known-good image tag and rerun with --known-good-image-tag <tag> --rollback-on-verify-fail.
EOF
        fi
      elif [[ "$failure_class" == "verify_failure" ]]; then
        cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Candidate appears deployed, but post-change verify did not pass. Do not retry blindly.
guidance_1=Inspect verify.log to determine whether health/read probes, routing, port selection, or post-start checks are mismatched with the deployed candidate.
guidance_2=If container_running, migration_ok, and env_guard_ok already passed, prioritize probe target, API reachability, and application-level verify expectations before the next deploy attempt.
EOF
        if [[ -n "$KNOWN_GOOD_IMAGE_TAG" ]]; then
          cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF
guidance_3=If the candidate should be removed, rerun with rollback armed using: $ROLLBACK_WORKFLOW_COMMAND
EOF
        else
          cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF
guidance_3=Before using workflow-driven rollback, provide a known-good image tag and rerun with --known-good-image-tag <tag> --rollback-on-verify-fail.
EOF
        fi
      elif [[ -n "$KNOWN_GOOD_IMAGE_TAG" ]]; then
        cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Candidate failed verify and automatic rollback was not armed. Do not retry blindly.
guidance_1=Inspect verify.log and determine whether the candidate is safe to keep for debugging.
guidance_2=If the candidate should be removed, rerun with rollback armed using: $ROLLBACK_WORKFLOW_COMMAND
EOF
      else
        cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Candidate failed verify and automatic rollback was not armed. Do not retry blindly.
guidance_1=Inspect verify.log and determine whether the candidate is safe to keep for debugging.
guidance_2=Before using workflow-driven rollback, provide a known-good image tag and rerun with --known-good-image-tag <tag> --rollback-on-verify-fail.
EOF
      fi
      ;;
    candidate_reverted_to_known_good)
      cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Verify failed for the candidate, but rollback recovered the known-good image. Keep service on known-good and investigate candidate logs before the next deploy.
guidance_1=Use verify.log to confirm why the candidate failed, then compare rollback.log to confirm the known-good image passed rollback verify on the target host and port.
guidance_2=Do not redeploy the same candidate until the candidate-specific verify failure is explained or a new image is prepared.
EOF
      ;;
    manual_recovery_required)
      if [[ "$failure_class" == "rollback_failure" ]]; then
        cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Verify failed and rollback did not recover service. Stop rollout and switch to manual recovery.
guidance_1=Inspect rollback.log for known-good image availability, rollback helper execution failures, and rollback verify failures before making another deploy attempt.
guidance_2=Confirm the intended known-good image tag exists on the target host and that the rollback host port / verify entrypoint are still valid.
guidance_3=If the failed candidate is still running, remove it or replace it with a verified known-good image before reopening traffic.
EOF
      else
        cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Verify failed and rollback did not recover service. Stop rollout and use rollback.log to restore a known-good image before any further deploy attempt.
EOF
      fi
      ;;
    *)
      cat >>"$OPERATOR_GUIDANCE_TXT" <<EOF

next_action=Inspect the artifact bundle and proceed with manual investigation.
EOF
      ;;
  esac
}

REMOTE_HEAD_SHA="unknown"
PREFLIGHT_RESULT="NOT_RUN"
DEPLOY_RESULT="NOT_RUN"
VERIFY_RESULT="NOT_RUN"
ROLLBACK_RESULT="SKIPPED"
FAILURE_CLASS="none"
FINAL_RESULT="FAIL"
TERMINAL_STAGE="init"
OPERATOR_ACTION="inspect_artifacts"

echo "[cloud_release_workflow] phase=S4D-4A target_head_sha=$LOCAL_HEAD_SHA ssh_target=${SSH_USER}@${SSH_HOST}:${SSH_PORT} artifact_dir=$(artifact_relpath "$ARTIFACT_DIR")"

if run_remote_step "$PREFLIGHT_LOG" "printf '[preflight] remote_repo_dir=%s\\n' \"$REMOTE_REPO_DIR\"; if ! test -d \"$REMOTE_REPO_DIR\"; then printf '[preflight] remote_repo_dir_missing=%s\\n' \"$REMOTE_REPO_DIR\"; exit 1; fi; if ! test -f \"$ENV_FILE\"; then printf '[preflight] env_file_missing=%s\\n' \"$ENV_FILE\"; exit 1; fi; printf '[preflight] env_file_ok=%s\\n' \"$ENV_FILE\"; printf '[preflight] remote_head_sha=%s\\n' \"\$(git rev-parse HEAD)\""; then
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

if run_remote_step "$VERIFY_LOG" "bash scripts/ops/cloud_release_verify.sh --env-file \"$ENV_FILE\" --container-name \"$CONTAINER_NAME\" --api-host \"$VERIFY_API_HOST\" --api-port \"$VERIFY_API_PORT\" --max-wait-seconds \"$VERIFY_MAX_WAIT_SECONDS\" --poll-interval-seconds \"$VERIFY_POLL_INTERVAL_SECONDS\""; then
  VERIFY_RESULT="PASS"
  DEPENDENCY_CONNECTIVITY_GATE="PASS"
  POST_CHANGE_VERIFY_GATE="PASS"
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