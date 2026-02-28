# Log-S0C-4A: workflow & scenarios taxonomy

---

**id**: `S0C-4A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `workflow & scenarios taxonomy`
**status**: `stable`          # draft | stable | archived
**scope**: `S0C`
**tags**: `EVOLUTION, Docs, Workflow, Scenarios, CI, sub/1`
**links**: ``
  **issue**: `#66, #83, #107, #114`
  **pr**: `#108`
  **adr**: ``
  **runbook**: `docs/runbook/run-S0C-docs-management-v3.md`
**created**: `2026-02-22`
**updated**: `2026-02-23`

---

## Decision / Outcome（结论区）

- 采用 3 维 taxonomy 统一 drills/scenarios 分类：`Intent（意图）` × `Pipeline（链路）` × `Runtime（依赖）`，避免把“阶段/目的/依赖”混在一个大列表里。
- 场景 ID（对人/对文档）使用分层命名：`{intent}/{pipeline}/{topic}`（或等价的 `_` 分隔），让名字本身可读、可审计。
- workflow 形态从“巨无霸 if/elif + 超长 inputs.options”演进为：`suite workflows（面向人） + 统一 runner（面向机器，可复用）`。
- 场景清单从 workflow 内移出到 `scenario catalog`（数据驱动），workflow 只保留一个核心输入 `scenario_id`；其余依赖与默认参数从 catalog 读取。
- 验收口径：不追求一次性推倒重来；优先实现“可扩展的分类轴 + 可迁移的命名规则 + runner 复用”，再逐步迁移旧场景名与 workflow。

落地收尾（本主题已完成）：

- `scenario catalog` 已成为 drills/suites 的单一事实源，suite workflows 收敛为 `scenario_id` 输入，runner 负责统一执行模板。
- 已补齐最小 guardrails（catalog/workflow 引用一致性校验）与可审计证据链（Actions run URLs + conclusion）。
- 执行性细节与证据持续维护转入：`docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md`。

## Background

目前 `.github/workflows/` 下的 drills（例如 `drill-write-gate.yml`、`drill-shadow-verify-entries.yml`）逐步演化成“把所有场景都塞进一个 workflow”的形态。随着场景增多，workflow inputs、步骤重复、if/elif 分支与场景列表都会快速膨胀，导致：维护成本高、排错慢、证据链不清晰。

## Problem / Malfunction

- **症状**：同一个 workflow / 同一组 scenario 同时混入 verify / readiness / dual-run / dual-write / fault 等不同“意图轴”，导致输入与分支越来越像“驾驶舱”。
- **根因**：分类维度混在一起（意图、链路、运行依赖），同时 workflow 把“场景清单、依赖、默认参数、执行模板”耦合在同一文件里。
- **风险**：
  - 新增一个场景就要改一堆重复步骤与 if/elif，容易错。
  - inputs.options 列表不可控变长，review 困难。
  - 场景名不可读，排错时很难定位“这属于哪个阶段/哪条链路/需要什么依赖”。

## What/How to do（落地规则）

### 1) Taxonomy（统一分类轴）

建议使用 3 个维度（你现在混在一起的就是这 3 个轴）：

- 维度 A：`Intent`（你想证明什么）
  - `VERIFY`：证明对齐/一致性/分页稳定/共享键证据包
  - `READINESS`：证明“可以开闸但默认不写”（dry-run / gate readiness）
  - `DUAL_RUN`：证明“并行处理/持续窗口运行/可消化”
  - `DUAL_WRITE`：证明“真写入 + 可控爆炸半径 + cleanup”
  - `FAULT`：故障注入（ES 429、bulk partial、DB contention、stuck reclaim…）
- 维度 B：`Pipeline`（你在动哪条链路）
  - `SEARCH`
  - `CHRONICLE`
  - `OBS_INFRA`（OTEL/collector、ES、DB）
- 维度 C：`Runtime`（跑它需要什么依赖）
  - `DB_ONLY`
  - `DB_ES`
  - `DB_ES_JAEGER`
  - （可选）`WORKER`（需要 worker loop）

目标：无论是文档、catalog、还是 workflow inputs，都能从名字/元数据直接读出“它是什么、动哪条链路、需要什么”。

### 2) Scenario ID 命名规则（对人友好）

建议格式：`{intent}/{pipeline}/{topic}`（`/` 或 `_` 二选一，但全局统一）。

示例（从现有名字迁移的建议映射）：

- `shadow_verify_search_index_write_gate` → `verify/search/write_gate_idempotency`
- `shadow_verify_search_index_paging_stability` → `verify/search/paging_stability`
- `shadow_verify_shared_keys` → `verify/obs_infra/shared_keys_bundle`
- `shadow_verify_dual_run_readiness_gate` → `readiness/search/dual_run_gate`
- `shadow_verify_dual_run_stage1` → `dual_run/search/stage1_backfill`
- `shadow_verify_dual_run_stage2` → `dual_run/search/stage2_worker`
- `shadow_verify_dual_run_window` → `dual_run/search/window_sustained`
- `shadow_verify_canary_dual_write` → `dual_write/search/canary_cleanup`
- `shadow_verify_dual_write_sampling` → `dual_write/search/sampling_cleanup`

迁移策略：优先“新增新 ID（alias）但保留旧 ID”，等 workflow 与文档稳定后再逐步下线旧命名。

### 3) Workflow 分层（suite + runner）

从“一个巨无霸 workflow”演进成两层：

