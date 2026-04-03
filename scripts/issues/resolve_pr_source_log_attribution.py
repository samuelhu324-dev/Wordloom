from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import (
    _derive_repo_slug,
    _parse_fields,
    _parse_sections,
    _repo_rel,
    _repo_root,
    _require_gh_auth,
    _require_gh_cli,
    _run_command,
)


LOG_ROW_RE = re.compile(r"^- Log:\s+`(?P<path>[^`]+)`\s*$")
WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:[\\/]")
ID_SEGMENT_RE = re.compile(r"^s\d+[a-z0-9-]*$")

RESULT_BY_STOP_REASON = {
    "missing-attribution": "stop-missing-attribution",
    "conflicting-attribution": "stop-conflicting-attribution",
    "multi-candidate-attribution": "stop-multi-candidate-attribution",
    "invalid-attribution-shape": "stop-invalid-attribution-shape",
}

SURFACE_PRECEDENCE = [
    "explicit-provenance",
    "pr-body-log-row",
    "exact-id-branch-fallback",
]


@dataclass
class SurfaceInspection:
    surface: str
    status: str
    value: str | None
    details: str
    candidates: list[str]


@dataclass
class AttributionPayload:
    mode: str
    result: str
    repository: str
    pr_ref: str
    pr_url: str
    source_log_path: str
    winning_surface: str
    consulted_surfaces: list[str]
    stop_reason: str
    eligible_for_secondary_enforcement: bool
    pr_payload_path: str
    surface_details: list[SurfaceInspection]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve PR source-log attribution and emit the 4E/P3 handoff payload")
    parser.add_argument("pr_ref", nargs="?", help="PR number or URL")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument(
        "--trusted-source-log-path",
        dest="trusted_source_log_path",
        help="Trusted explicit provenance carrying an exact repo-relative source_log_path",
    )
    parser.add_argument(
        "--pr-payload-path",
        dest="pr_payload_path",
        help="Use a local PR payload JSON file instead of fetching a live PR via gh",
    )
    parser.add_argument("--result-path", dest="result_path", help="Override output path for the attribution result JSON")
    parser.add_argument(
        "--snapshot-path",
        dest="snapshot_path",
        help="Override output path for the normalized PR payload snapshot JSON",
    )
    return parser.parse_args()


def _coerce_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (_repo_root() / path).resolve()


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse JSON from {path}: {exc}") from exc


def _fetch_pr(repo: str, pr_ref: str) -> dict:
    cmd = _run_command(
        [
            "gh",
            "pr",
            "view",
            pr_ref,
            "--repo",
            repo,
            "--json",
            "number,url,title,body,headRefName",
        ]
    )
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to view PR {pr_ref} in {repo}: {cmd.stderr.strip()}")
    try:
        return json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse PR view JSON: {exc}") from exc


def _normalize_pr_payload(raw: dict, fallback_pr_ref: str) -> dict:
    number = raw.get("number")
    pr_url = str(raw.get("url") or raw.get("pr_url") or "").strip()
    pr_ref = str(raw.get("pr_ref") or "").strip()
    if not pr_ref:
        if number not in {None, ""}:
            pr_ref = str(number)
        elif pr_url:
            pr_ref = pr_url
        else:
            pr_ref = fallback_pr_ref

    body = str(raw.get("body") or "")
    title = str(raw.get("title") or "")
    head_ref_name = str(raw.get("headRefName") or raw.get("head_ref_name") or raw.get("head_ref") or "")

    return {
        "pr_ref": pr_ref,
        "number": int(number) if isinstance(number, int) or str(number).isdigit() else None,
        "url": pr_url,
        "title": title,
        "body": body,
        "headRefName": head_ref_name,
        "trusted_source_log_path": str(raw.get("trusted_source_log_path") or "").strip(),
    }


