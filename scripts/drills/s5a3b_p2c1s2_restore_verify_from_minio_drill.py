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
    devtest_compose_file: Path
    infra_compose_file: Path
    db_service: str
    db_user: str
    db_password: str
    bucket: str
    prefix: str
    db_name: str
    target_db: str
    artifacts_dir: Path


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def require_ok(proc: subprocess.CompletedProcess, context: str) -> None:
    if proc.returncode == 0:
        return
    raise RuntimeError(
        f"{context} failed (exit={proc.returncode}).\nSTDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}\n"
    )


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "docker-compose.devtest-db.yml").exists():
            return parent
    raise RuntimeError("Could not find repo root.")


def pick_latest_upload_evidence(repo_root: Path) -> Path:
    env_value = os.environ.get("WORDLOOM_S5A3B_UPLOAD_EVIDENCE")
    if env_value:
        p = (repo_root / env_value).resolve()
        if not p.exists():
            raise RuntimeError(f"WORDLOOM_S5A3B_UPLOAD_EVIDENCE not found: {p}")
        return p

    d = repo_root / "artifacts" / "_tmp_s5a3b_p1c1s3"
    candidates = sorted(d.glob("drills_*.json"), key=lambda p: p.stat().st_mtime)
    if not candidates:
        raise RuntimeError(f"No upload evidence found in {d}")
    return candidates[-1]


