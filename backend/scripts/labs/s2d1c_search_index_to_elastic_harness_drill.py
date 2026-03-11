"""S2D-1C/P2-C2-S2: search_index_to_elastic harness drill (minimal real).

This lab validates the search outbox writer path for the
`search_index_to_elastic` projection by:

- Using SearchOutboxRepository to enqueue a unified outbox event for
  a deterministic `book` entity
- Verifying that a corresponding `outbox_events` row exists with
  projection=`search_index_to_elastic` and status='pending'

This is DB-only (no Elasticsearch), mirroring the
`_enqueue_search_outbox_only` pattern from S2C labs as the minimal
real harness for S2D-1C.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

_backend_dir = Path(__file__).resolve().parents[2]
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

import psycopg


SEARCH_PROJECTION = "search_index_to_elastic"
LAB_ID = "s2d1c_search_index_to_elastic_harness_drill"
SCENARIO_ID = "verify/search_index_to_elastic/harness_outbox_pending"


def _database_url_psycopg(database_url: str) -> str:
    """Convert SQLAlchemy psycopg URL to plain psycopg URL."""

    return database_url.replace("postgresql+psycopg://", "postgresql://")


def _utc_now_str() -> str:
    import time

    return time.strftime("%Y-%m-%d %H:%M:%S")


@dataclass(frozen=True)
class EvidenceResult:
    lab_id: str
    scenario: str
    run_id: str
    created_at: str
    ok: bool
    database_url: str
    search_outbox: dict[str, Any]


async def _enqueue_search_outbox_only(*, database_url: str) -> dict[str, Any]:
    """Enqueue a search_index_to_elastic outbox row and read it back."""

    os.environ["DATABASE_URL"] = database_url

    from infra.database.session import get_session_factory
    from infra.search.search_outbox_repository import SearchOutboxRepository

    session_factory = await get_session_factory()
    async with session_factory() as session:
        repo = SearchOutboxRepository(db=session)

        from uuid import UUID

        entity_type = "book"
        library_id = UUID("00000000-0000-0000-0000-000000000001")
        entity_id = UUID("00000000-0000-0000-0000-000000000002")

        await repo.enqueue(
            library_id=library_id,
            entity_type=entity_type,
            entity_id=entity_id,
            op="upsert",
            event_version=1,
        )

        await session.commit()

    cs = _database_url_psycopg(database_url)
    with psycopg.connect(cs) as conn:
        conn.execute("SET TIME ZONE 'UTC'")
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, projection, entity_type, entity_id, status, attempts, error_reason
                FROM outbox_events
                WHERE projection = %s
                  AND entity_type = %s
                  AND entity_id = %s
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (SEARCH_PROJECTION, entity_type, str(entity_id)),
            )
            row = cur.fetchone()

    if row is None:
        return {
            "found": False,
            "projection": SEARCH_PROJECTION,
            "entity_type": "book",
            "entity_id": "S2D1C-HARNESS-ENTITY",
        }

    (
        outbox_id,
        projection,
        entity_type_db,
        entity_id_db,
        status,
        attempts,
        error_reason,
    ) = row

    return {
        "found": True,
        "outbox_id": str(outbox_id),
        "projection": str(projection),
        "entity_type": str(entity_type_db),
        "entity_id": str(entity_id_db),
        "status": str(status),
        "attempts": int(attempts or 0),
        "error_reason": error_reason,
    }


async def _run(*, database_url: str, run_id: str, outdir: Path) -> EvidenceResult:
    outdir.mkdir(parents=True, exist_ok=True)

    search_outbox = await _enqueue_search_outbox_only(database_url=database_url)

    ok = bool(search_outbox.get("found")) and search_outbox.get("projection") == SEARCH_PROJECTION and search_outbox.get("status") == "pending"

    result = EvidenceResult(
        lab_id=LAB_ID,
        scenario=SCENARIO_ID,
        run_id=run_id,
        created_at=_utc_now_str(),
        ok=ok,
        database_url=database_url,
        search_outbox=search_outbox,
    )

    (outdir / "_result.json").write_text(
        json.dumps(asdict(result), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="S2D-1C search_index_to_elastic harness drill (minimal real)",
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
