# Log-S0C-3A-3A: dispatch-only + argparse extraction

---

**id**: `S0C-3A-3A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `cli thinning: dispatch-only + argparse extraction`
**status**: `draft`           # draft | stable | archived
**scope**: `S0C`
**tags**: `EVOLOTION, Docs, Tools, CLI, lab, sub/1`
**links**: ``
  **issue**: `#83, #66`
  **pr**: `null`
  **adr**: ``
  **runbook**: `null`
**created**: `2026-02-22`
**updated**: `2026-02-22`

---

## Decision / Outcome（结论区）

- 目标：将 `backend/scripts/cli.py` 进一步收敛为 **dispatch-only 薄入口**，并将 argparse 解析与命令定义抽离到 `backend/scripts/cli_app/`；入口文件行数 **~100–300** 作为目标线（非硬性门槛）。
- 验收口径：以 **dispatch-only + 行为/合约稳定** 为准（命令/参数/help/exit code/evidence contract 不漂移），而不是“卡行数”。
- 不可破坏约束：
  - CLI 对外行为不变（子命令路径、参数名、help、exit code 语义）。
  - CI/workflow 依赖不变（命令名、输入参数、产物路径/文件名/关键字段结构）。
- 与 S0C-3A-2A 边界：
  - 2A 负责 **artifacts contract + packing 单点化**（`cli_app/common.py` + workflow shared script）。
  - 3A 负责 **CLI 结构拆分**（dispatch-only + argparse extraction + 场景搬迁），减少 `cli.py` 体积与上下文压力。

## Background

- `backend/scripts/cli.py` 长期演进为超大入口文件（数千行），导致工具/Agent 容易拉取大量上下文并出现超时（例如 408）。
- 现已具备拆分前提：
  - 场景注册/分发机制（registry + handlers）已存在。
  - 证据产物 contract/packing 已在 2A 阶段单点化（`cli_app/common.py::pack_artifacts()`）。

## Problem / Constraints（问题与约束）

- CLI 入口同时承担：argparse 定义、业务逻辑、legacy wrapper、证据产物落盘等多种职责。
- 迁移必须保持对外兼容：
  - 不改变命令名与参数（除非同步更新所有调用方）。
  - 不改变 exit code 语义。
  - 不改变 evidence/outdir 计算与默认行为。

## Approach（落地方式）

### Step A：dispatch-only（入口只分发）

- 将 `cli.py` 中已存在或可迁移的命令实现，逐步改为：
  - `cli.py` 仅做：解析 → 选择 scenario/command → 调用 handler → 统一 exit code。
  - 业务逻辑放入 `backend/scripts/cli_app/scenarios/*`。

### Step B：argparse extraction（参数定义抽离）

- 将 `build_parser()` 与子命令定义从 `cli.py` 抽离到：
  - `backend/scripts/cli_app/parser.py`（建议）或同级模块。
- `cli.py` 只保留：
  - `main(argv)`
  - 调用 `cli_app.parser.build_parser()`
  - registry 分发与 `pack_artifacts(...)`（写盘由 2A 保障）

### Step C：legacy wrappers 最小化

- 对必须保留的 legacy wrapper：
  - 入口只保留“命令别名/兼容层”与最小参数桥接。
  - 逐步将其拆分到 `backend/scripts/legacy/`（或 `cli_app/legacy_shims.py`）并保持可控范围。

## Verification（验证方式）

- 每一批命令迁移：
  - `--help` 对比（命令/参数/描述）。
  - smoke run（ok 与 not ok 各一条更好）。
  - exit code 对齐（0/2 等语义不变）。
  - `_result.json` 路径/字段/编码/换行不变（由 2A contract 保障）。

## Evidence（本阶段实证 / 运行证据）

### 2026-02-22 — Step B first cut: `build_parser()` extracted

- change:
  - added `backend/scripts/cli_app/parser.py::build_parser(callbacks=...)`
  - `backend/scripts/cli.py` now delegates `build_parser()` to `cli_app.parser.build_parser` via injected callbacks (avoid circular imports)
  - legacy in-file parser removed（parser 单一事实来源）
  - moved `labs export-jaeger` 实现到 `backend/scripts/cli_app/labs/jaeger_export.py`，`cli.py` 保留同名薄 wrapper（回调名不变）
