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