- Layer 1：`suite workflows`（面向人，inputs 少、可读）
  - `drill-verify.yml`：只放 `verify/*`
  - `drill-write-gate.yml`：只放 `readiness/* + dual_write/*`
  - `drill-dual-run.yml`：只放 `dual_run/*`
  - `drill-failures.yml`：只放 `fault/*`（原 `failure-drills.yml`）
- Layer 2：`reusable runner`（面向机器，执行模板统一）
  - 把重复的 `start db/infra → install → migrate → run → finalize → upload` 抽成 `workflow_call`。
  - suite 只负责传：`scenario_id`、依赖开关（ES/Jaeger/worker）、覆写参数（duration/window/max_writes 等）。

### 4) Scenario catalog（数据驱动，解耦 inputs.options）

把“场景清单 + 元数据”从 workflow 内移出：

- 位置建议：`docs/labs/scenarios/catalog.yml`（或用脚本生成 JSON）
- 建议字段：
  - `id`：`dual_run/search/window_sustained`
  - `cli`：`python backend/scripts/cli.py ...`
  - `requires`：`{ db: true, es: true, jaeger: false, worker: false }`
  - `defaults`：`{ duration: 15, interval: 1, batch: 5, max_total: 75 }`
  - `tags`：`[S2B, write-gate, search]`

workflow 只保留一个输入 `scenario_id`；其余从 catalog 读取并传入 runner。

## Next

- 本 log 已收敛为“taxonomy 与迁移策略”的稳定记录，不再承载持续更新。
- 后续增量（新增/改名 scenario、suite/runner 调整、证据刷新、legacy 下线节奏）在 `S0C-4A-1A` 中跟踪与验收。

## Implementation Status（当前落地情况）

已存在（当前现实）：

- workflows：
  - `.github/workflows/drill-verify.yml`
  - `.github/workflows/drill-readiness.yml`
  - `.github/workflows/drill-dual-run.yml`
  - `.github/workflows/drill-dual-write.yml`
  - `.github/workflows/drill-shadow-verify-entries.yml`
  - `.github/workflows/drill-write-gate.yml`
  - `.github/workflows/drill-failures.yml`
- CLI/场景侧能力（可作为 runner 的执行目标）：`backend/scripts/cli.py` + `backend/scripts/cli_app/*`（含 scenario registry、artifacts contract 等）

已落地（本主题 DoD）：

- ✅ `scenario catalog`（集中定义 id/aliases/依赖/默认参数/CLI 调用）：`docs/labs/scenarios/catalog.yml`
- ✅ 可复用 runner（统一 setup/migrate/finalize/upload），suite workflows 通过 `uses` 调用
- ✅ suite workflows 按 intent 维度收敛，并统一输入为 `scenario_id: string`（不再维护 inputs.options 大列表）
- ✅ guardrails：CI 校验 catalog schema/唯一性/引用一致性，避免 catalog/workflow 漂移
- ✅ operator 路径：可列出合法 `scenario_id` + runbook 指引（见 links/runbook 与 `S0C-4A-1A`）

（方案A 已启动并落地一版：按 Intent 拆 suite workflows）

- ✅ intent-suites：verify/readiness/dual_run/dual_write/fault
  - verify：`.github/workflows/drill-verify.yml`（复用 write-gate runner）
  - readiness：`.github/workflows/drill-readiness.yml`（复用 write-gate runner）
  - dual_run：`.github/workflows/drill-dual-run.yml`（复用 write-gate runner）
  - dual_write：`.github/workflows/drill-dual-write.yml`（复用 write-gate runner）
  - fault：沿用 `.github/workflows/drill-failures.yml`（复用通用 runner；原 `failure-drills.yml`）
- ✅ `drill-write-gate.yml` 已收敛为 readiness + dual_write（不再混入 verify/dual_run）

（方案B 已启动并落地一版：alias 命名迁移，兼容旧/新 ID）

- ✅ catalog 场景 ID 已支持 `{intent}/{pipeline}/{topic}` 分层命名，并通过 `aliases` 保留 legacy id
- ✅ runners 已支持用新 id 或 legacy id 解析同一场景（不影响现有 suite/workflow 的旧输入）
- ✅ suites 已切换为新分层 id 作为默认值/静态引用（runner 仍兼容 legacy id）

验证证据（migrate 后行为一致）：

- drill-failures（原 failure-drills, scenario=all）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22275662579
- drill-failures（原 failure-drills, scenario=429）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22275663786
- drill-write-gate（scenario=shadow_verify_search_index_write_gate）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22276117940
- drill-shadow-verify-entries（scenario=shadow_verify_chronicle_entries）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22289438317
- drill-shadow-verify-entries（scenario=shadow_verify_search_index / verify/search/index_consistency）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22290042099
- drill-shadow-verify-entries（scenario=shadow_verify_search_index_write_gate / verify/search/write_gate_idempotency）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22290043428

- artifact 名包含 `/` 的修复验证（upload-artifact 兼容新分层 id）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22290531634

- 追加验证证据：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22290629837

- drill-verify（intent-suite）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22289785654
- drill-dual-write（intent-suite）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22289809091
- drill-readiness（intent-suite）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22289825657
- drill-dual-run（intent-suite）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22289831418

## References

- `.github/workflows/drill-shadow-verify-entries.yml`
- `.github/workflows/drill-write-gate.yml`
- `.github/workflows/drill-failures.yml`
- `backend/scripts/cli.py`
- `backend/scripts/cli_app/registry.py`
- `backend/scripts/cli_app/scenarios/*`