- smoke:
  - command: `python backend/scripts/cli.py --help`
  - result: help renders successfully (argparse wiring OK)
  - command: `python backend/scripts/cli.py labs export-jaeger --help`
  - result: subcommand help renders successfully（回调注入 OK）
  - notes: 下一步继续搬迁 `_cmd_*` 簇，让 `cli.py` 进一步变薄

### 2026-02-22 — Step A incremental: `collector_down` cmd cluster delegated

- change:
  - added `backend/scripts/cli_app/labs/collector_down.py`
  - `backend/scripts/cli.py` now delegates these commands to `cli_app` while keeping callback names stable:
    - `labs run collector_down`
    - `labs verify collector_down`
    - `labs export collector_down`
    - `labs clean collector_down`
- smoke:
  - command: `python backend/scripts/cli.py labs run collector_down --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs export collector_down --help`
  - result: help renders successfully

### 2026-02-22 — Step A batch: failure drills scenarios delegated via shared helper

- change:
  - added `backend/scripts/cli_app/labs/failure_drills.py` as shared implementation for `labs run|verify|export|clean <scenario>`
  - `backend/scripts/cli.py` kept all original callback function names, but implementations for the remaining failure-drill scenarios now delegate to `cli_app`:
    - `es_write_block_4xx`
    - `es_429_inject`
    - `es_down_connect`
    - `es_bulk_partial`
    - `db_claim_contention`
    - `stuck_reclaim`
    - `duplicate_delivery`
    - `projection_version` (verify/export fallback exit-code preserved: `ok ? 0 : 2`)
- smoke:
  - command: `python backend/scripts/cli.py labs run es_write_block_4xx --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs clean es_429_inject --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs verify db_claim_contention --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs verify projection_version --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs export projection_version --help`
  - result: help renders successfully

### 2026-02-22 — GitHub Actions evidence: `failure-drills` workflow (success + failure)

- collector_down (success):
  - workflow: `failure-drills.yml` (workflow_dispatch)
  - run: `failure-drills #18`
  - status: `success`
  - duration: `1m 43s`
  - artifacts: `1`
- es_429_inject (failure):
  - workflow: `failure-drills.yml` (workflow_dispatch)
  - run: `failure-drills #17`
  - status: `failure`
  - duration: `1m 38s`
  - artifacts: `1`
- es_429_inject (success):
  - workflow: `failure-drills.yml` (workflow_dispatch)
  - run: `failure-drills #16`
  - status: `success`
  - duration: `1m 41s`
  - artifacts: `1`

### 2026-02-22 — Step A batch: `shadow_verify_*` cmd cluster delegated

- change:
  - added `backend/scripts/cli_app/labs/shadow_verify.py` as the shared implementation module
  - `backend/scripts/cli.py` now delegates the full `shadow_verify_*` cluster to `cli_app` while keeping callback names stable:
    - `labs shadow-verify-chronicle-entries`
    - `labs shadow-verify-search-index`
    - `labs shadow-verify-search-index-write-gate`
    - `labs shadow-verify-search-index-paging-stability`
    - `labs shadow-verify-shared-keys`
    - `labs shadow-verify-dual-run-readiness-gate`
    - `labs shadow-verify-dual-run-stage1`
    - `labs shadow-verify-dual-run-stage2`
    - `labs shadow-verify-dual-run-window`
    - `labs shadow-verify-canary-dual-write`
    - `labs shadow-verify-dual-write-sampling`
  - size impact: `backend/scripts/cli.py` reduced from ~2386 lines → 1130 lines
- smoke:
  - command: `python backend/scripts/cli.py labs shadow-verify-search-index --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs shadow-verify-dual-run-stage1 --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs shadow-verify-dual-write-sampling --help`
  - result: help renders successfully

### 2026-02-22 — GitHub Actions evidence: `drill-shadow-verify-entries` workflow (success)

- workflow: `.github/workflows/drill-shadow-verify-entries.yml` (workflow_dispatch)
- run_url: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22273760746
- scenario: `shadow_verify_search_index`
- status: `success`
- duration: `46s`
- artifacts: `1`
- summary.json (key fields):
  - run_id: `22273760746-1`
  - scope: `all`
  - ok: `true`

### 2026-02-22 — Step A incremental: `expb-es429` cmd delegated

- change:
  - added `backend/scripts/cli_app/labs/expb_es429.py`
  - `backend/scripts/cli.py` now delegates `labs expb-es429` to `cli_app` (callback name stable: `_cmd_labs_expb_es429`)
