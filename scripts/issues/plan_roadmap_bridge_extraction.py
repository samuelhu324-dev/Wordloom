from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _load_text, _parse_fields, _repo_rel, _repo_root


ROADMAP_HEADING_RE = re.compile(r"^###\s+(M\d+):")
PHASE_SLOT_RE = re.compile(r"^- `?(M\d+-P\d+)`?:\s*$")
CHILD_ENTRY_RE = re.compile(r"^- `([^`]+)`(?: via `([^`]+)`)?\s*$")
PARENT_CONTRIB_RE = re.compile(r"^- `([^`]+)`\s*$")


@dataclass
class RoadmapBridgePlanItem:
    roadmap_path: str
    roadmap_id: str
    roadmap_kind: str
    milestone: str
    phase: str
    child_log_path: str | None
    via_road_id: str | None
    expected_log_roadmap_path: str | None
    expected_log_roadmap_milestone: str | None
    expected_log_roadmap_phase: str | None
    actual_log_roadmap_path: str | None
    actual_log_roadmap_milestone: str | None
    actual_log_roadmap_phase: str | None
    actual_log_roadmap_bridge_refs: list[str]
    planned_action: str
    status: str
    warnings: list[str]


@dataclass
class ParentAlignmentCheck:
    branch_roadmap_path: str
    branch_roadmap_id: str
    parent_roadmap_id: str
    parent_phase: str
    child_log_path: str
    status: str
    warnings: list[str]


@dataclass
class RoadmapBridgePlanResult:
    mode: str
    result: str
    manifest_path: str | None
    selection_input: str
    operation: str
    total_bridge_items: int
    aligned_items: int
    warning_items: int
    reconciliation_items: int
    unmapped_items: int
    warnings: list[str]
    items: list[RoadmapBridgePlanItem]
    parent_alignment_checks: list[ParentAlignmentCheck]


@dataclass
class RoadmapManifestItem:
    roadmap_path: str
    roadmap_kind: str | None
    verify_log_fields: bool
    verify_parent_alignment: bool


@dataclass
class RoadmapDocument:
    roadmap_path: str
    roadmap_id: str
    roadmap_kind: str
    bridge_items: list[tuple[str, str, str | None, str | None]]
    parent_contributions: list[tuple[str, str, str]]


