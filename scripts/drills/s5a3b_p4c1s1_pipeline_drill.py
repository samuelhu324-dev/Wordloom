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
    artifacts_dir: Path


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(cmd: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
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


def parse_last_nonempty_line(text: str) -> str:
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    return lines[-1] if lines else ""


def read_json(repo_root: Path, rel_path: str) -> dict:
    p = (repo_root / rel_path).resolve()
    if not p.exists():
        raise RuntimeError(f"Evidence file not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def build_config() -> Config:
    repo_root = find_repo_root()
    artifacts_dir = repo_root / "artifacts" / "_tmp_s5a3b_p4c1s1"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    return Config(repo_root=repo_root, artifacts_dir=artifacts_dir)


def main() -> int:
    cfg = build_config()

    run_id = str(uuid.uuid4())
    started_at = utc_now_iso()
    epoch = int(time.time())

    env_base = os.environ.copy()

    # Step 0: create a fresh local dump (S5A-3A backup drill)
    backup_script = cfg.repo_root / "scripts" / "drills" / "s5a3a_p1c1s2_backup_drill.py"
    if not backup_script.exists():
        raise RuntimeError(f"Backup drill not found: {backup_script}")

    backup_proc = run([sys.executable, str(backup_script)], cwd=cfg.repo_root, env=env_base)
    require_ok(backup_proc, "s5a3a backup drill")

    backup_evidence_rel = parse_last_nonempty_line(backup_proc.stdout)
    if not backup_evidence_rel:
        raise RuntimeError("Backup drill did not print an evidence path.")

    backup_evidence = read_json(cfg.repo_root, backup_evidence_rel)
    dump_rel = backup_evidence.get("drills", {}).get("backup_pg_dump", {}).get("dump_file")
    if not isinstance(dump_rel, str) or not dump_rel:
        raise RuntimeError(f"Backup evidence missing dump_file: {backup_evidence_rel}")

    # Step 1: upload dump to object storage (S5A-3B upload drill)
    upload_script = cfg.repo_root / "scripts" / "drills" / "s5a3b_p1c1s3_upload_drill.py"
    if not upload_script.exists():
        raise RuntimeError(f"Upload drill not found: {upload_script}")

    env_upload = env_base.copy()
    env_upload["WORDLOOM_S5A3A_DUMP_FILE"] = dump_rel

    upload_proc = run([sys.executable, str(upload_script)], cwd=cfg.repo_root, env=env_upload)
    require_ok(upload_proc, "s5a3b upload drill")

    upload_evidence_rel = parse_last_nonempty_line(upload_proc.stdout)
    if not upload_evidence_rel:
        raise RuntimeError("Upload drill did not print an evidence path.")

    # Step 2: download -> restore -> verify (S5A-3B P2 drill)
    p2_script = cfg.repo_root / "scripts" / "drills" / "s5a3b_p2c1s2_restore_verify_from_minio_drill.py"
    if not p2_script.exists():
        raise RuntimeError(f"P2 drill not found: {p2_script}")

    env_p2 = env_base.copy()
    env_p2["WORDLOOM_S5A3B_UPLOAD_EVIDENCE"] = upload_evidence_rel

    p2_proc = run([sys.executable, str(p2_script)], cwd=cfg.repo_root, env=env_p2)
    require_ok(p2_proc, "s5a3b p2 restore/verify drill")

    p2_evidence_rel = parse_last_nonempty_line(p2_proc.stdout)
    if not p2_evidence_rel:
        raise RuntimeError("P2 drill did not print an evidence path.")

    # Step 3: download -> restore -> sanitize -> verify (S5A-3B P3 drill)
    p3_script = cfg.repo_root / "scripts" / "drills" / "s5a3b_p3c1s2_restore_sanitize_verify_from_minio_drill.py"
    if not p3_script.exists():
        raise RuntimeError(f"P3 drill not found: {p3_script}")

    env_p3 = env_base.copy()
    env_p3["WORDLOOM_S5A3B_UPLOAD_EVIDENCE"] = upload_evidence_rel

    p3_proc = run([sys.executable, str(p3_script)], cwd=cfg.repo_root, env=env_p3)
    require_ok(p3_proc, "s5a3b p3 sanitize drill")

    p3_evidence_rel = parse_last_nonempty_line(p3_proc.stdout)
    if not p3_evidence_rel:
        raise RuntimeError("P3 drill did not print an evidence path.")

    # Summarize key fields for a single evidence artifact.
    upload_evidence = read_json(cfg.repo_root, upload_evidence_rel)
    upload_result = upload_evidence.get("drills", {}).get("upload", {}).get("result", {})

    p3_evidence = read_json(cfg.repo_root, p3_evidence_rel)
    verify_json = p3_evidence.get("drills", {}).get("verify", {}).get("verify_json")

    finished_at = utc_now_iso()

    evidence = {
        "meta": {
            "run_id": run_id,
            "started_at": started_at,
            "finished_at": finished_at,
            "config": {
                "backup_evidence": backup_evidence_rel,
                "upload_evidence": upload_evidence_rel,
                "p2_evidence": p2_evidence_rel,
                "p3_evidence": p3_evidence_rel,
            },
        },
        "summary": {
            "bucket": upload_result.get("bucket"),
            "object_key": upload_result.get("dump_object_key"),
            "sha256": upload_result.get("sha256"),
            "size_bytes": upload_result.get("size_bytes"),
            "p3_verify": verify_json,
        },
        "drills": {
            "s5a3a_backup": {
                "status": "ok",
                "evidence": backup_evidence_rel,
                "stdout": (backup_proc.stdout or "").strip(),
                "stderr": (backup_proc.stderr or "").strip(),
            },
            "s5a3b_upload": {
                "status": "ok",
                "evidence": upload_evidence_rel,
                "stdout": (upload_proc.stdout or "").strip(),
                "stderr": (upload_proc.stderr or "").strip(),
            },
            "s5a3b_restore_verify": {
                "status": "ok",
                "evidence": p2_evidence_rel,
                "stdout": (p2_proc.stdout or "").strip(),
                "stderr": (p2_proc.stderr or "").strip(),
            },
            "s5a3b_restore_sanitize_verify": {
                "status": "ok",
                "evidence": p3_evidence_rel,
                "stdout": (p3_proc.stdout or "").strip(),
                "stderr": (p3_proc.stderr or "").strip(),
            },
        },
        "notes": {
            "dump_file_committed": False,
            "reason": "DB dumps may contain sensitive data; store dump in object storage and commit only evidence JSON.",
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
