from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from gen_issue_draft import _parse_fields, _parse_sections


PR_REQUIRED_SECTIONS = ["Metadata", "Summary", "Execution Checklist", "Links"]
PR_OPTIONAL_SECTIONS = ["Evidence Footer", "Development Link"]
ISSUE_REQUIRED_SECTIONS = ["Metadata", "Context", "Definition of Done (DoD)", "Links"]
PR_ALLOWED_LINK_LABELS = {"Log", "Issue", "Runbook", "Evidence artifact", "Parent log", "Roadmap"}
ISSUE_ALLOWED_LINK_LABELS = {"Log", "Runbook", "Parent log", "Roadmap"}
EVIDENCE_FOOTER_LINE_RE = re.compile(r"^`(?P<stage>[^`]+)` \| artifact: `(?P<artifact>[^`]+)`$")
LINK_LINE_RE = re.compile(r"^- (?P<label>[^:]+):\s+`[^`]*`$")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
SENTENCE_TERMINATOR_RE = re.compile(r"[.!?]")
VERSION_SUFFIX_RE = re.compile(r"\s+v\d+\s*$", re.IGNORECASE)
INLINE_CODE_RE = re.compile(r"`([^`]*)`")
SECTION_PHASE_PREFIX_RE = re.compile(r"^`?P\d+(?:-C\d+(?:-S\d+(?:S\d+)*)?)?`?:\s*")
LOG_ID_FROM_PATH_RE = re.compile(r"log-(?P<id>[A-Z0-9]+(?:-[A-Z0-9]+)*)-")
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

    for raw in section_lines:
        stripped = raw.strip()
        if stripped == "**PR summary bullets**:":
            current = "summary"
            continue
        if stripped in {"**PR links**:", "**PR links / evidence footer**:"}:
            current = "links"
            continue
        if stripped == "**Evidence Footer Source**:":
            current = "evidence-footer-source"
            continue
        if stripped.startswith("**") and stripped.endswith(":"):
            current = None
            continue
        if not stripped.startswith("- "):
            continue
        value = stripped[2:].strip()
        if current == "summary":
            summary_bullets.append(value)
        elif current == "links":
            link_lines.append(value)
        elif current == "evidence-footer-source":
            evidence_footer_source_lines.append(value)

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
    fields = _parse_fields(source_log_text)
    parent_log = str(fields.get("parent_log") or "").strip()
    return 5 if not parent_log else 4


def _issue_context_scope_label(source_log_text: str) -> str:
    return "main" if issue_body_expected_context_line_count(source_log_text) == 5 else "child"


def _strip_markdown(text: str) -> str:
    plain = INLINE_CODE_RE.sub(r"\1", text)
    plain = plain.replace("**", "")
    plain = plain.replace("->", " to ")
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


def _format_pr_refs(merged_pr_numbers: list[int] | None) -> str:
    refs = [f"#{number}" for number in merged_pr_numbers or []]
    if not refs:
        return "the merged PR evidence"
    if len(refs) == 1:
        return refs[0]
    if len(refs) == 2:
        return f"{refs[0]} and {refs[1]}"
    return ", ".join(refs[:-1]) + f", and {refs[-1]}"


def issue_body_expected_context_anchors(source_log_text: str) -> list[str]:
    fields = _parse_fields(source_log_text)
    requested_id = str(fields.get("id") or "").strip()
    subject = _normalize_title_subject(str(fields.get("title") or requested_id))
    anchors = [anchor for anchor in [requested_id, subject] if anchor]
    previous_id = _extract_follow_up_id(str(fields.get("previous_log") or ""))
    if previous_id and _issue_context_scope_label(source_log_text) == "child":
        anchors.append(previous_id)
    return anchors


