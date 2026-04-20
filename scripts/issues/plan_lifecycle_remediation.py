from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _load_text, _parse_fields, _repo_rel, _repo_root


@dataclass
class RemediationStep:
    action_kind: str
    status: str
    details: str
    downstream_manifest_path: str | None


@dataclass
class LifecycleRemediationPlanItem:
    requested_id: str
    source_log_path: str
    issue_number: int | None
    issue_url: str | None
    audit_status: str
    remediation_status: str
    planned_action: str
    applied_action: str | None
    steps: list[RemediationStep]
    warnings: list[str]
    reason: str | None = None


@dataclass
class LifecycleRemediationPlanResult:
    mode: str
    result: str
    audit_plan_path: str
    selection_input: str
    operation: str
    total_items: int
    planned_items: int
    warnings: list[str]
    items: list[LifecycleRemediationPlanItem]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan dry-run remediation steps from a lifecycle-audit plan")
    parser.add_argument("audit_plan_path", help="Path to a lifecycle-audit dry-run plan JSON file")
    parser.add_argument("--plan-path", dest="plan_path", help="Override output remediation plan JSON path")
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _load_json(path: Path, error_label: str) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse {error_label} JSON: {exc}") from exc


def _manifest_slug_from_audit_plan(audit_plan_path: Path) -> str:
    stem = audit_plan_path.stem
    if stem.startswith("lifecycle-audit-") and stem.endswith("-plan"):
        return stem.removeprefix("lifecycle-audit-").removesuffix("-plan")
    if stem.endswith("-plan"):
        return stem.removesuffix("-plan")
    return stem


def _slug_from_plan_path(plan_path: Path) -> str:
    stem = plan_path.stem
    if stem.startswith("lifecycle-remediation-") and stem.endswith("-plan"):
        return stem.removeprefix("lifecycle-remediation-").removesuffix("-plan")
    if stem.endswith("-plan"):
        return stem.removesuffix("-plan")
    return stem


def _load_parent_log_path(source_log_path: Path) -> str | None:
    fields = _parse_fields(_load_text(source_log_path))
    value = fields.get("parent_log", "").strip()
    return value or None


def _find_check(item: dict, name: str) -> dict | None:
    for check in item.get("checks") or []:
        if isinstance(check, dict) and check.get("name") == name:
            return check
    return None


def _write_optional_manifest(path: Path, payload: dict | None) -> str | None:
    if payload is None:
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return _repo_rel(path)


