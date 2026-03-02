"""S2C-6A/P3 evidence runner (local, DB + ES).

This script provides a minimal, auditable scenario that proves:
- The stable Search worker entrypoint can run in harness mode via shim.
- The harness consumes unified outbox rows for projection=search_index_to_elastic.
- The shared adapter writes a doc to Elasticsearch (schema_version contract included).

It intentionally does not depend on ES bulk.

Outputs:
- Writes `<outdir>/_result.json` as the evidence SoT for the round.
- Writes `<outdir>/_es_doc.json` and `<outdir>/_outbox_row.json` as supporting snapshots.

Preconditions:
- PostgreSQL reachable via --database-url
- Elasticsearch reachable via --elastic-url

Notes:
- This scenario may create the target index if missing (setup only; worker still does
  not manage index lifecycle).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from uuid import UUID

# Ensure `import infra.*` works when executed as a plain script.
_backend_dir = Path(__file__).resolve().parents[2]
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

import httpx
import psycopg


SEARCH_PROJECTION = "search_index_to_elastic"
LAB_ENTITY_TYPE = "block"


def _utc_now_str() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def _database_url_psycopg(database_url: str) -> str:
    return database_url.replace("postgresql+psycopg://", "postgresql://")


def _seed_ids(run_id: str) -> tuple[UUID, UUID, UUID]:
    """Derive stable ids for this run.

    We tie ids to run_id so multiple rounds don't collide.
    """

    import uuid

    ns = uuid.uuid5(uuid.NAMESPACE_URL, "wordloom.s2c6a.search.harness.es.smoke.v1")
    row_id = uuid.uuid5(ns, f"row_id:{run_id}")
    entity_id = uuid.uuid5(ns, f"entity_id:{run_id}")
    library_id = uuid.uuid5(ns, f"library_id:{run_id}")
    return row_id, entity_id, library_id


def _ensure_search_index_row(*, database_url: str, run_id: str) -> dict[str, Any]:
    row_id, entity_id, library_id = _seed_ids(run_id)

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
                    str(row_id),
                    LAB_ENTITY_TYPE,
                    str(library_id),
                    str(entity_id),
                    f"LAB_S2C6A_SEARCH_HARNESS_ES_SMOKE_TEXT {run_id}",
                    "LAB_S2C6A_SEARCH_HARNESS_ES_SMOKE_SNIPPET",
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


def _insert_outbox_event(*, database_url: str, seeded: dict[str, Any], run_id: str) -> UUID:
    import uuid

    outbox_id = uuid.uuid4()
    cs = _database_url_psycopg(database_url)

    with psycopg.connect(cs) as conn:
        conn.execute("SET TIME ZONE 'UTC'")
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO outbox_events (
                    id, projection, entity_type, entity_id, op, event_version,
                    status, attempts, replay_count, payload, library_id,
                    created_at, updated_at
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s,
                    'pending', 0, 0, %s, %s,
                    NOW(), NOW()
                )
                """,
                (
                    str(outbox_id),
                    SEARCH_PROJECTION,
                    seeded["entity_type"],
                    seeded["entity_id"],
                    "upsert",
                    int(seeded["event_version"]),
                    json.dumps({}),
                    seeded.get("library_id"),
                ),
            )
        conn.commit()

    return UUID(str(outbox_id))


