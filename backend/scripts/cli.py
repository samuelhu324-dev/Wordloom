"""Minimal script router for backend/scripts.

Design goals:
- Keep it tiny and dependency-free.
- Provide a stable command namespace so people stop memorizing file names.
- Enforce consistent snapshot output locations for labs.

This is intentionally not a full-featured CLI framework.
"""

from __future__ import annotations
# 在 cli.py 顶部加（或 main 里局部 import 也行）
# 注意：cli.py 以脚本方式运行（python backend/scripts/cli.py）时，sys.path[0] 是 backend/scripts。
# 因此应从同级包 cli_app 导入，而不是 backend.scripts.cli_app。
from collections.abc import Callable

from cli_app import registry as _wg_registry
from cli_app.callbacks import build_callbacks as _build_callbacks
from cli_app.common import build_evidence_paths, build_evidence_paths_for_dir, pack_artifacts
from cli_app.parser import build_parser as _build_parser
from cli_app.types import DrillInputs

import argparse
from pathlib import Path


def _build_argparse_callbacks() -> dict[str, Callable[[argparse.Namespace], int]]:
    return _build_callbacks()


def build_parser() -> argparse.ArgumentParser:
    return _build_parser(callbacks=_build_argparse_callbacks())


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # 1) 确保内置 scenarios 被 import 并注册
    _wg_registry.load_builtin_scenarios()

    # 2) 识别 scenario：统一兼容 write_gate_scenario / scenario + _ / - 命名风格
    raw_scenario = getattr(args, "write_gate_scenario", None) or getattr(args, "scenario", None)
    scenario: str | None = None
    scenario_candidates: list[str] = []
    if isinstance(raw_scenario, str) and raw_scenario.strip():
        scenario = raw_scenario.strip()
        scenario_candidates.append(scenario)
        if "-" in scenario:
            scenario_candidates.append(scenario.replace("-", "_"))
        if "_" in scenario:
            scenario_candidates.append(scenario.replace("_", "-"))

    # 去重并保持顺序
    seen: set[str] = set()
    scenario_candidates = [s for s in scenario_candidates if not (s in seen or seen.add(s))]

    # 3) 只要匹配到“新架构的 scenario”，就抢先执行并退出（不走 args.func）
    if scenario_candidates:
        handler = None
        matched_scenario: str | None = None
        for candidate in scenario_candidates:
            try:
                handler = _wg_registry.get(candidate)
                matched_scenario = candidate
                break
            except KeyError:
                continue

        if handler is not None:
            scenario = matched_scenario or scenario_candidates[0]
            scope_id = getattr(args, "scope_id", None) or "S2B"
            run_id = getattr(args, "run_id", None) or "local"

            # pydantic 输入边界：自动透传 argparse 字段（extra=allow）
            input_payload = {k: v for k, v in vars(args).items() if k not in {"func"}}
            input_payload.update(
                {
                    "scenario": scenario,
                    "scope_id": scope_id,
                    "run_id": run_id,
                    "timeout_s": getattr(args, "timeout_s", None),
                    "sampling": getattr(args, "sampling", None),
                }
            )
            inputs = DrillInputs.model_validate(input_payload)

            result = handler(inputs)

            # 4) 按你的证据 contract 落盘：_result.json + summary.json（先做最小闭环）
            outdir_arg = getattr(args, "outdir", None)
            if outdir_arg:
                paths = build_evidence_paths_for_dir(Path(str(outdir_arg)))
            else:
                paths = build_evidence_paths(scope_id=inputs.scope_id, scenario=inputs.scenario, run_id=inputs.run_id)

            # Keep legacy evidence structure: _result.json is the scenario's meta dict.
            pack_artifacts(
                paths=paths,
                result=result.meta,
                summary=result.summary,
                zip_when="on_failure",
                zip_path=paths.snapshot_dir / "evidence.zip",
            )

            return 0 if result.ok else 2

    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
