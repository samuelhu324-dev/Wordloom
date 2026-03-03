import json
import os
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Config:
    repo_root: Path
    compose_file: Path
    service: str
    user: str
    password: str
    source_dump: Path
    target_db: str
    artifacts_dir: Path


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def require_ok(proc: subprocess.CompletedProcess, context: str) -> None:
    if proc.returncode == 0:
        return
    msg = (
        f"{context} failed (exit={proc.returncode}).\n"
        f"STDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}\n"
    )
    raise RuntimeError(msg)


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "docker-compose.devtest-db.yml").exists():
            return parent
    raise RuntimeError("Could not find repo root (docker-compose.devtest-db.yml not found in parents).")


def pick_latest_dump(repo_root: Path) -> Path:
    env_value = os.environ.get("WORDLOOM_S5A3A_DUMP_FILE")
    if env_value:
        candidate = (repo_root / env_value).resolve()
        if not candidate.exists():
            raise RuntimeError(f"WORDLOOM_S5A3A_DUMP_FILE not found: {candidate}")
        return candidate

    dumps_dir = repo_root / "artifacts" / "_tmp_s5a3a_p1c1s2"
    if not dumps_dir.exists():
        raise RuntimeError(f"Dump directory not found: {dumps_dir}")

    candidates = sorted(dumps_dir.glob("wordloom_wordloom_dev_*.dump"), key=lambda p: p.stat().st_mtime)
    if not candidates:
        raise RuntimeError(f"No dump files found in {dumps_dir}")

    return candidates[-1]


def build_config() -> Config:
    repo_root = find_repo_root()
    compose_file = repo_root / "docker-compose.devtest-db.yml"

    service = os.environ.get("WORDLOOM_DEVTEST_DB_SERVICE", "db_devtest")
    user = os.environ.get("WORDLOOM_DEVTEST_DB_USER", "wordloom")
    password = os.environ.get("WORDLOOM_DEVTEST_DB_PASSWORD", "wordloom")

    source_dump = pick_latest_dump(repo_root)
    target_db = os.environ.get("WORDLOOM_S5A3A_RESTORE_DB", "wordloom_restore_dev")

    artifacts_dir = repo_root / "artifacts" / "_tmp_s5a3a_p2c1s2"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    return Config(
        repo_root=repo_root,
        compose_file=compose_file,
        service=service,
        user=user,
        password=password,
        source_dump=source_dump,
        target_db=target_db,
        artifacts_dir=artifacts_dir,
    )


def docker_compose_up(cfg: Config) -> None:
    up = run(["docker", "compose", "-f", str(cfg.compose_file), "up", "-d"], cwd=cfg.repo_root)
    require_ok(up, "docker compose up")


def docker_compose_container_id(cfg: Config) -> str:
    ps = run(["docker", "compose", "-f", str(cfg.compose_file), "ps", "-q", cfg.service], cwd=cfg.repo_root)
    require_ok(ps, "docker compose ps")
    container_id = ps.stdout.strip()
    if not container_id:
        raise RuntimeError(f"No container found for service '{cfg.service}'.")
    return container_id


def psql_exec(container_id: str, cfg: Config, database: str, sql: str) -> subprocess.CompletedProcess:
    return run(
        [
            "docker",
            "exec",
            "-e",
            f"PGPASSWORD={cfg.password}",
            container_id,
            "psql",
            "-U",
            cfg.user,
            "-d",
            database,
            "-v",
            "ON_ERROR_STOP=1",
            "-tA",
            "-c",
            sql,
        ],
        cwd=cfg.repo_root,
    )


def main() -> int:
    cfg = build_config()

    run_id = str(uuid.uuid4())
    started_at = utc_now_iso()

    docker_compose_up(cfg)
    container_id = docker_compose_container_id(cfg)

    restore_script = cfg.repo_root / "scripts" / "backup" / "s5a3a_p2c1s1_pg_restore_devtest.ps1"
    if not restore_script.exists():
        raise RuntimeError(f"Restore script not found: {restore_script}")

    epoch = int(time.time())

    dump_rel = cfg.source_dump.relative_to(cfg.repo_root)

    restore_proc = run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(restore_script),
            "-ComposeFile",
            str(cfg.compose_file.relative_to(cfg.repo_root)),
            "-Service",
            cfg.service,
            "-DumpFile",
            str(dump_rel),
            "-TargetDatabase",
            cfg.target_db,
            "-User",
            cfg.user,
            "-Password",
            cfg.password,
            "-DropIfExists",
        ],
        cwd=cfg.repo_root,
    )
    require_ok(restore_proc, "pg_restore script")

    # Verification (minimal): target db exists and has user tables.
    verify: dict[str, object] = {}

    exists_proc = psql_exec(
        container_id,
        cfg,
        "postgres",
        f"SELECT count(*) FROM pg_database WHERE datname = '{cfg.target_db}';",
    )
    require_ok(exists_proc, "verify database exists")
    verify["db_exists_count"] = exists_proc.stdout.strip()

    ping_proc = psql_exec(container_id, cfg, cfg.target_db, "SELECT 1;")
    require_ok(ping_proc, "verify connect")
    verify["select_1"] = ping_proc.stdout.strip()

    table_count_sql = (
        "SELECT count(*) "
        "FROM pg_catalog.pg_tables "
        "WHERE schemaname NOT IN ('pg_catalog','information_schema');"
    )
    table_count_proc = psql_exec(container_id, cfg, cfg.target_db, table_count_sql)
    require_ok(table_count_proc, "verify table count")
    verify["user_table_count"] = table_count_proc.stdout.strip()

    sample_tables_sql = (
        "SELECT schemaname || '.' || tablename "
        "FROM pg_catalog.pg_tables "
        "WHERE schemaname NOT IN ('pg_catalog','information_schema') "
        "ORDER BY schemaname, tablename "
        "LIMIT 25;"
    )
    sample_proc = psql_exec(container_id, cfg, cfg.target_db, sample_tables_sql)
    require_ok(sample_proc, "verify sample tables")
    verify["sample_tables"] = [line for line in sample_proc.stdout.splitlines() if line.strip()]

    finished_at = utc_now_iso()

    evidence = {
        "meta": {
            "run_id": run_id,
            "started_at": started_at,
            "finished_at": finished_at,
            "config": {
                "compose_file": str(cfg.compose_file.relative_to(cfg.repo_root)),
                "service": cfg.service,
                "user": cfg.user,
                "target_db": cfg.target_db,
                "dump_file": dump_rel.as_posix(),
                "rpo": "24h",
                "rto": "1h",
            },
        },
        "drills": {
            "restore_pg_restore": {
                "status": "ok",
                "container_id": container_id,
                "stdout": restore_proc.stdout.strip(),
                "stderr": restore_proc.stderr.strip(),
            },
            "verify": verify,
        },
        "notes": {
            "dump_file_committed": False,
            "reason": "Restore drill uses a local dump file; evidence JSON is safe to commit but dump may contain sensitive data.",
        },
    }

    evidence_path = cfg.artifacts_dir / f"drills_{epoch}.json"
    evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

    print(evidence_path.relative_to(cfg.repo_root).as_posix())
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise
