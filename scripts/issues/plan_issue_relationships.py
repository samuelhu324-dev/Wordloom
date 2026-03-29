from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _load_text, _parse_fields, _repo_rel, _repo_root


ISSUE_URL_RE = re.compile(r"/issues/(\d+)$")
ALLOWED_RELATIONSHIP_TYPES = {"child-of", "parent-of"}


@dataclass
class RelationshipPlanItem:
    relationship_type: str
    parent_issue_number: int | None
    parent_issue_url: str | None
    child_issue_number: int | None
    child_issue_url: str | None
    parent_log_path: str | None
    child_log_path: str | None
    planned_action: str
    applied_action: str | None
    status: str
    warnings: list[str]
    reason: str | None = None


@dataclass
class RelationshipPlanResult:
    mode: str
    result: str
    manifest_path: str | None
    selection_input: str
    operation: str
    total_items: int
    planned_items: int
    warnings: list[str]
    items: list[RelationshipPlanItem]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan issue relationships from an explicit manifest")
    parser.add_argument("manifest_path", help="Path to a relationship manifest JSON file")
    parser.add_argument("--plan-path", dest="plan_path", help="Override output plan JSON path")
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _load_manifest(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse relationship manifest JSON: {exc}") from exc


def _normalize_issue_ref(number: int | None, url: str | None, role: str) -> tuple[int | None, str | None, list[str]]:
    warnings: list[str] = []
    parsed_number = number
    parsed_url = url.strip() if isinstance(url, str) and url.strip() else None
    if parsed_url:
        match = ISSUE_URL_RE.search(parsed_url)
        if not match:
            raise SystemExit(f"Invalid {role} issue URL: {parsed_url}")
        url_number = int(match.group(1))
        if parsed_number is not None and parsed_number != url_number:
            warnings.append(f"{role} issue number/url mismatch; using explicit conflict status")
        else:
            parsed_number = url_number
    return parsed_number, parsed_url, warnings


def _load_log_issue_ref(log_path: str, repo_root: Path) -> tuple[int | None, str | None]:
    resolved = _coerce_path(log_path, repo_root)
    if not resolved.is_file():
        raise SystemExit(f"Traceability log not found: {resolved}")
    fields = _parse_fields(_load_text(resolved))
    issue_url = fields.get("issue", "").strip() or None
    if not issue_url:
        return None, None
    match = ISSUE_URL_RE.search(issue_url)
    return (int(match.group(1)) if match else None, issue_url)


def _normalize_relationship_type(raw_type: str | None, defaults: dict) -> str:
    relationship_type = (raw_type or defaults.get("relationship_type") or "child-of").strip()
    if relationship_type not in ALLOWED_RELATIONSHIP_TYPES:
        raise SystemExit(f"Unsupported relationship_type: {relationship_type}")
    return relationship_type


def _build_item(item: dict, defaults: dict, repo_root: Path) -> RelationshipPlanItem:
    relationship_type = _normalize_relationship_type(item.get("relationship_type"), defaults)
    warnings: list[str] = []

    parent_number, parent_url, parent_warnings = _normalize_issue_ref(
        item.get("parent_issue_number"),
        item.get("parent_issue_url"),
        "parent",
    )
    child_number, child_url, child_warnings = _normalize_issue_ref(
        item.get("child_issue_number"),
        item.get("child_issue_url"),
        "child",
    )
    warnings.extend(parent_warnings)
    warnings.extend(child_warnings)

    parent_log_path = item.get("parent_log_path")
    child_log_path = item.get("child_log_path")
    reason = item.get("reason")

    if item.get("skip"):
        skip_reason = item.get("skip_reason") or "relationship item marked skip by manifest"
        warnings.append(skip_reason)
        return RelationshipPlanItem(
            relationship_type=relationship_type,
            parent_issue_number=parent_number,
            parent_issue_url=parent_url,
            child_issue_number=child_number,
            child_issue_url=child_url,
            parent_log_path=parent_log_path,
            child_log_path=child_log_path,
            planned_action="skip-relationship",
            applied_action=None,
            status="skipped",
            warnings=warnings,
            reason=reason,
        )

    if parent_number is None or child_number is None:
        warnings.append("explicit parent and child issue references are both required")
        return RelationshipPlanItem(
            relationship_type=relationship_type,
            parent_issue_number=parent_number,
            parent_issue_url=parent_url,
            child_issue_number=child_number,
            child_issue_url=child_url,
            parent_log_path=parent_log_path,
            child_log_path=child_log_path,
            planned_action="error-missing-reference",
            applied_action=None,
            status="error",
            warnings=warnings,
            reason=reason,
        )

    if parent_number == child_number:
        warnings.append("parent and child issue references cannot be the same issue")
        return RelationshipPlanItem(
            relationship_type=relationship_type,
            parent_issue_number=parent_number,
            parent_issue_url=parent_url,
            child_issue_number=child_number,
            child_issue_url=child_url,
            parent_log_path=parent_log_path,
            child_log_path=child_log_path,
            planned_action="error-self-reference",
            applied_action=None,
            status="error",
            warnings=warnings,
            reason=reason,
        )

    mismatch_detected = False
    if parent_log_path:
        trace_number, trace_url = _load_log_issue_ref(parent_log_path, repo_root)
        if trace_number is None or trace_number != parent_number:
            warnings.append("parent_log_path issue reference conflicts with explicit parent issue reference")
            mismatch_detected = True
        elif parent_url is None and trace_url:
            parent_url = trace_url
    if child_log_path:
        trace_number, trace_url = _load_log_issue_ref(child_log_path, repo_root)
        if trace_number is None or trace_number != child_number:
            warnings.append("child_log_path issue reference conflicts with explicit child issue reference")
            mismatch_detected = True
        elif child_url is None and trace_url:
            child_url = trace_url

    if mismatch_detected or any("mismatch" in warning for warning in warnings):
        return RelationshipPlanItem(
            relationship_type=relationship_type,
            parent_issue_number=parent_number,
            parent_issue_url=parent_url,
            child_issue_number=child_number,
            child_issue_url=child_url,
            parent_log_path=parent_log_path,
            child_log_path=child_log_path,
            planned_action="reconcile-relationship-input",
            applied_action=None,
            status="reconciliation",
            warnings=warnings,
            reason=reason,
        )

    planned_action = "link-child-to-parent" if relationship_type == "child-of" else "link-parent-to-child"
    return RelationshipPlanItem(
        relationship_type=relationship_type,
        parent_issue_number=parent_number,
        parent_issue_url=parent_url,
        child_issue_number=child_number,
        child_issue_url=child_url,
        parent_log_path=parent_log_path,
        child_log_path=child_log_path,
        planned_action=planned_action,
        applied_action=None,
        status="planned",
        warnings=warnings,
        reason=reason,
    )


def plan_issue_relationships(args: argparse.Namespace) -> RelationshipPlanResult:
    repo_root = _repo_root()
    manifest_path = _coerce_path(args.manifest_path, repo_root)
    if not manifest_path.is_file():
        raise SystemExit(f"Relationship manifest file not found: {manifest_path}")

    manifest = _load_manifest(manifest_path)
    defaults = manifest.get("defaults") or {}
    raw_items = manifest.get("items") or []
    if not raw_items:
        raise SystemExit(f"No relationship items defined in manifest: {manifest_path}")

    items = [_build_item(item, defaults, repo_root) for item in raw_items]
    top_warnings = [
        f"item {index + 1}: {item.status}"
        for index, item in enumerate(items)
        if item.status != "planned"
    ]

    manifest_rel = _repo_rel(manifest_path)
    manifest_stem = manifest_path.stem
    if manifest_stem.startswith("issue-relationship-"):
        manifest_slug = manifest_stem.removeprefix("issue-relationship-")
    else:
        manifest_slug = manifest_stem.removeprefix("issue-")
    default_plan_path = repo_root / "docs" / "issues" / f"issue-relationship-{manifest_slug}-plan.json"
    plan_path = _coerce_path(args.plan_path, repo_root) if args.plan_path else default_plan_path
    plan_path.parent.mkdir(parents=True, exist_ok=True)

    result = RelationshipPlanResult(
        mode="relationship-dry-run",
        result="ok",
        manifest_path=manifest_rel,
        selection_input="manifest",
        operation="plan-issue-relationships",
        total_items=len(items),
        planned_items=sum(1 for item in items if item.status == "planned"),
        warnings=top_warnings,
        items=items,
    )
    plan_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        plan_issue_relationships(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())