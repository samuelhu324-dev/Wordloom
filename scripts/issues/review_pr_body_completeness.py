from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from body_contract import validate_pr_body_contract
from gen_issue_draft import (
    _derive_repo_slug,
    _load_text,
    _parse_fields,
    _repo_rel,
    _repo_root,
    _require_gh_auth,
    _require_gh_cli,
    _run_command,
)
from rewrite_pr_body_scope_from_log import rewrite_pr_body_scope


PR_URL_RE = re.compile(r"/pull/(?P<number>\d+)(?:$|[/?#])")
PHASE_ID_RE = re.compile(r"^[A-Z0-9]+-\d+[A-Z0-9-]*$")


@dataclass
class ReviewItemResult:
    requested_id: str
    source_log_path: str
    pr_ref: str
    pr_url: str
    pr_title: str
    pr_state: str
    result: str
    details: str
    raw_match: bool
    normalized_match: bool
    live_body_path: str | None
    expected_body_path: str | None
    raw_diff_path: str | None
    normalized_diff_path: str | None
    contract_result: str | None
    contract_checks: list[dict]
    contract_warnings: list[str]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Review live PR body completeness by rebuilding expected bodies from source logs"
    )
    parser.add_argument(
        "--requested-id-prefix",
        dest="requested_id_prefixes",
        action="append",
        required=True,
        help="Review logs whose requested ID starts with this prefix, for example S0F-",
    )
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument(
        "--logs-dir",
        dest="logs_dir",
        help="Override logs directory; defaults to docs/logs under the repo root",
    )
    parser.add_argument(
        "--result-path",
        dest="result_path",
        help="Override output path for the review summary JSON",
    )
    parser.add_argument(
        "--artifact-dir",
        dest="artifact_dir",
        help="Override artifact directory for retained live/expected/diff files",
    )
    parser.add_argument(
        "--fail-on-findings",
        action="store_true",
        help="Exit non-zero when any item is not exact-match or formatting-only-drift",
    )
    return parser.parse_args()


def _coerce_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (_repo_root() / path).resolve()


def _safe_slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return cleaned or "review"


def _default_result_path(prefixes: list[str]) -> Path:
    joined = "-".join(_safe_slug(prefix.lower()) for prefix in prefixes)
    return _repo_root() / "artifacts" / f"pr-body-completeness-review-{joined}.json"


def _default_artifact_dir(result_path: Path) -> Path:
    stem = result_path.stem
    return result_path.with_name(f"{stem}-files")


def _extract_pr_ref(value: str) -> str | None:
    stripped = value.strip()
    if not stripped:
        return None
    if stripped.isdigit():
        return stripped
    match = PR_URL_RE.search(stripped)
    if match:
        return match.group("number")
    return stripped


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
            "number,url,title,body,state",
        ]
    )
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to view PR {pr_ref} in {repo}: {cmd.stderr.strip()}")
    try:
        return json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse PR view JSON for {pr_ref}: {exc}") from exc


def _iter_matching_logs(logs_dir: Path, prefixes: list[str]) -> list[Path]:
    matches: list[Path] = []
    normalized_prefixes = tuple(prefix.lower() for prefix in prefixes)
    for path in sorted(logs_dir.glob("log-*.md")):
        fields = _parse_fields(_load_text(path))
        requested_id = str(fields.get("id") or "").strip()
        if (
            requested_id
            and PHASE_ID_RE.fullmatch(requested_id)
            and requested_id.lower().startswith(normalized_prefixes)
        ):
            matches.append(path)
    return matches


