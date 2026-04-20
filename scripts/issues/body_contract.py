from __future__ import annotations

from datetime import datetime
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _derive_repo_slug, _parse_fields, _parse_sections, _require_gh_auth, _require_gh_cli, _run_command


PR_REQUIRED_SECTIONS = ["Metadata", "Summary", "Execution Checklist", "Links"]
PR_OPTIONAL_SECTIONS = ["Evidence Footer"]
ISSUE_REQUIRED_SECTIONS = ["Metadata", "Context", "Definition of Done (DoD)", "Links"]
PR_ALLOWED_LINK_LABELS = {"Log", "Runbook", "Evidence artifact", "Parent log", "Roadmap"}
ISSUE_ALLOWED_LINK_LABELS = {"Log", "Runbook", "Parent log", "Previous log", "Roadmap"}
EVIDENCE_FOOTER_LINE_RE = re.compile(r"^`(?P<stage>[^`]+)` \| artifact: `(?P<artifact>[^`]+)`$")
LINK_LINE_RE = re.compile(r"^- (?P<label>[^:]+):\s+`[^`]*`$")
CHECKLIST_ITEM_RE = re.compile(r"^- \[(?:x| )\] `?(?P<identifier>[^`]+)`?:")
ISSUE_REF_RE = re.compile(r"(?:/issues/|^#?)(?P<number>\d+)$")
PR_CLOSING_ISSUE_LINE_RE = re.compile(r"^Closes #(?P<number>\d+)$")
PHASE_LOG_KEY_RE = re.compile(r"^phase_log_(?P<index>\d+)$")
SCOPE_REF_RE = re.compile(r"\bP\d+(?:-C\d+(?:-S\d+(?:S\d+)*)?)?\b")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
SENTENCE_TERMINATOR_RE = re.compile(r"[.!?]")
MULTI_SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
VERSION_SUFFIX_RE = re.compile(r"\s+v\d+\s*$", re.IGNORECASE)
INLINE_CODE_RE = re.compile(r"`([^`]*)`")
SECTION_PHASE_PREFIX_RE = re.compile(r"^`?P\d+(?:-C\d+(?:-S\d+(?:S\d+)*)?)?`?:\s*")
LOG_ID_FROM_PATH_RE = re.compile(r"log-(?P<id>[A-Z0-9]+(?:-[A-Z0-9]+)*)-")
PLACEHOLDER_RE = re.compile(r"<placeholder>|\btodo\b|\btbd\b|\bn/a\b", re.IGNORECASE)
VERB_LEADERS = {
    "add",
    "align",
    "attach",
    "connect",
    "convert",
    "create",
    "define",
    "establish",
    "fix",
    "harden",
    "implement",
    "land",
    "make",
    "record",
    "regenerate",
    "remove",
    "repair",
    "replay",
    "rerun",
    "retain",
    "rewrite",
    "scope",
    "split",
    "stabilize",
    "track",
    "update",
    "validate",
    "verify",
    "wire",
}


@dataclass
class ContractCheck:
    name: str
    status: str
    details: str


@dataclass
class PrBodyContractResult:
    status: str
    checks: list[ContractCheck]
    warnings: list[str]
    expected_evidence_footer_lines: list[str]


def extract_section_order(text: str) -> list[str]:
    order: list[str] = []
    for raw in text.splitlines():
        if raw.startswith("## "):
            order.append(raw[3:].strip())
    return order


def _find_pr_summary_input_lines(text: str) -> list[str]:
    return _parse_sections(text).get("PR Summary Inputs (optional)", []) or _parse_sections(text).get("PR Summary Inputs", [])