def _build_plan_item(item: dict, relationship_manifest_rel: str | None, conclusion_manifest_rel: str | None, backfill_manifest_rel: str | None) -> LifecycleRemediationPlanItem:
    requested_id = str(item.get("requested_id") or "")
    source_log_path = str(item.get("source_log_path") or "")
    issue_number = item.get("issue_number")
    issue_url = item.get("issue_url")
    audit_status = str(item.get("status") or "error")
    reason = item.get("reason")
    warnings = list(item.get("warnings") or [])
    steps: list[RemediationStep] = []

    if audit_status == "pass":
        return LifecycleRemediationPlanItem(
            requested_id=requested_id,
            source_log_path=source_log_path,
            issue_number=issue_number,
            issue_url=issue_url,
            audit_status=audit_status,
            remediation_status="skipped",
            planned_action="skip-remediation-no-findings",
            applied_action=None,
            steps=[],
            warnings=warnings,
            reason=reason,
        )

    if audit_status in {"error", "reconciliation"}:
        steps.append(
            RemediationStep(
                action_kind="manual-reconcile-audit-input",
                status="manual",
                details="Audit input conflicts with source-log or GitHub references; reconcile the audit manifest before any automated remediation planning.",
                downstream_manifest_path=None,
            )
        )
        return LifecycleRemediationPlanItem(
            requested_id=requested_id,
            source_log_path=source_log_path,
            issue_number=issue_number,
            issue_url=issue_url,
            audit_status=audit_status,
            remediation_status="reconciliation",
            planned_action="reconcile-remediation-input",
            applied_action=None,
            steps=steps,
            warnings=warnings,
            reason=reason,
        )

    sidebar_check = _find_check(item, "sidebar-parent-relationship")
    if sidebar_check and sidebar_check.get("status") == "fail":
        steps.append(
            RemediationStep(
                action_kind="attach-parent-relationship",
                status="planned",
                details="Prepare a child-of relationship attach from the expected parent issue to the audited child issue.",
                downstream_manifest_path=relationship_manifest_rel,
            )
        )

    source_log_issue_check = _find_check(item, "source-log-issue-writeback")
    if source_log_issue_check and source_log_issue_check.get("status") == "fail":
        steps.append(
            RemediationStep(
                action_kind="write-back-source-log-issue-url",
                status="planned",
                details="Prepare a source-log write-back reconciliation so links.issue matches the live GitHub issue URL.",
                downstream_manifest_path=backfill_manifest_rel,
            )
        )

    conclusion_needed = False
    if str(item.get("issue_state") or "") != "CLOSED" and int(item.get("merged_pr_count") or 0) > 0:
        conclusion_needed = True
    for check_name in ["final-dod-pr-refs", "links-coverage", "closed-body-shape"]:
        check = _find_check(item, check_name)
        if check and check.get("status") == "fail":
            conclusion_needed = True
            break
    if conclusion_needed:
        steps.append(
            RemediationStep(
                action_kind="plan-issue-conclusion-refresh",
                status="planned",
                details="Prepare an issue-conclusion plan so the final body and close state can be regenerated from exact-ID merged PR evidence.",
                downstream_manifest_path=conclusion_manifest_rel,
            )
        )

    expected_labels_check = _find_check(item, "expected-labels")
    if expected_labels_check and expected_labels_check.get("status") == "fail":
        steps.append(
            RemediationStep(
                action_kind="manual-label-remediation",
                status="manual",
                details="Live GitHub labels diverge from the deterministic label set; no automatic label apply path exists yet, so review and add/remove labels manually.",
                downstream_manifest_path=None,
            )
        )

    body_parent_check = _find_check(item, "body-parent-metadata")
    if body_parent_check and body_parent_check.get("status") == "fail":
        steps.append(
            RemediationStep(
                action_kind="manual-body-parent-metadata-remediation",
                status="manual",
                details="Issue body metadata is missing the expected Parent issue line; refresh the issue body through the appropriate body-generation path after relationship state is correct.",
                downstream_manifest_path=None,
            )
        )

    remediation_status = "planned" if steps else "skipped"
    planned_action = "plan-remediation" if steps else "skip-remediation-no-actionable-findings"

    return LifecycleRemediationPlanItem(
        requested_id=requested_id,
        source_log_path=source_log_path,
        issue_number=issue_number,
        issue_url=issue_url,
        audit_status=audit_status,
        remediation_status=remediation_status,
        planned_action=planned_action,
        applied_action=None,
        steps=steps,
        warnings=warnings,
        reason=reason,
    )


