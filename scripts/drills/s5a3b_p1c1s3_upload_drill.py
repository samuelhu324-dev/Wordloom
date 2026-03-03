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
    infra_compose_file: Path
    db_service: str
    bucket: str
    prefix: str
    db_name: str
    dump_file: Path
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


def pick_latest_dump(repo_root: Path) -> Path:
    env_value = os.environ.get("WORDLOOM_S5A3A_DUMP_FILE")
    if env_value:
        candidate = (repo_root / env_value).resolve()
        if not candidate.exists():
            raise RuntimeError(f"WORDLOOM_S5A3A_DUMP_FILE not found: {candidate}")
        return candidate

    dumps_dir = repo_root / "artifacts" / "_tmp_s5a3a_p1c1s2"
    candidates = sorted(dumps_dir.glob("wordloom_wordloom_dev_*.dump"), key=lambda p: p.stat().st_mtime)
    if not candidates:
        raise RuntimeError(f"No dump files found in {dumps_dir}")
    return candidates[-1]


def build_config() -> Config:
    repo_root = find_repo_root()

    compose_file = repo_root / "docker-compose.devtest-db.yml"
    infra_compose_file = repo_root / "docker-compose.infra.yml"

    db_service = os.environ.get("WORDLOOM_DEVTEST_DB_SERVICE", "db_devtest")

    bucket = os.environ.get("WORDLOOM_S5A3B_BUCKET", "wordloom-backups-devtest")
    prefix = os.environ.get("WORDLOOM_S5A3B_PREFIX", "s5a3a")
    db_name = os.environ.get("WORDLOOM_S5A3B_DB_NAME", "wordloom_dev")

    dump_file = pick_latest_dump(repo_root)

    artifacts_dir = repo_root / "artifacts" / "_tmp_s5a3b_p1c1s3"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    return Config(
        repo_root=repo_root,
        compose_file=compose_file,
        infra_compose_file=infra_compose_file,
        db_service=db_service,
        bucket=bucket,
        prefix=prefix,
        db_name=db_name,
        dump_file=dump_file,
        artifacts_dir=artifacts_dir,
    )


def main() -> int:
    cfg = build_config()

    run_id = str(uuid.uuid4())
    started_at = utc_now_iso()
    epoch = int(time.time())

    dump_rel = cfg.dump_file.relative_to(cfg.repo_root)

    upload_script = cfg.repo_root / "scripts" / "backup" / "s5a3b_p1c1s2_upload_dump_to_minio.ps1"
    if not upload_script.exists():
        raise RuntimeError(f"Upload script not found: {upload_script}")

    manifest_rel = Path("artifacts") / "_tmp_s5a3b_p1c1s2" / f"manifest_{epoch}.json"

    upload_proc = run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(upload_script),
            "-ComposeFile",
            str(cfg.infra_compose_file.relative_to(cfg.repo_root)),
            "-DumpFile",
            dump_rel.as_posix(),
            "-Bucket",
            cfg.bucket,
            "-Prefix",
            cfg.prefix,
            "-DbName",
            cfg.db_name,
            "-ManifestFile",
            manifest_rel.as_posix(),
        ],
        cwd=cfg.repo_root,
    )
    require_ok(upload_proc, "upload dump to minio")

    stdout_text = (upload_proc.stdout or "").strip()
    stderr_text = (upload_proc.stderr or "").strip()

    upload_json = None
    try:
        upload_json = json.loads(stdout_text)
    except Exception:
        # Fallback: try to extract the last JSON object from mixed stdout.
        start = stdout_text.rfind("{")
        end = stdout_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                upload_json = json.loads(stdout_text[start : end + 1])
            except Exception:
                upload_json = {"parse_error": True, "raw": stdout_text}
        else:
            upload_json = {"parse_error": True, "raw": stdout_text}

    finished_at = utc_now_iso()

    evidence = {
        "meta": {
            "run_id": run_id,
            "started_at": started_at,
            "finished_at": finished_at,
            "config": {
                "infra_compose_file": str(cfg.infra_compose_file.relative_to(cfg.repo_root)),
                "bucket": cfg.bucket,
                "prefix": cfg.prefix,
                "db_name": cfg.db_name,
                "dump_file": dump_rel.as_posix(),
                "manifest_file": manifest_rel.as_posix(),
                "lifecycle_expiry_days": 7,
            },
        },
        "drills": {
            "upload": {
                "status": "ok",
                "stdout": stdout_text,
                "stderr": stderr_text,
                "result": upload_json,
            }
        },
        "notes": {
            "dump_file_committed": False,
            "reason": "Dump files may contain sensitive data; store in object storage and commit only evidence JSON.",
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
