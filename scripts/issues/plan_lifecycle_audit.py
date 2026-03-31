from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from body_contract import ISSUE_ALLOWED_LINK_LABELS, bullets_are_contiguous, extract_section_order, link_labels_are_allowed
from gen_issue_draft import (
    _derive_function_labels,
    _derive_module_labels,
    _derive_repo_slug,
    _derive_scope_labels,
    _derive_top_labels,
    _load_text,
    _parse_fields,
    _parse_sections,
    _repo_rel,
    _repo_root,
    _require_gh_auth,
    _require_gh_cli,
    _run_command,
    _split_csv,
)


ISSUE_URL_RE = re.compile(r"/issues/(\d+)$")
PR_REF_RE = re.compile(r"(?:/pull/|#)(\d+)$")
TITLE_UNIT_RE = re.compile(r"^[A-Z0-9-]+/(?P<unit>P\d+(?:[-+]P\d+)*(?:-C\d+(?:-S\d+(?:S\d+)*)?)?)")


@dataclass
class MergedPrEvidence:
    number: int
    title: str
    url: str
    merged_at: str


@dataclass
class AuditCheck:
    name: str
    status: str
    details: str


@dataclass
class LifecycleAuditPlanItem:
    requested_id: str
    source_log_path: str
    issue_number: int | None
    issue_url: str | None
    issue_title: str | None
    issue_state: str | None
    lifecycle_stage: str | None
    expected_parent_issue_number: int | None
    actual_parent_issue_number: int | None
    source_log_issue_url: str | None
    source_log_pr_url: str | None
    merged_pr_count: int
    merged_prs: list[MergedPrEvidence]
    planned_action: str
    applied_action: str | None
    status: str
    checks: list[AuditCheck]
    warnings: list[str]
    reason: str | None = None


@dataclass
class LifecycleAuditPlanResult:
    mode: str
    result: str
    manifest_path: str | None
    selection_input: str
    operation: str
    total_items: int
    planned_items: int
    warnings: list[str]
    items: list[LifecycleAuditPlanItem]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan dry-run lifecycle audits for existing issue/PR chains")
    parser.add_argument("manifest_path", help="Path to a lifecycle-audit manifest JSON file")
    parser.add_argument("--plan-path", dest="plan_path", help="Override output plan JSON path")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
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
        raise SystemExit(f"Failed to parse lifecycle-audit manifest JSON: {exc}") from exc


def _parse_issue_number_from_url(url: str | None) -> int | None:
    if not url:
        return None
    match = ISSUE_URL_RE.search(url.strip())
    return int(match.group(1)) if match else None


def _normalize_issue_ref(number: int | None, url: str | None) -> tuple[int | None, str | None, list[str]]:
    warnings: list[str] = []
    parsed_number = number
    parsed_url = url.strip() if isinstance(url, str) and url.strip() else None
    if parsed_url:
        url_number = _parse_issue_number_from_url(parsed_url)
        if url_number is None:
            raise SystemExit(f"Invalid issue URL: {parsed_url}")
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
        tokens.append(match.group(1))

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