def _normalize_body(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    normalized_lines = [line.rstrip() for line in lines]
    while normalized_lines and not normalized_lines[0].strip():
        normalized_lines.pop(0)
    while normalized_lines and not normalized_lines[-1].strip():
        normalized_lines.pop()

    collapsed: list[str] = []
    pending_blank = False
    for line in normalized_lines:
        if not line.strip():
            pending_blank = True
            continue
        if pending_blank and collapsed:
            collapsed.append("")
        collapsed.append(line)
        pending_blank = False

    if not collapsed:
        return ""
    return "\n".join(collapsed) + "\n"


def _render_diff(expected_text: str, live_text: str, *, fromfile: str, tofile: str) -> str:
    return "".join(
        difflib.unified_diff(
            expected_text.splitlines(keepends=True),
            live_text.splitlines(keepends=True),
            fromfile=fromfile,
            tofile=tofile,
        )
    )


def _write_optional_diff(path: Path, diff_text: str) -> str | None:
    if not diff_text:
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(diff_text, encoding="utf-8")
    return _repo_rel(path)


def _review_one_log(*, source_log_path: Path, repo_slug: str, artifact_dir: Path) -> ReviewItemResult:
    fields = _parse_fields(_load_text(source_log_path))
    requested_id = str(fields.get("id") or "").strip()
    pr_link = str(fields.get("pr") or "").strip()
    source_log_rel = _repo_rel(source_log_path)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    item_slug = _safe_slug(requested_id.lower())

    if not pr_link:
        return ReviewItemResult(
            requested_id=requested_id,
            source_log_path=source_log_rel,
            pr_ref="",
            pr_url="",
            pr_title="",
            pr_state="",
            result="stop-missing-pr-link",
            details="source log links.pr is blank, so the reviewer cannot resolve a canonical live PR to compare",
            raw_match=False,
            normalized_match=False,
            live_body_path=None,
            expected_body_path=None,
            raw_diff_path=None,
            normalized_diff_path=None,
            contract_result=None,
            contract_checks=[],
            contract_warnings=[],
        )

    pr_ref = _extract_pr_ref(pr_link)
    if not pr_ref:
        return ReviewItemResult(
            requested_id=requested_id,
            source_log_path=source_log_rel,
            pr_ref="",
            pr_url=pr_link,
            pr_title="",
            pr_state="",
            result="stop-invalid-pr-link",
            details="source log links.pr did not contain one exact PR reference or URL",
            raw_match=False,
            normalized_match=False,
            live_body_path=None,
            expected_body_path=None,
            raw_diff_path=None,
            normalized_diff_path=None,
            contract_result=None,
            contract_checks=[],
            contract_warnings=[],
        )

    pr_data = _fetch_pr(repo_slug, pr_ref)
    live_body_text = str(pr_data.get("body") or "")
    live_body_path = artifact_dir / f"{item_slug}-live-body.md"
    live_body_path.write_text(live_body_text, encoding="utf-8")

    expected_body_path = artifact_dir / f"{item_slug}-expected-body.md"
    rewrite_pr_body_scope(
        source_log_path=source_log_path,
        existing_body_path=live_body_path,
        requested_id=requested_id,
        pr_title=str(pr_data.get("title") or ""),
        output_path=expected_body_path,
    )
    expected_body_text = expected_body_path.read_text(encoding="utf-8")

    pr_development_issue = str(fields.get("pr_development_issue") or "").strip() or str(fields.get("issue") or "").strip() or None
    contract_result = validate_pr_body_contract(
        body_markdown=live_body_text,
        source_log_text=_load_text(source_log_path),
        pr_development_issue=pr_development_issue,
    )

    raw_match = live_body_text == expected_body_text
    normalized_live = _normalize_body(live_body_text)
    normalized_expected = _normalize_body(expected_body_text)
    normalized_match = normalized_live == normalized_expected

    if raw_match:
        result = "exact-match"
        details = "live PR body matched the source-log-derived expected body exactly"
    elif normalized_match:
        result = "formatting-only-drift"
        details = "live PR body drifted only by formatting noise after normalization"
    else:
        result = "substantive-drift"
        details = "live PR body differed from the source-log-derived expected body after normalization"

    raw_diff_path = _write_optional_diff(
        artifact_dir / f"{item_slug}-raw.diff",
        _render_diff(
            expected_body_text,
            live_body_text,
            fromfile=f"expected/{requested_id}",
            tofile=f"live/{requested_id}",
        ) if not raw_match else "",
    )
    normalized_diff_path = _write_optional_diff(
        artifact_dir / f"{item_slug}-normalized.diff",
        _render_diff(
            normalized_expected,
            normalized_live,
            fromfile=f"expected-normalized/{requested_id}",
            tofile=f"live-normalized/{requested_id}",
        ) if not normalized_match else "",
    )

    return ReviewItemResult(
        requested_id=requested_id,
        source_log_path=source_log_rel,
        pr_ref=str(pr_ref),
        pr_url=str(pr_data.get("url") or pr_link),
        pr_title=str(pr_data.get("title") or ""),
        pr_state=str(pr_data.get("state") or ""),
        result=result,
        details=details,
        raw_match=raw_match,
        normalized_match=normalized_match,
        live_body_path=_repo_rel(live_body_path),
        expected_body_path=_repo_rel(expected_body_path),
        raw_diff_path=raw_diff_path,
        normalized_diff_path=normalized_diff_path,
        contract_result=contract_result.status,
        contract_checks=[asdict(check) for check in contract_result.checks],
        contract_warnings=list(contract_result.warnings),
    )


def run_pr_body_completeness_review(
    *,
    requested_id_prefixes: list[str],
    repo: str | None = None,
    logs_dir: Path | None = None,
    result_path: Path | None = None,
    artifact_dir: Path | None = None,
) -> dict:
    repo_slug = _derive_repo_slug(repo)
    _require_gh_cli()
    _require_gh_auth()

    effective_logs_dir = logs_dir or (_repo_root() / "docs" / "logs")
    matching_logs = _iter_matching_logs(effective_logs_dir, requested_id_prefixes)
    if not matching_logs:
        raise SystemExit("No source logs matched the requested ID prefixes")

    effective_result_path = result_path or _default_result_path(requested_id_prefixes)
    effective_artifact_dir = artifact_dir or _default_artifact_dir(effective_result_path)

    items = [
        _review_one_log(source_log_path=source_log_path, repo_slug=repo_slug, artifact_dir=effective_artifact_dir)
        for source_log_path in matching_logs
    ]

    summary_counts: dict[str, int] = {}
    for item in items:
        summary_counts[item.result] = summary_counts.get(item.result, 0) + 1

    substantive_ids = [item.requested_id for item in items if item.result == "substantive-drift"]
    stop_ids = [item.requested_id for item in items if item.result.startswith("stop-")]
    formatting_only_ids = [item.requested_id for item in items if item.result == "formatting-only-drift"]
    exact_match_ids = [item.requested_id for item in items if item.result == "exact-match"]

    payload = {
        "mode": "pr-body-completeness-review",
        "repository": repo_slug,
        "requested_id_prefixes": requested_id_prefixes,
        "logs_dir": _repo_rel(effective_logs_dir),
        "result_path": _repo_rel(effective_result_path),
        "artifact_dir": _repo_rel(effective_artifact_dir),
        "summary": {
            "total_logs_reviewed": len(items),
            "counts_by_result": summary_counts,
            "exact_match_ids": exact_match_ids,
            "formatting_only_ids": formatting_only_ids,
            "substantive_drift_ids": substantive_ids,
            "stop_ids": stop_ids,
        },
        "items": [asdict(item) for item in items],
    }

    effective_result_path.parent.mkdir(parents=True, exist_ok=True)
    effective_result_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    args = _parse_args()
    payload = run_pr_body_completeness_review(
        requested_id_prefixes=args.requested_id_prefixes,
        repo=args.repo,
        logs_dir=_coerce_path(args.logs_dir) if args.logs_dir else None,
        result_path=_coerce_path(args.result_path) if args.result_path else None,
        artifact_dir=_coerce_path(args.artifact_dir) if args.artifact_dir else None,
    )
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    if args.fail_on_findings and (
        payload["summary"]["substantive_drift_ids"] or payload["summary"]["stop_ids"]
    ):
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit as exc:
        if isinstance(exc.code, int):
            raise
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
