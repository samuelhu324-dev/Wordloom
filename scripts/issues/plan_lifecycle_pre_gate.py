from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _repo_rel, _repo_root
from plan_lifecycle_audit import plan_lifecycle_audit
from plan_lifecycle_remediation import plan_lifecycle_remediation


@dataclass
class GatePolicy:
    warning_behavior: str
    blocked_behavior: str
    reconciliation_behavior: str
    error_behavior: str


@dataclass
class GateSummary:
    pass_count: int
    warning_count: int
    blocked_count: int
    reconciliation_count: int
    error_count: int


@dataclass
class GateDecisionItem:
    requested_id: str
    source_log_path: str
    issue_number: int | None
    issue_url: str | None
    audit_status: str
    gate_status: str
    apply_allowed: bool
    remediation_status: str | None
    remediation_step_count: int
    remediation_plan_path: str | None
    reason: str


@dataclass
class LifecyclePreGateDecision:
    mode: str
    result: str
    selection_input: str
    operation: str
    manifest_path: str
    audit_plan_path: str
    remediation_plan_path: str | None
    decision: str
    apply_allowed: bool
    decision_reason: str
    policy: GatePolicy
    summary: GateSummary
    warnings: list[str]
    items: list[GateDecisionItem]


DEFAULT_POLICY = GatePolicy(
    warning_behavior="stop-and-plan-remediation",
    blocked_behavior="stop-and-plan-remediation",
    reconciliation_behavior="hard-fail-before-mutation",
    error_behavior="hard-fail-before-mutation",
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan one lifecycle pre-gate decision from a manifest")
    parser.add_argument("input_path", help="Path to either a lifecycle-audit manifest JSON file or a lifecycle-audit plan JSON file")
    parser.add_argument("--input-kind", dest="input_kind", choices=["manifest", "audit-plan"], default="manifest", help="Interpret the positional input as a manifest or as a frozen audit plan")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--audit-plan-path", dest="audit_plan_path", help="Override output path for the lifecycle-audit plan")
    parser.add_argument("--remediation-plan-path", dest="remediation_plan_path", help="Override output path for the lifecycle-remediation plan")
    parser.add_argument("--decision-path", dest="decision_path", help="Override output path for the lifecycle pre-gate decision JSON")
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _manifest_slug(manifest_path: Path) -> str:
    stem = manifest_path.stem
    if stem.startswith("lifecycle-audit-") and stem.endswith("-manifest"):
        return stem.removeprefix("lifecycle-audit-").removesuffix("-manifest")
    if stem.startswith("lifecycle-audit-"):
        return stem.removeprefix("lifecycle-audit-")
    if stem.endswith("-manifest"):
        return stem.removesuffix("-manifest")
    return stem


def _audit_plan_slug(audit_plan_path: Path) -> str:
    stem = audit_plan_path.stem
    if stem.startswith("lifecycle-audit-") and stem.endswith("-plan"):
        return stem.removeprefix("lifecycle-audit-").removesuffix("-plan")
    if stem.endswith("-plan"):
        return stem.removesuffix("-plan")
    return stem


def _load_json(path: Path, error_label: str) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse {error_label} JSON: {exc}") from exc


def _summary_from_audit_items(items: list[dict]) -> GateSummary:
    counts = {"pass": 0, "warning": 0, "blocked": 0, "reconciliation": 0, "error": 0}
    for item in items:
        status = str(item.get("status") or "error")
        counts[status if status in counts else "error"] += 1
    return GateSummary(
        pass_count=counts["pass"],
        warning_count=counts["warning"],
        blocked_count=counts["blocked"],
        reconciliation_count=counts["reconciliation"],
        error_count=counts["error"],
    )


def _decision_from_summary(summary: GateSummary) -> tuple[str, bool, str]:
    if summary.error_count or summary.reconciliation_count:
        return (
            "hard-fail-input",
            False,
            "At least one audit item is in error or reconciliation state, so mutation must fail closed before remediation planning.",
        )
    if summary.warning_count or summary.blocked_count:
        return (
            "stop-for-remediation",
            False,
            "At least one audit item is warning or blocked, so mutation must stop and emit remediation planning artifacts.",
        )
    return (
        "allow-apply",
        True,
        "All audited items passed, so the requested mutation is structurally allowed to continue.",
    )


def _gate_item_reason(audit_status: str) -> tuple[str, bool, str]:
    if audit_status == "pass":
        return ("allow-apply", True, "Audit passed; no pre-gate remediation is required.")
    if audit_status in {"warning", "blocked"}:
        return (
            "stop-for-remediation",
            False,
            "Audit produced warning or blocked findings; the pre-gate policy requires remediation planning before mutation.",
        )
    return (
        "hard-fail-input",
        False,
        "Audit input is in reconciliation or error state; mutation must fail closed before any follow-up planning.",
    )


def plan_lifecycle_pre_gate(args: argparse.Namespace) -> LifecyclePreGateDecision:
    repo_root = _repo_root()
    input_path = _coerce_path(args.input_path, repo_root)
    if not input_path.is_file():
        raise SystemExit(f"Lifecycle pre-gate input file not found: {input_path}")

    if args.input_kind == "manifest":
        slug = _manifest_slug(input_path)
    else:
        slug = _audit_plan_slug(input_path)

    audit_plan_path = _coerce_path(args.audit_plan_path, repo_root) if args.audit_plan_path else (repo_root / "docs" / "issues" / f"lifecycle-audit-{slug}-plan.json")
    remediation_plan_path = _coerce_path(args.remediation_plan_path, repo_root) if args.remediation_plan_path else (repo_root / "docs" / "issues" / f"lifecycle-remediation-{slug}-plan.json")
    decision_path = _coerce_path(args.decision_path, repo_root) if args.decision_path else (repo_root / "docs" / "issues" / f"lifecycle-gate-{slug}-decision.json")

    if args.input_kind == "manifest":
        with contextlib.redirect_stdout(io.StringIO()):
            audit_result_data = asdict(
                plan_lifecycle_audit(
                    argparse.Namespace(
                        manifest_path=_repo_rel(input_path),
                        plan_path=_repo_rel(audit_plan_path),
                        repo=args.repo,
                    )
                )
            )
        manifest_rel = _repo_rel(input_path)
    else:
        if args.audit_plan_path:
            raise SystemExit("--audit-plan-path cannot be used when --input-kind audit-plan is selected")
        audit_result_data = _load_json(input_path, "lifecycle-audit plan")
        if audit_result_data.get("mode") != "lifecycle-audit-dry-run":
            raise SystemExit("Lifecycle pre-gate audit-plan input must be a lifecycle-audit-dry-run result")
        audit_plan_path = input_path
        manifest_rel = str(audit_result_data.get("manifest_path") or _repo_rel(input_path))

    audit_items = list(audit_result_data.get("items") or [])
    summary = _summary_from_audit_items(audit_items)
    decision, apply_allowed, decision_reason = _decision_from_summary(summary)

    remediation_result = None
    remediation_items_by_id: dict[str, dict] = {}
    remediation_plan_rel: str | None = None
    if decision == "stop-for-remediation":
        with contextlib.redirect_stdout(io.StringIO()):
            remediation_result = plan_lifecycle_remediation(
                argparse.Namespace(
                    audit_plan_path=_repo_rel(audit_plan_path),
                    plan_path=_repo_rel(remediation_plan_path),
                )
            )
        remediation_plan_rel = _repo_rel(remediation_plan_path)
        remediation_items_by_id = {
            str(item.requested_id): asdict(item)
            for item in remediation_result.items
        }

    items: list[GateDecisionItem] = []
    for item in audit_items:
        requested_id = str(item.get("requested_id") or "")
        gate_status, item_apply_allowed, item_reason = _gate_item_reason(str(item.get("status") or "error"))
        remediation_item = remediation_items_by_id.get(requested_id)
        remediation_status = remediation_item.get("remediation_status") if remediation_item else None
        remediation_steps = remediation_item.get("steps") if remediation_item else []
        items.append(
            GateDecisionItem(
                requested_id=requested_id,
                source_log_path=str(item.get("source_log_path") or ""),
                issue_number=item.get("issue_number"),
                issue_url=item.get("issue_url"),
                audit_status=str(item.get("status") or "error"),
                gate_status=gate_status,
                apply_allowed=item_apply_allowed,
                remediation_status=str(remediation_status) if remediation_status is not None else None,
                remediation_step_count=len(remediation_steps or []),
                remediation_plan_path=remediation_plan_rel if gate_status == "stop-for-remediation" else None,
                reason=item_reason,
            )
        )

    top_warnings = [
        f"{item.requested_id}: {item.gate_status}"
        for item in items
        if not item.apply_allowed
    ]

    result = LifecyclePreGateDecision(
        mode="lifecycle-pre-gate-dry-run",
        result="ok",
        selection_input=args.input_kind,
        operation="plan-lifecycle-pre-gate",
        manifest_path=manifest_rel,
        audit_plan_path=_repo_rel(audit_plan_path),
        remediation_plan_path=remediation_plan_rel,
        decision=decision,
        apply_allowed=apply_allowed,
        decision_reason=decision_reason,
        policy=DEFAULT_POLICY,
        summary=summary,
        warnings=top_warnings,
        items=items,
    )
    decision_path.parent.mkdir(parents=True, exist_ok=True)
    decision_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        plan_lifecycle_pre_gate(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())