- smoke:
  - command: `python backend/scripts/cli.py labs expb-es429 --help`
  - result: help renders successfully

### 2026-02-22 — Step C incremental: legacy runtime glue extracted (thin wrappers)

- change:
  - added `backend/scripts/cli_app/runtime.py` to centralize legacy subprocess + path glue:
    - `python_exe()`
    - `run(...)`
    - `with_backend_pythonpath(...)`
    - `REPO_ROOT` / `LEGACY_SCRIPTS_DIR`
  - updated `backend/scripts/cli_app/labs/jaeger_export.py` and `expb_es429.py` to default to `cli_app.runtime` (keeps existing override hooks)
  - `backend/scripts/cli.py` removed in-file legacy helpers (`_python_exe/_run/_with_backend_pythonpath`) and simplified wrappers for:
    - `labs export-jaeger`
    - `labs expb-es429`
- smoke:
  - command: `python backend/scripts/cli.py --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs export-jaeger --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs expb-es429 --help`
  - result: help renders successfully

### 2026-02-22 — Step A incremental: failure_drills wrappers thinned (reuse shared utils)

- change:
  - `backend/scripts/cli.py` now reuses `backend/scripts/cli_app/scenarios/_failure_drill_shared.py` for:
    - default outdir (`default_labs_auto_run_dir`)
    - run-dir resolution (`resolve_run_dir`)
  - removed now-unused legacy helper functions from `cli.py` (HTTP/ES/Prom/metrics parsing utilities that are already available under `_failure_drill_shared`)
  - reduced per-command wrapper noise (no more per-wrapper lambdas for outdir/resolve)
  - size impact: `backend/scripts/cli.py` reduced from ~996 lines → 826 lines
- smoke:
  - command: `python backend/scripts/cli.py labs run es_429_inject --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs verify es_429_inject --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs export es_429_inject --help`
  - result: help renders successfully

### 2026-02-22 — Step A incremental: shadow_verify wrappers de-injected (defaults moved to cli_app)

- change:
  - added `backend/scripts/cli_app/labs/shared.py` to host shared labs defaults:
    - `now_run_id()`
    - default outdir under `docs/labs/_snapshot/auto/<lab_id>/<scenario>/<run_id>`
    - `.env` loading helper used by labs
  - updated `backend/scripts/cli_app/labs/shadow_verify.py` so all `cmd_labs_shadow_verify_*` functions have defaults wired to `cli_app.labs.shared` (entrypoint no longer injects helpers)
  - updated `backend/scripts/cli.py` to remove per-wrapper injection of:
    - `now_run_id`
    - `default_outdir`
    - `ensure_dir`
    - `load_env`
  - removed now-unused entrypoint helper: `_default_s2b_auto_run_dir`
  - size impact: `backend/scripts/cli.py` reduced from 826 lines → 753 lines
- smoke:
  - command: `python backend/scripts/cli.py --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs shadow-verify-search-index --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs shadow-verify-dual-run-stage2 --help`
  - result: help renders successfully

### 2026-02-22 — Step C incremental: export-jaeger / expb-es429 wrappers de-injected

- change:
  - updated `backend/scripts/cli_app/labs/shared.py` to include `default_labs009_expb_outdir(run_id)`
  - updated `backend/scripts/cli_app/labs/jaeger_export.py::cmd_labs_export_jaeger(...)` to default `default_outdir/now_run_id/ensure_dir` to `cli_app.labs.shared`
  - updated `backend/scripts/cli_app/labs/expb_es429.py::cmd_labs_expb_es429(...)` to default `default_outdir/now_run_id/ensure_dir` to `cli_app.labs.shared`
  - updated `backend/scripts/cli.py` wrappers to stop injecting those helpers; removed now-unused entrypoint helper `_default_labs009_expb_outdir` (and `LABS_SNAPSHOT_ROOT`)
  - size impact: `backend/scripts/cli.py` reduced from 753 lines → 738 lines
- smoke:
  - command: `python backend/scripts/cli.py labs export-jaeger --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs expb-es429 --help`
  - result: help renders successfully

### 2026-02-22 — Step A/C incremental: failure_drills + collector_down wrappers de-injected (defaults moved to cli_app)

