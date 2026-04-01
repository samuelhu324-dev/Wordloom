from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import (
    _derive_repo_slug,
    _load_text,
    _parse_fields,
    _parse_sections,
    _repo_rel,
    _repo_root,
    _require_gh_auth,
    _require_gh_cli,
    _run_command,
)
from body_contract import build_issue_conclusion_context_lines, issue_body_context_line_bounds, validate_issue_context_lines


ISSUE_URL_RE = re.compile(r"/issues/(?P<number>\d+)$")
PR_REF_RE = re.compile(r"(?:/pull/|^#?)(?P<number>\d+)$")
TITLE_UNIT_RE = re.compile(r"^(?P<id>[A-Z0-9-]+)/(?P<unit>[^:]+):")


@dataclass
class MergedPrEvidence:
    number: int
    title: str
    url: str
    merged_at: str


@dataclass
class IssueConclusionPlanItem:
    requested_id: str
    source_log_path: str
    issue_number: int | None
    issue_url: str | None
    issue_title: str | None
    issue_state: str | None
    preview_body_path: str
    merged_pr_count: int
    merged_prs: list[MergedPrEvidence]
    planned_action: str
    applied_action: str | None
    status: str
    warnings: list[str]
    reason: str | None = None


@dataclass
class IssueConclusionPlanResult:
    mode: str
    result: str
    manifest_path: str | None
    selection_input: str
    operation: str
    total_items: int
    planned_items: int
    warnings: list[str]
    items: list[IssueConclusionPlanItem]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan issue conclusion output from merged PR evidence")
    parser.add_argument("manifest_path", help="Path to an issue-conclusion manifest JSON file")
    parser.add_argument("--plan-path", dest="plan_path", help="Override output plan JSON path")
    parser.add_argument(
        "--context-mode",
        dest="context_mode",
        choices=["preserve-existing", "single-generate"],
        default="preserve-existing",
        help="How to handle Context during conclusion planning: preserve-existing keeps the live block, single-generate rewrites it from the source log",
    )
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
        raise SystemExit(f"Failed to parse issue-conclusion manifest JSON: {exc}") from exc


def _normalize_issue_ref(number: int | None, url: str | None) -> tuple[int | None, str | None, list[str]]:
    warnings: list[str] = []
    parsed_number = number
    parsed_url = url.strip() if isinstance(url, str) and url.strip() else None
    if parsed_url:
        match = ISSUE_URL_RE.search(parsed_url)
        if not match:
            raise SystemExit(f"Invalid issue URL: {parsed_url}")
        url_number = int(match.group("number"))
        if parsed_number is not None and parsed_number != url_number:
            warnings.append("issue number/url mismatch; moving item to reconciliation")
        else:
            parsed_number = url_number
    return parsed_number, parsed_url, warnings


def _normalize_pr_override_refs(raw: object) -> list[str]:
    tokens: list[str] = []
    if raw is None:
        return tokens
    if isinstance(raw, str):
        candidates = [part.strip() for part in raw.split(",") if part.strip()]
    elif isinstance(raw, list):
        candidates = [str(part).strip() for part in raw if str(part).strip()]
    else:
        raise SystemExit("merged_pr_overrides must be a string or array")

    for token in candidates:
        match = PR_REF_RE.search(token)
        if not match:
            raise SystemExit(f"Invalid merged PR override reference: {token}")
        tokens.append(match.group("number"))
    seen: set[str] = set()
    result: list[str] = []
    for token in tokens:
        if token not in seen:
            seen.add(token)
            result.append(token)
    return result


