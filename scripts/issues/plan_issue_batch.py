from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from types import SimpleNamespace

from gen_issue_draft import _load_text, _parse_fields, _repo_rel, _repo_root, generate_issue_draft


@dataclass
class BatchPlanItem:
    source_log: str
    draft_path: str
    result_path: str
    issue_number: int | None
    issue_url: str | None
    planned_action: str
    applied_action: str | None
    status: str
    title: str
    warnings: list[str]


@dataclass
class BatchPlanResult:
    mode: str
    result: str
    manifest_path: str | None
    selection_input: str
    operation: str
    total_items: int
    planned_items: int
    warnings: list[str]
    items: list[BatchPlanItem]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan batch issue draft creation from a manifest")
    parser.add_argument("manifest_path", help="Path to a batch issue manifest JSON file")
    parser.add_argument("--plan-path", dest="plan_path", help="Override output plan JSON path")
    parser.add_argument("--repo", dest="repo", help="Repository slug override for live label preflight during batch planning")
    parser.add_argument(
        "--no-live-label-check",
        dest="no_live_label_check",
        action="store_true",
        help="Disable the default advisory live label preflight used by batch issue planning",
    )
    parser.add_argument(
        "--fail-on-missing-live-labels",
        dest="fail_on_missing_live_labels",
        action="store_true",
        help="Escalate batch planner live label preflight from advisory warnings to fail-closed behavior",
    )
    return parser.parse_args()


def _split_csv(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def _load_manifest(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse manifest JSON: {exc}") from exc


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _resolve_manifest_items(manifest: dict, manifest_path: Path, repo_root: Path) -> list[dict]:
    selection_filters = manifest.get("selection_filters") or {}
    include_globs = selection_filters.get("include_globs") or []
    exclude_globs = set(selection_filters.get("exclude_globs") or [])
    defaults = manifest.get("defaults") or {}

    merged: dict[str, dict] = {}
    for pattern in include_globs:
        for candidate in sorted(repo_root.glob(pattern)):
            if not candidate.is_file():
                continue
            rel = _repo_rel(candidate)
            if any(candidate.match(excluded) or rel == excluded for excluded in exclude_globs):
                continue
            merged[rel] = {"log_path": rel}

    for item in manifest.get("items") or []:
        log_path = item.get("log_path")
        if not log_path:
            raise SystemExit("Manifest item missing required log_path")
        resolved = _coerce_path(log_path, repo_root)
        rel = _repo_rel(resolved)
        merged.setdefault(rel, {"log_path": rel})
        merged[rel].update(item)
        merged[rel]["log_path"] = rel

    if not merged:
        raise SystemExit(f"No log files selected from manifest: {manifest_path}")

    items: list[dict] = []
    for rel in sorted(merged):
        item = dict(defaults)
        item.update(merged[rel])
        item["log_path"] = rel
        items.append(item)
    return items


def _parse_issue_link(fields: dict[str, str]) -> tuple[int | None, str | None]:
    raw_issue = fields.get("issue", "").strip()
    if not raw_issue:
        return None, None
    match = re.search(r"/(\d+)$", raw_issue)
    issue_number = int(match.group(1)) if match else None
    return issue_number, raw_issue


def _build_draft_args(item: dict, args: argparse.Namespace) -> SimpleNamespace:
    check_live_labels = item.get("check_live_labels")
    if check_live_labels is None:
        check_live_labels = not args.no_live_label_check

    fail_on_missing_live_labels = item.get("fail_on_missing_live_labels")
    if fail_on_missing_live_labels is None:
        fail_on_missing_live_labels = bool(args.fail_on_missing_live_labels)

    return SimpleNamespace(
        log_path=item["log_path"],
        output_path=item.get("output_path"),
        result_path=item.get("result_path"),
        parent_issue=item.get("parent_issue"),
        milestone_override=item.get("milestone_override"),
        module_label_overrides=_split_csv(item.get("module_label_overrides")) if isinstance(item.get("module_label_overrides"), str) else item.get("module_label_overrides"),
        strict_label_check=bool(item.get("strict_label_check", False)),
        repo=item.get("repo") or args.repo,
        check_live_labels=bool(check_live_labels),
        fail_on_missing_live_labels=bool(fail_on_missing_live_labels),
        context_mode=item.get("context_mode") or "llm-generate",
        create_issue=False,
    )


def plan_issue_batch(args: argparse.Namespace) -> BatchPlanResult:
    repo_root = _repo_root()
    manifest_path = _coerce_path(args.manifest_path, repo_root)
    if not manifest_path.is_file():
        raise SystemExit(f"Manifest file not found: {manifest_path}")

    manifest = _load_manifest(manifest_path)
    items = _resolve_manifest_items(manifest, manifest_path, repo_root)

    plan_items: list[BatchPlanItem] = []
    top_warnings: list[str] = []
    for item in items:
        log_path = _coerce_path(item["log_path"], repo_root)
        fields = _parse_fields(_load_text(log_path))
        issue_number, issue_url = _parse_issue_link(fields)
        draft_result = generate_issue_draft(_build_draft_args(item, args), emit_result=False)

        warnings = list(draft_result.warnings)
        if issue_url:
            warnings.append("source log already has links.issue; planned action is skip-existing-issue")

        planned_action = "skip-existing-issue" if issue_url else "create-issue"
        status = "skipped" if issue_url else "planned"
        if issue_url:
            top_warnings.append(f"{draft_result.log_path}: existing issue link present; create action skipped")

        result_path = item.get("result_path")
        if result_path:
            resolved_result_path = _coerce_path(result_path, repo_root)
        else:
            resolved_result_path = (repo_root / draft_result.draft_path).with_suffix(".json")

        plan_items.append(
            BatchPlanItem(
                source_log=draft_result.log_path,
                draft_path=draft_result.draft_path,
                result_path=_repo_rel(resolved_result_path),
                issue_number=issue_number,
                issue_url=issue_url,
                planned_action=planned_action,
                applied_action=None,
                status=status,
                title=draft_result.title,
                warnings=warnings,
            )
        )

    manifest_rel = _repo_rel(manifest_path)
    manifest_stem = manifest_path.stem
    if manifest_stem.startswith("issue-batch-"):
        manifest_slug = manifest_stem.removeprefix("issue-batch-")
    else:
        manifest_slug = manifest_stem.removeprefix("issue-")
    default_plan_path = repo_root / "docs" / "issues" / f"issue-batch-{manifest_slug}-plan.json"
    plan_path = _coerce_path(args.plan_path, repo_root) if args.plan_path else default_plan_path
    plan_path.parent.mkdir(parents=True, exist_ok=True)

    plan = BatchPlanResult(
        mode="batch-dry-run",
        result="ok",
        manifest_path=manifest_rel,
        selection_input="manifest",
        operation="plan-batch-issues",
        total_items=len(plan_items),
        planned_items=sum(1 for item in plan_items if item.status == "planned"),
        warnings=top_warnings,
        items=plan_items,
    )
    plan_path.write_text(json.dumps(asdict(plan), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(plan), indent=2, ensure_ascii=True))
    return plan


def main() -> int:
    args = _parse_args()
    try:
        plan_issue_batch(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())