from __future__ import annotations

from dataclasses import dataclass
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from ..common import REPO_ROOT


LABS_SNAPSHOT_ROOT = REPO_ROOT / "docs" / "labs" / "_snapshot"
LAB_ID_S3A_2A_3A = "S3A-2A-3A"
LEGACY_SCRIPTS_DIR = REPO_ROOT / "backend" / "scripts" / "legacy"

# Keep in sync with backend/scripts/search_outbox_worker_impl.py
SEARCH_OUTBOX_OBS_SCHEMA_VERSION = "labs-009-v2"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


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
            return int(resp.status), payload
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace") if getattr(exc, "fp", None) else str(exc)
        return int(getattr(exc, "code", 0) or 0), payload


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
) -> SpawnedWorker:
    """Spawn the Search outbox worker using the stable repo entry.

    This function is part of the Stable Entry contract for fault drills.
    Scenarios should not hardcode script paths or subprocess boilerplate.
    """

    ensure_dir(logs_dir)

    worker_script = REPO_ROOT / "backend" / "scripts" / "search_outbox_worker.py"
    if not worker_script.exists():
        raise FileNotFoundError(str(worker_script))

    cmd = [python_exe(), "-u", str(worker_script)] + (list(extra_args) if extra_args else [])
    log_path = logs_dir / (log_name or f"worker-{run_id}.log")

    log_file = open(log_path, "w", encoding="utf-8")
    started_at = time.time()
    proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)

    keys = sorted(set(evidence_env_keys or []))
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