def _parse_pr_summary_inputs(section_lines: list[str]) -> tuple[list[str], list[str], list[str]]:
    summary_bullets: list[str] = []
    link_lines: list[str] = []
    evidence_footer_source_lines: list[str] = []
    current: str | None = None
    evidence_footer_source_started = False

    for raw in section_lines:
        stripped = raw.strip()
        if stripped == "**PR summary bullets**:":
            current = "summary"
            evidence_footer_source_started = False
            continue
        if stripped in {"**PR links**:", "**PR links / evidence footer**:"}:
            current = "links"
            evidence_footer_source_started = False
            continue
        if stripped == "**Evidence Footer Source**:":
            current = "evidence-footer-source"
            evidence_footer_source_started = False
            continue
        if current == "evidence-footer-source":
            if stripped.startswith("- "):
                evidence_footer_source_lines.append(stripped[2:].strip())
                evidence_footer_source_started = True
                continue
            if not evidence_footer_source_started and not stripped:
                continue
            current = None
        if stripped.startswith("**") and stripped.endswith(":"):
            current = None
            evidence_footer_source_started = False
            continue
        if not stripped.startswith("- "):
            continue
        value = stripped[2:].strip()
        if current == "summary":
            summary_bullets.append(value)
        elif current == "links":
            link_lines.append(value)

    return summary_bullets, link_lines, evidence_footer_source_lines


def extract_evidence_footer_source_lines(log_text: str) -> list[str]:
    summary_lines = _find_pr_summary_input_lines(log_text)
    _, _, source_lines = _parse_pr_summary_inputs(summary_lines)
    if source_lines:
        return source_lines

    sections = _parse_sections(log_text)
    standalone = sections.get("Evidence Footer Source", [])
    if not standalone:
        return []

    result: list[str] = []
    for raw in standalone:
        stripped = raw.strip()
        if stripped.startswith("- "):
            result.append(stripped[2:].strip())
    return result


def extract_pr_summary_inputs(log_text: str) -> tuple[list[str], list[str], list[str]]:
    return _parse_pr_summary_inputs(_find_pr_summary_input_lines(log_text))


def issue_body_expected_context_line_count(source_log_text: str) -> int:
    _, max_count = issue_body_context_line_bounds(source_log_text)
    return max_count


def issue_body_context_line_bounds(source_log_text: str) -> tuple[int, int]:
    fields = _parse_fields(source_log_text)
    parent_log = str(fields.get("parent_log") or "").strip()
    return (5, 5) if not parent_log else (4, 4)


def _issue_context_scope_label(source_log_text: str) -> str:
    return "main" if issue_body_expected_context_line_count(source_log_text) == 5 else "child"


def _strip_markdown(text: str) -> str:
    plain = INLINE_CODE_RE.sub(r"\1", text)
    plain = plain.replace("**", "")
    plain = plain.replace("->", " to ")
    plain = plain.replace("→", " to ")
    plain = plain.replace("&", " and ")
    plain = re.sub(r"<[^>]+>", "", plain)
    plain = re.sub(r"\s+", " ", plain)
    return plain.strip()


