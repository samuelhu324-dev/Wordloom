# Log-S0C-3A-2A: convergence/artifacts contract / packing

---

**id**: `S0C-3A-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `convergence/artifacts contract packing`
**status**: `draft`           # draft | stable | archived
**scope**: `S0C`
**tags**: `EVOLOTION, Docs, Projection, Search, chronicle, lab, sub/1`
**links**: ``
  **issue**: `#86, #84, #83`
  **pr**: `null`
  **adr**: ``
  **runbook**: `null`
**created**: `2026-02-21`
**updated**: `2026-02-22`

---

## Decision / Outcome（结论区）

- 本阶段目标（Step A-C）：把所有 drill / lab 子命令的证据产物（artifacts）落盘与打包逻辑，收敛为 **一套可复用的 artifacts contract + packing 实现**，并逐步替换入口侧零散写盘/打包代码。
- 约束：
  - CLI 对外行为不变（子命令路径、参数名、help、exit code 语义）。
  - CI / workflow 依赖的产物契约不变（路径、文件名、关键字段结构）。
  - 允许新增字段与辅助文件；不允许删除/改名已有关键字段或改变落盘路径（除非同步更新所有依赖方）。

## Background

- 目前 `backend/scripts/cli.py` 仍承载了不少“写文件/打包 zip/生成 summary”的重复代码：
  - 难以做到每个场景严格一致（缩进、编码、换行、字段名、错误结构、zip 包含内容）。
  - 迁移/收口时需要重复搬运这些写盘细节，增加回归风险。
- 已经存在 `backend/scripts/cli_app/common.py`（基础能力：JSON 写盘、zip 打包等），但尚未把“contract + packing”提升为统一入口。

## Problem / Constraints（问题与约束）

- 不可破坏的 contract（典型）：
  - 结果文件：`_result.json`（被 workflow / 人工排障用作单一真相来源）。
  - 打包：失败时 zip（或某些聚合场景固定 zip）作为 evidence bundle。
  - 目录：outdir（通常按 `scope_id/scenario/run_id` 组织，或 workflow 指定 `.drill_snapshot/...`）。
- 环境差异：本地与 GitHub Actions、不同 OS（Windows/WSL2）路径与权限差异，需要 contract 足够稳健。

## Contract Definition（产物契约定义）

> 本小节不新增“新格式”，而是把已有惯例显式化，便于逐步统一实现。

### 1) 必选：`_result.json`

- 位置：`<outdir>/_result.json`
- 编码：UTF-8
- 内容：JSON object（dict）
- 最小建议字段（不同场景允许扩展）：
  - `lab_id`（string）
  - `scenario`（string）
  - `run_id`（string）
  - `created_at`（string，便于人工读）
  - `ok`（bool）
- 允许场景自定义字段（counts、checks、paths、meta 等）。

### 2) 可选：`summary.json`

- 位置：通常由 workflow 从 `_result.json` 派生；若 CLI 已落盘 `summary.json`，则必须保持字段与依赖方兼容。

### 3) 可选：zip evidence bundle

- 触发条件（两类都允许存在）：
  - 失败时打包（便于 CI artifacts 一键收集）
  - 聚合场景固定打包（例如 readiness / gate 类把子检查结果一起打包）
- 内容建议：整个 outdir（含 `_result.json`、子检查目录、日志/trace 等）
- 文件名：保持既有命名规则（如已有）

## Approach（落地方式）

### Step A：抽离 artifacts contract + packing（统一入口）

- 在 `cli_app/common.py`（或同级新模块，若必须）形成“一个入口函数/小集合 API”，覆盖：
  - 写 `_result.json`（统一编码/缩进/末尾换行规则）
  - 需要时写 `summary.json`（若当前就有）
  - 需要时 zip 打包 outdir（可配置：失败打包/总是打包/从不打包）
- 输出：对调用方只暴露稳定函数签名，避免每个命令重复拼装。

### Update — Step A 已落地（2026-02-22）