def plan_lifecycle_remediation(args: argparse.Namespace) -> LifecycleRemediationPlanResult:
    repo_root = _repo_root()
    audit_plan_path = _coerce_path(args.audit_plan_path, repo_root)
    if not audit_plan_path.is_file():
        raise SystemExit(f"Lifecycle-audit plan file not found: {audit_plan_path}")

    audit_plan = _load_json(audit_plan_path, "lifecycle-audit plan")
    if audit_plan.get("mode") != "lifecycle-audit-dry-run":
        raise SystemExit("Lifecycle remediation planner requires a lifecycle-audit-dry-run input plan")

    items = audit_plan.get("items") or []
    if not items:
        raise SystemExit(f"No lifecycle-audit items found in plan: {audit_plan_path}")

    manifest_slug = _manifest_slug_from_audit_plan(audit_plan_path)
    default_plan_path = repo_root / "docs" / "issues" / f"lifecycle-remediation-{manifest_slug}-plan.json"
    plan_path = _coerce_path(args.plan_path, repo_root) if args.plan_path else default_plan_path
    plan_path.parent.mkdir(parents=True, exist_ok=True)

    relationship_items: list[dict] = []
    conclusion_items: list[dict] = []
    backfill_items: list[dict] = []

    for item in items:
        source_log_rel = str(item.get("source_log_path") or "")
        source_log_path = _coerce_path(source_log_rel, repo_root)
        parent_log_path = _load_parent_log_path(source_log_path) if source_log_rel else None

        sidebar_check = _find_check(item, "sidebar-parent-relationship")
        expected_parent_issue_number = item.get("expected_parent_issue_number")
        if sidebar_check and sidebar_check.get("status") == "fail" and expected_parent_issue_number is not None and item.get("issue_number") is not None:
            relationship_items.append(
                {
                    "parent_issue_number": int(expected_parent_issue_number),
                    "child_issue_number": int(item["issue_number"]),
                    "parent_log_path": parent_log_path,
                    "child_log_path": source_log_rel,
                    "reason": item.get("reason") or f"Lifecycle remediation for {item.get('requested_id')}",
                }
            )

        source_log_issue_check = _find_check(item, "source-log-issue-writeback")
        if source_log_issue_check and source_log_issue_check.get("status") == "fail" and item.get("issue_number") is not None:
            backfill_items.append(
                {
                    "issue_number": int(item["issue_number"]),
                    "issue_url": item.get("issue_url"),
                    "source_log_path": source_log_rel,
                    "write_back_issue_url": True,
                    "reason": item.get("reason") or f"Lifecycle remediation for {item.get('requested_id')}",
                }
            )

        conclusion_needed = False
        if str(item.get("issue_state") or "") != "CLOSED" and int(item.get("merged_pr_count") or 0) > 0:
            conclusion_needed = True
        for check_name in ["final-dod-pr-refs", "links-coverage", "closed-body-shape"]:
            check = _find_check(item, check_name)
            if check and check.get("status") == "fail":
                conclusion_needed = True
                break
        if conclusion_needed and item.get("issue_number") is not None:
            conclusion_items.append(
                {
                    "requested_id": item.get("requested_id"),
                    "source_log_path": source_log_rel,
                    "issue_number": int(item["issue_number"]),
                    "merged_pr_overrides": [f"#{pr.get('number')}" for pr in item.get("merged_prs") or []],
                    "reason": item.get("reason") or f"Lifecycle remediation for {item.get('requested_id')}",
                }
            )

    downstream_slug = _slug_from_plan_path(plan_path)

    relationship_manifest_rel = _write_optional_manifest(
        plan_path.with_name(f"lifecycle-remediation-{downstream_slug}-relationship-manifest.json"),
        {
            "version": 1,
            "mode": "relationship-dry-run",
            "defaults": {"relationship_type": "child-of"},
            "items": relationship_items,
        } if relationship_items else None,
    )
    conclusion_manifest_rel = _write_optional_manifest(
        plan_path.with_name(f"lifecycle-remediation-{downstream_slug}-issue-conclusion-manifest.json"),
        {
            "version": "1",
            "mode": "issue-conclusion-dry-run",
            "defaults": {"repo": audit_plan.get("defaults", {}).get("repo", "samuelhu324-dev/wordloom-v3")},
            "items": conclusion_items,
        } if conclusion_items else None,
    )
    backfill_manifest_rel = _write_optional_manifest(
        plan_path.with_name(f"lifecycle-remediation-{downstream_slug}-issue-backfill-manifest.json"),
        {
            "defaults": {
                "write_back_issue_url": True,
                "desired_milestone": None,
            },
            "items": backfill_items,
        } if backfill_items else None,
    )

    plan_items = [
        _build_plan_item(item, relationship_manifest_rel, conclusion_manifest_rel, backfill_manifest_rel)
        for item in items
    ]

    top_warnings = [
        f"{item.requested_id}: {item.remediation_status}"
        for item in plan_items
        if item.remediation_status != "skipped"
    ]

    result = LifecycleRemediationPlanResult(
        mode="lifecycle-remediation-dry-run",
        result="ok",
        audit_plan_path=_repo_rel(audit_plan_path),
        selection_input="audit-plan",
        operation="plan-lifecycle-remediation",
        total_items=len(plan_items),
        planned_items=sum(1 for item in plan_items if item.remediation_status == "planned"),
        warnings=top_warnings,
        items=plan_items,
    )
    plan_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        plan_lifecycle_remediation(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())