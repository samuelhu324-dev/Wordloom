from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import (
    _derive_repo_slug,
    _fetch_existing_milestones,
    _load_text,
    _parse_fields,
    _repo_rel,
    _repo_root,
    _require_gh_auth,
    _require_gh_cli,
    _run_command,
)


ISSUE_URL_RE = re.compile(r"/issues/(\d+)$")


@dataclass
class BackfillPlanItem:
    issue_number: int | None
    issue_url: str | None
    source_log_path: str | None
    source_log_issue_url: str | None
    desired_milestone: str | None
    current_milestone: str | None
    write_back_issue_url: bool
    planned_action: str
    applied_action: str | None
    status: str
    warnings: list[str]
    reason: str | None = None


@dataclass
class BackfillPlanResult:
    mode: str
    result: str
    manifest_path: str | None
    selection_input: str
    operation: str
    total_items: int
    planned_items: int
    warnings: list[str]
    items: list[BackfillPlanItem]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan issue milestone/write-back reconciliation from an explicit manifest")
    parser.add_argument("manifest_path", help="Path to a backfill manifest JSON file")
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
        raise SystemExit(f"Failed to parse backfill manifest JSON: {exc}") from exc


def _normalize_issue_ref(number: int | None, url: str | None) -> tuple[int | None, str | None, list[str]]:
    warnings: list[str] = []
    parsed_number = number
    parsed_url = url.strip() if isinstance(url, str) and url.strip() else None
    if parsed_url:
        match = ISSUE_URL_RE.search(parsed_url)
        if not match:
            raise SystemExit(f"Invalid issue URL: {parsed_url}")
        url_number = int(match.group(1))
        if parsed_number is not None and parsed_number != url_number:
            warnings.append("issue number/url mismatch; moving item to reconciliation")
        else:
            parsed_number = url_number
    return parsed_number, parsed_url, warnings


