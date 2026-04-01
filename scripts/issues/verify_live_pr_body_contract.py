from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from body_contract import render_checks_payload, validate_pr_body_contract
from gen_issue_draft import _derive_repo_slug, _load_text, _parse_fields, _repo_rel, _repo_root, _require_gh_auth, _require_gh_cli, _run_command


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch a live PR body and validate it against the canonical PR body contract")
    parser.add_argument("source_log_path", help="Path to the source log markdown file")
    parser.add_argument("pr_ref", help="PR number or URL")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--live-body-path", dest="live_body_path", help="Override output path for the fetched live PR body")
    parser.add_argument("--result-path", dest="result_path", help="Override output path for the validation JSON")
    return parser.parse_args()


def _coerce_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (_repo_root() / path).resolve()


def _fetch_pr(repo: str, pr_ref: str) -> dict:
    cmd = _run_command([
        "gh",
        "pr",
        "view",
        pr_ref,
        "--repo",
        repo,
        "--json",
        "number,url,title,body,state",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to view PR {pr_ref} in {repo}: {cmd.stderr.strip()}")
    try:
        return json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse PR view JSON: {exc}") from exc


def run_live_pr_body_contract_check(
    *,
    source_log_path: Path,
    pr_ref: str,
    repo: str | None = None,
    live_body_path: Path | None = None,
    result_path: Path | None = None,
) -> dict:
    if not source_log_path.is_file():
        raise SystemExit(f"Source log not found: {source_log_path}")

    repo_slug = _derive_repo_slug(repo)
    _require_gh_cli()
    _require_gh_auth()
    pr_data = _fetch_pr(repo_slug, pr_ref)

    if live_body_path is None:
        live_body_path = _repo_root() / "docs" / "issues" / f"pr-live-contract-check-{int(pr_data['number'])}-body.md"
    live_body_path.parent.mkdir(parents=True, exist_ok=True)
    live_body_path.write_text(str(pr_data.get("body") or ""), encoding="utf-8")

    source_log_text = _load_text(source_log_path)
    fields = _parse_fields(source_log_text)
    result = validate_pr_body_contract(
        body_markdown=str(pr_data.get("body") or ""),
        source_log_text=source_log_text,
        pr_development_issue=fields.get("pr_development_issue", "").strip() or fields.get("issue", "").strip() or None,
    )
    payload = {
        "mode": "live-pr-body-contract-check",
        "result": result.status,
        "repository": repo_slug,
        "source_log_path": _repo_rel(source_log_path),
        "pr_number": int(pr_data["number"]),
        "pr_url": str(pr_data.get("url") or ""),
        "pr_title": str(pr_data.get("title") or ""),
        "pr_state": str(pr_data.get("state") or ""),
        "live_body_path": _repo_rel(live_body_path),
        **render_checks_payload(result),
    }

    if result_path is None:
        result_path = live_body_path.with_name(f"pr-live-contract-check-{int(pr_data['number'])}-result.json")
    result_path.parent.mkdir(parents=True, exist_ok=True)
    payload["result_path"] = _repo_rel(result_path)
    result_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    args = _parse_args()
    payload = run_live_pr_body_contract_check(
        source_log_path=_coerce_path(args.source_log_path),
        pr_ref=args.pr_ref,
        repo=args.repo,
        live_body_path=_coerce_path(args.live_body_path) if args.live_body_path else None,
        result_path=_coerce_path(args.result_path) if args.result_path else None,
    )
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0 if payload["result"] == "pass" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit as exc:
        if isinstance(exc.code, int):
            raise
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)