from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-not-found]


@dataclass(frozen=True)
class ValidationError:
    message: str


def _repo_root() -> Path:
    # backend/scripts/ci/validate_scenario_catalog.py -> repo root is parents[3]
    return Path(__file__).resolve().parents[3]


def _load_yaml(path: Path) -> Any:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SystemExit(f"file not found: {path}") from exc

    try:
        return yaml.safe_load(raw)
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"failed to parse yaml: {path}: {exc}") from exc


_SEGMENT_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def _validate_catalog(catalog_path: Path) -> tuple[set[str], list[ValidationError]]:
    errors: list[ValidationError] = []

    catalog = _load_yaml(catalog_path)
    if not isinstance(catalog, dict):
        return set(), [ValidationError("catalog root must be a mapping")]

    scenarios = catalog.get("scenarios")
    if not isinstance(scenarios, list):
        return set(), [ValidationError("catalog must contain a 'scenarios' list")]

    ids: list[str] = []
    aliases_all: list[str] = []

    for idx, item in enumerate(scenarios):
        if not isinstance(item, dict):
            errors.append(ValidationError(f"catalog.scenarios[{idx}] must be a mapping"))
            continue

        scenario_id = item.get("id")
        if not isinstance(scenario_id, str) or not scenario_id.strip():
            errors.append(ValidationError(f"catalog.scenarios[{idx}].id must be a non-empty string"))
            continue

        ids.append(scenario_id)

        segments = scenario_id.split("/")
        if len(segments) != 3 or not all(_SEGMENT_RE.match(seg or "") for seg in segments):
            errors.append(
                ValidationError(
                    "invalid scenario id format (expected intent/pipeline/topic with [a-z0-9_]): "
                    + scenario_id
                )
            )

        cli = item.get("cli")
        if not isinstance(cli, str) or not cli.strip():
            errors.append(ValidationError(f"scenario '{scenario_id}' must have non-empty 'cli'"))

        aliases = item.get("aliases")
        if aliases is None:
            continue
        if not isinstance(aliases, list) or not all(isinstance(a, str) and a.strip() for a in aliases):
            errors.append(ValidationError(f"scenario '{scenario_id}' aliases must be a list of non-empty strings"))
            continue

        aliases_all.extend([a.strip() for a in aliases])

    # Uniqueness checks
    dup_ids = {x for x in ids if ids.count(x) > 1}
    if dup_ids:
        errors.append(ValidationError(f"duplicate scenario ids: {sorted(dup_ids)}"))

    dup_aliases = {x for x in aliases_all if aliases_all.count(x) > 1}
    if dup_aliases:
        errors.append(ValidationError(f"duplicate aliases across catalog: {sorted(dup_aliases)}"))

    id_set = set(ids)
    alias_set = set(aliases_all)

    conflicts = sorted(id_set.intersection(alias_set))
    if conflicts:
        errors.append(ValidationError(f"aliases must not collide with ids: {conflicts}"))

    return id_set.union(alias_set), errors


def _iter_workflow_paths(workflows_dir: Path) -> list[Path]:
    if not workflows_dir.exists():
        return []
    return sorted([p for p in workflows_dir.glob("*.yml") if p.is_file()])


def _collect_workflow_choice_options(doc: Any) -> list[str]:
    # Safely walk: on.workflow_dispatch.inputs.<name>.options: [..]
    if not isinstance(doc, dict):
        return []

    on_section = doc.get("on")
    # NOTE: YAML 1.1 can parse 'on' as True in some parsers, but PyYAML preserves it as a key.
    if not isinstance(on_section, dict):
        return []

    wd = on_section.get("workflow_dispatch")
    if not isinstance(wd, dict):
        return []

    inputs = wd.get("inputs")
    if not isinstance(inputs, dict):
        return []

    options: list[str] = []
    for _, spec in inputs.items():
        if not isinstance(spec, dict):
            continue
        opts = spec.get("options")
        if isinstance(opts, list):
            for o in opts:
                if isinstance(o, str) and o.strip() and "${{" not in o:
                    options.append(o.strip())
    return options