def _normalize_title_subject(raw_title: str) -> str:
    text = _strip_markdown(raw_title)
    text = VERSION_SUFFIX_RE.sub("", text)
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"（[^）]*）", "", text)
    text = re.sub(r"\s*\+\s*drills/evidence\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*\+\s*evidence/drills\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*\+\s*drills\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip(" -")
    return text or "the recorded delivery scope"


def _extract_title_details(raw_title: str) -> str | None:
    matches = re.findall(r"\(([^()]*)\)", _strip_markdown(raw_title))
    for match in matches:
        detail = VERSION_SUFFIX_RE.sub("", match).strip(" -")
        if detail:
            return detail
    return None


def _single_sentence(text: str) -> str:
    stripped = _strip_markdown(text)
    stripped = re.sub(r"[.!?]+", "", stripped)
    stripped = re.sub(r"\s+", " ", stripped).strip(" ,;:-")
    return f"{stripped}." if stripped else "Context remains aligned with the source log."


def _sentence_bullet(text: str) -> str:
    return f"- {_single_sentence(text)}"


def _lower_first(text: str) -> str:
    if not text:
        return text
    if text[0].isalpha():
        return text[0].lower() + text[1:]
    return text


def _extract_follow_up_id(path: str) -> str | None:
    match = LOG_ID_FROM_PATH_RE.search(path or "")
    if match:
        return match.group("id")
    return None


def _sanitize_focus_phrase(raw: str) -> str:
    phrase = _strip_markdown(raw)
    phrase = SECTION_PHASE_PREFIX_RE.sub("", phrase)
    phrase = re.sub(r"^[-*]\s*", "", phrase)
    phrase = re.sub(r"\s+", " ", phrase).strip(" ,;:-")
    return phrase


def _english_focus_candidates(source_log_text: str) -> list[str]:
    summary_bullets, _, _ = extract_pr_summary_inputs(source_log_text)
    candidates: list[str] = []
    for bullet in summary_bullets:
        phrase = _sanitize_focus_phrase(bullet)
        if phrase and not CJK_RE.search(phrase) and re.search(r"[A-Za-z]", phrase):
            candidates.append(phrase)

    sections = _parse_sections(source_log_text)
    for section_name in ["Scope", "Success Criteria (DoD)", "Success Criteria", "Definitions (optional)", "Definitions"]:
        for raw in sections.get(section_name, []):
            stripped = raw.strip()
            if not stripped.startswith("- "):
                continue
            phrase = _sanitize_focus_phrase(stripped[2:].strip())
            if phrase and not CJK_RE.search(phrase) and re.search(r"[A-Za-z]", phrase):
                candidates.append(phrase)

    deduped: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = candidate.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(candidate)
    return deduped


def _focus_to_sentence(prefix_kind: str, phrase: str) -> str:
    lowered = _lower_first(phrase)
    first_word = lowered.split(" ", 1)[0].strip("`'\"").lower()
    if prefix_kind == "primary":
        if first_word in VERB_LEADERS:
            return f"The source log opened this slice to {lowered}"
        return f"The source log centers this slice on {lowered}"
    if first_word in VERB_LEADERS:
        return f"It also planned to {lowered}"
    return f"It also kept the scope on {lowered}"


def _extract_subsection_bullets(section_lines: list[str], header_prefixes: tuple[str, ...]) -> list[str]:
    bullets: list[str] = []
    current_enabled = False
    for raw in section_lines:
        stripped = raw.strip()
        if stripped.startswith("**") and stripped.endswith(":"):
            header = stripped.strip("*:").strip().lower()
            current_enabled = any(header.startswith(prefix) for prefix in header_prefixes)
            continue
        if current_enabled and stripped.startswith("- "):
            phrase = _sanitize_focus_phrase(stripped[2:].strip())
            if phrase and not CJK_RE.search(phrase) and re.search(r"[A-Za-z]", phrase):
                bullets.append(phrase)
    return bullets


def _extract_plain_section_bullets(section_lines: list[str]) -> list[str]:
    bullets: list[str] = []
    for raw in section_lines:
        stripped = raw.strip()
        if not stripped.startswith("- "):
            continue
        phrase = _sanitize_focus_phrase(stripped[2:].strip())
        if phrase and not CJK_RE.search(phrase) and re.search(r"[A-Za-z]", phrase):
            bullets.append(phrase)
    return bullets


def _dedupe_preserve(items: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for item in items:
        normalized = _single_sentence(item).lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(item)
    return deduped


def extract_issue_context_bullet_lines(section_lines: list[str]) -> list[str]:
    return [line.strip() for line in section_lines if line.strip().startswith("- ")]


def validate_issue_context_lines(section_lines: list[str], line_bounds: tuple[int, int], source_log_text: str | None = None) -> tuple[bool, str, list[str]]:
    trimmed = [line.strip() for line in section_lines if line.strip()]
    bullet_lines = [line for line in trimmed if line.startswith("- ")]
    invalid_lines: list[str] = []
    min_count, max_count = line_bounds

    if len(trimmed) != len(bullet_lines):
        return False, "Context contains non-bullet content or blank-gap drift", invalid_lines
    if len(bullet_lines) < min_count or len(bullet_lines) > max_count:
        if min_count == max_count:
            return False, f"Context must contain exactly {min_count} English bullet sentences; found {len(bullet_lines)}", invalid_lines
        return False, f"Context must contain between {min_count} and {max_count} English bullet sentences; found {len(bullet_lines)}", invalid_lines

    for raw in bullet_lines:
        sentence = raw[2:].strip()
        if not sentence:
            invalid_lines.append(raw)
            continue
        if PLACEHOLDER_RE.search(sentence):
            invalid_lines.append(raw)
            continue
        if CJK_RE.search(sentence) or not re.search(r"[A-Za-z]", sentence):
            invalid_lines.append(raw)
            continue
        if not re.search(r"[.!?]$", sentence):
            invalid_lines.append(raw)
            continue
        if MULTI_SENTENCE_BOUNDARY_RE.search(sentence):
            invalid_lines.append(raw)

    if invalid_lines:
        return False, "Context lines must be readable English sentences with no placeholder scaffolding", invalid_lines

    if min_count == max_count:
        return True, f"Context contains exactly {min_count} readable English bullet sentences with basic placeholder hygiene", invalid_lines
    return True, f"Context contains between {min_count} and {max_count} readable English bullet sentences with basic placeholder hygiene", invalid_lines


def pr_body_is_evidence_footer_eligible(source_log_text: str) -> bool:
    fields = _parse_fields(source_log_text)
    tags = str(fields.get("tags") or "").lower()
    pr_labels = str(fields.get("pr_labels") or "").lower()
    title = str(fields.get("title") or "").lower()
    return any(token in tags or token in pr_labels or token in title for token in ["drills", "evidence"])


def _extract_scope_refs(text: str) -> list[str]:
    seen: set[str] = set()
    refs: list[str] = []
    for match in SCOPE_REF_RE.finditer(text):
        value = match.group(0)
        if value not in seen:
            seen.add(value)
            refs.append(value)
    return refs


def _phase_ref(value: str) -> str | None:
    match = re.match(r"P\d+", value)
    return match.group(0) if match else None


def _expand_unit_scope_ref(token: str) -> list[str]:
    stripped = token.strip()
    if not stripped or "-S" not in stripped:
        return [stripped] if stripped else []

    prefix, step_suffix = stripped.split("-S", 1)
    step_numbers = [part for part in step_suffix.split("S") if part]
    if len(step_numbers) <= 1 or any(not part.isdigit() for part in step_numbers):
        return [stripped]
    return [f"{prefix}-S{part}" for part in step_numbers]


def _extract_rendered_checklist_scope(checklist_lines: list[str]) -> tuple[str, list[str]]:
    identifiers: list[str] = []
    seen: set[str] = set()
    for raw in checklist_lines:
        match = CHECKLIST_ITEM_RE.match(raw.strip())
        if not match:
            continue
        identifier = match.group("identifier").strip()
        if identifier not in seen:
            seen.add(identifier)
            identifiers.append(identifier)

    if not identifiers:
        return "all", []

    if any("-C" in identifier or "-S" in identifier for identifier in identifiers):
        expanded: list[str] = []
        for identifier in identifiers:
            expanded.extend(_expand_unit_scope_ref(identifier))
        deduped: list[str] = []
        seen_units: set[str] = set()
        for identifier in expanded:
            if identifier and identifier not in seen_units:
                seen_units.add(identifier)
                deduped.append(identifier)
        return "units", deduped

    phase_refs: list[str] = []
    seen_phases: set[str] = set()
    for identifier in identifiers:
        phase = _phase_ref(identifier)
        if phase and phase not in seen_phases:
            seen_phases.add(phase)
            phase_refs.append(phase)
    return ("phases", phase_refs) if phase_refs else ("all", [])


def _filter_evidence_footer_lines_for_scope(lines: list[str], scope_kind: str, scope_refs: list[str]) -> list[str]:
    if scope_kind == "all" or not scope_refs:
        return list(lines)

    filtered: list[str] = []
    phase_scope = set(scope_refs)
    for line in lines:
        raw_line_refs = _extract_scope_refs(line.split(":", 1)[0])
        line_refs: list[str] = []
        if scope_kind == "units":
            for ref in raw_line_refs:
                line_refs.extend(_expand_unit_scope_ref(ref))
        else:
            line_refs = raw_line_refs
        if not line_refs:
            continue
        if scope_kind == "phases":
            if any((_phase_ref(ref) or "") in phase_scope for ref in line_refs):
                filtered.append(line)
            continue
        if any(ref in scope_refs for ref in line_refs):
            filtered.append(line)
    return filtered


def _validate_order(actual: list[str], expected_prefix: list[str], optional_tail: list[str]) -> tuple[str, str]:
    allowed = expected_prefix + optional_tail
    unknown = [name for name in actual if name not in allowed]
    if unknown:
        return "fail", f"unexpected sections present: {unknown}"

    position = 0
    for section in actual:
        try:
            next_position = allowed.index(section, position)
        except ValueError:
            return "fail", f"section order is invalid: {actual}"
        position = next_position

    missing = [name for name in expected_prefix if name not in actual]
    if missing:
        return "fail", f"missing required sections for canonical order: {missing}"
    return "pass", "section order matches the canonical contract"


def bullets_are_contiguous(section_lines: list[str]) -> bool:
    trimmed = list(section_lines)
    while trimmed and not trimmed[0].strip():
        trimmed.pop(0)
    while trimmed and not trimmed[-1].strip():
        trimmed.pop()
    if not trimmed:
        return True
    saw_bullet = False
    saw_gap_after_bullet = False
    for raw in trimmed:
        stripped = raw.strip()
        if not stripped:
            if saw_bullet:
                saw_gap_after_bullet = True
            continue
        if not stripped.startswith("- "):
            return False
        if saw_gap_after_bullet:
            return False
        saw_bullet = True
    return True


def link_labels_are_allowed(link_lines: list[str], allowed_labels: set[str]) -> tuple[bool, list[str]]:
    invalid: list[str] = []
    for line in link_lines:
        match = LINK_LINE_RE.match(line)
        if not match or match.group("label") not in allowed_labels:
            invalid.append(line)
    return not invalid, invalid


def validate_evidence_footer_source_lines(lines: list[str]) -> tuple[bool, list[str]]:
    invalid = [line for line in lines if not EVIDENCE_FOOTER_LINE_RE.fullmatch(line)]
    return not invalid, invalid


def _extract_bullet_label(line: str) -> str | None:
    stripped = line.strip()
    if not stripped.startswith("- "):
        return None
    label, separator, _ = stripped[2:].partition(":")
    if not separator:
        return None
    return label.strip()


def metadata_contains_source_log_row(metadata_lines: list[str]) -> bool:
    return any(_extract_bullet_label(line) == "Source log" for line in metadata_lines)


def metadata_contains_parent_issue_row(metadata_lines: list[str]) -> bool:
    return any(_extract_bullet_label(line) == "Parent issue" for line in metadata_lines)


def strip_issue_navigation_metadata_rows(metadata_lines: list[str]) -> list[str]:
    cleaned: list[str] = []
    for line in metadata_lines:
        stripped = line.strip()
        if not stripped:
            continue
        if _extract_bullet_label(stripped) == "Source log":
            continue
        cleaned.append(stripped)
    return cleaned


def issue_uses_parent_body_contract(fields: dict[str, str]) -> bool:
    return not str(fields.get("parent_log") or "").strip()


def extract_phase_log_paths(fields: dict[str, str]) -> list[str]:
    entries: list[tuple[int, str]] = []
    for key, value in fields.items():
        match = PHASE_LOG_KEY_RE.fullmatch(key)
        if not match:
            continue
        path = str(value or "").strip()
        if not path:
            continue
        entries.append((int(match.group("index")), path))
    return [path for _, path in sorted(entries, key=lambda item: item[0])]


def parse_issue_number(value: str | None) -> int | None:
    if not value:
        return None
    match = ISSUE_REF_RE.search(value.strip())
    return int(match.group("number")) if match else None


def normalize_issue_short_ref(value: str | None) -> str | None:
    number = parse_issue_number(value)
    return f"#{number}" if number is not None else None


def _resolve_repo_path(repo_root: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate.resolve()
    return (repo_root / candidate).resolve()


def _repo_relative_or_absolute(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def _fetch_issue_completion_state(repo: str, short_ref: str) -> tuple[str | None, str | None]:
    cmd = _run_command([
        "gh",
        "issue",
        "view",
        short_ref,
        "--repo",
        repo,
        "--json",
        "state,stateReason",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to view issue {short_ref} in {repo}: {cmd.stderr.strip()}")
    try:
        data = json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse issue state JSON for {short_ref}: {exc}") from exc
    return str(data.get("state") or "") or None, str(data.get("stateReason") or "") or None


def ordered_parent_child_issue_refs(repo_root: Path, fields: dict[str, str]) -> list[str]:
    refs: list[tuple[str, int, str]] = []
    seen: set[str] = set()
    repo = _derive_repo_slug(None)
    _require_gh_cli()
    _require_gh_auth()
    for phase_index, phase_log_path in enumerate(extract_phase_log_paths(fields)):
        resolved = _resolve_repo_path(repo_root, phase_log_path)
        if not resolved.is_file():
            continue
        child_fields = _parse_fields(resolved.read_text(encoding="utf-8"))
        short_ref = normalize_issue_short_ref(child_fields.get("issue"))
        if not short_ref or short_ref in seen:
            continue

        created_raw = str(child_fields.get("created") or "").strip()
        if not created_raw:
            child_log = _repo_relative_or_absolute(resolved, repo_root)
            raise SystemExit(
                f"Parent child-ledger ordering requires child log created metadata: {child_log} ({short_ref})"
            )
        try:
            datetime.strptime(created_raw, "%Y-%m-%d")
        except ValueError as exc:
            child_log = _repo_relative_or_absolute(resolved, repo_root)
            raise SystemExit(
                f"Parent child-ledger ordering requires child log created metadata in YYYY-MM-DD format: {child_log} ({short_ref})"
            ) from exc

        issue_state, issue_state_reason = _fetch_issue_completion_state(repo, short_ref)
        if issue_state != "CLOSED" or issue_state_reason != "COMPLETED":
            continue

        seen.add(short_ref)
        refs.append((created_raw, phase_index, short_ref))

    return [short_ref for _, _, short_ref in sorted(refs, key=lambda item: (item[0], item[1], item[2]))]


def parse_issue_refs(value: str | None) -> list[str]:
    if not value:
        return []
    refs: list[str] = []
    for part in str(value).split(","):
        token = part.strip()
        if not token:
            continue
        match = ISSUE_REF_RE.search(token)
        if match:
            refs.append(f"#{match.group('number')}")
    seen: set[str] = set()
    ordered: list[str] = []
    for ref in refs:
        if ref not in seen:
            seen.add(ref)
            ordered.append(ref)
    return ordered


def build_pr_closing_issue_lines(pr_development_issue: str | None) -> list[str]:
    return [f"Closes {ref}" for ref in parse_issue_refs(pr_development_issue)]


def extract_pr_closing_issue_lines(body_markdown: str) -> list[str]:
    lines: list[str] = []
    for raw in body_markdown.splitlines():
        stripped = raw.strip()
        if PR_CLOSING_ISSUE_LINE_RE.fullmatch(stripped):
            lines.append(stripped)
    return lines


def build_canonical_issue_link_lines(fields: dict[str, str], source_log_rel: str) -> list[str]:
    lines = [f"- Log: `{source_log_rel}`"]
    for key, label in [
        ("runbook", "Runbook"),
        ("roadmap", "Roadmap"),
        ("parent_log", "Parent log"),
        ("previous_log", "Previous log"),
    ]:
        value = str(fields.get(key) or "").strip()
        if value:
            lines.append(f"- {label}: `{value}`")
    return lines


def validate_pr_body_contract(*, body_markdown: str, source_log_text: str, pr_development_issue: str | None) -> PrBodyContractResult:
    checks: list[ContractCheck] = []
    warnings: list[str] = []
    sections = _parse_sections(body_markdown)
    section_order = extract_section_order(body_markdown)

    missing = [name for name in PR_REQUIRED_SECTIONS if name not in sections]
    if missing:
        checks.append(ContractCheck("required-pr-sections", "fail", f"missing required PR sections: {missing}"))
    else:
        checks.append(ContractCheck("required-pr-sections", "pass", "required PR sections are present"))

    order_status, order_details = _validate_order(section_order, PR_REQUIRED_SECTIONS, PR_OPTIONAL_SECTIONS)
    checks.append(ContractCheck("pr-section-order", order_status, order_details))

    metadata_lines = sections.get("Metadata", [])
    if bullets_are_contiguous(metadata_lines):
        checks.append(ContractCheck("metadata-row-shape", "pass", "metadata bullet rows are contiguous"))
    else:
        checks.append(ContractCheck("metadata-row-shape", "fail", "metadata bullet rows contain blank gaps or non-bullet content"))

    link_lines = [line.strip() for line in sections.get("Links", []) if line.strip().startswith("- ")]
    links_ok, invalid_links = link_labels_are_allowed(link_lines, PR_ALLOWED_LINK_LABELS)
    if links_ok:
        checks.append(ContractCheck("pr-link-categories", "pass", "PR Links section uses only allowed link categories"))
    else:
        checks.append(ContractCheck("pr-link-categories", "fail", f"PR Links section contains invalid rows: {invalid_links}"))

    try:
        expected_evidence_lines = extract_evidence_footer_source_lines(source_log_text)
        source_valid, invalid_source_lines = validate_evidence_footer_source_lines(expected_evidence_lines)
    except Exception as exc:
        expected_evidence_lines = []
        source_valid = False
        invalid_source_lines = [str(exc)]

    if not source_valid:
        checks.append(ContractCheck("evidence-footer-source-shape", "fail", f"invalid Evidence Footer Source rows: {invalid_source_lines}"))
    elif expected_evidence_lines:
        checks.append(ContractCheck("evidence-footer-source-shape", "pass", "Evidence Footer Source rows match the canonical line shape"))
    else:
        checks.append(ContractCheck("evidence-footer-source-shape", "pass", "no Evidence Footer Source rows were provided"))

    rendered_footer_lines = [line.strip()[2:].strip() for line in sections.get("Evidence Footer", []) if line.strip().startswith("- ")]
    rendered_scope_kind, rendered_scope_refs = _extract_rendered_checklist_scope(sections.get("Execution Checklist", []))
    scoped_expected_evidence_lines = _filter_evidence_footer_lines_for_scope(expected_evidence_lines, rendered_scope_kind, rendered_scope_refs)
    evidence_footer_eligible = pr_body_is_evidence_footer_eligible(source_log_text)
    if expected_evidence_lines and not evidence_footer_eligible:
        checks.append(ContractCheck("evidence-footer-eligibility", "fail", "Evidence Footer Source is present but the source log is not drills/evidence eligible"))
    elif rendered_footer_lines and not evidence_footer_eligible:
        checks.append(ContractCheck("evidence-footer-eligibility", "fail", "Evidence Footer is rendered but the source log is not drills/evidence eligible"))
    else:
        checks.append(ContractCheck("evidence-footer-eligibility", "pass", "Evidence Footer eligibility matches the source log tags/labels contract"))

    if scoped_expected_evidence_lines:
        if "Evidence Footer" not in sections:
            checks.append(ContractCheck("evidence-footer-presence", "fail", "Evidence Footer Source exists but the rendered Evidence Footer section is missing"))
        elif rendered_footer_lines != scoped_expected_evidence_lines:
            checks.append(ContractCheck("evidence-footer-presence", "fail", f"rendered Evidence Footer rows do not match source rows: {rendered_footer_lines}"))
        else:
            checks.append(ContractCheck("evidence-footer-presence", "pass", "rendered Evidence Footer rows match the source block exactly"))
    elif expected_evidence_lines and "Evidence Footer" in sections:
        checks.append(ContractCheck("evidence-footer-presence", "fail", "Evidence Footer section must be omitted when no source rows match the rendered checklist scope"))
    elif "Evidence Footer" in sections:
        checks.append(ContractCheck("evidence-footer-presence", "fail", "Evidence Footer section must be omitted when no Evidence Footer Source rows exist"))
    else:
        checks.append(ContractCheck("evidence-footer-presence", "pass", "Evidence Footer section is omitted when the source block is absent"))

    footer_valid, invalid_footer_lines = validate_evidence_footer_source_lines(rendered_footer_lines)
    if not footer_valid:
        checks.append(ContractCheck("evidence-footer-line-shape", "fail", f"Evidence Footer rows do not match the canonical line shape: {invalid_footer_lines}"))
    elif rendered_footer_lines:
        checks.append(ContractCheck("evidence-footer-line-shape", "pass", "Evidence Footer rows match the canonical line shape"))
    else:
        checks.append(ContractCheck("evidence-footer-line-shape", "pass", "no Evidence Footer rows were rendered"))

    if "Development Link" in sections:
        checks.append(ContractCheck("development-link-presence", "fail", "Development Link section is no longer allowed in canonical PR bodies"))
    elif pr_development_issue:
        checks.append(ContractCheck("development-link-presence", "pass", "Development issue is tracked only through Metadata as required"))
    else:
        checks.append(ContractCheck("development-link-presence", "pass", "Development Link section is correctly omitted"))

    expected_closing_lines = build_pr_closing_issue_lines(pr_development_issue)
    rendered_closing_lines = extract_pr_closing_issue_lines(body_markdown)
    if expected_closing_lines:
        if rendered_closing_lines != expected_closing_lines:
            checks.append(ContractCheck("github-development-linkage", "fail", f"GitHub closing-link footer does not match the development issue set: {rendered_closing_lines}"))
        else:
            checks.append(ContractCheck("github-development-linkage", "pass", "GitHub closing-link footer matches the development issue set"))
    elif rendered_closing_lines:
        checks.append(ContractCheck("github-development-linkage", "fail", "GitHub closing-link footer must be omitted when no development issue is defined"))
    else:
        checks.append(ContractCheck("github-development-linkage", "pass", "GitHub closing-link footer is correctly omitted"))

    status = "pass" if all(check.status != "fail" for check in checks) else "fail"
    return PrBodyContractResult(
        status=status,
        checks=checks,
        warnings=warnings,
        expected_evidence_footer_lines=scoped_expected_evidence_lines,
    )


def render_checks_payload(result: PrBodyContractResult) -> dict:
    return {
        "status": result.status,
        "warnings": list(result.warnings),
        "expected_evidence_footer_lines": list(result.expected_evidence_footer_lines),
        "checks": [asdict(check) for check in result.checks],
    }