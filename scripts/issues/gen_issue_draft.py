from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


SCOPE_LABELS = {
    "S0": "s0/knowledge system",
    "S1": "s1/sot",
    "S2": "s2/projection",
    "S3": "s3/observability",
    "S4": "s4/ops",
    "S5": "s5/security governance",
    "S6": "s6/evidence & drills",
}

FIELD_RE = re.compile(r"^\s*\*\*([^*]+)\*\*:\s*`(.*)`\s*$")
VERSION_SUFFIX_RE = re.compile(r"\s+v\d+\s*$", re.IGNORECASE)
DEFAULT_WORKSPACE_PROJECT = "wordloom Board"
DEFAULT_COMMAND_TIMEOUT_SECONDS = 180


@dataclass
class IssueDraftResult:
    mode: str
    result: str
    log_path: str
    draft_path: str
    title: str
    top_labels: list[str]
    scope_labels: list[str]
    function_labels: list[str]
    module_labels: list[str]
    issue_projects: list[str]
    milestone: str | None
    parent_issue: str | None
    body_markdown: str
    warnings: list[str]
    issue_number: int | None = None
    issue_url: str | None = None
    created_at: str | None = None


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate issue draft markdown from a structured log")
    parser.add_argument("log_path", help="Path to the source log markdown file")
    parser.add_argument("--output-path", dest="output_path", help="Override output markdown path")
    parser.add_argument("--result-path", dest="result_path", help="Override structured result JSON path")
    parser.add_argument("--parent-issue", dest="parent_issue", help="Override parent issue URL/number")
    parser.add_argument("--milestone-override", dest="milestone_override", help="Override milestone")
    parser.add_argument(
        "--module-label-override",
        dest="module_label_overrides",
        action="append",
        help="Repeatable module label override; can also be a comma-separated list",
    )
    parser.add_argument(
        "--strict-label-check",
        dest="strict_label_check",
        action="store_true",
        help="Fail if derived labels are empty or malformed",
    )
    parser.add_argument("--repo", dest="repo", help="Repository slug for future create mode")
    parser.add_argument(
        "--create",
        dest="create_issue",
        action="store_true",
        help="Reserved for P2 create-issue mode; not implemented in P1",
    )
    return parser.parse_args()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _repo_rel(path: Path) -> str:
    return path.relative_to(_repo_root()).as_posix()


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _run_command(command: list[str], *, timeout_seconds: int = DEFAULT_COMMAND_TIMEOUT_SECONDS) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            text=True,
            capture_output=True,
            encoding="utf-8",
            stdin=subprocess.DEVNULL,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        rendered_command = " ".join(command)
        raise SystemExit(f"Command timed out after {timeout_seconds}s: {rendered_command}") from exc


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = FIELD_RE.match(line)
        if match:
            fields[match.group(1).strip()] = match.group(2)
    return fields


def _parse_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def _split_csv(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def _derive_sub_label(log_id: str) -> str:
    return "sub/1" if "-" in log_id else "sub/0"


def _normalize_specific_subject(title: str) -> str:
    text = title.strip()
    text = VERSION_SUFFIX_RE.sub("", text)
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"（[^）]*）", "", text)
    text = re.sub(r"\s*\+\s*drills/evidence\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*\+\s*evidence/drills\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*\+\s*drills\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*\+\s*", " and ", text)
    text = re.sub(r"\s+", " ", text).strip(" -")
    return text


def _infer_keyword(fields: dict[str, str], title: str, tags: list[str], section_text: str) -> str:
    explicit = fields.get("issue_keyword", "").strip()
    if explicit:
        return explicit

    haystack = " ".join([title, section_text, " ".join(tags)]).lower()
    checks = [
        ("evidence", ["evidence json", "self-explaining artifacts", " evidence ", " artifacts "]),
        ("enforcement", ["enforcement", "hard-stop", " hard gate", " hard-gate", "controlled exception"]),
        ("automation", ["automation", "github actions", "dispatch", "orchestration"]),
        ("runtime", ["runtime", "worker", "process"]),
        ("migration", ["migration", "cutover", "backfill", "transition"]),
        ("workflow", ["workflow", "operator path", "step sequence"]),
        ("authority", ["authority", "approver", "rollback authority"]),
        ("policy", ["policy", "default strategy", "allow", "forbid"]),
        ("records", ["ledger", "records", "record", "auditability"]),
        ("contract", ["contract", "mapping", "schema", "taxonomy", "fields"]),
    ]

    for keyword, needles in checks:
        if any(needle in haystack for needle in needles):
            return keyword
    return "contract"


