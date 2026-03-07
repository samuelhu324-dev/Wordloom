from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
import re


_RUN_DIR_RE = re.compile(r"Wrote artifacts(?: to)?:\s*(?P<dir>.+)\s*$")


def extract_run_dir_from_output(*, stdout: str, suite_root: Path | None = None, suite_id: str | None = None) -> str:
    """Extract run_dir from runner stdout, with optional mtime-based fallback.

    - First try to parse a line like "[OK] Wrote artifacts to <run_dir>" or
      "[OK] Wrote artifacts: <run_dir>".
    - If not found and suite_root is provided, fall back to the most recently
      modified child directory under suite_root.
    """

    run_dir = ""
    for line in (stdout or "").splitlines():
        m = _RUN_DIR_RE.search(line.strip())
        if m:
            run_dir = m.group("dir").strip()
            break

    if not run_dir and suite_root is not None and suite_root.is_dir():
        candidates = [p for p in suite_root.iterdir() if p.is_dir()]
        if candidates:
            candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            run_dir = str(candidates[0])

    if not run_dir and suite_id:
        raise RuntimeError(f"runner_did_not_emit_run_dir:suite={suite_id}")

    return run_dir


@dataclass
class HardGateRunRecord:
    log_id: str
    phase: str
    cycle: str
    step: str
    head_sha: str
    run_dir: str
    suite_id: str
    ok: bool
    contract_ok: bool
    result_ok: bool
    ci_url: str | None
    created_at: str


def append_run_record(path: Path, record: HardGateRunRecord) -> None:
    """Append a run record to a JSON array file under artifacts/.

    The file will be created if it does not exist.
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    data: list[dict[str, Any]]
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, list):  # pragma: no cover - defensive
                data = []
        except Exception:  # pragma: no cover - defensive
            data = []
    else:
        data = []

    payload = {
        "log_id": record.log_id,
        "phase": record.phase,
        "cycle": record.cycle,
        "step": record.step,
        "head_sha": record.head_sha,
        "run_dir": record.run_dir.replace("\\", "/"),
        "suite_id": record.suite_id,
        "ok": record.ok,
        "contract_ok": record.contract_ok,
        "result_ok": record.result_ok,
        "ci_url": record.ci_url,
        "created_at": record.created_at,
    }

    data.append(payload)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
