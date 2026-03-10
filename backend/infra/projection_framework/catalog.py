from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List

from .builtins import register_builtin_specs
from .registry import list_specs


@dataclass(frozen=True)
class ProjectionCatalogEntry:
    """S2D onboarding catalog metadata for a single projection.

    This is a lightweight, in-code catalog used for S2D-2A.
    In v1 we keep it simple and derive most fields from the
    existing ProjectionSpec registry, plus a small set of
    explicit overrides for S2D-enabled projections.
    """

    projection_name: str
    onboarding_status: str  # platformized | legacy | experimental | unknown
    onboarding_phase: str   # S2D-1A | S2D-2A | S2D-3A | none
    owner_team: str | None = None


def _static_overrides() -> Dict[str, ProjectionCatalogEntry]:
    """Static overrides for projections with known S2D onboarding state.

    v1 only marks the S2D-1A sample projection as platformized;
    other projections will be treated as legacy by default.
    """

    return {
        "chronicle_daily_stats": ProjectionCatalogEntry(
            projection_name="chronicle_daily_stats",
            onboarding_status="platformized",
            onboarding_phase="S2D-1A",
            owner_team="data-platform",
        ),
    }


def build_catalog_entries() -> List[ProjectionCatalogEntry]:
    """Enumerate all registered projections with S2D catalog metadata.

    - Ensures builtin specs are registered.
    - Applies static overrides for known S2D-enabled projections.
    - Defaults unknown projections to `legacy/none` status.
    """

    register_builtin_specs()
    specs = list_specs()

    overrides = _static_overrides()
    entries: List[ProjectionCatalogEntry] = []

    for spec in specs:
        name = spec.projection_name
        if name in overrides:
            entries.append(overrides[name])
        else:
            entries.append(
                ProjectionCatalogEntry(
                    projection_name=name,
                    onboarding_status="legacy",
                    onboarding_phase="none",
                    owner_team=None,
                )
            )

    return entries


def compute_coverage_snapshot() -> Dict[str, Any]:
    """Compute a JSON-serializable onboarding coverage snapshot.

    The schema follows the S2D-2A P0-C1-S2 contract:
    - generated_at (UTC ISO8601)
    - total_projections / platformized_projections / legacy_projections
    - by_team (aggregated counts)
    - projections (per-projection summary rows)
    """

    entries = build_catalog_entries()

    total = len(entries)
    platformized = sum(1 for e in entries if e.onboarding_status == "platformized")
    legacy = sum(1 for e in entries if e.onboarding_status == "legacy")

    by_team: Dict[str, Dict[str, Any]] = {}
    for e in entries:
        team = e.owner_team or "unknown"
        agg = by_team.setdefault(
            team,
            {
                "owner_team": team,
                "total_projections": 0,
                "platformized_projections": 0,
                "legacy_projections": 0,
            },
        )
        agg["total_projections"] += 1
        if e.onboarding_status == "platformized":
            agg["platformized_projections"] += 1
        if e.onboarding_status == "legacy":
            agg["legacy_projections"] += 1

    snapshot: Dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_projections": total,
        "platformized_projections": platformized,
        "legacy_projections": legacy,
        "by_team": list(by_team.values()),
        "projections": [
            {
                "projection_name": e.projection_name,
                "onboarding_status": e.onboarding_status,
                "onboarding_phase": e.onboarding_phase,
                "owner_team": e.owner_team,
            }
            for e in entries
        ],
    }

    return snapshot


__all__ = [
    "ProjectionCatalogEntry",
    "build_catalog_entries",
    "compute_coverage_snapshot",
]
