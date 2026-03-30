from __future__ import annotations

import argparse
from pathlib import Path

from gen_issue_draft import _load_text, _parse_sections, _repo_rel, _repo_root
from plan_pr_prep import (
    _derive_scope_from_pr_title,
    _extract_checked_items,
    _extract_scoped_evidence_lines,
    _filter_checked_items,
    _find_section_lines,
    _matches_scope,
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rewrite PR body checklist/evidence sections from source-log scope")
    parser.add_argument("source_log_path", help="Path to the source log markdown file")
    parser.add_argument("existing_body_path", help="Path to the existing PR body markdown file")
    parser.add_argument("requested_id", help="Requested ID such as S0E-4C")
    parser.add_argument("pr_title", help="Final PR title whose scope should control checklist/evidence")
    parser.add_argument("--output-path", required=True, dest="output_path", help="Output path for the rewritten body")
    return parser.parse_args()


def _coerce_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (_repo_root() / path).resolve()


def _render_section(name: str, lines: list[str]) -> list[str]:
    cleaned_lines = list(lines)
    while cleaned_lines and not cleaned_lines[0].strip():
        cleaned_lines.pop(0)
    while cleaned_lines and not cleaned_lines[-1].strip():
        cleaned_lines.pop()
    return [f"## {name}", "", *cleaned_lines, ""]


def _extract_heading_evidence_lines(section_lines: list[str], scope_kind: str, scope_refs: list[str]) -> list[str]:
    lines: list[str] = []
    for raw in section_lines:
        stripped = raw.strip()
        if not stripped.startswith("### "):
            continue
        heading = stripped[4:].strip()
        if _matches_scope(heading, scope_kind, scope_refs):
            lines.append(heading)
    return lines


def rewrite_pr_body_scope(*, source_log_path: Path, existing_body_path: Path, requested_id: str, pr_title: str, output_path: Path) -> str:
    source_sections = _parse_sections(_load_text(source_log_path))
    body_sections = _parse_sections(_load_text(existing_body_path))

    scope_kind, scope_refs = _derive_scope_from_pr_title(pr_title, requested_id)

    checklist_items = _extract_checked_items(_find_section_lines(source_sections, "Execution Checklist"))
    filtered_checklist_items = _filter_checked_items(checklist_items, scope_kind, scope_refs)
    if checklist_items and not filtered_checklist_items:
        raise SystemExit("No checklist items matched the requested PR title scope")

    evidence_lines = _extract_scoped_evidence_lines(
        _find_section_lines(source_sections, "Evidence"),
        scope_kind,
        scope_refs,
    )
    if not evidence_lines:
        evidence_lines = _extract_heading_evidence_lines(
            _find_section_lines(source_sections, "Evidence"),
            scope_kind,
            scope_refs,
        )
    if not evidence_lines:
        raise SystemExit("No evidence lines matched the requested PR title scope")

    ordered_sections = [
        "Metadata",
        "Summary",
        "Execution Checklist",
        "Links",
        "Evidence Footer",
        "Development Link",
    ]

    rewritten_sections: dict[str, list[str]] = dict(body_sections)
    rewritten_sections["Execution Checklist"] = [
        f"- [x] `{item.identifier}`: {item.text}" for item in filtered_checklist_items
    ]
    rewritten_sections["Evidence Footer"] = [f"- {line}" for line in evidence_lines]

    rendered: list[str] = []
    for section_name in ordered_sections:
        if section_name not in rewritten_sections:
            continue
        rendered.extend(_render_section(section_name, rewritten_sections[section_name]))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(rendered).rstrip() + "\n", encoding="utf-8")
    return _repo_rel(output_path)


def main() -> int:
    args = _parse_args()
    source_log_path = _coerce_path(args.source_log_path)
    existing_body_path = _coerce_path(args.existing_body_path)
    output_path = _coerce_path(args.output_path)

    print(
        rewrite_pr_body_scope(
            source_log_path=source_log_path,
            existing_body_path=existing_body_path,
            requested_id=args.requested_id,
            pr_title=args.pr_title,
            output_path=output_path,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())