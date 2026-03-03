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
    sanitize_sql: Path
    verify_sql: Path
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

    sanitize_sql = repo_root / "scripts" / "backup" / "s5a3a_p3c1s1_sanitize_restore_db.sql"
    verify_sql = repo_root / "scripts" / "backup" / "s5a3a_p3c1s2_verify_sanitization.sql"

    if not sanitize_sql.exists():
        raise RuntimeError(f"Sanitize SQL not found: {sanitize_sql}")
    if not verify_sql.exists():
        raise RuntimeError(f"Verify SQL not found: {verify_sql}")

    artifacts_dir = repo_root / "artifacts" / "_tmp_s5a3a_p3c1s2"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    return Config(
        repo_root=repo_root,
        compose_file=compose_file,
        service=service,
        user=user,
        password=password,
        source_dump=source_dump,
        target_db=target_db,
        sanitize_sql=sanitize_sql,
        verify_sql=verify_sql,
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


def docker_cp_to_container(container_id: str, src: Path, dst: str, cwd: Path) -> subprocess.CompletedProcess:
    return run(["docker", "cp", str(src), f"{container_id}:{dst}"], cwd=cwd)


def psql_file(container_id: str, cfg: Config, database: str, file_path: str) -> subprocess.CompletedProcess:
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
            "-f",
            file_path,
        ],
        cwd=cfg.repo_root,
    )


def extract_last_json_object(stdout: str) -> str:
    lines = [line.strip() for line in (stdout or "").splitlines() if line.strip()]
    for line in reversed(lines):
        if line.startswith("{") and line.endswith("}"):
            return line
    return ""


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

    # Copy SQL into container to avoid quoting issues.
    sanitize_dst = "/tmp/s5a3a_p3_sanitize.sql"
    verify_dst = "/tmp/s5a3a_p3_verify.sql"

    cp_sanitize = docker_cp_to_container(container_id, cfg.sanitize_sql, sanitize_dst, cwd=cfg.repo_root)
    require_ok(cp_sanitize, "docker cp sanitize sql")

    cp_verify = docker_cp_to_container(container_id, cfg.verify_sql, verify_dst, cwd=cfg.repo_root)
    require_ok(cp_verify, "docker cp verify sql")

    sanitize_proc = psql_file(container_id, cfg, cfg.target_db, sanitize_dst)
    require_ok(sanitize_proc, "sanitize sql")

    verify_proc = psql_file(container_id, cfg, cfg.target_db, verify_dst)
    require_ok(verify_proc, "verify sql")

    # Extract JSON outputs (each script prints 1 JSON line).
    sanitize_json_line = extract_last_json_object(sanitize_proc.stdout)
    verify_json_line = extract_last_json_object(verify_proc.stdout)

    sanitize_json = None
    verify_json = None
    try:
        sanitize_json = json.loads(sanitize_json_line) if sanitize_json_line else None
    except Exception:
        sanitize_json = {"parse_error": True, "raw": sanitize_proc.stdout.strip()}

    try:
        verify_json = json.loads(verify_json_line) if verify_json_line else None
    except Exception:
        verify_json = {"parse_error": True, "raw": verify_proc.stdout.strip()}

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
                "sanitize_sql": cfg.sanitize_sql.relative_to(cfg.repo_root).as_posix(),
                "verify_sql": cfg.verify_sql.relative_to(cfg.repo_root).as_posix(),
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
            "sanitize": {
                "status": "ok",
                "stdout": sanitize_proc.stdout.strip(),
                "stderr": sanitize_proc.stderr.strip(),
                "summary_json": sanitize_json,
            },
            "verify": {
                "status": "ok",
                "stdout": verify_proc.stdout.strip(),
                "stderr": verify_proc.stderr.strip(),
                "verify_json": verify_json,
            },
        },
        "notes": {
            "dump_file_committed": False,
            "reason": "Sanitization drill uses a local dump file; evidence JSON is safe to commit but dump may contain sensitive data.",
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
