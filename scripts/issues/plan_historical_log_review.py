from __future__ import annotations

import argparse
import json
import re
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


ISSUE_URL_RE = re.compile(r"/issues/(\d+)$")
PR_URL_RE = re.compile(r"(?:/pull/|#)(\d+)$")
REQUIRED_FIELD_NAMES = ["id", "kind", "title", "status", "scope", "tags"]
EVIDENCE_FOOTER_LINE_RE = re.compile(r"^`(?P<stage>[^`]+)` \| artifact: `(?P<artifact>[^`]+)`$")
REQUIRED_SECTION_PREFIXES = [
    "Decision / Outcome",
    "Scope",
    "Current Status",
    "Execution Checklist",
    "Evidence",
]


@dataclass
class ReviewCheck:
    name: str
    status: str
    details: str


@dataclass
class HistoricalLogReviewItem:
    requested_id: str
    source_log_path: str
    log_status: str | None
    issue_number: int | None
    issue_url: str | None
    issue_state: str | None
    pr_number: int | None
    pr_url: str | None
    pr_state: str | None
    pr_merged_at: str | None
    lifecycle_stage: str
    structure_status: str
    planned_action: str
    status: str
    checks: list[ReviewCheck]
    warnings: list[str]
    reason: str | None = None


@dataclass
class HistoricalLogReviewResult:
    mode: str
    result: str
    manifest_path: str
    selection_input: str
    operation: str
    repository: str | None
    total_items: int
    planned_items: int
    pass_items: int
    review_required_items: int
    error_items: int
    warnings: list[str]
    items: list[HistoricalLogReviewItem]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan a manifest-driven historical log review across lifecycle completeness and log structure")
    parser.add_argument("manifest_path", help="Path to a historical-log-review manifest JSON file")
    parser.add_argument("--plan-path", dest="plan_path", help="Override output plan JSON path")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument(
        "--skip-live",
        dest="skip_live",
        action="store_true",
        help="Do not query live GitHub issue/PR state; classify from source-log links only",
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
        raise SystemExit(f"Failed to parse historical log review manifest JSON: {exc}") from exc


def _parse_issue_number(url: str | None) -> int | None:
    if not url:
        return None
    match = ISSUE_URL_RE.search(url.strip())
    return int(match.group(1)) if match else None


def _parse_pr_number(value: str | None) -> int | None:
    if not value:
        return None
    match = PR_URL_RE.search(value.strip())
    return int(match.group(1)) if match else None


def _first_section_name(sections: dict[str, list[str]], prefix: str) -> str | None:
    for name in sections:
        if name.startswith(prefix):
            return name
    return None


def _contains_placeholders(text: str) -> bool:
    lowered = text.lower()
    return "<placeholder>" in lowered or "todo" in lowered or "tbd" in lowered


def _execution_checklist_has_unchecked_items(section_lines: list[str]) -> bool:
    return any(raw.strip().startswith("- [ ]") for raw in section_lines)


def _extract_footer_source_lines(section_lines: list[str]) -> list[str]:
    collecting = False
    rows: list[str] = []
    for raw in section_lines:
        stripped = raw.strip()
        if stripped == "**Evidence Footer Source**:":
            collecting = True
            continue
        if not collecting:
            continue
        if not stripped:
            if rows:
                break
            continue
        if stripped.startswith("**") and stripped.endswith(":"):
            break
        if not stripped.startswith("- "):
            if rows:
                break
            continue
        rows.append(stripped[2:].strip())
    return rows


def _validate_evidence_footer_source_lines(lines: list[str]) -> tuple[bool, list[str]]:
    invalid = [line for line in lines if not EVIDENCE_FOOTER_LINE_RE.fullmatch(line)]
    return not invalid, invalid


def _validate_log_structure(log_text: str, fields: dict[str, str], sections: dict[str, list[str]]) -> tuple[str, list[ReviewCheck], list[str]]:
    checks: list[ReviewCheck] = []
    warnings: list[str] = []

    missing_fields = [name for name in REQUIRED_FIELD_NAMES if not str(fields.get(name, "")).strip()]
    if missing_fields:
        checks.append(ReviewCheck("frontmatter-required-fields", "fail", f"missing required fields: {missing_fields}"))
    else:
        checks.append(ReviewCheck("frontmatter-required-fields", "pass", "required frontmatter fields are present"))

    missing_sections = [prefix for prefix in REQUIRED_SECTION_PREFIXES if _first_section_name(sections, prefix) is None]
    if missing_sections:
        checks.append(ReviewCheck("required-section-presence", "fail", f"missing required sections: {missing_sections}"))
    else:
        checks.append(ReviewCheck("required-section-presence", "pass", "required sections are present"))

    pr_summary_name = _first_section_name(sections, "PR Summary Inputs")
    if pr_summary_name is None:
        checks.append(ReviewCheck("pr-summary-inputs-presence", "fail", "PR Summary Inputs block is missing"))
    else:
        checks.append(ReviewCheck("pr-summary-inputs-presence", "pass", "PR Summary Inputs block is present"))

    try:
        footer_source_lines = _extract_footer_source_lines(sections.get(pr_summary_name or "", [])) if pr_summary_name else []
        source_ok, invalid_lines = _validate_evidence_footer_source_lines(footer_source_lines)
    except Exception as exc:
        footer_source_lines = []
        source_ok = False
        invalid_lines = [str(exc)]

    if not source_ok:
        checks.append(ReviewCheck("evidence-footer-source-shape", "fail", f"invalid Evidence Footer Source rows: {invalid_lines}"))
    else:
        details = "no Evidence Footer Source rows were provided" if not footer_source_lines else "Evidence Footer Source rows match canonical shape"
        checks.append(ReviewCheck("evidence-footer-source-shape", "pass", details))

    if _contains_placeholders(log_text):
        checks.append(ReviewCheck("placeholder-hygiene", "fail", "placeholder scaffolding is still present in the log"))
    else:
        checks.append(ReviewCheck("placeholder-hygiene", "pass", "no placeholder scaffolding detected"))

    execution_name = _first_section_name(sections, "Execution Checklist")
    log_status = str(fields.get("status") or "").strip().lower()
    if log_status == "stable" and execution_name and _execution_checklist_has_unchecked_items(sections[execution_name]):
        checks.append(ReviewCheck("stable-contradiction", "fail", "log is marked stable but execution checklist still has unchecked items"))
    else:
        checks.append(ReviewCheck("stable-contradiction", "pass", "stable status does not contradict the execution checklist"))

    structure_status = "pass" if all(check.status != "fail" for check in checks) else "fail"
    if structure_status == "fail":
        warnings.append("historical log review should fix structure drift before trusting this log as automation input")
    return structure_status, checks, warnings


def _read_json_command(command: list[str], error_context: str) -> tuple[dict | None, str | None]:
    result = _run_command(command)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown gh error"
        return None, f"{error_context}: {detail}"
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError as exc:
        return None, f"{error_context}: failed to parse JSON output ({exc})"


def _fetch_issue_state(repo: str, issue_number: int) -> tuple[dict | None, str | None]:
    return _read_json_command(
        ["gh", "issue", "view", str(issue_number), "--repo", repo, "--json", "number,url,title,state"],
        f"failed to view issue #{issue_number}",
    )


def _fetch_pr_state(repo: str, pr_number: int) -> tuple[dict | None, str | None]:
    return _read_json_command(
        ["gh", "pr", "view", str(pr_number), "--repo", repo, "--json", "number,url,title,state,isDraft,mergedAt"],
        f"failed to view PR #{pr_number}",
    )


def _classify_item(
    *,
    structure_status: str,
    issue_number: int | None,
    issue_url: str | None,
    issue_state: str | None,
    pr_number: int | None,
    pr_url: str | None,
    pr_state: str | None,
    pr_merged_at: str | None,
) -> tuple[str, str, str, str | None]:
    if issue_number is None and pr_number is None:
        return "log-only", "open-issue-flow", "review-required", "log has no linked issue or PR evidence yet"

    if issue_number is not None and pr_number is None:
        if issue_state == "OPEN":
            return "issue-open-no-pr", "complete-pr-create", "review-required", "issue exists but no PR is linked yet"
        return "issue-closed-no-pr", "manual-reconcile", "review-required", "issue is closed without linked PR evidence"

    if issue_number is None and pr_number is not None:
        if pr_state == "MERGED":
            return "pr-merged-no-issue", "backfill-issue-link", "review-required", "merged PR exists but issue linkage is missing"
        return "pr-open-no-issue", "manual-reconcile", "review-required", "PR exists but issue linkage is missing"

    if pr_state == "MERGED":
        if issue_state == "CLOSED":
            status = "pass-review" if structure_status == "pass" else "review-required"
            reason = None if structure_status == "pass" else "lifecycle is closed-loop, but log structure still drifts from the current contract"
            return "concluded", "none", status, reason
        return "merged-open", "run-issue-conclusion", "review-required", "merged PR exists but the issue is still open"

    if pr_state in {"OPEN", "DRAFT"}:
        return "pr-open", "await-merge-or-review", "review-required", "PR is still open, so the lifecycle is not yet concluded"

    return "pr-closed-unmerged", "manual-reconcile", "review-required", "linked PR is closed without merge evidence"


def _error_item(log_path: str, requested_id: str, detail: str) -> HistoricalLogReviewItem:
    return HistoricalLogReviewItem(
        requested_id=requested_id,
        source_log_path=log_path,
        log_status=None,
        issue_number=None,
        issue_url=None,
        issue_state=None,
        pr_number=None,
        pr_url=None,
        pr_state=None,
        pr_merged_at=None,
        lifecycle_stage="error",
        structure_status="fail",
        planned_action="manual-reconcile",
        status="error",
        checks=[ReviewCheck("item-load", "fail", detail)],
        warnings=[],
        reason=detail,
    )


def _build_item(item: dict, defaults: dict, repo_root: Path, repo: str | None, skip_live: bool) -> HistoricalLogReviewItem:
    if not isinstance(item, dict):
        raise ValueError("each manifest item must be an object")

    raw_log_path = str(item.get("log_path") or "").strip()
    if not raw_log_path:
        raise ValueError("manifest item is missing log_path")

    resolved_log_path = _coerce_path(raw_log_path, repo_root)
    if not resolved_log_path.is_file():
        raise ValueError(f"log file not found: {resolved_log_path}")

    log_text = _load_text(resolved_log_path)
    fields = _parse_fields(log_text)
    sections = _parse_sections(log_text)
    requested_id = str(fields.get("id") or item.get("requested_id") or resolved_log_path.stem).strip()
    source_log_path = _repo_rel(resolved_log_path)
    log_status = str(fields.get("status") or "").strip() or None
    issue_url = str(fields.get("issue") or "").strip() or None
    pr_url = str(fields.get("pr") or "").strip() or None
    issue_number = _parse_issue_number(issue_url)
    pr_number = _parse_pr_number(pr_url)

    structure_status, checks, warnings = _validate_log_structure(log_text, fields, sections)

    issue_state: str | None = None
    pr_state: str | None = None
    pr_merged_at: str | None = None

    if not skip_live and repo and issue_number is not None:
        issue_payload, issue_error = _fetch_issue_state(repo, issue_number)
        if issue_error:
            checks.append(ReviewCheck("live-issue-read", "fail", issue_error))
        elif isinstance(issue_payload, dict):
            issue_state = str(issue_payload.get("state") or "").strip() or None
            issue_url = str(issue_payload.get("url") or issue_url or "").strip() or issue_url
            checks.append(ReviewCheck("live-issue-read", "pass", f"live issue state captured as {issue_state}"))

    if not skip_live and repo and pr_number is not None:
        pr_payload, pr_error = _fetch_pr_state(repo, pr_number)
        if pr_error:
            checks.append(ReviewCheck("live-pr-read", "fail", pr_error))
        elif isinstance(pr_payload, dict):
            merged_at = str(pr_payload.get("mergedAt") or "").strip()
            state = str(pr_payload.get("state") or "").strip()
            is_draft = bool(pr_payload.get("isDraft"))
            pr_state = "DRAFT" if state == "OPEN" and is_draft else state or None
            pr_merged_at = merged_at or None
            pr_url = str(pr_payload.get("url") or pr_url or "").strip() or pr_url
            checks.append(ReviewCheck("live-pr-read", "pass", f"live PR state captured as {pr_state or 'unknown'}"))

    if skip_live:
        warnings.append("live GitHub reads were skipped; lifecycle stage is classified from source-log links only")

    lifecycle_stage, planned_action, item_status, reason = _classify_item(
        structure_status=structure_status,
        issue_number=issue_number,
        issue_url=issue_url,
        issue_state=issue_state,
        pr_number=pr_number,
        pr_url=pr_url,
        pr_state=pr_state,
        pr_merged_at=pr_merged_at,
    )

    return HistoricalLogReviewItem(
        requested_id=requested_id,
        source_log_path=source_log_path,
        log_status=log_status,
        issue_number=issue_number,
        issue_url=issue_url,
        issue_state=issue_state,
        pr_number=pr_number,
        pr_url=pr_url,
        pr_state=pr_state,
        pr_merged_at=pr_merged_at,
        lifecycle_stage=lifecycle_stage,
        structure_status=structure_status,
        planned_action=planned_action,
        status=item_status,
        checks=checks,
        warnings=warnings,
        reason=reason,
    )


def plan_historical_log_review(args: argparse.Namespace) -> HistoricalLogReviewResult:
    repo_root = _repo_root()
    manifest_path = _coerce_path(args.manifest_path, repo_root)
    if not manifest_path.is_file():
        raise SystemExit(f"Historical log review manifest file not found: {manifest_path}")

    manifest = _load_manifest(manifest_path)
    defaults = manifest.get("defaults") if isinstance(manifest.get("defaults"), dict) else {}
    items = manifest.get("items") or []
    if not isinstance(items, list) or not items:
        raise SystemExit("Historical log review manifest must contain at least one item")

    skip_live = bool(args.skip_live or defaults.get("skip_live"))
    repo: str | None = None
    if not skip_live:
        _require_gh_cli()
        _require_gh_auth()
        repo = _derive_repo_slug(args.repo or str(defaults.get("repo") or "") or None)

    result_items: list[HistoricalLogReviewItem] = []
    warnings: list[str] = []
    for raw_item in items:
        try:
            result_items.append(_build_item(raw_item, defaults, repo_root, repo, skip_live))
        except Exception as exc:
            raw_log_path = str(raw_item.get("log_path") if isinstance(raw_item, dict) else "")
            requested_id = str(raw_item.get("requested_id") if isinstance(raw_item, dict) else "") or Path(raw_log_path or "unknown").stem
            result_items.append(_error_item(raw_log_path or "<missing-log-path>", requested_id, str(exc)))

    pass_items = sum(1 for item in result_items if item.status == "pass-review")
    review_required_items = sum(1 for item in result_items if item.status == "review-required")
    error_items = sum(1 for item in result_items if item.status == "error")
    planned_items = sum(1 for item in result_items if item.planned_action != "none")

    if error_items:
        overall_result = "error"
    elif review_required_items:
        overall_result = "review-required"
    else:
        overall_result = "pass"

    selection_filters = manifest.get("selection_filters")
    selection_input = json.dumps(selection_filters, ensure_ascii=True, sort_keys=True) if isinstance(selection_filters, dict) else "explicit manifest items"
    if skip_live:
        warnings.append("plan was generated without live GitHub reads")

    return HistoricalLogReviewResult(
        mode="historical-log-review-plan",
        result=overall_result,
        manifest_path=_repo_rel(manifest_path),
        selection_input=selection_input,
        operation="historical-log-review",
        repository=repo,
        total_items=len(result_items),
        planned_items=planned_items,
        pass_items=pass_items,
        review_required_items=review_required_items,
        error_items=error_items,
        warnings=warnings,
        items=result_items,
    )


def main() -> None:
    args = _parse_args()
    plan = plan_historical_log_review(args)

    repo_root = _repo_root()
    manifest_path = _coerce_path(args.manifest_path, repo_root)
    default_plan_path = manifest_path.with_name(f"{manifest_path.stem.removesuffix('-manifest')}-plan.json")
    plan_path = _coerce_path(args.plan_path, repo_root) if args.plan_path else default_plan_path
    plan_path.write_text(json.dumps(asdict(plan), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    print(json.dumps(asdict(plan), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()