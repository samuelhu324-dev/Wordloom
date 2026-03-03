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
    database: str
    user: str
    password: str
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
    msg = (
        f"{context} failed (exit={proc.returncode}).\n"
        f"STDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}\n"
    )
    raise RuntimeError(msg)


def sha256_file(file_path: Path) -> str:
    import hashlib

    hasher = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        candidate = parent / "docker-compose.devtest-db.yml"
        if candidate.exists():
            return parent
    raise RuntimeError("Could not find repo root (docker-compose.devtest-db.yml not found in parents).")


def build_config() -> Config:
    repo_root = find_repo_root()
    compose_file = repo_root / "docker-compose.devtest-db.yml"

    service = os.environ.get("WORDLOOM_DEVTEST_DB_SERVICE", "db_devtest")
    database = os.environ.get("WORDLOOM_DEVTEST_DB_NAME", "wordloom_dev")
    user = os.environ.get("WORDLOOM_DEVTEST_DB_USER", "wordloom")
    password = os.environ.get("WORDLOOM_DEVTEST_DB_PASSWORD", "wordloom")

    artifacts_dir = repo_root / "artifacts" / "_tmp_s5a3a_p1c1s2"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    return Config(
        repo_root=repo_root,
        compose_file=compose_file,
        service=service,
        database=database,
        user=user,
        password=password,
        artifacts_dir=artifacts_dir,
    )


def main() -> int:
    cfg = build_config()

    run_id = str(uuid.uuid4())
    started_at = utc_now_iso()

    # Ensure devtest DB is up.
    up = run(["docker", "compose", "-f", str(cfg.compose_file), "up", "-d"], cwd=cfg.repo_root)
    require_ok(up, "docker compose up")

    # Determine container id (service).
    ps = run(["docker", "compose", "-f", str(cfg.compose_file), "ps", "-q", cfg.service], cwd=cfg.repo_root)
    require_ok(ps, "docker compose ps")
    container_id = ps.stdout.strip()
    if not container_id:
        raise RuntimeError(
            f"No container found for service '{cfg.service}'. Output:\n{ps.stdout}\n{ps.stderr}"
        )

    epoch = int(time.time())
    dump_name = f"wordloom_{cfg.database}_{epoch}.dump"
    dump_path = cfg.artifacts_dir / dump_name

    backup_script = cfg.repo_root / "scripts" / "backup" / "s5a3a_p1c1s1_pg_dump_devtest.ps1"
    if not backup_script.exists():
        raise RuntimeError(f"Backup script not found: {backup_script}")

    # Run backup via Windows PowerShell for maximum compatibility.
    proc = run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(backup_script),
            "-ComposeFile",
            str(cfg.compose_file.relative_to(cfg.repo_root)),
            "-Service",
            cfg.service,
            "-Database",
            cfg.database,
            "-User",
            cfg.user,
            "-Password",
            cfg.password,
            "-OutFile",
            str(dump_path),
        ],
        cwd=cfg.repo_root,
    )
    require_ok(proc, "pg_dump script")

    size_bytes = dump_path.stat().st_size
    sha256 = sha256_file(dump_path)

    dump_rel_posix = dump_path.relative_to(cfg.repo_root).as_posix()

    finished_at = utc_now_iso()

    evidence = {
        "meta": {
            "run_id": run_id,
            "started_at": started_at,
            "finished_at": finished_at,
            "config": {
                "compose_file": str(cfg.compose_file.relative_to(cfg.repo_root)),
                "service": cfg.service,
                "database": cfg.database,
                "user": cfg.user,
                "rpo": "24h",
                "rto": "1h",
            },
        },
        "drills": {
            "backup_pg_dump": {
                "status": "ok",
                "container_id": container_id,
                "dump_file": dump_rel_posix,
                "sha256": sha256,
                "size_bytes": size_bytes,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
            }
        },
        "notes": {
            "dump_file_committed": False,
            "reason": "DB dumps may contain sensitive data; evidence records path+hash but does not commit dump contents.",
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