def _dedupe_tuples(items: list[tuple[str, ...]]) -> list[tuple[str, ...]]:
    seen: set[tuple[str, ...]] = set()
    result: list[tuple[str, ...]] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan roadmap bridge extraction from explicit bridge ledgers")
    parser.add_argument("manifest_path", help="Path to a roadmap bridge manifest JSON file")
    parser.add_argument("--plan-path", dest="plan_path", help="Override output plan JSON path")
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _load_manifest(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse roadmap bridge manifest JSON: {exc}") from exc


def _manifest_items(manifest: dict) -> list[RoadmapManifestItem]:
    defaults = manifest.get("defaults") or {}
    raw_items = manifest.get("items") or []
    if not raw_items:
        raise SystemExit("Roadmap bridge manifest requires at least one item")

    items: list[RoadmapManifestItem] = []
    for raw in raw_items:
        roadmap_path = raw.get("roadmap_path")
        if not roadmap_path:
            raise SystemExit("Roadmap bridge manifest item missing roadmap_path")
        items.append(
            RoadmapManifestItem(
                roadmap_path=roadmap_path,
                roadmap_kind=raw.get("roadmap_kind") or defaults.get("roadmap_kind"),
                verify_log_fields=bool(raw.get("verify_log_fields", defaults.get("verify_log_fields", True))),
                verify_parent_alignment=bool(raw.get("verify_parent_alignment", defaults.get("verify_parent_alignment", True))),
            )
        )
    return items


def _parse_parent_contribution_content(content: str) -> tuple[str, str, str] | None:
    if " <- " not in content:
        return None
    left, child_log_path = content.split(" <- ", 1)
    left_parts = left.split()
    if len(left_parts) != 2:
        return None
    parent_roadmap_id, parent_phase = left_parts
    return parent_roadmap_id, parent_phase, child_log_path.strip()


def _parse_bridge_refs(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def _extract_roadmap_document(path: Path, roadmap_kind_override: str | None) -> RoadmapDocument:
    text = _load_text(path)
    fields = _parse_fields(text)
    roadmap_id = fields.get("id", path.stem).strip()
    parent_road = fields.get("parent_road", "").strip()
    roadmap_kind = roadmap_kind_override or ("branch" if parent_road else "mainline")

    bridge_items: list[tuple[str, str, str | None, str | None]] = []
    parent_contributions: list[tuple[str, str, str]] = []

    current_milestone: str | None = None
    current_phase: str | None = None
    in_bridge = False
    in_parent_alignment = False
    in_parent_ledger = False

    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()

        heading = ROADMAP_HEADING_RE.match(line)
        if heading:
            current_milestone = heading.group(1)
            current_phase = None
            in_bridge = False
            in_parent_alignment = False
            continue

        if stripped.startswith("## "):
            in_parent_ledger = stripped == "## Parent Contribution Ledger"
            if stripped != "## Parent Contribution Ledger":
                in_parent_alignment = False
            if stripped != "## Milestones (M1–M5)" and stripped != "## Milestones (M1-M5)":
                current_phase = None if stripped != "## Parent Contribution Ledger" else current_phase

        if stripped == "**Bridge Ledger (child logs only)**":
            in_bridge = True
            in_parent_alignment = False
            current_phase = None
            continue

        if stripped == "**Parent alignment**":
            in_parent_alignment = True
            in_bridge = False
            current_phase = None
            continue

        if stripped.startswith("**") and stripped not in {"**Bridge Ledger (child logs only)**", "**Parent alignment**"}:
            in_bridge = False
            in_parent_alignment = False

        if in_bridge:
            phase_match = PHASE_SLOT_RE.match(stripped)
            if phase_match:
                current_phase = phase_match.group(1)
                continue
            child_match = CHILD_ENTRY_RE.match(stripped)
            if child_match and current_milestone and current_phase:
                child_log = child_match.group(1).strip()
                via_road = child_match.group(2).strip() if child_match.group(2) else None
                child_log_path = None if child_log == "unmapped" else child_log
                bridge_items.append((current_milestone, current_phase, child_log_path, via_road))
                continue

        if in_parent_ledger or in_parent_alignment:
            contrib_match = PARENT_CONTRIB_RE.match(stripped)
            if contrib_match:
                parsed = _parse_parent_contribution_content(contrib_match.group(1).strip())
                if parsed is not None:
                    parent_contributions.append(parsed)

    return RoadmapDocument(
        roadmap_path=_repo_rel(path),
        roadmap_id=roadmap_id,
        roadmap_kind=roadmap_kind,
        bridge_items=bridge_items,
        parent_contributions=_dedupe_tuples(parent_contributions),
    )


def _verify_log_fields(
    *,
    repo_root: Path,
    child_log_path: str | None,
    expected_roadmap_path: str | None,
    expected_milestone: str | None,
    expected_phase: str | None,
    verify_log_fields: bool,
) -> tuple[str, str, list[str], str | None, str | None, str | None, list[str]]:
    warnings: list[str] = []
    if child_log_path is None:
        return "skip-unmapped-slot", "unmapped", warnings, None, None, None, []

    resolved_log = _coerce_path(child_log_path, repo_root)
    if not resolved_log.is_file():
        warnings.append("child log path does not exist")
        return "reconcile-missing-child-log", "reconciliation", warnings, None, None, None, []

    fields = _parse_fields(_load_text(resolved_log))
    actual_path = fields.get("roadmap_path", "").strip() or None
    actual_milestone = fields.get("roadmap_milestone", "").strip() or None
    actual_phase = fields.get("roadmap_phase", "").strip() or None
    actual_bridge_refs = _parse_bridge_refs(fields.get("roadmap_bridge_refs", "").strip() or None)

    if not verify_log_fields:
        return "extract-roadmap-bridge", "aligned", warnings, actual_path, actual_milestone, actual_phase, actual_bridge_refs

    if not actual_path and not actual_milestone and not actual_phase and not actual_bridge_refs:
        warnings.append("child log is missing roadmap bridge fields; roadmap ledger remains the canonical source")
        return "extract-roadmap-bridge", "warning", warnings, actual_path, actual_milestone, actual_phase, actual_bridge_refs

    expected_bridge_ref = None
    if expected_roadmap_path and expected_phase:
        expected_bridge_ref = f"{expected_roadmap_path}#{expected_phase}"

    if expected_bridge_ref and expected_bridge_ref in actual_bridge_refs:
        return "extract-roadmap-bridge", "aligned", warnings, actual_path, actual_milestone, actual_phase, actual_bridge_refs

    mismatches: list[str] = []
    if actual_path != expected_roadmap_path:
        mismatches.append("roadmap_path mismatch")
    if actual_milestone != expected_milestone:
        mismatches.append("roadmap_milestone mismatch")
    if actual_phase != expected_phase:
        mismatches.append("roadmap_phase mismatch")
    if mismatches:
        warnings.extend(mismatches)
        return "reconcile-log-bridge-fields", "reconciliation", warnings, actual_path, actual_milestone, actual_phase, actual_bridge_refs

    return "extract-roadmap-bridge", "aligned", warnings, actual_path, actual_milestone, actual_phase, actual_bridge_refs


def plan_roadmap_bridge_extraction(args: argparse.Namespace) -> RoadmapBridgePlanResult:
    repo_root = _repo_root()
    manifest_path = _coerce_path(args.manifest_path, repo_root)
    if not manifest_path.is_file():
        raise SystemExit(f"Roadmap bridge manifest file not found: {manifest_path}")

    manifest = _load_manifest(manifest_path)
    manifest_items = _manifest_items(manifest)
    documents = [_extract_roadmap_document(_coerce_path(item.roadmap_path, repo_root), item.roadmap_kind) for item in manifest_items]

    road_by_id = {document.roadmap_id: document for document in documents}
    ledger_lookup: set[tuple[str, str, str, str | None]] = set()
    for document in documents:
        for _, phase, child_log_path, via_road in document.bridge_items:
            if child_log_path is None:
                continue
            ledger_lookup.add((document.roadmap_id, phase, child_log_path, via_road))

    items: list[RoadmapBridgePlanItem] = []
    parent_checks: list[ParentAlignmentCheck] = []
    top_warnings: list[str] = []

    for manifest_item, document in zip(manifest_items, documents):
        for milestone, phase, child_log_path, via_road_id in document.bridge_items:
            expected_roadmap_path = document.roadmap_path
            if via_road_id and via_road_id in road_by_id:
                expected_roadmap_path = road_by_id[via_road_id].roadmap_path

            planned_action, status, warnings, actual_path, actual_milestone, actual_phase, actual_bridge_refs = _verify_log_fields(
                repo_root=repo_root,
                child_log_path=child_log_path,
                expected_roadmap_path=expected_roadmap_path if child_log_path else None,
                expected_milestone=milestone if child_log_path else None,
                expected_phase=phase if child_log_path else None,
                verify_log_fields=manifest_item.verify_log_fields,
            )
            if warnings:
                top_warnings.append(f"{document.roadmap_id} {phase}: {'; '.join(warnings)}")
            items.append(
                RoadmapBridgePlanItem(
                    roadmap_path=document.roadmap_path,
                    roadmap_id=document.roadmap_id,
                    roadmap_kind=document.roadmap_kind,
                    milestone=milestone,
                    phase=phase,
                    child_log_path=child_log_path,
                    via_road_id=via_road_id,
                    expected_log_roadmap_path=expected_roadmap_path if child_log_path else None,
                    expected_log_roadmap_milestone=milestone if child_log_path else None,
                    expected_log_roadmap_phase=phase if child_log_path else None,
                    actual_log_roadmap_path=actual_path,
                    actual_log_roadmap_milestone=actual_milestone,
                    actual_log_roadmap_phase=actual_phase,
                    actual_log_roadmap_bridge_refs=actual_bridge_refs,
                    planned_action=planned_action,
                    status=status,
                    warnings=warnings,
                )
            )

        if manifest_item.verify_parent_alignment:
            for parent_roadmap_id, parent_phase, child_log_path in document.parent_contributions:
                warnings: list[str] = []
                expected = (parent_roadmap_id, parent_phase, child_log_path, document.roadmap_id)
                if expected in ledger_lookup:
                    status = "aligned"
                else:
                    warnings.append("parent roadmap ledger does not contain the expected child log via this branch road")
                    status = "reconciliation"
                    top_warnings.append(f"{document.roadmap_id} {parent_phase}: missing mirrored parent alignment for {child_log_path}")

                parent_checks.append(
                    ParentAlignmentCheck(
                        branch_roadmap_path=document.roadmap_path,
                        branch_roadmap_id=document.roadmap_id,
                        parent_roadmap_id=parent_roadmap_id,
                        parent_phase=parent_phase,
                        child_log_path=child_log_path,
                        status=status,
                        warnings=warnings,
                    )
                )

    manifest_rel = _repo_rel(manifest_path)
    manifest_slug = manifest_path.stem
    if manifest_slug.endswith("-manifest"):
        manifest_slug = manifest_slug[: -len("-manifest")]
    default_plan_path = repo_root / "docs" / "issues" / f"{manifest_slug}-plan.json"
    plan_path = _coerce_path(args.plan_path, repo_root) if args.plan_path else default_plan_path
    plan_path.parent.mkdir(parents=True, exist_ok=True)

    result = RoadmapBridgePlanResult(
        mode="roadmap-bridge-dry-run",
        result="ok",
        manifest_path=manifest_rel,
        selection_input="manifest",
        operation="extract-roadmap-bridge",
        total_bridge_items=len(items),
        aligned_items=sum(1 for item in items if item.status == "aligned"),
        warning_items=sum(1 for item in items if item.status == "warning"),
        reconciliation_items=sum(1 for item in items if item.status == "reconciliation"),
        unmapped_items=sum(1 for item in items if item.status == "unmapped"),
        warnings=top_warnings,
        items=items,
        parent_alignment_checks=parent_checks,
    )
    plan_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        plan_roadmap_bridge_extraction(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())