def build_issue_draft_context_lines(source_log_text: str) -> list[str]:
    fields = _parse_fields(source_log_text)
    requested_id = str(fields.get("id") or "this log").strip() or "this log"
    subject = _normalize_title_subject(str(fields.get("title") or requested_id))
    previous_id = _extract_follow_up_id(str(fields.get("previous_log") or ""))
    focus_phrases = _english_focus_candidates(source_log_text)

    if _issue_context_scope_label(source_log_text) == "main":
        lines = [
            _sentence_bullet(f"This issue was opened to track the main {requested_id} contract for {subject}"),
            _sentence_bullet("It acts as the parent S0E spine that keeps downstream child slices aligned to one shared delivery record"),
            _sentence_bullet(_focus_to_sentence("primary", focus_phrases[0]) if focus_phrases else f"The source log centers this spine on {subject}"),
            _sentence_bullet(_focus_to_sentence("secondary", focus_phrases[1]) if len(focus_phrases) > 1 else "Child slices inherit this parent context before they branch into narrower implementation work"),
            _sentence_bullet(f"Completion for this parent issue depends on linked delivery evidence and the final DoD recorded for {requested_id}"),
        ]
        return lines

    follow_up_sentence = (
        f"It follows {previous_id} under the parent S0E spine, so this child log carries a narrower delivery boundary"
        if previous_id
        else "It sits under the parent S0E spine as a child log with its own narrower delivery boundary"
    )
    lines = [
        _sentence_bullet(f"This issue was opened to track the {requested_id} slice for {subject}"),
        _sentence_bullet(follow_up_sentence),
        _sentence_bullet(_focus_to_sentence("primary", focus_phrases[0]) if focus_phrases else f"The source log focuses this slice on {subject} work within the current S0E chain"),
        _sentence_bullet(_focus_to_sentence("secondary", focus_phrases[1]) if len(focus_phrases) > 1 else f"Completion for this issue depends on the linked delivery evidence and the final DoD recorded for {requested_id}"),
    ]
    return lines


def build_issue_conclusion_context_lines(source_log_text: str, merged_pr_numbers: list[int] | None = None) -> list[str]:
    fields = _parse_fields(source_log_text)
    requested_id = str(fields.get("id") or "this log").strip() or "this log"
    subject = _normalize_title_subject(str(fields.get("title") or requested_id))
    previous_id = _extract_follow_up_id(str(fields.get("previous_log") or ""))
    focus_phrases = _english_focus_candidates(source_log_text)
    merged_pr_refs = _format_pr_refs(merged_pr_numbers)

    if _issue_context_scope_label(source_log_text) == "main":
        lines = [
            _sentence_bullet(f"This issue was opened to track the main {requested_id} contract for {subject}"),
            _sentence_bullet("It serves as the parent S0E spine that keeps downstream child slices attached to one shared delivery record"),
            _sentence_bullet(_focus_to_sentence("primary", focus_phrases[0]) if focus_phrases else f"The source log centers this spine on {subject}"),
            _sentence_bullet(f"The merged PR evidence now shows that {merged_pr_refs} completed the planned delivery recorded for this parent scope"),
            _sentence_bullet(f"The closed issue now preserves the finished parent record for {subject} and downstream child-log traceability"),
        ]
        return lines

    follow_up_sentence = (
        f"It follows {previous_id} under the parent S0E spine, so this child log carries a narrower delivery boundary"
        if previous_id
        else "It sits under the parent S0E spine as a child log with its own narrower delivery boundary"
    )
    outcome_sentence = f"The closed issue now records the finished {subject} path for downstream S0E follow-up"
    lines = [
        _sentence_bullet(f"This issue was opened to track the {requested_id} slice for {subject}"),
        _sentence_bullet(follow_up_sentence),
        _sentence_bullet(f"The merged PR evidence now shows that {merged_pr_refs} completed the planned delivery for this slice"),
        _sentence_bullet(outcome_sentence),
    ]
    return lines


def extract_issue_context_bullet_lines(section_lines: list[str]) -> list[str]:
    return [line.strip() for line in section_lines if line.strip().startswith("- ")]


