from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any
from uuid import UUID

from ..common import REPO_ROOT


LABS_SNAPSHOT_ROOT = REPO_ROOT / "docs" / "labs" / "_snapshot"
LAB_ID_S3A_2A_3A = "S3A-2A-3A"
LEGACY_SCRIPTS_DIR = REPO_ROOT / "backend" / "scripts" / "legacy"

# Keep in sync with backend/scripts/search_outbox_worker_impl.py
SEARCH_OUTBOX_OBS_SCHEMA_VERSION = "labs-009-v2"


SUPPLY_EVIDENCE_PREFIX = "SUPPLY_EVIDENCE_JSON:"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


@dataclass
class SearchOutboxSupplySqlTargetV1:
    table_name: str
    projection: str | None
    chosen_cols: list[str]
    col_types: dict[str, str]


def read_env_file(path: Path) -> dict[str, str]:
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


def load_env(*, env_file: str | None) -> dict[str, str]:
    env = os.environ.copy()
    if env_file:
        env_path = (REPO_ROOT / env_file).resolve() if not Path(env_file).is_absolute() else Path(env_file)
        env.update(read_env_file(env_path))
    return env


def with_backend_pythonpath(env: dict[str, str]) -> dict[str, str]:
    backend_path = str(REPO_ROOT / "backend")
    existing = env.get("PYTHONPATH") or ""
    parts = [p for p in existing.split(os.pathsep) if p]
    if backend_path not in parts:
        parts.insert(0, backend_path)
    env["PYTHONPATH"] = os.pathsep.join(parts)
    return env


def default_labs_auto_run_dir(*, scenario: str, run_id: str) -> Path:
    return LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / scenario / run_id


def latest_child_dir(base: Path) -> Path | None:
    if not base.exists():
        return None
    children = [p for p in base.iterdir() if p.is_dir()]
    if not children:
        return None
    return sorted(children, key=lambda p: p.name, reverse=True)[0]


def resolve_run_dir(*, run_id: str | None, outdir: str | None, scenario: str) -> Path:
    if outdir:
        return Path(outdir)
    if run_id:
        return default_labs_auto_run_dir(scenario=scenario, run_id=run_id)
    latest = latest_child_dir(LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / scenario)
    if latest is None:
        raise SystemExit(f"No runs found for scenario={scenario}")
    return latest