def _collect_workflow_dispatch_scenario_defaults(doc: Any) -> list[str]:
    """Collect workflow_dispatch input defaults for scenario-like inputs.

    This supports suites that intentionally avoid `type: choice` + `options`.
    """

    if not isinstance(doc, dict):
        return []

    on_section = doc.get("on")
    if not isinstance(on_section, dict):
        return []

    wd = on_section.get("workflow_dispatch")
    if not isinstance(wd, dict):
        return []

    inputs = wd.get("inputs")
    if not isinstance(inputs, dict):
        return []

    defaults: list[str] = []
    for input_name, spec in inputs.items():
        if input_name not in {"scenario", "scenario_id"}:
            continue
        if not isinstance(spec, dict):
            continue

        default = spec.get("default")
        if isinstance(default, str) and default.strip() and "${{" not in default:
            defaults.append(default.strip())

    return defaults


def _collect_static_job_scenarios(doc: Any) -> list[str]:
    """Collect literal scenario values passed into reusable workflows.

    We only collect plain strings without GitHub expressions to avoid false positives.
    """

    if not isinstance(doc, dict):
        return []

    jobs = doc.get("jobs")
    if not isinstance(jobs, dict):
        return []

    found: list[str] = []
    for _, job in jobs.items():
        if not isinstance(job, dict):
            continue
        with_section = job.get("with")
        if not isinstance(with_section, dict):
            continue

        for key in ("scenario", "scenario_id"):
            value = with_section.get(key)
            if isinstance(value, str) and value.strip() and "${{" not in value:
                found.append(value.strip())

    return found


_BAD_ARTIFACT_NAME_VAR_PATTERNS = (
    "inputs.scenario_id",
    "matrix.scenario",
    "outputs.scenario",
)

_GOOD_ARTIFACT_NAME_VAR_PATTERNS = (
    "env.SAFE_SCENARIO_ID",
    "outputs.safe_scenario",
)


def _validate_upload_artifact_names(doc: Any, path: Path) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if not isinstance(doc, dict):
        return errors

    jobs = doc.get("jobs")
    if not isinstance(jobs, dict):
        return errors

    for job_id, job in jobs.items():
        if not isinstance(job, dict):
            continue
        steps = job.get("steps")
        if not isinstance(steps, list):
            continue

        for i, step in enumerate(steps):
            if not isinstance(step, dict):
                continue

            uses = step.get("uses")
            if not isinstance(uses, str) or "actions/upload-artifact" not in uses:
                continue

            with_section = step.get("with")
            if not isinstance(with_section, dict):
                continue

            name = with_section.get("name")
            if not isinstance(name, str) or not name.strip():
                continue

            name_str = name.strip()
            if any(bad in name_str for bad in _BAD_ARTIFACT_NAME_VAR_PATTERNS) and not any(
                good in name_str for good in _GOOD_ARTIFACT_NAME_VAR_PATTERNS
            ):
                errors.append(
                    ValidationError(
                        f"{path.name}: jobs.{job_id}.steps[{i}] upload-artifact name uses scenario without safe variant: {name_str}"
                    )
                )

    return errors


def main() -> int:
    root = _repo_root()
    catalog_path = root / "docs" / "labs" / "scenarios" / "catalog.yml"
    workflows_dir = root / ".github" / "workflows"

    valid_keys, errors = _validate_catalog(catalog_path)

    workflow_paths = _iter_workflow_paths(workflows_dir)
    referenced: list[tuple[Path, str, str]] = []

    for wf in workflow_paths:
        doc = _load_yaml(wf)
        for opt in _collect_workflow_choice_options(doc):
            referenced.append((wf, opt, "workflow_dispatch.options"))

        for default in _collect_workflow_dispatch_scenario_defaults(doc):
            referenced.append((wf, default, "workflow_dispatch.default"))

        for scenario in _collect_static_job_scenarios(doc):
            referenced.append((wf, scenario, "jobs.*.with"))

        errors.extend(_validate_upload_artifact_names(doc, wf))

    # Validate that all workflow choice options resolve to some scenario in catalog (id or aliases)
    for wf, value, source in referenced:
        if value not in valid_keys:
            errors.append(
                ValidationError(
                    f"{wf.name}: referenced scenario not found in catalog (id/aliases) [{source}]: {value}"
                )
            )

    if errors:
        for e in errors:
            print(f"[error] {e.message}", file=sys.stderr)
        print(f"[error] validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1

    print("[ok] scenario catalog + workflow references validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
