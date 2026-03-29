from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _load_text, _parse_fields, _parse_sections, _repo_rel, _repo_root, _run_command


ID_PREFIX_RE = re.compile(r"^(?P<id>[A-Z0-9-]+)(?:/|:)")
CHECKED_ITEM_RE = re.compile(r"^- \[x\] `?([^`]+)`?:\s*(.+)$", re.IGNORECASE)


@dataclass
class CommitSelection:
    sha: str
    subject: str
    matched_id: str | None
    status: str
    reason: str


@dataclass
class PrPrepPlanItem:
    requested_id: str
    source_log_path: str
    current_branch: str
    head_ref: str
    base_branch: str
    merge_base: str
    candidate_pr_branch: str
    pr_title: str
    pr_base: str | None
    pr_labels: list[str]
    pr_projects: list[str]
    pr_milestone: str | None
    pr_development_issue: str | None
    preview_body_path: str
    selected_commit_count: int
    selected_commits: list[CommitSelection]
    branch_commits: list[CommitSelection]
    planned_action: str
    status: str
    warnings: list[str]


@dataclass
class PrPrepPlanResult:
    mode: str
    result: str
    manifest_path: str | None
    selection_input: str
    operation: str
    total_items: int
    planned_items: int
    warnings: list[str]
    items: list[PrPrepPlanItem]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan dry-run PR prep from a mixed working branch")
    parser.add_argument("manifest_path", help="Path to a PR-prep manifest JSON file")
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
        raise SystemExit(f"Failed to parse PR-prep manifest JSON: {exc}") from exc


