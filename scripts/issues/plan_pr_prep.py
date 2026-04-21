from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from body_contract import PR_ALLOWED_LINK_LABELS, build_pr_closing_issue_lines, extract_pr_summary_inputs, link_labels_are_allowed
from gen_issue_draft import _load_text, _parse_fields, _parse_sections, _repo_rel, _repo_root, _run_command


ID_PREFIX_RE = re.compile(r"^(?P<id>[A-Z0-9-]+)(?:/|:)")
CHECKED_ITEM_RE = re.compile(r"^- \[x\] `?([^`]+)`?:\s*(.+)$", re.IGNORECASE)
COMMIT_SUBJECT_RE = re.compile(r"^(?P<id>[A-Z0-9-]+)/(?P<unit>[^:]+):\s*(?P<summary>.+)$")
ISSUE_REF_RE = re.compile(r"(?:/issues/|^#?)(?P<number>\d+)$")
SCOPE_REF_RE = re.compile(r"\bP\d+(?:-C\d+(?:-S\d+(?:S\d+)*)?)?\b")


@dataclass
class CommitSelection:
    sha: str
    subject: str
    matched_id: str | None
    status: str
    reason: str


@dataclass
class CheckedItem:
    identifier: str
    text: str


@dataclass
class PrPrepPlanItem:
    requested_id: str
    source_log_path: str
    current_branch: str
    head_ref: str
    base_branch: str
    merge_base: str
    candidate_pr_branch: str
    pr_title: str
    pr_scope_kind: str
    pr_scope_refs: list[str]
    pr_base: str | None
    pr_labels: list[str]
    pr_projects: list[str]
    pr_milestone: str | None
    pr_development_issue: str | None
    pr_development_issue_refs: list[str]
    summary_bullet_count: int
    preview_body_path: str
    selected_commit_count: int
    selected_commits: list[CommitSelection]
    branch_commits: list[CommitSelection]
    planned_action: str
    status: str
    warnings: list[str]


