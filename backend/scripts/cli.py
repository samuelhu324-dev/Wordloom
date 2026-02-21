"""Minimal script router for backend/scripts.

Design goals:
- Keep it tiny and dependency-free.
- Provide a stable command namespace so people stop memorizing file names.
- Enforce consistent snapshot output locations for labs.

This is intentionally not a full-featured CLI framework.
"""

from __future__ import annotations
# 在 cli.py 顶部加（或 main 里局部 import 也行）
# 注意：cli.py 以脚本方式运行（python backend/scripts/cli.py）时，sys.path[0] 是 backend/scripts。
# 因此应从同级包 cli_app 导入，而不是 backend.scripts.cli_app。
from cli_app import registry as _wg_registry
from cli_app.common import build_evidence_paths, build_evidence_paths_for_dir, write_json, zip_directory
from cli_app.types import DrillInputs

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import bindparam, create_engine, text


REPO_ROOT = Path(__file__).resolve().parents[2]
LEGACY_SCRIPTS_DIR = REPO_ROOT / "backend" / "scripts" / "legacy"
LABS_SNAPSHOT_ROOT = REPO_ROOT / "docs" / "labs" / "_snapshot"


LAB_ID_S3A_2A_3A = "S3A-2A-3A"
LAB_ID_S2B_1A_1A = "S2B-1A-1A"
LAB_ID_S2B_1A_2A = "S2B-1A-2A"
LAB_ID_S2B_2A_1A = "S2B-2A-1A"
LAB_ID_S2B_2A_2A = "S2B-2A-2A"

SCENARIO_SHADOW_VERIFY_CHRONICLE_ENTRIES = "shadow_verify_chronicle_entries"
SCENARIO_SHADOW_VERIFY_SEARCH_INDEX = "shadow_verify_search_index"
SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_WRITE_GATE = "shadow_verify_search_index_write_gate"
SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_PAGING_STABILITY = "shadow_verify_search_index_paging_stability"
SCENARIO_ES_WRITE_BLOCK_4XX = "es_write_block_4xx"
SCENARIO_ES_429_INJECT = "es_429_inject"
SCENARIO_ES_DOWN_CONNECT = "es_down_connect"
SCENARIO_ES_BULK_PARTIAL = "es_bulk_partial"
SCENARIO_DB_CLAIM_CONTENTION = "db_claim_contention"
SCENARIO_STUCK_RECLAIM = "stuck_reclaim"
SCENARIO_DUPLICATE_DELIVERY = "duplicate_delivery"
SCENARIO_PROJECTION_VERSION = "projection_version"
SCENARIO_COLLECTOR_DOWN = "collector_down"

SCENARIO_SHADOW_VERIFY_SHARED_KEYS = "shadow_verify_shared_keys"
SCENARIO_SHADOW_VERIFY_DUAL_RUN_READINESS_GATE = "shadow_verify_dual_run_readiness_gate"
SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE1 = "shadow_verify_dual_run_stage1"
SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE2 = "shadow_verify_dual_run_stage2"
SCENARIO_SHADOW_VERIFY_DUAL_RUN_WINDOW = "shadow_verify_dual_run_window"
SCENARIO_SHADOW_VERIFY_CANARY_DUAL_WRITE = "shadow_verify_canary_dual_write"
SCENARIO_SHADOW_VERIFY_DUAL_WRITE_SAMPLING = "shadow_verify_dual_write_sampling"

# Keep in sync with backend/scripts/legacy/search_outbox_worker.py
SEARCH_OUTBOX_OBS_SCHEMA_VERSION = "labs-009-v2"


def _now_run_id() -> str:
    # local time is fine for manual runs; keep it filesystem-safe
    return time.strftime("%Y%m%dT%H%M%S")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _read_env_file(path: Path) -> dict[str, str]:
    """Very small .env parser (KEY=VALUE, supports quotes, ignores comments)."""

    if not path.exists():
        raise FileNotFoundError(str(path))

    env: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if (len(value) >= 2) and ((value[0] == value[-1] == '"') or (value[0] == value[-1] == "'")):
            value = value[1:-1]
        env[key] = value
    return env


def _load_env(*, env_file: str | None) -> dict[str, str]:
    env = os.environ.copy()
    if env_file:
        env_path = (REPO_ROOT / env_file).resolve() if not Path(env_file).is_absolute() else Path(env_file)
        env.update(_read_env_file(env_path))
    return env


def _default_labs_auto_run_dir(*, scenario: str, run_id: str) -> Path:
    return LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / scenario / run_id


def _default_s2b_auto_run_dir(*, lab_id: str, scenario: str, run_id: str) -> Path:
    return LABS_SNAPSHOT_ROOT / "auto" / lab_id / scenario / run_id


def _latest_child_dir(base: Path) -> Path | None:
    if not base.exists():
        return None
    children = [p for p in base.iterdir() if p.is_dir()]
    if not children:
        return None
    return sorted(children, key=lambda p: p.name, reverse=True)[0]


def _http_json(
    method: str,
    url: str,
    *,
    body: dict[str, object] | None = None,
    timeout_s: float = 5.0,
) -> tuple[int, str]:
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url=url, data=data, method=method.upper(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310
            payload = resp.read().decode("utf-8", errors="replace")
            return int(resp.status), payload
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace") if getattr(exc, "fp", None) else str(exc)
        return int(getattr(exc, "code", 0) or 0), payload


def _es_set_index_write_block(*, es_url: str, index: str, enabled: bool) -> tuple[int, str]:
    es_url = es_url.strip().rstrip("/")
    index = index.strip()
    url = f"{es_url}/{index}/_settings"
    return _http_json("PUT", url, body={"index": {"blocks": {"write": bool(enabled)}}}, timeout_s=5.0)


def _es_create_index_if_missing(*, es_url: str, index: str) -> tuple[int, str]:
    """Create index if it does not exist.

    Returns (status, payload) from ES.
    - 200/201: created
    - 400: already exists (treated as ok by caller)
    """

    es_url = es_url.strip().rstrip("/")
    index = index.strip()
    url = f"{es_url}/{index}"
    return _http_json("PUT", url, body=None, timeout_s=5.0)


def _scrape_metrics_text(*, port: int, timeout_s: float = 2.0) -> str:
    url = f"http://localhost:{int(port)}/metrics"
    req = urllib.request.Request(url=url, headers={"Accept": "text/plain"})
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310
        return resp.read().decode("utf-8", errors="replace")


def _prom_parse_counter_sum(text: str, metric: str, *, labels: dict[str, str] | None = None) -> float:
    """Very small Prometheus text parser: sum matching samples for a counter metric."""

    want = labels or {}
    total = 0.0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith(metric):
            continue

        # metric{a="b"} 123 or metric 123
        name_and_labels, *rest = line.split(None, 1)
        if not rest:
            continue
        value_str = rest[0].strip().split()[0]

        lbls: dict[str, str] = {}
        if "{" in name_and_labels and name_and_labels.endswith("}"):
            inside = name_and_labels.split("{", 1)[1][:-1]
            # naive split is ok because our labels are simple
            for part in inside.split(","):
                part = part.strip()
                if not part or "=" not in part:
                    continue
                k, v = part.split("=", 1)
                k = k.strip()
                v = v.strip()
                if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
                    v = v[1:-1]
                lbls[k] = v

        ok = True
        for k, v in want.items():
            if lbls.get(k) != v:
                ok = False
                break
        if not ok:
            continue

        try:
            total += float(value_str)
        except ValueError:
            continue

    return float(total)


def _default_labs009_expb_outdir(run_id: str) -> Path:
    return LABS_SNAPSHOT_ROOT / "manual" / "_lab-S3A-2A-3A-expB" / run_id


def _python_exe() -> str:
    # Prefer a repo-local venv if present, but only for the current OS.
    # This avoids WSL calling Windows python.exe with POSIX paths (exit code 2).
    if os.getenv("VIRTUAL_ENV"):
        return sys.executable

    if os.name == "nt":
        win_venv = REPO_ROOT / ".venv" / "Scripts" / "python.exe"
        if win_venv.exists():
            return str(win_venv)
        return sys.executable

    unix_venv = REPO_ROOT / ".venv" / "bin" / "python"
    if unix_venv.exists():
        return str(unix_venv)
    return sys.executable


def _run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> int:
    print("[scripts] run:", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(cwd) if cwd else None, env=env)


def _docker_compose(*, args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    cmd = ["docker", "compose"] + args
    print("[scripts] run:", " ".join(cmd))
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=False)


def _prom_sum_reasons(text: str, metric: str, *, reasons: list[str]) -> float:
    return float(sum(_prom_parse_counter_sum(text, metric, labels={"reason": r}) for r in reasons))


def _extract_last_claim_batch_id(log_path: Path) -> str | None:
    if not log_path.exists():
        return None
    try:
        lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return None
    rx = re.compile(r'"claim_batch_id"\s*:\s*"([^"]+)"')
    for line in reversed(lines):
        m = rx.search(line)
        if m:
            return m.group(1)
    return None


def _with_backend_pythonpath(env: dict[str, str]) -> dict[str, str]:
    backend_path = str(REPO_ROOT / "backend")
    existing = env.get("PYTHONPATH") or ""
    parts = [p for p in existing.split(os.pathsep) if p]
    if backend_path not in parts:
        parts.insert(0, backend_path)
    env["PYTHONPATH"] = os.pathsep.join(parts)
    return env


def _parse_last_json_line(text: str) -> dict[str, object] | None:
    if not text:
        return None
    for raw in reversed(text.splitlines()):
        line = (raw or "").strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if isinstance(obj, dict):
            return obj
    return None


def _read_json_file(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None


def _cmd_labs_shadow_verify_chronicle_entries(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_s2b_auto_run_dir(
        lab_id=LAB_ID_S2B_1A_1A,
        scenario=SCENARIO_SHADOW_VERIFY_CHRONICLE_ENTRIES,
        run_id=run_id,
    )
    _ensure_dir(outdir)

    env = _load_env(env_file=args.env_file)
    database_url = (args.database_url or env.get("DATABASE_URL") or "").strip()
    if not database_url:
        print("[labs shadow-verify-chronicle-entries] DATABASE_URL is required (via env or --database-url)")
        return 2

    book_id = (args.book_id or "").strip() or None
    if book_id is not None:
        try:
            uuid.UUID(book_id)
        except ValueError:
            print(f"[labs shadow-verify-chronicle-entries] invalid --book-id: {book_id}")
            return 2

    engine = create_engine(database_url)
    with engine.connect() as conn:
        if book_id is None:
            events_total = int(conn.execute(text("SELECT COUNT(*) FROM chronicle_events")).scalar() or 0)
            entries_total = int(conn.execute(text("SELECT COUNT(*) FROM chronicle_entries")).scalar() or 0)
            missing_entries = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_events e
                        LEFT JOIN chronicle_entries p ON p.id = e.id
                        WHERE p.id IS NULL
                        """
                    )
                ).scalar()
                or 0
            )
            extra_entries = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_entries p
                        LEFT JOIN chronicle_events e ON e.id = p.id
                        WHERE e.id IS NULL
                        """
                    )
                ).scalar()
                or 0
            )
            mismatched_book_id = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_events e
                        JOIN chronicle_entries p ON p.id = e.id
                        WHERE p.book_id <> e.book_id
                        """
                    )
                ).scalar()
                or 0
            )
            scope = "all"
        else:
            events_total = int(
                conn.execute(
                    text("SELECT COUNT(*) FROM chronicle_events WHERE book_id = :book_id"),
                    {"book_id": book_id},
                ).scalar()
                or 0
            )
            entries_total = int(
                conn.execute(
                    text("SELECT COUNT(*) FROM chronicle_entries WHERE book_id = :book_id"),
                    {"book_id": book_id},
                ).scalar()
                or 0
            )
            missing_entries = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_events e
                        LEFT JOIN chronicle_entries p ON p.id = e.id
                        WHERE e.book_id = :book_id AND p.id IS NULL
                        """
                    ),
                    {"book_id": book_id},
                ).scalar()
                or 0
            )
            extra_entries = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_entries p
                        LEFT JOIN chronicle_events e ON e.id = p.id
                        WHERE p.book_id = :book_id AND e.id IS NULL
                        """
                    ),
                    {"book_id": book_id},
                ).scalar()
                or 0
            )
            mismatched_book_id = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_events e
                        JOIN chronicle_entries p ON p.id = e.id
                        WHERE e.book_id = :book_id AND p.book_id <> e.book_id
                        """
                    ),
                    {"book_id": book_id},
                ).scalar()
                or 0
            )
            scope = f"book:{book_id}"

    ok = (missing_entries == 0) and (extra_entries == 0) and (mismatched_book_id == 0)
    result = {
        "lab_id": LAB_ID_S2B_1A_1A,
        "scenario": SCENARIO_SHADOW_VERIFY_CHRONICLE_ENTRIES,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "events_total": events_total,
        "entries_total": entries_total,
        "missing_entries": missing_entries,
        "extra_entries": extra_entries,
        "mismatched_book_id": mismatched_book_id,
        "ok": bool(ok),
    }

    (outdir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("labs-010.shadow_verify_chronicle_entries")
    print(f"scope={scope}")
    print(f"events_total={events_total}")
    print(f"entries_total={entries_total}")
    print(f"missing_entries={missing_entries}")
    print(f"extra_entries={extra_entries}")
    print(f"mismatched_book_id={mismatched_book_id}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def _cmd_labs_shadow_verify_search_index(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_s2b_auto_run_dir(
        lab_id=LAB_ID_S2B_1A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_SEARCH_INDEX,
        run_id=run_id,
    )
    _ensure_dir(outdir)

    env = _load_env(env_file=args.env_file)
    database_url = (args.database_url or env.get("DATABASE_URL") or "").strip()
    if not database_url:
        print("[labs shadow-verify-search-index] DATABASE_URL is required (via env or --database-url)")
        return 2

    library_id = (args.library_id or "").strip() or None
    if library_id is not None:
        try:
            uuid.UUID(library_id)
        except ValueError:
            print(f"[labs shadow-verify-search-index] invalid --library-id: {library_id}")
            return 2

    engine = create_engine(database_url)
    with engine.connect() as conn:
        if library_id is None:
            scope = "all"
            blocks_total = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM blocks bl
                        JOIN books bo ON bo.id = bl.book_id
                        WHERE bl.soft_deleted_at IS NULL
                          AND bo.soft_deleted_at IS NULL
                        """
                    )
                ).scalar()
                or 0
            )
            blocks_index_total = int(
                conn.execute(text("SELECT COUNT(*) FROM search_index WHERE entity_type = 'block' ")).scalar() or 0
            )
            blocks_missing = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM blocks bl
                        JOIN books bo ON bo.id = bl.book_id
                        LEFT JOIN search_index si
                          ON si.entity_type = 'block'
                         AND si.entity_id = bl.id
                        WHERE bl.soft_deleted_at IS NULL
                          AND bo.soft_deleted_at IS NULL
                          AND si.entity_id IS NULL
                        """
                    )
                ).scalar()
                or 0
            )
            blocks_extra = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        LEFT JOIN blocks bl ON bl.id = si.entity_id
                        LEFT JOIN books bo ON bo.id = bl.book_id
                        WHERE si.entity_type = 'block'
                          AND (
                            bl.id IS NULL
                            OR bl.soft_deleted_at IS NOT NULL
                            OR bo.id IS NULL
                            OR bo.soft_deleted_at IS NOT NULL
                          )
                        """
                    )
                ).scalar()
                or 0
            )
            blocks_mismatched_library_id = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        JOIN blocks bl ON bl.id = si.entity_id
                        JOIN books bo ON bo.id = bl.book_id
                        WHERE si.entity_type = 'block'
                          AND bo.soft_deleted_at IS NULL
                          AND bl.soft_deleted_at IS NULL
                          AND (si.library_id IS DISTINCT FROM bo.library_id)
                        """
                    )
                ).scalar()
                or 0
            )

            books_total = int(conn.execute(text("SELECT COUNT(*) FROM books WHERE soft_deleted_at IS NULL")).scalar() or 0)
            books_index_total = int(conn.execute(text("SELECT COUNT(*) FROM search_index WHERE entity_type = 'book'")).scalar() or 0)
            books_missing = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM books bo
                        LEFT JOIN search_index si
                          ON si.entity_type = 'book'
                         AND si.entity_id = bo.id
                        WHERE bo.soft_deleted_at IS NULL
                          AND si.entity_id IS NULL
                        """
                    )
                ).scalar()
                or 0
            )
            books_extra = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        LEFT JOIN books bo ON bo.id = si.entity_id
                        WHERE si.entity_type = 'book'
                          AND (bo.id IS NULL OR bo.soft_deleted_at IS NOT NULL)
                        """
                    )
                ).scalar()
                or 0
            )
            books_mismatched_library_id = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        JOIN books bo ON bo.id = si.entity_id
                        WHERE si.entity_type = 'book'
                          AND bo.soft_deleted_at IS NULL
                          AND (si.library_id IS DISTINCT FROM bo.library_id)
                        """
                    )
                ).scalar()
                or 0
            )
        else:
            scope = f"library:{library_id}"
            params = {"library_id": library_id}

            blocks_total = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM blocks bl
                        JOIN books bo ON bo.id = bl.book_id
                        WHERE bl.soft_deleted_at IS NULL
                          AND bo.soft_deleted_at IS NULL
                          AND bo.library_id = :library_id
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            blocks_index_total = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_index
                        WHERE entity_type = 'block'
                          AND library_id = :library_id
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            blocks_missing = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM blocks bl
                        JOIN books bo ON bo.id = bl.book_id
                        LEFT JOIN search_index si
                          ON si.entity_type = 'block'
                         AND si.entity_id = bl.id
                        WHERE bl.soft_deleted_at IS NULL
                          AND bo.soft_deleted_at IS NULL
                          AND bo.library_id = :library_id
                          AND si.entity_id IS NULL
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            blocks_extra = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        LEFT JOIN blocks bl ON bl.id = si.entity_id
                        LEFT JOIN books bo ON bo.id = bl.book_id
                        WHERE si.entity_type = 'block'
                          AND si.library_id = :library_id
                          AND (
                            bl.id IS NULL
                            OR bl.soft_deleted_at IS NOT NULL
                            OR bo.id IS NULL
                            OR bo.soft_deleted_at IS NOT NULL
                            OR bo.library_id <> :library_id
                          )
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            blocks_mismatched_library_id = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        JOIN blocks bl ON bl.id = si.entity_id
                        JOIN books bo ON bo.id = bl.book_id
                        WHERE si.entity_type = 'block'
                          AND bo.library_id = :library_id
                          AND bo.soft_deleted_at IS NULL
                          AND bl.soft_deleted_at IS NULL
                          AND (si.library_id IS DISTINCT FROM bo.library_id)
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )

            books_total = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM books
                        WHERE soft_deleted_at IS NULL
                          AND library_id = :library_id
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            books_index_total = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_index
                        WHERE entity_type = 'book'
                          AND library_id = :library_id
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            books_missing = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM books bo
                        LEFT JOIN search_index si
                          ON si.entity_type = 'book'
                         AND si.entity_id = bo.id
                        WHERE bo.soft_deleted_at IS NULL
                          AND bo.library_id = :library_id
                          AND si.entity_id IS NULL
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            books_extra = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        LEFT JOIN books bo ON bo.id = si.entity_id
                        WHERE si.entity_type = 'book'
                          AND si.library_id = :library_id
                          AND (
                            bo.id IS NULL
                            OR bo.soft_deleted_at IS NOT NULL
                            OR bo.library_id <> :library_id
                          )
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            books_mismatched_library_id = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        JOIN books bo ON bo.id = si.entity_id
                        WHERE si.entity_type = 'book'
                          AND bo.library_id = :library_id
                          AND bo.soft_deleted_at IS NULL
                          AND (si.library_id IS DISTINCT FROM bo.library_id)
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )

        tags_total = int(conn.execute(text("SELECT COUNT(*) FROM tags WHERE deleted_at IS NULL")).scalar() or 0)
        tags_index_total = int(conn.execute(text("SELECT COUNT(*) FROM search_index WHERE entity_type = 'tag'")).scalar() or 0)
        tags_missing = int(
            conn.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM tags t
                    LEFT JOIN search_index si
                      ON si.entity_type = 'tag'
                     AND si.entity_id = t.id
                    WHERE t.deleted_at IS NULL
                      AND si.entity_id IS NULL
                    """
                )
            ).scalar()
            or 0
        )
        tags_extra = int(
            conn.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM search_index si
                    LEFT JOIN tags t ON t.id = si.entity_id
                    WHERE si.entity_type = 'tag'
                      AND (t.id IS NULL OR t.deleted_at IS NOT NULL)
                    """
                )
            ).scalar()
            or 0
        )
        tags_invalid_library_id = int(
            conn.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM search_index
                    WHERE entity_type = 'tag'
                      AND library_id IS NOT NULL
                    """
                )
            ).scalar()
            or 0
        )

        outbox_total = int(conn.execute(text("SELECT COUNT(*) FROM search_outbox_events")).scalar() or 0)
        outbox_pending = int(conn.execute(text("SELECT COUNT(*) FROM search_outbox_events WHERE status = 'pending'")).scalar() or 0)
        outbox_processing = int(
            conn.execute(text("SELECT COUNT(*) FROM search_outbox_events WHERE status = 'processing'")).scalar() or 0
        )
        outbox_done = int(conn.execute(text("SELECT COUNT(*) FROM search_outbox_events WHERE status = 'done'")).scalar() or 0)
        outbox_failed = int(conn.execute(text("SELECT COUNT(*) FROM search_outbox_events WHERE status = 'failed'")).scalar() or 0)

    ok = (
        (blocks_missing == 0)
        and (blocks_extra == 0)
        and (blocks_mismatched_library_id == 0)
        and (books_missing == 0)
        and (books_extra == 0)
        and (books_mismatched_library_id == 0)
        and (tags_missing == 0)
        and (tags_extra == 0)
        and (tags_invalid_library_id == 0)
    )

    result = {
        "lab_id": LAB_ID_S2B_1A_2A,
        "scenario": SCENARIO_SHADOW_VERIFY_SEARCH_INDEX,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "blocks_total": blocks_total,
        "blocks_index_total": blocks_index_total,
        "blocks_missing": blocks_missing,
        "blocks_extra": blocks_extra,
        "blocks_mismatched_library_id": blocks_mismatched_library_id,
        "books_total": books_total,
        "books_index_total": books_index_total,
        "books_missing": books_missing,
        "books_extra": books_extra,
        "books_mismatched_library_id": books_mismatched_library_id,
        "tags_total": tags_total,
        "tags_index_total": tags_index_total,
        "tags_missing": tags_missing,
        "tags_extra": tags_extra,
        "tags_invalid_library_id": tags_invalid_library_id,
        "outbox_total": outbox_total,
        "outbox_pending": outbox_pending,
        "outbox_processing": outbox_processing,
        "outbox_done": outbox_done,
        "outbox_failed": outbox_failed,
        "ok": bool(ok),
    }

    (outdir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("labs-011.shadow_verify_search_index")
    print(f"scope={scope}")
    print(f"blocks_total={blocks_total}")
    print(f"blocks_index_total={blocks_index_total}")
    print(f"blocks_missing={blocks_missing}")
    print(f"blocks_extra={blocks_extra}")
    print(f"blocks_mismatched_library_id={blocks_mismatched_library_id}")
    print(f"books_total={books_total}")
    print(f"books_index_total={books_index_total}")
    print(f"books_missing={books_missing}")
    print(f"books_extra={books_extra}")
    print(f"books_mismatched_library_id={books_mismatched_library_id}")
    print(f"tags_total={tags_total}")
    print(f"tags_index_total={tags_index_total}")
    print(f"tags_missing={tags_missing}")
    print(f"tags_extra={tags_extra}")
    print(f"tags_invalid_library_id={tags_invalid_library_id}")
    print(f"outbox_total={outbox_total}")
    print(f"outbox_pending={outbox_pending}")
    print(f"outbox_processing={outbox_processing}")
    print(f"outbox_done={outbox_done}")
    print(f"outbox_failed={outbox_failed}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def _cmd_labs_shadow_verify_search_index_write_gate(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_s2b_auto_run_dir(
        lab_id=LAB_ID_S2B_2A_1A,
        scenario=SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_WRITE_GATE,
        run_id=run_id,
    )
    _ensure_dir(outdir)

    env = _load_env(env_file=args.env_file)
    database_url = (args.database_url or env.get("DATABASE_URL") or "").strip()
    if not database_url:
        print("[labs shadow-verify-search-index-write-gate] DATABASE_URL is required (via env or --database-url)")
        return 2

    library_id = (args.library_id or "").strip() or None
    if library_id is not None:
        try:
            uuid.UUID(library_id)
        except ValueError:
            print(f"[labs shadow-verify-search-index-write-gate] invalid --library-id: {library_id}")
            return 2

    _wg_registry.load_builtin_scenarios()
    handler = _wg_registry.get(SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_WRITE_GATE)

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_WRITE_GATE,
            "scope_id": LAB_ID_S2B_2A_1A,
            "run_id": run_id,
            "outdir": str(outdir),
            "database_url": database_url,
            "library_id": library_id,
        }
    )
    inputs = DrillInputs.model_validate(input_payload)
    drill = handler(inputs)
    result = drill.meta or {}
    write_json(outdir / "_result.json", result)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or "")
    duplicates_groups_total = int(result.get("duplicates_groups_total") or 0)
    duplicates_extra_rows_total = int(result.get("duplicates_extra_rows_total") or 0)
    duplicates_groups_scoped = result.get("duplicates_groups_scoped")
    duplicates_extra_rows_scoped = result.get("duplicates_extra_rows_scoped")

    print("labs-012.shadow_verify_search_index_write_gate")
    print(f"scope={scope}")
    print(f"duplicates_groups_total={duplicates_groups_total}")
    print(f"duplicates_extra_rows_total={duplicates_extra_rows_total}")
    if duplicates_groups_scoped is not None:
        print(f"duplicates_groups_scoped={duplicates_groups_scoped}")
    if duplicates_extra_rows_scoped is not None:
        print(f"duplicates_extra_rows_scoped={duplicates_extra_rows_scoped}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def _ensure_search_index_min_rows(
    *,
    conn,
    ensure_min_rows: int,
    library_id: str | None,
    seed_entity_type: str = "seed",
    seed_text_prefix: str | None = None,
) -> int:
    if ensure_min_rows <= 0:
        return 0

    where_parts: list[str] = []
    params: dict[str, object] = {}
    if library_id is not None:
        where_parts.append("library_id = :library_id")
        params["library_id"] = library_id
    where_sql = ("WHERE " + " AND ".join(where_parts)) if where_parts else ""

    existing = int(conn.execute(text(f"SELECT COUNT(*) FROM search_index {where_sql}"), params).scalar() or 0)
    need = int(ensure_min_rows) - existing
    if need <= 0:
        return 0

    now = datetime.now(timezone.utc)
    rows = []
    for i in range(need):
        prefix = seed_text_prefix if seed_text_prefix is not None else f"seed:{seed_entity_type}:"
        rows.append(
            {
                "id": str(uuid.uuid4()),
                "entity_type": seed_entity_type,
                "library_id": library_id,
                "entity_id": str(uuid.uuid4()),
                "text": f"{prefix}{i}",
                "snippet": None,
                "rank_score": 0.0,
                "created_at": now,
                "updated_at": now,
                "event_version": int(i + 1),
            }
        )

    conn.execute(
        text(
            """
            INSERT INTO search_index
              (id, entity_type, library_id, entity_id, text, snippet, rank_score, created_at, updated_at, event_version)
            VALUES
              (:id, :entity_type, :library_id, :entity_id, :text, :snippet, :rank_score, :created_at, :updated_at, :event_version)
            """
        ),
        rows,
    )
    conn.commit()
    return int(need)


