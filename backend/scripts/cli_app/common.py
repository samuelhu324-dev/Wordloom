from __future__ import annotations

import json
import uuid
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from typing import Literal


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SNAPSHOT_ROOT = REPO_ROOT / "docs" / "labs" / "_snapshot" / "auto"

RESULT_FILENAME = "_result.json"
ARTIFACTS_DIRNAME = "artifacts"
SUMMARY_FILENAME = "summary.json"
LOGS_FILENAME = "logs.txt"
TRACES_FILENAME = "traces.json"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_run_id() -> str:
    return uuid.uuid4().hex


def resolve_snapshot_dir(
    *, scope_id: str, scenario: str, run_id: str, snapshot_root: Path | None = None
) -> Path:
    root = snapshot_root or DEFAULT_SNAPSHOT_ROOT
    return root / scope_id / scenario / run_id


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: Any, *, indent: int = 2) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
        f.write("\n")


def write_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    path.write_text(text, encoding="utf-8")


def result_path(snapshot_dir: Path) -> Path:
    return snapshot_dir / RESULT_FILENAME


def artifacts_dir(snapshot_dir: Path) -> Path:
    return snapshot_dir / ARTIFACTS_DIRNAME


def summary_path(snapshot_dir: Path) -> Path:
    return artifacts_dir(snapshot_dir) / SUMMARY_FILENAME


def logs_path(snapshot_dir: Path) -> Path:
    return artifacts_dir(snapshot_dir) / LOGS_FILENAME


def traces_path(snapshot_dir: Path) -> Path:
    return artifacts_dir(snapshot_dir) / TRACES_FILENAME


def zip_directory(*, source_dir: Path, zip_path: Path) -> None:
    """Create a zip file containing the full contents of source_dir."""

    ensure_dir(zip_path.parent)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in source_dir.rglob("*"):
            if file_path.is_dir():
                continue
            arcname = file_path.relative_to(source_dir)
            zf.write(file_path, arcname.as_posix())


@dataclass(frozen=True)
class EvidencePaths:
    snapshot_dir: Path
    result_json: Path
    artifacts_dir: Path
    summary_json: Path
    logs_txt: Path
    traces_json: Path


def build_evidence_paths(*, scope_id: str, scenario: str, run_id: str) -> EvidencePaths:
    """Resolve canonical evidence bundle paths.

    Contract reference: docs/runbook/run-S2B-projection-table-merge.md
    """

    snapshot_dir = resolve_snapshot_dir(scope_id=scope_id, scenario=scenario, run_id=run_id)
    return EvidencePaths(
        snapshot_dir=snapshot_dir,
        result_json=result_path(snapshot_dir),
        artifacts_dir=artifacts_dir(snapshot_dir),
        summary_json=summary_path(snapshot_dir),
        logs_txt=logs_path(snapshot_dir),
        traces_json=traces_path(snapshot_dir),
    )


def build_evidence_paths_for_dir(snapshot_dir: Path) -> EvidencePaths:
    """Build evidence paths rooted at an explicit snapshot directory.

    This is used by shim/double-parallel mode where legacy CLI commands accept
    `--outdir` and we must respect it.
    """

    return EvidencePaths(
        snapshot_dir=snapshot_dir,
        result_json=result_path(snapshot_dir),
        artifacts_dir=artifacts_dir(snapshot_dir),
        summary_json=summary_path(snapshot_dir),
        logs_txt=logs_path(snapshot_dir),
        traces_json=traces_path(snapshot_dir),
    )


ZipWhen = Literal["never", "on_failure", "always"]


@dataclass(frozen=True)
class PackedArtifacts:
    """Represents the concrete files produced by pack_artifacts()."""

    result_json: Path
    summary_json: Path | None
    logs_txt: Path | None
    traces_json: Path | None
    zip_path: Path | None


def pack_artifacts(
    *,
    paths: EvidencePaths,
    result: dict[str, Any],
    summary: dict[str, Any] | None = None,
    logs_text: str | None = None,
    traces: dict[str, Any] | None = None,
    zip_when: ZipWhen = "never",
    zip_path: Path | None = None,
    indent: int = 2,
) -> PackedArtifacts:
    """Write evidence artifacts according to the stable contract.

    Contract goals:
    - Always write `<outdir>/_result.json` (UTF-8, pretty JSON, trailing newline).
    - Optionally write `artifacts/summary.json`, `artifacts/logs.txt`, `artifacts/traces.json`.
    - Optionally zip the full `snapshot_dir` for CI/upload, with caller-controlled naming.

    Notes:
    - This function intentionally does not invent zip naming. When zipping is enabled,
      callers must provide `zip_path` to preserve existing conventions per workflow.
    """

    write_json(paths.result_json, result, indent=indent)

    written_summary: Path | None = None
    written_logs: Path | None = None
    written_traces: Path | None = None

    if summary is not None:
        write_json(paths.summary_json, summary, indent=indent)
        written_summary = paths.summary_json

    if logs_text is not None:
        write_text(paths.logs_txt, logs_text)
        written_logs = paths.logs_txt

    if traces is not None:
        write_json(paths.traces_json, traces, indent=indent)
        written_traces = paths.traces_json

    ok = bool(result.get("ok"))
    should_zip = (
        (zip_when == "always")
        or (zip_when == "on_failure" and not ok)
        or (zip_when == "never" and False)
    )

    written_zip: Path | None = None
    if should_zip:
        if zip_path is None:
            raise ValueError("zip_path is required when zip_when is not 'never'")
        zip_directory(source_dir=paths.snapshot_dir, zip_path=zip_path)
        written_zip = zip_path

    return PackedArtifacts(
        result_json=paths.result_json,
        summary_json=written_summary,
        logs_txt=written_logs,
        traces_json=written_traces,
        zip_path=written_zip,
    )
