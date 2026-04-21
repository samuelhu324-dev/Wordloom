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

  if [[ "$stage" == "verify" ]] && grep -q 'ACCESS_VERIFY_RESULT=FAIL' <<<"$content"; then
    printf 'access_aware_verify_failure\n'
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
    access_aware_verify_failure)
      printf 'access_aware_verify_gate\n'
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
    access_aware_verify_failure)
      ACCESS_AWARE_VERIFY_GATE="FAIL"
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

  if [[ "${ACCESS_VERIFY_OVERLAY:-0}" == "1" && ! -f "${ACCESS_VERIFY_RESULT_JSON:-}" ]]; then
    complete="false"
  fi

  printf '%s' "$complete"
}

extract_access_verify_result_from_log() {
  local log_file="$1"
  local output_path="$2"

  python - "$log_file" "$output_path" <<'PY'
from __future__ import annotations

import sys
from pathlib import Path

log_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
begin = "[cloud_release_access_verify] ACCESS_VERIFY_RESULT_JSON_BEGIN"
end = "[cloud_release_access_verify] ACCESS_VERIFY_RESULT_JSON_END"

lines = log_path.read_text(encoding="utf-8").splitlines()
capturing = False
payload_lines: list[str] = []
for line in lines:
    if line.strip() == begin:
        capturing = True
        payload_lines.clear()
        continue
    if line.strip() == end:
        if not payload_lines:
            raise SystemExit(2)
        output_path.write_text("\n".join(payload_lines) + "\n", encoding="utf-8")
        raise SystemExit(0)
    if capturing:
        payload_lines.append(line)

raise SystemExit(2)
PY
}

load_access_verify_result_fields() {
  local result_json_path="$1"

  while IFS='=' read -r key value; do
    case "$key" in
      access_verify_result)
        ACCESS_VERIFY_RESULT="$value"
        ;;
      member_read_result)
        MEMBER_READ_RESULT_JSON="$value"
        ;;
      admin_read_result)
        ADMIN_READ_RESULT_JSON="$value"
        ;;
      lifecycle_mutation_result)
        LIFECYCLE_MUTATION_RESULT_JSON="$value"
        ;;
      rerendered_state_result)
        RERENDERED_STATE_RESULT_JSON="$value"
        ;;
    esac
  done < <(
    python - "$result_json_path" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
checks = payload.get("checks") or {}
ok = bool(payload.get("ok"))
print(f"access_verify_result={'PASS' if ok else 'FAIL'}")
print(f"member_read_result={json.dumps(checks.get('memberReadResult'))}")
print(f"admin_read_result={json.dumps(checks.get('adminReadResult'))}")
print(f"lifecycle_mutation_result={json.dumps(checks.get('lifecycleMutationResult'))}")
print(f"rerendered_state_result={json.dumps(checks.get('rerenderedStateResult'))}")
PY
  )
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
  "expectedHeadSha": "$(json_escape "$EXPECTED_HEAD_SHA")",
  "remoteHeadSha": "$(json_escape "$remote_head_sha")",
  "remoteBranch": "$(json_escape "$REMOTE_BRANCH")",
  "workflowCommandSummary": "$(json_escape "$WORKFLOW_COMMAND_SUMMARY")",
  "targetHostKind": "$(json_escape "$TARGET_HOST_KIND")",
  "envFilePath": "$(json_escape "$ENV_FILE")",
  "imageTag": "$(json_escape "$IMAGE_TAG")",
  "knownGoodImageTag": "$(json_escape "$KNOWN_GOOD_IMAGE_TAG")",
  "deployResult": "$(json_escape "$deploy_result")",
  "verifyResult": "$(json_escape "$verify_result")",
  "accessVerifyResult": "$(json_escape "${ACCESS_VERIFY_RESULT:-NOT_RUN}")",
  "memberReadResult": ${MEMBER_READ_RESULT_JSON:-null},
  "adminReadResult": ${ADMIN_READ_RESULT_JSON:-null},
  "lifecycleMutationResult": ${LIFECYCLE_MUTATION_RESULT_JSON:-null},
  "rerenderedStateResult": ${RERENDERED_STATE_RESULT_JSON:-null},
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
    "accessAwareVerifyGate": "$(json_escape "${ACCESS_AWARE_VERIFY_GATE:-NOT_RUN}")",
    "rollbackReadinessGate": "$(json_escape "$ROLLBACK_READINESS_GATE")"
  },
  "evidenceComplete": $evidence_complete,
  "artifacts": {
    "preflightLog": "$(json_escape "$(artifact_relpath "$PREFLIGHT_LOG")")",
    "deployLog": "$(json_escape "$(artifact_relpath "$DEPLOY_LOG")")",
    "verifyLog": "$(json_escape "$(artifact_relpath "$VERIFY_LOG")")",
    "accessVerifyResultJson": "$(json_escape "$(artifact_relpath "${ACCESS_VERIFY_RESULT_JSON:-$ARTIFACT_DIR/access_verify_result.json}")")",
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