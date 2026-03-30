from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _derive_repo_slug, _repo_root, _require_gh_auth, _require_gh_cli, _run_command


@dataclass
class IssueConclusionApplyResult:
    mode: str
    result: str
    plan_path: str
    item_index: int
    requested_id: str
    source_log_path: str
    repository: str
    issue_number: int
    issue_url: str
    issue_title: str
    previous_issue_state: str | None
    final_issue_state: str | None
    body_path: str
    close_reason: str | None
    warnings: list[str]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply a real issue-conclusion write-back from an issue-conclusion dry-run plan")
    parser.add_argument("plan_path", help="Path to an issue-conclusion plan JSON file")
    parser.add_argument("--item-index", dest="item_index", type=int, default=0, help="Plan item index to apply")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--leave-open", dest="leave_open", action="store_true", help="Update the issue body but do not close an open issue")
    parser.add_argument("--result-path", dest="result_path", help="Override output result JSON path")
    parser.add_argument("--body-path", dest="body_path", help="Override output applied body markdown path")
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _repo_rel(path: Path) -> str:
    return path.relative_to(_repo_root()).as_posix()


def _load_plan(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse issue-conclusion plan JSON: {exc}") from exc


def _fetch_issue_state(repo: str, issue_ref: str) -> dict:
    cmd = _run_command([
        "gh",
        "issue",
        "view",
        issue_ref,
        "--repo",
        repo,
        "--json",
        "number,url,title,state,body",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to view issue {issue_ref} in {repo}: {cmd.stderr.strip()}")
    try:
        return json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse issue view JSON: {exc}") from exc


def _edit_issue_body(repo: str, issue_ref: str, body_path: Path) -> None:
    cmd = _run_command([
        "gh",
        "issue",
        "edit",
        issue_ref,
        "--repo",
        repo,
        "--body-file",
        str(body_path),
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"gh issue edit failed: {cmd.stderr.strip()}")


def _close_issue(repo: str, issue_ref: str, reason: str) -> None:
    cmd = _run_command([
        "gh",
        "issue",
        "close",
        issue_ref,
        "--repo",
        repo,
        "--reason",
        reason,
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"gh issue close failed: {cmd.stderr.strip()}")


def apply_issue_conclusion_from_plan(args: argparse.Namespace) -> IssueConclusionApplyResult:
    repo_root = _repo_root()
    plan_path = _coerce_path(args.plan_path, repo_root)
    if not plan_path.is_file():
        raise SystemExit(f"Issue-conclusion plan file not found: {plan_path}")

    plan = _load_plan(plan_path)
    items = plan.get("items") or []
    if args.item_index < 0 or args.item_index >= len(items):
        raise SystemExit(f"Plan item index out of range: {args.item_index}")

    item = items[args.item_index]
    if item.get("status") != "planned":
        raise SystemExit(f"Selected plan item is not in planned state: {item.get('status')}")

    issue_number = item.get("issue_number")
    issue_url = item.get("issue_url")
    if not issue_number or not issue_url:
        raise SystemExit("Selected plan item is missing issue_number or issue_url")

    preview_body_path = _coerce_path(item["preview_body_path"], repo_root)
    if not preview_body_path.is_file():
        raise SystemExit(f"Issue-conclusion preview body file not found: {preview_body_path}")

    repo = _derive_repo_slug(args.repo)
    _require_gh_cli()
    _require_gh_auth()

    plan_slug = plan_path.stem.removesuffix("-plan")
    requested_id = str(item.get("requested_id") or f"item-{args.item_index}")
    default_body_path = plan_path.with_name(f"{plan_slug}-{requested_id.lower()}-apply-body.md")
    default_result_path = plan_path.with_name(f"{plan_slug}-{requested_id.lower()}-apply-result.json")
    body_path = _coerce_path(args.body_path, repo_root) if args.body_path else default_body_path
    result_path = _coerce_path(args.result_path, repo_root) if args.result_path else default_result_path
    body_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.parent.mkdir(parents=True, exist_ok=True)

    body_text = preview_body_path.read_text(encoding="utf-8")
    body_path.write_text(body_text, encoding="utf-8")

    before = _fetch_issue_state(repo, str(issue_number))
    previous_state = str(before.get("state") or "")
    warnings: list[str] = []

    _edit_issue_body(repo, str(issue_number), body_path)

    close_reason: str | None = None
    if previous_state != "CLOSED":
        if args.leave_open:
            warnings.append("issue remained open because --leave-open was requested")
        else:
            close_reason = "completed"
            _close_issue(repo, str(issue_number), close_reason)
            warnings.append("issue was open before apply; body updated and issue closed with reason=completed")
    else:
        warnings.append("issue was already closed before apply; body updated in place")

    after = _fetch_issue_state(repo, str(issue_number))
    result = IssueConclusionApplyResult(
        mode="issue-conclusion-apply",
        result="ok",
        plan_path=_repo_rel(plan_path),
        item_index=args.item_index,
        requested_id=requested_id,
        source_log_path=str(item.get("source_log_path") or ""),
        repository=repo,
        issue_number=int(after["number"]),
        issue_url=str(after["url"]),
        issue_title=str(after.get("title") or ""),
        previous_issue_state=previous_state or None,
        final_issue_state=str(after.get("state") or "") or None,
        body_path=_repo_rel(body_path),
        close_reason=close_reason,
        warnings=warnings,
    )
    result_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        apply_issue_conclusion_from_plan(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())