def _fetch_outbox_row(*, database_url: str, outbox_id: UUID) -> dict[str, Any] | None:
    cs = _database_url_psycopg(database_url)
    with psycopg.connect(cs) as conn:
        conn.execute("SET TIME ZONE 'UTC'")
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, projection, status, processed_at, attempts, error_reason
                FROM outbox_events
                WHERE id = %s
                """,
                (str(outbox_id),),
            )
            row = cur.fetchone()

    if row is None:
        return None

    id_raw, projection, status, processed_at, attempts, error_reason = row
    return {
        "id": str(id_raw),
        "projection": str(projection),
        "status": str(status),
        "processed_at": processed_at.isoformat() if processed_at else None,
        "attempts": int(attempts or 0),
        "error_reason": str(error_reason) if error_reason else None,
    }


def _ensure_es_index(*, elastic_url: str, elastic_index: str) -> dict[str, Any]:
    base_url = (elastic_url or "").strip().rstrip("/")
    if not base_url:
        raise RuntimeError("elastic_url is required")
    if not elastic_index.strip():
        raise RuntimeError("elastic_index is required")

    with httpx.Client(base_url=base_url, timeout=10.0) as client:
        r = client.get(f"/{elastic_index}")
        if r.status_code == 200:
            return {"created": False, "status_code": 200}
        if r.status_code != 404:
            r.raise_for_status()

        # Minimal default index. Keep it permissive (dynamic mappings) for smoke.
        r2 = client.put(f"/{elastic_index}", json={})
        r2.raise_for_status()
        return {"created": True, "status_code": int(r2.status_code)}


def _fetch_es_doc(
    *,
    elastic_url: str,
    elastic_index: str,
    doc_id: str,
) -> dict[str, Any] | None:
    base_url = (elastic_url or "").strip().rstrip("/")
    with httpx.Client(base_url=base_url, timeout=10.0) as client:
        r = client.get(f"/{elastic_index}/_doc/{doc_id}")
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return dict(r.json())


def _run_worker_harness_mode(*, env: dict[str, str]) -> int:
    cmd = [sys.executable, "backend/scripts/search_outbox_worker.py"]
    return int(subprocess.call(cmd, env=env))


@dataclass(frozen=True)
class EvidenceResult:
    lab_id: str
    scenario: str
    run_id: str
    created_at: str
    ok: bool
    database_url: str
    elastic_url: str
    elastic_index: str
    seeded: dict[str, Any]
    outbox_id: str
    worker_exit_code: int
    outbox_row: dict[str, Any] | None
    es_index: dict[str, Any]
    es_doc_found: bool
    es_doc_source: dict[str, Any] | None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", required=True)
    parser.add_argument("--elastic-url", required=True)
    parser.add_argument("--elastic-index", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--outdir", required=True)

    args = parser.parse_args()

    database_url = str(args.database_url).strip()
    elastic_url = str(args.elastic_url).strip()
    elastic_index = str(args.elastic_index).strip()
    run_id = str(args.run_id).strip()
    outdir = Path(str(args.outdir).strip())
    outdir.mkdir(parents=True, exist_ok=True)

    # Set env for the harness path.
    env = dict(os.environ)
    env["DATABASE_URL"] = database_url
    env["ELASTIC_URL"] = elastic_url
    env["ELASTIC_INDEX"] = elastic_index
    env["SEARCH_OUTBOX_RUNNER"] = "harness"
    env.setdefault("OUTBOX_EXIT_WHEN_IDLE", "1")
    env.setdefault("OUTBOX_POLL_INTERVAL_SECONDS", "0.2")
    env.setdefault("OUTBOX_RECLAIM_INTERVAL_SECONDS", "1.0")
    # Avoid port conflicts in local evidence runs.
    env["OUTBOX_METRICS_PORT"] = ""

    es_index = _ensure_es_index(elastic_url=elastic_url, elastic_index=elastic_index)

    seeded = _ensure_search_index_row(database_url=database_url, run_id=run_id)
    outbox_id = _insert_outbox_event(database_url=database_url, seeded=seeded, run_id=run_id)

    worker_exit_code = _run_worker_harness_mode(env=env)

    outbox_row = _fetch_outbox_row(database_url=database_url, outbox_id=outbox_id)

    doc_id = f"{seeded['entity_type']}:{seeded['entity_id']}"

    es_doc = None
    for _ in range(10):
        es_doc = _fetch_es_doc(
            elastic_url=elastic_url,
            elastic_index=elastic_index,
            doc_id=doc_id,
        )
        if es_doc is not None:
            break
        time.sleep(0.2)

    es_source = None
    if isinstance(es_doc, dict) and isinstance(es_doc.get("_source"), dict):
        es_source = dict(es_doc["_source"])

    ok = (
        worker_exit_code == 0
        and outbox_row is not None
        and outbox_row.get("status") == "done"
        and es_source is not None
        and es_source.get("schema_version") == 1
        and es_source.get("entity_id") == str(seeded["entity_id"])
        and es_source.get("entity_type") == str(seeded["entity_type"])
    )

    result = EvidenceResult(
        lab_id="s2c6a_search_harness_es_smoke",
        scenario="verify/search/harness_es_smoke",
        run_id=run_id,
        created_at=_utc_now_str(),
        ok=bool(ok),
        database_url=database_url,
        elastic_url=elastic_url,
        elastic_index=elastic_index,
        seeded=seeded,
        outbox_id=str(outbox_id),
        worker_exit_code=int(worker_exit_code),
        outbox_row=outbox_row,
        es_index=es_index,
        es_doc_found=bool(es_source is not None),
        es_doc_source=es_source,
    )

    (outdir / "_result.json").write_text(json.dumps(asdict(result), indent=2, sort_keys=True), encoding="utf-8")
    (outdir / "_outbox_row.json").write_text(json.dumps(outbox_row or {}, indent=2, sort_keys=True), encoding="utf-8")
    (outdir / "_es_doc.json").write_text(json.dumps(es_doc or {}, indent=2, sort_keys=True), encoding="utf-8")

    if not result.ok:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
