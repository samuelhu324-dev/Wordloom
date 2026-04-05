from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from body_contract import issue_uses_parent_body_contract, ordered_parent_child_issue_refs
from gen_issue_draft import _allowed_issue_keywords, _derive_issue_title, _derive_repo_slug, _parse_fields, _parse_sections, _repo_root, _run_command


ISSUE_URL_RE = re.compile(r"/issues/(\d+)$")
FETCH_PARENT_ISSUE_QUERY = (
    "query($owner:String!,$repo:String!,$number:Int!){"
    "repository(owner:$owner,name:$repo){"
    "issue(number:$number){"
    "number url title state subIssues(first:100){nodes{number url title}}"
    "}"
    "}"
    "}"
)


@dataclass
class LegacyTitleKeywordItem:
    log_path: str
    log_id: str
    issue_number: int
    issue_url: str
    issue_state: str
    live_issue_title: str
    issue_keyword: str
    allowed_issue_keywords: list[str]
    expected_live_title_under_current_log_state: str
    live_title_matches_current_log_state: bool
    migration_status: str
    reason: str


@dataclass
class ParentOrderingItem:
    log_path: str
    log_id: str
    issue_number: int
    issue_url: str
    issue_title: str
    issue_state: str
    expected_subissue_numbers: list[int]
    actual_subissue_numbers: list[int]
    status: str
    canonical_repair_surface: str | None
    reason: str


