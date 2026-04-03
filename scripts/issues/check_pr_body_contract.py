from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from body_contract import render_checks_payload, validate_pr_body_contract
from gen_issue_draft import _load_text, _parse_fields, _repo_rel, _repo_root


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a PR body markdown file against the canonical PR body contract")
    parser.add_argument("source_log_path", help="Path to the source log markdown file")
    parser.add_argument("body_path", help="Path to the PR body markdown file")
    parser.add_argument("--result-path", dest="result_path", help="Override output path for the validation JSON")
    return parser.parse_args()


def _coerce_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (_repo_root() / path).resolve()


def main() -> int:
    args = _parse_args()
    source_log_path = _coerce_path(args.source_log_path)
    body_path = _coerce_path(args.body_path)
    if not source_log_path.is_file():
        raise SystemExit(f"Source log not found: {source_log_path}")
    if not body_path.is_file():
        raise SystemExit(f"PR body file not found: {body_path}")

    source_log_text = _load_text(source_log_path)
    fields = _parse_fields(source_log_text)
    result = validate_pr_body_contract(
        body_markdown=_load_text(body_path),
        source_log_text=source_log_text,
        pr_development_issue=fields.get("pr_development_issue", "").strip() or fields.get("issue", "").strip() or None,
    )
    payload = {
        "mode": "pr-body-contract-check",
        "result": result.status,
        "source_log_path": _repo_rel(source_log_path),
        "body_path": _repo_rel(body_path),
        **render_checks_payload(result),
    }

    if args.result_path:
        result_path = _coerce_path(args.result_path)
    else:
        result_path = body_path.with_name(f"{body_path.stem}-contract-check.json")
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0 if result.status == "pass" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit as exc:
        if isinstance(exc.code, int):
            raise
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)