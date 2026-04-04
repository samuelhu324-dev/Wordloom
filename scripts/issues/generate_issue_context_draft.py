from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _load_text, _repo_rel, _repo_root
from issue_context_llm import generate_issue_context_lines_with_llm


@dataclass
class IssueContextDraftResult:
    mode: str
    result: str
    context_mode: str
    log_path: str
    output_path: str
    phase: str
    merged_pr_numbers: list[int]
    context_lines: list[str]
    warnings: list[str]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one issue Context draft from a single structured log")
    parser.add_argument("log_path", help="Path to the source log markdown file")
    parser.add_argument("--output-path", dest="output_path", help="Override output markdown path")
    parser.add_argument("--result-path", dest="result_path", help="Override structured result JSON path")
    parser.add_argument(
        "--phase",
        dest="phase",
        choices=["conclusion"],
        default="conclusion",
        help="Render a conclusion-side Context block",
    )
    parser.add_argument(
        "--merged-pr",
        dest="merged_pr_numbers",
        type=int,
        action="append",
        default=[],
        help="Repeatable merged PR number used only for conclusion-phase Context drafts",
    )
    parser.add_argument(
        "--context-mode",
        dest="context_mode",
        choices=["llm-generate"],
        default="llm-generate",
        help="How to render one-item Context authoring output; llm-generate is the canonical mode",
    )
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def generate_issue_context_draft(args: argparse.Namespace) -> IssueContextDraftResult:
    repo_root = _repo_root()
    log_path = _coerce_path(args.log_path, repo_root)
    if not log_path.is_file():
        raise SystemExit(f"Issue Context source log not found: {log_path}")

    log_text = _load_text(log_path)
    phase = str(args.phase or "conclusion")
    merged_pr_numbers = [int(number) for number in args.merged_pr_numbers or []]
    context_lines = generate_issue_context_lines_with_llm(log_text, merged_pr_numbers)

    stem = log_path.stem.removeprefix("log-")
    default_output = repo_root / "docs" / "issues" / f"issue-context-{stem}-{phase}.md"
    output_path = _coerce_path(args.output_path, repo_root) if args.output_path else default_output
    result_path = _coerce_path(args.result_path, repo_root) if args.result_path else output_path.with_suffix(".json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.parent.mkdir(parents=True, exist_ok=True)

    markdown = "## Context\n\n" + "\n".join(context_lines) + "\n"
    output_path.write_text(markdown, encoding="utf-8")

    warnings = [
        "This script is the single-item conclusion Context authoring entrypoint; review the generated text before copying or applying it",
    ]
    warnings.append("Conclusion-phase Context generation is intended for one closed issue at a time after merged PR evidence is known")

    result = IssueContextDraftResult(
        mode="issue-context-draft",
        result="ok",
        context_mode=str(args.context_mode or "llm-generate"),
        log_path=_repo_rel(log_path),
        output_path=_repo_rel(output_path),
        phase=phase,
        merged_pr_numbers=merged_pr_numbers,
        context_lines=context_lines,
        warnings=warnings,
    )
    result_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        generate_issue_context_draft(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())