- 已在 `backend/scripts/cli_app/common.py` 落地统一 packing API：
  - `pack_artifacts(paths, result, summary=None, logs_text=None, traces=None, zip_when='never|on_failure|always', zip_path=None)`
  - 固化 `_result.json` 写盘细节：UTF-8 / pretty JSON / 末尾换行
  - 可选写 `artifacts/summary.json`、`artifacts/logs.txt`、`artifacts/traces.json`
  - zip 采用“调用方显式提供 `zip_path`”策略，避免改变既有命名/路径约定

### Step B：逐命令切换到统一 packing（保持对外不变）

- 每切换一个命令：
  - 保持现有 outdir 计算方式与路径不变
  - 保持 `_result.json` 的结构与关键字段不变
  - 只替换“写盘/打包”的实现路径（改为调用 common packing）
- 优先级：从 CI/workflow 依赖最强、产物最复杂的命令开始（最能暴露 contract 问题）：
  - 聚合/打包类场景（readiness gate 类）
  - failure-drills 的 export/打包类命令

### Update — Step B 起步：readiness gate（2026-02-22）

- 已从 readiness gate 聚合场景开始，先收敛其“子检查结果写盘”的 contract：
  - 文件：`backend/scripts/cli_app/scenarios/shadow_verify_dual_run_readiness_gate.py`
  - 改动：对子检查 `<outdir>/_checks/<scenario>/_result.json` 的写盘，从零散 `write_json(...)` 改为统一 `common.pack_artifacts(...)`
- 契约保持不变：
  - 子检查结果仍落在原路径（`_checks/.../_result.json`），字段结构来自各 child scenario 的 `meta`，未做改名/删字段
  - readiness gate 主 `_result.json` 仍由外层 shim 写入（本阶段不改主写盘路径/时机，避免影响 workflow）

### Update — Step B 扩面：failure-drills verify（2026-02-22）

- 以 CI 依赖优先（workflow: `failure-drills.yml`）扩面：将 failure-drills 的 9 个场景在 `verify` 阶段写入 `<run_dir>/_result.json` 的实现，统一切到 `common.pack_artifacts(...)`：
  - `es_429_inject`
  - `es_write_block_4xx`
  - `es_down_connect`
  - `collector_down`
  - `es_bulk_partial`
  - `db_claim_contention`
  - `stuck_reclaim`
  - `duplicate_delivery`
  - `projection_version`
- 契约保持不变：仍写入原路径 `_result.json`（UTF-8 / pretty JSON / 末尾换行），仅收敛写盘实现，便于后续统一演进。

### Step C：删除 legacy packing 分支（入口真正变薄）

- 当 Step B 覆盖率足够：
  - 删除 `cli.py` 中零散的写盘/打包实现块
  - 将“证据产物的变化”收敛为：只改 `cli_app/common.py`，避免多点漂移

## Verification（验证方式）

- 每完成一个命令的 packing 切换：
  - 本地跑一次（ok 与 not ok 各一条更好）
  - 核对 `_result.json`：字段/路径/编码/换行
  - 若涉及 zip：核对 zip 内包含文件集合与相对路径

## Evidence（本阶段实证 / 运行证据）

> 目的：证明 packing 抽离后不破坏 contract，并能被 workflow 正常消费。

### Template

- artifact: `_result.json` / `summary.json` / `*.zip`
- scenario:
- run_id:
- result: `ok=true|false`
- notes: contract checks（路径/字段/zip 内容）

## Risks（风险与缓解）

- 风险：统一 packing 时不小心改变了 JSON 序列化细节（缩进、ensure_ascii、末尾换行）导致工具链解析差异。
  - 缓解：以现有 `_result.json` 为基线，做“字节级”对齐（至少结构/字段对齐，必要时对齐格式）。
- 风险：zip 内容或路径变化导致 Actions 收集不到 artifacts。
  - 缓解：优先从 workflow 依赖最强的场景开始迁移，并对 zip 内容做明确清单校验。

## Next

- 先落地 Step A：定义并固化 packing API（不改任何业务逻辑）。
- 然后挑 1 个“打包最复杂且 CI 依赖”的命令做 Step B 的样板迁移。
- 形成样板后再批量推进其余命令。
