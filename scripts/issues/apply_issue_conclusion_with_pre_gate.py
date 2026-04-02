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
    parser.add_argument("--context-mode", dest="context_mode", choices=["preserve-existing", "single-generate"], default="preserve-existing", help="Pass through the issue-conclusion context rendering mode when the delegated planner is invoked")
    parser.add_argument("--leave-open", dest="leave_open", action="store_true", help="Update the issue body but do not close an open issue")
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def guarded_issue_conclusion_apply(args: argparse.Namespace) -> GuardedIssueConclusionApplyResult:
    repo_root = _repo_root()
    gate_input_path = _coerce_path(args.gate_input_path, repo_root)
    conclusion_manifest_path = _coerce_path(args.conclusion_manifest_path, repo_root)
    if not gate_input_path.is_file():
        raise SystemExit(f"Lifecycle gate input file not found: {gate_input_path}")
    if not conclusion_manifest_path.is_file():
        raise SystemExit(f"Issue-conclusion manifest file not found: {conclusion_manifest_path}")

    manifest_slug = conclusion_manifest_path.stem.removeprefix("issue-conclusion-").removesuffix("-manifest")
    default_guarded_result_path = conclusion_manifest_path.with_name(f"issue-conclusion-{manifest_slug}-guarded-apply-result.json")
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

    if not gate_result.apply_allowed:
        guarded_action = "stopped-before-apply"
        warnings.append(f"mutation blocked by lifecycle pre-gate decision: {gate_result.decision}")
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
        gate_decision_path=_repo_rel(_coerce_path(args.gate_decision_path, repo_root)) if args.gate_decision_path else gate_result.audit_plan_path.replace("lifecycle-audit-", "lifecycle-gate-").replace("-plan.json", "-decision.json"),
        gate_decision=gate_result.decision,
        apply_allowed=gate_result.apply_allowed,
        conclusion_manifest_path=_repo_rel(conclusion_manifest_path),
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