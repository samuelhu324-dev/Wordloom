from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SuiteSpec:
    workflow: str
    scenario_id: str
    extra_inputs: dict[str, str]


@dataclass(frozen=True)
class RunRecord:
    workflow: str
    scenario_id: str
    url: str
    status: str | None
    conclusion: str | None


def _repo_root() -> Path:
    # backend/scripts/ci/<this_file>
    return Path(__file__).resolve().parents[3]


def _run(
    args: list[str],
    *,
    cwd: Path,
    check: bool = True,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd),
        check=check,
        text=True,
        capture_output=capture,
    )


def _detect_gh() -> str:
    gh = shutil.which("gh")
    if gh:
        return gh

    fallback = Path(r"C:\Program Files\GitHub CLI\gh.exe")
    if fallback.exists():
        return str(fallback)

    raise SystemExit(
        "GitHub CLI (gh) not found. Install it and/or ensure it's on PATH."
    )


def _git_head_sha(repo_root: Path) -> str | None:
    try:
        cp = _run(["git", "rev-parse", "HEAD"], cwd=repo_root)
    except Exception:
        return None
    sha = (cp.stdout or "").strip()
    return sha or None


def _git_branch(repo_root: Path) -> str | None:
    try:
        cp = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_root)
    except Exception:
        return None
    branch = (cp.stdout or "").strip()
    return branch or None


def _parse_iso8601(value: str) -> dt.datetime | None:
    # GitHub typically returns Zulu timestamps like 2026-02-23T12:34:56Z
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return dt.datetime.fromisoformat(value)
    except Exception:
        return None


def _gh_run_view(gh: str, *, repo_root: Path, run: str) -> dict[str, Any]:
    # `gh run view` accepts a run ID (and in some versions also a URL).
    # Normalize to run ID for maximum compatibility.
    run_arg = run
    if run.startswith("http"):
        m = re.search(r"/runs/(?P<id>\d+)", run)
        if not m:
            raise ValueError(f"Unable to parse run id from URL: {run}")
        run_arg = m.group("id")

    cp = _run(
        [
            gh,
            "run",
            "view",
            run_arg,
            "--json",
            "url,status,conclusion,createdAt,headSha",
        ],
        cwd=repo_root,
    )
    return json.loads(cp.stdout or "{}")


def _extract_latest_auto_block(text: str) -> tuple[int, int] | None:
    marker = "  - [x] suite 全量回归证据（auto,"
    start = text.rfind(marker)
    if start == -1:
        return None
    end = text.find("\n\n", start)
    if end == -1:
        end = len(text)
    return start, end


_EVIDENCE_LINE_RE = re.compile(
    r"^(?P<prefix>\s*-\s+.*?：)(?P<url>https://\S+?)(?:\s+\((?P<meta>[^)]*)\))?\s*$"
)


def _update_auto_block_with_conclusions(
    *,
    gh: str,
    repo_root: Path,
    log_path: Path,
    wait_seconds: int,
    poll_interval_seconds: int,
) -> None:
    text = log_path.read_text(encoding="utf-8")
    span = _extract_latest_auto_block(text)
    if span is None:
        raise SystemExit(
            f"No auto evidence block found in log: {log_path}. Look for 'suite 全量回归证据（auto,'."
        )

    start, end = span
    block = text[start:end]
    lines = block.splitlines()

    updated_lines: list[str] = []
    for line in lines:
        m = _EVIDENCE_LINE_RE.match(line)
        if not m:
            updated_lines.append(line)
            continue

        url = m.group("url")

        deadline = time.time() + max(0, wait_seconds)
        last = _gh_run_view(gh, repo_root=repo_root, run=url)
        while wait_seconds > 0 and time.time() < deadline:
            status = str(last.get("status") or "")
            conclusion = last.get("conclusion")
            if status in {"completed"} and conclusion:
                break
            time.sleep(max(1, poll_interval_seconds))
            last = _gh_run_view(gh, repo_root=repo_root, run=url)

        status = last.get("status")
        conclusion = last.get("conclusion")

        bits: list[str] = []
        if status:
            bits.append(f"status={status}")
        if conclusion:
            bits.append(f"conclusion={conclusion}")

        suffix = f" ({', '.join(bits)})" if bits else ""
        updated_lines.append(f"{m.group('prefix')}{url}{suffix}")

    new_block = "\n".join(updated_lines)
    new_text = text[:start] + new_block + text[end:]
    log_path.write_text(new_text, encoding="utf-8")