def _fetch_issue_state(repo: str, issue_ref: str) -> dict:
    cmd = _run_command([
        "gh",
        "issue",
        "view",
        issue_ref,
        "--repo",
        repo,
        "--json",
        "number,url,title,state,body,labels",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to view issue {issue_ref} in {repo}: {cmd.stderr.strip()}")
    try:
        return json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse issue view JSON: {exc}") from exc


def _fetch_pr_state(repo: str, pr_ref: str) -> dict:
    cmd = _run_command([
        "gh",
        "pr",
        "view",
        pr_ref,
        "--repo",
        repo,
        "--json",
        "number,title,url,state,isDraft,mergedAt",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to view PR {pr_ref} in {repo}: {cmd.stderr.strip()}")
    try:
        return json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse PR view JSON: {exc}") from exc


def _fetch_candidate_prs(repo: str, requested_id: str) -> list[dict]:
    cmd = _run_command([
        "gh",
        "pr",
        "list",
        "--repo",
        repo,
        "--state",
        "merged",
        "--search",
        f"{requested_id}/ in:title",
        "--limit",
        "100",
        "--json",
        "number,title,url,state,isDraft,mergedAt",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to list merged PRs for {requested_id} in {repo}: {cmd.stderr.strip()}")
    try:
        data = json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse PR list JSON: {exc}") from exc
    return [
        item for item in data
        if isinstance(item, dict)
        and str(item.get("title", "")).startswith(f"{requested_id}/")
        and item.get("mergedAt")
        and item.get("state") == "MERGED"
        and not item.get("isDraft")
    ]


def _extract_section_lines(body: str, heading: str) -> list[str]:
    sections = _parse_sections(body)
    return sections.get(heading, [])


def _extract_bullet_lines(section_lines: list[str]) -> list[str]:
    lines: list[str] = []
    for raw in section_lines:
        stripped = raw.strip()
        if stripped.startswith("- "):
            lines.append(stripped)
    return lines


def _has_substantive_text(section_lines: list[str]) -> bool:
    for raw in section_lines:
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped == "- <placeholder>":
            continue
        return True
    return False


def _fallback_metadata_lines(issue_data: dict, source_log_rel: str) -> list[str]:
    labels = [item.get("name", "") for item in issue_data.get("labels", []) if isinstance(item, dict) and item.get("name")]
    return [
        f"- Labels: {', '.join(f'`{label}`' for label in labels) if labels else '``'}",
        "- Projects: ``",
        "- Milestone: ``",
        f"- Source log: `{source_log_rel}`",
    ]


def _parse_unit_sort_key(pr_title: str) -> tuple[int, int, int, int]:
    match = TITLE_UNIT_RE.match(pr_title.strip())
    if not match:
        return (10**9, 10**9, 10**9, 10**9)
    unit = match.group("unit")
    phase_values = [int(value) for value in re.findall(r"P(\d+)", unit)]
    cycle_values = [int(value) for value in re.findall(r"C(\d+)", unit)]
    step_values = [int(value) for value in re.findall(r"S(\d+)", unit)]
    return (
        min(phase_values) if phase_values else 10**9,
        min(cycle_values) if cycle_values else 10**9,
        min(step_values) if step_values else 10**9,
        len(phase_values),
    )


def _sort_prs(items: list[dict]) -> list[dict]:
    return sorted(
        items,
        key=lambda item: (
            _parse_unit_sort_key(str(item.get("title", ""))),
            str(item.get("mergedAt", "")),
            int(item.get("number", 0)),
        ),
    )


def _build_link_lines(existing_link_lines: list[str], issue_url: str, merged_prs: list[MergedPrEvidence]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()

    def add(line: str) -> None:
        if line not in seen:
            seen.add(line)
            result.append(line)

    for line in existing_link_lines:
        if line.startswith("- PR:") or line.startswith("- Issue:"):
            continue
        add(line)
    return result


def _render_body_preview(
    metadata_lines: list[str],
    context_lines: list[str],
    merged_prs: list[MergedPrEvidence],
    link_lines: list[str],
) -> str:
    dod_lines = [f"- #{pr.number}" for pr in merged_prs]
    lines = ["## Metadata", "", *metadata_lines]
    lines.extend(["", "## Context", "", *context_lines])
    lines.extend([
        "",
        "## Definition of Done (DoD)",
        "",
        *dod_lines,
        "",
        "## Links",
        "",
        *link_lines,
        "",
    ])
    return "\n".join(lines)


def _build_item(
    item: dict,
    defaults: dict,
    repo_root: Path,
    repo: str,
    preview_path: Path,
    cli_context_mode: str,
) -> IssueConclusionPlanItem:
    warnings: list[str] = []
    source_log_value = item.get("source_log_path") or defaults.get("source_log_path")
    if not source_log_value:
        raise SystemExit("Issue-conclusion manifest item missing source_log_path")
    source_log_path = _coerce_path(source_log_value, repo_root)
    if not source_log_path.is_file():
        raise SystemExit(f"Issue-conclusion source log not found: {source_log_path}")

    fields = _parse_fields(_load_text(source_log_path))
    requested_id = (item.get("requested_id") or fields.get("id") or "").strip()
    if not requested_id:
        raise SystemExit("Issue-conclusion manifest item missing requested_id")

    issue_number, issue_url, ref_warnings = _normalize_issue_ref(item.get("issue_number"), item.get("issue_url"))
    warnings.extend(ref_warnings)
    if issue_number is None:
        warnings.append("explicit issue reference is required for issue conclusion planning")
        return IssueConclusionPlanItem(
            requested_id=requested_id,
            source_log_path=_repo_rel(source_log_path),
            issue_number=None,
            issue_url=issue_url,
            issue_title=None,
            issue_state=None,
            preview_body_path=_repo_rel(preview_path),
            merged_pr_count=0,
            merged_prs=[],
            planned_action="error-missing-issue-reference",
            applied_action=None,
            status="error",
            warnings=warnings,
            reason=item.get("reason"),
        )

    issue_data = _fetch_issue_state(repo, issue_url or str(issue_number))
    issue_number = int(issue_data["number"])
    issue_url = str(issue_data["url"])
    issue_title = str(issue_data.get("title") or "")
    issue_state = str(issue_data.get("state") or "")
    if issue_state != "CLOSED":
        warnings.append("issue is not closed yet; conclusion body may still be planned after merge evidence is available")

    override_refs = _normalize_pr_override_refs(item.get("merged_pr_overrides"))
    candidate_prs = [_fetch_pr_state(repo, pr_ref) for pr_ref in override_refs] if override_refs else _fetch_candidate_prs(repo, requested_id)
    if override_refs:
        warnings.append("merged PR set supplied by explicit override")

    merged_candidates: list[dict] = []
    for pr in candidate_prs:
        if pr.get("state") != "MERGED" or not pr.get("mergedAt") or pr.get("isDraft"):
            warnings.append(f"PR #{pr.get('number')} is not a merged non-draft PR; item moved to error")
            return IssueConclusionPlanItem(
                requested_id=requested_id,
                source_log_path=_repo_rel(source_log_path),
                issue_number=issue_number,
                issue_url=issue_url,
                issue_title=issue_title,
                issue_state=issue_state,
                preview_body_path=_repo_rel(preview_path),
                merged_pr_count=0,
                merged_prs=[],
                planned_action="error-unmerged-pr-evidence",
                applied_action=None,
                status="error",
                warnings=warnings,
                reason=item.get("reason"),
            )
        if not override_refs and not str(pr.get("title", "")).startswith(f"{requested_id}/"):
            continue
        merged_candidates.append(pr)

    if not merged_candidates:
        warnings.append("no merged PRs matched the requested exact ID prefix")
        return IssueConclusionPlanItem(
            requested_id=requested_id,
            source_log_path=_repo_rel(source_log_path),
            issue_number=issue_number,
            issue_url=issue_url,
            issue_title=issue_title,
            issue_state=issue_state,
            preview_body_path=_repo_rel(preview_path),
            merged_pr_count=0,
            merged_prs=[],
            planned_action="error-missing-merged-pr-evidence",
            applied_action=None,
            status="error",
            warnings=warnings,
            reason=item.get("reason"),
        )

    ordered_prs = [
        MergedPrEvidence(
            number=int(pr["number"]),
            title=str(pr["title"]),
            url=str(pr["url"]),
            merged_at=str(pr["mergedAt"]),
        )
        for pr in _sort_prs(merged_candidates)
    ]

    body = str(issue_data.get("body") or "")
    metadata_lines = _extract_bullet_lines(_extract_section_lines(body, "Metadata"))
    if not metadata_lines:
        metadata_lines = _fallback_metadata_lines(issue_data, _repo_rel(source_log_path))
        warnings.append("issue body metadata block missing; preview uses reconstructed metadata")

    source_log_text = _load_text(source_log_path)
    context_section_lines = _extract_section_lines(body, "Context")
    context_line_bounds = issue_body_context_line_bounds(source_log_text)
    context_ok, _, _ = validate_issue_context_lines(context_section_lines, context_line_bounds, source_log_text)
    context_mode = str(item.get("context_mode") or defaults.get("context_mode") or cli_context_mode or "preserve-existing")
    if context_mode not in {"preserve-existing", "single-generate"}:
        raise SystemExit(f"Unsupported issue-conclusion context_mode: {context_mode}")
    if context_mode == "single-generate":
        context_lines = build_issue_conclusion_context_lines(source_log_text, [pr.number for pr in ordered_prs])
    else:
        context_lines = context_section_lines
    existing_link_lines = _extract_bullet_lines(_extract_section_lines(body, "Links"))
    link_lines = _build_link_lines(existing_link_lines, issue_url, ordered_prs)

    if context_mode == "single-generate":
        warnings.append("preview uses a single-generated conclusion Context block that ends on outcome wording and keeps exact merged-PR evidence in DoD only; do not use this mode for batch authoring unless the rewrite is explicitly intended")
        if not context_ok:
            warnings.append(f"existing Context section did not satisfy the prose-first Context gate for line range {context_line_bounds}; preview uses the single-generated conclusion Context block with outcome wording instead of PR-evidence wording")
    else:
        if context_section_lines:
            if context_ok:
                warnings.append("preview preserves the existing live Context block because batch conclusion planning now avoids Context authoring by default")
            else:
                warnings.append(f"existing Context section did not satisfy the prose-first Context gate for line range {context_line_bounds}; preview preserves the live Context block and leaves one-item Context authoring to manual or single-item generation")
        else:
            warnings.append("Context section is blank in the live issue body; batch conclusion planning preserved that state instead of auto-authoring replacement prose")
    if not _has_substantive_text(_extract_section_lines(body, "Definition of Done (DoD)")):
        warnings.append("existing issue DoD is still blank create-time scaffold")

    preview_body = _render_body_preview(metadata_lines, context_lines, ordered_prs, link_lines)
    preview_path.write_text(preview_body + "\n", encoding="utf-8")

    return IssueConclusionPlanItem(
        requested_id=requested_id,
        source_log_path=_repo_rel(source_log_path),
        issue_number=issue_number,
        issue_url=issue_url,
        issue_title=issue_title,
        issue_state=issue_state,
        preview_body_path=_repo_rel(preview_path),
        merged_pr_count=len(ordered_prs),
        merged_prs=ordered_prs,
        planned_action="plan-issue-conclusion",
        applied_action=None,
        status="planned",
        warnings=warnings,
        reason=item.get("reason"),
    )


def plan_issue_conclusion(args: argparse.Namespace) -> IssueConclusionPlanResult:
    repo_root = _repo_root()
    manifest_path = _coerce_path(args.manifest_path, repo_root)
    if not manifest_path.is_file():
        raise SystemExit(f"Issue-conclusion manifest file not found: {manifest_path}")

    manifest = _load_manifest(manifest_path)
    defaults = manifest.get("defaults") or {}
    raw_items = manifest.get("items") or []
    if not raw_items:
        raise SystemExit(f"No issue-conclusion items defined in manifest: {manifest_path}")

    _require_gh_cli()
    _require_gh_auth()
    repo = _derive_repo_slug(defaults.get("repo"))

    manifest_rel = _repo_rel(manifest_path)
    manifest_stem = manifest_path.stem
    if manifest_stem.startswith("issue-conclusion-"):
        manifest_slug = manifest_stem.removeprefix("issue-conclusion-")
    else:
        manifest_slug = manifest_stem.removeprefix("issue-")
    if manifest_slug.endswith("-manifest"):
        manifest_slug = manifest_slug[: -len("-manifest")]
    default_plan_path = repo_root / "docs" / "issues" / f"issue-conclusion-{manifest_slug}-plan.json"
    plan_path = _coerce_path(args.plan_path, repo_root) if args.plan_path else default_plan_path
    plan_path.parent.mkdir(parents=True, exist_ok=True)

    items: list[IssueConclusionPlanItem] = []
    for raw_item in raw_items:
        requested_id = (raw_item.get("requested_id") or "item").strip() or "item"
        preview_name = raw_item.get("body_output_path")
        if preview_name:
            preview_path = _coerce_path(str(preview_name), repo_root)
        else:
            preview_path = plan_path.with_name(f"issue-conclusion-{manifest_slug}-{requested_id.lower()}-body.md")
        preview_path.parent.mkdir(parents=True, exist_ok=True)
        items.append(_build_item(raw_item, defaults, repo_root, repo, preview_path, args.context_mode))

    top_warnings = [
        f"item {index + 1}: {item.status}"
        for index, item in enumerate(items)
        if item.status != "planned"
    ]
    for item in items:
        for warning in item.warnings:
            top_warnings.append(f"{item.requested_id}: {warning}")

    result = IssueConclusionPlanResult(
        mode="issue-conclusion-dry-run",
        result="ok",
        manifest_path=manifest_rel,
        selection_input="manifest",
        operation="plan-issue-conclusion",
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
        plan_issue_conclusion(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())