@dataclass
class PrPrepPlanResult:
    mode: str
    result: str
    manifest_path: str | None
    selection_input: str
    operation: str
    total_items: int
    planned_items: int
    warnings: list[str]
    items: list[PrPrepPlanItem]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan dry-run PR prep from a mixed working branch")
    parser.add_argument("manifest_path", help="Path to a PR-prep manifest JSON file")
    parser.add_argument("--plan-path", dest="plan_path", help="Override output plan JSON path")
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _load_manifest(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse PR-prep manifest JSON: {exc}") from exc


def _split_csv(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _normalize_branch_name(raw: str) -> str:
    lowered = raw.lower()
    lowered = re.sub(r"[^a-z0-9._/-]+", "-", lowered)
    lowered = re.sub(r"/{2,}", "/", lowered).strip("-/. ")
    return lowered or "pr-prep"


def _git_stdout(*args: str) -> str:
    cmd = _run_command(["git", "-C", str(_repo_root()), *args])
    if cmd.returncode != 0:
        raise SystemExit(cmd.stderr.strip() or f"git command failed: {' '.join(args)}")
    return cmd.stdout.strip()


def _git_ref_exists(ref_name: str) -> bool:
    cmd = _run_command(["git", "-C", str(_repo_root()), "rev-parse", "--verify", ref_name])
    return cmd.returncode == 0


def _resolve_compare_base_ref(base_branch: str) -> str:
    remote_ref = f"origin/{base_branch}"
    if _git_ref_exists(remote_ref):
        return remote_ref
    return base_branch


def _find_section_lines(sections: dict[str, list[str]], prefix: str) -> list[str]:
    lowered_prefix = prefix.lower()
    for name, lines in sections.items():
        if name.lower().startswith(lowered_prefix):
            return lines
    return []


def _section_has_substantive_evidence(section_lines: list[str]) -> bool:
    for raw in section_lines:
        stripped = raw.strip()
        if not stripped:
            continue
        lowered = stripped.lower()
        if "<placeholder>" in lowered:
            continue
        if stripped.startswith("- ") or stripped.startswith("### ") or stripped.startswith("headSha:") or stripped.startswith("artifacts:"):
            return True
    return False


def _should_add_drills_label(fields: dict[str, str], sections: dict[str, list[str]]) -> bool:
    combined = " ".join(
        [fields.get("title", ""), fields.get("tags", ""), fields.get("scope", "")]
    ).lower()
    if "drills" in combined or "evidence" in combined:
        return True
    return _section_has_substantive_evidence(_find_section_lines(sections, "Evidence"))


def _build_pr_labels(fields: dict[str, str], sections: dict[str, list[str]]) -> list[str]:
    inherited = (
        _split_csv(fields.get("issue_top_labels"))
        + _split_csv(fields.get("issue_scope_labels"))
        + _split_csv(fields.get("issue_module_labels"))
    )
    explicit_pr = _split_csv(fields.get("pr_labels"))
    derived = explicit_pr + inherited
    if _should_add_drills_label(fields, sections):
        derived.append("drills")
    return _dedupe(derived)


def _build_pr_projects(fields: dict[str, str], source_log_rel: str) -> list[str]:
    explicit_pr = _split_csv(fields.get("pr_projects"))
    if explicit_pr:
        return explicit_pr
    return []


def _parse_commit_subject(subject: str) -> dict[str, str | int] | None:
    match = COMMIT_SUBJECT_RE.match(subject.strip())
    if not match:
        return None
    unit = match.group("unit").strip()
    phase_match = re.match(r"P(?P<phase>\d+)", unit)
    if not phase_match:
        return None
    return {
        "id": match.group("id").strip(),
        "unit": unit,
        "summary": match.group("summary").strip(),
        "phase": int(phase_match.group("phase")),
    }


def _compress_phase_numbers(values: list[int]) -> str:
    if not values:
        return ""

    ordered_unique: list[int] = []
    for value in sorted(set(values)):
        ordered_unique.append(value)

    parts: list[str] = []
    start = ordered_unique[0]
    end = ordered_unique[0]
    for value in ordered_unique[1:]:
        if value == end + 1:
            end = value
            continue
        parts.append(f"P{start}" if start == end else f"P{start}-P{end}")
        start = value
        end = value
    parts.append(f"P{start}" if start == end else f"P{start}-P{end}")
    return "+".join(parts)


def _build_pr_title(
    requested_id: str,
    log_title: str,
    selected_commits: list[CommitSelection],
    checklist_phase_numbers: list[int],
) -> tuple[str, str, list[str]]:
    if len(checklist_phase_numbers) > 1:
        phase_refs = [f"P{value}" for value in checklist_phase_numbers]
        return f"{requested_id}/{_compress_phase_numbers(checklist_phase_numbers)}: {log_title}", "phases", phase_refs

    parsed = [_parse_commit_subject(item.subject) for item in selected_commits]
    parsed_infos = [item for item in parsed if item is not None]

    if len(parsed_infos) == len(selected_commits) and len(parsed_infos) > 1:
        phases = [int(item["phase"]) for item in parsed_infos]
        if len(set(phases)) > 1:
            phase_refs = [f"P{value}" for value in sorted(set(phases))]
            return f"{requested_id}/{_compress_phase_numbers(phases)}: {log_title}", "phases", phase_refs

    if len(parsed_infos) == 1 and len(selected_commits) == 1:
        return selected_commits[0].subject, "units", [str(parsed_infos[0]["unit"])]

    if parsed_infos:
        units = "+".join(str(item["unit"]) for item in parsed_infos)
        summaries = _dedupe([str(item["summary"]) for item in parsed_infos])
        summary_text = "; ".join(summaries) if summaries else log_title
        return f"{requested_id}/{units}: {summary_text}", "units", _dedupe([str(item["unit"]) for item in parsed_infos])

    return f"{requested_id}: {log_title}", "all", []


def _render_commit_footer_line(commit: CommitSelection) -> str:
    parsed = _parse_commit_subject(commit.subject)
    if not parsed:
        return f"- `{commit.sha[:8]}` {commit.subject}"
    return f"- `{commit.sha[:8]}` / `{parsed['id']}` / `{parsed['unit']}`: {parsed['summary']}"


def _extract_checked_items(section_lines: list[str]) -> list[CheckedItem]:
    items: list[str] = []
    for raw in section_lines:
        match = CHECKED_ITEM_RE.match(raw.strip())
        if match:
            items.append(
                CheckedItem(
                    identifier=match.group(1).strip(),
                    text=match.group(2).strip(),
                )
            )
    return items


def _extract_scope_refs(text: str) -> list[str]:
    return _dedupe([match.group(0) for match in SCOPE_REF_RE.finditer(text)])


def _phase_ref(value: str) -> str | None:
    match = re.match(r"P\d+", value)
    return match.group(0) if match else None


def _expand_phase_scope_token(token: str) -> list[str]:
    stripped = token.strip()
    if not stripped:
        return []

    range_match = re.fullmatch(r"P(?P<start>\d+)-P(?P<end>\d+)", stripped)
    if range_match:
        start = int(range_match.group("start"))
        end = int(range_match.group("end"))
        if start > end:
            start, end = end, start
        return [f"P{value}" for value in range(start, end + 1)]

    single_match = re.fullmatch(r"P(?P<phase>\d+)", stripped)
    if single_match:
        return [f"P{single_match.group('phase')}"]

    return []


def _expand_unit_scope_ref(token: str) -> list[str]:
    stripped = token.strip()
    if not stripped or "-S" not in stripped:
        return [stripped] if stripped else []

    prefix, step_suffix = stripped.split("-S", 1)
    step_numbers = [part for part in step_suffix.split("S") if part]
    if len(step_numbers) <= 1 or any(not part.isdigit() for part in step_numbers):
        return [stripped]
    return [f"{prefix}-S{part}" for part in step_numbers]


def _derive_scope_from_pr_title(pr_title: str, requested_id: str) -> tuple[str, list[str]]:
    title_match = re.match(rf"^{re.escape(requested_id)}/(?P<scope>[^:]+):", pr_title.strip())
    if not title_match:
        return "all", []

    scope_text = title_match.group("scope").strip()
    if not scope_text:
        return "all", []

    scope_refs = _extract_scope_refs(scope_text)
    if any("-C" in ref or "-S" in ref for ref in scope_refs):
        expanded_unit_refs: list[str] = []
        for ref in scope_refs:
            expanded_unit_refs.extend(_expand_unit_scope_ref(ref))
        return "units", _dedupe(expanded_unit_refs)

    expanded_phase_refs: list[str] = []
    for token in scope_text.split("+"):
        expanded_phase_refs.extend(_expand_phase_scope_token(token))
    if expanded_phase_refs:
        return "phases", _dedupe(expanded_phase_refs)

    return "all", []


def _matches_scope(value: str, scope_kind: str, scope_refs: list[str]) -> bool:
    if scope_kind == "all" or not scope_refs:
        return True

    line_refs = _extract_scope_refs(value)
    if not line_refs:
        return False

    if scope_kind == "phases":
        phase_refs = set(scope_refs)
        return any((_phase_ref(ref) or "") in phase_refs for ref in line_refs)

    return any(ref in scope_refs for ref in line_refs)


def _extract_evidence_scope_refs(value: str) -> list[str]:
    prefix = value.split(":", 1)[0]
    return _extract_scope_refs(prefix)


def _filter_checked_items(
    items: list[CheckedItem],
    scope_kind: str,
    scope_refs: list[str],
) -> list[CheckedItem]:
    if scope_kind == "all" or not scope_refs:
        return items

    filtered: list[CheckedItem] = []
    for item in items:
        if scope_kind == "phases":
            item_phase = _phase_ref(item.identifier)
            if item_phase and item_phase in scope_refs:
                filtered.append(item)
            continue
        if item.identifier in scope_refs:
            filtered.append(item)
    return filtered


def _extract_scoped_evidence_lines(
    section_lines: list[str],
    scope_kind: str,
    scope_refs: list[str],
) -> list[str]:
    evidence_lines: list[str] = []
    for raw in section_lines:
        stripped = raw.strip()
        if not stripped:
            continue
        value = stripped[2:].strip() if stripped.startswith("- ") else stripped
        evidence_scope_refs = _extract_evidence_scope_refs(value)
        if scope_kind == "all" or not scope_refs:
            evidence_lines.append(value)
            continue
        if not evidence_scope_refs:
            continue
        if scope_kind == "phases":
            phase_refs = set(scope_refs)
            if any((_phase_ref(ref) or "") in phase_refs for ref in evidence_scope_refs):
                evidence_lines.append(value)
            continue
        if any(ref in scope_refs for ref in evidence_scope_refs):
            evidence_lines.append(value)
    return evidence_lines


def _extract_checked_phase_numbers(section_lines: list[str]) -> list[int]:
    phases: list[int] = []
    for raw in section_lines:
        match = CHECKED_ITEM_RE.match(raw.strip())
        if not match:
            continue
        phase_match = re.match(r"P(?P<phase>\d+)", match.group(1).strip())
        if phase_match:
            phases.append(int(phase_match.group("phase")))
    return sorted(set(phases))


def _build_default_link_lines(fields: dict[str, str], source_log_path: str) -> list[str]:
    lines = [f"Log: `{source_log_path}`"]
    if fields.get("runbook", "").strip():
        lines.append(f"Runbook: `{fields['runbook'].strip()}`")
    if fields.get("parent_log", "").strip():
        lines.append(f"Parent log: `{fields['parent_log'].strip()}`")
    if fields.get("roadmap", "").strip():
        lines.append(f"Roadmap: `{fields['roadmap'].strip()}`")
    return lines


def _select_pr_link_lines(fields: dict[str, str], explicit_link_lines: list[str], source_log_path: str) -> list[str]:
    sanitized: list[str] = []
    for line in explicit_link_lines:
        valid, _ = link_labels_are_allowed([f"- {line}"], PR_ALLOWED_LINK_LABELS)
        if valid:
            sanitized.append(line)
    return sanitized or _build_default_link_lines(fields, source_log_path)


def _parse_issue_refs(raw: str | None) -> tuple[list[str], list[str]]:
    refs: list[str] = []
    warnings: list[str] = []
    for part in _split_csv(raw):
        token = part.strip()
        if not token:
            continue
        match = ISSUE_REF_RE.search(token)
        if not match:
            warnings.append(f"unrecognized issue reference skipped: {token}")
            continue
        refs.append(f"#{match.group('number')}")
    return _dedupe(refs), warnings


def _derive_pr_development_issue(fields: dict[str, str]) -> tuple[str | None, list[str]]:
    warnings: list[str] = []

    explicit_value = fields.get("pr_development_issue", "").strip()
    explicit_refs, explicit_warnings = _parse_issue_refs(explicit_value)
    warnings.extend([f"pr_development_issue {item}" for item in explicit_warnings])
    if explicit_refs:
        return ", ".join(explicit_refs), warnings

    source_issue_value = fields.get("issue", "").strip()
    source_issue_refs, source_issue_warnings = _parse_issue_refs(source_issue_value)
    warnings.extend([f"source log issue {item}" for item in source_issue_warnings])
    if source_issue_refs:
        warnings.append("pr_development_issue derived from source log issue link")
        return ", ".join(source_issue_refs), warnings

    return None, warnings


def _render_body_preview(
    *,
    requested_id: str,
    pr_title: str,
    base_branch: str,
    candidate_pr_branch: str,
    source_log_path: str,
    summary_bullets: list[str],
    checklist_items: list[CheckedItem],
    link_lines: list[str],
    evidence_footer_lines: list[str],
    pr_labels: list[str],
    pr_projects: list[str],
    pr_development_issue: str | None,
) -> str:
    closing_issue_lines = build_pr_closing_issue_lines(pr_development_issue)
    summary_lines = [f"- {item}" for item in summary_bullets] or ["- <placeholder>"]
    checklist_lines = [f"- [x] `{item.identifier}`: {item.text}" for item in checklist_items] or ["- [ ] <placeholder>"]
    lines = [
        "## Metadata",
        "",
        f"- Requested ID: `{requested_id}`",
        f"- Base branch: `{base_branch}`",
        f"- Candidate PR-prep branch: `{candidate_pr_branch}`",
        f"- Source log: `{source_log_path}`",
        f"- Labels: `{', '.join(pr_labels)}`",
        f"- Development issue: {pr_development_issue or ''}",
        "",
        "## Summary",
        "",
        *summary_lines,
        "",
        "## Execution Checklist",
        "",
        *checklist_lines,
        "",
        "## Links",
        "",
        *[f"- {item}" for item in link_lines],
    ]
    if evidence_footer_lines:
        lines.extend([
            "",
            "## Evidence Footer",
            "",
            *[f"- {item}" for item in evidence_footer_lines],
        ])
    if closing_issue_lines:
        lines.extend([
            "",
            *closing_issue_lines,
        ])
    return "\n".join(lines)


def _collect_branch_commits(base_branch: str, head_ref: str) -> tuple[str, list[CommitSelection]]:
    compare_base_ref = _resolve_compare_base_ref(base_branch)
    merge_base = _git_stdout("merge-base", compare_base_ref, head_ref)
    raw = _git_stdout("log", "--reverse", "--format=%H%x1f%s", f"{compare_base_ref}..{head_ref}")
    items: list[CommitSelection] = []
    if raw:
        for line in raw.splitlines():
            sha, subject = line.split("\x1f", 1)
            match = ID_PREFIX_RE.match(subject.strip())
            matched_id = match.group("id") if match else None
            items.append(
                CommitSelection(
                    sha=sha,
                    subject=subject,
                    matched_id=matched_id,
                    status="unclassified",
                    reason="branch-exclusive commit",
                )
            )
    return merge_base, items


def _build_plan_item(item: dict, defaults: dict, repo_root: Path, preview_dir: Path, preview_stem: str) -> PrPrepPlanItem:
    warnings: list[str] = []
    requested_id = (item.get("requested_id") or defaults.get("requested_id") or "").strip()
    if not requested_id:
        raise SystemExit("PR-prep manifest item missing requested_id")
    preview_path = preview_dir / f"{preview_stem}-{requested_id.lower()}-body.md"

    source_log_value = item.get("source_log_path") or defaults.get("source_log_path")
    if not source_log_value:
        raise SystemExit("PR-prep manifest item missing source_log_path")
    source_log_path = _coerce_path(source_log_value, repo_root)
    if not source_log_path.is_file():
        raise SystemExit(f"PR-prep source log not found: {source_log_path}")

    full_text = _load_text(source_log_path)
    fields = _parse_fields(full_text)
    sections = _parse_sections(full_text)
    source_log_rel = _repo_rel(source_log_path)

    current_branch = _git_stdout("branch", "--show-current")
    head_ref = (item.get("head_ref") or defaults.get("head_ref") or current_branch or "HEAD").strip()
    manifest_base_branch = (item.get("base_branch") or defaults.get("base_branch") or "").strip() or None
    source_log_pr_base = fields.get("pr_base", "").strip() or None

    if manifest_base_branch and source_log_pr_base and manifest_base_branch != source_log_pr_base:
        warnings.append("manifest base_branch differs from source log pr_base; source log pr_base remains canonical")

    base_branch = source_log_pr_base or manifest_base_branch
    pr_labels = _build_pr_labels(fields, sections)
    pr_projects = _build_pr_projects(fields, source_log_rel)
    pr_milestone = fields.get("pr_milestone", "").strip() or None
    pr_development_issue, development_warnings = _derive_pr_development_issue(fields)
    warnings.extend(development_warnings)

    if not base_branch:
        return PrPrepPlanItem(
            requested_id=requested_id,
            source_log_path=source_log_rel,
            current_branch=current_branch,
            head_ref=head_ref,
            base_branch="",
            merge_base="",
            candidate_pr_branch="",
            pr_title="",
            pr_scope_kind="all",
            pr_scope_refs=[],
            pr_base=source_log_pr_base,
            pr_labels=pr_labels,
            pr_projects=pr_projects,
            pr_milestone=pr_milestone,
            pr_development_issue=pr_development_issue,
            pr_development_issue_refs=_parse_issue_refs(pr_development_issue)[0] if pr_development_issue else [],
            summary_bullet_count=0,
            preview_body_path=_repo_rel(preview_path),
            selected_commit_count=0,
            selected_commits=[],
            branch_commits=[],
            planned_action="error-missing-base-branch",
            status="error",
            warnings=warnings + ["base branch is required for PR-prep dry-run"],
        )

    merge_base, branch_commits = _collect_branch_commits(base_branch, head_ref)
    selected_commits: list[CommitSelection] = []
    for commit in branch_commits:
        if commit.matched_id == requested_id:
            commit.status = "selected"
            commit.reason = "commit subject matches requested ID prefix"
            selected_commits.append(commit)
        else:
            commit.status = "skipped"
            commit.reason = "commit subject does not match requested ID prefix"

    if not selected_commits:
        warnings.append("no branch-exclusive commits matched the requested ID prefix")

    requested_slug = _normalize_branch_name(requested_id)
    candidate_pr_branch = (item.get("candidate_pr_branch") or defaults.get("candidate_pr_branch") or f"pr-prep/{requested_slug}").strip()

    summary_bullets, explicit_link_lines, evidence_footer_source_lines = extract_pr_summary_inputs(full_text)
    if not summary_bullets:
        warnings.append("source log is missing PR summary bullets; preview uses placeholders")

    checklist_section_lines = _find_section_lines(sections, "Execution Checklist")
    checklist_items = _extract_checked_items(checklist_section_lines)
    checklist_phase_numbers = _extract_checked_phase_numbers(checklist_section_lines)
    if not checklist_items:
        warnings.append("source log has no checked execution checklist items for PR preview")

    pr_title, fallback_scope_kind, fallback_scope_refs = _build_pr_title(
        requested_id,
        fields.get("title", "").strip() or requested_id,
        selected_commits,
        checklist_phase_numbers,
    )

    pr_scope_kind, pr_scope_refs = _derive_scope_from_pr_title(pr_title, requested_id)
    if pr_scope_kind == "all" and not pr_scope_refs:
        pr_scope_kind = fallback_scope_kind
        pr_scope_refs = fallback_scope_refs

    scoped_checklist_items = _filter_checked_items(checklist_items, pr_scope_kind, pr_scope_refs)
    if checklist_items and not scoped_checklist_items:
        warnings.append("scope-aligned checklist selection found no matches; preview falls back to all checked items")
        scoped_checklist_items = checklist_items

    scoped_evidence_lines = _extract_scoped_evidence_lines(
        evidence_footer_source_lines,
        pr_scope_kind,
        pr_scope_refs,
    )

    link_lines = _select_pr_link_lines(fields, explicit_link_lines, source_log_rel)
    preview_body = _render_body_preview(
        requested_id=requested_id,
        pr_title=pr_title,
        base_branch=base_branch,
        candidate_pr_branch=candidate_pr_branch,
        source_log_path=source_log_rel,
        summary_bullets=summary_bullets,
        checklist_items=scoped_checklist_items,
        link_lines=link_lines,
        evidence_footer_lines=scoped_evidence_lines,
        pr_labels=pr_labels,
        pr_projects=pr_projects,
        pr_development_issue=pr_development_issue,
    )
    preview_path.write_text(preview_body + "\n", encoding="utf-8")

    status = "planned" if selected_commits else "warning"
    planned_action = "prepare-pr-prep-branch" if selected_commits else "inspect-commit-history"
    return PrPrepPlanItem(
        requested_id=requested_id,
        source_log_path=source_log_rel,
        current_branch=current_branch,
        head_ref=head_ref,
        base_branch=base_branch,
        merge_base=merge_base,
        candidate_pr_branch=candidate_pr_branch,
        pr_title=pr_title,
        pr_scope_kind=pr_scope_kind,
        pr_scope_refs=pr_scope_refs,
        pr_base=source_log_pr_base,
        pr_labels=pr_labels,
        pr_projects=pr_projects,
        pr_milestone=pr_milestone,
        pr_development_issue=pr_development_issue,
        pr_development_issue_refs=_parse_issue_refs(pr_development_issue)[0] if pr_development_issue else [],
        summary_bullet_count=len(summary_bullets),
        preview_body_path=_repo_rel(preview_path),
        selected_commit_count=len(selected_commits),
        selected_commits=selected_commits,
        branch_commits=branch_commits,
        planned_action=planned_action,
        status=status,
        warnings=warnings,
    )


def plan_pr_prep(args: argparse.Namespace) -> PrPrepPlanResult:
    repo_root = _repo_root()
    manifest_path = _coerce_path(args.manifest_path, repo_root)
    if not manifest_path.is_file():
        raise SystemExit(f"PR-prep manifest file not found: {manifest_path}")

    manifest = _load_manifest(manifest_path)
    defaults = manifest.get("defaults") or {}
    items = manifest.get("items") or []
    if not items:
        raise SystemExit("PR-prep manifest requires at least one item")

    manifest_rel = _repo_rel(manifest_path)
    manifest_slug = manifest_path.stem
    if manifest_slug.endswith("-manifest"):
        manifest_slug = manifest_slug[: -len("-manifest")]
    default_plan_path = repo_root / "docs" / "issues" / f"{manifest_slug}-plan.json"
    plan_path = _coerce_path(args.plan_path, repo_root) if args.plan_path else default_plan_path
    plan_path.parent.mkdir(parents=True, exist_ok=True)

    preview_dir = plan_path.parent
    preview_stem = manifest_slug
    plan_items = [_build_plan_item(item, defaults, repo_root, preview_dir, preview_stem) for item in items]
    top_warnings: list[str] = []
    for item in plan_items:
        for warning in item.warnings:
            top_warnings.append(f"{item.requested_id}: {warning}")

    result = PrPrepPlanResult(
        mode="pr-prep-dry-run",
        result="ok",
        manifest_path=manifest_rel,
        selection_input="manifest",
        operation="plan-pr-prep",
        total_items=len(plan_items),
        planned_items=sum(1 for item in plan_items if item.status == "planned"),
        warnings=top_warnings,
        items=plan_items,
    )
    plan_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        plan_pr_prep(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())