def _fetch_issue_parent(repo: str, issue_number: int) -> tuple[int | None, str | None]:
    owner, name = repo.split("/", 1)
    query = """
query($owner:String!, $name:String!, $number:Int!) {
  repository(owner:$owner, name:$name) {
    issue(number:$number) {
      parent {
        number
        title
      }
    }
  }
}
"""
    cmd = _run_command([
        "gh",
        "api",
        "graphql",
        "-f",
        f"query={query}",
        "-F",
        f"owner={owner}",
        "-F",
        f"name={name}",
        "-F",
        f"number={issue_number}",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to fetch issue parent via GraphQL: {cmd.stderr.strip()}")
    try:
        payload = json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse GraphQL issue parent JSON: {exc}") from exc
    parent = (((payload.get("data") or {}).get("repository") or {}).get("issue") or {}).get("parent") or None
    if not isinstance(parent, dict):
        return None, None
    number = parent.get("number")
    title = parent.get("title")
    return (int(number) if number is not None else None), str(title) if title else None


def _load_log_issue_ref(log_path: str | None, repo_root: Path) -> tuple[int | None, str | None]:
    if not log_path:
        return None, None
    resolved = _coerce_path(log_path, repo_root)
    if not resolved.is_file():
        raise SystemExit(f"Log not found: {resolved}")
    fields = _parse_fields(_load_text(resolved))
    issue_url = fields.get("issue", "").strip() or None
    return _parse_issue_number_from_url(issue_url), issue_url


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


def _build_check(name: str, status: str, details: str) -> AuditCheck:
    return AuditCheck(name=name, status=status, details=details)


def _contains_fragment(lines: list[str], fragment: str) -> bool:
    return any(fragment in line for line in lines)


def _extract_dod_refs(lines: list[str]) -> list[str]:
    refs: list[str] = []
    for line in lines:
        match = re.match(r"-\s+#(\d+)\s*$", line)
        if match:
            refs.append(f"#{match.group(1)}")
    return refs


def _build_planned_action(status: str) -> str:
    if status == "pass":
        return "pass-audit"
    if status == "warning":
        return "review-audit-findings"
    if status == "blocked":
        return "block-mutation"
    if status == "reconciliation":
        return "reconcile-audit-input"
    return "error-audit-input"


def _classify_stage(issue_state: str, merged_prs: list[MergedPrEvidence], source_log_pr_url: str | None, link_lines: list[str]) -> str:
    if issue_state == "CLOSED":
        return "concluded"
    if merged_prs:
        return "merged-open"
    if source_log_pr_url or any("/pull/" in line for line in link_lines):
        return "pr-linked"
    return "issue-created"


def _item_bool(item: dict, defaults: dict, key: str, fallback: bool = True) -> bool:
    if key in item:
        return bool(item.get(key))
    if key in defaults:
        return bool(defaults.get(key))
    return fallback


def _expected_parent_issue_number(item: dict, defaults: dict, fields: dict[str, str], repo_root: Path) -> tuple[int | None, list[str]]:
    warnings: list[str] = []
    explicit = item.get("expected_parent_issue_number")
    if explicit is None:
        explicit = defaults.get("expected_parent_issue_number")
    if explicit is not None:
        expected = int(explicit)
    else:
        parent_log_path = fields.get("parent_log", "").strip() or item.get("parent_log_path") or defaults.get("parent_log_path")
        parent_log_issue_number, _ = _load_log_issue_ref(parent_log_path, repo_root) if parent_log_path else (None, None)
        expected = parent_log_issue_number
        if expected is None and parent_log_path:
            warnings.append("parent log exists but has no live issue reference for relationship audit")
    return expected, warnings


def _build_item(item: dict, defaults: dict, repo_root: Path, repo: str) -> LifecycleAuditPlanItem:
    warnings: list[str] = []
    source_log_value = item.get("source_log_path") or defaults.get("source_log_path")
    if not source_log_value:
        raise SystemExit("Lifecycle-audit manifest item missing source_log_path")
    source_log_path = _coerce_path(source_log_value, repo_root)
    if not source_log_path.is_file():
        raise SystemExit(f"Lifecycle-audit source log not found: {source_log_path}")

    full_text = _load_text(source_log_path)
    fields = _parse_fields(full_text)
    log_sections = _parse_sections(full_text)
    requested_id = str(item.get("requested_id") or fields.get("id") or "").strip()
    if not requested_id:
        raise SystemExit(f"Lifecycle-audit source log has no id field: {source_log_path}")

    explicit_issue_number, explicit_issue_url, ref_warnings = _normalize_issue_ref(item.get("issue_number"), item.get("issue_url"))
    warnings.extend(ref_warnings)

    source_log_issue_url = fields.get("issue", "").strip() or None
    source_log_issue_number = _parse_issue_number_from_url(source_log_issue_url)
    source_log_pr_url = fields.get("pr", "").strip() or None

    if explicit_issue_number is None and source_log_issue_number is not None:
        explicit_issue_number = source_log_issue_number
        explicit_issue_url = source_log_issue_url
    elif explicit_issue_number is not None and source_log_issue_number is not None and explicit_issue_number != source_log_issue_number:
        warnings.append("source log issue reference conflicts with explicit issue reference")

    if explicit_issue_number is None:
        return LifecycleAuditPlanItem(
            requested_id=requested_id,
            source_log_path=_repo_rel(source_log_path),
            issue_number=None,
            issue_url=explicit_issue_url,
            issue_title=None,
            issue_state=None,
            lifecycle_stage=None,
            expected_parent_issue_number=None,
            actual_parent_issue_number=None,
            source_log_issue_url=source_log_issue_url,
            source_log_pr_url=source_log_pr_url,
            merged_pr_count=0,
            merged_prs=[],
            planned_action="error-missing-issue-reference",
            applied_action=None,
            status="error",
            checks=[],
            warnings=warnings + ["explicit issue reference is required or source log links.issue must be populated"],
            reason=item.get("reason"),
        )

    if any("conflicts" in warning or "mismatch" in warning for warning in warnings):
        return LifecycleAuditPlanItem(
            requested_id=requested_id,
            source_log_path=_repo_rel(source_log_path),
            issue_number=explicit_issue_number,
            issue_url=explicit_issue_url,
            issue_title=None,
            issue_state=None,
            lifecycle_stage=None,
            expected_parent_issue_number=None,
            actual_parent_issue_number=None,
            source_log_issue_url=source_log_issue_url,
            source_log_pr_url=source_log_pr_url,
            merged_pr_count=0,
            merged_prs=[],
            planned_action="reconcile-audit-input",
            applied_action=None,
            status="reconciliation",
            checks=[],
            warnings=warnings,
            reason=item.get("reason"),
        )

    issue_data = _fetch_issue_state(repo, explicit_issue_url or str(explicit_issue_number))
    issue_number = int(issue_data["number"])
    issue_url = str(issue_data["url"])
    issue_title = str(issue_data["title"])
    issue_state = str(issue_data["state"])
    issue_body = str(issue_data.get("body") or "")
    body_sections = _parse_sections(issue_body)
    metadata_lines = _extract_bullet_lines(_extract_section_lines(issue_body, "Metadata"))
    dod_lines = _extract_bullet_lines(_extract_section_lines(issue_body, "Definition of Done (DoD)"))
    link_lines = _extract_bullet_lines(_extract_section_lines(issue_body, "Links"))
    context_lines = _extract_section_lines(issue_body, "Context")

    expected_parent_issue_number, parent_warnings = _expected_parent_issue_number(item, defaults, fields, repo_root)
    warnings.extend(parent_warnings)
    actual_parent_issue_number, _ = _fetch_issue_parent(repo, issue_number)

    override_refs = _normalize_pr_override_refs(item.get("merged_pr_overrides"))
    if override_refs:
        warnings.append("merged PR set supplied by explicit override")
        pr_items = [_fetch_pr_state(repo, ref) for ref in override_refs]
    else:
        pr_items = _fetch_candidate_prs(repo, requested_id)
    ordered_prs = [
        MergedPrEvidence(
            number=int(pr["number"]),
            title=str(pr["title"]),
            url=str(pr["url"]),
            merged_at=str(pr["mergedAt"]),
        )
        for pr in _sort_prs(pr_items)
    ]

    lifecycle_stage = _classify_stage(issue_state, ordered_prs, source_log_pr_url, link_lines)

    tags = _split_csv(fields.get("tags"))
    log_title = str(fields.get("title") or requested_id)
    scope = str(fields.get("scope") or "")
    expected_labels = []
    if _item_bool(item, defaults, "check_expected_labels", True):
        expected_labels = list(dict.fromkeys(
            _derive_top_labels(fields, tags)
            + _derive_scope_labels(fields, requested_id, scope)
            + _derive_function_labels(log_title, tags, log_sections)
            + _derive_module_labels(fields, [])
        ))
    live_labels = [label.get("name", "") for label in issue_data.get("labels", []) if isinstance(label, dict) and label.get("name")]

    checks: list[AuditCheck] = []

    if source_log_issue_url == issue_url:
        checks.append(_build_check("source-log-issue-writeback", "pass", "source log links.issue matches the live issue URL"))
    elif source_log_issue_url:
        checks.append(_build_check("source-log-issue-writeback", "fail", "source log links.issue does not match the live issue URL"))
    else:
        checks.append(_build_check("source-log-issue-writeback", "fail", "source log links.issue is blank"))

    missing_sections = [name for name in ["Metadata", "Context", "Definition of Done (DoD)", "Links"] if name not in body_sections]
    if missing_sections:
        checks.append(_build_check("required-body-sections", "fail", f"missing required sections: {', '.join(missing_sections)}"))
    else:
        checks.append(_build_check("required-body-sections", "pass", "Metadata, Context, Definition of Done (DoD), and Links sections are present"))

    issue_section_order = extract_section_order(issue_body)
    expected_issue_section_order = ["Metadata", "Context", "Definition of Done (DoD)", "Links"]
    filtered_issue_order = [name for name in issue_section_order if name in expected_issue_section_order]
    if filtered_issue_order == expected_issue_section_order:
        checks.append(_build_check("issue-section-order", "pass", "issue body section order matches the canonical contract"))
    else:
        checks.append(_build_check("issue-section-order", "fail", f"issue body section order is {filtered_issue_order}; expected {expected_issue_section_order}"))

    if bullets_are_contiguous(_extract_section_lines(issue_body, "Metadata")):
        checks.append(_build_check("metadata-row-shape", "pass", "Metadata bullet rows are contiguous"))
    else:
        checks.append(_build_check("metadata-row-shape", "fail", "Metadata bullet rows contain blank gaps or non-bullet content"))

    if expected_labels:
        missing_labels = [label for label in expected_labels if label not in live_labels]
        if missing_labels:
            checks.append(_build_check("expected-labels", "fail", f"missing expected labels: {', '.join(missing_labels)}"))
        else:
            checks.append(_build_check("expected-labels", "pass", "live issue labels cover the deterministic label set derived from the source log"))
    else:
        checks.append(_build_check("expected-labels", "skipped", "no deterministic labels were derived from the source log"))

    if expected_parent_issue_number is not None:
        if _contains_fragment(metadata_lines, f"Parent issue: #{expected_parent_issue_number}"):
            checks.append(_build_check("body-parent-metadata", "pass", f"Metadata section records Parent issue: #{expected_parent_issue_number}"))
        else:
            checks.append(_build_check("body-parent-metadata", "fail", f"Metadata section does not record Parent issue: #{expected_parent_issue_number}"))

        if actual_parent_issue_number == expected_parent_issue_number:
            checks.append(_build_check("sidebar-parent-relationship", "pass", f"live GitHub parent relationship points to #{expected_parent_issue_number}"))
        else:
            checks.append(_build_check("sidebar-parent-relationship", "fail", f"live GitHub parent relationship is {actual_parent_issue_number}; expected #{expected_parent_issue_number}"))
    else:
        checks.append(_build_check("body-parent-metadata", "skipped", "no expected parent issue was derived for this item"))
        checks.append(_build_check("sidebar-parent-relationship", "skipped", "no expected parent issue was derived for this item"))

    if issue_state == "CLOSED":
        if ordered_prs:
            checks.append(_build_check("exact-id-merged-pr-evidence", "pass", f"found {len(ordered_prs)} exact-ID merged PR(s)"))
        else:
            checks.append(_build_check("exact-id-merged-pr-evidence", "fail", "concluded issue has no exact-ID merged PR evidence"))
    elif ordered_prs:
        checks.append(_build_check("exact-id-merged-pr-evidence", "pass", f"found {len(ordered_prs)} exact-ID merged PR(s)"))
    elif source_log_pr_url:
        checks.append(_build_check("exact-id-merged-pr-evidence", "warning", "source log references a PR, but no exact-ID merged PRs are present yet"))
    else:
        checks.append(_build_check("exact-id-merged-pr-evidence", "skipped", "no merged PR evidence is required for the current issue-created stage"))

    expected_dod_refs = [f"#{pr.number}" for pr in ordered_prs]
    actual_dod_refs = _extract_dod_refs(dod_lines)
    if issue_state == "CLOSED":
        if actual_dod_refs == expected_dod_refs and expected_dod_refs:
            checks.append(_build_check("final-dod-pr-refs", "pass", "DoD PR refs match the exact-ID merged PR evidence set"))
        else:
            checks.append(_build_check("final-dod-pr-refs", "fail", f"DoD PR refs {actual_dod_refs or '[]'} do not match expected {expected_dod_refs or '[]'}"))
    elif ordered_prs:
        checks.append(_build_check("final-dod-pr-refs", "warning", "merged PR evidence exists while the issue is still open; final DoD refs should be reviewed before conclusion"))
    else:
        checks.append(_build_check("final-dod-pr-refs", "skipped", "no final DoD PR refs are required before merged PR evidence exists"))

    links_allowed, invalid_link_rows = link_labels_are_allowed(link_lines, ISSUE_ALLOWED_LINK_LABELS)
    if links_allowed:
        checks.append(_build_check("link-categories", "pass", "Links section uses only allowed issue link categories"))
    else:
        checks.append(_build_check("link-categories", "fail", f"Links section contains invalid rows: {invalid_link_rows}"))

    expected_link_fragments = [f"Log: `{_repo_rel(source_log_path)}`"]
    runbook_value = fields.get("runbook", "").strip()
    if runbook_value:
        expected_link_fragments.append(f"Runbook: `{runbook_value}`")
    parent_log_value = fields.get("parent_log", "").strip()
    if parent_log_value:
        expected_link_fragments.append(f"Parent log: `{parent_log_value}`")
    roadmap_value = fields.get("roadmap", "").strip()
    if roadmap_value:
        expected_link_fragments.append(f"Roadmap: `{roadmap_value}`")
    missing_link_fragments = [fragment for fragment in expected_link_fragments if not _contains_fragment(link_lines, fragment)]
    if missing_link_fragments:
        checks.append(_build_check("links-coverage", "fail", f"Links section is missing expected issue-link fragments: {missing_link_fragments}"))
    else:
        checks.append(_build_check("links-coverage", "pass", "Links section covers the expected canonical issue-link fragments"))

    if issue_state == "CLOSED":
        if _has_substantive_text(context_lines):
            checks.append(_build_check("closed-body-shape", "pass", "concluded issue keeps substantive Context content as required by the canonical contract"))
        else:
            checks.append(_build_check("closed-body-shape", "fail", "concluded issue is missing substantive Context content"))
    else:
        checks.append(_build_check("closed-body-shape", "skipped", "closed-body shape is not required while the issue remains open"))

    if source_log_pr_url:
        merged_urls = [pr.url for pr in ordered_prs]
        if not ordered_prs:
            checks.append(_build_check("source-log-pr-link", "warning", "source log links.pr is populated, but no exact-ID merged PRs exist yet"))
        elif source_log_pr_url in merged_urls:
            checks.append(_build_check("source-log-pr-link", "pass", "source log links.pr is represented in the exact-ID merged PR evidence set"))
        else:
            checks.append(_build_check("source-log-pr-link", "warning", "source log links.pr does not appear in the exact-ID merged PR evidence set"))
    else:
        checks.append(_build_check("source-log-pr-link", "skipped", "source log links.pr is blank"))

    statuses = {check.status for check in checks}
    if "fail" in statuses:
        status = "blocked"
    elif any("mismatch" in warning or "conflicts" in warning for warning in warnings):
        status = "reconciliation"
    elif "warning" in statuses:
        status = "warning"
    else:
        status = "pass"

    return LifecycleAuditPlanItem(
        requested_id=requested_id,
        source_log_path=_repo_rel(source_log_path),
        issue_number=issue_number,
        issue_url=issue_url,
        issue_title=issue_title,
        issue_state=issue_state,
        lifecycle_stage=lifecycle_stage,
        expected_parent_issue_number=expected_parent_issue_number,
        actual_parent_issue_number=actual_parent_issue_number,
        source_log_issue_url=source_log_issue_url,
        source_log_pr_url=source_log_pr_url,
        merged_pr_count=len(ordered_prs),
        merged_prs=ordered_prs,
        planned_action=_build_planned_action(status),
        applied_action=None,
        status=status,
        checks=checks,
        warnings=warnings,
        reason=item.get("reason"),
    )


def plan_lifecycle_audit(args: argparse.Namespace) -> LifecycleAuditPlanResult:
    repo_root = _repo_root()
    manifest_path = _coerce_path(args.manifest_path, repo_root)
    if not manifest_path.is_file():
        raise SystemExit(f"Lifecycle-audit manifest file not found: {manifest_path}")

    manifest = _load_manifest(manifest_path)
    defaults = manifest.get("defaults") or {}
    raw_items = manifest.get("items") or []
    if not raw_items:
        raise SystemExit(f"No lifecycle-audit items defined in manifest: {manifest_path}")

    repo = _derive_repo_slug(args.repo or defaults.get("repo"))
    _require_gh_cli()
    _require_gh_auth()

    items = [_build_item(item, defaults, repo_root, repo) for item in raw_items]
    top_warnings = [
        f"{item.requested_id}: {item.status}"
        for item in items
        if item.status != "pass"
    ]

    manifest_rel = _repo_rel(manifest_path)
    manifest_stem = manifest_path.stem
    if manifest_stem.startswith("lifecycle-audit-"):
        manifest_slug = manifest_stem.removeprefix("lifecycle-audit-")
    else:
        manifest_slug = manifest_stem
    default_plan_path = repo_root / "docs" / "issues" / f"lifecycle-audit-{manifest_slug}-plan.json"
    plan_path = _coerce_path(args.plan_path, repo_root) if args.plan_path else default_plan_path
    plan_path.parent.mkdir(parents=True, exist_ok=True)

    result = LifecycleAuditPlanResult(
        mode="lifecycle-audit-dry-run",
        result="ok",
        manifest_path=manifest_rel,
        selection_input="manifest",
        operation="plan-lifecycle-audit",
        total_items=len(items),
        planned_items=sum(1 for item in items if item.status == "pass"),
        warnings=top_warnings,
        items=items,
    )
    plan_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        plan_lifecycle_audit(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())