def _find_run_url(
    gh: str,
    *,
    repo_root: Path,
    workflow: str,
    head_sha: str | None,
    started_at: dt.datetime,
    timeout_seconds: int,
) -> RunRecord:
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        cp = _run(
            [
                gh,
                "run",
                "list",
                "--workflow",
                workflow,
                "--event",
                "workflow_dispatch",
                "--limit",
                "20",
                "--json",
                "url,createdAt,headSha,status,conclusion",
            ],
            cwd=repo_root,
        )
        runs: list[dict[str, Any]] = json.loads(cp.stdout or "[]")

        best: dict[str, Any] | None = None
        for item in runs:
            created_at_raw = str(item.get("createdAt") or "")
            created_at = _parse_iso8601(created_at_raw)
            if created_at is None:
                continue
            if created_at < started_at - dt.timedelta(minutes=2):
                continue
            if head_sha and str(item.get("headSha") or "") != head_sha:
                continue
            best = item
            break

        # Fallback: if sha filter didn't match (e.g., repo run on default ref), take the newest within time window
        if best is None:
            for item in runs:
                created_at_raw = str(item.get("createdAt") or "")
                created_at = _parse_iso8601(created_at_raw)
                if created_at is None:
                    continue
                if created_at < started_at - dt.timedelta(minutes=2):
                    continue
                best = item
                break

        if best and best.get("url"):
            return RunRecord(
                workflow=workflow,
                scenario_id="",
                url=str(best.get("url")),
                status=(str(best.get("status")) if best.get("status") else None),
                conclusion=(
                    str(best.get("conclusion")) if best.get("conclusion") else None
                ),
            )

        time.sleep(2)

    raise TimeoutError(
        f"Timed out finding run URL for workflow '{workflow}' within {timeout_seconds}s"
    )


