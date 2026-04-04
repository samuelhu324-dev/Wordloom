from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _repo_rel, _repo_root
from apply_issue_conclusion_from_plan import apply_issue_conclusion_from_plan
from plan_issue_conclusion import plan_issue_conclusion
from plan_lifecycle_pre_gate import plan_lifecycle_pre_gate


@dataclass
class GuardedIssueConclusionApplyResult:
    mode: str
    result: str
    gate_input_kind: str
    gate_input_path: str
    gate_decision_path: str
    gate_decision: str
    apply_allowed: bool
    guarded_eligibility: str
    conclusion_manifest_path: str
    conclusion_plan_path: str | None
    guarded_action: str
    apply_result_path: str | None
    warnings: list[str]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run issue conclusion apply behind the lifecycle pre-gate")
    parser.add_argument("gate_input_path", help="Path to a lifecycle-audit manifest JSON file or frozen lifecycle-audit plan JSON file")
    parser.add_argument("conclusion_manifest_path", help="Path to an issue-conclusion manifest JSON file")
    parser.add_argument("--gate-input-kind", dest="gate_input_kind", choices=["manifest", "audit-plan"], default="manifest", help="Interpret the gate input as a manifest or a frozen audit plan")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--gate-audit-plan-path", dest="gate_audit_plan_path", help="Override output path for the lifecycle-audit plan when gate input is a manifest")
    parser.add_argument("--gate-remediation-plan-path", dest="gate_remediation_plan_path", help="Override output path for the lifecycle-remediation plan")
    parser.add_argument("--gate-decision-path", dest="gate_decision_path", help="Override output path for the lifecycle pre-gate decision")
    parser.add_argument("--conclusion-plan-path", dest="conclusion_plan_path", help="Override output path for the issue-conclusion plan")
    parser.add_argument("--apply-result-path", dest="apply_result_path", help="Override output path for the underlying issue-conclusion apply result")
    parser.add_argument("--body-path", dest="body_path", help="Override output path for the applied issue body markdown")
    parser.add_argument("--guarded-result-path", dest="guarded_result_path", help="Override output path for the guarded apply result")
    parser.add_argument("--context-mode", dest="context_mode", choices=["preserve-existing", "single-generate"], default="preserve-existing", help="How to handle Context during conclusion planning when delegating behind the guard")
    parser.add_argument("--leave-open", dest="leave_open", action="store_true", help="Update the issue body but do not close an open issue")
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _load_json(path: Path, error_label: str) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse {error_label} JSON: {exc}") from exc


def _default_decision_path(gate_result: object, explicit_path: str | None, repo_root: Path) -> str:
    if explicit_path:
        return _repo_rel(_coerce_path(explicit_path, repo_root))
    audit_plan_path = str(gate_result.audit_plan_path)
    return audit_plan_path.replace("lifecycle-audit-", "lifecycle-gate-").replace("-plan.json", "-decision.json")


def _conclusion_manifest_candidates(remediation_plan: dict) -> tuple[list[str], list[str]]:
    conclusion_paths: list[str] = []
    disallowed_actions: list[str] = []

    for item in remediation_plan.get("items") or []:
        status = str(item.get("remediation_status") or "")
        if status == "skipped":
            continue
        if status != "planned":
            disallowed_actions.append(f"remediation-status:{status}")
            continue
        for step in item.get("steps") or []:
            step_status = str(step.get("status") or "")
            action_kind = str(step.get("action_kind") or "")
            if step_status != "planned":
                disallowed_actions.append(f"{action_kind or 'unknown'}:{step_status}")
                continue
            if action_kind != "plan-issue-conclusion-refresh":
                disallowed_actions.append(action_kind or "unknown")
                continue
            downstream_path = str(step.get("downstream_manifest_path") or "").strip()
            if downstream_path:
                conclusion_paths.append(downstream_path)
            else:
                disallowed_actions.append("plan-issue-conclusion-refresh:missing-downstream-manifest")

    unique_paths = list(dict.fromkeys(conclusion_paths))
    unique_disallowed = list(dict.fromkeys(disallowed_actions))
    return unique_paths, unique_disallowed


def _resolve_conclusion_manifest_path(
    *,
    repo_root: Path,
    explicit_manifest_path: Path,
    gate_result: object,
    warnings: list[str],
) -> tuple[Path | None, str, str | None]:
    if gate_result.apply_allowed:
        return explicit_manifest_path, "allowed-via-audit-pass", None

    remediation_plan_rel = str(gate_result.remediation_plan_path or "")
    if not remediation_plan_rel:
        return None, "blocked-no-remediation-plan", "Lifecycle pre-gate did not emit a remediation plan to derive an issue-conclusion manifest."

    remediation_plan_path = _coerce_path(remediation_plan_rel, repo_root)
    remediation_plan = _load_json(remediation_plan_path, "lifecycle-remediation plan")
    conclusion_paths, disallowed_actions = _conclusion_manifest_candidates(remediation_plan)

    if disallowed_actions:
        detail = ", ".join(disallowed_actions)
        return None, "blocked-mixed-remediation", f"Lifecycle remediation includes non-conclusion or non-planned follow-up actions: {detail}."

    if not conclusion_paths:
        return None, "blocked-no-conclusion-remediation", "Lifecycle remediation did not emit a planned issue-conclusion manifest."

    if len(conclusion_paths) != 1:
        detail = ", ".join(conclusion_paths)
        return None, "blocked-ambiguous-conclusion-manifest", f"Lifecycle remediation emitted multiple issue-conclusion manifests: {detail}."

    derived_manifest_path = _coerce_path(conclusion_paths[0], repo_root)
    if not derived_manifest_path.is_file():
        raise SystemExit(f"Derived issue-conclusion manifest file not found: {derived_manifest_path}")

    if explicit_manifest_path != derived_manifest_path:
        return None, "blocked-manifest-mismatch", "Explicit issue-conclusion manifest path does not match the remediation-planned issue-conclusion manifest."

    warnings.append("issue conclusion apply allowed through targeted remediation because issue-conclusion refresh is the only planned follow-up action")
    return derived_manifest_path, "allowed-via-targeted-conclusion-remediation", None