def validate_issue_context_lines(section_lines: list[str], expected_line_count: int, source_log_text: str | None = None) -> tuple[bool, str, list[str]]:
    trimmed = [line.strip() for line in section_lines if line.strip()]
    bullet_lines = [line for line in trimmed if line.startswith("- ")]
    invalid_lines: list[str] = []

    if len(trimmed) != len(bullet_lines):
        return False, "Context contains non-bullet content or blank-gap drift", invalid_lines
    if len(bullet_lines) != expected_line_count:
        return False, f"Context must contain exactly {expected_line_count} English bullet sentences; found {len(bullet_lines)}", invalid_lines

    for raw in bullet_lines:
        sentence = raw[2:].strip()
        if not sentence:
            invalid_lines.append(raw)
            continue
        if CJK_RE.search(sentence) or not re.search(r"[A-Za-z]", sentence):
            invalid_lines.append(raw)
            continue
        if not re.search(r"[.!?]$", sentence):
            invalid_lines.append(raw)
            continue
        if len(SENTENCE_TERMINATOR_RE.findall(sentence)) != 1:
            invalid_lines.append(raw)

    if invalid_lines:
        return False, "Context lines must each be one English sentence on one bullet row", invalid_lines

    if source_log_text:
        joined = " ".join(bullet_lines).lower()
        missing_anchors = [anchor for anchor in issue_body_expected_context_anchors(source_log_text) if anchor.lower() not in joined]
        if missing_anchors:
            return False, f"Context must mention source-log-specific anchors: {missing_anchors}", bullet_lines

    return True, f"Context contains exactly {expected_line_count} one-sentence English bullet rows with source-log-specific anchors", invalid_lines


def pr_body_is_evidence_footer_eligible(source_log_text: str) -> bool:
    fields = _parse_fields(source_log_text)
    tags = str(fields.get("tags") or "").lower()
    pr_labels = str(fields.get("pr_labels") or "").lower()
    title = str(fields.get("title") or "").lower()
    return any(token in tags or token in pr_labels or token in title for token in ["drills", "evidence"])


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
    evidence_footer_eligible = pr_body_is_evidence_footer_eligible(source_log_text)
    if expected_evidence_lines and not evidence_footer_eligible:
        checks.append(ContractCheck("evidence-footer-eligibility", "fail", "Evidence Footer Source is present but the source log is not drills/evidence eligible"))
    elif rendered_footer_lines and not evidence_footer_eligible:
        checks.append(ContractCheck("evidence-footer-eligibility", "fail", "Evidence Footer is rendered but the source log is not drills/evidence eligible"))
    else:
        checks.append(ContractCheck("evidence-footer-eligibility", "pass", "Evidence Footer eligibility matches the source log tags/labels contract"))

    if expected_evidence_lines:
        if "Evidence Footer" not in sections:
            checks.append(ContractCheck("evidence-footer-presence", "fail", "Evidence Footer Source exists but the rendered Evidence Footer section is missing"))
        elif rendered_footer_lines != expected_evidence_lines:
            checks.append(ContractCheck("evidence-footer-presence", "fail", f"rendered Evidence Footer rows do not match source rows: {rendered_footer_lines}"))
        else:
            checks.append(ContractCheck("evidence-footer-presence", "pass", "rendered Evidence Footer rows match the source block exactly"))
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

    if pr_development_issue:
        if "Development Link" not in sections:
            checks.append(ContractCheck("development-link-presence", "fail", "Development Link section is required when a development issue exists"))
        else:
            checks.append(ContractCheck("development-link-presence", "pass", "Development Link section is present for the development issue"))
    elif "Development Link" in sections:
        checks.append(ContractCheck("development-link-presence", "fail", "Development Link section must be omitted when no development issue exists"))
    else:
        checks.append(ContractCheck("development-link-presence", "pass", "Development Link section is correctly omitted"))

    status = "pass" if all(check.status != "fail" for check in checks) else "fail"
    return PrBodyContractResult(
        status=status,
        checks=checks,
        warnings=warnings,
        expected_evidence_footer_lines=expected_evidence_lines,
    )


def render_checks_payload(result: PrBodyContractResult) -> dict:
    return {
        "status": result.status,
        "warnings": list(result.warnings),
        "expected_evidence_footer_lines": list(result.expected_evidence_footer_lines),
        "checks": [asdict(check) for check in result.checks],
    }