def _fetch_issue_state(repo: str, issue_ref: str) -> tuple[int, str, str | None]:
    cmd = _run_command([
        "gh",
        "issue",
        "view",
        issue_ref,
        "--repo",
        repo,
        "--json",
        "number,url,milestone",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to view issue {issue_ref} in {repo}: {cmd.stderr.strip()}")
    try:
        data = json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse issue view JSON: {exc}") from exc

    milestone = data.get("milestone")
    milestone_title = milestone.get("title") if isinstance(milestone, dict) else None
    return int(data["number"]), str(data["url"]), milestone_title


def _load_source_log_issue_url(source_log_path: str | None, repo_root: Path) -> str | None:
    if not source_log_path:
        return None
    resolved = _coerce_path(source_log_path, repo_root)
    if not resolved.is_file():
        raise SystemExit(f"Source log not found for backfill item: {resolved}")
    fields = _parse_fields(_load_text(resolved))
    raw_issue = fields.get("issue", "").strip()
    return raw_issue or None


def _build_planned_action(actions: list[str]) -> str:
    if not actions:
        return "skip-no-change"
    return "+".join(actions)


def _build_item(item: dict, defaults: dict, repo_root: Path, repo: str, existing_milestones: set[str]) -> BackfillPlanItem:
    warnings: list[str] = []
    issue_number, issue_url, ref_warnings = _normalize_issue_ref(item.get("issue_number"), item.get("issue_url"))
    warnings.extend(ref_warnings)

    source_log_path = item.get("source_log_path")
    desired_milestone = item.get("desired_milestone")
    if desired_milestone == "":
        desired_milestone = None
    if desired_milestone is None:
        desired_milestone = defaults.get("desired_milestone")
    write_back_issue_url = bool(item.get("write_back_issue_url", defaults.get("write_back_issue_url", False)))
    reason = item.get("reason")

    source_log_issue_url = _load_source_log_issue_url(source_log_path, repo_root) if source_log_path else None

    if issue_number is None:
        warnings.append("explicit issue reference is required for milestone/write-back reconciliation")
        return BackfillPlanItem(
            issue_number=None,
            issue_url=issue_url,
            source_log_path=source_log_path,
            source_log_issue_url=source_log_issue_url,
            desired_milestone=desired_milestone,
            current_milestone=None,
            write_back_issue_url=write_back_issue_url,
            planned_action="error-missing-issue-reference",
            applied_action=None,
            status="error",
            warnings=warnings,
            reason=reason,
        )

    issue_number, resolved_issue_url, current_milestone = _fetch_issue_state(repo, issue_url or str(issue_number))
    if issue_url is None:
        issue_url = resolved_issue_url

    if any("mismatch" in warning for warning in warnings):
        return BackfillPlanItem(
            issue_number=issue_number,
            issue_url=issue_url,
            source_log_path=source_log_path,
            source_log_issue_url=source_log_issue_url,
            desired_milestone=desired_milestone,
            current_milestone=current_milestone,
            write_back_issue_url=write_back_issue_url,
            planned_action="reconcile-backfill-input",
            applied_action=None,
            status="reconciliation",
            warnings=warnings,
            reason=reason,
        )

    if desired_milestone and desired_milestone not in existing_milestones:
        warnings.append("desired milestone does not exist in the target repository")
        return BackfillPlanItem(
            issue_number=issue_number,
            issue_url=issue_url,
            source_log_path=source_log_path,
            source_log_issue_url=source_log_issue_url,
            desired_milestone=desired_milestone,
            current_milestone=current_milestone,
            write_back_issue_url=write_back_issue_url,
            planned_action="error-missing-milestone",
            applied_action=None,
            status="error",
            warnings=warnings,
            reason=reason,
        )

    actions: list[str] = []
    reconciliation = False

    if desired_milestone:
        if current_milestone is None:
            actions.append("apply-milestone")
        elif current_milestone == desired_milestone:
            warnings.append("desired milestone already matches current issue milestone")
        else:
            warnings.append("current issue milestone conflicts with desired milestone")
            reconciliation = True
    else:
        warnings.append("desired milestone left blank; milestone remains unmanaged")

    if write_back_issue_url:
        if not source_log_path:
            warnings.append("source_log_path is required when write_back_issue_url=true")
            return BackfillPlanItem(
                issue_number=issue_number,
                issue_url=issue_url,
                source_log_path=source_log_path,
                source_log_issue_url=source_log_issue_url,
                desired_milestone=desired_milestone,
                current_milestone=current_milestone,
                write_back_issue_url=write_back_issue_url,
                planned_action="error-missing-source-log",
                applied_action=None,
                status="error",
                warnings=warnings,
                reason=reason,
            )
        if source_log_issue_url is None:
            actions.append("write-back-issue-url")
        elif source_log_issue_url == issue_url:
            warnings.append("source log issue URL already matches explicit issue URL")
        else:
            warnings.append("source log issue URL conflicts with explicit issue URL")
            reconciliation = True
    else:
        warnings.append("write-back not requested for this item")

    if reconciliation:
        return BackfillPlanItem(
            issue_number=issue_number,
            issue_url=issue_url,
            source_log_path=source_log_path,
            source_log_issue_url=source_log_issue_url,
            desired_milestone=desired_milestone,
            current_milestone=current_milestone,
            write_back_issue_url=write_back_issue_url,
            planned_action="reconcile-milestone-or-writeback",
            applied_action=None,
            status="reconciliation",
            warnings=warnings,
            reason=reason,
        )

    status = "planned" if actions else "skipped"
    return BackfillPlanItem(
        issue_number=issue_number,
        issue_url=issue_url,
        source_log_path=source_log_path,
        source_log_issue_url=source_log_issue_url,
        desired_milestone=desired_milestone,
        current_milestone=current_milestone,
        write_back_issue_url=write_back_issue_url,
        planned_action=_build_planned_action(actions),
        applied_action=None,
        status=status,
        warnings=warnings,
        reason=reason,
    )


def plan_issue_backfill(args: argparse.Namespace) -> BackfillPlanResult:
    repo_root = _repo_root()
    manifest_path = _coerce_path(args.manifest_path, repo_root)
    if not manifest_path.is_file():
        raise SystemExit(f"Backfill manifest file not found: {manifest_path}")

    manifest = _load_manifest(manifest_path)
    defaults = manifest.get("defaults") or {}
    raw_items = manifest.get("items") or []
    if not raw_items:
        raise SystemExit(f"No backfill items defined in manifest: {manifest_path}")

    _require_gh_cli()
    _require_gh_auth()
    repo = _derive_repo_slug(defaults.get("repo"))
    existing_milestones = _fetch_existing_milestones(repo)

    items = [_build_item(item, defaults, repo_root, repo, existing_milestones) for item in raw_items]
    top_warnings = [
        f"item {index + 1}: {item.status}"
        for index, item in enumerate(items)
        if item.status != "planned"
    ]

    manifest_rel = _repo_rel(manifest_path)
    manifest_stem = manifest_path.stem
    if manifest_stem.startswith("issue-backfill-"):
        manifest_slug = manifest_stem.removeprefix("issue-backfill-")
    else:
        manifest_slug = manifest_stem.removeprefix("issue-")
    default_plan_path = repo_root / "docs" / "issues" / f"issue-backfill-{manifest_slug}-plan.json"
    plan_path = _coerce_path(args.plan_path, repo_root) if args.plan_path else default_plan_path
    plan_path.parent.mkdir(parents=True, exist_ok=True)

    result = BackfillPlanResult(
        mode="backfill-dry-run",
        result="ok",
        manifest_path=manifest_rel,
        selection_input="manifest",
        operation="plan-issue-backfill",
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
        plan_issue_backfill(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())