from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path

from cli_app import registry as _wg_registry
from cli_app.common import build_evidence_paths_for_dir, pack_artifacts
from cli_app.labs import shared as _labs_shared
from cli_app.types import DrillInputs


def _require_database_url(*, env: dict[str, str], provided: str | None, log_prefix: str) -> str | None:
    database_url = (provided or env.get("DATABASE_URL") or "").strip()
    if not database_url:
        print(f"[{log_prefix}] DATABASE_URL is required (via env or --database-url)")
        return None
    return database_url


def _invoke_and_pack(*, scenario: str, payload: dict[str, object], outdir: Path) -> dict[str, object]:
    _wg_registry.load_builtin_scenarios()
    handler = _wg_registry.get(scenario)

    inputs = DrillInputs.model_validate(payload)
    drill = handler(inputs)
    result = drill.meta or {}
    pack_artifacts(paths=build_evidence_paths_for_dir(outdir), result=result)
    return result


def cmd_labs_chronicle_entries_envelope_backfill_rehearsal(
    args: argparse.Namespace,
    *,
    lab_id: str,
    scenario: str,
    now_run_id: Callable[[], str] = _labs_shared.now_run_id,
    default_outdir: Callable[..., Path] = _labs_shared.default_auto_outdir,
    ensure_dir: Callable[[Path], None] = _labs_shared.ensure_dir,
    load_env: Callable[..., dict[str, str]] = _labs_shared.load_env,
) -> int:
    log_prefix = "labs chronicle-entries-envelope-backfill-rehearsal"

    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(lab_id=lab_id, scenario=scenario, run_id=run_id)
    ensure_dir(outdir)

    env = load_env(env_file=args.env_file)
    database_url = _require_database_url(env=env, provided=args.database_url, log_prefix=log_prefix)
    if not database_url:
        return 2

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": scenario,
            "scope_id": lab_id,
            "run_id": run_id,
            "outdir": str(outdir),
            "database_url": database_url,
        }
    )

    result = _invoke_and_pack(scenario=scenario, payload=input_payload, outdir=outdir)

    ok = bool(result.get("ok"))
    event_id = str(result.get("event_id") or "")

    print("labs-p2c2.rehearsal_chronicle_entries_envelope_backfill")
    if event_id:
        print(f"event_id={event_id}")
    print(f"ok={ok}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2
