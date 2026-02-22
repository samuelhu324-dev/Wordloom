from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path

from cli_app import registry as _wg_registry
from cli_app.labs import shared as _labs_shared
from cli_app.scenarios import _failure_drill_shared as _fd_shared
from cli_app.types import DrillInputs


def _default_outdir(scenario: str, run_id: str) -> Path:
    return _fd_shared.default_labs_auto_run_dir(scenario=scenario, run_id=run_id)


def _resolve_run_dir(run_id: str | None, outdir: str | None, scenario: str) -> Path:
    return _fd_shared.resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario)


def _invoke_scenario(
    *,
    handler_name: str,
    payload: dict[str, object],
    fallback_exit_code: int | Callable[[bool], int],
) -> int:
    _wg_registry.load_builtin_scenarios()
    handler = _wg_registry.get(handler_name)

    inputs = DrillInputs.model_validate(payload)
    drill = handler(inputs)

    exit_code = drill.meta.get("exit_code")
    if exit_code is not None:
        return int(exit_code)

    if callable(fallback_exit_code):
        return int(fallback_exit_code(bool(drill.ok)))
    return int(fallback_exit_code)


def cmd_labs_run(
    args: argparse.Namespace,
    *,
    scope_id: str,
    scenario: str,
    handler_base: str,
    now_run_id: Callable[[], str] = _labs_shared.now_run_id,
    default_outdir: Callable[[str, str], Path] = _default_outdir,
    fallback_exit_code: int | Callable[[bool], int] = lambda ok: 0 if ok else 2,
) -> int:
    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(scenario, run_id)

    payload = dict(vars(args))
    payload.pop("func", None)
    payload.update(
        {
            "scenario": f"{handler_base}.run",
            "scope_id": scope_id,
            "run_id": run_id,
            "outdir": str(outdir),
        }
    )

    return _invoke_scenario(handler_name=f"{handler_base}.run", payload=payload, fallback_exit_code=fallback_exit_code)


def cmd_labs_verify(
    args: argparse.Namespace,
    *,
    scope_id: str,
    scenario: str,
    handler_base: str,
    resolve_run_dir: Callable[[str | None, str | None, str], Path] = _resolve_run_dir,
    fallback_exit_code: int | Callable[[bool], int] = lambda ok: 0 if ok else 10,
) -> int:
    run_dir = resolve_run_dir(args.run_id, args.outdir, scenario)

    payload = dict(vars(args))
    payload.pop("func", None)
    payload.update(
        {
            "scenario": f"{handler_base}.verify",
            "scope_id": scope_id,
            "run_id": str(args.run_id or run_dir.name),
            "outdir": str(run_dir),
        }
    )

    return _invoke_scenario(handler_name=f"{handler_base}.verify", payload=payload, fallback_exit_code=fallback_exit_code)


def cmd_labs_export(
    args: argparse.Namespace,
    *,
    scope_id: str,
    scenario: str,
    handler_base: str,
    resolve_run_dir: Callable[[str | None, str | None, str], Path] = _resolve_run_dir,
    fallback_exit_code: int | Callable[[bool], int] = 0,
) -> int:
    run_dir = resolve_run_dir(args.run_id, args.outdir, scenario)

    payload = dict(vars(args))
    payload.pop("func", None)
    payload.update(
        {
            "scenario": f"{handler_base}.export",
            "scope_id": scope_id,
            "run_id": str(args.run_id or run_dir.name),
            "outdir": str(run_dir),
        }
    )

    return _invoke_scenario(handler_name=f"{handler_base}.export", payload=payload, fallback_exit_code=fallback_exit_code)


def cmd_labs_clean(
    args: argparse.Namespace,
    *,
    scope_id: str,
    handler_base: str,
    now_run_id: Callable[[], str] = _labs_shared.now_run_id,
    fallback_exit_code: int | Callable[[bool], int] = 0,
) -> int:
    payload = dict(vars(args))
    payload.pop("func", None)
    payload.update(
        {
            "scenario": f"{handler_base}.clean",
            "scope_id": scope_id,
            "run_id": now_run_id(),
            "outdir": str(args.outdir) if args.outdir else None,
        }
    )

    return _invoke_scenario(handler_name=f"{handler_base}.clean", payload=payload, fallback_exit_code=fallback_exit_code)
