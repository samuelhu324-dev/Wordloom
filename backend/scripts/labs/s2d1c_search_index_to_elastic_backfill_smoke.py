"""S2D-1C/P2-C2-S1: search_index_to_elastic backfill smoke (minimal real).

This lab exercises the generic backfill template for the Search
projection by:

- Seeding one `search_index` SoT row (self-contained; no FK dependencies)
- Running a DB-only backfill that emits a deterministic `outbox_events`
  row (projection=`search_index_to_elastic`) from the SoT row
- Re-running the same backfill to verify idempotence (second pass
  inserts 0 new rows)

Outputs:
- Writes `<outdir>/_result.json` as the evidence SoT for the round.

This is DB-only (no Elasticsearch dependency) and is intended as the
C2 "minimal real" backfill smoke for S2D-1C. `ok=true` means:
- First backfill inserted exactly 1 outbox row
- Second backfill inserted 0 rows and total rows stayed at 1
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from uuid import UUID

_backend_dir = Path(__file__).resolve().parents[2]
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

import psycopg
from sqlalchemy import select

from infra.projection_framework.backfill_template import (
    BackfillEmitter,
    BackfillItem,
    BackfillStats,
    require_enabled_env,
    run_backfill,
)


SEARCH_PROJECTION = "search_index_to_elastic"
LAB_ENTITY_TYPE = "block"


def _utc_now_str() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def _database_url_psycopg(database_url: str) -> str:
    """Convert SQLAlchemy psycopg URL to plain psycopg URL."""

    return database_url.replace("postgresql+psycopg://", "postgresql://")


def _seed_ids(run_id: str) -> tuple[UUID, UUID]:
    """Derive stable ids for this run based on `run_id`."""

    import uuid

    ns = uuid.uuid5(uuid.NAMESPACE_URL, "wordloom.s2d1c.backfill.search.smoke.v1")
    entity_id = uuid.uuid5(ns, f"entity_id:{run_id}")
    library_id = uuid.uuid5(ns, f"library_id:{run_id}")
    return entity_id, library_id


def _ensure_search_index_row(*, database_url: str, run_id: str) -> dict[str, Any]:
    """Ensure a deterministic search_index row exists for this run."""

    entity_id, library_id = _seed_ids(run_id)

    import uuid

    row_id = str(uuid.uuid4())

    cs = _database_url_psycopg(database_url)
    now = _utc_now_str()

    with psycopg.connect(cs) as conn:
        conn.execute("SET TIME ZONE 'UTC'")
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO search_index (
                    id, entity_type, library_id, entity_id,
                    text, snippet, rank_score,
                    created_at, updated_at, event_version
                )
                VALUES (
                    %s, %s, %s, %s,
                    %s, %s, %s,
                    NOW(), NOW(), %s
                )
                ON CONFLICT (entity_type, entity_id)
                DO UPDATE SET
                    library_id = EXCLUDED.library_id,
                    text = EXCLUDED.text,
                    snippet = EXCLUDED.snippet,
                    rank_score = EXCLUDED.rank_score,
                    updated_at = NOW(),
                    event_version = GREATEST(search_index.event_version, EXCLUDED.event_version)
                """,
                (
                    row_id,
                    LAB_ENTITY_TYPE,
                    str(library_id),
                    str(entity_id),
                    f"LAB_S2D1C_BACKFILL_SMOKE_TEXT {run_id}",
                    "LAB_S2D1C_BACKFILL_SMOKE_SNIPPET",
                    0.0,
                    1,
                ),
            )
        conn.commit()

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT entity_type, library_id, entity_id, event_version
                FROM search_index
                WHERE entity_type = %s AND entity_id = %s
                """,
                (LAB_ENTITY_TYPE, str(entity_id)),
            )
            row = cur.fetchone()

    if row is None:
        raise RuntimeError("failed to seed search_index row")

    entity_type, library_id_db, entity_id_db, event_version = row
    return {
        "entity_type": str(entity_type),
        "library_id": str(library_id_db) if library_id_db else None,
        "entity_id": str(entity_id_db),
        "event_version": int(event_version or 0),
        "seeded_at": now,
    }


def _count_outbox_rows(*, database_url: str, entity_id: str, event_version: int) -> int:
    cs = _database_url_psycopg(database_url)
    with psycopg.connect(cs) as conn:
        conn.execute("SET TIME ZONE 'UTC'")
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*)
                FROM outbox_events
                WHERE projection = %s
                  AND entity_type = %s
                  AND entity_id = %s
                  AND op = 'upsert'
                  AND event_version = %s
                """,
                (SEARCH_PROJECTION, LAB_ENTITY_TYPE, entity_id, int(event_version)),
            )
            (n,) = cur.fetchone()
            return int(n or 0)