def _default_result_path(pr_ref: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", pr_ref).strip("-") or "pr"
    return _repo_root() / "docs" / "issues" / f"pr-source-log-attribution-{safe}-result.json"


def _default_snapshot_path(result_path: Path) -> Path:
    stem = result_path.stem.removesuffix("-result")
    return result_path.with_name(f"{stem}-pr-payload.json")


def _canonical_repo_rel_path(value: str) -> str | None:
    raw = value.strip()
    if not raw or "\\" in raw or raw.startswith("/") or WINDOWS_DRIVE_RE.match(raw):
        return None

    repo_root = _repo_root()
    resolved = (repo_root / raw).resolve()
    try:
        canonical = resolved.relative_to(repo_root).as_posix()
    except ValueError:
        return None
    if canonical != raw or not resolved.is_file():
        return None
    return canonical


def _inspect_explicit_provenance(raw_value: str | None) -> SurfaceInspection:
    if not raw_value or not raw_value.strip():
        return SurfaceInspection(
            surface="explicit-provenance",
            status="absent",
            value=None,
            details="trusted explicit provenance was not supplied",
            candidates=[],
        )

    canonical = _canonical_repo_rel_path(raw_value)
    if not canonical:
        return SurfaceInspection(
            surface="explicit-provenance",
            status="invalid",
            value=None,
            details="trusted explicit provenance was supplied but was not one exact existing repo-relative log path",
            candidates=[],
        )

    return SurfaceInspection(
        surface="explicit-provenance",
        status="candidate",
        value=canonical,
        details="trusted explicit provenance supplied one exact repo-relative source_log_path",
        candidates=[canonical],
    )


def _inspect_pr_body_log_row(body_markdown: str) -> SurfaceInspection:
    sections = _parse_sections(body_markdown)
    link_lines = [line.strip() for line in sections.get("Links", []) if line.strip().startswith("- ")]
    log_rows = [line for line in link_lines if line.startswith("- Log:")]

    if not log_rows:
        return SurfaceInspection(
            surface="pr-body-log-row",
            status="absent",
            value=None,
            details="PR body Links section did not contain a Log row",
            candidates=[],
        )

    if len(log_rows) != 1:
        return SurfaceInspection(
            surface="pr-body-log-row",
            status="invalid",
            value=None,
            details="PR body Links section contained multiple Log rows instead of one canonical ownership row",
            candidates=[],
        )

    match = LOG_ROW_RE.match(log_rows[0])
    if not match:
        return SurfaceInspection(
            surface="pr-body-log-row",
            status="invalid",
            value=None,
            details="PR body Log row did not match the canonical line shape",
            candidates=[],
        )

    canonical = _canonical_repo_rel_path(match.group("path"))
    if not canonical:
        return SurfaceInspection(
            surface="pr-body-log-row",
            status="invalid",
            value=None,
            details="PR body Log row was present but did not carry one exact existing repo-relative log path",
            candidates=[],
        )

    return SurfaceInspection(
        surface="pr-body-log-row",
        status="candidate",
        value=canonical,
        details="PR body Log row carried one exact repo-relative source_log_path",
        candidates=[canonical],
    )


def _build_log_index() -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    logs_dir = _repo_root() / "docs" / "logs"
    for path in sorted(logs_dir.glob("log-*.md")):
        fields = _parse_fields(path.read_text(encoding="utf-8"))
        log_id = str(fields.get("id") or "").strip()
        if not log_id:
            continue
        index.setdefault(log_id.lower(), []).append(_repo_rel(path))
    return index


def _extract_branch_exact_id(head_ref_name: str) -> tuple[str | None, str | None]:
    tokens = [token.strip().lower() for token in head_ref_name.split("/") if token.strip()]
    id_tokens = [token for token in tokens if ID_SEGMENT_RE.fullmatch(token)]
    unique = sorted(set(id_tokens))
    if not unique:
        return None, None
    if len(unique) > 1:
        return None, "branch head ref contained more than one exact-ID token"
    return unique[0], None


def _inspect_exact_id_branch_fallback(head_ref_name: str, log_index: dict[str, list[str]]) -> SurfaceInspection:
    if not head_ref_name.strip():
        return SurfaceInspection(
            surface="exact-id-branch-fallback",
            status="absent",
            value=None,
            details="PR head ref was blank so exact-ID branch fallback was unavailable",
            candidates=[],
        )

    exact_id, extraction_error = _extract_branch_exact_id(head_ref_name)
    if extraction_error:
        return SurfaceInspection(
            surface="exact-id-branch-fallback",
            status="invalid",
            value=None,
            details=extraction_error,
            candidates=[],
        )

    if not exact_id:
        return SurfaceInspection(
            surface="exact-id-branch-fallback",
            status="absent",
            value=None,
            details="PR head ref did not expose one exact-ID token for branch fallback",
            candidates=[],
        )

    candidates = log_index.get(exact_id, [])
    if not candidates:
        return SurfaceInspection(
            surface="exact-id-branch-fallback",
            status="absent",
            value=None,
            details="PR head ref exposed one exact-ID token but no source log matched that exact ID",
            candidates=[],
        )

    if len(candidates) > 1:
        return SurfaceInspection(
            surface="exact-id-branch-fallback",
            status="multi-candidate",
            value=None,
            details="PR head ref exact-ID fallback matched more than one source log",
            candidates=candidates,
        )

    return SurfaceInspection(
        surface="exact-id-branch-fallback",
        status="candidate",
        value=candidates[0],
        details="PR head ref exact-ID fallback resolved to one source log",
        candidates=candidates,
    )


def _select_winning_surface(surface_details: list[SurfaceInspection]) -> tuple[str, str]:
    candidate_map = {detail.surface: detail.value for detail in surface_details if detail.status == "candidate" and detail.value}
    chosen_surface = ""
    chosen_value = ""
    for surface in SURFACE_PRECEDENCE:
        value = candidate_map.get(surface)
        if value:
            chosen_surface = surface
            chosen_value = value
            break
    return chosen_surface, chosen_value


def resolve_pr_source_log_attribution(
    *,
    pr_ref: str,
    repo: str | None = None,
    trusted_source_log_path: str | None = None,
    pr_payload_path: Path | None = None,
    result_path: Path | None = None,
    snapshot_path: Path | None = None,
) -> dict:
    repo_slug = _derive_repo_slug(repo)

    if pr_payload_path is not None:
        if not pr_payload_path.is_file():
            raise SystemExit(f"PR payload file not found: {pr_payload_path}")
        raw_pr_payload = _load_json(pr_payload_path)
    else:
        _require_gh_cli()
        _require_gh_auth()
        raw_pr_payload = _fetch_pr(repo_slug, pr_ref)

    normalized_pr_payload = _normalize_pr_payload(raw_pr_payload, pr_ref)
    explicit_value = trusted_source_log_path or normalized_pr_payload.get("trusted_source_log_path") or None
    log_index = _build_log_index()

    surface_details = [
        _inspect_explicit_provenance(explicit_value),
        _inspect_pr_body_log_row(str(normalized_pr_payload.get("body") or "")),
        _inspect_exact_id_branch_fallback(str(normalized_pr_payload.get("headRefName") or ""), log_index),
    ]

    valid_values = {detail.value for detail in surface_details if detail.status == "candidate" and detail.value}
    invalid_present = any(detail.status == "invalid" for detail in surface_details)
    multi_present = any(detail.status == "multi-candidate" for detail in surface_details)

    if len(valid_values) > 1:
        stop_reason = "conflicting-attribution"
        result = RESULT_BY_STOP_REASON[stop_reason]
        winning_surface = ""
        source_log_path = ""
        eligible = False
    elif invalid_present:
        stop_reason = "invalid-attribution-shape"
        result = RESULT_BY_STOP_REASON[stop_reason]
        winning_surface = ""
        source_log_path = ""
        eligible = False
    elif multi_present:
        stop_reason = "multi-candidate-attribution"
        result = RESULT_BY_STOP_REASON[stop_reason]
        winning_surface = ""
        source_log_path = ""
        eligible = False
    elif len(valid_values) == 1:
        winning_surface, source_log_path = _select_winning_surface(surface_details)
        stop_reason = ""
        result = "resolved"
        eligible = True
    else:
        stop_reason = "missing-attribution"
        result = RESULT_BY_STOP_REASON[stop_reason]
        winning_surface = ""
        source_log_path = ""
        eligible = False

    effective_pr_ref = str(normalized_pr_payload.get("pr_ref") or pr_ref)
    if result_path is None:
        result_path = _default_result_path(effective_pr_ref)
    if snapshot_path is None:
        snapshot_path = _default_snapshot_path(result_path)

    result_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps(normalized_pr_payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    payload = AttributionPayload(
        mode="pr-source-log-attribution",
        result=result,
        repository=repo_slug,
        pr_ref=effective_pr_ref,
        pr_url=str(normalized_pr_payload.get("url") or ""),
        source_log_path=source_log_path,
        winning_surface=winning_surface,
        consulted_surfaces=[detail.surface for detail in surface_details],
        stop_reason=stop_reason,
        eligible_for_secondary_enforcement=eligible,
        pr_payload_path=_repo_rel(snapshot_path),
        surface_details=surface_details,
    )
    rendered = asdict(payload)
    rendered["result_path"] = _repo_rel(result_path)
    result_path.write_text(json.dumps(rendered, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return rendered


def main() -> int:
    args = _parse_args()
    if not args.pr_ref and not args.pr_payload_path:
        raise SystemExit("Either pr_ref or --pr-payload-path is required")

    payload = resolve_pr_source_log_attribution(
        pr_ref=args.pr_ref or "pr-payload",
        repo=args.repo,
        trusted_source_log_path=args.trusted_source_log_path,
        pr_payload_path=_coerce_path(args.pr_payload_path) if args.pr_payload_path else None,
        result_path=_coerce_path(args.result_path) if args.result_path else None,
        snapshot_path=_coerce_path(args.snapshot_path) if args.snapshot_path else None,
    )
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0 if payload["result"] == "resolved" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit as exc:
        if isinstance(exc.code, int):
            raise
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)