def _append_block_to_log(
    *,
    log_path: Path,
    block: str,
) -> None:
    text = log_path.read_text(encoding="utf-8")
    anchor = "## Risks / Notes"
    idx = text.find(anchor)
    if idx == -1:
        raise SystemExit(f"Log anchor not found: {anchor!r} in {log_path}")

    before = text[:idx].rstrip() + "\n\n"
    after = text[idx:]
    log_path.write_text(before + block.rstrip() + "\n\n" + after, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Trigger drill suite workflows (workflow_dispatch) and append run URLs into the S0C-4A-1A log."
        )
    )
    parser.add_argument(
        "--ref",
        default=None,
        help="Git ref to run workflows on (default: current git branch)",
    )
    parser.add_argument(
        "--log",
        default=None,
        help="Path to log markdown (default: S0C-4A-1A log)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without triggering workflows or editing log",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=120,
        help="How long to wait for each run to appear in gh run list",
    )
    parser.add_argument(
        "--refresh-conclusions",
        action="store_true",
        help=(
            "Update the latest auto evidence block in the log by querying each run's status/conclusion via `gh run view`."
        ),
    )
    parser.add_argument(
        "--wait-seconds",
        type=int,
        default=0,
        help=(
            "When refreshing conclusions, optionally wait up to this many seconds for runs to complete (0 = no waiting)."
        ),
    )
    parser.add_argument(
        "--poll-interval-seconds",
        type=int,
        default=10,
        help="Polling interval used when --wait-seconds is set.",
    )
    args = parser.parse_args()

    repo_root = _repo_root()
    gh = _detect_gh()
    head_sha = _git_head_sha(repo_root)
    ref = args.ref or _git_branch(repo_root) or "main"

    log_path = (
        Path(args.log)
        if args.log
        else repo_root
        / "docs"
        / "logs"
        / "log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md"
    )

    if args.refresh_conclusions:
        if args.dry_run:
            print(f"[dry-run] refresh conclusions log={log_path}")
            return 0

        _update_auto_block_with_conclusions(
            gh=gh,
            repo_root=repo_root,
            log_path=log_path,
            wait_seconds=int(args.wait_seconds),
            poll_interval_seconds=int(args.poll_interval_seconds),
        )
        print(f"Refreshed conclusions in log: {log_path}")
        return 0

    suites: list[SuiteSpec] = [
        SuiteSpec(
            workflow="drill-readiness.yml",
            scenario_id="readiness/search/dual_run_gate",
            extra_inputs={},
        ),
        SuiteSpec(
            workflow="drill-dual-write.yml",
            scenario_id="dual_write/search/canary_cleanup",
            extra_inputs={},
        ),
        SuiteSpec(
            workflow="drill-dual-run.yml",
            scenario_id="dual_run/search/stage1_backfill",
            extra_inputs={},
        ),
        SuiteSpec(
            workflow="drill-shadow-verify-entries.yml",
            scenario_id="verify/chronicle/entries",
            extra_inputs={},
        ),
        SuiteSpec(
            workflow="drill-write-gate.yml",
            scenario_id="readiness/search/dual_run_gate",
            extra_inputs={},
        ),
        SuiteSpec(
            workflow="drill-verify.yml",
            scenario_id="verify/search/write_gate_idempotency",
            extra_inputs={},
        ),
        SuiteSpec(
            workflow="drill-failures.yml",
            scenario_id="fault/obs_infra/all",
            extra_inputs={
                "env_file": ".env.test",
                "duration": "25",
                "lookback": "30m",
                "keep_last": "20",
                # keep force_failure explicit so it can't surprise operators
                "force_failure": "false",
            },
        ),
    ]

    now_utc = dt.datetime.now(dt.timezone.utc)
    started_at = now_utc

    if args.dry_run:
        print(f"[dry-run] gh={gh}")
        print(f"[dry-run] ref={ref} sha={(head_sha or 'unknown')}")
        print(f"[dry-run] log={log_path}")
        for spec in suites:
            print(
                f"[dry-run] trigger {spec.workflow} scenario_id={spec.scenario_id} extras={spec.extra_inputs}"
            )
        return 0

    records: list[RunRecord] = []
    for spec in suites:
        trigger_args = [
            gh,
            "workflow",
            "run",
            spec.workflow,
            "--ref",
            ref,
            "-f",
            f"scenario_id={spec.scenario_id}",
        ]
        for key, value in spec.extra_inputs.items():
            trigger_args.extend(["-f", f"{key}={value}"])

        _run(trigger_args, cwd=repo_root, check=True)
        found = _find_run_url(
            gh,
            repo_root=repo_root,
            workflow=spec.workflow,
            head_sha=head_sha,
            started_at=started_at,
            timeout_seconds=args.timeout_seconds,
        )
        records.append(
            RunRecord(
                workflow=spec.workflow,
                scenario_id=spec.scenario_id,
                url=found.url,
                status=found.status,
                conclusion=found.conclusion,
            )
        )
        # Small delay to reduce the chance of list ordering races across workflows
        time.sleep(1)

    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    sha_short = (head_sha or "unknown")[:8]
    block_lines = [
        f"  - [x] suite 全量回归证据（auto, {ts}, ref={ref}, sha={sha_short}）：",
    ]
    for r in records:
        wf_name = r.workflow.removesuffix(".yml")
        status_bits = []
        if r.status:
            status_bits.append(f"status={r.status}")
        if r.conclusion:
            status_bits.append(f"conclusion={r.conclusion}")
        status_suffix = f" ({', '.join(status_bits)})" if status_bits else ""
        block_lines.append(
            f"    - {wf_name}（scenario_id={r.scenario_id}）：{r.url}{status_suffix}"
        )

    _append_block_to_log(log_path=log_path, block="\n".join(block_lines))

    print("Appended run URLs to log:")
    for r in records:
        print(f"- {r.workflow}: {r.url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