async def _work(*, session: Any, emit: BackfillEmitter, entity_id: UUID) -> None:
    from infra.database.models.search_index_models import SearchIndexModel

    stmt = select(SearchIndexModel).where(SearchIndexModel.entity_id == entity_id)
    row = (await session.execute(stmt)).scalars().first()
    if row is None:
        raise RuntimeError(f"search_index row not found for entity_id={entity_id}")

    await emit.emit(
        BackfillItem(
            projection=SEARCH_PROJECTION,
            entity_type=row.entity_type,
            entity_id=row.entity_id,
            op="upsert",
            event_version=int(row.event_version or 0),
            library_id=row.library_id,
            payload={},
        )
    )

    await emit.flush()


@dataclass(frozen=True)
class EvidenceResult:
    lab_id: str
    scenario: str
    run_id: str
    created_at: str
    ok: bool
    database_url: str
    seeded: dict[str, Any]
    pass1: dict[str, Any]
    pass2: dict[str, Any]


def _stats_jsonable(stats: BackfillStats) -> dict[str, Any]:
    raw = asdict(stats)
    raw["started_at"] = stats.started_at.isoformat()
    raw["finished_at"] = stats.finished_at.isoformat()
    return raw


async def _run(*, database_url: str, run_id: str, outdir: Path) -> EvidenceResult:
    outdir.mkdir(parents=True, exist_ok=True)

    # Align DB access layers (SQLAlchemy engine reads env at import time).
    os.environ["DATABASE_URL"] = database_url

    # Labs: satisfy the gate explicitly, then enforce it.
    os.environ.setdefault("OUTBOX_BACKFILL_ENABLED", "true")
    require_enabled_env()

    seeded = _ensure_search_index_row(database_url=database_url, run_id=run_id)

    entity_id = UUID(seeded["entity_id"])
    event_version = int(seeded["event_version"])

    before0 = _count_outbox_rows(
        database_url=database_url,
        entity_id=str(entity_id),
        event_version=event_version,
    )

    from infra.database.session import get_session_factory

    session_factory = await get_session_factory()

    # Pass 1
    _, stats1 = await run_backfill(
        projection_name=SEARCH_PROJECTION,
        session_factory=session_factory,
        work=lambda session, emit: _work(session=session, emit=emit, entity_id=entity_id),
        run_id=run_id,
        worker_id=f"s2d1c_backfill_smoke:{run_id}",
        dry_run=False,
        batch_size=100,
    )

    after1 = _count_outbox_rows(
        database_url=database_url,
        entity_id=str(entity_id),
        event_version=event_version,
    )

    # Pass 2 (idempotence)
    _, stats2 = await run_backfill(
        projection_name=SEARCH_PROJECTION,
        session_factory=session_factory,
        work=lambda session, emit: _work(session=session, emit=emit, entity_id=entity_id),
        run_id=run_id,
        worker_id=f"s2d1c_backfill_smoke:{run_id}",
        dry_run=False,
        batch_size=100,
    )

    after2 = _count_outbox_rows(
        database_url=database_url,
        entity_id=str(entity_id),
        event_version=event_version,
    )

    pass1 = {
        "before": int(before0),
        "after": int(after1),
        "inserted": int(after1 - before0),
        "stats": _stats_jsonable(stats1),
    }
    pass2 = {
        "before": int(after1),
        "after": int(after2),
        "inserted": int(after2 - after1),
        "stats": _stats_jsonable(stats2),
    }

    ok = pass1["inserted"] == 1 and pass2["inserted"] == 0 and after2 == 1

    result = EvidenceResult(
        lab_id="s2d1c_search_index_to_elastic_backfill_smoke",
        scenario="verify/search_index_to_elastic/backfill_outbox_smoke",
        run_id=run_id,
        created_at=_utc_now_str(),
        ok=bool(ok),
        database_url=database_url,
        seeded=seeded,
        pass1=pass1,
        pass2=pass2,
    )

    (outdir / "_result.json").write_text(
        json.dumps(asdict(result), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="S2D-1C search_index_to_elastic backfill smoke (minimal real)",
    )
    parser.add_argument("--database-url", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--outdir", required=True)

    args = parser.parse_args(argv)

    database_url = str(args.database_url).strip()
    run_id = str(args.run_id).strip()
    outdir = Path(str(args.outdir).strip())

    if sys.platform.startswith("win"):
        import selectors

        loop_factory = lambda: asyncio.SelectorEventLoop(selectors.SelectSelector())
        result = asyncio.run(
            _run(database_url=database_url, run_id=run_id, outdir=outdir),
            loop_factory=loop_factory,
        )
    else:
        result = asyncio.run(_run(database_url=database_url, run_id=run_id, outdir=outdir))

    if not result.ok:
        raise SystemExit(2)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