def _extract_decision_bullets(lines: list[str]) -> list[str]:
    bullets: list[str] = []
    in_decision = False
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("**Decision"):
            in_decision = True
            continue
        if in_decision and line.startswith("**"):
            break
        stripped = line.strip()
        if in_decision and stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
    return bullets


def _extract_bullets(lines: list[str]) -> list[str]:
    bullets: list[str] = []
    for raw in lines:
        stripped = raw.strip()
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
    return bullets


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


def _derive_top_labels(fields: dict[str, str], tags: list[str]) -> list[str]:
    explicit = _split_csv(fields.get("issue_top_labels"))
    if explicit:
        return explicit
    return [tag for tag in tags if tag.isupper()]


def _derive_scope_labels(fields: dict[str, str], log_id: str, scope: str) -> list[str]:
    explicit = _split_csv(fields.get("issue_scope_labels"))
    if explicit:
        return explicit
    labels: list[str] = []
    mapped = SCOPE_LABELS.get(scope)
    if mapped:
        labels.append(mapped)
    labels.append(_derive_sub_label(log_id))
    return labels


def _derive_function_labels(title: str, tags: list[str], sections: dict[str, list[str]]) -> list[str]:
    haystack = " ".join([title, " ".join(tags)]).lower()
    labels: list[str] = []
    if "drills" in haystack or "drill" in haystack or "evidence" in haystack:
        labels.append("drills")
    elif _section_has_substantive_evidence(sections.get("Evidence", [])):
        labels.append("drills")
    return labels


def _derive_module_labels(fields: dict[str, str], overrides: list[str]) -> list[str]:
    explicit = _split_csv(fields.get("issue_module_labels"))
    return explicit + overrides


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _normalize_override_list(raw_values: list[str] | None) -> list[str]:
    values: list[str] = []
    for raw in raw_values or []:
        values.extend(_split_csv(raw))
    return values


def _derive_issue_projects(fields: dict[str, str], log_rel_path: str) -> list[str]:
    explicit = _split_csv(fields.get("issue_projects"))
    if explicit:
        return explicit
    if log_rel_path.startswith("docs/logs/"):
        return [DEFAULT_WORKSPACE_PROJECT]
    return []


def _derive_milestone(fields: dict[str, str], milestone_override: str | None) -> tuple[str | None, list[str]]:
    warnings: list[str] = []
    if milestone_override:
        return milestone_override, warnings

    explicit = fields.get("issue_milestone", "").strip()
    if explicit:
        return explicit, warnings

    roadmap_path = fields.get("roadmap_path", "").strip()
    roadmap_milestone = fields.get("roadmap_milestone", "").strip()
    roadmap_phase = fields.get("roadmap_phase", "").strip()
    if roadmap_path and roadmap_milestone and roadmap_phase:
        warnings.append("issue_milestone derived from exact roadmap bridge metadata")
        return roadmap_milestone, warnings

    if roadmap_path or roadmap_milestone or roadmap_phase:
        warnings.append("roadmap bridge metadata incomplete; issue_milestone left blank")
    return None, warnings


def _normalize_issue_reference(value: str | None) -> str | None:
    if not value:
        return None
    text = value.strip()
    if not text:
        return None
    match = re.search(r"(?:/issues/|^#?)(\d+)$", text)
    if match:
        return f"#{match.group(1)}"
    return text


def _resolve_parent_issue(repo_root: Path, fields: dict[str, str], override: str | None) -> tuple[str | None, bool, list[str]]:
    warnings: list[str] = []
    explicit_parent = (override or fields.get("issue_parent") or "").strip()
    parent_log_path = fields.get("parent_log", "").strip()
    show_parent_issue = bool(explicit_parent or parent_log_path)

    if explicit_parent:
        return _normalize_issue_reference(explicit_parent), show_parent_issue, warnings

    if not parent_log_path:
        return None, False, warnings

    parent_log = repo_root / Path(parent_log_path)
    if not parent_log.is_file():
        warnings.append("parent_log path missing; issue_parent left blank")
        return None, True, warnings

    parent_fields = _parse_fields(_load_text(parent_log))
    parent_issue = _normalize_issue_reference(parent_fields.get("issue", ""))
    if parent_issue:
        warnings.append("issue_parent derived from parent log issue link")
        return parent_issue, True, warnings

    warnings.append("parent_log issue link missing; issue_parent left blank")
    return None, True, warnings


def _build_links(fields: dict[str, str], log_rel_path: str) -> list[str]:
    lines = [f"- Log: `{log_rel_path}`"]
    for key, label in [
        ("runbook", "Runbook"),
        ("roadmap", "Roadmap"),
        ("parent_log", "Parent log"),
    ]:
        value = fields.get(key, "").strip()
        if value:
            lines.append(f"- {label}: `{value}`")
    return lines


