# Log-S0C-3A-2A: convergence/artifacts contract / packing

---

**id**: `S0C-3A-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `convergence/artifacts contract packing`
**status**: `stable`           # draft | stable | archived
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

### Update — Step B 补齐：stuck_reclaim.verify（2026-02-22）

- 发现并修复 `stuck_reclaim.verify` 场景内仍存在的“直接写 `_result.json`”点：
  - 从 `(run_dir / "_result.json").write_text(json.dumps(...))` 改为 `common.pack_artifacts(paths=build_evidence_paths_for_dir(run_dir), result=...)`
- 契约保持不变：仍写入 `<run_dir>/_result.json`，仅统一写盘实现。

### Update — Step B 扩面：统一 ancillary JSON 写盘（2026-02-22）

- 在 failure-drills 相关场景中，将 `_recipe.json` / `_worker_exit.json` / `_ports.json` / `_run.json` 等“辅助 JSON 文件”的写盘，从 `Path.write_text(json.dumps(...))` 收敛为 `common.write_json(...)`：
  - 保持文件名/路径与字段结构不变
  - 统一 UTF-8 / pretty JSON / 末尾换行 / 确保父目录存在
- 目的：进一步减少入口/场景内部多点手写 JSON 的漂移风险，为 Step C 删除 legacy packing 分支做准备。

### Update — Step B 收口：standalone labs scripts 写盘收敛（2026-02-22）

- 发现 `backend/scripts/labs/` 下仍存在少量脚本直接写 `<OUTDIR>/_result.json`：
  - `lab-S2B-1A-1A.py`
  - `lab-S2B-1A-2A.py`
  - `lab-S2B-2A-1A.py`
- 改动：将写盘从 `Path.write_text(json.dumps(...)+"\n")` 收敛为复用 `cli_app/common.write_json(...)`（UTF-8 / pretty JSON / 末尾换行一致）。
- 说明：这些脚本不是 `cli_app` handler，但其产物契约同样是 `_result.json`；因此纳入 Step B 的“写盘实现收敛”范围。

### Update — Step B 扫描：drill-write-gate workflow（2026-02-22）

- 以 CI 依赖优先（workflow: `drill-write-gate.yml`）扫描其直接调用的场景实现：
  - 除 readiness gate 的子检查（已在上一个 Update 中落地）外，未发现其它场景在 handler 内部直接写入 `<outdir>/_result.json` 或进行 zip 打包。
  - 结论：该 workflow 的主 `_result.json` 仍主要由外层 shim 负责写盘（尊重 `--outdir .drill_snapshot` 约束），Step B 下一轮扩面应优先寻找“聚合/子检查/导出”类命令中分散的写盘/打包点。

  ### Update — Step B 扩面：workflow 侧收敛 summary + zip（2026-02-22）

  - 动机：workflow 内联的 `python -c ...`（summary 兜底 / `_result.json` 缺失兜底）与 `zipfile.ZipFile`（失败时打包）属于“contract/packing 的另一套实现”，会造成多点漂移；因此也纳入 Step B 的“CI 依赖优先”收敛范围。
  - 落地方式：新增仓内共享脚本，将 workflow 的重复实现单点化，并复用 `cli_app/common.py` 的写盘与 zip 能力：
    - 文件：`backend/scripts/ci/workflow_artifacts.py`
    - 子命令：
      - `placeholder`：生成占位 `artifacts/summary.json`（防止脚本中途崩溃导致下游 step 读不到 summary）
      - `finalize`：
        - 若存在 `.drill_snapshot/_result.json`，则复制到 `artifacts/summary.json`
        - 若缺失 `.drill_snapshot/_result.json`，则生成最小兜底 JSON，同时写入 `.drill_snapshot/_result.json` 与 `artifacts/summary.json`
        - best-effort 复制 `.drill_snapshot/traces.json` → `artifacts/traces.json`（不存在则写 `[]` 占位）
        - best-effort 复制 `.drill_snapshot/backfill.log` / `.drill_snapshot/worker.log` → `artifacts/`
      - `zip`：将 `artifacts/` 目录打包为 `artifacts.zip`
  - 影响范围：
    - `.github/workflows/drill-write-gate.yml`
    - `.github/workflows/drill-shadow-verify-entries.yml`
  - 契约保持不变：
    - `artifacts/summary.json` 仍是 workflow 上传的 success-only summary
    - failure-only 仍上传 `artifacts.zip`
    - `.drill_snapshot/_result.json` 仍作为“单一真相来源”供 snapshot/evidence 链路消费（缺失时兜底补写）

### Step C：删除 legacy packing 分支（入口真正变薄）

- 当 Step B 覆盖率足够：
  - 删除 `cli.py` 中零散的写盘/打包实现块
  - 将“证据产物的变化”收敛为：只改 `cli_app/common.py`，避免多点漂移

### Update — Step C 落地：cli.py 分发路径 packing 单点化（2026-02-22）

- 目标：删除/合并 `backend/scripts/cli.py` 中“新架构 scenario 分发路径”的内联 packing（`_result.json` / `artifacts/summary.json` / failure-only `evidence.zip`），改为单点复用 `backend/scripts/cli_app/common.py::pack_artifacts()`。
- 改动：
  - `cli.py` 在命中新架构 scenario handler 后，调用 `pack_artifacts(paths=..., result=result.meta, summary=result.summary, zip_when='on_failure', zip_path='<snapshot_dir>/evidence.zip')`。
  - 结果：入口侧不再直接维护 summary/zip 的实现细节；contract 变更只需在 `common.py` 单点调整。
- 契约保持不变：
  - `<outdir>/_result.json` 仍为“单一真相来源”（UTF-8/pretty/newline）
  - summary 仍写入 `<outdir>/artifacts/summary.json`
  - failure-only 时仍打包 `<outdir>/evidence.zip`（zip 根为 `<outdir>`，相对路径不变）
- 验证：VS Code Problems 对 `backend/scripts/cli.py`、`backend/scripts/cli_app/common.py`、`backend/scripts/ci/workflow_artifacts.py` 均为 `No errors found`。

### Update — Step C 收口：cli.py 入口侧 _result.json 写盘单点化（2026-02-22）

- 背景：`cli.py` 中仍存在多处 `write_json(outdir / "_result.json", ...)` 的重复落盘点（属于入口侧“零散 packing”）。
- 改动：将这些落盘点统一替换为 `common.pack_artifacts(paths=build_evidence_paths_for_dir(outdir), result=...)`。
- 结果：`cli.py` 不再直接写 `_result.json`；所有证据产物写盘细节统一由 `cli_app/common.py` 单点维护。
- 契约保持不变：仍仅写 `<outdir>/_result.json`（不新增 summary/zip），字段结构来自各场景 `meta`。

## Verification（验证方式）

- 每完成一个命令的 packing 切换：
  - 本地跑一次（ok 与 not ok 各一条更好）
  - 核对 `_result.json`：字段/路径/编码/换行
  - 若涉及 zip：核对 zip 内包含文件集合与相对路径

## Evidence（本阶段实证 / 运行证据）

> 目的：证明 packing 抽离后不破坏 contract，并能被 workflow 正常消费。

### CI Evidence — GitHub Actions（2026-02-22）

- workflow: `failure-drills.yml`
- artifact: `labs-evidence-<scenario>-<GITHUB_RUN_ID>-<GITHUB_RUN_ATTEMPT>`（来自 `docs/labs/_snapshot/auto/`）
- scenario: `failure-drills`（matrix=9 scenarios）
- success run（截图2）：
  - run_id: `22270016158-1`
  - run_url: https://github.com/samuelhu324-dev/Wordloom/actions/runs/22270016158
  - result: `ok=true`（9 jobs 全绿，artifacts=9）
- forced failure run（截图1，`force_failure=true`）：
  - run_id: `22270015344-1`
  - run_url: https://github.com/samuelhu324-dev/Wordloom/actions/runs/22270015344
  - result: `ok=false`（9 jobs 全红）
  - notes: 失败注入发生在 evidence 上传前；`Upload evidence bundle` 采用 `if: always()`，因此即使 job fail 也仍会产出/上传 evidence artifact（用于 failure-only 证据截图）。

### CI Evidence — workflow 侧收敛推广（2026-02-22）

- workflow:
  - `drill-write-gate.yml`
  - `drill-shadow-verify-entries.yml`
- change: 将 workflow 内联的“summary 兜底 + finalize + failure-only zip”收敛为仓内脚本 `backend/scripts/ci/workflow_artifacts.py`（`placeholder/finalize/zip`）
- artifacts contract（保持不变）：
  - success-only：上传 `artifacts/summary.json`
  - failure-only：打包并上传 `artifacts.zip`

### Local Evidence — smoke test（2026-02-22）

- artifact: `backend/scripts/ci/workflow_artifacts.py`
- scenario: `placeholder/finalize/zip`
- run_id: `local/.tmp_workflow_artifacts`
- result: `ok=true`（生成 `artifacts/summary.json`、`artifacts/traces.json`、缺失时补写 `.drill_snapshot/_result.json`、并成功生成 `artifacts.zip`）
- notes: 证明 workflow shared script 在“_result.json 缺失/存在”的基本分支上可用，并可替代 YAML 内联 python/zipfile 实现。

### Local Evidence — Step C compile check（2026-02-22）

- command: `python -m py_compile backend/scripts/cli.py backend/scripts/cli_app/common.py backend/scripts/ci/workflow_artifacts.py`
- result: `exit_code=0`

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

- Step B：已收口完成（非 legacy 路径的 `_result.json`/aux JSON 写盘与 workflow 侧打包/兜底已收敛；残留仅存在于 `backend/scripts/legacy/`）。
- Step C：已收口完成（入口侧 packing 细节已单点化；后续 `cli.py` 变薄/场景搬迁属于 S0C-3A 的拆分工作，不再归入 2A）。