- change:
  - updated `backend/scripts/cli_app/labs/failure_drills.py` to provide defaults for:
    - `now_run_id` (via `cli_app.labs.shared.now_run_id`)
    - `default_outdir` / `resolve_run_dir` (via `cli_app.scenarios._failure_drill_shared` adapters)
  - updated `backend/scripts/cli_app/labs/collector_down.py` similarly
  - updated `backend/scripts/cli.py` to stop injecting `now_run_id/default_outdir/resolve_run_dir` across these wrappers; removed now-unused in-file helpers/imports
  - size impact: `backend/scripts/cli.py` reduced from 738 lines → 665 lines
- smoke:
  - command: `python backend/scripts/cli.py --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs run es_429_inject --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs run collector_down --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs verify projection_version --help`
  - result: help renders successfully

### 2026-02-22 — Step C incremental: bulk wrapper boilerplate collapsed via `partial(...)`

- change:
  - updated `backend/scripts/cli.py` to replace many repetitive `_cmd_labs_*` wrapper functions with `functools.partial(...)` callables
  - callback names stay stable (argparse continues to resolve by the same string keys)
  - size impact: `backend/scripts/cli.py` reduced from 665 lines → 514 lines
- smoke:
  - command: `python backend/scripts/cli.py --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs run es_429_inject --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs verify db_claim_contention --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs export stuck_reclaim --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs run collector_down --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs shadow-verify-shared-keys --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs export-jaeger --help`
  - result: help renders successfully

### 2026-02-22 — Step C incremental: callback mapping auto-discovery (remove static name list)

- change:
  - updated `backend/scripts/cli.py::_build_argparse_callbacks()` to auto-discover callback keys by convention:
    - include: names starting with `_cmd_labs_`
    - exclude: imported implementation callables ending with `_impl`
  - keeps callback keys unchanged (argparse continues to resolve by the same string keys), while removing the long `names=[...]` boilerplate
  - size impact: `backend/scripts/cli.py` reduced from 514 lines → 475 lines
- smoke:
  - command: `python backend/scripts/cli.py --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs run es_429_inject --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs verify db_claim_contention --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs export stuck_reclaim --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs run collector_down --help`
  - result: help renders successfully

### 2026-02-22 — Step A/C: callback glue extracted to `cli_app/callbacks.py` (entrypoint shrink)

- change:
  - added `backend/scripts/cli_app/callbacks.py::build_callbacks()` to centralize all `_cmd_labs_*` callback wiring (partials/constants/imports)
  - updated `backend/scripts/cli.py` to delegate callback construction to `cli_app.callbacks.build_callbacks`, removing the large in-file callback block
  - size impact: `backend/scripts/cli.py` reduced from 475 lines → 112 lines
- smoke:
  - command: `python backend/scripts/cli.py --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs run es_429_inject --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs verify db_claim_contention --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs export stuck_reclaim --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs run collector_down --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs shadow-verify-shared-keys --help`
  - result: help renders successfully
  - command: `python backend/scripts/cli.py labs export-jaeger --help`
  - result: help renders successfully

### Template

- artifact: `_result.json` / `summary.json` / `*.zip`
- command/scenario:
- run_id:
- result: `ok=true|false`
- notes: help diff / exit code / contract checks

## Risks（风险与缓解）

- 风险：argparse 抽离导致参数默认值或 help 文案轻微漂移。
  - 缓解：将 help diff 纳入每次迁移的验证清单；必要时保留 compatibility shim。
- 风险：入口变薄过程中误改 outdir 计算或 workflow 依赖路径。
  - 缓解：优先迁移 CI 强依赖命令；每次变更前先从 workflow 找调用点做回归。

## Next

- 盘点：列出 `cli.py` 中“可直接映射到现有 scenarios”的命令清单，优先迁移这批。
- 盘点：列出 `cli.py` 中可继续“整簇搬迁”的 `_cmd_*`（例如 `duplicate_delivery` / `stuck_reclaim` / `db_claim_contention` 四连）。
- 迁移：优先搬迁 workflow/CI 依赖最强、且实现最自洽的命令簇，保持 argparse/exit code/contract 不变。
- 收口：抽取 `cli.py` 里通用的 `run/verify/export/clean` 调用模板到 `cli_app`（减少重复、进一步变薄入口）。
- 目标态：`cli.py` 最终仅保留 `main()` + 最小桥接层（~100–300 行）。