def _render_issue_markdown(
    *,
    title: str,
    labels: list[str],
    issue_projects: list[str],
    milestone: str | None,
    source_log: str,
    parent_issue: str | None,
    show_parent_issue: bool,
    link_lines: list[str],
    context_lines: list[str],
) -> str:
    lines = [
        "## Metadata",
        "",
        f"- Labels: {', '.join(f'`{label}`' for label in labels) if labels else '``'}",
        f"- Projects: `{', '.join(issue_projects)}`",
        f"- Milestone: `{milestone or ''}`",
        f"- Source log: `{source_log}`",
    ]
    if show_parent_issue:
        lines.append(f"- Parent issue: {parent_issue or ''}")
    lines.extend([
        "",
        "## Context",
        "",
        *context_lines,
        "",
        "## Definition of Done (DoD)",
        "",
        "## Links",
        "",
        *link_lines,
        "",
    ])
    return "\n".join(lines)


def _validate_labels(labels: list[str], strict: bool) -> None:
    if not strict:
        return
    if not labels:
        raise SystemExit("strict label check failed: no labels derived")
    for label in labels:
        if not label.strip():
            raise SystemExit("strict label check failed: blank label found")


def _require_gh_cli() -> None:
    if shutil.which("gh") is None:
        raise SystemExit("gh CLI is required for create-issue mode but was not found in PATH")


def _derive_repo_slug(explicit_repo: str | None) -> str:
    if explicit_repo:
        return explicit_repo

    remote_cmd = _run_command(["git", "-C", str(_repo_root()), "config", "--get", "remote.origin.url"])
    remote = remote_cmd.stdout.strip()
    if remote_cmd.returncode != 0 or not remote:
        raise SystemExit("Could not determine repository slug from remote.origin.url; use --repo")

    match = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$", remote)
    if not match:
        raise SystemExit("Could not parse GitHub repository slug from remote.origin.url; use --repo")
    return f"{match.group('owner')}/{match.group('repo')}"


def _require_gh_auth() -> None:
    auth = _run_command(["gh", "auth", "status"])
    if auth.returncode != 0:
        raise SystemExit("gh auth status failed; authenticate GitHub CLI before using --create")


def _fetch_existing_labels(repo: str) -> set[str]:
    cmd = _run_command(["gh", "label", "list", "--repo", repo, "--limit", "200", "--json", "name"])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to list labels for {repo}: {cmd.stderr.strip()}")
    try:
        data = json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse label list JSON: {exc}") from exc
    return {item.get('name', '').strip() for item in data if isinstance(item, dict)}


def _fetch_existing_milestones(repo: str) -> set[str]:
    cmd = _run_command(["gh", "api", f"repos/{repo}/milestones", "--paginate"])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to list milestones for {repo}: {cmd.stderr.strip()}")
    try:
        data = json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse milestone JSON: {exc}") from exc
    return {item.get('title', '').strip() for item in data if isinstance(item, dict)}


