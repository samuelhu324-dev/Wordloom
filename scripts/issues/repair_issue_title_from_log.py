from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _derive_issue_title, _derive_repo_slug, _parse_fields, _parse_sections, _repo_root, _run_command
from raw_live_mutation_guard import add_raw_live_mutation_guard_arg, require_raw_live_mutation_guard


@dataclass
class IssueTitleRepairResult:
    mode: str
    result: str
    apply: bool
    repository: str
    log_path: str
    issue_number: int
    issue_url: str
    issue_state: str
    before_title: str
    expected_title: str
    final_title: str
    changed: bool
    warnings: list[str]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan or apply one canonical live issue title repair from a source log")
    parser.add_argument("log_path", help="Path to the source log that owns the canonical issue title")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--apply", dest="apply", action="store_true", help="Apply the live issue title repair")
    parser.add_argument("--result-path", dest="result_path", help="Override output result JSON path")
    add_raw_live_mutation_guard_arg(parser)
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _repo_rel(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def _parse_issue_number_from_url(url: str | None) -> int | None:
    if not url:
        return None
    marker = "/issues/"
    if marker not in url:
        return None
    return int(url.rsplit(marker, 1)[1])


def _fetch_issue_state(repo: str, issue_ref: str) -> dict:
    cmd = _run_command([
        "gh",
        "issue",
        "view",
        issue_ref,
        "--repo",
        repo,
        "--json",
        "number,url,title,state",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to view issue {issue_ref} in {repo}: {cmd.stderr.strip()}")
    try:
        return json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse issue view JSON: {exc}") from exc


def _edit_issue_title(repo: str, issue_ref: str, title: str) -> None:
    cmd = _run_command([
        "gh",
        "issue",
        "edit",
        issue_ref,
        "--repo",
        repo,
        "--title",
        title,
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"gh issue edit failed: {cmd.stderr.strip()}")


def repair_issue_title_from_log(args: argparse.Namespace) -> IssueTitleRepairResult:
    if args.apply:
        require_raw_live_mutation_guard(
            args,
            canonical_surface="scripts/issues/repair_issue_title_from_log.py --apply --allow-raw-live-mutation-internal",
        )

    repo_root = _repo_root()
    log_path = _coerce_path(args.log_path, repo_root)
    if not log_path.is_file():
        raise SystemExit(f"Log file not found: {log_path}")

    text = log_path.read_text(encoding="utf-8")
    fields = _parse_fields(text)
    sections = _parse_sections(text)
    issue_url = fields.get("issue", "").strip() or None
    issue_number = _parse_issue_number_from_url(issue_url)
    if issue_number is None:
        raise SystemExit(f"Source log has no live issue URL: {log_path}")

    log_id = fields.get("id", log_path.stem.removeprefix("log-"))
    log_title = fields.get("title", log_id)
    tags = [part.strip() for part in (fields.get("tags") or "").split(",") if part.strip()]
    expected_title, _ = _derive_issue_title(log_id, log_title, tags, sections, fields)

    repo = _derive_repo_slug(args.repo)
    issue_data = _fetch_issue_state(repo, str(issue_number))
    before_title = str(issue_data.get("title") or "")
    warnings: list[str] = []
    changed = False
    if before_title == expected_title:
        warnings.append("live issue title already matches the canonical source-log-owned title")
    elif args.apply:
        _edit_issue_title(repo, str(issue_number), expected_title)
        changed = True

    refreshed = _fetch_issue_state(repo, str(issue_number)) if args.apply else issue_data
    final_title = str(refreshed.get("title") or before_title)
    if args.apply and final_title != expected_title:
        raise SystemExit(
            f"live issue title did not converge to expected title; final='{final_title}', expected='{expected_title}'"
        )

    return IssueTitleRepairResult(
        mode="issue-title-repair",
        result="ok",
        apply=bool(args.apply),
        repository=repo,
        log_path=_repo_rel(log_path, repo_root),
        issue_number=int(refreshed.get("number") or issue_number),
        issue_url=str(refreshed.get("url") or issue_url or ""),
        issue_state=str(refreshed.get("state") or ""),
        before_title=before_title,
        expected_title=expected_title,
        final_title=final_title,
        changed=changed,
        warnings=warnings,
    )


def main() -> int:
    args = _parse_args()
    try:
        result = repair_issue_title_from_log(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2

    repo_root = _repo_root()
    output_path = Path(args.result_path) if args.result_path else repo_root / "artifacts" / f"issue-title-repair-{Path(args.log_path).stem.removeprefix('log-')}.json"
    if not output_path.is_absolute():
        output_path = repo_root / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())