def _split_csv(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def _normalize_branch_name(raw: str) -> str:
    lowered = raw.lower()
    lowered = re.sub(r"[^a-z0-9._/-]+", "-", lowered)
    lowered = re.sub(r"/{2,}", "/", lowered).strip("-/. ")
    return lowered or "pr-prep"


def _git_stdout(*args: str) -> str:
    cmd = _run_command(["git", "-C", str(_repo_root()), *args])
    if cmd.returncode != 0:
        raise SystemExit(cmd.stderr.strip() or f"git command failed: {' '.join(args)}")
    return cmd.stdout.strip()


def _parse_pr_summary_inputs(section_lines: list[str]) -> tuple[list[str], list[str]]:
    summary_bullets: list[str] = []
    link_lines: list[str] = []
    current: str | None = None

    for raw in section_lines:
        stripped = raw.strip()
        if stripped == "**PR summary bullets**:":
            current = "summary"
            continue
        if stripped == "**PR links / evidence footer**:":
            current = "links"
            continue
        if stripped.startswith("**") and stripped.endswith(":"):
            current = None
            continue
        if not stripped.startswith("- "):
            continue
        value = stripped[2:].strip()
        if current == "summary":
            summary_bullets.append(value)
        elif current == "links":
            link_lines.append(value)

    return summary_bullets, link_lines


def _extract_checked_items(section_lines: list[str]) -> list[str]:
    items: list[str] = []
    for raw in section_lines:
        match = CHECKED_ITEM_RE.match(raw.strip())
        if match:
            items.append(f"{match.group(1)}: {match.group(2).strip()}")
    return items


def _build_default_link_lines(fields: dict[str, str], source_log_path: str) -> list[str]:
    lines = [f"Log: `{source_log_path}`"]
    if fields.get("issue", "").strip():
        lines.append(f"Issue: `{fields['issue'].strip()}`")
    if fields.get("runbook", "").strip():
        lines.append(f"Runbook: `{fields['runbook'].strip()}`")
    return lines


def _render_body_preview(
    *,
    requested_id: str,
    pr_title: str,
    base_branch: str,
    candidate_pr_branch: str,
    source_log_path: str,
    summary_bullets: list[str],
    checklist_items: list[str],
    link_lines: list[str],
    selected_commits: list[CommitSelection],
    pr_development_issue: str | None,
) -> str:
    summary_lines = [f"- {item}" for item in summary_bullets] or ["- <placeholder>"]
    checklist_lines = [f"- [x] {item}" for item in checklist_items] or ["- [ ] <placeholder>"]
    selected_commit_lines = [f"- `{item.sha[:8]}` {item.subject}" for item in selected_commits] or ["- <none>"]
    lines = [
        f"# {pr_title}",
        "",
        "## Metadata",
        "",
        f"- Requested ID: `{requested_id}`",
        f"- Base branch: `{base_branch}`",
        f"- Candidate PR-prep branch: `{candidate_pr_branch}`",
        f"- Source log: `{source_log_path}`",
        f"- Development issue: `{pr_development_issue or ''}`",
        "",
        "## Summary",
        "",
        *summary_lines,
        "",
        "## Execution Checklist",
        "",
        *checklist_lines,
        "",
        "## Links",
        "",
        *[f"- {item}" for item in link_lines],
        "",
        "## Evidence Footer",
        "",
        *selected_commit_lines,
        "",
    ]
    return "\n".join(lines)


def _collect_branch_commits(base_branch: str, head_ref: str) -> tuple[str, list[CommitSelection]]:
    merge_base = _git_stdout("merge-base", base_branch, head_ref)
    raw = _git_stdout("log", "--reverse", "--format=%H%x1f%s", f"{base_branch}..{head_ref}")
    items: list[CommitSelection] = []
    if raw:
        for line in raw.splitlines():
            sha, subject = line.split("\x1f", 1)
            match = ID_PREFIX_RE.match(subject.strip())
            matched_id = match.group("id") if match else None
            items.append(
                CommitSelection(
                    sha=sha,
                    subject=subject,
                    matched_id=matched_id,
                    status="unclassified",
                    reason="branch-exclusive commit",
                )
            )
    return merge_base, items


def _build_plan_item(item: dict, defaults: dict, repo_root: Path, preview_path: Path) -> PrPrepPlanItem:
    warnings: list[str] = []
    requested_id = (item.get("requested_id") or defaults.get("requested_id") or "").strip()
    if not requested_id:
        raise SystemExit("PR-prep manifest item missing requested_id")

    source_log_value = item.get("source_log_path") or defaults.get("source_log_path")
    if not source_log_value:
        raise SystemExit("PR-prep manifest item missing source_log_path")
    source_log_path = _coerce_path(source_log_value, repo_root)
    if not source_log_path.is_file():
        raise SystemExit(f"PR-prep source log not found: {source_log_path}")

    fields = _parse_fields(_load_text(source_log_path))
    sections = _parse_sections(_load_text(source_log_path))
    source_log_rel = _repo_rel(source_log_path)

    current_branch = _git_stdout("branch", "--show-current")
    head_ref = (item.get("head_ref") or defaults.get("head_ref") or current_branch or "HEAD").strip()
    manifest_base_branch = (item.get("base_branch") or defaults.get("base_branch") or "").strip() or None
    source_log_pr_base = fields.get("pr_base", "").strip() or None

    if manifest_base_branch and source_log_pr_base and manifest_base_branch != source_log_pr_base:
        warnings.append("manifest base_branch differs from source log pr_base; source log pr_base remains canonical")

    base_branch = source_log_pr_base or manifest_base_branch
    if not base_branch:
        return PrPrepPlanItem(
            requested_id=requested_id,
            source_log_path=source_log_rel,
            current_branch=current_branch,
            head_ref=head_ref,
            base_branch="",
            merge_base="",
            candidate_pr_branch="",
            pr_title="",
            pr_base=source_log_pr_base,
            pr_labels=_split_csv(fields.get("pr_labels")),
            pr_projects=_split_csv(fields.get("pr_projects")),
            pr_milestone=fields.get("pr_milestone", "").strip() or None,
            pr_development_issue=fields.get("pr_development_issue", "").strip() or None,
            preview_body_path=_repo_rel(preview_path),
            selected_commit_count=0,
            selected_commits=[],
            branch_commits=[],
            planned_action="error-missing-base-branch",
            status="error",
            warnings=warnings + ["base branch is required for PR-prep dry-run"],
        )

    merge_base, branch_commits = _collect_branch_commits(base_branch, head_ref)
    selected_commits: list[CommitSelection] = []
    for commit in branch_commits:
        if commit.matched_id == requested_id:
            commit.status = "selected"
            commit.reason = "commit subject matches requested ID prefix"
            selected_commits.append(commit)
        else:
            commit.status = "skipped"
            commit.reason = "commit subject does not match requested ID prefix"

    if not selected_commits:
        warnings.append("no branch-exclusive commits matched the requested ID prefix")

    requested_slug = _normalize_branch_name(requested_id)
    candidate_pr_branch = (item.get("candidate_pr_branch") or defaults.get("candidate_pr_branch") or f"pr-prep/{requested_slug}").strip()

    pr_title = f"{fields.get('id', requested_id).strip()}: {fields.get('title', requested_id).strip()}"
    summary_bullets, explicit_link_lines = _parse_pr_summary_inputs(sections.get("PR Summary Inputs", []))
    if not summary_bullets:
        warnings.append("source log is missing PR summary bullets; preview uses placeholders")
    checklist_items = _extract_checked_items(sections.get("Execution Checklist (unchecked)", []))
    if not checklist_items:
        checklist_items = _extract_checked_items(sections.get("Execution Checklist", []))
    if not checklist_items:
        warnings.append("source log has no checked execution checklist items for PR preview")

    link_lines = explicit_link_lines or _build_default_link_lines(fields, source_log_rel)
    pr_development_issue = fields.get("pr_development_issue", "").strip() or None
    preview_body = _render_body_preview(
        requested_id=requested_id,
        pr_title=pr_title,
        base_branch=base_branch,
        candidate_pr_branch=candidate_pr_branch,
        source_log_path=source_log_rel,
        summary_bullets=summary_bullets,
        checklist_items=checklist_items,
        link_lines=link_lines,
        selected_commits=selected_commits,
        pr_development_issue=pr_development_issue,
    )
    preview_path.write_text(preview_body + "\n", encoding="utf-8")

    status = "planned" if selected_commits else "warning"
    planned_action = "prepare-pr-prep-branch" if selected_commits else "inspect-commit-history"
    return PrPrepPlanItem(
        requested_id=requested_id,
        source_log_path=source_log_rel,
        current_branch=current_branch,
        head_ref=head_ref,
        base_branch=base_branch,
        merge_base=merge_base,
        candidate_pr_branch=candidate_pr_branch,
        pr_title=pr_title,
        pr_base=source_log_pr_base,
        pr_labels=_split_csv(fields.get("pr_labels")),
        pr_projects=_split_csv(fields.get("pr_projects")),
        pr_milestone=fields.get("pr_milestone", "").strip() or None,
        pr_development_issue=pr_development_issue,
        preview_body_path=_repo_rel(preview_path),
        selected_commit_count=len(selected_commits),
        selected_commits=selected_commits,
        branch_commits=branch_commits,
        planned_action=planned_action,
        status=status,
        warnings=warnings,
    )


def plan_pr_prep(args: argparse.Namespace) -> PrPrepPlanResult:
    repo_root = _repo_root()
    manifest_path = _coerce_path(args.manifest_path, repo_root)
    if not manifest_path.is_file():
        raise SystemExit(f"PR-prep manifest file not found: {manifest_path}")

    manifest = _load_manifest(manifest_path)
    defaults = manifest.get("defaults") or {}
    items = manifest.get("items") or []
    if not items:
        raise SystemExit("PR-prep manifest requires at least one item")

    manifest_rel = _repo_rel(manifest_path)
    manifest_slug = manifest_path.stem
    if manifest_slug.endswith("-manifest"):
        manifest_slug = manifest_slug[: -len("-manifest")]
    default_plan_path = repo_root / "docs" / "issues" / f"{manifest_slug}-plan.json"
    plan_path = _coerce_path(args.plan_path, repo_root) if args.plan_path else default_plan_path
    plan_path.parent.mkdir(parents=True, exist_ok=True)

    preview_path = plan_path.with_name(f"{manifest_slug}-body.md")
    plan_items = [_build_plan_item(item, defaults, repo_root, preview_path) for item in items]
    top_warnings: list[str] = []
    for item in plan_items:
        for warning in item.warnings:
            top_warnings.append(f"{item.requested_id}: {warning}")

    result = PrPrepPlanResult(
        mode="pr-prep-dry-run",
        result="ok",
        manifest_path=manifest_rel,
        selection_input="manifest",
        operation="plan-pr-prep",
        total_items=len(plan_items),
        planned_items=sum(1 for item in plan_items if item.status == "planned"),
        warnings=top_warnings,
        items=plan_items,
    )
    plan_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        plan_pr_prep(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())