def parse_upload_evidence(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    result = data.get("drills", {}).get("upload", {}).get("result", {})
    if not isinstance(result, dict) or not result.get("ok"):
        raise RuntimeError(f"Upload evidence missing ok result: {path}")
    return result


def build_config() -> Config:
    repo_root = find_repo_root()

    devtest_compose_file = repo_root / "docker-compose.devtest-db.yml"
    infra_compose_file = repo_root / "docker-compose.infra.yml"

    db_service = os.environ.get("WORDLOOM_DEVTEST_DB_SERVICE", "db_devtest")
    db_user = os.environ.get("WORDLOOM_DEVTEST_DB_USER", "wordloom")
    db_password = os.environ.get("WORDLOOM_DEVTEST_DB_PASSWORD", "wordloom")

    bucket = os.environ.get("WORDLOOM_S5A3B_BUCKET", "wordloom-backups-devtest")
    prefix = os.environ.get("WORDLOOM_S5A3B_PREFIX", "s5a3a")
    db_name = os.environ.get("WORDLOOM_S5A3B_DB_NAME", "wordloom_dev")

    target_db = os.environ.get("WORDLOOM_S5A3B_RESTORE_DB", "wordloom_restore_dev")

    artifacts_dir = repo_root / "artifacts" / "_tmp_s5a3b_p2c1s2"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    return Config(
        repo_root=repo_root,
        devtest_compose_file=devtest_compose_file,
        infra_compose_file=infra_compose_file,
        db_service=db_service,
        db_user=db_user,
        db_password=db_password,
        bucket=bucket,
        prefix=prefix,
        db_name=db_name,
        target_db=target_db,
        artifacts_dir=artifacts_dir,
    )


def docker_compose_up(compose_file: Path, repo_root: Path) -> None:
    up = run(["docker", "compose", "-f", str(compose_file), "up", "-d"], cwd=repo_root)
    require_ok(up, f"docker compose up ({compose_file.name})")


def docker_compose_container_id(compose_file: Path, service: str, repo_root: Path) -> str:
    ps = run(["docker", "compose", "-f", str(compose_file), "ps", "-q", service], cwd=repo_root)
    require_ok(ps, "docker compose ps")
    container_id = (ps.stdout or "").strip()
    if not container_id:
        raise RuntimeError(f"No container found for service '{service}'.")
    return container_id


def psql_exec(container_id: str, user: str, password: str, database: str, sql: str, cwd: Path) -> subprocess.CompletedProcess:
    return run(
        [
            "docker",
            "exec",
            "-e",
            f"PGPASSWORD={password}",
            container_id,
            "psql",
            "-U",
            user,
            "-d",
            database,
            "-v",
            "ON_ERROR_STOP=1",
            "-tA",
            "-c",
            sql,
        ],
        cwd=cwd,
    )


def main() -> int:
    cfg = build_config()

    run_id = str(uuid.uuid4())
    started_at = utc_now_iso()
    epoch = int(time.time())

    upload_evidence_path = pick_latest_upload_evidence(cfg.repo_root)
    upload_result = parse_upload_evidence(upload_evidence_path)

    object_key = os.environ.get("WORDLOOM_S5A3B_DUMP_OBJECT_KEY") or upload_result["dump_object_key"]
    expected_sha256 = upload_result.get("sha256")
    expected_size_bytes = upload_result.get("size_bytes")

    download_script = cfg.repo_root / "scripts" / "backup" / "s5a3b_p2c1s1_download_dump_from_minio.ps1"
    if not download_script.exists():
        raise RuntimeError(f"Download script not found: {download_script}")

    download_rel_out = Path("artifacts") / "_tmp_s5a3b_p2c1s1" / f"download_{epoch}.dump"

    download_proc = run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(download_script),
            "-ComposeFile",
            str(cfg.infra_compose_file.relative_to(cfg.repo_root)),
            "-Bucket",
            cfg.bucket,
            "-ObjectKey",
            object_key,
            "-OutputFile",
            download_rel_out.as_posix(),
            "-ExpectedSha256",
            str(expected_sha256),
            "-ExpectedSizeBytes",
            str(expected_size_bytes),
        ],
        cwd=cfg.repo_root,
    )
    require_ok(download_proc, "download dump from minio")

    stdout_text = (download_proc.stdout or "").strip()
    download_json = None
    try:
        download_json = json.loads(stdout_text)
    except Exception:
        start = stdout_text.rfind("{")
        end = stdout_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            download_json = json.loads(stdout_text[start : end + 1])
        else:
            download_json = {"parse_error": True, "raw": stdout_text}

    downloaded_rel = Path(download_json.get("output_file", download_rel_out.as_posix()))
    downloaded_abs = (cfg.repo_root / downloaded_rel).resolve()
    if not downloaded_abs.exists():
        raise RuntimeError(f"Downloaded dump not found: {downloaded_abs}")

    # Bring up devtest DB.
    docker_compose_up(cfg.devtest_compose_file, cfg.repo_root)
    container_id = docker_compose_container_id(cfg.devtest_compose_file, cfg.db_service, cfg.repo_root)

    # Restore using the existing S5A-3A restore script.
    restore_script = cfg.repo_root / "scripts" / "backup" / "s5a3a_p2c1s1_pg_restore_devtest.ps1"
    if not restore_script.exists():
        raise RuntimeError(f"Restore script not found: {restore_script}")

    dump_rel_for_restore = downloaded_abs.relative_to(cfg.repo_root)

    restore_proc = run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(restore_script),
            "-ComposeFile",
            str(cfg.devtest_compose_file.relative_to(cfg.repo_root)),
            "-Service",
            cfg.db_service,
            "-DumpFile",
            dump_rel_for_restore.as_posix(),
            "-TargetDatabase",
            cfg.target_db,
            "-User",
            cfg.db_user,
            "-Password",
            cfg.db_password,
            "-DropIfExists",
        ],
        cwd=cfg.repo_root,
    )
    require_ok(restore_proc, "pg_restore script")

    # Verification (minimal): target db exists and has user tables.
    verify: dict[str, object] = {}

    exists_proc = psql_exec(
        container_id,
        cfg.db_user,
        cfg.db_password,
        "postgres",
        f"SELECT count(*) FROM pg_database WHERE datname = '{cfg.target_db}';",
        cwd=cfg.repo_root,
    )
    require_ok(exists_proc, "verify database exists")
    verify["db_exists_count"] = (exists_proc.stdout or "").strip()

    ping_proc = psql_exec(container_id, cfg.db_user, cfg.db_password, cfg.target_db, "SELECT 1;", cwd=cfg.repo_root)
    require_ok(ping_proc, "verify connect")
    verify["select_1"] = (ping_proc.stdout or "").strip()

    table_count_sql = (
        "SELECT count(*) "
        "FROM pg_catalog.pg_tables "
        "WHERE schemaname NOT IN ('pg_catalog','information_schema');"
    )
    table_count_proc = psql_exec(container_id, cfg.db_user, cfg.db_password, cfg.target_db, table_count_sql, cwd=cfg.repo_root)
    require_ok(table_count_proc, "verify table count")
    verify["user_table_count"] = (table_count_proc.stdout or "").strip()

    finished_at = utc_now_iso()

    evidence = {
        "meta": {
            "run_id": run_id,
            "started_at": started_at,
            "finished_at": finished_at,
            "config": {
                "infra_compose_file": str(cfg.infra_compose_file.relative_to(cfg.repo_root)),
                "devtest_compose_file": str(cfg.devtest_compose_file.relative_to(cfg.repo_root)),
                "db_service": cfg.db_service,
                "db_user": cfg.db_user,
                "target_db": cfg.target_db,
                "bucket": cfg.bucket,
                "object_key": object_key,
                "expected_sha256": expected_sha256,
                "expected_size_bytes": expected_size_bytes,
                "downloaded_dump_file": dump_rel_for_restore.as_posix(),
                "upload_evidence": upload_evidence_path.relative_to(cfg.repo_root).as_posix(),
                "rpo": "24h",
                "rto": "1h",
            },
        },
        "drills": {
            "download": {
                "status": "ok",
                "stdout": stdout_text,
                "stderr": (download_proc.stderr or "").strip(),
                "result": download_json,
            },
            "restore_pg_restore": {
                "status": "ok",
                "container_id": container_id,
                "stdout": (restore_proc.stdout or "").strip(),
                "stderr": (restore_proc.stderr or "").strip(),
            },
            "verify": verify,
        },
        "notes": {
            "dump_file_committed": False,
            "reason": "Downloaded dump may contain sensitive data; keep dump local and commit only evidence JSON.",
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