@dataclass
class IdentityGovernanceInventoryResult:
    mode: str
    result: str
    repository: str
    generated_at: str
    scanned_logs: int
    legacy_title_keyword_item_count: int
    parent_ordering_item_count: int
    active_parent_ordering_drift_count: int
    warnings: list[str]
    legacy_title_keyword_items: list[LegacyTitleKeywordItem] = field(default_factory=list)
    parent_ordering_items: list[ParentOrderingItem] = field(default_factory=list)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory historical issue-identity governance drift from source logs and live GitHub issues")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--output-path", dest="output_path", help="Override output JSON path")
    parser.add_argument("--skip-legacy-title-keywords", dest="skip_legacy_title_keywords", action="store_true", help="Skip inventorying historical legacy issue_keyword items")
    parser.add_argument("--skip-parent-ordering", dest="skip_parent_ordering", action="store_true", help="Skip inventorying top-level parent sub-issue ordering state")
    return parser.parse_args()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _repo_rel(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def _parse_issue_number_from_url(url: str | None) -> int | None:
    if not url:
        return None
    match = ISSUE_URL_RE.search(url.strip())
    return int(match.group(1)) if match else None


def _split_repo_slug(repo: str) -> tuple[str, str]:
    owner, name = repo.split("/", 1)
    return owner, name


def _run_graphql(query: str, variables: dict[str, str | int | None]) -> dict:
    command = ["gh", "api", "graphql", "-f", f"query={query}"]
    for name, value in variables.items():
        if value is None:
            continue
        command.extend(["-F", f"{name}={value}"])
    cmd = _run_command(command)
    if cmd.returncode != 0:
        raise SystemExit(f"GitHub GraphQL call failed: {cmd.stderr.strip()}")
    try:
        payload = json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse GraphQL JSON: {exc}") from exc
    if payload.get("errors"):
        raise SystemExit(f"GraphQL returned errors: {json.dumps(payload['errors'], ensure_ascii=True)}")
    return payload.get("data") or {}


def _fetch_issue_state(repo: str, issue_number: int) -> dict:
    cmd = _run_command([
        "gh",
        "issue",
        "view",
        str(issue_number),
        "--repo",
        repo,
        "--json",
        "number,url,title,state",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to view issue #{issue_number} in {repo}: {cmd.stderr.strip()}")
    try:
        return json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse issue view JSON: {exc}") from exc


def _fetch_parent_issue(repo: str, issue_number: int) -> dict:
    owner, repo_name = _split_repo_slug(repo)
    data = _run_graphql(
        FETCH_PARENT_ISSUE_QUERY,
        {"owner": owner, "repo": repo_name, "number": issue_number},
    )
    issue = (((data.get("repository") or {}).get("issue")) or None)
    if not issue:
        raise SystemExit(f"Issue not found in {repo}: #{issue_number}")
    return issue


def _iter_log_paths(repo_root: Path) -> list[Path]:
    return sorted(
        path
        for path in (repo_root / "docs" / "logs").glob("log-*.md")
        if path.is_file()
    )


def _build_legacy_title_keyword_item(repo_root: Path, log_path: Path, fields: dict[str, str], sections: dict[str, list[str]], repo: str) -> LegacyTitleKeywordItem | None:
    issue_url = fields.get("issue", "").strip() or None
    issue_number = _parse_issue_number_from_url(issue_url)
    issue_keyword = fields.get("issue_keyword", "").strip()
    if issue_number is None or not issue_keyword:
        return None

    allowed_issue_keywords = _allowed_issue_keywords(fields)
    if issue_keyword.strip().lower() in allowed_issue_keywords:
        return None

    issue_data = _fetch_issue_state(repo, issue_number)
    log_id = fields.get("id", log_path.stem.removeprefix("log-"))
    log_title = fields.get("title", log_id)
    tags = [part.strip() for part in (fields.get("tags") or "").split(",") if part.strip()]
    expected_live_title_under_current_log_state, _ = _derive_issue_title(log_id, log_title, tags, sections, fields)
    live_issue_title = str(issue_data.get("title") or "")
    return LegacyTitleKeywordItem(
        log_path=_repo_rel(log_path, repo_root),
        log_id=log_id,
        issue_number=issue_number,
        issue_url=str(issue_data.get("url") or issue_url or ""),
        issue_state=str(issue_data.get("state") or ""),
        live_issue_title=live_issue_title,
        issue_keyword=issue_keyword,
        allowed_issue_keywords=allowed_issue_keywords,
        expected_live_title_under_current_log_state=expected_live_title_under_current_log_state,
        live_title_matches_current_log_state=live_issue_title == expected_live_title_under_current_log_state,
        migration_status="legacy-source-keyword-drift",
        reason="source log still carries a historical issue_keyword outside the current controlled vocabulary, so future repair must migrate the source-owned keyword before any live title rewrite is considered",
    )


def _build_parent_ordering_item(repo_root: Path, log_path: Path, fields: dict[str, str], repo: str) -> ParentOrderingItem | None:
    if not issue_uses_parent_body_contract(fields):
        return None

    issue_url = fields.get("issue", "").strip() or None
    issue_number = _parse_issue_number_from_url(issue_url)
    if issue_number is None:
        return None

    expected_refs = ordered_parent_child_issue_refs(repo_root, fields)
    expected_numbers = [int(ref.removeprefix("#")) for ref in expected_refs]
    if not expected_numbers:
        return None

    live_issue = _fetch_parent_issue(repo, issue_number)
    actual_numbers = [
        int(node["number"])
        for node in (((live_issue.get("subIssues") or {}).get("nodes")) or [])
        if isinstance(node, dict) and node.get("number") is not None
    ]
    if actual_numbers == expected_numbers:
        status = "matches-canonical-order"
        reason = "live GitHub sub-issue sidebar order already matches the source-log-owned child ledger"
        canonical_repair_surface = None
    elif sorted(actual_numbers) == sorted(expected_numbers):
        status = "ordering-drift"
        reason = "live GitHub sub-issue set matches the canonical child set, but the sidebar order still diverges from the source-log-owned order"
        canonical_repair_surface = "scripts/issues/reprioritize_parent_subissues.py --apply --allow-raw-live-mutation-internal"
    else:
        status = "child-set-drift"
        reason = "live GitHub child issue set no longer matches the canonical source-log-owned child set, so reprioritize must not run until the relationship set is reconciled"
        canonical_repair_surface = None

    return ParentOrderingItem(
        log_path=_repo_rel(log_path, repo_root),
        log_id=fields.get("id", log_path.stem.removeprefix("log-")),
        issue_number=int(live_issue.get("number") or issue_number),
        issue_url=str(live_issue.get("url") or issue_url or ""),
        issue_title=str(live_issue.get("title") or ""),
        issue_state=str(live_issue.get("state") or ""),
        expected_subissue_numbers=expected_numbers,
        actual_subissue_numbers=actual_numbers,
        status=status,
        canonical_repair_surface=canonical_repair_surface,
        reason=reason,
    )


def inventory_issue_identity_governance_drift(args: argparse.Namespace) -> IdentityGovernanceInventoryResult:
    repo_root = _repo_root()
    repo = _derive_repo_slug(args.repo)
    log_paths = _iter_log_paths(repo_root)

    legacy_title_keyword_items: list[LegacyTitleKeywordItem] = []
    parent_ordering_items: list[ParentOrderingItem] = []
    warnings: list[str] = []

    for log_path in log_paths:
        text = log_path.read_text(encoding="utf-8")
        fields = _parse_fields(text)
        if fields.get("kind", "").strip() != "log":
            continue
        sections = _parse_sections(text)

        if not args.skip_legacy_title_keywords:
            legacy_item = _build_legacy_title_keyword_item(repo_root, log_path, fields, sections, repo)
            if legacy_item is not None:
                legacy_title_keyword_items.append(legacy_item)

        if not args.skip_parent_ordering:
            parent_item = _build_parent_ordering_item(repo_root, log_path, fields, repo)
            if parent_item is not None:
                parent_ordering_items.append(parent_item)

    active_parent_ordering_drift_count = sum(1 for item in parent_ordering_items if item.status != "matches-canonical-order")
    if args.skip_legacy_title_keywords:
        warnings.append("legacy title-keyword inventory skipped by request")
    elif not legacy_title_keyword_items:
        warnings.append("no historical live issues currently require legacy title-keyword migration inventory")
    if args.skip_parent_ordering:
        warnings.append("parent ordering inventory skipped by request")
    elif not parent_ordering_items:
        warnings.append("no top-level parent issues with canonical child ledgers were found for parent ordering inventory")

    return IdentityGovernanceInventoryResult(
        mode="issue-identity-governance-inventory",
        result="ok",
        repository=repo,
        generated_at=_utc_now(),
        scanned_logs=len(log_paths),
        legacy_title_keyword_item_count=len(legacy_title_keyword_items),
        parent_ordering_item_count=len(parent_ordering_items),
        active_parent_ordering_drift_count=active_parent_ordering_drift_count,
        warnings=warnings,
        legacy_title_keyword_items=legacy_title_keyword_items,
        parent_ordering_items=parent_ordering_items,
    )


def main() -> int:
    args = _parse_args()
    try:
        result = inventory_issue_identity_governance_drift(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2

    repo_root = _repo_root()
    output_path = Path(args.output_path) if args.output_path else repo_root / "artifacts" / "s0f-1g-p4-identity-governance-inventory.json"
    if not output_path.is_absolute():
        output_path = repo_root / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())