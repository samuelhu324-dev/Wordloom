from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RunRef:
    scenario_id: str
    run_id: int
    url: str


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _run(
    args: list[str],
    *,
    check: bool = True,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        check=check,
        text=True,
        capture_output=capture,
    )


def _gh_path() -> str:
    override = os.environ.get("GH_PATH")
    if override:
        return override

    default = r"C:\Program Files\GitHub CLI\gh.exe"
    if Path(default).exists():
        return default

    return "gh"


def _gh_json(gh: str, args: list[str]) -> Any:
    completed = _run([gh, *args])
    if not completed.stdout.strip():
        return None
    return json.loads(completed.stdout)


def _list_recent_dispatch_runs(gh: str, *, limit: int = 30) -> list[dict[str, Any]]:
    runs = _gh_json(
        gh,
        [
            "run",
            "list",
            "--workflow",
            "drill-write-gate.yml",
            "--branch",
            "main",
            "--event",
            "workflow_dispatch",
            "--limit",
            str(limit),
            "--json",
            "databaseId,url,createdAt,status,conclusion,displayTitle",
        ],
    )
    if not runs:
        return []
    return list(runs)


def _trigger_and_get_run(gh: str, scenario_id: str, *, poll_seconds: int = 120) -> RunRef:
    before = {r["databaseId"] for r in _list_recent_dispatch_runs(gh, limit=30)}

    _run(
        [
            gh,
            "workflow",
            "run",
            "drill-write-gate.yml",
            "--ref",
            "main",
            "-f",
            f"scenario_id={scenario_id}",
        ],
        capture=True,
    )

    deadline = time.time() + poll_seconds
    while time.time() < deadline:
        runs = _list_recent_dispatch_runs(gh, limit=30)
        for r in runs:
            if r["databaseId"] not in before:
                return RunRef(
                    scenario_id=scenario_id,
                    run_id=int(r["databaseId"]),
                    url=str(r["url"]),
                )
        time.sleep(3)

    raise RuntimeError(f"Timed out waiting for run to appear for scenario_id={scenario_id}")


def _view_run(gh: str, run_id: int) -> dict[str, Any]:
    obj = _gh_json(
        gh,
        [
            "run",
            "view",
            str(run_id),
            "--json",
            "status,conclusion,url,startedAt,updatedAt,headBranch,headSha,displayTitle",
        ],
    )
    if not isinstance(obj, dict):
        raise RuntimeError(f"Unexpected gh run view output for run_id={run_id}: {obj!r}")
    return obj


def main() -> int:
    gh = _gh_path()

    scenarios = [
        # Use legacy IDs as aliases (runner resolves aliases via catalog)
        "shadow_verify_search_index_write_gate",
        "shadow_verify_search_index_paging_stability",
        "shadow_verify_shared_keys",
        "shadow_verify_dual_run_window",
        "shadow_verify_canary_dual_write",
        "shadow_verify_dual_write_sampling",
    ]

    out_dir = Path("artifacts")
    out_dir.mkdir(parents=True, exist_ok=True)

    started = _utc_now().isoformat()
    run_refs: list[RunRef] = []

    for scenario_id in scenarios:
        print(f"Triggering drill-write-gate scenario_id={scenario_id}")
        run_ref = _trigger_and_get_run(gh, scenario_id)
        run_refs.append(run_ref)
        print(f"  -> run_id={run_ref.run_id} url={run_ref.url}")

    (out_dir / "s2b3a-baseline-runs.json").write_text(
        json.dumps(
            {
                "startedAt": started,
                "runs": [r.__dict__ for r in run_refs],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # Poll for completion (best-effort, bounded)
    timeout_seconds = int(os.environ.get("S2B3A_WAIT_SECONDS", "900"))
    poll_interval_seconds = int(os.environ.get("S2B3A_POLL_INTERVAL_SECONDS", "15"))
    deadline = time.time() + timeout_seconds

    final: dict[int, dict[str, Any]] = {}
    while time.time() < deadline and len(final) < len(run_refs):
        for r in run_refs:
            if r.run_id in final:
                continue
            view = _view_run(gh, r.run_id)
            if view.get("status") == "completed":
                final[r.run_id] = view
        if len(final) < len(run_refs):
            time.sleep(poll_interval_seconds)

    final_payload = {
        "startedAt": started,
        "capturedAt": _utc_now().isoformat(),
        "timeoutSeconds": timeout_seconds,
        "runs": [],
    }

    for r in run_refs:
        view = final.get(r.run_id) or _view_run(gh, r.run_id)
        final_payload["runs"].append(
            {
                "scenario_id": r.scenario_id,
                "run_id": r.run_id,
                "url": r.url,
                "status": view.get("status"),
                "conclusion": view.get("conclusion"),
                "headBranch": view.get("headBranch"),
                "headSha": view.get("headSha"),
                "startedAt": view.get("startedAt"),
                "updatedAt": view.get("updatedAt"),
                "displayTitle": view.get("displayTitle"),
            }
        )

    (out_dir / "s2b3a-baseline-runs.final.json").write_text(
        json.dumps(final_payload, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote {out_dir / 's2b3a-baseline-runs.final.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