def http_json(
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
            return int(getattr(resp, "status", 0) or 0), payload
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace") if getattr(exc, "fp", None) else str(exc)
        return int(getattr(exc, "code", 0) or 0), payload
    except Exception as exc:
        return 0, f"{type(exc).__name__}: {exc}"


def resolve_search_outbox_supply_sql_target_v1(*, conn, projection: str) -> SearchOutboxSupplySqlTargetV1:
    """Resolve unified-vs-legacy supply target for Search outbox.

    S6A-2A supply contract: default to unified `outbox_events` (projection-scoped)
    when present; fall back to legacy `search_outbox_events` otherwise.
    """

    try:
        from sqlalchemy import text
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(f"sqlalchemy_import_failed: {type(exc).__name__}: {exc}") from exc

    def _table_columns(table_name: str) -> set[str]:
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

    def _table_column_types(table_name: str) -> dict[str, str]:
        rows = conn.execute(
            text(
                """
                SELECT column_name, udt_name
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = :t
                """
            ),
            {"t": table_name},
        ).all()
        return {str(r[0]): str(r[1]) for r in rows if r and r[0] and r[1]}

    outbox_cols = _table_columns("outbox_events")
    if outbox_cols:
        table_name = "outbox_events"
        proj_val: str | None = str(projection)
        fallback_used = False
    else:
        legacy_cols = _table_columns("search_outbox_events")
        if not legacy_cols:
            raise RuntimeError("Neither outbox_events nor search_outbox_events table found")
        table_name = "search_outbox_events"
        proj_val = None
        fallback_used = True

    col_types = _table_column_types(table_name)
    cols = _table_columns(table_name)

    required_cols = {"id", "entity_type", "entity_id", "op", "event_version", "status"}
    if table_name == "outbox_events":
        required_cols.add("projection")
    missing_required = sorted([c for c in required_cols if c not in cols])
    if missing_required:
        raise RuntimeError(f"{table_name} missing required columns: {missing_required}")

    chosen_cols = [
        c
        for c in (
            "id",
            "projection",
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
        if c in cols
    ]

    # Make the fallback decision observable to callers without needing extra queries.
    _ = fallback_used  # kept for readability; evidence uses table_name comparison.

    return SearchOutboxSupplySqlTargetV1(
        table_name=table_name,
        projection=proj_val,
        chosen_cols=chosen_cols,
        col_types=col_types,
    )


def insert_search_outbox_supply_rows_sql_v1(
    *,
    conn,
    target: SearchOutboxSupplySqlTargetV1,
    projection: str,
    candidates: list[dict[str, object]],
    entity_type: str,
    op: str,
    status: str,
) -> dict[str, object]:
    """Insert pending Search outbox rows via SQLAlchemy.

    This is used by shadow_verify_* scenarios where we already have projection
    candidates (entity_id + event_version) and want to enqueue deterministic
    outbox events that follow the S6A-2A supply contract.
    """

    try:
        from sqlalchemy import text
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(f"sqlalchemy_import_failed: {type(exc).__name__}: {exc}") from exc

    now = dt.datetime.now(dt.timezone.utc)
    outbox_event_ids: list[str] = []

    if not candidates:
        return {
            "target_table": target.table_name,
            "projection": (target.projection if target.table_name == "outbox_events" else None),
            "insert_count": 0,
            "entity_type": str(entity_type),
            "op": str(op),
            "create_search_index_row": False,
            "outbox_event_ids": [],
            "fallback": {
                "used": bool(target.table_name != "outbox_events"),
                "reason": ("outbox_events_table_missing" if target.table_name != "outbox_events" else None),
            },
        }

    chosen_cols = list(target.chosen_cols)
    if not chosen_cols:
        raise RuntimeError("target has no chosen_cols")

    proj_val = target.projection if target.table_name == "outbox_events" else None
    if target.table_name == "outbox_events" and proj_val is None:
        proj_val = str(projection)

    rows: list[dict[str, object]] = []
    for c in candidates:
        ev_uuid = uuid.uuid4()
        outbox_event_ids.append(str(ev_uuid))

        entity_id_raw = c.get("entity_id")
        if entity_id_raw is None:
            raise RuntimeError("candidate missing entity_id")
        try:
            entity_uuid = UUID(str(entity_id_raw))
        except Exception as exc:
            raise RuntimeError(f"invalid candidate.entity_id={entity_id_raw!r}: {type(exc).__name__}: {exc}") from exc

        library_id_raw = c.get("library_id")
        library_uuid: UUID | None = None
        if library_id_raw:
            try:
                library_uuid = UUID(str(library_id_raw))
            except Exception as exc:
                raise RuntimeError(
                    f"invalid candidate.library_id={library_id_raw!r}: {type(exc).__name__}: {exc}"
                ) from exc

        try:
            ev_version = int(c.get("event_version") or 0)
        except Exception:
            ev_version = 0

        row: dict[str, object] = {}
        for col in chosen_cols:
            if col == "id":
                row[col] = ev_uuid
            elif col == "projection":
                row[col] = proj_val
            elif col == "entity_type":
                row[col] = str(entity_type)
            elif col == "library_id":
                row[col] = library_uuid
            elif col == "entity_id":
                row[col] = entity_uuid
            elif col == "op":
                row[col] = str(op)
            elif col == "event_version":
                row[col] = int(ev_version)
            elif col == "status":
                row[col] = str(status)
            elif col == "attempts":
                row[col] = 0
            elif col == "replay_count":
                row[col] = 0
            elif col == "created_at":
                row[col] = now
            elif col == "updated_at":
                row[col] = now
            elif col == "traceparent":
                row[col] = None
            elif col == "tracestate":
                row[col] = None

        rows.append(row)

    cols_sql = ", ".join(chosen_cols)
    placeholders = ", ".join([f":{c}" for c in chosen_cols])
    stmt = text(f"INSERT INTO {target.table_name} ({cols_sql}) VALUES ({placeholders})")
    conn.execute(stmt, rows)
    conn.commit()

    return {
        "target_table": target.table_name,
        "projection": (proj_val if target.table_name == "outbox_events" else None),
        "insert_count": int(len(rows)),
        "entity_type": str(entity_type),
        "op": str(op),
        "create_search_index_row": False,
        "outbox_event_ids": list(outbox_event_ids),
        "fallback": {
            "used": bool(target.table_name != "outbox_events"),
            "reason": ("outbox_events_table_missing" if target.table_name != "outbox_events" else None),
        },
    }


def es_set_index_write_block(*, es_url: str, index: str, enabled: bool) -> tuple[int, str]:
    es_url = es_url.strip().rstrip("/")
    index = index.strip()
    url = f"{es_url}/{index}/_settings"
    return http_json("PUT", url, body={"index": {"blocks": {"write": bool(enabled)}}}, timeout_s=5.0)


def es_create_index_if_missing(*, es_url: str, index: str) -> tuple[int, str]:
    es_url = es_url.strip().rstrip("/")
    index = index.strip()
    url = f"{es_url}/{index}"
    return http_json("PUT", url, body=None, timeout_s=5.0)


def scrape_metrics_text(*, port: int, timeout_s: float = 2.0) -> str:
    url = f"http://localhost:{int(port)}/metrics"
    req = urllib.request.Request(url=url, headers={"Accept": "text/plain"})
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310
        return resp.read().decode("utf-8", errors="replace")


def readiness_sleep_v1(scrape_delay_s: float) -> float:
    """Default readiness wait for fault drills.

    We keep this as a small, stable contract: scenarios should not each invent
    their own ad-hoc sleeps.
    """

    sleep_s = max(0.5, float(scrape_delay_s or 0.0))
    time.sleep(sleep_s)
    return float(sleep_s)


def scrape_metrics_text_readiness_v1(
    *,
    port: int,
    timeout_s: float = 4.0,
    readiness_timeout_s: float = 8.0,
    interval_s: float = 0.25,
) -> str:
    """Scrape Prometheus text with a small readiness retry window.

    Returns either the raw metrics text, or a single-line "scrape_failed: ...".
    """

    deadline = time.time() + float(readiness_timeout_s)
    last_exc: Exception | None = None
    while True:
        try:
            return scrape_metrics_text(port=int(port), timeout_s=float(timeout_s))
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if time.time() >= deadline:
                return f"scrape_failed: {type(last_exc).__name__}: {last_exc}\n"
            time.sleep(max(0.05, float(interval_s)))


def prom_parse_counter_sum(text: str, metric: str, *, labels: dict[str, str] | None = None) -> float:
    want = labels or {}
    total = 0.0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith(metric):
            continue

        name_and_labels, *rest = line.split(None, 1)
        if not rest:
            continue
        value_str = rest[0].strip().split()[0]

        lbls: dict[str, str] = {}
        if "{" in name_and_labels and name_and_labels.endswith("}"):
            inside = name_and_labels.split("{", 1)[1][:-1]
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


def prom_sum_reasons(text: str, metric: str, *, reasons: list[str]) -> float:
    return float(sum(prom_parse_counter_sum(text, metric, labels={"reason": r}) for r in reasons))


def extract_last_claim_batch_id(log_path: Path) -> str | None:
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


def parse_last_json_line(text: str) -> dict[str, object] | None:
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


def read_json_file(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None


def python_exe() -> str:
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


def run_cmd(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> int:
    print("[scripts] run:", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(cwd) if cwd else None, env=env)


@dataclass
class SearchOutboxSupplyInsertResult:
    outbox_event_ids: list[str]
    evidence: dict[str, object] | None
    returncode: int | None
    stdout_path: Path
    stderr_path: Path
    timeout_path: Path


def _parse_supply_evidence(stdout_text: str) -> tuple[dict[str, object] | None, list[str]]:
    """Parse optional supply evidence header and return (evidence, id_lines)."""

    if not stdout_text:
        return (None, [])

    lines = [ln.strip() for ln in stdout_text.splitlines() if ln.strip()]
    if not lines:
        return (None, [])

    evidence: dict[str, object] | None = None
    if lines and lines[0].startswith(SUPPLY_EVIDENCE_PREFIX):
        raw = lines[0][len(SUPPLY_EVIDENCE_PREFIX) :].strip()
        try:
            obj = json.loads(raw)
            if isinstance(obj, dict):
                evidence = obj
        except Exception:
            evidence = None
        lines = lines[1:]

    return (evidence, lines)


def run_search_outbox_supply_inserter_v1(
    *,
    outdir: Path,
    env: dict[str, str],
    op: str,
    insert_count: int = 1,
    create_search_index_row: bool = True,
    event_version: str | int | None = 0,
    timeout_s: float = 30.0,
    file_prefix: str = "_trigger_insert_outbox",
) -> SearchOutboxSupplyInsertResult:
    """Insert unified outbox_events supply via the stable Labs-009 inserter.

    S6A-2A contract: default to unified `outbox_events` (projection-scoped) and
    only fall back to legacy when unified table is missing.
    """

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"

    stdout_path = outdir / f"{file_prefix}.stdout.txt"
    stderr_path = outdir / f"{file_prefix}.stderr.txt"
    timeout_path = outdir / f"{file_prefix}.timeout.txt"

    trigger_env = dict(env)
    trigger_env["OUTBOX_OP"] = str(op)
    trigger_env["OUTBOX_INSERT_COUNT"] = str(int(insert_count))
    trigger_env["OUTBOX_CREATE_SEARCH_INDEX_ROW"] = "1" if create_search_index_row else "0"
    if event_version is not None:
        trigger_env.setdefault("OUTBOX_EVENT_VERSION", str(event_version))
    trigger_env["OUTBOX_SUPPLY_EVIDENCE_JSON"] = "1"

    cmd = [python_exe(), str(inserter)]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            env=trigger_env,
            capture_output=True,
            text=True,
            timeout=float(timeout_s),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout_path.write_text((exc.stdout or "") if isinstance(exc.stdout, str) else "", encoding="utf-8")
        stderr_path.write_text((exc.stderr or "") if isinstance(exc.stderr, str) else "", encoding="utf-8")
        timeout_path.write_text(
            f"timeout_s={timeout_s}\ncmd={cmd!r}\n",
            encoding="utf-8",
        )
        return SearchOutboxSupplyInsertResult(
            outbox_event_ids=[],
            evidence=None,
            returncode=None,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            timeout_path=timeout_path,
        )

    stdout_text = proc.stdout or ""
    stderr_text = proc.stderr or ""
    stdout_path.write_text(stdout_text, encoding="utf-8")
    stderr_path.write_text(stderr_text, encoding="utf-8")

    evidence, ids = _parse_supply_evidence(stdout_text)
    return SearchOutboxSupplyInsertResult(
        outbox_event_ids=ids,
        evidence=evidence,
        returncode=int(proc.returncode),
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        timeout_path=timeout_path,
    )


def load_env_from_run_recipe_v1(*, run_dir: Path) -> dict[str, str]:
    recipe = read_json_file(run_dir / "_recipe.json") or {}
    env_file = recipe.get("env_file")
    env = with_backend_pythonpath(load_env(env_file=str(env_file) if env_file else None))
    return env


def _coerce_uuids(ids: list[str]) -> list[UUID]:
    out: list[UUID] = []
    for raw in ids:
        try:
            out.append(UUID(str(raw)))
        except Exception:
            continue
    return out


def verify_supply_rows_v1(*, database_url: str, supply: dict[str, object]) -> dict[str, object]:
    """DB-side verification that supplied outbox ids are present.

    Returns a small evidence object; does not raise on DB failures.
    """

    try:
        from sqlalchemy import bindparam, create_engine, text
    except Exception as exc:  # pragma: no cover
        return {"ok": False, "error": f"sqlalchemy_import_failed: {type(exc).__name__}: {exc}"}

    target_table = str(supply.get("target_table") or "").strip() or None
    projection = str(supply.get("projection") or "").strip() or None
    ids_raw = supply.get("outbox_event_ids")
    if isinstance(ids_raw, list):
        ids = [str(x).strip() for x in ids_raw if str(x).strip()]
    else:
        one = str(supply.get("outbox_event_id") or "").strip()
        ids = [one] if one else []

    if not database_url:
        return {"ok": False, "skipped": True, "reason": "missing_database_url"}
    if not target_table:
        return {"ok": False, "skipped": True, "reason": "missing_target_table"}
    if not ids:
        return {"ok": False, "skipped": True, "reason": "missing_outbox_event_ids"}

    allowed_tables = {"outbox_events", "search_outbox_events"}
    if target_table not in allowed_tables:
        return {"ok": False, "skipped": True, "reason": f"unsupported_target_table:{target_table}"}

    engine = create_engine(str(database_url))
    try:
        with engine.connect() as conn:
            if target_table == "outbox_events":
                if not projection:
                    return {"ok": False, "skipped": True, "reason": "missing_projection_for_outbox_events"}
                stmt = text(
                    "SELECT id::text AS id, status "
                    "FROM outbox_events "
                    "WHERE projection = :projection AND id::text IN :ids"
                ).bindparams(bindparam("ids", expanding=True))
                rows = list(conn.execute(stmt, {"projection": projection, "ids": list(ids)}).fetchall())
            else:
                stmt = text(
                    "SELECT id::text AS id, status "
                    "FROM search_outbox_events "
                    "WHERE id::text IN :ids"
                ).bindparams(bindparam("ids", expanding=True))
                rows = list(conn.execute(stmt, {"ids": list(ids)}).fetchall())

        found = {str(r[0]) for r in rows}
        missing = [x for x in ids if x not in found]
        return {
            "ok": bool(len(missing) == 0),
            "target_table": target_table,
            "projection": projection,
            "expected": int(len(ids)),
            "found": int(len(found)),
            "missing": missing,
        }
    except Exception as exc:
        return {"ok": False, "error": f"db_check_failed: {type(exc).__name__}: {exc}", "target_table": target_table}
    finally:
        try:
            engine.dispose()
        except Exception:
            pass


def docker_compose(*, args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    cmd = ["docker", "compose"] + args
    print("[scripts] run:", " ".join(cmd))
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=False)


@dataclass
class SpawnedWorker:
    entry_id: str
    cmd: list[str]
    cwd: Path
    env_keys: list[str]
    log_path: Path
    proc: subprocess.Popen[object]
    started_at_s: float
    _log_file: object

    def evidence_summary(self) -> dict[str, object]:
        return {
            "entry_id": self.entry_id,
            "cmd": list(self.cmd),
            "cwd": str(self.cwd),
            "pid": int(self.proc.pid) if getattr(self.proc, "pid", None) else None,
            "log_path": str(self.log_path),
            "env_keys": list(self.env_keys),
            "started_at_s": float(self.started_at_s),
        }

    def terminate_and_wait(self, *, timeout_s: float = 30.0) -> None:
        try:
            try:
                self.proc.terminate()
            except Exception:
                return
            try:
                self.proc.wait(timeout=float(timeout_s))
            except subprocess.TimeoutExpired:
                try:
                    self.proc.kill()
                except Exception:
                    pass
                self.proc.wait(timeout=5)
        finally:
            try:
                if self._log_file is not None:
                    self._log_file.close()
            except Exception:
                pass

    def wait(self, *, timeout_s: float = 30.0) -> None:
        try:
            self.proc.wait(timeout=float(timeout_s))
        finally:
            try:
                if self._log_file is not None:
                    self._log_file.close()
            except Exception:
                pass


def spawn_search_outbox_worker(
    *,
    env: dict[str, str],
    logs_dir: Path,
    run_id: str,
    log_name: str | None = None,
    extra_args: list[str] | None = None,
    evidence_env_keys: list[str] | None = None,
    log_mode: str = "w",
    log_header: str | None = None,
) -> SpawnedWorker:
    """Spawn the Search outbox worker using the stable repo entry.

    This function is part of the Stable Entry contract for fault drills.
    Scenarios should not hardcode script paths or subprocess boilerplate.
    """

    ensure_dir(logs_dir)

    # Labs env files often disable the worker by default to keep test runs quiet.
    # Fault drills must explicitly enable the worker so metrics and retry/failure
    # paths can be observed.
    env2 = dict(env)
    raw_enabled = (env2.get("SEARCH_OUTBOX_WORKER_ENABLED") or "").strip().lower()
    if raw_enabled in {"0", "false", "no", "n", "off"}:
        env2["SEARCH_OUTBOX_WORKER_ENABLED"] = "1"

    worker_script = REPO_ROOT / "backend" / "scripts" / "search_outbox_worker.py"
    if not worker_script.exists():
        raise FileNotFoundError(str(worker_script))

    cmd = [python_exe(), "-u", str(worker_script)] + (list(extra_args) if extra_args else [])
    log_path = logs_dir / (log_name or f"worker-{run_id}.log")

    mode = str(log_mode or "w")
    if mode not in {"w", "a"}:
        raise ValueError(f"unsupported log_mode={mode!r}; expected 'w' or 'a'")

    log_file = open(log_path, mode, encoding="utf-8")
    if log_header:
        try:
            log_file.write(str(log_header))
            log_file.flush()
        except Exception:
            pass
    started_at = time.time()
    proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env2, stdout=log_file, stderr=subprocess.STDOUT)

    keys = sorted(set(evidence_env_keys or []))
    if "SEARCH_OUTBOX_WORKER_ENABLED" in env2:
        keys = sorted(set([*keys, "SEARCH_OUTBOX_WORKER_ENABLED"]))
    return SpawnedWorker(
        entry_id="search_outbox_worker@v1",
        cmd=cmd,
        cwd=REPO_ROOT,
        env_keys=keys,
        log_path=log_path,
        proc=proc,
        started_at_s=started_at,
        _log_file=log_file,
    )


def spawn_chronicle_outbox_worker(
    *,
    env: dict[str, str],
    logs_dir: Path,
    run_id: str,
    log_name: str | None = None,
    extra_args: list[str] | None = None,
    evidence_env_keys: list[str] | None = None,
    log_mode: str = "w",
    log_header: str | None = None,
) -> SpawnedWorker:
    """Spawn the Chronicle outbox worker using the stable repo entry.

    This exists to keep fault drills from hardcoding script paths or duplicating
    subprocess boilerplate.
    """

    ensure_dir(logs_dir)

    worker_script = REPO_ROOT / "backend" / "scripts" / "chronicle_outbox_worker.py"
    if not worker_script.exists():
        legacy_script = LEGACY_SCRIPTS_DIR / "chronicle_outbox_worker.py"
        if legacy_script.exists():
            worker_script = legacy_script
        else:
            raise FileNotFoundError(str(worker_script))

    cmd = [python_exe(), "-u", str(worker_script)] + (list(extra_args) if extra_args else [])
    log_path = logs_dir / (log_name or f"chronicle-worker-{run_id}.log")

    mode = str(log_mode or "w")
    if mode not in {"w", "a"}:
        raise ValueError(f"unsupported log_mode={mode!r}; expected 'w' or 'a'")

    log_file = open(log_path, mode, encoding="utf-8")
    if log_header:
        try:
            log_file.write(str(log_header))
            log_file.flush()
        except Exception:
            pass

    started_at = time.time()
    proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)

    keys = sorted(set(evidence_env_keys or []))
    return SpawnedWorker(
        entry_id="chronicle_outbox_worker@v1",
        cmd=cmd,
        cwd=REPO_ROOT,
        env_keys=keys,
        log_path=log_path,
        proc=proc,
        started_at_s=started_at,
        _log_file=log_file,
    )