def guarded_issue_conclusion_apply(args: argparse.Namespace) -> GuardedIssueConclusionApplyResult:
    repo_root = _repo_root()
    gate_input_path = _coerce_path(args.gate_input_path, repo_root)
    explicit_conclusion_manifest_path = _coerce_path(args.conclusion_manifest_path, repo_root)
    if not gate_input_path.is_file():
        raise SystemExit(f"Lifecycle gate input file not found: {gate_input_path}")
    if not explicit_conclusion_manifest_path.is_file():
        raise SystemExit(f"Issue-conclusion manifest file not found: {explicit_conclusion_manifest_path}")

    manifest_slug = explicit_conclusion_manifest_path.stem.removeprefix("issue-conclusion-").removesuffix("-manifest")
    default_guarded_result_path = explicit_conclusion_manifest_path.with_name(f"issue-conclusion-{manifest_slug}-guarded-apply-result.json")
    guarded_result_path = _coerce_path(args.guarded_result_path, repo_root) if args.guarded_result_path else default_guarded_result_path

    with contextlib.redirect_stdout(io.StringIO()):
        gate_result = plan_lifecycle_pre_gate(
            argparse.Namespace(
                input_path=_repo_rel(gate_input_path),
                input_kind=args.gate_input_kind,
                repo=args.repo,
                audit_plan_path=args.gate_audit_plan_path,
                remediation_plan_path=args.gate_remediation_plan_path,
                decision_path=args.gate_decision_path,
            )
        )

    warnings: list[str] = []
    conclusion_plan_rel: str | None = None
    apply_result_rel: str | None = None
    guarded_action: str

    conclusion_manifest_path, guarded_eligibility, blocked_reason = _resolve_conclusion_manifest_path(
        repo_root=repo_root,
        explicit_manifest_path=explicit_conclusion_manifest_path,
        gate_result=gate_result,
        warnings=warnings,
    )

    if conclusion_manifest_path is None:
        guarded_action = "stopped-before-apply"
        if blocked_reason:
            warnings.append(blocked_reason)
    else:
        conclusion_plan_path = _coerce_path(args.conclusion_plan_path, repo_root) if args.conclusion_plan_path else conclusion_manifest_path.with_name(f"issue-conclusion-{manifest_slug}-plan.json")
        with contextlib.redirect_stdout(io.StringIO()):
            plan_issue_conclusion(
                argparse.Namespace(
                    manifest_path=_repo_rel(conclusion_manifest_path),
                    plan_path=_repo_rel(conclusion_plan_path),
                    context_mode=args.context_mode,
                )
            )
        conclusion_plan_rel = _repo_rel(conclusion_plan_path)

        with contextlib.redirect_stdout(io.StringIO()):
            apply_result = apply_issue_conclusion_from_plan(
                argparse.Namespace(
                    plan_path=conclusion_plan_rel,
                    item_index=0,
                    repo=args.repo,
                    leave_open=args.leave_open,
                    result_path=args.apply_result_path,
                    body_path=args.body_path,
                    allow_raw_live_mutation_internal=True,
                )
            )
        apply_result_rel = str(apply_result.plan_path).replace("-plan.json", f"-{apply_result.requested_id.lower()}-apply-result.json")
        if args.apply_result_path:
            apply_result_rel = _repo_rel(_coerce_path(args.apply_result_path, repo_root))
        guarded_action = "applied-after-pre-gate"
        warnings.extend(list(apply_result.warnings or []))

    result = GuardedIssueConclusionApplyResult(
        mode="issue-conclusion-guarded-apply",
        result="ok",
        gate_input_kind=args.gate_input_kind,
        gate_input_path=_repo_rel(gate_input_path),
        gate_decision_path=_default_decision_path(gate_result, args.gate_decision_path, repo_root),
        gate_decision=gate_result.decision,
        apply_allowed=gate_result.apply_allowed,
        guarded_eligibility=guarded_eligibility,
        conclusion_manifest_path=_repo_rel(conclusion_manifest_path) if conclusion_manifest_path else _repo_rel(explicit_conclusion_manifest_path),
        conclusion_plan_path=conclusion_plan_rel,
        guarded_action=guarded_action,
        apply_result_path=apply_result_rel,
        warnings=warnings,
    )
    guarded_result_path.parent.mkdir(parents=True, exist_ok=True)
    guarded_result_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        guarded_issue_conclusion_apply(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())