def _cmd_labs_shadow_verify_search_index_paging_stability(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_s2b_auto_run_dir(
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_PAGING_STABILITY,
        run_id=run_id,
    )
    _ensure_dir(outdir)

    env = _load_env(env_file=args.env_file)
    database_url = (args.database_url or env.get("DATABASE_URL") or "").strip()
    if not database_url:
        print(
            "[labs shadow-verify-search-index-paging-stability] DATABASE_URL is required (via env or --database-url)"
        )
        return 2

    library_id = (args.library_id or "").strip() or None
    if library_id is not None:
        try:
            uuid.UUID(library_id)
        except ValueError:
            print(f"[labs shadow-verify-search-index-paging-stability] invalid --library-id: {library_id}")
            return 2

    page_size = int(args.page_size)
    pages_checked = int(args.pages_checked)
    ensure_min_rows = int(args.ensure_min_rows)
    if page_size <= 0:
        print("[labs shadow-verify-search-index-paging-stability] --page-size must be > 0")
        return 2
    if pages_checked < 2:
        print("[labs shadow-verify-search-index-paging-stability] --pages-checked must be >= 2")
        return 2
    if ensure_min_rows < 0:
        print("[labs shadow-verify-search-index-paging-stability] --ensure-min-rows must be >= 0")
        return 2

    _wg_registry.load_builtin_scenarios()
    handler = _wg_registry.get(SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_PAGING_STABILITY)

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_PAGING_STABILITY,
            "scope_id": LAB_ID_S2B_2A_2A,
            "run_id": run_id,
            "outdir": str(outdir),
            "database_url": database_url,
            "library_id": library_id,
        }
    )
    inputs = DrillInputs.model_validate(input_payload)
    drill = handler(inputs)
    result = drill.meta or {}
    write_json(outdir / "_result.json", result)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or "")
    order_key = result.get("order_key")
    rows_total = int(result.get("rows_total") or 0)
    inserted_rows = int(result.get("seed_rows_inserted") or 0)
    data_sufficient = bool(result.get("data_sufficient"))
    duplicates_across_pages_total = int(result.get("duplicates_across_pages_total") or 0)
    ordering_ok = bool(result.get("ordering_ok"))
    pages_returned = int(result.get("pages_returned") or 0)

    print("labs-013.shadow_verify_search_index_paging_stability")
    print(f"scope={scope}")
    print(f"order_key={order_key}")
    print(f"page_size={page_size}")
    print(f"pages_checked={pages_checked}")
    print(f"pages_returned={pages_returned}")
    print(f"rows_total={rows_total}")
    print(f"ensure_min_rows={ensure_min_rows}")
    print(f"seed_rows_inserted={inserted_rows}")
    print(f"data_sufficient={data_sufficient}")
    print(f"duplicates_across_pages_total={duplicates_across_pages_total}")
    print(f"ordering_ok={ordering_ok}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def _cmd_labs_shadow_verify_shared_keys(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_s2b_auto_run_dir(
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_SHARED_KEYS,
        run_id=run_id,
    )
    _ensure_dir(outdir)

    env = _load_env(env_file=args.env_file)
    database_url = (args.database_url or env.get("DATABASE_URL") or "").strip()
    if not database_url:
        print("[labs shadow-verify-shared-keys] DATABASE_URL is required (via env or --database-url)")
        return 2

    library_id = (args.library_id or "").strip() or None
    if library_id is not None:
        try:
            uuid.UUID(library_id)
        except ValueError:
            print(f"[labs shadow-verify-shared-keys] invalid --library-id: {library_id}")
            return 2

    ensure_min_rows = int(args.ensure_min_rows)
    if ensure_min_rows < 0:
        print("[labs shadow-verify-shared-keys] --ensure-min-rows must be >= 0")
        return 2

    _wg_registry.load_builtin_scenarios()
    handler = _wg_registry.get(SCENARIO_SHADOW_VERIFY_SHARED_KEYS)

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": SCENARIO_SHADOW_VERIFY_SHARED_KEYS,
            "scope_id": LAB_ID_S2B_2A_2A,
            "run_id": run_id,
            "outdir": str(outdir),
            "database_url": database_url,
            "library_id": library_id,
        }
    )
    inputs = DrillInputs.model_validate(input_payload)
    drill = handler(inputs)
    result = drill.meta or {}
    write_json(outdir / "_result.json", result)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or "")
    inserted_rows = int(result.get("seed_rows_inserted") or 0)
    shared_keys = result.get("shared_keys") or {}
    samples = list(shared_keys.get("samples") or [])

    print("labs-014.shadow_verify_shared_keys")
    print(f"scope={scope}")
    print(f"ensure_min_rows={ensure_min_rows}")
    print(f"seed_rows_inserted={inserted_rows}")
    print(f"samples_total={len(samples)}")
    if samples:
        print(f"sample_entity_type={samples[0]['entity_type']}")
        print(f"sample_entity_id={samples[0]['entity_id']}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def _cmd_labs_shadow_verify_dual_run_readiness_gate(args: argparse.Namespace) -> int:
    """Dry-run gate for 2A: aggregate the prerequisites into one drill evidence bundle.

    This does NOT perform any external writes; it only runs verification-style checks and
    produces a single _result.json that links to sub-results.
    """

    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_s2b_auto_run_dir(
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_DUAL_RUN_READINESS_GATE,
        run_id=run_id,
    )
    _ensure_dir(outdir)

    env = _load_env(env_file=args.env_file)
    database_url = (args.database_url or env.get("DATABASE_URL") or "").strip()
    if not database_url:
        print("[labs shadow-verify-dual-run-readiness-gate] DATABASE_URL is required (via env or --database-url)")
        return 2

    library_id = (args.library_id or "").strip() or None
    if library_id is not None:
        try:
            uuid.UUID(library_id)
        except ValueError:
            print(f"[labs shadow-verify-dual-run-readiness-gate] invalid --library-id: {library_id}")
            return 2

    page_size = int(args.page_size)
    pages_checked = int(args.pages_checked)
    ensure_min_rows_paging = int(args.ensure_min_rows_paging)
    ensure_min_rows_keys = int(args.ensure_min_rows_keys)
    if page_size <= 0:
        print("[labs shadow-verify-dual-run-readiness-gate] --page-size must be > 0")
        return 2
    if pages_checked < 2:
        print("[labs shadow-verify-dual-run-readiness-gate] --pages-checked must be >= 2")
        return 2
    if ensure_min_rows_paging < 0 or ensure_min_rows_keys < 0:
        print("[labs shadow-verify-dual-run-readiness-gate] --ensure-min-rows-* must be >= 0")
        return 2

    scope = "all" if library_id is None else f"library:{library_id}"

    _wg_registry.load_builtin_scenarios()
    handler = _wg_registry.get(SCENARIO_SHADOW_VERIFY_DUAL_RUN_READINESS_GATE)

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": SCENARIO_SHADOW_VERIFY_DUAL_RUN_READINESS_GATE,
            "scope_id": LAB_ID_S2B_2A_2A,
            "run_id": run_id,
            "outdir": str(outdir),
            "env": env,
            "database_url": database_url,
            "library_id": library_id,
            "page_size": page_size,
            "pages_checked": pages_checked,
            "ensure_min_rows_paging": ensure_min_rows_paging,
            "ensure_min_rows_keys": ensure_min_rows_keys,
        }
    )

    inputs = DrillInputs.model_validate(input_payload)
    drill = handler(inputs)
    result = drill.meta or {}
    write_json(outdir / "_result.json", result)

    ok = bool(result.get("ok"))

    print("labs-015.shadow_verify_dual_run_readiness_gate")
    print(f"scope={scope}")
    print(f"page_size={page_size}")
    print(f"pages_checked={pages_checked}")
    print(f"ensure_min_rows_paging={ensure_min_rows_paging}")
    print(f"ensure_min_rows_keys={ensure_min_rows_keys}")
    print(f"ok={ok}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def _cmd_labs_shadow_verify_dual_run_stage1(args: argparse.Namespace) -> int:
    """True dual-run (stage1) drill: compare Postgres vs Elasticsearch results.

    CI-safe path:
    - Seed a small, drill-scoped set of `search_index` rows as `entity_type='block'`.
    - Backfill Elasticsearch from Postgres using the legacy backfill script.
    - Query both stores with a deterministic token and compare ordered candidates.

    This does NOT run the outbox worker; it's a parity drill for read-path dual-run.
    """

    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_s2b_auto_run_dir(
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE1,
        run_id=run_id,
    )
    _ensure_dir(outdir)

    env = _load_env(env_file=args.env_file)
    database_url = (args.database_url or env.get("DATABASE_URL") or "").strip()
    if not database_url:
        print("[labs shadow-verify-dual-run-stage1] DATABASE_URL is required (via env or --database-url)")
        return 2

    library_id = (args.library_id or "").strip() or None
    if library_id is not None:
        try:
            uuid.UUID(library_id)
        except ValueError:
            print(f"[labs shadow-verify-dual-run-stage1] invalid --library-id: {library_id}")
            return 2

    ensure_min_rows = int(args.ensure_min_rows)
    candidate_limit = int(args.candidate_limit)
    backfill_batch_size = int(args.backfill_batch_size)
    strategy = str(args.strategy)

    if ensure_min_rows < 0:
        print("[labs shadow-verify-dual-run-stage1] --ensure-min-rows must be >= 0")
        return 2
    if candidate_limit <= 0:
        print("[labs shadow-verify-dual-run-stage1] --candidate-limit must be > 0")
        return 2
    if backfill_batch_size <= 0:
        print("[labs shadow-verify-dual-run-stage1] --backfill-batch-size must be > 0")
        return 2
    if strategy not in {"soft", "strict"}:
        print("[labs shadow-verify-dual-run-stage1] --strategy must be one of: soft, strict")
        return 2

    es_url = (args.es_url or env.get("ELASTIC_URL") or "http://127.0.0.1:19200").strip().rstrip("/")
    token_default = "dualrun" + re.sub(r"[^0-9A-Za-z]+", "", run_id)
    token = (args.token or token_default).strip() or token_default

    def _sanitize_index_name(name: str) -> str:
        safe = re.sub(r"[^a-z0-9_\-]+", "-", name.lower()).strip("-_")
        safe = re.sub(r"-+", "-", safe)
        if not safe:
            safe = "wordloom-search-index"
        return safe[:80]

    es_index = (
        args.es_index
        or env.get("ELASTIC_INDEX")
        or _sanitize_index_name(f"wordloom-search-index-dualrun-{token}")
    ).strip()
    es_index = _sanitize_index_name(es_index)
    recreate_index = bool(args.recreate_index)

    _wg_registry.load_builtin_scenarios()
    handler = _wg_registry.get(SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE1)

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE1,
            "scope_id": LAB_ID_S2B_2A_2A,
            "run_id": run_id,
            "outdir": str(outdir),
            "env": env,
            "database_url": database_url,
            "library_id": library_id,
            "ensure_min_rows": ensure_min_rows,
            "candidate_limit": candidate_limit,
            "backfill_batch_size": backfill_batch_size,
            "strategy": strategy,
            "es_url": es_url,
            "token": token,
            "es_index": es_index,
            "recreate_index": recreate_index,
        }
    )
    inputs = DrillInputs.model_validate(input_payload)
    drill = handler(inputs)
    result = drill.meta or {}
    write_json(outdir / "_result.json", result)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or "")

    inputs_obj = result.get("inputs") if isinstance(result, dict) else None
    if not isinstance(inputs_obj, dict):
        inputs_obj = {}

    token = str(inputs_obj.get("token") or token)
    strategy = str(inputs_obj.get("strategy") or strategy)

    seed_rows_inserted = int(result.get("seed_rows_inserted") or 0)

    pg_candidates: list[object] = []
    postgres_obj = result.get("postgres")
    if isinstance(postgres_obj, dict):
        cands = postgres_obj.get("candidates")
        if isinstance(cands, list):
            pg_candidates = cands
    pg_candidates_total = int(len(pg_candidates))

    es_obj = result.get("elasticsearch")
    es_health_ok = False
    backfill_ok = False
    backfill_exit_code = 0
    es_search_ok = False
    es_search_status = 0
    es_candidates_total = 0
    if isinstance(es_obj, dict):
        health = es_obj.get("health")
        if isinstance(health, dict):
            es_health_ok = bool(health.get("ok"))
        backfill = es_obj.get("backfill")
        if isinstance(backfill, dict):
            backfill_ok = bool(backfill.get("ok"))
            backfill_exit_code = int(backfill.get("exit_code") or 0)
        search = es_obj.get("search")
        if isinstance(search, dict):
            es_search_ok = bool(search.get("ok"))
            es_search_status = int(search.get("status") or 0)
            es_cands = search.get("candidates")
            if isinstance(es_cands, list):
                es_candidates_total = int(len(es_cands))

    parity_ok = False
    compare_obj = result.get("compare")
    if isinstance(compare_obj, dict):
        parity_ok = bool(compare_obj.get("parity_ok"))

    print("labs-018.shadow_verify_dual_run_stage1")
    print(f"scope={scope}")
    print(f"token={token}")
    print(f"ensure_min_rows={ensure_min_rows}")
    print(f"seed_rows_inserted={seed_rows_inserted}")
    print(f"pg_candidates_total={pg_candidates_total}")
    print(f"es_health_ok={es_health_ok}")
    print(f"backfill_ok={backfill_ok} (rc={backfill_exit_code})")
    print(f"es_search_ok={es_search_ok} (status={es_search_status})")
    print(f"es_candidates_total={es_candidates_total}")
    print(f"parity_ok={parity_ok} (strategy={strategy})")
    print(f"ok={ok}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def _cmd_labs_shadow_verify_dual_run_stage2(args: argparse.Namespace) -> int:
    """True dual-run (stage2) drill: run the real outbox worker, then verify parity.

    Stage1 verified read-path parity by backfilling ES from Postgres.
    Stage2 verifies the write-side projection path:
    - Seed a drill-scoped set of `search_index` rows (entity_type='block').
    - Enqueue matching `search_outbox_events` rows (op='upsert').
    - Start Elasticsearch and ensure the index mapping exists.
    - Run the search outbox worker in one-shot mode (exit when idle).
    - Refresh + query ES and compare ordered candidates with Postgres.
    """

    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_s2b_auto_run_dir(
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE2,
        run_id=run_id,
    )
    _ensure_dir(outdir)

    env = _load_env(env_file=args.env_file)
    database_url = (args.database_url or env.get("DATABASE_URL") or "").strip()
    if not database_url:
        print("[labs shadow-verify-dual-run-stage2] DATABASE_URL is required (via env or --database-url)")
        return 2

    library_id = (args.library_id or "").strip() or None
    if library_id is not None:
        try:
            uuid.UUID(library_id)
        except ValueError:
            print(f"[labs shadow-verify-dual-run-stage2] invalid --library-id: {library_id}")
            return 2

    ensure_min_rows = int(args.ensure_min_rows)
    candidate_limit = int(args.candidate_limit)
    strategy = str(args.strategy)
    worker_batch_size = int(args.worker_batch_size)
    worker_concurrency = int(args.worker_concurrency)
    worker_poll_interval_seconds = float(args.worker_poll_interval_seconds)
    worker_max_runtime_seconds = float(args.worker_max_runtime_seconds)
    worker_idle_polls_before_exit = int(args.worker_idle_polls_before_exit)

    if ensure_min_rows < 0:
        print("[labs shadow-verify-dual-run-stage2] --ensure-min-rows must be >= 0")
        return 2
    if candidate_limit <= 0:
        print("[labs shadow-verify-dual-run-stage2] --candidate-limit must be > 0")
        return 2
    if strategy not in {"soft", "strict"}:
        print("[labs shadow-verify-dual-run-stage2] --strategy must be one of: soft, strict")
        return 2
    if worker_batch_size <= 0:
        print("[labs shadow-verify-dual-run-stage2] --worker-batch-size must be > 0")
        return 2
    if worker_concurrency <= 0:
        print("[labs shadow-verify-dual-run-stage2] --worker-concurrency must be > 0")
        return 2
    if worker_poll_interval_seconds < 0:
        print("[labs shadow-verify-dual-run-stage2] --worker-poll-interval-seconds must be >= 0")
        return 2
    if worker_max_runtime_seconds <= 0:
        print("[labs shadow-verify-dual-run-stage2] --worker-max-runtime-seconds must be > 0")
        return 2
    if worker_idle_polls_before_exit <= 0:
        print("[labs shadow-verify-dual-run-stage2] --worker-idle-polls-before-exit must be > 0")
        return 2

    es_url = (args.es_url or env.get("ELASTIC_URL") or "http://127.0.0.1:19200").strip().rstrip("/")
    token_default = "dualrun" + re.sub(r"[^0-9A-Za-z]+", "", run_id)
    token = (args.token or token_default).strip() or token_default

    def _sanitize_index_name(name: str) -> str:
        safe = re.sub(r"[^a-z0-9_\-]+", "-", name.lower()).strip("-_")
        safe = re.sub(r"-+", "-", safe)
        if not safe:
            safe = "wordloom-search-index"
        return safe[:80]

    es_index = (
        args.es_index
        or env.get("ELASTIC_INDEX")
        or _sanitize_index_name(f"wordloom-search-index-dualrun-{token}")
    ).strip()
    es_index = _sanitize_index_name(es_index)
    recreate_index = bool(args.recreate_index)

    _wg_registry.load_builtin_scenarios()
    handler = _wg_registry.get(SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE2)

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE2,
            "scope_id": LAB_ID_S2B_2A_2A,
            "run_id": run_id,
            "outdir": str(outdir),
            "env": env,
            "database_url": database_url,
            "library_id": library_id,
            "ensure_min_rows": ensure_min_rows,
            "candidate_limit": candidate_limit,
            "strategy": strategy,
            "worker_batch_size": worker_batch_size,
            "worker_concurrency": worker_concurrency,
            "worker_poll_interval_seconds": worker_poll_interval_seconds,
            "worker_max_runtime_seconds": worker_max_runtime_seconds,
            "worker_idle_polls_before_exit": worker_idle_polls_before_exit,
            "es_url": es_url,
            "token": token,
            "es_index": es_index,
            "recreate_index": recreate_index,
        }
    )

    inputs = DrillInputs.model_validate(input_payload)
    drill = handler(inputs)
    result = drill.meta or {}
    write_json(outdir / "_result.json", result)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or ("all" if library_id is None else f"library:{library_id}"))

    inputs_obj = result.get("inputs") if isinstance(result, dict) else None
    if not isinstance(inputs_obj, dict):
        inputs_obj = {}

    token = str(inputs_obj.get("token") or token)
    strategy = str(inputs_obj.get("strategy") or strategy)

    seed_rows_inserted = int(result.get("seed_rows_inserted") or 0)

    pg_candidates: list[object] = []
    postgres_obj = result.get("postgres")
    if isinstance(postgres_obj, dict):
        cands = postgres_obj.get("candidates")
        if isinstance(cands, list):
            pg_candidates = cands
    pg_candidates_total = int(len(pg_candidates))

    outbox_enqueued_total = 0
    outbox_done = 0
    outbox_pending = 0
    outbox_processing = 0
    outbox_failed = 0
    outbox_obj = result.get("outbox")
    if isinstance(outbox_obj, dict):
        outbox_enqueued_total = int(outbox_obj.get("enqueued_total") or 0)
        status_counts = outbox_obj.get("status_counts")
        if isinstance(status_counts, dict):
            outbox_done = int(status_counts.get("done") or 0)
            outbox_pending = int(status_counts.get("pending") or 0)
            outbox_processing = int(status_counts.get("processing") or 0)
            outbox_failed = int(status_counts.get("failed") or 0)

    es_obj = result.get("elasticsearch")
    es_health_ok = False
    es_index_ok = False
    es_index_status = 0
    es_refresh_ok = False
    es_refresh_status = 0
    es_search_ok = False
    es_search_status = 0
    es_candidates_total = 0
    if isinstance(es_obj, dict):
        health = es_obj.get("health")
        if isinstance(health, dict):
            es_health_ok = bool(health.get("ok"))
        idx = es_obj.get("index")
        if isinstance(idx, dict):
            es_index_ok = bool(idx.get("ok"))
            es_index_status = int(idx.get("status") or 0)
        refresh = es_obj.get("refresh")
        if isinstance(refresh, dict):
            es_refresh_ok = bool(refresh.get("ok"))
            es_refresh_status = int(refresh.get("status") or 0)
        search = es_obj.get("search")
        if isinstance(search, dict):
            es_search_ok = bool(search.get("ok"))
            es_search_status = int(search.get("status") or 0)
            es_cands = search.get("candidates")
            if isinstance(es_cands, list):
                es_candidates_total = int(len(es_cands))

    worker_ok = False
    worker_exit_code = 0
    worker_runtime_s = 0.0
    worker_obj = result.get("worker")
    if isinstance(worker_obj, dict):
        worker_ok = bool(worker_obj.get("ok"))
        worker_exit_code = int(worker_obj.get("exit_code") or 0)
        try:
            worker_runtime_s = float(worker_obj.get("runtime_seconds") or 0.0)
        except Exception:
            worker_runtime_s = 0.0

    parity_ok = False
    compare_obj = result.get("compare")
    if isinstance(compare_obj, dict):
        parity_ok = bool(compare_obj.get("parity_ok"))

    print("labs-019.shadow_verify_dual_run_stage2")
    print(f"scope={scope}")
    print(f"token={token}")
    print(f"ensure_min_rows={ensure_min_rows}")
    print(f"seed_rows_inserted={seed_rows_inserted}")
    print(f"pg_candidates_total={pg_candidates_total}")
    print(f"outbox_enqueued_total={outbox_enqueued_total}")
    print(f"outbox_done={outbox_done} pending={outbox_pending} processing={outbox_processing} failed={outbox_failed}")
    print(f"es_health_ok={es_health_ok}")
    print(f"es_index_ok={es_index_ok} (status={es_index_status})")
    print(f"worker_ok={worker_ok} (rc={worker_exit_code}, runtime_s={worker_runtime_s:.2f})")
    print(f"es_refresh_ok={es_refresh_ok} (status={es_refresh_status})")
    print(f"es_search_ok={es_search_ok} (status={es_search_status})")
    print(f"es_candidates_total={es_candidates_total}")
    print(f"parity_ok={parity_ok} (strategy={strategy})")
    print(f"ok={ok}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def _cmd_labs_shadow_verify_dual_run_window(args: argparse.Namespace) -> int:
    """Sustained dual-run window drill: run worker continuously while enqueueing events.

    Goal: prove that during a sustained window, backlog does not grow unbounded and
    that the outbox projection path stays healthy (no failed events), while ES parity
    remains consistent for a deterministic candidate set.
    """

    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_s2b_auto_run_dir(
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_DUAL_RUN_WINDOW,
        run_id=run_id,
    )
    _ensure_dir(outdir)

    env = _load_env(env_file=args.env_file)
    database_url = (args.database_url or env.get("DATABASE_URL") or "").strip()
    if not database_url:
        print("[labs shadow-verify-dual-run-window] DATABASE_URL is required (via env or --database-url)")
        return 2

    library_id = (args.library_id or "").strip() or None
    if library_id is not None:
        try:
            uuid.UUID(library_id)
        except ValueError:
            print(f"[labs shadow-verify-dual-run-window] invalid --library-id: {library_id}")
            return 2

    ensure_min_rows = int(args.ensure_min_rows)
    candidate_limit = int(args.candidate_limit)
    strategy = str(args.strategy)
    duration_seconds = float(args.duration_seconds)
    interval_seconds = float(args.interval_seconds)
    enqueue_batch_size = int(args.enqueue_batch_size)
    max_total_events = int(args.max_total_events)
    drain_timeout_seconds = float(args.drain_timeout_seconds)

    max_outbox_failed = int(args.max_outbox_failed)
    max_outbox_pending = int(args.max_outbox_pending)
    max_outbox_processing = int(args.max_outbox_processing)
    require_outbox_done_eq_enqueued = bool(args.require_outbox_done_eq_enqueued)

    worker_batch_size = int(args.worker_batch_size)
    worker_concurrency = int(args.worker_concurrency)
    worker_poll_interval_seconds = float(args.worker_poll_interval_seconds)
    worker_max_runtime_seconds = float(args.worker_max_runtime_seconds)

    if ensure_min_rows < 0:
        print("[labs shadow-verify-dual-run-window] --ensure-min-rows must be >= 0")
        return 2
    if candidate_limit <= 0:
        print("[labs shadow-verify-dual-run-window] --candidate-limit must be > 0")
        return 2
    if strategy not in {"soft", "strict"}:
        print("[labs shadow-verify-dual-run-window] --strategy must be one of: soft, strict")
        return 2
    if duration_seconds <= 0:
        print("[labs shadow-verify-dual-run-window] --duration-seconds must be > 0")
        return 2
    if interval_seconds <= 0:
        print("[labs shadow-verify-dual-run-window] --interval-seconds must be > 0")
        return 2
    if enqueue_batch_size <= 0:
        print("[labs shadow-verify-dual-run-window] --enqueue-batch-size must be > 0")
        return 2
    if max_total_events <= 0:
        print("[labs shadow-verify-dual-run-window] --max-total-events must be > 0")
        return 2
    if drain_timeout_seconds <= 0:
        print("[labs shadow-verify-dual-run-window] --drain-timeout-seconds must be > 0")
        return 2
    if max_outbox_failed < 0:
        print("[labs shadow-verify-dual-run-window] --max-outbox-failed must be >= 0")
        return 2
    if max_outbox_pending < 0:
        print("[labs shadow-verify-dual-run-window] --max-outbox-pending must be >= 0")
        return 2
    if max_outbox_processing < 0:
        print("[labs shadow-verify-dual-run-window] --max-outbox-processing must be >= 0")
        return 2
    if worker_batch_size <= 0:
        print("[labs shadow-verify-dual-run-window] --worker-batch-size must be > 0")
        return 2
    if worker_concurrency <= 0:
        print("[labs shadow-verify-dual-run-window] --worker-concurrency must be > 0")
        return 2
    if worker_poll_interval_seconds < 0:
        print("[labs shadow-verify-dual-run-window] --worker-poll-interval-seconds must be >= 0")
        return 2
    if worker_max_runtime_seconds <= 0:
        print("[labs shadow-verify-dual-run-window] --worker-max-runtime-seconds must be > 0")
        return 2

    scope = "all" if library_id is None else f"library:{library_id}"

    es_url = (args.es_url or env.get("ELASTIC_URL") or "http://127.0.0.1:19200").strip().rstrip("/")
    token_default = "dualrun" + re.sub(r"[^0-9A-Za-z]+", "", run_id)
    token = (args.token or token_default).strip() or token_default

    def _sanitize_index_name(name: str) -> str:
        safe = re.sub(r"[^a-z0-9_\-]+", "-", name.lower()).strip("-_")
        safe = re.sub(r"-+", "-", safe)
        if not safe:
            safe = "wordloom-search-index"
        return safe[:80]

    es_index = (
        args.es_index
        or env.get("ELASTIC_INDEX")
        or _sanitize_index_name(f"wordloom-search-index-dualrun-{token}")
    ).strip()
    es_index = _sanitize_index_name(es_index)
    recreate_index = bool(args.recreate_index)

    seed_text_prefix = f"{token} "
    seed_entity_type = "block"

    where_parts: list[str] = ["entity_type = :entity_type", "text ILIKE :pattern"]
    base_params: dict[str, object] = {
        "entity_type": seed_entity_type,
        "pattern": f"{seed_text_prefix}%",
    }
    if library_id is not None:
        where_parts.append("library_id = :library_id")
        base_params["library_id"] = library_id
    where_sql = " AND ".join(where_parts)

    engine = create_engine(database_url)
    inserted_rows = 0
    pg_candidates: list[dict[str, object]] = []

    def _table_columns(conn, table_name: str) -> set[str]:
        rows = conn.execute(
            text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = :t
                """
            ),
            {"t": table_name},
        ).all()
        return {str(r[0]) for r in rows if r and r[0]}

    outbox_cols: set[str] = set()
    with engine.connect() as conn:
        existing_for_token = int(
            conn.execute(text(f"SELECT COUNT(*) FROM search_index WHERE {where_sql}"), base_params).scalar() or 0
        )
        need = int(ensure_min_rows) - int(existing_for_token)
        if need > 0:
            now = datetime.now(timezone.utc)
            max_ev = int(conn.execute(text("SELECT COALESCE(MAX(event_version), 0) FROM search_index")).scalar() or 0)
            rows = []
            for i in range(int(need)):
                rows.append(
                    {
                        "id": uuid.uuid4(),
                        "entity_type": seed_entity_type,
                        "library_id": (uuid.UUID(library_id) if library_id else None),
                        "entity_id": uuid.uuid4(),
                        "text": f"{seed_text_prefix}{i}",
                        "snippet": None,
                        "rank_score": 0.0,
                        "created_at": now,
                        "updated_at": now,
                        "event_version": int(max_ev + i + 1),
                    }
                )

            conn.execute(
                text(
                    """
                    INSERT INTO search_index
                      (id, entity_type, library_id, entity_id, text, snippet, rank_score, created_at, updated_at, event_version)
                    VALUES
                      (:id, :entity_type, :library_id, :entity_id, :text, :snippet, :rank_score, :created_at, :updated_at, :event_version)
                    """
                ),
                rows,
            )
            conn.commit()
            inserted_rows = int(need)

        pg_sql = f"""
            SELECT entity_id::text AS entity_id,
                   COALESCE(event_version, 0) AS event_version,
                   library_id::text AS library_id
            FROM search_index
            WHERE {where_sql}
            ORDER BY COALESCE(event_version, 0) ASC, entity_id::text ASC
            LIMIT :limit
        """
        pg_params = dict(base_params)
        pg_params["limit"] = candidate_limit
        pg_rows = conn.execute(text(pg_sql), pg_params).all()
        pg_candidates = [
            {
                "entity_id": str(r[0]),
                "event_version": int(r[1] or 0),
                "library_id": (str(r[2]) if (len(r) > 2 and r[2] is not None) else None),
            }
            for r in pg_rows
        ]
        if not pg_candidates:
            print("[labs shadow-verify-dual-run-window] no pg candidates; increase --ensure-min-rows")
            return 2

        outbox_cols = _table_columns(conn, "search_outbox_events")
        if not outbox_cols:
            print("[labs shadow-verify-dual-run-window] table search_outbox_events not found")
            return 2
        required_cols = {"id", "entity_type", "entity_id", "op", "event_version", "status"}
        missing_required = sorted([c for c in required_cols if c not in outbox_cols])
        if missing_required:
            print(
                f"[labs shadow-verify-dual-run-window] search_outbox_events missing required columns: {missing_required}"
            )
            return 2

    if enqueue_batch_size > len(pg_candidates):
        print(
            f"[labs shadow-verify-dual-run-window] --enqueue-batch-size ({enqueue_batch_size}) exceeds pg_candidates_total ({len(pg_candidates)})"
        )
        return 2

    # Strong mutual evidence: stdout probe.
    probe: dict[str, object] = {
        "event": "labs.dual_run.window.probe",
        "lab_id": LAB_ID_S2B_2A_2A,
        "scenario": SCENARIO_SHADOW_VERIFY_DUAL_RUN_WINDOW,
        "run_id": run_id,
        "scope": scope,
        "library_id": library_id,
        "token": token,
        "pg_candidates_total": len(pg_candidates),
        "duration_seconds": duration_seconds,
        "interval_seconds": interval_seconds,
        "enqueue_batch_size": enqueue_batch_size,
        "max_total_events": max_total_events,
        "es_url": es_url,
        "es_index": es_index,
    }
    print(json.dumps(probe, ensure_ascii=False, separators=(",", ":")))

    # ES health + ensure index mapping.
    es_health_status, es_health_payload = _http_json("GET", f"{es_url}", body=None, timeout_s=5.0)
    es_health_ok = bool(es_health_status == 200)

    if recreate_index:
        _http_json("DELETE", f"{es_url}/{es_index}", body=None, timeout_s=10.0)

    mapping = {
        "mappings": {
            "properties": {
                "entity_type": {"type": "keyword"},
                "library_id": {"type": "keyword"},
                "entity_id": {"type": "keyword"},
                "text": {"type": "text"},
                "snippet": {"type": "text", "index": False},
                "rank_score": {"type": "float"},
                "event_version": {"type": "long"},
                "updated_at": {"type": "date"},
            }
        }
    }
    es_index_status, es_index_payload = _http_json(
        "PUT",
        f"{es_url}/{es_index}",
        body=mapping,
        timeout_s=10.0,
    )
    es_index_ok = bool(es_index_status in {200, 201} or es_index_status == 400)

    # Worker subprocess (continuous during the window).
    worker_script = REPO_ROOT / "backend" / "scripts" / "ops" / "search_outbox_worker.py"
    worker_env = env.copy()
    worker_env["DATABASE_URL"] = database_url
    worker_env["ELASTIC_URL"] = es_url
    worker_env["ELASTIC_INDEX"] = es_index

    # Scope precedence for worker claim allowlist:
    # 1) explicit SEARCH_OUTBOX_LIBRARY_ALLOWLIST from caller/workflow (if provided)
    # 2) otherwise default to --library-id (if provided)
    explicit_allowlist = str(worker_env.get("SEARCH_OUTBOX_LIBRARY_ALLOWLIST") or "").strip()
    if explicit_allowlist:
        worker_env["SEARCH_OUTBOX_LIBRARY_ALLOWLIST"] = explicit_allowlist
    elif library_id is not None:
        worker_env["SEARCH_OUTBOX_LIBRARY_ALLOWLIST"] = str(library_id)
    else:
        worker_env.pop("SEARCH_OUTBOX_LIBRARY_ALLOWLIST", None)

    backend_path = str(REPO_ROOT / "backend")
    existing_pythonpath = str(worker_env.get("PYTHONPATH") or "").strip()
    if existing_pythonpath:
        if backend_path not in existing_pythonpath.split(os.pathsep):
            worker_env["PYTHONPATH"] = backend_path + os.pathsep + existing_pythonpath
    else:
        worker_env["PYTHONPATH"] = backend_path

    # Do not exit when idle; keep running for the window (bounded by max runtime).
    worker_env["OUTBOX_EXIT_WHEN_IDLE"] = "0"
    worker_env["OUTBOX_MAX_RUNTIME_SECONDS"] = str(float(worker_max_runtime_seconds))
    worker_env["OUTBOX_POLL_INTERVAL_SECONDS"] = str(float(worker_poll_interval_seconds))
    worker_env["OUTBOX_BULK_SIZE"] = str(int(worker_batch_size))
    worker_env["OUTBOX_CONCURRENCY"] = str(int(worker_concurrency))
    worker_env["OUTBOX_REQUIRE_ES_READY"] = "1"
    worker_env["OUTBOX_SHUTDOWN_GRACE_SECONDS"] = "5"

    worker_log_path = outdir / "worker.log"
    worker_started_at = time.time()
    worker_exit_code: int | None = None
    worker_runtime_s: float | None = None
    worker_ok = False
    last_claim_batch_id: str | None = None
    worker_stop_requested = False
    worker_stop_kind: str | None = None

    # Enqueue loop.
    outbox_event_ids: list[str] = []
    enqueued_entity_ids: list[str] = []
    window_samples: list[dict[str, object]] = []

    def _tail_file(path: Path, limit: int = 4000) -> str:
        try:
            t = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return ""
        if len(t) <= limit:
            return t
        return t[-limit:]

    def _try_parse_json(payload: str) -> dict[str, object]:
        try:
            obj = json.loads(payload) if payload else {}
            return obj if isinstance(obj, dict) else {"_": obj}
        except Exception:
            return {"raw": payload}

    def _outbox_status_counts_for_ids(ids: list[str]) -> dict[str, int]:
        if not ids:
            return {}
        outbox_sql = (
            text(
                """
                SELECT status, COUNT(*) AS n
                FROM search_outbox_events
                WHERE id IN :ids
                GROUP BY status
                """
            )
            .bindparams(bindparam("ids", expanding=True))
        )
        counts: dict[str, int] = {}
        with engine.connect() as conn:
            rows = conn.execute(outbox_sql, {"ids": [uuid.UUID(x) for x in ids]}).all()
            for st, n in rows:
                counts[str(st)] = int(n or 0)
        return counts

    now = datetime.now(timezone.utc)
    base_event: dict[str, object] = {
        "entity_type": seed_entity_type,
        "op": "upsert",
        "status": "pending",
        "attempts": 0,
        "replay_count": 0,
        "created_at": now,
        "updated_at": now,
        "traceparent": None,
        "tracestate": None,
    }
    chosen_cols = [
        c
        for c in (
            "id",
            "entity_type",
            "library_id",
            "entity_id",
            "op",
            "event_version",
            "status",
            "attempts",
            "replay_count",
            "created_at",
            "updated_at",
            "traceparent",
            "tracestate",
        )
        if c in outbox_cols
    ]
    cols_sql = ", ".join(chosen_cols)
    placeholders = ", ".join([f":{c}" for c in chosen_cols])
    outbox_insert_sql = text(f"INSERT INTO search_outbox_events ({cols_sql}) VALUES ({placeholders})")

    # NOTE: Keep logs deterministic and always write the combined worker output.
    with worker_log_path.open("w", encoding="utf-8") as wf:
        worker_proc = subprocess.Popen(
            [_python_exe(), str(worker_script)],
            cwd=str(REPO_ROOT),
            env=worker_env,
            stdout=wf,
            stderr=subprocess.STDOUT,
            text=True,
        )

        t_start = time.monotonic()
        t_end = t_start + float(duration_seconds)
        cursor = 0
        while True:
            t_now = time.monotonic()
            if t_now >= t_end:
                break
            if len(outbox_event_ids) >= int(max_total_events):
                break
            if worker_proc.poll() is not None:
                break

            batch: list[dict[str, object]] = []
            for _ in range(enqueue_batch_size):
                if len(outbox_event_ids) >= int(max_total_events):
                    break
                c = pg_candidates[cursor]
                cursor = (cursor + 1) % len(pg_candidates)
                ev_uuid = uuid.uuid4()
                outbox_event_ids.append(str(ev_uuid))
                enqueued_entity_ids.append(str(c["entity_id"]))
                row = {
                    **{k: v for k, v in base_event.items() if k in chosen_cols},
                    "id": ev_uuid,
                    "entity_id": uuid.UUID(str(c["entity_id"])),
                    "event_version": int(c["event_version"] or 0),
                }
                if "library_id" in chosen_cols:
                    lib = c.get("library_id") or library_id
                    row["library_id"] = (uuid.UUID(str(lib)) if lib else None)
                batch.append(row)

            if batch:
                with engine.connect() as conn:
                    conn.execute(outbox_insert_sql, batch)
                    conn.commit()

            counts = _outbox_status_counts_for_ids(outbox_event_ids)
            window_samples.append(
                {
                    "t_seconds": float(time.monotonic() - t_start),
                    "enqueued_total": int(len(outbox_event_ids)),
                    "status_counts": counts,
                }
            )

            # Throttle to interval.
            sleep_s = float(interval_seconds)
            if sleep_s > 0:
                time.sleep(sleep_s)

        enqueue_finished_at = time.time()

        # Drain: wait for pending/processing to reach zero for our inserted ids.
        drain_t0 = time.monotonic()
        final_status_counts: dict[str, int] = {}
        while True:
            if worker_proc.poll() is not None:
                break
            final_status_counts = _outbox_status_counts_for_ids(outbox_event_ids)
            pending = int(final_status_counts.get("pending", 0))
            processing = int(final_status_counts.get("processing", 0))
            if pending == 0 and processing == 0:
                break
            if (time.monotonic() - drain_t0) >= float(drain_timeout_seconds):
                break
            time.sleep(0.25)

        # Stop worker if still running.
        if worker_proc.poll() is None:
            worker_stop_requested = True
            worker_stop_kind = "terminate"
            try:
                worker_proc.terminate()
                worker_proc.wait(timeout=10.0)
            except Exception:
                worker_stop_kind = "kill"
                try:
                    worker_proc.kill()
                    try:
                        worker_proc.wait(timeout=2.0)
                    except Exception:
                        pass
                except Exception:
                    pass

        worker_exit_code = int(worker_proc.returncode) if worker_proc.returncode is not None else None
        worker_runtime_s = float(time.time() - worker_started_at)
        # For window drills we may intentionally stop the worker after draining.
        # Treat this as OK (exit code may be non-zero on Windows terminate).
        worker_ok = bool((worker_exit_code == 0) or worker_stop_requested)

        wf.write("\n--- labs window metadata ---\n")
        wf.write(
            json.dumps(
                {
                    "event": "labs.dual_run.window.meta",
                    "scenario": SCENARIO_SHADOW_VERIFY_DUAL_RUN_WINDOW,
                    "run_id": run_id,
                    "enqueue_finished_at": enqueue_finished_at,
                    "total_events": int(len(outbox_event_ids)),
                },
                ensure_ascii=False,
                separators=(",", ":"),
            )
            + "\n"
        )

    last_claim_batch_id = _extract_last_claim_batch_id(worker_log_path)

    # Post-worker: refresh index for deterministic visibility.
    es_refresh_status, _es_refresh_payload = _http_json(
        "POST",
        f"{es_url}/{es_index}/_refresh",
        body=None,
        timeout_s=10.0,
    )
    es_refresh_ok = bool(es_refresh_status < 400)

    es_query_filters: list[dict[str, object]] = [{"term": {"entity_type": seed_entity_type}}]
    if library_id is not None:
        es_query_filters.append({"term": {"library_id": library_id}})

    es_search_body: dict[str, object] = {
        "query": {
            "bool": {
                "must": [{"match": {"text": token}}],
                "filter": es_query_filters,
            }
        },
        "sort": [{"event_version": "asc"}, {"entity_id": "asc"}],
        "_source": ["entity_id", "event_version", "entity_type", "library_id"],
        "size": candidate_limit,
    }

    es_search_status, es_search_payload = _http_json(
        "POST",
        f"{es_url}/{es_index}/_search",
        body=es_search_body,
        timeout_s=10.0,
    )
    es_search_ok = bool(es_search_status < 400)
    es_search_obj = _try_parse_json(es_search_payload)
    hits = (((es_search_obj.get("hits") or {}) if isinstance(es_search_obj, dict) else {}).get("hits") or [])
    if not isinstance(hits, list):
        hits = []

    es_candidates: list[dict[str, object]] = []
    for h in hits:
        if not isinstance(h, dict):
            continue
        src = h.get("_source")
        if not isinstance(src, dict):
            continue
        entity_id = src.get("entity_id")
        event_version = src.get("event_version")
        if entity_id is None:
            continue
        try:
            ev = int(event_version or 0)
        except Exception:
            ev = 0
        es_candidates.append({"entity_id": str(entity_id), "event_version": ev})

    es_count_status, es_count_payload = _http_json(
        "POST",
        f"{es_url}/{es_index}/_count",
        body={"query": es_search_body.get("query")},
        timeout_s=10.0,
    )
    es_count_obj = _try_parse_json(es_count_payload)
    es_count = None
    if isinstance(es_count_obj, dict) and isinstance(es_count_obj.get("count"), int):
        es_count = int(es_count_obj["count"])

    outbox_status_counts = _outbox_status_counts_for_ids(outbox_event_ids)
    outbox_done = int(outbox_status_counts.get("done", 0))
    outbox_pending = int(outbox_status_counts.get("pending", 0))
    outbox_processing = int(outbox_status_counts.get("processing", 0))
    outbox_failed = int(outbox_status_counts.get("failed", 0))

    expected_id_set = set(enqueued_entity_ids)
    expected_pg_candidates = [c for c in pg_candidates if str(c["entity_id"]) in expected_id_set]
    expected_pg_ids = [str(c["entity_id"]) for c in expected_pg_candidates]
    es_ids = [str(c["entity_id"]) for c in es_candidates]

    if strategy == "strict":
        parity_ok = bool(expected_pg_ids == es_ids[: len(expected_pg_ids)])
    else:
        parity_ok = bool(set(expected_pg_ids) & set(es_ids))

    ok = bool(
        len(outbox_event_ids) > 0
        and es_health_ok
        and es_index_ok
        and worker_ok
        and es_refresh_ok
        and es_search_ok
        and outbox_failed <= max_outbox_failed
        and outbox_pending <= max_outbox_pending
        and outbox_processing <= max_outbox_processing
        and ((not require_outbox_done_eq_enqueued) or (outbox_done == len(outbox_event_ids)))
        and parity_ok
    )

    def _rel_repo(path: Path) -> str:
        try:
            return str(path.resolve().relative_to(REPO_ROOT).as_posix())
        except Exception:
            return str(path.as_posix())

    result: dict[str, object] = {
        "lab_id": LAB_ID_S2B_2A_2A,
        "scenario": SCENARIO_SHADOW_VERIFY_DUAL_RUN_WINDOW,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "inputs": {
            "token": token,
            "ensure_min_rows": ensure_min_rows,
            "seed_entity_type": seed_entity_type,
            "candidate_limit": candidate_limit,
            "strategy": strategy,
            "duration_seconds": duration_seconds,
            "interval_seconds": interval_seconds,
            "enqueue_batch_size": enqueue_batch_size,
            "max_total_events": max_total_events,
            "drain_timeout_seconds": drain_timeout_seconds,
            "max_outbox_failed": max_outbox_failed,
            "max_outbox_pending": max_outbox_pending,
            "max_outbox_processing": max_outbox_processing,
            "require_outbox_done_eq_enqueued": bool(require_outbox_done_eq_enqueued),
            "es_url": es_url,
            "es_index": es_index,
            "recreate_index": recreate_index,
            "worker_batch_size": worker_batch_size,
            "worker_concurrency": worker_concurrency,
            "worker_poll_interval_seconds": worker_poll_interval_seconds,
            "worker_max_runtime_seconds": worker_max_runtime_seconds,
        },
        "seed_rows_inserted": int(inserted_rows),
        "postgres": {
            "candidates": pg_candidates,
        },
        "window": {
            "enqueued_total": int(len(outbox_event_ids)),
            "samples": window_samples,
        },
        "outbox": {
            "enqueued_total": int(len(outbox_event_ids)),
            "event_ids": outbox_event_ids,
            "status_counts": outbox_status_counts,
        },
        "elasticsearch": {
            "health": {"status": int(es_health_status), "ok": bool(es_health_ok), "payload": es_health_payload},
            "index": {"status": int(es_index_status), "ok": bool(es_index_ok), "payload": es_index_payload},
            "refresh": {"status": int(es_refresh_status), "ok": bool(es_refresh_ok)},
            "search": {
                "status": int(es_search_status),
                "ok": bool(es_search_ok),
                "request": es_search_body,
                "response_excerpt": {
                    "hits_total": (
                        (es_search_obj.get("hits") or {}).get("total") if isinstance(es_search_obj, dict) else None
                    ),
                },
                "candidates": es_candidates,
            },
            "count": {"status": int(es_count_status), "count": es_count, "payload": es_count_obj},
        },
        "worker": {
            "script": _rel_repo(worker_script),
            "exit_code": worker_exit_code,
            "ok": bool(worker_ok),
            "runtime_seconds": worker_runtime_s,
            "log_path": _rel_repo(worker_log_path),
            "last_claim_batch_id": last_claim_batch_id,
            "stop_requested": bool(worker_stop_requested),
            "stop_kind": worker_stop_kind,
            "stdout_stderr_tail": _tail_file(worker_log_path),
        },
        "compare": {
            "expected_pg_ids": expected_pg_ids,
            "es_ids": es_ids,
            "parity_ok": bool(parity_ok),
        },
        "ok": bool(ok),
    }

    (outdir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("labs-020.shadow_verify_dual_run_window")
    print(f"scope={scope}")
    print(f"token={token}")
    print(f"ensure_min_rows={ensure_min_rows}")
    print(f"seed_rows_inserted={inserted_rows}")
    print(f"pg_candidates_total={len(pg_candidates)}")
    print(f"outbox_enqueued_total={len(outbox_event_ids)}")
    print(f"outbox_done={outbox_done} pending={outbox_pending} processing={outbox_processing} failed={outbox_failed}")
    print(f"es_health_ok={es_health_ok}")
    print(f"es_index_ok={es_index_ok} (status={es_index_status})")
    print(f"worker_ok={worker_ok} (rc={worker_exit_code}, runtime_s={(worker_runtime_s or 0.0):.2f})")
    print(f"es_refresh_ok={es_refresh_ok} (status={es_refresh_status})")
    print(f"es_search_ok={es_search_ok} (status={es_search_status})")
    print(f"es_candidates_total={len(es_candidates)}")
    print(f"parity_ok={parity_ok} (strategy={strategy})")
    print(f"ok={ok}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def _cmd_labs_shadow_verify_canary_dual_write(args: argparse.Namespace) -> int:
    """Minimal canary dual-write drill for Search.

    Writes a very small, drill-scoped set of rows to:
    - search_index (projection)
    - search_outbox_events (outbox enqueue)

    Then verifies presence and performs cleanup (rollback) by default.
    """

    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_s2b_auto_run_dir(
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_CANARY_DUAL_WRITE,
        run_id=run_id,
    )
    _ensure_dir(outdir)

    env = _load_env(env_file=args.env_file)
    database_url = (args.database_url or env.get("DATABASE_URL") or "").strip()
    if not database_url:
        print("[labs shadow-verify-canary-dual-write] DATABASE_URL is required (via env or --database-url)")
        return 2

    library_id = (args.library_id or "").strip() or None
    if library_id is not None:
        try:
            uuid.UUID(library_id)
        except ValueError:
            print(f"[labs shadow-verify-canary-dual-write] invalid --library-id: {library_id}")
            return 2

    max_writes = int(args.max_writes)
    if max_writes <= 0:
        print("[labs shadow-verify-canary-dual-write] --max-writes must be > 0")
        return 2

    cleanup = bool(args.cleanup)
    scope = "all" if library_id is None else f"library:{library_id}"
    entity_type = "canary"

    now = datetime.now(timezone.utc)
    entity_ids: list[str] = [str(uuid.uuid4()) for _ in range(max_writes)]
    search_index_ids: list[str] = [str(uuid.uuid4()) for _ in range(max_writes)]
    outbox_ids: list[str] = [str(uuid.uuid4()) for _ in range(max_writes)]

    search_rows = []
    outbox_rows = []
    for i in range(max_writes):
        search_rows.append(
            {
                "id": search_index_ids[i],
                "entity_type": entity_type,
                "library_id": library_id,
                "entity_id": entity_ids[i],
                "text": f"canary:{run_id}:{i}",
                "snippet": None,
                "rank_score": 0.0,
                "created_at": now,
                "updated_at": now,
                "event_version": int(i + 1),
            }
        )
        outbox_rows.append(
            {
                "id": outbox_ids[i],
                "entity_type": entity_type,
                "library_id": library_id,
                "entity_id": entity_ids[i],
                "op": "upsert",
                "event_version": int(i + 1),
                "created_at": now,
                "status": "pending",
                "attempts": 0,
                "updated_at": now,
                "replay_count": 0,
            }
        )

    engine = create_engine(database_url)
    inserted_search = 0
    inserted_outbox = 0
    verify_search_count = 0
    verify_outbox_count = 0
    cleanup_deleted_search = 0
    cleanup_deleted_outbox = 0
    cleanup_remaining_search = None
    cleanup_remaining_outbox = None

    with engine.connect() as conn:
        # 1) insert projection rows
        conn.execute(
            text(
                """
                INSERT INTO search_index
                  (id, entity_type, library_id, entity_id, text, snippet, rank_score, created_at, updated_at, event_version)
                VALUES
                  (:id, :entity_type, :library_id, :entity_id, :text, :snippet, :rank_score, :created_at, :updated_at, :event_version)
                """
            ),
            search_rows,
        )
        inserted_search = max_writes

        # 2) enqueue outbox rows
        conn.execute(
            text(
                """
                INSERT INTO search_outbox_events
                                    (id, entity_type, library_id, entity_id, op, event_version, created_at, status, attempts, updated_at, replay_count)
                VALUES
                                    (:id, :entity_type, :library_id, :entity_id, :op, :event_version, :created_at, :status, :attempts, :updated_at, :replay_count)
                """
            ),
            outbox_rows,
        )
        inserted_outbox = max_writes

        conn.commit()

        # 3) verify presence
        verify_search_count = int(
            conn.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM search_index
                    WHERE entity_type = :entity_type
                      AND entity_id IN :entity_ids
                    """
                ).bindparams(bindparam("entity_ids", expanding=True)),
                {"entity_type": entity_type, "entity_ids": entity_ids},
            ).scalar()
            or 0
        )
        verify_outbox_count = int(
            conn.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM search_outbox_events
                    WHERE entity_type = :entity_type
                      AND entity_id IN :entity_ids
                    """
                ).bindparams(bindparam("entity_ids", expanding=True)),
                {"entity_type": entity_type, "entity_ids": entity_ids},
            ).scalar()
            or 0
        )

        # 4) verify write-gate uniqueness still holds
        dup_extra = int(
            conn.execute(
                text(
                    """
                    SELECT COALESCE(SUM(cnt - 1), 0)
                    FROM (
                      SELECT COUNT(*) AS cnt
                      FROM search_index
                      GROUP BY entity_type, entity_id
                      HAVING COUNT(*) > 1
                    ) t
                    """
                )
            ).scalar()
            or 0
        )

        # 5) cleanup (rollback evidence)
        if cleanup:
            conn.execute(
                text(
                    """
                    DELETE FROM search_outbox_events
                    WHERE entity_type = :entity_type
                      AND entity_id IN :entity_ids
                    """
                ).bindparams(bindparam("entity_ids", expanding=True)),
                {"entity_type": entity_type, "entity_ids": entity_ids},
            )
            conn.execute(
                text(
                    """
                    DELETE FROM search_index
                    WHERE entity_type = :entity_type
                      AND entity_id IN :entity_ids
                    """
                ).bindparams(bindparam("entity_ids", expanding=True)),
                {"entity_type": entity_type, "entity_ids": entity_ids},
            )
            conn.commit()

            cleanup_remaining_search = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_index
                        WHERE entity_type = :entity_type
                          AND entity_id IN :entity_ids
                        """
                    ).bindparams(bindparam("entity_ids", expanding=True)),
                    {"entity_type": entity_type, "entity_ids": entity_ids},
                ).scalar()
                or 0
            )
            cleanup_remaining_outbox = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_outbox_events
                        WHERE entity_type = :entity_type
                          AND entity_id IN :entity_ids
                        """
                    ).bindparams(bindparam("entity_ids", expanding=True)),
                    {"entity_type": entity_type, "entity_ids": entity_ids},
                ).scalar()
                or 0
            )

            cleanup_deleted_search = verify_search_count - cleanup_remaining_search
            cleanup_deleted_outbox = verify_outbox_count - cleanup_remaining_outbox

    ok = (
        inserted_search == max_writes
        and inserted_outbox == max_writes
        and verify_search_count == max_writes
        and verify_outbox_count == max_writes
        and dup_extra == 0
        and ((not cleanup) or (cleanup_remaining_search == 0 and cleanup_remaining_outbox == 0))
    )

    result: dict[str, object] = {
        "lab_id": LAB_ID_S2B_2A_2A,
        "scenario": SCENARIO_SHADOW_VERIFY_CANARY_DUAL_WRITE,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "dry_run": False,
        "targets": {
            "projection_table": "search_index",
            "outbox_table": "search_outbox_events",
            "entrypoint_hint": "backend/infra/search/search_indexer.py::PostgresSearchIndexer (writes search_index + enqueues search_outbox_events)",
        },
        "canary": {
            "entity_type": entity_type,
            "max_writes": max_writes,
            "entity_ids": entity_ids,
            "search_index_ids": search_index_ids,
            "outbox_event_ids": outbox_ids,
        },
        "verify": {
            "search_index_rows_found": int(verify_search_count),
            "search_outbox_rows_found": int(verify_outbox_count),
            "duplicates_extra_rows_total": int(dup_extra),
        },
        "rollback": {
            "cleanup_enabled": bool(cleanup),
            "deleted_search_index": int(cleanup_deleted_search),
            "deleted_search_outbox_events": int(cleanup_deleted_outbox),
            "remaining_search_index": cleanup_remaining_search,
            "remaining_search_outbox_events": cleanup_remaining_outbox,
            "note": "Cleanup is executed by default to keep CI/devtest DB clean.",
        },
        "ok": bool(ok),
    }

    (outdir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("labs-016.shadow_verify_canary_dual_write")
    print(f"scope={scope}")
    print(f"max_writes={max_writes}")
    print(f"verify_search_index_rows_found={verify_search_count}")
    print(f"verify_search_outbox_rows_found={verify_outbox_count}")
    print(f"duplicates_extra_rows_total={dup_extra}")
    print(f"cleanup_enabled={cleanup}")
    print(f"cleanup_deleted_search_index={cleanup_deleted_search}")
    print(f"cleanup_deleted_search_outbox_events={cleanup_deleted_outbox}")
    if cleanup:
        print(f"cleanup_remaining_search_index={cleanup_remaining_search}")
        print(f"cleanup_remaining_search_outbox_events={cleanup_remaining_outbox}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def _parse_csv_list(value: str | None) -> list[str]:
    if not value:
        return []
    parts = [p.strip() for p in str(value).split(",")]
    return [p for p in parts if p]


def _cmd_labs_shadow_verify_dual_write_sampling(args: argparse.Namespace) -> int:
    """Sustained dual-write (outbox enqueue) with allowlist/sampling controls.

    This drill enqueues outbox events (shadow) for a sampled subset of existing
    `search_index` rows, optionally scoped by library_id and entity_types.

    It records policy evidence for new-side failures:
    - soft vs strict strategy
    - DLQ simulation (mark some inserted rows as failed)
    - replay evidence (failed -> pending with audit fields)

    By default it cleans up inserted outbox rows to keep CI/devtest clean.
    """

    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_s2b_auto_run_dir(
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_DUAL_WRITE_SAMPLING,
        run_id=run_id,
    )
    _ensure_dir(outdir)

    env = _load_env(env_file=args.env_file)
    database_url = (args.database_url or env.get("DATABASE_URL") or "").strip()
    if not database_url:
        print("[labs shadow-verify-dual-write-sampling] DATABASE_URL is required (via env or --database-url)")
        return 2

    library_id = (args.library_id or "").strip() or None
    if library_id is not None:
        try:
            uuid.UUID(library_id)
        except ValueError:
            print(f"[labs shadow-verify-dual-write-sampling] invalid --library-id: {library_id}")
            return 2

    entity_types = _parse_csv_list(args.entity_types)
    ensure_min_rows = int(args.ensure_min_rows)
    if ensure_min_rows < 0:
        print("[labs shadow-verify-dual-write-sampling] --ensure-min-rows must be >= 0")
        return 2

    sample_size = int(args.sample_size)
    if sample_size <= 0:
        print("[labs shadow-verify-dual-write-sampling] --sample-size must be > 0")
        return 2

    duration_seconds = int(args.duration_seconds)
    if duration_seconds < 0:
        print("[labs shadow-verify-dual-write-sampling] --duration-seconds must be >= 0")
        return 2

    interval_seconds = float(args.interval_seconds)
    if interval_seconds <= 0:
        print("[labs shadow-verify-dual-write-sampling] --interval-seconds must be > 0")
        return 2

    max_total_events = int(args.max_total_events)
    if max_total_events <= 0:
        print("[labs shadow-verify-dual-write-sampling] --max-total-events must be > 0")
        return 2

    strategy = str(args.strategy).strip().lower()
    if strategy not in {"soft", "strict"}:
        print("[labs shadow-verify-dual-write-sampling] --strategy must be one of: soft, strict")
        return 2

    inject_failed_rate = float(args.inject_failed_rate)
    if inject_failed_rate < 0.0 or inject_failed_rate > 1.0:
        print("[labs shadow-verify-dual-write-sampling] --inject-failed-rate must be in [0.0, 1.0]")
        return 2

    replay_failed = bool(args.replay_failed)
    replay_by = str(args.replay_by or "labs")[:120]
    replay_reason = str(args.replay_reason or "labs shadow dual-write sampling replay")
    cleanup = bool(args.cleanup)

    scope = "all" if library_id is None else f"library:{library_id}"
    engine = create_engine(database_url)

    now = datetime.now(timezone.utc)
    stop_at = now.timestamp() + float(duration_seconds)

    inserted_outbox_ids: list[str] = []
    inserted_total = 0
    dlq_failed_total = 0
    replayed_total = 0
    seed_rows_inserted = 0
    loops = 0

    def _select_candidates(conn, limit: int) -> list[tuple[str, str, int, str | None]]:
        where_parts: list[str] = []
        params: dict[str, object] = {"limit": int(limit)}

        if library_id is not None:
            where_parts.append("library_id = :library_id")
            params["library_id"] = library_id

        if entity_types:
            where_parts.append("entity_type IN :entity_types")
            params["entity_types"] = entity_types

        where_sql = ("WHERE " + " AND ".join(where_parts)) if where_parts else ""
        stmt = text(
            f"""
            SELECT entity_type, entity_id::text, event_version, library_id::text AS library_id
            FROM search_index
            {where_sql}
            ORDER BY updated_at DESC, entity_type, entity_id
            LIMIT :limit
            """
        )
        if entity_types:
            stmt = stmt.bindparams(bindparam("entity_types", expanding=True))

        rows = conn.execute(stmt, params).fetchall()
        return [(str(r[0]), str(r[1]), int(r[2] or 0), (str(r[3]) if (len(r) > 3 and r[3] is not None) else None)) for r in rows]

    with engine.connect() as conn:
        if ensure_min_rows > 0:
            seed_rows_inserted = _ensure_search_index_min_rows(
                conn=conn,
                ensure_min_rows=ensure_min_rows,
                library_id=library_id,
                seed_entity_type="seed_sampling",
            )

        while True:
            loops += 1
            remaining_budget = max_total_events - inserted_total
            if remaining_budget <= 0:
                break

            batch_limit = min(int(sample_size), int(remaining_budget))
            candidates = _select_candidates(conn, limit=batch_limit)
            if not candidates:
                break

            batch_now = datetime.now(timezone.utc)
            outbox_rows = []
            batch_ids = []
            for (entity_type, entity_id, event_version, candidate_library_id) in candidates:
                outbox_id = str(uuid.uuid4())
                batch_ids.append(outbox_id)
                outbox_rows.append(
                    {
                        "id": outbox_id,
                        "entity_type": entity_type,
                        "library_id": candidate_library_id,
                        "entity_id": entity_id,
                        "op": "upsert",
                        "event_version": int(event_version),
                        "created_at": batch_now,
                        "status": "pending",
                        "attempts": 0,
                        "updated_at": batch_now,
                        "replay_count": 0,
                    }
                )

            conn.execute(
                text(
                    """
                    INSERT INTO search_outbox_events
                                            (id, entity_type, library_id, entity_id, op, event_version, created_at, status, attempts, updated_at, replay_count)
                    VALUES
                                            (:id, :entity_type, :library_id, :entity_id, :op, :event_version, :created_at, :status, :attempts, :updated_at, :replay_count)
                    """
                ),
                outbox_rows,
            )
            conn.commit()

            inserted_outbox_ids.extend(batch_ids)
            inserted_total += len(batch_ids)

            # DLQ simulation: mark a subset as failed.
            fail_n = int(round(float(inject_failed_rate) * float(len(batch_ids))))
            fail_ids = batch_ids[: max(0, min(fail_n, len(batch_ids)))]
            if fail_ids:
                conn.execute(
                    text(
                        """
                        UPDATE search_outbox_events
                        SET status='failed',
                            error_reason='simulated_new_side_failure',
                            error='simulated by labs shadow-verify-dual-write-sampling',
                            updated_at=:now
                        WHERE id IN :ids
                        """
                    ).bindparams(bindparam("ids", expanding=True)),
                    {"now": datetime.now(timezone.utc), "ids": fail_ids},
                )
                conn.commit()
                dlq_failed_total += len(fail_ids)

            # Replay evidence (failed -> pending with audit fields).
            if replay_failed and fail_ids:
                replay_now = datetime.now(timezone.utc)
                conn.execute(
                    text(
                        """
                        UPDATE search_outbox_events
                        SET status='pending',
                            owner=NULL,
                            lease_until=NULL,
                            processing_started_at=NULL,
                            attempts=0,
                            next_retry_at=NULL,
                            error_reason=NULL,
                            error=NULL,
                            replay_count=(replay_count + 1),
                            last_replayed_at=:now,
                            last_replayed_by=:by,
                            last_replayed_reason=:reason,
                            updated_at=:now
                        WHERE id IN :ids
                          AND status='failed'
                        """
                    ).bindparams(bindparam("ids", expanding=True)),
                    {"now": replay_now, "by": replay_by, "reason": replay_reason, "ids": fail_ids},
                )
                conn.commit()
                replayed_total += len(fail_ids)

            if duration_seconds <= 0:
                break

            if datetime.now(timezone.utc).timestamp() >= stop_at:
                break

            time.sleep(interval_seconds)

        # Verify status distribution for inserted rows.
        pending_count = 0
        failed_count = 0
        if inserted_outbox_ids:
            rows = conn.execute(
                text(
                    """
                    SELECT status, COUNT(*)
                    FROM search_outbox_events
                    WHERE id IN :ids
                    GROUP BY status
                    """
                ).bindparams(bindparam("ids", expanding=True)),
                {"ids": inserted_outbox_ids},
            ).fetchall()
            for status, cnt in rows:
                if str(status) == "pending":
                    pending_count = int(cnt)
                elif str(status) == "failed":
                    failed_count = int(cnt)

        remaining_outbox = None
        if cleanup and inserted_outbox_ids:
            conn.execute(
                text("DELETE FROM search_outbox_events WHERE id IN :ids").bindparams(bindparam("ids", expanding=True)),
                {"ids": inserted_outbox_ids},
            )
            conn.commit()
            remaining_outbox = int(
                conn.execute(
                    text("SELECT COUNT(*) FROM search_outbox_events WHERE id IN :ids").bindparams(
                        bindparam("ids", expanding=True)
                    ),
                    {"ids": inserted_outbox_ids},
                ).scalar()
                or 0
            )

    strict_failed = failed_count > 0
    ok = True
    if strategy == "strict" and strict_failed:
        ok = False
    if cleanup and inserted_outbox_ids and remaining_outbox not in (0, None):
        ok = False

    result: dict[str, object] = {
        "lab_id": LAB_ID_S2B_2A_2A,
        "scenario": SCENARIO_SHADOW_VERIFY_DUAL_WRITE_SAMPLING,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "dry_run": False,
        "artifacts_contract_hint": "success uploads summary.json only; failure uploads artifacts.zip; _result.json is single source of truth",
        "targets": {
            "projection_table": "search_index",
            "outbox_table": "search_outbox_events",
            "enqueue_entrypoint": "backend/infra/search/search_outbox_repository.py::SearchOutboxRepository.enqueue",
            "producer_entrypoint": "backend/infra/search/search_indexer.py::PostgresSearchIndexer",
            "replay_tool_hint": "backend/scripts/ops/search_outbox_replay_failed.py (stable shim)",
        },
        "config": {
            "library_id": library_id,
            "entity_types": entity_types,
            "ensure_min_rows": int(ensure_min_rows),
            "sample_size": int(sample_size),
            "duration_seconds": int(duration_seconds),
            "interval_seconds": float(interval_seconds),
            "max_total_events": int(max_total_events),
            "strategy": strategy,
            "inject_failed_rate": float(inject_failed_rate),
            "replay_failed": bool(replay_failed),
            "cleanup": bool(cleanup),
        },
        "observed": {
            "loops": int(loops),
            "seed_rows_inserted": int(seed_rows_inserted),
            "outbox_inserted_total": int(inserted_total),
            "dlq_failed_simulated_total": int(dlq_failed_total),
            "replayed_total": int(replayed_total),
            "pending_after": int(pending_count),
            "failed_after": int(failed_count),
        },
        "rollback": {
            "cleanup_enabled": bool(cleanup),
            "remaining_outbox_rows": remaining_outbox,
        },
        "policy": {
            "strategy": strategy,
            "strict_fails_on_failed": True,
            "soft_allows_failed": True,
            "dlq_definition": "status=failed rows are treated as terminal by worker; ops can replay to pending with audit fields",
            "replay_audit_fields": [
                "replay_count",
                "last_replayed_at",
                "last_replayed_by",
                "last_replayed_reason",
            ],
        },
        "ok": bool(ok),
    }

    (outdir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("labs-017.shadow_verify_dual_write_sampling")
    print(f"scope={scope}")
    print(f"strategy={strategy}")
    print(f"outbox_inserted_total={inserted_total}")
    print(f"pending_after={pending_count}")
    print(f"failed_after={failed_count}")
    print(f"dlq_failed_simulated_total={dlq_failed_total}")
    print(f"replayed_total={replayed_total}")
    print(f"cleanup_enabled={cleanup}")
    if cleanup:
        print(f"remaining_outbox_rows={remaining_outbox}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def _cmd_labs_export_jaeger(args: argparse.Namespace) -> int:
    outdir = Path(args.outdir) if args.outdir else _default_labs009_expb_outdir(_now_run_id())
    exports_dir = outdir / "_exports"
    _ensure_dir(exports_dir)

    script = LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"
    cmd = [
        _python_exe(),
        str(script),
        "--outdir",
        str(exports_dir),
        "--service",
        args.service,
        "--lookback",
        args.lookback,
        "--limit",
        str(args.limit),
    ]

    if args.operation:
        cmd += ["--operation", args.operation]

    if args.outbox_event_id:
        cmd += ["--outbox-event-id", args.outbox_event_id]

    if args.claim_batch_id:
        cmd += ["--claim-batch-id", args.claim_batch_id]

    return _run(cmd, cwd=REPO_ROOT)


def _cmd_labs_expb_es429(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_labs009_expb_outdir(run_id)

    exports_dir = outdir / "_exports"
    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    _ensure_dir(exports_dir)
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)

    # Prepare env (inherit, then override)
    env = _with_backend_pythonpath(os.environ.copy())

    # Tracing (opt-in). Default to grpc/4317 for stability.
    env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    env.setdefault("OTEL_SERVICE_NAME", args.service)
    env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    # ES 429 injection knobs (deterministic-ish)
    if args.every_n is not None:
        env["OUTBOX_EXPERIMENT_ES_429_EVERY_N"] = str(args.every_n)
    if args.ratio is not None:
        env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = str(args.ratio)
    if args.seed is not None:
        env["OUTBOX_EXPERIMENT_ES_429_SEED"] = str(args.seed)
    if args.ops:
        env["OUTBOX_EXPERIMENT_ES_429_OPS"] = args.ops

    # Optional: metrics port override (so users can scrape later)
    if args.metrics_port is not None:
        env["OUTBOX_METRICS_PORT"] = str(args.metrics_port)

    notes = outdir / "_notes.md"
    if not notes.exists():
        notes.write_text(
            "# Labs-009 ExpB (ES 429) run\n\n"
            f"run_id: {run_id}\n\n"
            "## Commands\n\n"
            "- This run was started via `backend/scripts/cli.py labs expb-es429`.\n"
            "\n## Checklist\n\n"
            "- [ ] metrics shows retry_scheduled_total{reason=\"es_429\"}\n"
            "- [ ] jaeger export contains outbox.process / projection spans\n"
            "- [ ] logs contain trace_id/span_id for representative event\n",
            encoding="utf-8",
        )

    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    log_path = logs_dir / f"worker-{run_id}.log"

    # Run worker for a bounded duration using Python wrapper (no extra dependencies).
    # We run it in a subprocess and let the user stop it with Ctrl+C too.
    cmd = [_python_exe(), "-u", str(worker)]

    print(f"[scripts] output dir: {outdir}")
    print(f"[scripts] worker log: {log_path}")
    print(f"[scripts] duration: {args.duration}s")

    start = time.time()
    with open(log_path, "w", encoding="utf-8") as log_file:
        proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)
        try:
            while True:
                if args.duration > 0 and (time.time() - start) >= args.duration:
                    proc.terminate()
                    break
                ret = proc.poll()
                if ret is not None:
                    break
                time.sleep(0.25)
        except KeyboardInterrupt:
            proc.terminate()

        proc.wait(timeout=30)

    # Always export a small Jaeger snapshot at the end.
    jaeger_script = LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"
    export_cmd = [
        _python_exe(),
        str(jaeger_script),
        "--outdir",
        str(exports_dir),
        "--service",
        args.service,
        "--lookback",
        args.lookback,
        "--limit",
        str(args.limit),
    ]
    _run(export_cmd, cwd=REPO_ROOT)

    print("[scripts] done")
    print(f"[scripts] outputs: {outdir}")
    return 0


def _cmd_labs_run_es_write_block_4xx(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_labs_auto_run_dir(scenario=SCENARIO_ES_WRITE_BLOCK_4XX, run_id=run_id)

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    exports_dir = outdir / "_exports"
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)
    _ensure_dir(exports_dir)

    env = _with_backend_pythonpath(_load_env(env_file=args.env_file))

    es_url = (env.get("ELASTIC_URL") or "http://localhost:19200").strip().rstrip("/")
    es_index = (env.get("ELASTIC_INDEX") or "wordloom-search-index").strip()

    # Tracing: stable defaults
    service_name = args.service
    env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    env.setdefault("OTEL_SERVICE_NAME", service_name)
    env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    # Ensure batch logs include claim_batch_id for export correlation.
    env["LOG_LEVEL"] = "INFO"

    # Ensure deterministic, irrecoverable failure (no 429 injection).
    env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = "0"

    # Metrics port
    env["OUTBOX_METRICS_PORT"] = str(int(args.metrics_port))

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_ES_WRITE_BLOCK_4XX,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": args.env_file,
        "service": service_name,
        "es": {"url": es_url, "index": es_index, "inject": {"index.blocks.write": True}},
        "worker": {"duration_s": int(args.duration), "metrics_port": int(args.metrics_port)},
    }
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # 1) Run worker first, scrape baseline metrics, then inject + trigger.
    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    log_path = logs_dir / f"worker-{run_id}.log"
    cmd = [_python_exe(), "-u", str(worker)]

    print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] worker log: {log_path}")

    metrics_before_path = metrics_dir / "metrics-before.txt"
    metrics_after_path = metrics_dir / "metrics-after.txt"

    start = time.time()
    stopped_by_controller = False
    with open(log_path, "w", encoding="utf-8") as log_file:
        worker_proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)
        try:
            # Best-effort metrics scrape before/after.
            time.sleep(max(0.5, float(args.scrape_delay)))
            try:
                metrics_before = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                metrics_before_path.write_text(metrics_before, encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                metrics_before_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

            # 2) Inject: block writes at the index.
            status, payload = _es_set_index_write_block(es_url=es_url, index=es_index, enabled=True)
            if status == 404:
                c_status, c_payload = _es_create_index_if_missing(es_url=es_url, index=es_index)
                (outdir / "_inject_es_create_index.response.txt").write_text(
                    f"status={c_status}\n\n{c_payload}\n", encoding="utf-8"
                )
                if c_status not in (200, 201, 400):
                    print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] failed to create index: http {c_status}")
                    worker_proc.terminate()
                    worker_proc.wait(timeout=30)
                    return 2

                status, payload = _es_set_index_write_block(es_url=es_url, index=es_index, enabled=True)
            (outdir / "_inject_es_write_block.response.txt").write_text(
                f"status={status}\n\n{payload}\n", encoding="utf-8"
            )
            if status < 200 or status >= 300:
                print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] failed to enable write block: http {status}")
                worker_proc.terminate()
                worker_proc.wait(timeout=30)
                return 2

            # 3) Trigger: insert a pending outbox event (and ensure a matching search_index row exists).
            inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
            if not inserter.exists():
                inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"
            trigger_env = env.copy()
            trigger_env.setdefault("OUTBOX_OP", "upsert")
            trigger_env.setdefault("OUTBOX_CREATE_SEARCH_INDEX_ROW", "1")

            proc = subprocess.run(
                [_python_exe(), str(inserter)],
                cwd=str(REPO_ROOT),
                env=trigger_env,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            (outdir / "_trigger_insert_outbox.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
            (outdir / "_trigger_insert_outbox.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
            if proc.returncode != 0:
                print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] failed to insert outbox event: rc={proc.returncode}")
                worker_proc.terminate()
                worker_proc.wait(timeout=30)
                return 3

            outbox_event_id = (proc.stdout or "").strip().splitlines()[-1].strip()
            (outdir / "_outbox_event_id.txt").write_text(outbox_event_id + "\n", encoding="utf-8")
            print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] outbox_event_id: {outbox_event_id}")

            while True:
                if args.duration > 0 and (time.time() - start) >= args.duration:
                    # scrape right before stop (server is still up)
                    try:
                        metrics_after = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    stopped_by_controller = True
                    worker_proc.terminate()
                    break

                ret = worker_proc.poll()
                if ret is not None:
                    # Worker exited early; capture whatever metrics we can.
                    try:
                        metrics_after = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    break
                time.sleep(0.25)
        except KeyboardInterrupt:
            stopped_by_controller = True
            worker_proc.terminate()

        worker_proc.wait(timeout=30)

    exit_info = {"returncode": int(worker_proc.returncode) if worker_proc.returncode is not None else None}
    (outdir / "_worker_exit.json").write_text(
        json.dumps(exit_info, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    if not metrics_after_path.exists():
        metrics_after_path.write_text("scrape_failed: missing_metrics_after\n", encoding="utf-8")

    if (not stopped_by_controller) and (worker_proc.returncode not in (None, 0)):
        print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] worker exited early: rc={worker_proc.returncode}")
        print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] see logs: {log_path}")
        return 4

    print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] outputs: {outdir}")
    return 0


def _resolve_run_dir(*, run_id: str | None, outdir: str | None, scenario: str) -> Path:
    if outdir:
        return Path(outdir)
    if run_id:
        return _default_labs_auto_run_dir(scenario=scenario, run_id=run_id)
    latest = _latest_child_dir(LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / scenario)
    if latest is None:
        raise SystemExit(f"No runs found for scenario={scenario}")
    return latest


def _cmd_labs_verify_es_write_block_4xx(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_ES_WRITE_BLOCK_4XX)
    metrics_dir = run_dir / "_metrics"
    before_path = metrics_dir / "metrics-before.txt"
    after_path = metrics_dir / "metrics-after.txt"

    before = before_path.read_text(encoding="utf-8") if before_path.exists() else ""
    after = after_path.read_text(encoding="utf-8") if after_path.exists() else ""

    failed_before = _prom_parse_counter_sum(before, "outbox_failed_total", labels={"reason": "es_4xx"})
    failed_after = _prom_parse_counter_sum(after, "outbox_failed_total", labels={"reason": "es_4xx"})
    retry_before = _prom_parse_counter_sum(before, "outbox_retry_scheduled_total", labels={"reason": "es_4xx"})
    retry_after = _prom_parse_counter_sum(after, "outbox_retry_scheduled_total", labels={"reason": "es_4xx"})

    delta_failed = failed_after - failed_before
    delta_retry = retry_after - retry_before

    ok = (delta_failed >= float(args.min_failed_delta)) and (delta_retry <= float(args.max_retry_delta))
    result = {
        "scenario": SCENARIO_ES_WRITE_BLOCK_4XX,
        "run_dir": str(run_dir),
        "checks": {
            "failed_delta_ge": float(args.min_failed_delta),
            "retry_delta_le": float(args.max_retry_delta),
        },
        "observed": {
            "outbox_failed_total_reason_es_4xx": {"before": failed_before, "after": failed_after, "delta": delta_failed},
            "outbox_retry_scheduled_total_reason_es_4xx": {"before": retry_before, "after": retry_after, "delta": delta_retry},
        },
        "ok": bool(ok),
    }
    (run_dir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if ok:
        print(f"[labs verify {SCENARIO_ES_WRITE_BLOCK_4XX}] OK")
        return 0
    print(f"[labs verify {SCENARIO_ES_WRITE_BLOCK_4XX}] FAILED")
    return 10


def _cmd_labs_export_es_write_block_4xx(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_ES_WRITE_BLOCK_4XX)
    exports_dir = run_dir / "_exports"
    _ensure_dir(exports_dir)

    outbox_event_id_path = run_dir / "_outbox_event_id.txt"
    outbox_event_id = outbox_event_id_path.read_text(encoding="utf-8").strip() if outbox_event_id_path.exists() else None

    cmd = [
        _python_exe(),
        str(LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"),
        "--outdir",
        str(exports_dir),
        "--service",
        args.service,
        "--lookback",
        args.lookback,
        "--limit",
        str(args.limit),
    ]
    if outbox_event_id:
        cmd += ["--outbox-event-id", outbox_event_id]

    return _run(cmd, cwd=REPO_ROOT)


def _cmd_labs_run_es_429_inject(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_labs_auto_run_dir(scenario=SCENARIO_ES_429_INJECT, run_id=run_id)

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    exports_dir = outdir / "_exports"
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)
    _ensure_dir(exports_dir)

    env = _with_backend_pythonpath(_load_env(env_file=args.env_file))

    # Tracing: stable defaults
    service_name = args.service
    env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    env.setdefault("OTEL_SERVICE_NAME", service_name)
    env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    # Fault injection: enable ES 429 injection in worker
    if args.every_n is not None and int(args.every_n) > 0:
        env["OUTBOX_EXPERIMENT_ES_429_EVERY_N"] = str(int(args.every_n))
        env.pop("OUTBOX_EXPERIMENT_ES_429_RATIO", None)
    else:
        env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = str(float(args.ratio))
        env.pop("OUTBOX_EXPERIMENT_ES_429_EVERY_N", None)

    env["OUTBOX_EXPERIMENT_ES_429_OPS"] = str(args.ops)
    if args.seed is not None:
        env["OUTBOX_EXPERIMENT_ES_429_SEED"] = str(int(args.seed))
    else:
        env.pop("OUTBOX_EXPERIMENT_ES_429_SEED", None)

    # Metrics port
    env["OUTBOX_METRICS_PORT"] = str(int(args.metrics_port))

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_ES_429_INJECT,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": args.env_file,
        "service": service_name,
        "inject": {
            "kind": "es_429",
            "mode": "every_n" if (args.every_n is not None and int(args.every_n) > 0) else "ratio",
            "every_n": int(args.every_n) if (args.every_n is not None) else None,
            "ratio": float(args.ratio),
            "ops": str(args.ops),
            "seed": int(args.seed) if args.seed is not None else None,
        },
        "worker": {"duration_s": int(args.duration), "metrics_port": int(args.metrics_port)},
        "trigger": {"op": str(args.op)},
    }
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    log_path = logs_dir / f"worker-{run_id}.log"
    cmd = [_python_exe(), "-u", str(worker)]

    print(f"[labs run {SCENARIO_ES_429_INJECT}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_ES_429_INJECT}] worker log: {log_path}")

    metrics_before_path = metrics_dir / "metrics-before.txt"
    metrics_after_path = metrics_dir / "metrics-after.txt"

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"

    start = time.time()
    stopped_by_controller = False
    with open(log_path, "w", encoding="utf-8") as log_file:
        worker_proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)
        try:
            time.sleep(max(0.5, float(args.scrape_delay)))
            try:
                metrics_before = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                metrics_before_path.write_text(metrics_before, encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                metrics_before_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

            # Trigger a single outbox event (and ensure a matching search_index row exists).
            trigger_env = env.copy()
            trigger_env["OUTBOX_OP"] = str(args.op)
            trigger_env.setdefault("OUTBOX_CREATE_SEARCH_INDEX_ROW", "1")
            # Ensure our event is claimed quickly even if there is backlog.
            trigger_env.setdefault("OUTBOX_EVENT_VERSION", "0")

            proc = subprocess.run(
                [_python_exe(), str(inserter)],
                cwd=str(REPO_ROOT),
                env=trigger_env,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            (outdir / "_trigger_insert_outbox.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
            (outdir / "_trigger_insert_outbox.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
            if proc.returncode != 0:
                print(f"[labs run {SCENARIO_ES_429_INJECT}] failed to insert outbox event: rc={proc.returncode}")
                worker_proc.terminate()
                worker_proc.wait(timeout=30)
                return 3

            outbox_event_id = (proc.stdout or "").strip().splitlines()[-1].strip()
            (outdir / "_outbox_event_id.txt").write_text(outbox_event_id + "\n", encoding="utf-8")
            print(f"[labs run {SCENARIO_ES_429_INJECT}] outbox_event_id: {outbox_event_id}")

            while True:
                if args.duration > 0 and (time.time() - start) >= args.duration:
                    try:
                        metrics_after = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    stopped_by_controller = True
                    worker_proc.terminate()
                    break

                ret = worker_proc.poll()
                if ret is not None:
                    try:
                        metrics_after = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    break
                time.sleep(0.25)
        except KeyboardInterrupt:
            stopped_by_controller = True
            worker_proc.terminate()

        worker_proc.wait(timeout=30)

    exit_info = {"returncode": int(worker_proc.returncode) if worker_proc.returncode is not None else None}
    (outdir / "_worker_exit.json").write_text(
        json.dumps(exit_info, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    if not metrics_after_path.exists():
        metrics_after_path.write_text("scrape_failed: missing_metrics_after\n", encoding="utf-8")

    if (not stopped_by_controller) and (worker_proc.returncode not in (None, 0)):
        print(f"[labs run {SCENARIO_ES_429_INJECT}] worker exited early: rc={worker_proc.returncode}")
        print(f"[labs run {SCENARIO_ES_429_INJECT}] see logs: {log_path}")
        return 4

    print(f"[labs run {SCENARIO_ES_429_INJECT}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_ES_429_INJECT}] outputs: {outdir}")
    return 0


def _cmd_labs_verify_es_429_inject(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_ES_429_INJECT)
    metrics_dir = run_dir / "_metrics"
    before_path = metrics_dir / "metrics-before.txt"
    after_path = metrics_dir / "metrics-after.txt"

    before = before_path.read_text(encoding="utf-8") if before_path.exists() else ""
    after = after_path.read_text(encoding="utf-8") if after_path.exists() else ""

    retry_before = _prom_parse_counter_sum(before, "outbox_retry_scheduled_total", labels={"reason": "es_429"})
    retry_after = _prom_parse_counter_sum(after, "outbox_retry_scheduled_total", labels={"reason": "es_429"})
    failed_before = _prom_parse_counter_sum(before, "outbox_failed_total", labels={"reason": "es_429"})
    failed_after = _prom_parse_counter_sum(after, "outbox_failed_total", labels={"reason": "es_429"})
    terminal_before = _prom_parse_counter_sum(before, "outbox_terminal_failed_total", labels={"reason": "es_429"})
    terminal_after = _prom_parse_counter_sum(after, "outbox_terminal_failed_total", labels={"reason": "es_429"})

    delta_retry = retry_after - retry_before
    delta_failed = failed_after - failed_before
    delta_terminal = terminal_after - terminal_before

    ok = (
        (delta_retry >= float(args.min_retry_delta))
        and (delta_failed >= float(args.min_failed_delta))
        and (delta_terminal <= float(args.max_terminal_delta))
    )

    result = {
        "scenario": SCENARIO_ES_429_INJECT,
        "run_dir": str(run_dir),
        "checks": {
            "retry_delta_ge": float(args.min_retry_delta),
            "failed_delta_ge": float(args.min_failed_delta),
            "terminal_delta_le": float(args.max_terminal_delta),
        },
        "observed": {
            "outbox_retry_scheduled_total_reason_es_429": {"before": retry_before, "after": retry_after, "delta": delta_retry},
            "outbox_failed_total_reason_es_429": {"before": failed_before, "after": failed_after, "delta": delta_failed},
            "outbox_terminal_failed_total_reason_es_429": {"before": terminal_before, "after": terminal_after, "delta": delta_terminal},
        },
        "ok": bool(ok),
    }
    (run_dir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if ok:
        print(f"[labs verify {SCENARIO_ES_429_INJECT}] OK")
        return 0
    print(f"[labs verify {SCENARIO_ES_429_INJECT}] FAILED")
    return 10


def _cmd_labs_run_es_down_connect(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_labs_auto_run_dir(scenario=SCENARIO_ES_DOWN_CONNECT, run_id=run_id)

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    exports_dir = outdir / "_exports"
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)
    _ensure_dir(exports_dir)

    env = _with_backend_pythonpath(_load_env(env_file=args.env_file))

    # Tracing: stable defaults
    service_name = args.service
    env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    env.setdefault("OTEL_SERVICE_NAME", service_name)
    env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    # Ensure 429 injection is disabled (we want pure connect failure).
    env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = "0"
    env.pop("OUTBOX_EXPERIMENT_ES_429_EVERY_N", None)

    env["OUTBOX_METRICS_PORT"] = str(int(args.metrics_port))

    compose_file = str((REPO_ROOT / "docker-compose.infra.yml").resolve())
    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_ES_DOWN_CONNECT,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": args.env_file,
        "service": service_name,
        "inject": {"kind": "es_down", "compose": {"file": compose_file, "service": "es", "action": "stop"}},
        "worker": {"duration_s": int(args.duration), "metrics_port": int(args.metrics_port)},
        "trigger": {"op": str(args.op)},
    }
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] outdir: {outdir}")

    # 1) Inject: stop ES
    stop_proc = _docker_compose(args=["-f", compose_file, "stop", "es"], cwd=REPO_ROOT)
    (outdir / "_inject_es_stop.stdout.txt").write_text(stop_proc.stdout or "", encoding="utf-8")
    (outdir / "_inject_es_stop.stderr.txt").write_text(stop_proc.stderr or "", encoding="utf-8")
    (outdir / "_inject_es_stop.exitcode.txt").write_text(str(int(stop_proc.returncode)) + "\n", encoding="utf-8")
    if stop_proc.returncode != 0:
        print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] failed to stop es: rc={stop_proc.returncode}")
        return 2

    # 2) Run worker, scrape baseline, then trigger.
    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    log_path = logs_dir / f"worker-{run_id}.log"
    cmd = [_python_exe(), "-u", str(worker)]

    print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] worker log: {log_path}")

    metrics_before_path = metrics_dir / "metrics-before.txt"
    metrics_after_path = metrics_dir / "metrics-after.txt"

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"

    start = time.time()
    stopped_by_controller = False
    with open(log_path, "w", encoding="utf-8") as log_file:
        worker_proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)
        try:
            time.sleep(max(0.5, float(args.scrape_delay)))
            try:
                metrics_before = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                metrics_before_path.write_text(metrics_before, encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                metrics_before_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

            trigger_env = env.copy()
            trigger_env["OUTBOX_OP"] = str(args.op)
            trigger_env.setdefault("OUTBOX_CREATE_SEARCH_INDEX_ROW", "1")
            trigger_env.setdefault("OUTBOX_EVENT_VERSION", "0")

            proc = subprocess.run(
                [_python_exe(), str(inserter)],
                cwd=str(REPO_ROOT),
                env=trigger_env,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            (outdir / "_trigger_insert_outbox.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
            (outdir / "_trigger_insert_outbox.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
            if proc.returncode != 0:
                print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] failed to insert outbox event: rc={proc.returncode}")
                worker_proc.terminate()
                worker_proc.wait(timeout=30)
                return 3

            outbox_event_id = (proc.stdout or "").strip().splitlines()[-1].strip()
            (outdir / "_outbox_event_id.txt").write_text(outbox_event_id + "\n", encoding="utf-8")
            print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] outbox_event_id: {outbox_event_id}")

            while True:
                if args.duration > 0 and (time.time() - start) >= args.duration:
                    try:
                        metrics_after = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    stopped_by_controller = True
                    worker_proc.terminate()
                    break

                ret = worker_proc.poll()
                if ret is not None:
                    try:
                        metrics_after = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    break
                time.sleep(0.25)
        except KeyboardInterrupt:
            stopped_by_controller = True
            worker_proc.terminate()

        worker_proc.wait(timeout=30)

    exit_info = {"returncode": int(worker_proc.returncode) if worker_proc.returncode is not None else None}
    (outdir / "_worker_exit.json").write_text(
        json.dumps(exit_info, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    if not metrics_after_path.exists():
        metrics_after_path.write_text("scrape_failed: missing_metrics_after\n", encoding="utf-8")

    if (not stopped_by_controller) and (worker_proc.returncode not in (None, 0)):
        print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] worker exited early: rc={worker_proc.returncode}")
        print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] see logs: {log_path}")
        return 4

    print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] outputs: {outdir}")
    return 0


def _cmd_labs_verify_es_down_connect(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_ES_DOWN_CONNECT)
    metrics_dir = run_dir / "_metrics"
    before_path = metrics_dir / "metrics-before.txt"
    after_path = metrics_dir / "metrics-after.txt"

    before = before_path.read_text(encoding="utf-8") if before_path.exists() else ""
    after = after_path.read_text(encoding="utf-8") if after_path.exists() else ""

    reasons = ["es_connect", "es_unreachable"]

    retry_before = _prom_sum_reasons(before, "outbox_retry_scheduled_total", reasons=reasons)
    retry_after = _prom_sum_reasons(after, "outbox_retry_scheduled_total", reasons=reasons)
    failed_before = _prom_sum_reasons(before, "outbox_failed_total", reasons=reasons)
    failed_after = _prom_sum_reasons(after, "outbox_failed_total", reasons=reasons)
    terminal_before = _prom_sum_reasons(before, "outbox_terminal_failed_total", reasons=reasons)
    terminal_after = _prom_sum_reasons(after, "outbox_terminal_failed_total", reasons=reasons)

    delta_retry = retry_after - retry_before
    delta_failed = failed_after - failed_before
    delta_terminal = terminal_after - terminal_before

    ok = (
        (delta_retry >= float(args.min_retry_delta))
        and (delta_failed >= float(args.min_failed_delta))
        and (delta_terminal <= float(args.max_terminal_delta))
    )

    result = {
        "scenario": SCENARIO_ES_DOWN_CONNECT,
        "run_dir": str(run_dir),
        "checks": {
            "reasons": reasons,
            "retry_delta_ge": float(args.min_retry_delta),
            "failed_delta_ge": float(args.min_failed_delta),
            "terminal_delta_le": float(args.max_terminal_delta),
        },
        "observed": {
            "outbox_retry_scheduled_total_reason_es_connect_or_unreachable": {"before": retry_before, "after": retry_after, "delta": delta_retry},
            "outbox_failed_total_reason_es_connect_or_unreachable": {"before": failed_before, "after": failed_after, "delta": delta_failed},
            "outbox_terminal_failed_total_reason_es_connect_or_unreachable": {"before": terminal_before, "after": terminal_after, "delta": delta_terminal},
        },
        "ok": bool(ok),
    }
    (run_dir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if ok:
        print(f"[labs verify {SCENARIO_ES_DOWN_CONNECT}] OK")
        return 0
    print(f"[labs verify {SCENARIO_ES_DOWN_CONNECT}] FAILED")
    return 10


def _cmd_labs_export_es_down_connect(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_ES_DOWN_CONNECT)
    exports_dir = run_dir / "_exports"
    _ensure_dir(exports_dir)

    outbox_event_id_path = run_dir / "_outbox_event_id.txt"
    outbox_event_id = outbox_event_id_path.read_text(encoding="utf-8").strip() if outbox_event_id_path.exists() else None

    cmd = [
        _python_exe(),
        str(LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"),
        "--outdir",
        str(exports_dir),
        "--service",
        args.service,
        "--lookback",
        args.lookback,
        "--limit",
        str(args.limit),
    ]
    if outbox_event_id:
        cmd += ["--outbox-event-id", outbox_event_id]

    return _run(cmd, cwd=REPO_ROOT)


def _cmd_labs_run_collector_down(args: argparse.Namespace) -> int:
    """P1: observability failure drill - stop Jaeger OTLP collector while worker runs.

    We use the `jaeger` service in docker-compose.infra.yml as the OTLP receiver.
    Expected behavior: business processing continues; traces export is unavailable.
    """

    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_labs_auto_run_dir(scenario=SCENARIO_COLLECTOR_DOWN, run_id=run_id)

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    exports_dir = outdir / "_exports"
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)
    _ensure_dir(exports_dir)

    env = _with_backend_pythonpath(_load_env(env_file=args.env_file))

    # Tracing intentionally enabled; endpoint remains the default Jaeger OTLP gRPC.
    service_name = args.service
    env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    env.setdefault("OTEL_SERVICE_NAME", service_name)
    env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    env["OUTBOX_METRICS_PORT"] = str(int(args.metrics_port))

    compose_file = str((REPO_ROOT / "docker-compose.infra.yml").resolve())
    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_COLLECTOR_DOWN,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": args.env_file,
        "service": service_name,
        "inject": {"kind": "collector_down", "compose": {"file": compose_file, "service": "jaeger", "action": "stop"}},
        "worker": {"duration_s": int(args.duration), "metrics_port": int(args.metrics_port)},
        "trigger": {"op": str(args.op)},
    }
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] outdir: {outdir}")

    # 1) Inject: stop Jaeger (OTLP collector + query API)
    stop_proc = _docker_compose(args=["-f", compose_file, "stop", "jaeger"], cwd=REPO_ROOT)
    (outdir / "_inject_jaeger_stop.stdout.txt").write_text(stop_proc.stdout or "", encoding="utf-8")
    (outdir / "_inject_jaeger_stop.stderr.txt").write_text(stop_proc.stderr or "", encoding="utf-8")
    (outdir / "_inject_jaeger_stop.exitcode.txt").write_text(str(int(stop_proc.returncode)) + "\n", encoding="utf-8")
    if stop_proc.returncode != 0:
        print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] failed to stop jaeger: rc={stop_proc.returncode}")
        return 2

    # 2) Run worker, scrape baseline, then trigger.
    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    log_path = logs_dir / f"worker-{run_id}.log"
    cmd = [_python_exe(), "-u", str(worker)]

    print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] worker log: {log_path}")

    metrics_before_path = metrics_dir / "metrics-before.txt"
    metrics_after_path = metrics_dir / "metrics-after.txt"

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"

    start = time.time()
    stopped_by_controller = False
    with open(log_path, "w", encoding="utf-8") as log_file:
        worker_proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)
        try:
            time.sleep(max(0.5, float(args.scrape_delay)))
            try:
                metrics_before = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                metrics_before_path.write_text(metrics_before, encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                metrics_before_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

            trigger_env = env.copy()
            trigger_env["OUTBOX_OP"] = str(args.op)
            trigger_env.setdefault("OUTBOX_CREATE_SEARCH_INDEX_ROW", "1")
            trigger_env.setdefault("OUTBOX_EVENT_VERSION", "0")

            proc = subprocess.run(
                [_python_exe(), str(inserter)],
                cwd=str(REPO_ROOT),
                env=trigger_env,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            (outdir / "_trigger_insert_outbox.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
            (outdir / "_trigger_insert_outbox.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
            if proc.returncode != 0:
                print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] failed to insert outbox event: rc={proc.returncode}")
                worker_proc.terminate()
                worker_proc.wait(timeout=30)
                return 3

            outbox_event_id = (proc.stdout or "").strip().splitlines()[-1].strip()
            (outdir / "_outbox_event_id.txt").write_text(outbox_event_id + "\n", encoding="utf-8")
            print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] outbox_event_id: {outbox_event_id}")

            while True:
                if args.duration > 0 and (time.time() - start) >= args.duration:
                    try:
                        metrics_after = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    stopped_by_controller = True
                    worker_proc.terminate()
                    break

                ret = worker_proc.poll()
                if ret is not None:
                    try:
                        metrics_after = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    break
                time.sleep(0.25)
        except KeyboardInterrupt:
            stopped_by_controller = True
            worker_proc.terminate()

        worker_proc.wait(timeout=30)

    exit_info = {"returncode": int(worker_proc.returncode) if worker_proc.returncode is not None else None}
    (outdir / "_worker_exit.json").write_text(
        json.dumps(exit_info, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    if not metrics_after_path.exists():
        metrics_after_path.write_text("scrape_failed: missing_metrics_after\n", encoding="utf-8")

    if (not stopped_by_controller) and (worker_proc.returncode not in (None, 0)):
        print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] worker exited early: rc={worker_proc.returncode}")
        print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] see logs: {log_path}")
        return 4

    print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] outputs: {outdir}")
    return 0


def _cmd_labs_verify_collector_down(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_COLLECTOR_DOWN)
    metrics_dir = run_dir / "_metrics"

    before_path = metrics_dir / "metrics-before.txt"
    after_path = metrics_dir / "metrics-after.txt"

    before = before_path.read_text(encoding="utf-8") if before_path.exists() else ""
    after = after_path.read_text(encoding="utf-8") if after_path.exists() else ""

    before_scrape_ok = "scrape_failed" not in before
    after_scrape_ok = "scrape_failed" not in after

    processed_before = _prom_parse_counter_sum(before, "outbox_processed_total")
    processed_after = _prom_parse_counter_sum(after, "outbox_processed_total")
    failed_before = _prom_parse_counter_sum(before, "outbox_failed_total")
    failed_after = _prom_parse_counter_sum(after, "outbox_failed_total")

    delta_processed = processed_after - processed_before
    delta_failed = failed_after - failed_before

    # Fallback: metrics scrape can be flaky in CI due to timing.
    # For collector_down we can deterministically assert the inserted outbox row
    # was processed successfully.
    outbox_event_id_path = run_dir / "_outbox_event_id.txt"
    outbox_event_id = outbox_event_id_path.read_text(encoding="utf-8").strip() if outbox_event_id_path.exists() else None

    db_observed: dict[str, object] = {}
    db_ok = False
    try:
        recipe_env_file = None
        recipe_path = run_dir / "_recipe.json"
        if recipe_path.exists():
            try:
                recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
                recipe_env_file = (recipe or {}).get("env_file")
            except Exception:
                recipe_env_file = None

        env = _load_env(env_file=str(recipe_env_file) if recipe_env_file else None)
        database_url = (env.get("DATABASE_URL") or "").strip()
        if database_url and outbox_event_id:
            engine = create_engine(database_url, pool_pre_ping=True)
            with engine.connect() as conn:
                row = conn.execute(
                    text(
                        """
                        SELECT status, processed_at, attempts, error_reason
                        FROM search_outbox_events
                        WHERE id = CAST(:id AS uuid)
                        """
                    ),
                    {"id": outbox_event_id},
                ).mappings().fetchone()

            if row is None:
                db_observed = {"found": False}
            else:
                status = row.get("status")
                processed_at = row.get("processed_at")
                attempts = row.get("attempts")
                error_reason = row.get("error_reason")
                db_observed = {
                    "found": True,
                    "status": status,
                    "processed_at": str(processed_at) if processed_at is not None else None,
                    "attempts": int(attempts) if attempts is not None else None,
                    "error_reason": error_reason,
                }
                db_ok = (status == "done") and (processed_at is not None)
    except Exception as exc:  # noqa: BLE001
        db_observed = {"error": f"{type(exc).__name__}: {exc}"}
        db_ok = False

    inject_exitcode_path = run_dir / "_inject_jaeger_stop.exitcode.txt"
    inject_exitcode = None
    if inject_exitcode_path.exists():
        try:
            inject_exitcode = int((inject_exitcode_path.read_text(encoding="utf-8", errors="replace") or "").strip() or "0")
        except Exception:
            inject_exitcode = None

    metrics_ok = (
        before_scrape_ok
        and after_scrape_ok
        and (delta_processed >= float(args.min_processed_delta))
        and (delta_failed <= float(args.max_failed_delta))
    )

    # Accept either strong metrics evidence or DB evidence that the outbox row
    # was processed successfully.
    ok = (inject_exitcode == 0) and (metrics_ok or db_ok)

    result = {
        "scenario": SCENARIO_COLLECTOR_DOWN,
        "run_dir": str(run_dir),
        "outbox_event_id": outbox_event_id,
        "checks": {
            "inject_jaeger_stop_exitcode_eq": 0,
            "min_processed_delta": float(args.min_processed_delta),
            "max_failed_delta": float(args.max_failed_delta),
            "metrics_scrape_required": True,
            "db_outbox_processed_fallback_allowed": True,
        },
        "observed": {
            "inject_jaeger_stop_exitcode": inject_exitcode,
            "metrics_before_scrape_ok": bool(before_scrape_ok),
            "metrics_after_scrape_ok": bool(after_scrape_ok),
            "outbox_processed_total": {"before": processed_before, "after": processed_after, "delta": delta_processed},
            "outbox_failed_total": {"before": failed_before, "after": failed_after, "delta": delta_failed},
            "db_outbox_event": db_observed,
        },
        "ok": bool(ok),
    }
    (run_dir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if ok:
        print(f"[labs verify {SCENARIO_COLLECTOR_DOWN}] OK")
        return 0
    why = []
    if inject_exitcode != 0:
        why.append(f"inject_exitcode={inject_exitcode}")
    if not metrics_ok:
        why.append(
            f"metrics_ok=false (before_ok={before_scrape_ok} after_ok={after_scrape_ok} delta_processed={delta_processed} delta_failed={delta_failed})"
        )
    if not db_ok:
        why.append("db_ok=false")
    print(f"[labs verify {SCENARIO_COLLECTOR_DOWN}] FAILED: {'; '.join(why) if why else 'unknown'}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 10


def _cmd_labs_export_collector_down(args: argparse.Namespace) -> int:
    """Export evidence for collector_down.

    Jaeger is intentionally stopped, so trace export may fail. We treat that failure
    as expected and still return rc=0 after writing evidence files.
    """

    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_COLLECTOR_DOWN)
    exports_dir = run_dir / "_exports"
    _ensure_dir(exports_dir)

    outbox_event_id_path = run_dir / "_outbox_event_id.txt"
    outbox_event_id = outbox_event_id_path.read_text(encoding="utf-8").strip() if outbox_event_id_path.exists() else None

    cmd = [
        _python_exe(),
        str(LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"),
        "--outdir",
        str(exports_dir),
        "--service",
        args.service,
        "--lookback",
        args.lookback,
        "--limit",
        str(args.limit),
    ]
    if outbox_event_id:
        cmd += ["--outbox-event-id", outbox_event_id]

    print("[scripts] run:", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, check=False)
    (run_dir / "_export_jaeger.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (run_dir / "_export_jaeger.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (run_dir / "_export_jaeger.exitcode.txt").write_text(str(int(proc.returncode)) + "\n", encoding="utf-8")

    if proc.returncode != 0:
        (run_dir / "_export_note.txt").write_text(
            "collector_down: Jaeger is intentionally stopped; trace export failure is expected.\n",
            encoding="utf-8",
        )

    return 0


def _cmd_labs_clean_collector_down(args: argparse.Namespace) -> int:
    # 1) Restore Jaeger
    compose_file = str((REPO_ROOT / "docker-compose.infra.yml").resolve())
    start_proc = _docker_compose(args=["-f", compose_file, "start", "jaeger"], cwd=REPO_ROOT)
    print(f"[labs clean {SCENARIO_COLLECTOR_DOWN}] start jaeger: rc={start_proc.returncode}")

    if args.outdir:
        outdir = Path(args.outdir)
        _ensure_dir(outdir)
        (outdir / "_clean.txt").write_text(
            f"scenario={SCENARIO_COLLECTOR_DOWN}\n"
            "action=start_jaeger\n"
            f"at={time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )
        (outdir / "_clean_jaeger_start.stdout.txt").write_text(start_proc.stdout or "", encoding="utf-8")
        (outdir / "_clean_jaeger_start.stderr.txt").write_text(start_proc.stderr or "", encoding="utf-8")
        (outdir / "_clean_jaeger_start.exitcode.txt").write_text(str(int(start_proc.returncode)) + "\n", encoding="utf-8")

    # 2) Optional pruning
    if args.keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_COLLECTOR_DOWN
        if base.exists():
            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(args.keep_last) :]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_COLLECTOR_DOWN}] kept_last={args.keep_last}")

    return 0


def _cmd_labs_run_duplicate_delivery(args: argparse.Namespace) -> int:
    """ExpG: duplicate delivery / idempotency via delete-on-missing (404 noop).

    Strategy:
    1) Insert 1 upsert for a fixed entity_id and ensure a search_index row exists.
    2) Insert 2 deletes for the same entity_id (second should be a noop: ES 404).
    """

    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_labs_auto_run_dir(scenario=SCENARIO_DUPLICATE_DELIVERY, run_id=run_id)

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    exports_dir = outdir / "_exports"
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)
    _ensure_dir(exports_dir)

    env = _with_backend_pythonpath(_load_env(env_file=args.env_file))

    # Tracing: stable defaults
    service_name = args.service
    env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    env.setdefault("OTEL_SERVICE_NAME", service_name)
    env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    # Prefer per-event spans for this experiment.
    env["OUTBOX_USE_ES_BULK"] = "0"

    # ES connection defaults for local infra compose (only if env-file didn't specify them).
    env.setdefault("ELASTIC_URL", "http://localhost:19200")
    env.setdefault("ELASTIC_INDEX", "wordloom-test-search-index")

    # Ensure other experiments do not interfere.
    env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = "0"
    env.pop("OUTBOX_EXPERIMENT_ES_429_EVERY_N", None)
    env["OUTBOX_EXPERIMENT_ES_BULK_PARTIAL"] = "0"
    env["OUTBOX_EXPERIMENT_BREAK_CLAIM"] = "0"
    env["OUTBOX_EXPERIMENT_PROCESS_SLEEP_SECONDS"] = "0"

    env["OUTBOX_METRICS_PORT"] = str(int(args.metrics_port))

    entity_id = str(args.entity_id).strip() if args.entity_id else str(uuid.uuid4())
    (outdir / "_entity_id.txt").write_text(entity_id + "\n", encoding="utf-8")

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_DUPLICATE_DELIVERY,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": args.env_file,
        "service": service_name,
        "entity": {"entity_type": str(args.entity_type), "entity_id": entity_id},
        "worker": {"duration_s": int(args.duration), "metrics_port": int(args.metrics_port)},
        "trigger": {"upsert_count": 1, "delete_count": int(args.delete_count)},
        "expect": {"idempotent_noop": {"kind": "es_delete_404", "count": 1}},
    }
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    log_path = logs_dir / f"worker-{run_id}.log"
    cmd = [_python_exe(), "-u", str(worker)]

    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] worker log: {log_path}")
    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] entity_id: {entity_id}")

    metrics_before_path = metrics_dir / "metrics-before.txt"
    metrics_after_path = metrics_dir / "metrics-after.txt"

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"

    start = time.time()
    stopped_by_controller = False
    outbox_event_ids: list[str] = []

    with open(log_path, "w", encoding="utf-8") as log_file:
        worker_proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)
        try:
            time.sleep(max(0.5, float(args.scrape_delay)))
            try:
                metrics_before = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                metrics_before_path.write_text(metrics_before, encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                metrics_before_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

            # 1) Upsert (ensures doc exists in ES via search_index)
            upsert_env = env.copy()
            upsert_env["OUTBOX_ENTITY_TYPE"] = str(args.entity_type)
            upsert_env["OUTBOX_ENTITY_ID"] = entity_id
            upsert_env["OUTBOX_OP"] = "upsert"
            upsert_env["OUTBOX_CREATE_SEARCH_INDEX_ROW"] = "1"
            upsert_env.setdefault("OUTBOX_EVENT_VERSION", "0")

            proc = subprocess.run(
                [_python_exe(), str(inserter)],
                cwd=str(REPO_ROOT),
                env=upsert_env,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            (outdir / "_trigger_upsert.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
            (outdir / "_trigger_upsert.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
            if proc.returncode != 0:
                print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] failed to insert upsert outbox event: rc={proc.returncode}")
                worker_proc.terminate()
                worker_proc.wait(timeout=30)
                return 3

            upsert_event_id = (proc.stdout or "").strip().splitlines()[-1].strip()
            outbox_event_ids.append(upsert_event_id)
            time.sleep(1.5)

            # 2) Duplicate deletes (second should be ES 404 noop)
            delete_env = env.copy()
            delete_env["OUTBOX_ENTITY_TYPE"] = str(args.entity_type)
            delete_env["OUTBOX_ENTITY_ID"] = entity_id
            delete_env["OUTBOX_OP"] = "delete"
            delete_env.setdefault("OUTBOX_EVENT_VERSION", "0")
            delete_env["OUTBOX_CREATE_SEARCH_INDEX_ROW"] = "0"

            for idx in range(max(1, int(args.delete_count))):
                proc2 = subprocess.run(
                    [_python_exe(), str(inserter)],
                    cwd=str(REPO_ROOT),
                    env=delete_env,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                (outdir / f"_trigger_delete_{idx+1}.stdout.txt").write_text(proc2.stdout or "", encoding="utf-8")
                (outdir / f"_trigger_delete_{idx+1}.stderr.txt").write_text(proc2.stderr or "", encoding="utf-8")
                if proc2.returncode != 0:
                    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] failed to insert delete outbox event #{idx+1}: rc={proc2.returncode}")
                    worker_proc.terminate()
                    worker_proc.wait(timeout=30)
                    return 4
                delete_event_id = (proc2.stdout or "").strip().splitlines()[-1].strip()
                outbox_event_ids.append(delete_event_id)

            (outdir / "_outbox_event_ids.txt").write_text("\n".join(outbox_event_ids) + "\n", encoding="utf-8")

            while True:
                if args.duration > 0 and (time.time() - start) >= args.duration:
                    try:
                        metrics_after = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    stopped_by_controller = True
                    worker_proc.terminate()
                    break

                ret = worker_proc.poll()
                if ret is not None:
                    try:
                        metrics_after = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    break
                time.sleep(0.25)
        except KeyboardInterrupt:
            stopped_by_controller = True
            worker_proc.terminate()

        worker_proc.wait(timeout=30)

    exit_info = {"returncode": int(worker_proc.returncode) if worker_proc.returncode is not None else None}
    (outdir / "_worker_exit.json").write_text(
        json.dumps(exit_info, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    if not metrics_after_path.exists():
        metrics_after_path.write_text("scrape_failed: missing_metrics_after\n", encoding="utf-8")

    if (not stopped_by_controller) and (worker_proc.returncode not in (None, 0)):
        print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] worker exited early: rc={worker_proc.returncode}")
        print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] see logs: {log_path}")
        return 5

    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] outputs: {outdir}")
    return 0


def _cmd_labs_verify_duplicate_delivery(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_DUPLICATE_DELIVERY)
    metrics_dir = run_dir / "_metrics"
    logs_dir = run_dir / "_logs"

    before_path = metrics_dir / "metrics-before.txt"
    after_path = metrics_dir / "metrics-after.txt"

    before = before_path.read_text(encoding="utf-8") if before_path.exists() else ""
    after = after_path.read_text(encoding="utf-8") if after_path.exists() else ""

    processed_before = _prom_parse_counter_sum(before, "outbox_processed_total")
    processed_after = _prom_parse_counter_sum(after, "outbox_processed_total")
    failed_before = _prom_parse_counter_sum(before, "outbox_failed_total")
    failed_after = _prom_parse_counter_sum(after, "outbox_failed_total")
    noop_before = _prom_parse_counter_sum(before, "outbox_idempotent_noop_total")
    noop_after = _prom_parse_counter_sum(after, "outbox_idempotent_noop_total")

    # Backward-safe: if metrics are missing or the new metric isn't present, rely on logs.

    delta_processed = processed_after - processed_before
    delta_failed = failed_after - failed_before
    delta_noop = noop_after - noop_before

    metrics_available = ("scrape_failed" not in before.lower()) and ("scrape_failed" not in after.lower())

    # Logs evidence: at least one noop delete line.
    log_paths = sorted([p for p in logs_dir.glob("*.log") if p.is_file()])
    noop_log_count = 0
    if log_paths:
        try:
            text = log_paths[0].read_text(encoding="utf-8", errors="replace")
            noop_log_count = len(re.findall(r"Outbox delete: doc .* not found in ES \(noop\)", text))
        except Exception:
            noop_log_count = 0

    ok = (
        (delta_processed >= float(args.min_processed_delta))
        and (delta_failed <= float(args.max_failed_delta))
        and ((delta_noop >= float(args.min_noop_delta)) or (noop_log_count >= int(args.min_noop_logs)))
    )

    result = {
        "scenario": SCENARIO_DUPLICATE_DELIVERY,
        "run_dir": str(run_dir),
        "checks": {
            "min_processed_delta": float(args.min_processed_delta),
            "max_failed_delta": float(args.max_failed_delta),
            "min_noop_delta": float(args.min_noop_delta),
            "min_noop_logs": int(args.min_noop_logs),
        },
        "observed": {
            "metrics_available": bool(metrics_available),
            "outbox_processed_total": {"before": processed_before, "after": processed_after, "delta": delta_processed},
            "outbox_failed_total": {"before": failed_before, "after": failed_after, "delta": delta_failed},
            "outbox_idempotent_noop_total": {"before": noop_before, "after": noop_after, "delta": delta_noop},
            "noop_log_count": int(noop_log_count),
        },
        "ok": bool(ok),
    }
    (run_dir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if ok:
        print(f"[labs verify {SCENARIO_DUPLICATE_DELIVERY}] OK")
        return 0
    print(f"[labs verify {SCENARIO_DUPLICATE_DELIVERY}] FAILED")
    return 10


def _cmd_labs_export_duplicate_delivery(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_DUPLICATE_DELIVERY)
    exports_dir = run_dir / "_exports"
    _ensure_dir(exports_dir)

    entity_id_path = run_dir / "_entity_id.txt"
    entity_id = entity_id_path.read_text(encoding="utf-8").strip() if entity_id_path.exists() else None

    tags = {
        "wordloom.obs_schema": SEARCH_OUTBOX_OBS_SCHEMA_VERSION,
    }
    if entity_id:
        tags["wordloom.entity_id"] = str(entity_id)

    cmd = [
        _python_exe(),
        str(LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"),
        "--outdir",
        str(exports_dir),
        "--service",
        args.service,
        "--lookback",
        args.lookback,
        "--limit",
        str(args.limit),
        "--operation",
        "outbox.process",
        "--tags-json",
        json.dumps(tags, ensure_ascii=False),
    ]
    return _run(cmd, cwd=REPO_ROOT)


def _cmd_labs_clean_duplicate_delivery(args: argparse.Namespace) -> int:
    # No external state to revert; optionally prune snapshots.
    if args.keep_last is None:
        return 0

    base = (LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_DUPLICATE_DELIVERY)
    if not base.exists():
        return 0

    runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
    for p in runs[int(args.keep_last):]:
        shutil.rmtree(p, ignore_errors=True)
    print(f"[labs clean {SCENARIO_DUPLICATE_DELIVERY}] kept_last={args.keep_last}")
    return 0


def _cmd_labs_run_es_bulk_partial(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_labs_auto_run_dir(scenario=SCENARIO_ES_BULK_PARTIAL, run_id=run_id)

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    exports_dir = outdir / "_exports"
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)
    _ensure_dir(exports_dir)

    env = _with_backend_pythonpath(_load_env(env_file=args.env_file))

    # Tracing: stable defaults
    service_name = args.service
    env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    env.setdefault("OTEL_SERVICE_NAME", service_name)
    env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    # Force ES bulk path + partial injection.
    env["OUTBOX_USE_ES_BULK"] = "1"
    env["OUTBOX_BULK_SIZE"] = str(int(args.bulk_size))
    env["OUTBOX_EXPERIMENT_ES_BULK_PARTIAL"] = "1"
    env["OUTBOX_EXPERIMENT_ES_BULK_PARTIAL_STATUS"] = str(int(args.partial_status))

    # Make ExpD deterministic:
    # - Slow poll so we can insert N events without races.
    # - Scrape metrics-before before inserting events so verify sees non-zero deltas.
    env["OUTBOX_POLL_INTERVAL_SECONDS"] = "5.0"

    # ES connection defaults for local infra compose (only if env-file didn't specify them).
    env.setdefault("ELASTIC_URL", "http://localhost:19200")
    env.setdefault("ELASTIC_INDEX", "wordloom-test-search-index")

    # Ensure other experiments do not interfere.
    env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = "0"
    env.pop("OUTBOX_EXPERIMENT_ES_429_EVERY_N", None)

    env["OUTBOX_METRICS_PORT"] = str(int(args.metrics_port))

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_ES_BULK_PARTIAL,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": args.env_file,
        "service": service_name,
        "inject": {
            "kind": "es_bulk_partial",
            "enabled": True,
            "status": int(args.partial_status),
        },
        "worker": {
            "duration_s": int(args.duration),
            "metrics_port": int(args.metrics_port),
            "use_es_bulk": True,
            "bulk_size": int(args.bulk_size),
        },
        "trigger": {"op": str(args.op), "count": int(args.trigger_count)},
    }
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    log_path = logs_dir / f"worker-{run_id}.log"
    cmd = [_python_exe(), "-u", str(worker)]

    print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] worker log: {log_path}")

    metrics_before_path = metrics_dir / "metrics-before.txt"
    metrics_after_path = metrics_dir / "metrics-after.txt"

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"

    start = time.time()
    stopped_by_controller = False
    outbox_event_ids: list[str] = []

    with open(log_path, "w", encoding="utf-8") as log_file:
        worker_proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)
        try:
            time.sleep(max(0.5, float(args.scrape_delay)))
            try:
                metrics_before = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                metrics_before_path.write_text(metrics_before, encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                metrics_before_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

            # Insert outbox events after metrics-before so verify sees meaningful deltas.
            trigger_env = env.copy()
            trigger_env["OUTBOX_OP"] = str(args.op)
            trigger_env.setdefault("OUTBOX_CREATE_SEARCH_INDEX_ROW", "1")
            trigger_env.setdefault("OUTBOX_EVENT_VERSION", "0")
            trigger_env["OUTBOX_INSERT_COUNT"] = str(int(args.trigger_count))

            proc = subprocess.run(
                [_python_exe(), str(inserter)],
                cwd=str(REPO_ROOT),
                env=trigger_env,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            (outdir / "_trigger_insert_outbox.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
            (outdir / "_trigger_insert_outbox.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
            if proc.returncode != 0:
                print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] failed to insert outbox events: rc={proc.returncode}")
                return 3

            outbox_event_ids = [ln.strip() for ln in (proc.stdout or "").splitlines() if ln.strip()]
            (outdir / "_outbox_event_ids.txt").write_text("\n".join(outbox_event_ids) + "\n", encoding="utf-8")
            print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] outbox_event_ids: {', '.join(outbox_event_ids)}")

            while True:
                if args.duration > 0 and (time.time() - start) >= args.duration:
                    try:
                        metrics_after = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    stopped_by_controller = True
                    worker_proc.terminate()
                    break

                ret = worker_proc.poll()
                if ret is not None:
                    try:
                        metrics_after = _scrape_metrics_text(port=int(args.metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    break
                time.sleep(0.25)
        except KeyboardInterrupt:
            stopped_by_controller = True
            worker_proc.terminate()

        worker_proc.wait(timeout=30)

    exit_info = {"returncode": int(worker_proc.returncode) if worker_proc.returncode is not None else None}
    (outdir / "_worker_exit.json").write_text(
        json.dumps(exit_info, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    if not metrics_after_path.exists():
        metrics_after_path.write_text("scrape_failed: missing_metrics_after\n", encoding="utf-8")

    claim_batch_id = _extract_last_claim_batch_id(log_path)
    if claim_batch_id:
        (outdir / "_claim_batch_id.txt").write_text(claim_batch_id + "\n", encoding="utf-8")

    if (not stopped_by_controller) and (worker_proc.returncode not in (None, 0)):
        print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] worker exited early: rc={worker_proc.returncode}")
        print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] see logs: {log_path}")
        return 4

    print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] outputs: {outdir}")
    return 0


def _cmd_labs_verify_es_bulk_partial(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_ES_BULK_PARTIAL)
    metrics_dir = run_dir / "_metrics"
    before_path = metrics_dir / "metrics-before.txt"
    after_path = metrics_dir / "metrics-after.txt"

    before = before_path.read_text(encoding="utf-8") if before_path.exists() else ""
    after = after_path.read_text(encoding="utf-8") if after_path.exists() else ""

    partial_before = _prom_parse_counter_sum(before, "outbox_es_bulk_requests_total", labels={"result": "partial"})
    partial_after = _prom_parse_counter_sum(after, "outbox_es_bulk_requests_total", labels={"result": "partial"})

    success_items_before = (
        _prom_parse_counter_sum(before, "outbox_es_bulk_items_total", labels={"op": "index", "result": "success"})
        + _prom_parse_counter_sum(before, "outbox_es_bulk_items_total", labels={"op": "delete", "result": "success"})
    )
    success_items_after = (
        _prom_parse_counter_sum(after, "outbox_es_bulk_items_total", labels={"op": "index", "result": "success"})
        + _prom_parse_counter_sum(after, "outbox_es_bulk_items_total", labels={"op": "delete", "result": "success"})
    )

    failed_items_before = (
        _prom_parse_counter_sum(before, "outbox_es_bulk_items_total", labels={"op": "index", "result": "failed"})
        + _prom_parse_counter_sum(before, "outbox_es_bulk_items_total", labels={"op": "delete", "result": "failed"})
    )
    failed_items_after = (
        _prom_parse_counter_sum(after, "outbox_es_bulk_items_total", labels={"op": "index", "result": "failed"})
        + _prom_parse_counter_sum(after, "outbox_es_bulk_items_total", labels={"op": "delete", "result": "failed"})
    )

    failed_4xx_before = (
        _prom_parse_counter_sum(before, "outbox_es_bulk_item_failures_total", labels={"op": "index", "failure_class": "4xx"})
        + _prom_parse_counter_sum(before, "outbox_es_bulk_item_failures_total", labels={"op": "delete", "failure_class": "4xx"})
    )
    failed_4xx_after = (
        _prom_parse_counter_sum(after, "outbox_es_bulk_item_failures_total", labels={"op": "index", "failure_class": "4xx"})
        + _prom_parse_counter_sum(after, "outbox_es_bulk_item_failures_total", labels={"op": "delete", "failure_class": "4xx"})
    )

    delta_partial = partial_after - partial_before
    delta_success_items = success_items_after - success_items_before
    delta_failed_items = failed_items_after - failed_items_before
    delta_failed_4xx = failed_4xx_after - failed_4xx_before

    ok = (
        (delta_partial >= float(args.min_partial_delta))
        and (delta_success_items >= float(args.min_success_items_delta))
        and (delta_failed_items >= float(args.min_failed_items_delta))
        and (delta_failed_4xx >= float(args.min_failed_4xx_delta))
    )

    result = {
        "scenario": SCENARIO_ES_BULK_PARTIAL,
        "run_dir": str(run_dir),
        "checks": {
            "partial_delta_ge": float(args.min_partial_delta),
            "success_items_delta_ge": float(args.min_success_items_delta),
            "failed_items_delta_ge": float(args.min_failed_items_delta),
            "failed_4xx_delta_ge": float(args.min_failed_4xx_delta),
        },
        "observed": {
            "outbox_es_bulk_requests_total_result_partial": {"before": partial_before, "after": partial_after, "delta": delta_partial},
            "outbox_es_bulk_items_total_success_sum": {"before": success_items_before, "after": success_items_after, "delta": delta_success_items},
            "outbox_es_bulk_items_total_failed_sum": {"before": failed_items_before, "after": failed_items_after, "delta": delta_failed_items},
            "outbox_es_bulk_item_failures_total_failure_class_4xx_sum": {"before": failed_4xx_before, "after": failed_4xx_after, "delta": delta_failed_4xx},
        },
        "ok": bool(ok),
    }
    (run_dir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if ok:
        print(f"[labs verify {SCENARIO_ES_BULK_PARTIAL}] OK")
        return 0
    print(f"[labs verify {SCENARIO_ES_BULK_PARTIAL}] FAILED")
    return 10


def _cmd_labs_export_es_bulk_partial(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_ES_BULK_PARTIAL)
    exports_dir = run_dir / "_exports"
    _ensure_dir(exports_dir)

    claim_batch_id_path = run_dir / "_claim_batch_id.txt"
    claim_batch_id = claim_batch_id_path.read_text(encoding="utf-8").strip() if claim_batch_id_path.exists() else None

    exporter = LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"
    base_cmd = [
        _python_exe(),
        str(exporter),
        "--outdir",
        str(exports_dir),
        "--service",
        args.service,
        "--lookback",
        args.lookback,
        "--limit",
        str(args.limit),
    ]

    if claim_batch_id:
        return _run(base_cmd + ["--claim-batch-id", claim_batch_id], cwd=REPO_ROOT)

    # Bulk mode may not emit per-event `outbox.process` spans, so exporting by outbox_event_id
    # is often empty. Use a narrowed tag export instead.
    return _run(
        base_cmd
        + ["--tags-json", json.dumps({"wordloom.obs_schema": SEARCH_OUTBOX_OBS_SCHEMA_VERSION}, ensure_ascii=False)],
        cwd=REPO_ROOT,
    )


def _cmd_labs_clean_es_bulk_partial(args: argparse.Namespace) -> int:
    # No external state to revert: injection is env-only.
    if args.outdir:
        outdir = Path(args.outdir)
        _ensure_dir(outdir)
        (outdir / "_clean.txt").write_text(
            f"scenario={SCENARIO_ES_BULK_PARTIAL}\n"
            "action=noop\n"
            f"at={time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )

    if args.keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_ES_BULK_PARTIAL
        if base.exists():
            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(args.keep_last):]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_ES_BULK_PARTIAL}] kept_last={args.keep_last}")
    else:
        print(f"[labs clean {SCENARIO_ES_BULK_PARTIAL}] noop")
    return 0


def _cmd_labs_run_db_claim_contention(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_labs_auto_run_dir(scenario=SCENARIO_DB_CLAIM_CONTENTION, run_id=run_id)

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    exports_dir = outdir / "_exports"
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)
    _ensure_dir(exports_dir)

    base_env = _with_backend_pythonpath(_load_env(env_file=args.env_file))

    # Tracing: stable defaults
    service_name = args.service
    base_env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    base_env.setdefault("OTEL_SERVICE_NAME", service_name)
    base_env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    base_env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    base_env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    # Local infra defaults (ensure ES is reachable even if env-file doesn't specify).
    base_env.setdefault("ELASTIC_URL", "http://localhost:19200")
    base_env.setdefault("ELASTIC_INDEX", "wordloom-test-search-index")

    # Keep logs parseable + export-friendly.
    base_env["LOG_LEVEL"] = "INFO"

    # Ensure other experiments do not interfere.
    base_env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = "0"
    base_env.pop("OUTBOX_EXPERIMENT_ES_429_EVERY_N", None)
    base_env.pop("OUTBOX_EXPERIMENT_ES_BULK_PARTIAL", None)

    # Force non-bulk path so per-event spans are likely to exist.
    base_env["OUTBOX_USE_ES_BULK"] = "0"

    # Experiment E injection: break claim atomicity to create contention signals.
    base_env["OUTBOX_EXPERIMENT_BREAK_CLAIM"] = "1"
    base_env["OUTBOX_EXPERIMENT_BREAK_CLAIM_SLEEP_SECONDS"] = str(float(args.break_claim_sleep))

    # Improve determinism for owner-mismatch signal:
    # give the competing worker a window to overwrite ownership after claim.
    base_env["OUTBOX_EXPERIMENT_PROCESS_SLEEP_SECONDS"] = str(max(1.0, float(args.break_claim_sleep)))

    # Make the claim loop tight to increase overlap probability.
    base_env["OUTBOX_POLL_INTERVAL_SECONDS"] = str(float(args.poll_interval))
    base_env["OUTBOX_BULK_SIZE"] = str(int(args.batch_size))
    base_env["OUTBOX_CONCURRENCY"] = "1"

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_DB_CLAIM_CONTENTION,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": args.env_file,
        "service": service_name,
        "inject": {
            "kind": "break_claim_atomicity",
            "enabled": True,
            "sleep_seconds": float(args.break_claim_sleep),
        },
        "worker": {
            "duration_s": int(args.duration),
            "metrics_ports": [int(args.metrics_port_1), int(args.metrics_port_2)],
            "poll_interval_seconds": float(args.poll_interval),
            "batch_size": int(args.batch_size),
        },
        "trigger": {"op": str(args.op), "count": int(args.trigger_count)},
    }
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    cmd = [_python_exe(), "-u", str(worker)]

    # Prepare env + logs for two competing worker processes.
    env1 = base_env.copy()
    env1["OUTBOX_WORKER_ID"] = str(args.worker_id_1)
    env1["OUTBOX_METRICS_PORT"] = str(int(args.metrics_port_1))
    env1["OUTBOX_HTTP_PORT"] = str(int(args.metrics_port_1) + 20)

    env2 = base_env.copy()
    env2["OUTBOX_WORKER_ID"] = str(args.worker_id_2)
    env2["OUTBOX_METRICS_PORT"] = str(int(args.metrics_port_2))
    env2["OUTBOX_HTTP_PORT"] = str(int(args.metrics_port_2) + 20)

    log_path_1 = logs_dir / f"worker1-{run_id}.log"
    log_path_2 = logs_dir / f"worker2-{run_id}.log"

    print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] worker1 log: {log_path_1} (metrics :{args.metrics_port_1})")
    print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] worker2 log: {log_path_2} (metrics :{args.metrics_port_2})")

    before_1_path = metrics_dir / "metrics-before-1.txt"
    before_2_path = metrics_dir / "metrics-before-2.txt"
    after_1_path = metrics_dir / "metrics-after-1.txt"
    after_2_path = metrics_dir / "metrics-after-2.txt"

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"

    start = time.time()
    stopped_by_controller = False
    outbox_event_ids: list[str] = []

    with open(log_path_1, "w", encoding="utf-8") as log_file_1, open(log_path_2, "w", encoding="utf-8") as log_file_2:
        proc1 = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env1, stdout=log_file_1, stderr=subprocess.STDOUT)
        proc2 = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env2, stdout=log_file_2, stderr=subprocess.STDOUT)
        try:
            time.sleep(max(0.5, float(args.scrape_delay)))
            try:
                before_1_path.write_text(_scrape_metrics_text(port=int(args.metrics_port_1), timeout_s=4.0), encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                before_1_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
            try:
                before_2_path.write_text(_scrape_metrics_text(port=int(args.metrics_port_2), timeout_s=4.0), encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                before_2_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

            for i in range(int(args.trigger_count)):
                trigger_env = base_env.copy()
                trigger_env["OUTBOX_OP"] = str(args.op)
                trigger_env.setdefault("OUTBOX_CREATE_SEARCH_INDEX_ROW", "1")
                trigger_env.setdefault("OUTBOX_EVENT_VERSION", "0")

                proc = subprocess.run(
                    [_python_exe(), str(inserter)],
                    cwd=str(REPO_ROOT),
                    env=trigger_env,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                (outdir / f"_trigger_insert_outbox_{i+1}.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
                (outdir / f"_trigger_insert_outbox_{i+1}.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
                if proc.returncode != 0:
                    print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] failed to insert outbox event #{i+1}: rc={proc.returncode}")
                    proc1.terminate()
                    proc2.terminate()
                    proc1.wait(timeout=30)
                    proc2.wait(timeout=30)
                    return 3
                outbox_event_id = (proc.stdout or "").strip().splitlines()[-1].strip()
                outbox_event_ids.append(outbox_event_id)

            (outdir / "_outbox_event_ids.txt").write_text("\n".join(outbox_event_ids) + "\n", encoding="utf-8")
            print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] outbox_event_ids: {', '.join(outbox_event_ids)}")

            while True:
                if args.duration > 0 and (time.time() - start) >= args.duration:
                    try:
                        after_1_path.write_text(_scrape_metrics_text(port=int(args.metrics_port_1), timeout_s=4.0), encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        after_1_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    try:
                        after_2_path.write_text(_scrape_metrics_text(port=int(args.metrics_port_2), timeout_s=4.0), encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        after_2_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    stopped_by_controller = True
                    proc1.terminate()
                    proc2.terminate()
                    break

                ret1 = proc1.poll()
                ret2 = proc2.poll()
                if ret1 is not None or ret2 is not None:
                    try:
                        after_1_path.write_text(_scrape_metrics_text(port=int(args.metrics_port_1), timeout_s=4.0), encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        after_1_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    try:
                        after_2_path.write_text(_scrape_metrics_text(port=int(args.metrics_port_2), timeout_s=4.0), encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        after_2_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    break
                time.sleep(0.25)
        except KeyboardInterrupt:
            stopped_by_controller = True
            proc1.terminate()
            proc2.terminate()

        proc1.wait(timeout=30)
        proc2.wait(timeout=30)

    exit_info = {
        "worker1": {"returncode": int(proc1.returncode) if proc1.returncode is not None else None},
        "worker2": {"returncode": int(proc2.returncode) if proc2.returncode is not None else None},
    }
    (outdir / "_worker_exit.json").write_text(json.dumps(exit_info, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Combined convenience file
    combined = (
        "# metrics-after-1\n\n" + (after_1_path.read_text(encoding="utf-8", errors="replace") if after_1_path.exists() else "")
        + "\n\n# metrics-after-2\n\n" + (after_2_path.read_text(encoding="utf-8", errors="replace") if after_2_path.exists() else "")
    )
    (outdir / "_metrics.txt").write_text(combined, encoding="utf-8")

    claim_batch_ids: list[str] = []
    for lp in (log_path_1, log_path_2):
        cid = _extract_last_claim_batch_id(lp)
        if cid:
            claim_batch_ids.append(cid)
    if claim_batch_ids:
        (outdir / "_claim_batch_ids.txt").write_text("\n".join(claim_batch_ids) + "\n", encoding="utf-8")

    if (not stopped_by_controller) and (proc1.returncode not in (None, 0) or proc2.returncode not in (None, 0)):
        print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] a worker exited early: rc1={proc1.returncode} rc2={proc2.returncode}")
        print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] see logs: {log_path_1} {log_path_2}")
        return 4

    print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] outputs: {outdir}")
    return 0


def _cmd_labs_verify_db_claim_contention(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_DB_CLAIM_CONTENTION)
    metrics_dir = run_dir / "_metrics"

    before1 = (metrics_dir / "metrics-before-1.txt").read_text(encoding="utf-8") if (metrics_dir / "metrics-before-1.txt").exists() else ""
    before2 = (metrics_dir / "metrics-before-2.txt").read_text(encoding="utf-8") if (metrics_dir / "metrics-before-2.txt").exists() else ""
    after1 = (metrics_dir / "metrics-after-1.txt").read_text(encoding="utf-8") if (metrics_dir / "metrics-after-1.txt").exists() else ""
    after2 = (metrics_dir / "metrics-after-2.txt").read_text(encoding="utf-8") if (metrics_dir / "metrics-after-2.txt").exists() else ""

    metric_owner_mismatch = "outbox_owner_mismatch_skips_total"
    metric_processed = "outbox_processed_total"
    metric_failed = "outbox_failed_total"

    mismatch_before = _prom_parse_counter_sum(before1, metric_owner_mismatch) + _prom_parse_counter_sum(before2, metric_owner_mismatch)
    mismatch_after = _prom_parse_counter_sum(after1, metric_owner_mismatch) + _prom_parse_counter_sum(after2, metric_owner_mismatch)

    processed_before = _prom_parse_counter_sum(before1, metric_processed) + _prom_parse_counter_sum(before2, metric_processed)
    processed_after = _prom_parse_counter_sum(after1, metric_processed) + _prom_parse_counter_sum(after2, metric_processed)

    failed_before = _prom_parse_counter_sum(before1, metric_failed) + _prom_parse_counter_sum(before2, metric_failed)
    failed_after = _prom_parse_counter_sum(after1, metric_failed) + _prom_parse_counter_sum(after2, metric_failed)

    delta_mismatch = mismatch_after - mismatch_before
    delta_processed = processed_after - processed_before
    delta_failed = failed_after - failed_before

    ok = (
        (delta_mismatch >= float(args.min_owner_mismatch_delta))
        and (delta_processed >= float(args.min_processed_delta))
        and (delta_failed <= float(args.max_failed_delta))
    )

    result = {
        "scenario": SCENARIO_DB_CLAIM_CONTENTION,
        "run_dir": str(run_dir),
        "checks": {
            "owner_mismatch_delta_ge": float(args.min_owner_mismatch_delta),
            "processed_delta_ge": float(args.min_processed_delta),
            "failed_delta_le": float(args.max_failed_delta),
        },
        "observed": {
            metric_owner_mismatch: {"before": mismatch_before, "after": mismatch_after, "delta": delta_mismatch},
            metric_processed: {"before": processed_before, "after": processed_after, "delta": delta_processed},
            metric_failed: {"before": failed_before, "after": failed_after, "delta": delta_failed},
        },
        "ok": bool(ok),
    }
    (run_dir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if ok:
        print(f"[labs verify {SCENARIO_DB_CLAIM_CONTENTION}] OK")
        return 0
    print(f"[labs verify {SCENARIO_DB_CLAIM_CONTENTION}] FAILED")
    return 10


def _cmd_labs_export_db_claim_contention(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_DB_CLAIM_CONTENTION)
    exports_dir = run_dir / "_exports"
    _ensure_dir(exports_dir)

    exporter = LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"
    base_cmd = [
        _python_exe(),
        str(exporter),
        "--outdir",
        str(exports_dir),
        "--service",
        args.service,
        "--lookback",
        args.lookback,
        "--limit",
        str(args.limit),
    ]

    # For ExpE, `outbox.claim_batch` is the primary evidence. Export a bounded sample.
    return _run(
        base_cmd
        + [
            "--operation",
            "outbox.claim_batch",
            "--tags-json",
            json.dumps({"wordloom.obs_schema": SEARCH_OUTBOX_OBS_SCHEMA_VERSION}, ensure_ascii=False),
        ],
        cwd=REPO_ROOT,
    )


def _cmd_labs_clean_db_claim_contention(args: argparse.Namespace) -> int:
    # No external state to revert: injection is env-only.
    if args.outdir:
        outdir = Path(args.outdir)
        _ensure_dir(outdir)
        (outdir / "_clean.txt").write_text(
            f"scenario={SCENARIO_DB_CLAIM_CONTENTION}\n"
            "action=noop\n"
            f"at={time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )

    if args.keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_DB_CLAIM_CONTENTION
        if base.exists():
            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(args.keep_last):]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_DB_CLAIM_CONTENTION}] kept_last={args.keep_last}")
    else:
        print(f"[labs clean {SCENARIO_DB_CLAIM_CONTENTION}] noop")
    return 0


def _cmd_labs_run_stuck_reclaim(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_labs_auto_run_dir(scenario=SCENARIO_STUCK_RECLAIM, run_id=run_id)

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    exports_dir = outdir / "_exports"
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)
    _ensure_dir(exports_dir)

    base_env = _with_backend_pythonpath(_load_env(env_file=args.env_file))

    # Tracing: stable defaults
    service_name = args.service
    base_env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    base_env.setdefault("OTEL_SERVICE_NAME", service_name)
    base_env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    base_env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    base_env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    # Local infra defaults
    base_env.setdefault("ELASTIC_URL", "http://localhost:19200")
    base_env.setdefault("ELASTIC_INDEX", "wordloom-test-search-index")

    # Keep logs parseable + export-friendly.
    base_env["LOG_LEVEL"] = "INFO"

    # Ensure other experiments do not interfere.
    base_env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = "0"
    base_env.pop("OUTBOX_EXPERIMENT_ES_429_EVERY_N", None)
    base_env.pop("OUTBOX_EXPERIMENT_ES_BULK_PARTIAL", None)
    base_env.pop("OUTBOX_EXPERIMENT_BREAK_CLAIM", None)
    base_env.pop("OUTBOX_EXPERIMENT_BREAK_CLAIM_SLEEP_SECONDS", None)

    # Force non-bulk path so per-event spans are likely to exist.
    base_env["OUTBOX_USE_ES_BULK"] = "0"

    # Tune lease/reclaim to make stuck+reclaim happen quickly.
    base_env["OUTBOX_LEASE_SECONDS"] = str(int(args.lease_seconds))
    base_env["OUTBOX_RECLAIM_INTERVAL_SECONDS"] = str(float(args.reclaim_interval))
    base_env["OUTBOX_MAX_PROCESSING_SECONDS"] = str(int(args.max_processing_seconds))
    base_env["OUTBOX_POLL_INTERVAL_SECONDS"] = str(float(args.poll_interval))
    base_env["OUTBOX_BULK_SIZE"] = str(int(args.batch_size))
    base_env["OUTBOX_CONCURRENCY"] = "1"

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_STUCK_RECLAIM,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": args.env_file,
        "service": service_name,
        "worker": {
            "duration_s": int(args.duration),
            "metrics_ports": [int(args.metrics_port_1), int(args.metrics_port_2)],
            "lease_seconds": int(args.lease_seconds),
            "reclaim_interval_seconds": float(args.reclaim_interval),
            "max_processing_seconds": int(args.max_processing_seconds),
            "poll_interval_seconds": float(args.poll_interval),
            "batch_size": int(args.batch_size),
        },
        "trigger": {"op": str(args.op), "count": int(args.trigger_count)},
        "crash": {"kind": "process_kill", "target": "worker1", "claim_timeout_s": float(args.claim_timeout)},
    }
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    cmd = [_python_exe(), "-u", str(worker)]

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"
    outbox_event_ids: list[str] = []
    for i in range(int(args.trigger_count)):
        trigger_env = base_env.copy()
        trigger_env["OUTBOX_OP"] = str(args.op)
        trigger_env.setdefault("OUTBOX_CREATE_SEARCH_INDEX_ROW", "1")
        trigger_env.setdefault("OUTBOX_EVENT_VERSION", "0")

        proc = subprocess.run(
            [_python_exe(), str(inserter)],
            cwd=str(REPO_ROOT),
            env=trigger_env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        (outdir / f"_trigger_insert_outbox_{i+1}.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
        (outdir / f"_trigger_insert_outbox_{i+1}.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
        if proc.returncode != 0:
            print(f"[labs run {SCENARIO_STUCK_RECLAIM}] failed to insert outbox event #{i+1}: rc={proc.returncode}")
            return 3
        outbox_event_id = (proc.stdout or "").strip().splitlines()[-1].strip()
        outbox_event_ids.append(outbox_event_id)

    (outdir / "_outbox_event_ids.txt").write_text("\n".join(outbox_event_ids) + "\n", encoding="utf-8")
    print(f"[labs run {SCENARIO_STUCK_RECLAIM}] outbox_event_ids: {', '.join(outbox_event_ids)}")

    def _spawn_worker_with_retry(
        *,
        worker_id: str,
        preferred_metrics_port: int,
        log_path: Path,
        max_attempts: int = 4,
        extra_env: dict[str, str] | None = None,
    ) -> tuple[subprocess.Popen, dict[str, str], int, int]:
        candidate_ports: list[int] = []
        for i in range(max_attempts):
            p = int(preferred_metrics_port) + (i * 10_000)
            if 1024 <= p <= 65_000:
                candidate_ports.append(p)
        if not candidate_ports:
            candidate_ports = [19128, 29128, 39128, 49128]

        last_proc: subprocess.Popen | None = None
        last_env: dict[str, str] | None = None
        last_metrics_port = int(preferred_metrics_port)
        last_http_port = int(preferred_metrics_port) + 20

        for attempt, metrics_port in enumerate(candidate_ports, start=1):
            http_port = int(metrics_port) + 20
            env = base_env.copy()
            env["OUTBOX_WORKER_ID"] = str(worker_id)
            env["OUTBOX_METRICS_PORT"] = str(int(metrics_port))
            env["OUTBOX_HTTP_PORT"] = str(int(http_port))
            if extra_env:
                env.update({str(k): str(v) for k, v in extra_env.items()})

            header = f"\n\n# controller: spawn attempt {attempt}/{len(candidate_ports)} metrics_port={metrics_port} http_port={http_port}\n"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write(header)
                log_file.flush()
                proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)

                # Give the process a moment to bind ports & start up.
                time.sleep(0.75)

                if proc.poll() is None:
                    return proc, env, int(metrics_port), int(http_port)

            # Process exited quickly. If it's the known Windows bind issue, try next port.
            try:
                tail = log_path.read_text(encoding="utf-8", errors="replace")[-4000:]
            except Exception:
                tail = ""
            if "WinError 10013" in tail or "PermissionError" in tail:
                last_proc = proc
                last_env = env
                last_metrics_port = int(metrics_port)
                last_http_port = int(http_port)
                continue
            return proc, env, int(metrics_port), int(http_port)

        assert last_proc is not None
        assert last_env is not None
        return last_proc, last_env, int(last_metrics_port), int(last_http_port)

    log_path_1 = logs_dir / f"worker1-{run_id}.log"
    log_path_2 = logs_dir / f"worker2-{run_id}.log"

    before_1_path = metrics_dir / "metrics-before-1.txt"
    before_2_path = metrics_dir / "metrics-before-2.txt"
    after_1_path = metrics_dir / "metrics-after-1.txt"
    after_2_path = metrics_dir / "metrics-after-2.txt"

    print(f"[labs run {SCENARIO_STUCK_RECLAIM}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_STUCK_RECLAIM}] worker1 log: {log_path_1} (metrics :{args.metrics_port_1})")
    print(f"[labs run {SCENARIO_STUCK_RECLAIM}] worker2 log: {log_path_2} (metrics :{args.metrics_port_2})")

    killed_worker1 = False
    observed_claim = False
    worker2_exited_early = False
    worker2_terminated_by_controller = False

    rx_claimed = re.compile(r'"event"\s*:\s*"outbox\\.claim_batch".*?"claimed"\s*:\s*([1-9][0-9]*)')

    # Ensure log files start empty for this run.
    log_path_1.write_text("", encoding="utf-8")
    log_path_2.write_text("", encoding="utf-8")

    # Critical for ExpF: slow worker1 immediately after claim, so controller can
    # kill it before processing completes, leaving rows in `processing` to be
    # reclaimed by worker2.
    worker1_sleep_after_claim_s = max(3.0, float(int(args.lease_seconds)) + 1.0)

    proc1, env1, actual_metrics_port_1, actual_http_port_1 = _spawn_worker_with_retry(
        worker_id=str(args.worker_id_1),
        preferred_metrics_port=int(args.metrics_port_1),
        log_path=log_path_1,
        extra_env={"OUTBOX_EXPERIMENT_PROCESS_SLEEP_SECONDS": str(worker1_sleep_after_claim_s)},
    )
    try:
        time.sleep(max(0.5, float(args.scrape_delay)))
        try:
            before_1_path.write_text(_scrape_metrics_text(port=int(actual_metrics_port_1), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            before_1_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

        # Wait until worker1 claims at least one row, then kill it hard to simulate a crash.
        claim_deadline = time.time() + float(args.claim_timeout)
        while time.time() < claim_deadline:
            if proc1.poll() is not None:
                break
            try:
                text = log_path_1.read_text(encoding="utf-8", errors="replace")
            except Exception:
                text = ""
            if rx_claimed.search(text):
                observed_claim = True
                break
            time.sleep(0.1)

        if proc1.poll() is None:
            killed_worker1 = True
            proc1.kill()
    except KeyboardInterrupt:
        killed_worker1 = True
        try:
            proc1.kill()
        except Exception:
            pass
    finally:
        try:
            proc1.wait(timeout=30)
        except Exception:
            pass

    after_1_path.write_text(
        f"note: worker1 was {'killed' if killed_worker1 else 'not_killed'} by controller\n"
        f"note: observed_claim={observed_claim}\n",
        encoding="utf-8",
    )

    proc2, env2, actual_metrics_port_2, actual_http_port_2 = _spawn_worker_with_retry(
        worker_id=str(args.worker_id_2),
        preferred_metrics_port=int(args.metrics_port_2),
        log_path=log_path_2,
        extra_env={"OUTBOX_EXPERIMENT_PROCESS_SLEEP_SECONDS": "0"},
    )
    try:
        time.sleep(max(0.5, float(args.scrape_delay)))
        try:
            before_2_path.write_text(_scrape_metrics_text(port=int(actual_metrics_port_2), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            before_2_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

        start = time.time()
        while True:
            if args.duration > 0 and (time.time() - start) >= args.duration:
                break
            if proc2.poll() is not None:
                worker2_exited_early = True
                break
            time.sleep(0.25)

        try:
            after_2_path.write_text(_scrape_metrics_text(port=int(actual_metrics_port_2), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            after_2_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

        # Stop worker2 only if it's still running (normal case: we ran it for
        # `--duration`). If it exited on its own, keep its exit code.
        if proc2.poll() is None:
            worker2_terminated_by_controller = True
            proc2.terminate()
    except KeyboardInterrupt:
        try:
            proc2.terminate()
        except Exception:
            pass
    finally:
        try:
            proc2.wait(timeout=30)
        except Exception:
            pass

    exit_info = {
        "worker1": {
            "returncode": int(proc1.returncode) if proc1.returncode is not None else None,
            "killed_by_controller": bool(killed_worker1),
            "observed_claim": bool(observed_claim),
        },
        "worker2": {
            "returncode": int(proc2.returncode) if proc2.returncode is not None else None,
            "exited_early": bool(worker2_exited_early),
            "terminated_by_controller": bool(worker2_terminated_by_controller),
        },
    }
    (outdir / "_worker_exit.json").write_text(json.dumps(exit_info, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    ports_info = {
        "worker1": {"metrics_port": int(actual_metrics_port_1), "http_port": int(actual_http_port_1)},
        "worker2": {"metrics_port": int(actual_metrics_port_2), "http_port": int(actual_http_port_2)},
    }
    (outdir / "_ports.json").write_text(json.dumps(ports_info, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    combined = (
        "# metrics-before-1\n\n" + (before_1_path.read_text(encoding="utf-8", errors="replace") if before_1_path.exists() else "")
        + "\n\n# metrics-before-2\n\n" + (before_2_path.read_text(encoding="utf-8", errors="replace") if before_2_path.exists() else "")
        + "\n\n# metrics-after-2\n\n" + (after_2_path.read_text(encoding="utf-8", errors="replace") if after_2_path.exists() else "")
    )
    (outdir / "_metrics.txt").write_text(combined, encoding="utf-8")

    claim_batch_ids: list[str] = []
    for lp in (log_path_1, log_path_2):
        cid = _extract_last_claim_batch_id(lp)
        if cid:
            claim_batch_ids.append(cid)
    if claim_batch_ids:
        (outdir / "_claim_batch_ids.txt").write_text("\n".join(claim_batch_ids) + "\n", encoding="utf-8")

    # Treat controller-termination as success (Windows returns non-zero for terminate()).
    if worker2_exited_early and (proc2.returncode not in (None, 0)):
        print(f"[labs run {SCENARIO_STUCK_RECLAIM}] worker2 exited early: rc={proc2.returncode}")
        print(f"[labs run {SCENARIO_STUCK_RECLAIM}] see logs: {log_path_2}")
        return 4

    print(f"[labs run {SCENARIO_STUCK_RECLAIM}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_STUCK_RECLAIM}] outputs: {outdir}")
    return 0


def _cmd_labs_verify_stuck_reclaim(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_STUCK_RECLAIM)
    metrics_dir = run_dir / "_metrics"
    logs_dir = run_dir / "_logs"

    before2 = (metrics_dir / "metrics-before-2.txt").read_text(encoding="utf-8") if (metrics_dir / "metrics-before-2.txt").exists() else ""
    after2 = (metrics_dir / "metrics-after-2.txt").read_text(encoding="utf-8") if (metrics_dir / "metrics-after-2.txt").exists() else ""

    metric_processed = "outbox_processed_total"
    metric_failed = "outbox_failed_total"

    metrics_available = (not before2.strip().startswith("scrape_failed")) and (not after2.strip().startswith("scrape_failed"))

    processed_before = _prom_parse_counter_sum(before2, metric_processed) if metrics_available else 0.0
    processed_after = _prom_parse_counter_sum(after2, metric_processed) if metrics_available else 0.0
    failed_before = _prom_parse_counter_sum(before2, metric_failed) if metrics_available else 0.0
    failed_after = _prom_parse_counter_sum(after2, metric_failed) if metrics_available else 0.0

    delta_processed = processed_after - processed_before
    delta_failed = failed_after - failed_before

    # Confirm reclaim happened by log signal.
    reclaimed_count = 0
    reclaim_log_found = False
    worker2_log_path: Path | None = (logs_dir / f"worker2-{args.run_id}.log") if args.run_id else None
    if not (worker2_log_path and worker2_log_path.exists()):
        worker2_logs = sorted([p for p in logs_dir.glob("worker2-*.log") if p.is_file()], key=lambda p: p.name, reverse=True)
        worker2_log_path = worker2_logs[0] if worker2_logs else None

    worker2_text = ""
    if worker2_log_path and worker2_log_path.exists():
        worker2_text = worker2_log_path.read_text(encoding="utf-8", errors="replace")

    m = re.search(r"Reclaimed\s+(\d+)\s+stuck\s+outbox\s+events", worker2_text)
    if m:
        reclaim_log_found = True
        reclaimed_count = int(m.group(1))

    processed_log_count = len(re.findall(r"Outbox\s+(upsert|delete):", worker2_text))

    # Metrics delta can be 0 when worker2 processes everything before the first scrape.
    processed_ok = (
        (metrics_available and (delta_processed >= float(args.min_processed_delta)))
        or (processed_log_count >= 1)
    )
    ok = (
        processed_ok
        and (delta_failed <= float(args.max_failed_delta) if metrics_available else True)
        and (reclaim_log_found and reclaimed_count >= int(args.min_reclaimed))
    )

    result = {
        "scenario": SCENARIO_STUCK_RECLAIM,
        "run_dir": str(run_dir),
        "checks": {
            "processed_delta_ge": float(args.min_processed_delta),
            "failed_delta_le": float(args.max_failed_delta),
            "reclaimed_ge": int(args.min_reclaimed),
        },
        "observed": {
            "metrics_available": bool(metrics_available),
            metric_processed: {"before": processed_before, "after": processed_after, "delta": delta_processed},
            metric_failed: {"before": failed_before, "after": failed_after, "delta": delta_failed},
            "reclaimed": {"count": int(reclaimed_count), "log_found": bool(reclaim_log_found)},
            "processed_log_count": int(processed_log_count),
            "worker2_log": str(worker2_log_path) if worker2_log_path else None,
        },
        "ok": bool(ok),
    }
    (run_dir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if ok:
        print(f"[labs verify {SCENARIO_STUCK_RECLAIM}] OK")
        return 0
    print(f"[labs verify {SCENARIO_STUCK_RECLAIM}] FAILED")
    return 10


def _cmd_labs_export_stuck_reclaim(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_STUCK_RECLAIM)
    exports_dir = run_dir / "_exports"
    _ensure_dir(exports_dir)

    exporter = LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"
    cmd = [
        _python_exe(),
        str(exporter),
        "--outdir",
        str(exports_dir),
        "--service",
        args.service,
        "--lookback",
        args.lookback,
        "--limit",
        str(int(args.limit)),
        "--operation",
        "outbox.claim_batch",
        "--tags-json",
        json.dumps({"wordloom.obs_schema": SEARCH_OUTBOX_OBS_SCHEMA_VERSION}),
    ]
    return int(_run(cmd, cwd=REPO_ROOT, env=_load_env(env_file=None)))


def _cmd_labs_clean_stuck_reclaim(args: argparse.Namespace) -> int:
    if args.keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_STUCK_RECLAIM
        if base.exists():
            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(args.keep_last):]:
                shutil.rmtree(p, ignore_errors=True)
        print(f"[labs clean {SCENARIO_STUCK_RECLAIM}] kept_last={args.keep_last}")
    else:
        print(f"[labs clean {SCENARIO_STUCK_RECLAIM}] noop")
    return 0


def _cmd_labs_clean_es_down_connect(args: argparse.Namespace) -> int:
    # 1) Restore ES
    compose_file = str((REPO_ROOT / "docker-compose.infra.yml").resolve())
    start_proc = _docker_compose(args=["-f", compose_file, "start", "es"], cwd=REPO_ROOT)
    print(f"[labs clean {SCENARIO_ES_DOWN_CONNECT}] start es: rc={start_proc.returncode}")

    if args.outdir:
        outdir = Path(args.outdir)
        _ensure_dir(outdir)
        (outdir / "_clean.txt").write_text(
            f"scenario={SCENARIO_ES_DOWN_CONNECT}\n"
            "action=start_es\n"
            f"at={time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )
        (outdir / "_clean_es_start.stdout.txt").write_text(start_proc.stdout or "", encoding="utf-8")
        (outdir / "_clean_es_start.stderr.txt").write_text(start_proc.stderr or "", encoding="utf-8")
        (outdir / "_clean_es_start.exitcode.txt").write_text(str(int(start_proc.returncode)) + "\n", encoding="utf-8")

    # 2) Optional pruning
    if args.keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_ES_DOWN_CONNECT
        if base.exists():
            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(args.keep_last):]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_ES_DOWN_CONNECT}] kept_last={args.keep_last}")

    return 0


def _cmd_labs_export_es_429_inject(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_ES_429_INJECT)
    exports_dir = run_dir / "_exports"
    _ensure_dir(exports_dir)

    outbox_event_id_path = run_dir / "_outbox_event_id.txt"
    outbox_event_id = outbox_event_id_path.read_text(encoding="utf-8").strip() if outbox_event_id_path.exists() else None

    cmd = [
        _python_exe(),
        str(LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"),
        "--outdir",
        str(exports_dir),
        "--service",
        args.service,
        "--lookback",
        args.lookback,
        "--limit",
        str(args.limit),
    ]
    if outbox_event_id:
        cmd += ["--outbox-event-id", outbox_event_id]

    return _run(cmd, cwd=REPO_ROOT)


def _cmd_labs_clean_es_429_inject(args: argparse.Namespace) -> int:
    # No external state to revert: injection is env-only.
    if args.outdir:
        outdir = Path(args.outdir)
        _ensure_dir(outdir)
        (outdir / "_clean.txt").write_text(
            f"scenario={SCENARIO_ES_429_INJECT}\n"
            "action=noop\n"
            f"at={time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )

    if args.keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_ES_429_INJECT
        if base.exists():
            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(args.keep_last):]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_ES_429_INJECT}] kept_last={args.keep_last}")
    else:
        print(f"[labs clean {SCENARIO_ES_429_INJECT}] noop")
    return 0


def _cmd_labs_clean_es_write_block_4xx(args: argparse.Namespace) -> int:
    # 1) Revert injection (index.blocks.write=false)
    env = _load_env(env_file=args.env_file)
    es_url = (env.get("ELASTIC_URL") or "http://localhost:19200").strip().rstrip("/")
    es_index = (env.get("ELASTIC_INDEX") or "wordloom-search-index").strip()
    status, payload = _es_set_index_write_block(es_url=es_url, index=es_index, enabled=False)
    print(f"[labs clean {SCENARIO_ES_WRITE_BLOCK_4XX}] disable write block: http {status}")
    if args.outdir:
        outdir = Path(args.outdir)
        (outdir / "_clean_es_write_block.response.txt").write_text(
            f"status={status}\n\n{payload}\n", encoding="utf-8"
        )

    # 2) Prune old snapshots (optional)
    if args.keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_ES_WRITE_BLOCK_4XX
        if base.exists():
            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(args.keep_last):]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_ES_WRITE_BLOCK_4XX}] kept_last={args.keep_last}")

    return 0


def _cmd_labs_run_projection_version(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_labs_auto_run_dir(scenario=SCENARIO_PROJECTION_VERSION, run_id=run_id)
    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)

    env = _load_env(env_file=args.env_file)
    env = _with_backend_pythonpath(env)

    # Make the worker bounded and predictable.
    env["OUTBOX_RUN_SECONDS"] = str(int(args.duration))
    env["OUTBOX_POLL_INTERVAL_SECONDS"] = str(float(args.poll_interval))
    env["OUTBOX_BATCH_SIZE"] = str(int(args.batch_size))
    env["OUTBOX_LEASE_SECONDS"] = str(int(args.lease_seconds))
    env["OUTBOX_RECLAIM_INTERVAL_SECONDS"] = str(float(args.reclaim_interval))
    env["OUTBOX_MAX_PROCESSING_SECONDS"] = str(int(args.max_processing_seconds))
    env["LOG_LEVEL"] = "INFO"

    # Ensure the outbox row is processed quickly.
    env.pop("OUTBOX_EXPERIMENT_PROCESS_SLEEP_SECONDS", None)

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_PROJECTION_VERSION,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": args.env_file,
        "service": args.service,
        "phase": {
            "v1": int(args.projection_version_1),
            "v2": int(args.projection_version_2),
        },
        "worker": {
            "duration_s": int(args.duration),
            "preferred_metrics_port": int(args.metrics_port),
            "poll_interval_seconds": float(args.poll_interval),
            "batch_size": int(args.batch_size),
            "lease_seconds": int(args.lease_seconds),
            "reclaim_interval_seconds": float(args.reclaim_interval),
            "max_processing_seconds": int(args.max_processing_seconds),
        },
    }
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    worker = LEGACY_SCRIPTS_DIR / "chronicle_outbox_worker.py"
    cmd = [_python_exe(), "-u", str(worker)]

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_chronicle_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_chronicle_outbox_pending.py"

    prober = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_probe_chronicle_entry.py"
    if not prober.exists():
        prober = LEGACY_SCRIPTS_DIR / "labs_009_probe_chronicle_entry.py"

    def _spawn_worker_with_retry(
        *,
        preferred_metrics_port: int,
        log_path: Path,
        extra_env: dict[str, str] | None = None,
        max_attempts: int = 4,
    ) -> tuple[subprocess.Popen, dict[str, str], int, int]:
        candidate_ports: list[int] = []
        for i in range(max_attempts):
            p = int(preferred_metrics_port) + (i * 10_000)
            if 1024 <= p <= 65_000:
                candidate_ports.append(p)
        if not candidate_ports:
            candidate_ports = [19110, 29110, 39110, 49110]

        last_proc: subprocess.Popen | None = None
        last_env: dict[str, str] | None = None
        last_metrics_port = int(preferred_metrics_port)
        last_http_port = int(preferred_metrics_port) + 2

        for attempt, metrics_port in enumerate(candidate_ports, start=1):
            http_port = int(metrics_port) + 2
            run_env = env.copy()
            run_env["OUTBOX_METRICS_PORT"] = str(int(metrics_port))
            run_env["OUTBOX_HTTP_PORT"] = str(int(http_port))
            if extra_env:
                run_env.update({str(k): str(v) for k, v in extra_env.items()})

            header = f"\n\n# controller: spawn attempt {attempt}/{len(candidate_ports)} metrics_port={metrics_port} http_port={http_port}\n"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write(header)
                log_file.flush()
                proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=run_env, stdout=log_file, stderr=subprocess.STDOUT)
                time.sleep(0.75)
                if proc.poll() is None:
                    return proc, run_env, int(metrics_port), int(http_port)

            try:
                tail = log_path.read_text(encoding="utf-8", errors="replace")[-4000:]
            except Exception:
                tail = ""
            if "WinError 10013" in tail or "PermissionError" in tail:
                last_proc = proc
                last_env = run_env
                last_metrics_port = int(metrics_port)
                last_http_port = int(http_port)
                continue

            return proc, run_env, int(metrics_port), int(http_port)

        assert last_proc is not None
        assert last_env is not None
        return last_proc, last_env, int(last_metrics_port), int(last_http_port)

    def _run_probe(*, chronicle_event_id: str, out_path: Path) -> None:
        probe_env = env.copy()
        probe_env["OUTBOX_CHRONICLE_EVENT_ID"] = chronicle_event_id
        proc = subprocess.run(
            [_python_exe(), str(prober)],
            cwd=str(REPO_ROOT),
            env=probe_env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        out_path.write_text((proc.stdout or "").strip() + "\n", encoding="utf-8")
        if proc.returncode != 0:
            (out_path.parent / (out_path.name + ".stderr.txt")).write_text(proc.stderr or "", encoding="utf-8")

    print(f"[labs run {SCENARIO_PROJECTION_VERSION}] outdir: {outdir}")

    # Phase 1: projection_version=v1
    insert_env = env.copy()
    insert_proc_1 = subprocess.run(
        [_python_exe(), str(inserter)],
        cwd=str(REPO_ROOT),
        env=insert_env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    (outdir / "_trigger_insert_v1.stdout.txt").write_text(insert_proc_1.stdout or "", encoding="utf-8")
    (outdir / "_trigger_insert_v1.stderr.txt").write_text(insert_proc_1.stderr or "", encoding="utf-8")
    if insert_proc_1.returncode != 0:
        print(f"[labs run {SCENARIO_PROJECTION_VERSION}] failed to insert v1 outbox: rc={insert_proc_1.returncode}")
        return 3

    insert_obj_1 = _parse_last_json_line(insert_proc_1.stdout or "") or {}
    chronicle_event_id = str(insert_obj_1.get("chronicle_event_id") or "").strip()
    outbox_event_id_1 = str(insert_obj_1.get("outbox_event_id") or "").strip()
    if not chronicle_event_id or not outbox_event_id_1:
        print(f"[labs run {SCENARIO_PROJECTION_VERSION}] unexpected inserter output; see _trigger_insert_v1.stdout.txt")
        return 3

    (outdir / "_chronicle_event_id.txt").write_text(chronicle_event_id + "\n", encoding="utf-8")
    (outdir / "_outbox_event_id_v1.txt").write_text(outbox_event_id_1 + "\n", encoding="utf-8")

    log_v1 = logs_dir / f"worker-v1-{run_id}.log"
    log_v1.write_text("", encoding="utf-8")
    before_v1 = metrics_dir / "metrics-before-v1.txt"
    after_v1 = metrics_dir / "metrics-after-v1.txt"

    proc1, _env1, actual_metrics_port_1, _http1 = _spawn_worker_with_retry(
        preferred_metrics_port=int(args.metrics_port),
        log_path=log_v1,
        extra_env={"CHRONICLE_PROJECTION_VERSION": str(int(args.projection_version_1))},
    )
    try:
        time.sleep(max(0.5, float(args.scrape_delay)))
        try:
            before_v1.write_text(_scrape_metrics_text(port=int(actual_metrics_port_1), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            before_v1.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

        proc1.wait(timeout=max(10, int(args.duration) + 20))
    except Exception:
        try:
            proc1.terminate()
        except Exception:
            pass
        try:
            proc1.wait(timeout=30)
        except Exception:
            pass
    finally:
        try:
            after_v1.write_text(_scrape_metrics_text(port=int(actual_metrics_port_1), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            after_v1.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

    _run_probe(chronicle_event_id=chronicle_event_id, out_path=(outdir / "_probe_entry_v1.json"))

    # Phase 2: enqueue same event again, run with projection_version=v2
    insert_env_2 = env.copy()
    insert_env_2["OUTBOX_CHRONICLE_EVENT_ID"] = chronicle_event_id
    insert_proc_2 = subprocess.run(
        [_python_exe(), str(inserter)],
        cwd=str(REPO_ROOT),
        env=insert_env_2,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    (outdir / "_trigger_insert_v2.stdout.txt").write_text(insert_proc_2.stdout or "", encoding="utf-8")
    (outdir / "_trigger_insert_v2.stderr.txt").write_text(insert_proc_2.stderr or "", encoding="utf-8")
    if insert_proc_2.returncode != 0:
        print(f"[labs run {SCENARIO_PROJECTION_VERSION}] failed to insert v2 outbox: rc={insert_proc_2.returncode}")
        return 3

    insert_obj_2 = _parse_last_json_line(insert_proc_2.stdout or "") or {}
    outbox_event_id_2 = str(insert_obj_2.get("outbox_event_id") or "").strip()
    if not outbox_event_id_2:
        print(f"[labs run {SCENARIO_PROJECTION_VERSION}] unexpected v2 inserter output; see _trigger_insert_v2.stdout.txt")
        return 3
    (outdir / "_outbox_event_id_v2.txt").write_text(outbox_event_id_2 + "\n", encoding="utf-8")

    log_v2 = logs_dir / f"worker-v2-{run_id}.log"
    log_v2.write_text("", encoding="utf-8")
    before_v2 = metrics_dir / "metrics-before-v2.txt"
    after_v2 = metrics_dir / "metrics-after-v2.txt"

    proc2, _env2, actual_metrics_port_2, _http2 = _spawn_worker_with_retry(
        preferred_metrics_port=int(args.metrics_port) + 1,
        log_path=log_v2,
        extra_env={"CHRONICLE_PROJECTION_VERSION": str(int(args.projection_version_2))},
    )
    try:
        time.sleep(max(0.5, float(args.scrape_delay)))
        try:
            before_v2.write_text(_scrape_metrics_text(port=int(actual_metrics_port_2), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            before_v2.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

        proc2.wait(timeout=max(10, int(args.duration) + 20))
    except Exception:
        try:
            proc2.terminate()
        except Exception:
            pass
        try:
            proc2.wait(timeout=30)
        except Exception:
            pass
    finally:
        try:
            after_v2.write_text(_scrape_metrics_text(port=int(actual_metrics_port_2), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            after_v2.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

    _run_probe(chronicle_event_id=chronicle_event_id, out_path=(outdir / "_probe_entry_v2.json"))

    result = {
        "scenario": SCENARIO_PROJECTION_VERSION,
        "run_id": run_id,
        "chronicle_event_id": chronicle_event_id,
        "outbox_event_ids": {"v1": outbox_event_id_1, "v2": outbox_event_id_2},
        "worker_logs": {
            "v1": str(log_v1.relative_to(REPO_ROOT)),
            "v2": str(log_v2.relative_to(REPO_ROOT)),
        },
        "probe": {
            "v1": _read_json_file(outdir / "_probe_entry_v1.json"),
            "v2": _read_json_file(outdir / "_probe_entry_v2.json"),
        },
    }
    # Keep verify output standardized as `_result.json`. Run output is `_run.json`.
    (outdir / "_run.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"[labs run {SCENARIO_PROJECTION_VERSION}] chronicle_event_id: {chronicle_event_id}")
    print(f"[labs run {SCENARIO_PROJECTION_VERSION}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_PROJECTION_VERSION}] outputs: {outdir}")
    return 0


def _cmd_labs_verify_projection_version(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_PROJECTION_VERSION)
    if not run_dir.exists():
        print(f"[labs verify {SCENARIO_PROJECTION_VERSION}] run_dir not found: {run_dir}")
        return 2

    probe1 = _read_json_file(run_dir / "_probe_entry_v1.json") or {}
    probe2 = _read_json_file(run_dir / "_probe_entry_v2.json") or {}

    want1 = int(args.projection_version_1)
    want2 = int(args.projection_version_2)
    got1 = probe1.get("projection_version")
    got2 = probe2.get("projection_version")

    ok = True
    errors: list[str] = []
    if got1 != want1:
        ok = False
        errors.append(f"probe v1 projection_version mismatch: got={got1!r} want={want1}")
    if got2 != want2:
        ok = False
        errors.append(f"probe v2 projection_version mismatch: got={got2!r} want={want2}")

    checks = [
        {
            "name": "probe v1 projection_version match",
            "expected": want1,
            "observed": got1,
            "ok": bool(got1 == want1),
        },
        {
            "name": "probe v2 projection_version match",
            "expected": want2,
            "observed": got2,
            "ok": bool(got2 == want2),
        },
    ]

    why = "ok" if ok else (errors[0] if errors else "verify failed")

    result = {
        "scenario": SCENARIO_PROJECTION_VERSION,
        "run_id": run_dir.name,
        "ok": bool(ok),
        "why": why,
        "checks": checks,
        "expected": {"v1": want1, "v2": want2},
        "observed": {"v1": got1, "v2": got2},
        "errors": errors,
    }

    # Standard contract: verify writes `_result.json`.
    (run_dir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # Back-compat: keep the previous file name too.
    (run_dir / "_verify_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if ok:
        print(f"[labs verify {SCENARIO_PROJECTION_VERSION}] OK")
        return 0

    print(f"[labs verify {SCENARIO_PROJECTION_VERSION}] FAILED")
    for e in errors:
        print("  -", e)
    return 2


def _cmd_labs_export_projection_version(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(run_id=args.run_id, outdir=args.outdir, scenario=SCENARIO_PROJECTION_VERSION)
    if not run_dir.exists():
        print(f"[labs export {SCENARIO_PROJECTION_VERSION}] run_dir not found: {run_dir}")
        return 2

    event_id_path = run_dir / "_chronicle_event_id.txt"
    if not event_id_path.exists():
        print(f"[labs export {SCENARIO_PROJECTION_VERSION}] missing: {event_id_path}")
        return 2
    chronicle_event_id = (event_id_path.read_text(encoding="utf-8", errors="replace") or "").strip()
    if not chronicle_event_id:
        print(f"[labs export {SCENARIO_PROJECTION_VERSION}] empty chronicle_event_id")
        return 2

    exports_dir = run_dir / "_exports"
    _ensure_dir(exports_dir)

    script = LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"
    cmd = [
        _python_exe(),
        str(script),
        "--outdir",
        str(exports_dir),
        "--service",
        args.service,
        "--lookback",
        args.lookback,
        "--limit",
        str(int(args.limit)),
        "--operation",
        "outbox.process",
        "--tags-json",
        json.dumps({"wordloom.entity.id": chronicle_event_id}, ensure_ascii=False),
    ]
    return _run(cmd, cwd=REPO_ROOT)


def _cmd_labs_clean_projection_version(args: argparse.Namespace) -> int:
    if args.keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_PROJECTION_VERSION
        if base.exists():
            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(args.keep_last):]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_PROJECTION_VERSION}] kept_last={args.keep_last}")
    else:
        print(f"[labs clean {SCENARIO_PROJECTION_VERSION}] noop")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="scripts", description="backend/scripts router")
    sub = p.add_subparsers(dest="cmd", required=True)

    labs = sub.add_parser("labs", help="Lab/experiment commands")
    labs_sub = labs.add_subparsers(dest="labs_cmd", required=True)

    exp = labs_sub.add_parser("export-jaeger", help="Export Jaeger snapshots (wraps v1 script)")
    exp.add_argument("--service", required=True)
    exp.add_argument("--lookback", default="24h")
    exp.add_argument("--limit", type=int, default=20)
    exp.add_argument("--operation")
    exp.add_argument("--outbox-event-id")
    exp.add_argument("--claim-batch-id")
    exp.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    exp.set_defaults(func=_cmd_labs_export_jaeger)

    sv = labs_sub.add_parser(
        "shadow-verify-chronicle-entries",
        help="Labs-010: shadow verify chronicle_entries vs chronicle_events (writes _result.json)",
    )
    sv.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv.add_argument("--book-id", help="Optional book_id scope (UUID)")
    sv.add_argument("--run-id", help="Optional run_id folder name")
    sv.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv.set_defaults(func=_cmd_labs_shadow_verify_chronicle_entries)

    sv_search = labs_sub.add_parser(
        "shadow-verify-search-index",
        help="Labs-011: shadow verify search_index vs source tables (writes _result.json)",
    )
    sv_search.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_search.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_search.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_search.add_argument("--run-id", help="Optional run_id folder name")
    sv_search.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_search.set_defaults(func=_cmd_labs_shadow_verify_search_index)

    sv_search_gate = labs_sub.add_parser(
        "shadow-verify-search-index-write-gate",
        help="Labs-012: write-gate verify search_index uniqueness (writes _result.json)",
    )
    sv_search_gate.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_search_gate.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_search_gate.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_search_gate.add_argument("--run-id", help="Optional run_id folder name")
    sv_search_gate.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_search_gate.set_defaults(func=_cmd_labs_shadow_verify_search_index_write_gate)

    sv_search_paging = labs_sub.add_parser(
        "shadow-verify-search-index-paging-stability",
        help="Labs-013: verify stable keyset paging over search_index (writes _result.json)",
    )
    sv_search_paging.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_search_paging.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_search_paging.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_search_paging.add_argument("--page-size", type=int, default=50)
    sv_search_paging.add_argument("--pages-checked", type=int, default=2)
    sv_search_paging.add_argument(
        "--ensure-min-rows",
        type=int,
        default=0,
        help="Optional: seed search_index rows in devtest DB to make paging checks meaningful",
    )
    sv_search_paging.add_argument("--run-id", help="Optional run_id folder name")
    sv_search_paging.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_search_paging.set_defaults(func=_cmd_labs_shadow_verify_search_index_paging_stability)

    sv_keys = labs_sub.add_parser(
        "shadow-verify-shared-keys",
        help="Labs-014: emit shared-key evidence bundle (writes _result.json)",
    )
    sv_keys.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_keys.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_keys.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_keys.add_argument(
        "--ensure-min-rows",
        type=int,
        default=0,
        help="Optional: seed search_index rows in devtest DB to ensure sample keys exist",
    )
    sv_keys.add_argument("--run-id", help="Optional run_id folder name")
    sv_keys.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_keys.set_defaults(func=_cmd_labs_shadow_verify_shared_keys)

    sv_ready = labs_sub.add_parser(
        "shadow-verify-dual-run-readiness-gate",
        help="Labs-015: dry-run readiness gate (aggregates 1A+2A prerequisites; writes _result.json)",
    )
    sv_ready.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_ready.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_ready.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_ready.add_argument("--page-size", type=int, default=50)
    sv_ready.add_argument("--pages-checked", type=int, default=2)
    sv_ready.add_argument("--ensure-min-rows-paging", type=int, default=120)
    sv_ready.add_argument("--ensure-min-rows-keys", type=int, default=5)
    sv_ready.add_argument("--run-id", help="Optional run_id folder name")
    sv_ready.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_ready.set_defaults(func=_cmd_labs_shadow_verify_dual_run_readiness_gate)

    sv_dualrun = labs_sub.add_parser(
        "shadow-verify-dual-run-stage1",
        help="Labs-018: true dual-run parity (Postgres vs Elasticsearch; writes _result.json)",
    )
    sv_dualrun.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_dualrun.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_dualrun.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_dualrun.add_argument(
        "--ensure-min-rows",
        type=int,
        default=25,
        help="Optional: seed search_index rows (entity_type=block) so Postgres+ES queries have candidates",
    )
    sv_dualrun.add_argument("--candidate-limit", type=int, default=20)
    sv_dualrun.add_argument("--strategy", choices=["soft", "strict"], default="strict")
    sv_dualrun.add_argument("--es-url", help="Override ELASTIC_URL (default: env or http://127.0.0.1:19200)")
    sv_dualrun.add_argument("--es-index", help="Override ELASTIC_INDEX (default: drill-scoped)")
    sv_dualrun.add_argument("--recreate-index", action=argparse.BooleanOptionalAction, default=True)
    sv_dualrun.add_argument("--backfill-batch-size", type=int, default=200)
    sv_dualrun.add_argument("--token", help="Optional: override the deterministic query token")
    sv_dualrun.add_argument("--run-id", help="Optional run_id folder name")
    sv_dualrun.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_dualrun.set_defaults(func=_cmd_labs_shadow_verify_dual_run_stage1)

    sv_dualrun2 = labs_sub.add_parser(
        "shadow-verify-dual-run-stage2",
        help="Labs-019: true dual-run (outbox worker to ES) + parity verify (writes _result.json)",
    )
    sv_dualrun2.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_dualrun2.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_dualrun2.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_dualrun2.add_argument(
        "--ensure-min-rows",
        type=int,
        default=25,
        help="Optional: seed search_index rows (entity_type=block) so outbox+ES queries have candidates",
    )
    sv_dualrun2.add_argument("--candidate-limit", type=int, default=20)
    sv_dualrun2.add_argument("--strategy", choices=["soft", "strict"], default="strict")
    sv_dualrun2.add_argument("--es-url", help="Override ELASTIC_URL (default: env or http://127.0.0.1:19200)")
    sv_dualrun2.add_argument("--es-index", help="Override ELASTIC_INDEX (default: drill-scoped)")
    sv_dualrun2.add_argument("--recreate-index", action=argparse.BooleanOptionalAction, default=True)
    sv_dualrun2.add_argument("--worker-batch-size", type=int, default=100)
    sv_dualrun2.add_argument("--worker-concurrency", type=int, default=1)
    sv_dualrun2.add_argument("--worker-poll-interval-seconds", type=float, default=0.2)
    sv_dualrun2.add_argument("--worker-idle-polls-before-exit", type=int, default=2)
    sv_dualrun2.add_argument("--worker-max-runtime-seconds", type=float, default=60.0)
    sv_dualrun2.add_argument("--token", help="Optional: override the deterministic query token")
    sv_dualrun2.add_argument("--run-id", help="Optional run_id folder name")
    sv_dualrun2.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_dualrun2.set_defaults(func=_cmd_labs_shadow_verify_dual_run_stage2)

    sv_dualrun_window = labs_sub.add_parser(
        "shadow-verify-dual-run-window",
        help="Labs-020: sustained dual-run window (worker runs while enqueueing) + parity verify (writes _result.json)",
    )
    sv_dualrun_window.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_dualrun_window.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_dualrun_window.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_dualrun_window.add_argument(
        "--ensure-min-rows",
        type=int,
        default=25,
        help="Optional: seed search_index rows (entity_type=block) so outbox+ES queries have candidates",
    )
    sv_dualrun_window.add_argument("--candidate-limit", type=int, default=20)
    sv_dualrun_window.add_argument("--strategy", choices=["soft", "strict"], default="strict")
    sv_dualrun_window.add_argument("--duration-seconds", type=float, default=30.0)
    sv_dualrun_window.add_argument("--interval-seconds", type=float, default=1.0)
    sv_dualrun_window.add_argument("--enqueue-batch-size", type=int, default=20)
    sv_dualrun_window.add_argument("--max-total-events", type=int, default=200)
    sv_dualrun_window.add_argument("--drain-timeout-seconds", type=float, default=20.0)
    sv_dualrun_window.add_argument(
        "--max-outbox-failed",
        type=int,
        default=0,
        help="Hard gate: maximum allowed failed outbox events for the inserted ids (default: 0)",
    )
    sv_dualrun_window.add_argument(
        "--max-outbox-pending",
        type=int,
        default=0,
        help="Hard gate: maximum allowed pending outbox events at the end of the drain (default: 0)",
    )
    sv_dualrun_window.add_argument(
        "--max-outbox-processing",
        type=int,
        default=0,
        help="Hard gate: maximum allowed processing outbox events at the end of the drain (default: 0)",
    )
    sv_dualrun_window.add_argument(
        "--require-outbox-done-eq-enqueued",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Hard gate: require outbox done == enqueued_total for the inserted ids (default: true)",
    )
    sv_dualrun_window.add_argument("--es-url", help="Override ELASTIC_URL (default: env or http://127.0.0.1:19200)")
    sv_dualrun_window.add_argument("--es-index", help="Override ELASTIC_INDEX (default: drill-scoped)")
    sv_dualrun_window.add_argument("--recreate-index", action=argparse.BooleanOptionalAction, default=True)
    sv_dualrun_window.add_argument("--worker-batch-size", type=int, default=100)
    sv_dualrun_window.add_argument("--worker-concurrency", type=int, default=1)
    sv_dualrun_window.add_argument("--worker-poll-interval-seconds", type=float, default=0.2)
    sv_dualrun_window.add_argument("--worker-max-runtime-seconds", type=float, default=120.0)
    sv_dualrun_window.add_argument("--token", help="Optional: override the deterministic query token")
    sv_dualrun_window.add_argument("--run-id", help="Optional run_id folder name")
    sv_dualrun_window.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_dualrun_window.set_defaults(func=_cmd_labs_shadow_verify_dual_run_window)

    sv_canary = labs_sub.add_parser(
        "shadow-verify-canary-dual-write",
        help="Labs-016: canary dual-write (projection + outbox) with rollback/cleanup (writes _result.json)",
    )
    sv_canary.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_canary.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_canary.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_canary.add_argument("--max-writes", type=int, default=5)
    sv_canary.add_argument(
        "--cleanup",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="When enabled, deletes the canary rows (rollback) after verification",
    )
    sv_canary.add_argument("--run-id", help="Optional run_id folder name")
    sv_canary.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_canary.set_defaults(func=_cmd_labs_shadow_verify_canary_dual_write)

    sv_sampling = labs_sub.add_parser(
        "shadow-verify-dual-write-sampling",
        help="Labs-017: allowlist/sampling sustained dual-write (outbox enqueue) + DLQ/replay evidence (writes _result.json)",
    )
    sv_sampling.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_sampling.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_sampling.add_argument("--library-id", help="Optional library_id allowlist scope (UUID)")
    sv_sampling.add_argument(
        "--entity-types",
        default="",
        help="Optional allowlist for search_index.entity_type (comma-separated); empty means all",
    )
    sv_sampling.add_argument(
        "--ensure-min-rows",
        type=int,
        default=0,
        help="Optional: seed search_index rows in devtest DB so sampling has candidates",
    )
    sv_sampling.add_argument("--sample-size", type=int, default=20)
    sv_sampling.add_argument("--duration-seconds", type=int, default=0, help="0 means single batch")
    sv_sampling.add_argument("--interval-seconds", type=float, default=1.0)
    sv_sampling.add_argument("--max-total-events", type=int, default=100)
    sv_sampling.add_argument("--strategy", choices=["soft", "strict"], default="strict")
    sv_sampling.add_argument(
        "--inject-failed-rate",
        type=float,
        default=0.0,
        help="Simulate new-side failure: fraction of inserted rows to mark failed (DLQ)",
    )
    sv_sampling.add_argument(
        "--replay-failed",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="When enabled, replays simulated failed rows back to pending with audit fields",
    )
    sv_sampling.add_argument("--replay-by", default="labs", help="Replay audit: operator identifier")
    sv_sampling.add_argument("--replay-reason", default="labs drill", help="Replay audit: reason")
    sv_sampling.add_argument(
        "--cleanup",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="When enabled, deletes inserted outbox rows after verification",
    )
    sv_sampling.add_argument("--run-id", help="Optional run_id folder name")
    sv_sampling.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_sampling.set_defaults(func=_cmd_labs_shadow_verify_dual_write_sampling)

    b = labs_sub.add_parser("expb-es429", help="Run Labs-009 ExpB (ES 429 injection) bounded")
    b.add_argument("--service", default="wordloom-search-outbox-worker")
    b.add_argument("--lookback", default="24h")
    b.add_argument("--limit", type=int, default=20)
    b.add_argument("--duration", type=int, default=30, help="Seconds to run worker; 0 means run until it exits")
    b.add_argument("--run-id", help="Optional run_id folder name")
    b.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")

    b.add_argument("--every-n", type=int, default=2)
    b.add_argument("--ratio", type=float)
    b.add_argument("--seed", type=int, default=1)
    b.add_argument("--ops", default="delete", help="Comma-separated ops, e.g. upsert,delete")
    b.add_argument("--metrics-port", type=int)

    b.set_defaults(func=_cmd_labs_expb_es429)

    run = labs_sub.add_parser("run", help="Run a lab scenario (auto snapshot outputs)")
    run_sub = run.add_subparsers(dest="scenario", required=True)

    c_run = run_sub.add_parser(SCENARIO_ES_WRITE_BLOCK_4XX, help="ExpC: ES index write-block -> deterministic 4xx")
    c_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    c_run.add_argument("--service", default="wordloom-search-outbox-worker")
    c_run.add_argument("--duration", type=int, default=20)
    c_run.add_argument("--metrics-port", type=int, default=9109)
    c_run.add_argument("--scrape-delay", type=float, default=2.0)
    c_run.add_argument("--run-id")
    c_run.add_argument("--outdir")
    c_run.set_defaults(func=_cmd_labs_run_es_write_block_4xx)

    b_run = run_sub.add_parser(SCENARIO_ES_429_INJECT, help="ExpB: deterministic ES 429 injection (retry/backoff)")
    b_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    b_run.add_argument("--service", default="wordloom-search-outbox-worker")
    b_run.add_argument("--duration", type=int, default=20)
    b_run.add_argument("--metrics-port", type=int, default=9109)
    b_run.add_argument("--scrape-delay", type=float, default=2.0)
    b_run.add_argument("--run-id")
    b_run.add_argument("--outdir")
    b_run.add_argument("--op", default="upsert", choices=["upsert", "delete"], help="Outbox op to trigger")
    b_run.add_argument("--every-n", type=int, default=1, help="Inject 1 out of N operations deterministically")
    b_run.add_argument("--ratio", type=float, default=0.0, help="Probabilistic injection ratio (used when every-n<=0)")
    b_run.add_argument("--ops", default="upsert", help="Comma-separated ops to apply injection to")
    b_run.add_argument("--seed", type=int, default=1)
    b_run.set_defaults(func=_cmd_labs_run_es_429_inject)

    a_run = run_sub.add_parser(SCENARIO_ES_DOWN_CONNECT, help="ExpA: stop ES -> connect failure -> retry/backoff")
    a_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    a_run.add_argument("--service", default="wordloom-search-outbox-worker")
    a_run.add_argument("--duration", type=int, default=20)
    a_run.add_argument("--metrics-port", type=int, default=9109)
    a_run.add_argument("--scrape-delay", type=float, default=2.0)
    a_run.add_argument("--run-id")
    a_run.add_argument("--outdir")
    a_run.add_argument("--op", default="delete", choices=["upsert", "delete"], help="Outbox op to trigger")
    a_run.set_defaults(func=_cmd_labs_run_es_down_connect)

    cd_run = run_sub.add_parser(SCENARIO_COLLECTOR_DOWN, help="P1: stop Jaeger collector/query while worker runs")
    cd_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    cd_run.add_argument("--service", default="wordloom-search-outbox-worker")
    cd_run.add_argument("--duration", type=int, default=20)
    cd_run.add_argument("--metrics-port", type=int, default=9109)
    cd_run.add_argument("--scrape-delay", type=float, default=2.0)
    cd_run.add_argument("--run-id")
    cd_run.add_argument("--outdir")
    cd_run.add_argument("--op", default="upsert", choices=["upsert", "delete"], help="Outbox op to trigger")
    cd_run.set_defaults(func=_cmd_labs_run_collector_down)

    d_run = run_sub.add_parser(SCENARIO_ES_BULK_PARTIAL, help="ExpD: ES bulk partial success (mixed item outcomes)")
    d_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    d_run.add_argument("--service", default="wordloom-search-outbox-worker")
    d_run.add_argument("--duration", type=int, default=20)
    d_run.add_argument("--metrics-port", type=int, default=9109)
    d_run.add_argument("--scrape-delay", type=float, default=2.0)
    d_run.add_argument("--run-id")
    d_run.add_argument("--outdir")
    d_run.add_argument("--op", default="upsert", choices=["upsert", "delete"], help="Outbox op to trigger")
    d_run.add_argument("--trigger-count", type=int, default=2, help="How many outbox events to insert")
    d_run.add_argument("--bulk-size", type=int, default=10, help="OUTBOX_BULK_SIZE for the worker")
    d_run.add_argument("--partial-status", type=int, default=400, help="Injected bulk-item status code")
    d_run.set_defaults(func=_cmd_labs_run_es_bulk_partial)

    e_run = run_sub.add_parser(SCENARIO_DB_CLAIM_CONTENTION, help="ExpE: DB claim contention (two workers, non-atomic claim)")
    e_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    e_run.add_argument("--service", default="wordloom-search-outbox-worker")
    e_run.add_argument("--duration", type=int, default=25)
    e_run.add_argument("--metrics-port-1", dest="metrics_port_1", type=int, default=9126)
    e_run.add_argument("--metrics-port-2", dest="metrics_port_2", type=int, default=9127)
    e_run.add_argument("--worker-id-1", dest="worker_id_1", default="labs-expE-w1")
    e_run.add_argument("--worker-id-2", dest="worker_id_2", default="labs-expE-w2")
    e_run.add_argument("--scrape-delay", type=float, default=2.0)
    e_run.add_argument("--run-id")
    e_run.add_argument("--outdir")
    e_run.add_argument("--op", default="upsert", choices=["upsert", "delete"], help="Outbox op to trigger")
    e_run.add_argument("--trigger-count", type=int, default=1, help="How many outbox events to insert")
    e_run.add_argument("--break-claim-sleep", type=float, default=1.0, help="Delay between SELECT and UPDATE in non-atomic claim")
    e_run.add_argument("--poll-interval", type=float, default=0.05)
    e_run.add_argument("--batch-size", type=int, default=50)
    e_run.set_defaults(func=_cmd_labs_run_db_claim_contention)

    f_run = run_sub.add_parser(SCENARIO_STUCK_RECLAIM, help="ExpF: stuck & reclaim (kill worker1 mid-lease; worker2 reclaims)")
    f_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    f_run.add_argument("--service", default="wordloom-search-outbox-worker")
    f_run.add_argument("--duration", type=int, default=20, help="How long to keep worker2 running")
    f_run.add_argument("--metrics-port-1", dest="metrics_port_1", type=int, default=19128)
    f_run.add_argument("--metrics-port-2", dest="metrics_port_2", type=int, default=19129)
    f_run.add_argument("--worker-id-1", dest="worker_id_1", default="labs-expF-w1")
    f_run.add_argument("--worker-id-2", dest="worker_id_2", default="labs-expF-w2")
    f_run.add_argument("--scrape-delay", type=float, default=2.0)
    f_run.add_argument("--run-id")
    f_run.add_argument("--outdir")
    f_run.add_argument("--op", default="upsert", choices=["upsert", "delete"], help="Outbox op to trigger")
    f_run.add_argument("--trigger-count", type=int, default=5, help="How many outbox events to insert")
    f_run.add_argument("--lease-seconds", dest="lease_seconds", type=int, default=3)
    f_run.add_argument("--reclaim-interval", dest="reclaim_interval", type=float, default=1.0)
    f_run.add_argument("--max-processing-seconds", dest="max_processing_seconds", type=int, default=60)
    f_run.add_argument("--poll-interval", dest="poll_interval", type=float, default=0.1)
    f_run.add_argument("--batch-size", dest="batch_size", type=int, default=50)
    f_run.add_argument("--claim-timeout", dest="claim_timeout", type=float, default=8.0)
    f_run.set_defaults(func=_cmd_labs_run_stuck_reclaim)

    g_run = run_sub.add_parser(SCENARIO_DUPLICATE_DELIVERY, help="ExpG: duplicate delivery / idempotent noop (delete 404)")
    g_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    g_run.add_argument("--service", default="wordloom-search-outbox-worker")
    g_run.add_argument("--duration", type=int, default=20)
    g_run.add_argument("--metrics-port", type=int, default=19130)
    g_run.add_argument("--scrape-delay", type=float, default=2.0)
    g_run.add_argument("--run-id")
    g_run.add_argument("--outdir")
    g_run.add_argument("--entity-type", dest="entity_type", default="book")
    g_run.add_argument("--entity-id", dest="entity_id", help="Optional explicit entity_id (UUID or string)")
    g_run.add_argument("--delete-count", dest="delete_count", type=int, default=2)
    g_run.set_defaults(func=_cmd_labs_run_duplicate_delivery)

    h_run = run_sub.add_parser(SCENARIO_PROJECTION_VERSION, help="ExpH: projection_version (chronicle projector v1/v2)")
    h_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    h_run.add_argument("--service", default="wordloom-chronicle-outbox-worker")
    h_run.add_argument("--duration", type=int, default=8)
    h_run.add_argument("--metrics-port", type=int, default=19110)
    h_run.add_argument("--scrape-delay", type=float, default=1.5)
    h_run.add_argument("--run-id")
    h_run.add_argument("--outdir")
    h_run.add_argument("--projection-version-1", dest="projection_version_1", type=int, default=1)
    h_run.add_argument("--projection-version-2", dest="projection_version_2", type=int, default=2)
    h_run.add_argument("--poll-interval", type=float, default=0.2)
    h_run.add_argument("--batch-size", type=int, default=50)
    h_run.add_argument("--lease-seconds", dest="lease_seconds", type=int, default=10)
    h_run.add_argument("--reclaim-interval", dest="reclaim_interval", type=float, default=2.0)
    h_run.add_argument("--max-processing-seconds", dest="max_processing_seconds", type=int, default=60)
    h_run.set_defaults(func=_cmd_labs_run_projection_version)

    verify = labs_sub.add_parser("verify", help="Verify a scenario run using captured evidence")
    verify_sub = verify.add_subparsers(dest="scenario", required=True)

    c_verify = verify_sub.add_parser(SCENARIO_ES_WRITE_BLOCK_4XX, help="Verify ExpC run")
    c_verify.add_argument("--run-id")
    c_verify.add_argument("--outdir")
    c_verify.add_argument("--min-failed-delta", type=float, default=1.0)
    c_verify.add_argument("--max-retry-delta", type=float, default=0.0)
    c_verify.set_defaults(func=_cmd_labs_verify_es_write_block_4xx)

    b_verify = verify_sub.add_parser(SCENARIO_ES_429_INJECT, help="Verify ExpB run")
    b_verify.add_argument("--run-id")
    b_verify.add_argument("--outdir")
    b_verify.add_argument("--min-retry-delta", type=float, default=1.0)
    b_verify.add_argument("--min-failed-delta", type=float, default=1.0)
    b_verify.add_argument("--max-terminal-delta", type=float, default=0.0)
    b_verify.set_defaults(func=_cmd_labs_verify_es_429_inject)

    a_verify = verify_sub.add_parser(SCENARIO_ES_DOWN_CONNECT, help="Verify ExpA run")
    a_verify.add_argument("--run-id")
    a_verify.add_argument("--outdir")
    a_verify.add_argument("--min-retry-delta", type=float, default=1.0)
    a_verify.add_argument("--min-failed-delta", type=float, default=1.0)
    a_verify.add_argument("--max-terminal-delta", type=float, default=0.0)
    a_verify.set_defaults(func=_cmd_labs_verify_es_down_connect)

    cd_verify = verify_sub.add_parser(SCENARIO_COLLECTOR_DOWN, help="Verify P1 collector_down run")
    cd_verify.add_argument("--run-id")
    cd_verify.add_argument("--outdir")
    cd_verify.add_argument("--min-processed-delta", type=float, default=1.0)
    cd_verify.add_argument("--max-failed-delta", type=float, default=0.0)
    cd_verify.set_defaults(func=_cmd_labs_verify_collector_down)

    d_verify = verify_sub.add_parser(SCENARIO_ES_BULK_PARTIAL, help="Verify ExpD run")
    d_verify.add_argument("--run-id")
    d_verify.add_argument("--outdir")
    d_verify.add_argument("--min-partial-delta", type=float, default=1.0)
    d_verify.add_argument("--min-success-items-delta", type=float, default=1.0)
    d_verify.add_argument("--min-failed-items-delta", type=float, default=1.0)
    d_verify.add_argument("--min-failed-4xx-delta", type=float, default=1.0)
    d_verify.set_defaults(func=_cmd_labs_verify_es_bulk_partial)

    e_verify = verify_sub.add_parser(SCENARIO_DB_CLAIM_CONTENTION, help="Verify ExpE run")
    e_verify.add_argument("--run-id")
    e_verify.add_argument("--outdir")
    e_verify.add_argument("--min-owner-mismatch-delta", type=float, default=1.0)
    e_verify.add_argument("--min-processed-delta", type=float, default=1.0)
    e_verify.add_argument("--max-failed-delta", type=float, default=0.0)
    e_verify.set_defaults(func=_cmd_labs_verify_db_claim_contention)

    f_verify = verify_sub.add_parser(SCENARIO_STUCK_RECLAIM, help="Verify ExpF run")
    f_verify.add_argument("--run-id")
    f_verify.add_argument("--outdir")
    f_verify.add_argument("--min-processed-delta", type=float, default=1.0)
    f_verify.add_argument("--max-failed-delta", type=float, default=0.0)
    f_verify.add_argument("--min-reclaimed", type=int, default=1)
    f_verify.set_defaults(func=_cmd_labs_verify_stuck_reclaim)

    g_verify = verify_sub.add_parser(SCENARIO_DUPLICATE_DELIVERY, help="Verify ExpG run")
    g_verify.add_argument("--run-id")
    g_verify.add_argument("--outdir")
    g_verify.add_argument("--min-processed-delta", type=float, default=3.0)
    g_verify.add_argument("--max-failed-delta", type=float, default=0.0)
    g_verify.add_argument("--min-noop-delta", type=float, default=1.0)
    g_verify.add_argument("--min-noop-logs", type=int, default=1)
    g_verify.set_defaults(func=_cmd_labs_verify_duplicate_delivery)

    h_verify = verify_sub.add_parser(SCENARIO_PROJECTION_VERSION, help="Verify ExpH run")
    h_verify.add_argument("--run-id")
    h_verify.add_argument("--outdir")
    h_verify.add_argument("--projection-version-1", dest="projection_version_1", type=int, default=1)
    h_verify.add_argument("--projection-version-2", dest="projection_version_2", type=int, default=2)
    h_verify.set_defaults(func=_cmd_labs_verify_projection_version)

    export = labs_sub.add_parser("export", help="Export additional evidence (e.g. Jaeger) for a run")
    export_sub = export.add_subparsers(dest="scenario", required=True)

    c_export = export_sub.add_parser(SCENARIO_ES_WRITE_BLOCK_4XX, help="Export Jaeger traces for ExpC run")
    c_export.add_argument("--run-id")
    c_export.add_argument("--outdir")
    c_export.add_argument("--service", default="wordloom-search-outbox-worker")
    c_export.add_argument("--lookback", default="1h")
    c_export.add_argument("--limit", type=int, default=20)
    c_export.set_defaults(func=_cmd_labs_export_es_write_block_4xx)

    b_export = export_sub.add_parser(SCENARIO_ES_429_INJECT, help="Export Jaeger traces for ExpB run")
    b_export.add_argument("--run-id")
    b_export.add_argument("--outdir")
    b_export.add_argument("--service", default="wordloom-search-outbox-worker")
    b_export.add_argument("--lookback", default="1h")
    b_export.add_argument("--limit", type=int, default=20)
    b_export.set_defaults(func=_cmd_labs_export_es_429_inject)

    a_export = export_sub.add_parser(SCENARIO_ES_DOWN_CONNECT, help="Export Jaeger traces for ExpA run")
    a_export.add_argument("--run-id")
    a_export.add_argument("--outdir")
    a_export.add_argument("--service", default="wordloom-search-outbox-worker")
    a_export.add_argument("--lookback", default="1h")
    a_export.add_argument("--limit", type=int, default=20)
    a_export.set_defaults(func=_cmd_labs_export_es_down_connect)

    cd_export = export_sub.add_parser(SCENARIO_COLLECTOR_DOWN, help="Export Jaeger traces for P1 collector_down run")
    cd_export.add_argument("--run-id")
    cd_export.add_argument("--outdir")
    cd_export.add_argument("--service", default="wordloom-search-outbox-worker")
    cd_export.add_argument("--lookback", default="30m")
    cd_export.add_argument("--limit", type=int, default=20)
    cd_export.set_defaults(func=_cmd_labs_export_collector_down)

    d_export = export_sub.add_parser(SCENARIO_ES_BULK_PARTIAL, help="Export Jaeger traces for ExpD run")
    d_export.add_argument("--run-id")
    d_export.add_argument("--outdir")
    d_export.add_argument("--service", default="wordloom-search-outbox-worker")
    d_export.add_argument("--lookback", default="1h")
    d_export.add_argument("--limit", type=int, default=20)
    d_export.set_defaults(func=_cmd_labs_export_es_bulk_partial)

    e_export = export_sub.add_parser(SCENARIO_DB_CLAIM_CONTENTION, help="Export Jaeger traces for ExpE run")
    e_export.add_argument("--run-id")
    e_export.add_argument("--outdir")
    e_export.add_argument("--service", default="wordloom-search-outbox-worker")
    e_export.add_argument("--lookback", default="30m")
    e_export.add_argument("--limit", type=int, default=50)
    e_export.set_defaults(func=_cmd_labs_export_db_claim_contention)

    f_export = export_sub.add_parser(SCENARIO_STUCK_RECLAIM, help="Export Jaeger traces for ExpF run")
    f_export.add_argument("--run-id")
    f_export.add_argument("--outdir")
    f_export.add_argument("--service", default="wordloom-search-outbox-worker")
    f_export.add_argument("--lookback", default="30m")
    f_export.add_argument("--limit", type=int, default=50)
    f_export.set_defaults(func=_cmd_labs_export_stuck_reclaim)

    g_export = export_sub.add_parser(SCENARIO_DUPLICATE_DELIVERY, help="Export Jaeger traces for ExpG run")
    g_export.add_argument("--run-id")
    g_export.add_argument("--outdir")
    g_export.add_argument("--service", default="wordloom-search-outbox-worker")
    g_export.add_argument("--lookback", default="30m")
    g_export.add_argument("--limit", type=int, default=50)
    g_export.set_defaults(func=_cmd_labs_export_duplicate_delivery)

    h_export = export_sub.add_parser(SCENARIO_PROJECTION_VERSION, help="Export Jaeger traces for ExpH run")
    h_export.add_argument("--run-id")
    h_export.add_argument("--outdir")
    h_export.add_argument("--service", default="wordloom-chronicle-outbox-worker")
    h_export.add_argument("--lookback", default="30m")
    h_export.add_argument("--limit", type=int, default=50)
    h_export.set_defaults(func=_cmd_labs_export_projection_version)

    clean = labs_sub.add_parser("clean", help="Cleanup a scenario (revert injection / prune snapshots)")
    clean_sub = clean.add_subparsers(dest="scenario", required=True)

    clean_common = argparse.ArgumentParser(add_help=False)
    clean_common.add_argument(
        "--env-file",
        default=".env.test",
        help="Env file to load (repo-root relative by default). Only used by scenarios that revert external state.",
    )

    c_clean = clean_sub.add_parser(
        SCENARIO_ES_WRITE_BLOCK_4XX,
        help="Disable write block + optional snapshot pruning",
        parents=[clean_common],
    )
    c_clean.add_argument("--outdir")
    c_clean.add_argument("--keep-last", type=int, default=None)
    c_clean.set_defaults(func=_cmd_labs_clean_es_write_block_4xx)

    b_clean = clean_sub.add_parser(
        SCENARIO_ES_429_INJECT,
        help="Noop cleanup + optional snapshot pruning",
        parents=[clean_common],
    )
    b_clean.add_argument("--outdir")
    b_clean.add_argument("--keep-last", type=int, default=None)
    b_clean.set_defaults(func=_cmd_labs_clean_es_429_inject)

    a_clean = clean_sub.add_parser(
        SCENARIO_ES_DOWN_CONNECT,
        help="Start ES + optional snapshot pruning",
        parents=[clean_common],
    )
    a_clean.add_argument("--outdir")
    a_clean.add_argument("--keep-last", type=int, default=None)
    a_clean.set_defaults(func=_cmd_labs_clean_es_down_connect)

    cd_clean = clean_sub.add_parser(
        SCENARIO_COLLECTOR_DOWN,
        help="Start Jaeger + optional snapshot pruning",
        parents=[clean_common],
    )
    cd_clean.add_argument("--outdir")
    cd_clean.add_argument("--keep-last", type=int, default=None)
    cd_clean.set_defaults(func=_cmd_labs_clean_collector_down)

    d_clean = clean_sub.add_parser(
        SCENARIO_ES_BULK_PARTIAL,
        help="Noop cleanup + optional snapshot pruning",
        parents=[clean_common],
    )
    d_clean.add_argument("--outdir")
    d_clean.add_argument("--keep-last", type=int, default=None)
    d_clean.set_defaults(func=_cmd_labs_clean_es_bulk_partial)

    e_clean = clean_sub.add_parser(
        SCENARIO_DB_CLAIM_CONTENTION,
        help="Noop cleanup + optional snapshot pruning",
        parents=[clean_common],
    )
    e_clean.add_argument("--outdir")
    e_clean.add_argument("--keep-last", type=int, default=None)
    e_clean.set_defaults(func=_cmd_labs_clean_db_claim_contention)

    f_clean = clean_sub.add_parser(
        SCENARIO_STUCK_RECLAIM,
        help="Noop cleanup + optional snapshot pruning",
        parents=[clean_common],
    )
    f_clean.add_argument("--outdir")
    f_clean.add_argument("--keep-last", type=int, default=None)
    f_clean.set_defaults(func=_cmd_labs_clean_stuck_reclaim)

    g_clean = clean_sub.add_parser(
        SCENARIO_DUPLICATE_DELIVERY,
        help="Noop cleanup + optional snapshot pruning",
        parents=[clean_common],
    )
    g_clean.add_argument("--outdir")
    g_clean.add_argument("--keep-last", type=int, default=None)
    g_clean.set_defaults(func=_cmd_labs_clean_duplicate_delivery)

    h_clean = clean_sub.add_parser(
        SCENARIO_PROJECTION_VERSION,
        help="Noop cleanup + optional snapshot pruning",
        parents=[clean_common],
    )
    h_clean.add_argument("--outdir")
    h_clean.add_argument("--keep-last", type=int, default=None)
    h_clean.set_defaults(func=_cmd_labs_clean_projection_version)

    return p

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # 1) 确保内置 scenarios 被 import 并注册
    _wg_registry.load_builtin_scenarios()

    # 2) 识别 scenario：统一兼容 write_gate_scenario / scenario + _ / - 命名风格
    raw_scenario = getattr(args, "write_gate_scenario", None) or getattr(args, "scenario", None)
    scenario: str | None = None
    scenario_candidates: list[str] = []
    if isinstance(raw_scenario, str) and raw_scenario.strip():
        scenario = raw_scenario.strip()
        scenario_candidates.append(scenario)
        if "-" in scenario:
            scenario_candidates.append(scenario.replace("-", "_"))
        if "_" in scenario:
            scenario_candidates.append(scenario.replace("_", "-"))

    # 去重并保持顺序
    seen: set[str] = set()
    scenario_candidates = [s for s in scenario_candidates if not (s in seen or seen.add(s))]

    # 3) 只要匹配到“新架构的 scenario”，就抢先执行并退出（不走 args.func）
    if scenario_candidates:
        handler = None
        matched_scenario: str | None = None
        for candidate in scenario_candidates:
            try:
                handler = _wg_registry.get(candidate)
                matched_scenario = candidate
                break
            except KeyError:
                continue

        if handler is not None:
            scenario = matched_scenario or scenario_candidates[0]
            scope_id = getattr(args, "scope_id", None) or "S2B"
            run_id = getattr(args, "run_id", None) or "local"

            # pydantic 输入边界：自动透传 argparse 字段（extra=allow）
            input_payload = {k: v for k, v in vars(args).items() if k not in {"func"}}
            input_payload.update(
                {
                    "scenario": scenario,
                    "scope_id": scope_id,
                    "run_id": run_id,
                    "timeout_s": getattr(args, "timeout_s", None),
                    "sampling": getattr(args, "sampling", None),
                }
            )
            inputs = DrillInputs.model_validate(input_payload)

            result = handler(inputs)

            # 4) 按你的证据 contract 落盘：_result.json + summary.json（先做最小闭环）
            outdir_arg = getattr(args, "outdir", None)
            if outdir_arg:
                paths = build_evidence_paths_for_dir(Path(str(outdir_arg)))
            else:
                paths = build_evidence_paths(scope_id=inputs.scope_id, scenario=inputs.scenario, run_id=inputs.run_id)

            # Keep legacy evidence structure: _result.json is the scenario's meta dict.
            write_json(paths.result_json, result.meta)
            write_json(paths.summary_json, result.summary)

            # 5) 可选：把整个 snapshot_dir 打 zip（如果你后面 workflow 需要）
            zip_path = paths.snapshot_dir / "evidence.zip"
            if not result.ok:
                zip_directory(source_dir=paths.snapshot_dir, zip_path=zip_path)

            return 0 if result.ok else 2

    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
