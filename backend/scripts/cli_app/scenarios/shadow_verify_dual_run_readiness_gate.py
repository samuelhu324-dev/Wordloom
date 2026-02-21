from __future__ import annotations

import json
import time
import uuid
from pathlib import Path

from ..common import ensure_dir, write_json
from ..registry import get as get_scenario
from ..registry import register
from ..types import DrillInputs, DrillResult


SCOPE_ID_S2B_2A_1A = "S2B-2A-1A"
SCOPE_ID_S2B_2A_2A = "S2B-2A-2A"

SCENARIO_WRITE_GATE = "shadow_verify_search_index_write_gate"
SCENARIO_PAGING = "shadow_verify_search_index_paging_stability"
SCENARIO_SHARED_KEYS = "shadow_verify_shared_keys"


def _load_result(path: Path) -> dict[str, object] | None:
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
        return obj if isinstance(obj, dict) else {"_": obj}
    except Exception:
        return None


@register("shadow_verify_dual_run_readiness_gate")
@register("shadow-verify-dual-run-readiness-gate")
def run(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    database_url = str(payload.get("database_url") or "").strip()
    if not database_url:
        return DrillResult(ok=False, errors=["DATABASE_URL is required"], meta={}, summary={})

    library_id = (str(payload.get("library_id") or "").strip() or None)
    if library_id is not None:
        try:
            uuid.UUID(library_id)
        except ValueError:
            return DrillResult(ok=False, errors=[f"invalid library_id: {library_id}"], meta={}, summary={})

    page_size = int(payload.get("page_size") or 0)
    pages_checked = int(payload.get("pages_checked") or 0)
    ensure_min_rows_paging = int(payload.get("ensure_min_rows_paging") or 0)
    ensure_min_rows_keys = int(payload.get("ensure_min_rows_keys") or 0)

    if page_size <= 0:
        return DrillResult(ok=False, errors=["page_size must be > 0"], meta={}, summary={})
    if pages_checked < 2:
        return DrillResult(ok=False, errors=["pages_checked must be >= 2"], meta={}, summary={})
    if ensure_min_rows_paging < 0 or ensure_min_rows_keys < 0:
        return DrillResult(ok=False, errors=["ensure_min_rows_* must be >= 0"], meta={}, summary={})

    outdir_raw = payload.get("outdir")
    outdir = Path(str(outdir_raw)) if outdir_raw else None
    if outdir is None:
        return DrillResult(ok=False, errors=["outdir is required"], meta={}, summary={})

    ensure_dir(outdir)

    scope = "all" if library_id is None else f"library:{library_id}"

    checks_root = outdir / "_checks"
    ensure_dir(checks_root)

    env = payload.get("env") if isinstance(payload.get("env"), dict) else None

    def _run_child(
        *,
        scenario: str,
        scope_id: str,
        child_outdir: Path,
        extra: dict[str, object],
    ) -> tuple[int, dict[str, object] | None]:
        ensure_dir(child_outdir)

        input_payload: dict[str, object] = {
            "scenario": scenario,
            "scope_id": scope_id,
            "run_id": inputs.run_id,
            "outdir": str(child_outdir),
            "database_url": database_url,
            "library_id": library_id,
        }
        if env is not None:
            input_payload["env"] = env
        input_payload.update(extra)

        child_inputs = DrillInputs.model_validate(input_payload)
        handler = get_scenario(scenario)
        child_drill = handler(child_inputs)

        child_result = child_drill.meta or {}
        write_json(child_outdir / "_result.json", child_result)

        exit_code = 0 if bool(child_result.get("ok")) else 2
        return exit_code, _load_result(child_outdir / "_result.json")

    wg_dir = checks_root / SCENARIO_WRITE_GATE
    wg_rc, wg_result = _run_child(
        scenario=SCENARIO_WRITE_GATE,
        scope_id=SCOPE_ID_S2B_2A_1A,
        child_outdir=wg_dir,
        extra={},
    )

    paging_dir = checks_root / SCENARIO_PAGING
    paging_rc, paging_result = _run_child(
        scenario=SCENARIO_PAGING,
        scope_id=SCOPE_ID_S2B_2A_2A,
        child_outdir=paging_dir,
        extra={
            "page_size": page_size,
            "pages_checked": pages_checked,
            "ensure_min_rows": ensure_min_rows_paging,
        },
    )

    keys_dir = checks_root / SCENARIO_SHARED_KEYS
    keys_rc, keys_result = _run_child(
        scenario=SCENARIO_SHARED_KEYS,
        scope_id=SCOPE_ID_S2B_2A_2A,
        child_outdir=keys_dir,
        extra={"ensure_min_rows": ensure_min_rows_keys},
    )

    checks = {
        "write_gate": {
            "scenario": SCENARIO_WRITE_GATE,
            "exit_code": int(wg_rc),
            "ok": bool(wg_rc == 0 and (wg_result or {}).get("ok") is True),
            "result_path": str((wg_dir / "_result.json").as_posix()),
            "result": wg_result,
        },
        "paging_stability": {
            "scenario": SCENARIO_PAGING,
            "exit_code": int(paging_rc),
            "ok": bool(paging_rc == 0 and (paging_result or {}).get("ok") is True),
            "result_path": str((paging_dir / "_result.json").as_posix()),
            "result": paging_result,
        },
        "shared_keys": {
            "scenario": SCENARIO_SHARED_KEYS,
            "exit_code": int(keys_rc),
            "ok": bool(keys_rc == 0 and (keys_result or {}).get("ok") is True),
            "result_path": str((keys_dir / "_result.json").as_posix()),
            "result": keys_result,
        },
    }

    ok = bool(all(v["ok"] is True for v in checks.values()))

    result: dict[str, object] = {
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_dual_run_readiness_gate",
        "run_id": inputs.run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "dry_run": True,
        "inputs": {
            "page_size": page_size,
            "pages_checked": pages_checked,
            "ensure_min_rows_paging": ensure_min_rows_paging,
            "ensure_min_rows_keys": ensure_min_rows_keys,
        },
        "checks": checks,
        "next_step": {
            "recommendation": "After this gate is green in CI, add a minimal canary dual-write scenario with strict scope/limit + one-click rollback.",
            "note": "This gate now emits shared-keys cross-evidence (stdout log probe + traces.json span). Metrics mutual evidence is still out of scope for this drill.",
        },
        "ok": bool(ok),
    }

    return DrillResult(
        ok=bool(ok),
        meta=result,
        summary={
            "scope": scope,
            "dry_run": True,
            "checks_ok": bool(ok),
        },
        errors=[],
    )