def _ensure_title_not_already_used(repo: str, title: str) -> None:
    cmd = _run_command([
        "gh",
        "issue",
        "list",
        "--repo",
        repo,
        "--search",
        f'{title} in:title',
        "--limit",
        "20",
        "--json",
        "title,number,url",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to search existing issues for duplicate title: {cmd.stderr.strip()}")
    try:
        data = json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse issue search JSON: {exc}") from exc
    for item in data:
        if isinstance(item, dict) and item.get("title") == title:
            raise SystemExit(f"Issue with title already exists: #{item.get('number')} {item.get('url')}")


def _create_issue(
    *,
    repo: str,
    title: str,
    body_path: Path,
    labels: list[str],
    projects: list[str],
    milestone: str | None,
) -> tuple[int, str]:
    command = [
        "gh",
        "issue",
        "create",
        "--repo",
        repo,
        "--title",
        title,
        "--body-file",
        str(body_path),
    ]
    for label in labels:
        command.extend(["--label", label])
    for project in projects:
        command.extend(["--project", project])
    if milestone:
        command.extend(["--milestone", milestone])

    result = _run_command(command)
    if result.returncode != 0:
        raise SystemExit(f"gh issue create failed: {result.stderr.strip()}")
    issue_url = result.stdout.strip().splitlines()[-1].strip()
    match = re.search(r"/(\d+)$", issue_url)
    if not match:
        raise SystemExit(f"Could not parse issue number from URL: {issue_url}")
    return int(match.group(1)), issue_url


def generate_issue_draft(args: argparse.Namespace, *, emit_result: bool = True) -> IssueDraftResult:
    repo_root = _repo_root()
    log_path = (repo_root / args.log_path).resolve() if not Path(args.log_path).is_absolute() else Path(args.log_path)
    if not log_path.is_file():
        raise SystemExit(f"Log file not found: {log_path}")

    text = _load_text(log_path)
    fields = _parse_fields(text)
    sections = _parse_sections(text)

    log_id = fields.get("id", log_path.stem.replace("log-", ""))
    log_title = fields.get("title", log_id)
    scope = fields.get("scope", "")
    tags = _split_csv(fields.get("tags"))
    section_text = "\n".join(text for lines in sections.values() for text in lines)

    keyword = _infer_keyword(fields, log_title, tags, section_text)
    specific_subject = _normalize_specific_subject(log_title)
    issue_title = f"{log_id}: {keyword}/{specific_subject}"

    top_labels = _derive_top_labels(fields, tags)
    scope_labels = _derive_scope_labels(fields, log_id, scope)
    function_labels = _derive_function_labels(log_title, tags, sections)
    module_labels = _derive_module_labels(fields, _normalize_override_list(args.module_label_overrides))
    all_labels = _dedupe(top_labels + scope_labels + function_labels + module_labels)
    _validate_labels(all_labels, args.strict_label_check)

    milestone, milestone_warnings = _derive_milestone(fields, args.milestone_override)
    parent_issue, show_parent_issue, parent_warnings = _resolve_parent_issue(repo_root, fields, args.parent_issue)

    warnings: list[str] = []
    warnings.extend(milestone_warnings)
    warnings.extend(parent_warnings)
    if not fields.get("issue_keyword"):
        warnings.append("issue_keyword inferred from source log content")
    if not module_labels:
        warnings.append("module labels left blank")
    if not milestone:
        warnings.append("issue_milestone missing")
    if show_parent_issue and not parent_issue:
        warnings.append("issue_parent missing")
    warnings.append("Context now uses the canonical source-log-derived natural-summary block for issue-body review")
    warnings.append("Definition of Done (DoD) remains intentionally blank pending operator input")

    rel_log_path = _repo_rel(log_path)
    link_lines = _build_links(fields, rel_log_path)
    issue_projects = _derive_issue_projects(fields, rel_log_path)
    from body_contract import build_issue_draft_context_lines

    default_output = repo_root / "docs" / "issues" / f"issue-{log_path.stem.removeprefix('log-')}.md"
    output_path = Path(args.output_path) if args.output_path else default_output
    if not output_path.is_absolute():
        output_path = repo_root / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    result_path = Path(args.result_path) if args.result_path else output_path.with_suffix(".json")
    if not result_path.is_absolute():
        result_path = repo_root / result_path
    result_path.parent.mkdir(parents=True, exist_ok=True)

    markdown = _render_issue_markdown(
        title=issue_title,
        labels=all_labels,
        issue_projects=issue_projects,
        milestone=milestone,
        source_log=rel_log_path,
        parent_issue=parent_issue,
        show_parent_issue=show_parent_issue,
        link_lines=link_lines,
        context_lines=build_issue_draft_context_lines(text),
    )
    output_path.write_text(markdown, encoding="utf-8")

    result = IssueDraftResult(
        mode="create-issue" if args.create_issue else "draft-generation",
        result="ok",
        log_path=rel_log_path,
        draft_path=_repo_rel(output_path),
        title=issue_title,
        top_labels=top_labels,
        scope_labels=scope_labels,
        function_labels=function_labels,
        module_labels=module_labels,
        issue_projects=issue_projects,
        milestone=milestone,
        parent_issue=parent_issue,
        body_markdown=markdown,
        warnings=warnings,
    )

    if args.create_issue:
        _require_gh_cli()
        _require_gh_auth()
        repo = _derive_repo_slug(args.repo)
        existing_labels = _fetch_existing_labels(repo)
        missing_labels = [label for label in all_labels if label not in existing_labels]
        if missing_labels:
            raise SystemExit(f"Missing pre-created labels in {repo}: {', '.join(missing_labels)}")

        if milestone:
            milestones = _fetch_existing_milestones(repo)
            if milestone not in milestones:
                raise SystemExit(f"Milestone does not exist in {repo}: {milestone}")

        _ensure_title_not_already_used(repo, issue_title)
        issue_number, issue_url = _create_issue(
            repo=repo,
            title=issue_title,
            body_path=output_path,
            labels=all_labels,
            projects=issue_projects,
            milestone=milestone,
        )
        result.issue_number = issue_number
        result.issue_url = issue_url
        result.created_at = _utc_now()
        warnings.append("source log write-back not performed; update links.issue in a later tracked docs change")

    result_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    if emit_result:
        print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        generate_issue_draft(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())