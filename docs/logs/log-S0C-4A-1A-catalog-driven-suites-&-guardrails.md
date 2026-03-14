# Log-S0C-4A-1A: convergence/catalog-driven suites & guardrails

---

**id**: `S0C-4A-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `convergence/catalog-driven suites & guardrails`
**status**: `draft`          # draft | stable | archived
**scope**: `S0C`
**tags**: `EVOLUTION, Docs, Workflow, Scenarios, CI, sub/1`
**links**: ``
  **issue**: `#83, #66`
  **pr**: `null`
  **adr**: ``
  **runbook**: `null`
**created**: `2026-02-23`
**updated**: `2026-02-23`

---

## Decision / Outcome（结论区）

本阶段（S0C-4A-1A）目标：在已完成的 taxonomy + canonical id 迁移基础上，进一步降低 suite workflow 维护成本，并用最小护栏防止回归。

- 主线（B）：suite workflows 进一步“收口”为 catalog 驱动：suite 尽量只保留 `scenario_id` + 少量必要覆写输入，避免重复维护超长 `options`。
- 配套（C）：增加一层最小 CI 护栏，在 PR 合并前快速发现：catalog/schema 错误、id/alias 冲突、workflow 引用不存在的 scenario、artifact name 不可用字符等。
- 兼容（A）：明确 legacy id（aliases）下线节奏与 DoD：短期继续兼容；中期“只展示 canonical”；长期再考虑“拒绝 legacy 输入”。

为降低“string 输入下不知道填什么 id”的操作摩擦：

- ✅ 新增场景查询脚本：`backend/scripts/ci/list_scenarios.py`
  - 从 `docs/labs/scenarios/catalog.yml` 读取
  - 支持：`--intent <verify|readiness|dual_run|dual_write|fault>`、`--grep <keyword>`
- ✅ 新增用法 runbook：`docs/runbook/run-S0C-scenarios-taxonomy.md`
  - 记录：如何查找 `scenario_id`、以及 suite 的操作建议

## Background

S0C-4A 已完成：
- taxonomy：`Intent × Pipeline × Runtime`
- canonical id：`{intent}/{pipeline}/{topic}` + `aliases` 兼容旧 id
- runner 复用：suite → reusable runner（workflow_call）
- 关键修复：canonical id 含 `/` 导致 `upload-artifact` 失败，runner 侧已做 artifact-safe name（`/` → `_`）

但目前仍存在两个持续成本点：
1) suite inputs 的 `options`（choice 列表）仍要人工同步 catalog；越多越难 review。
2) 没有“合并前护栏”，一旦 catalog/workflow 的引用关系断裂，会在运行时才暴露。

## Problem / Malfunction

- **症状**：
  - catalog 与 suite 之间容易“列表漂移”（catalog 新增/改名后 suite 未同步）。
  - 少量非业务性错误（比如 artifact name 字符集、scenario id 拼写）会导致 CI 直接失败，且排查成本高。
- **根因**：
  - suite 仍承担“枚举列表”的职责。
  - 缺少静态校验与约束（schema、唯一性、引用完整性、字符合法性）。
- **风险**：
  - 迁移越深入，越容易在边角回归；证据链会变薄。

## What/How to do（落地规则）

### 1) Suite 收口规则（B 主线）

原则：suite 负责“意图入口 + 极少数必要参数”，catalog 负责“场景清单 + 元数据”。

- suite inputs：
  - 必须保留：`scenario_id`（string）
  - 可选保留：仅与 runner 机制强相关、且对操作者必要的覆写参数（例如 `duration/lookback/keep_last` 之类）
  - 避免：在 workflow 里维护长 `options` 列表（除非场景数极少且稳定）

- suite UI 体验（最小化）：
  - 输入为 string 时，会失去 GitHub UI 的“下拉选项”，这是可接受的 tradeoff：换取维护成本下降 + catalog 单一真相。
  - 仍保留少量“meta/常用默认”说明（写在 description 或 README/runbook），由 catalog 提供可审计的枚举。

### 2) Catalog 约束（作为单一真相）

- `id`：canonical（intent/pipeline/topic），全局唯一
- `aliases`：legacy id 列表，元素全局唯一（不能与任意 `id` 冲突，也不能与其他场景 aliases 冲突）
- `cli`：必须非空字符串（允许多行）
- `requires/defaults/tags`：保持结构一致；tags 用于“反向索引”（例如 workflow/intent/pipeline/runtime）

### 3) 最小护栏（C 配套）

新增一个轻量校验（建议作为 CI job 或 pre-commit/脚本），覆盖：

- catalog schema：顶层字段存在、`scenarios` 为 list、每个 item 为 dict
- 唯一性：
  - `id` 全局唯一
  - `aliases` 展开后全局唯一
  - `aliases` 不得与任何 `id` 重名
- 可用性：
  - 任何 suite/workflow 引用的 scenario 必须能在 catalog 通过 `id` 或 `aliases` 解析
  - `id` 允许包含 `/`，但需要同时提供一个“artifact-safe”派生名（runner 侧已实现）
- 可读性（可选但推荐）：
  - `id` 必须符合 `{intent}/{pipeline}/{topic}` 三段结构（允许未来扩展，但要有明确白名单策略）

落地位置（本 repo 约定）：

- 校验脚本：`backend/scripts/ci/validate_scenario_catalog.py`
- 独立 CI workflow（PR 触发）：`.github/workflows/ci-scenario-guardrails.yml`

### 4) Legacy 下线节奏（A 温和兼容）

- Phase 0（当前）：runner 接受 `id` 与 `aliases`；suite 默认展示 canonical
- Phase 1（稳定窗口后）：文档与 runbook 仅写 canonical；legacy 只作为“兼容输入”存在
- Phase 2（可选）：当确认没有外部引用依赖 legacy 后，再考虑在 runner 上加“拒绝 legacy”的开关或告警

为了让 A 不停留在“方向”，这里给出最小化的时间窗与 DoD（不引入额外流程，只约束产出物）：

- 锚点日期：T0 = 2026-02-23（Phase 0 start / 本 log 创建日）

- Phase 0（Now → T+14d）：保持兼容 + 迁移窗口
  - 目标：让操作者习惯 canonical，避免“突然断掉”
  - DoD：
    - 任何 suite 的 `scenario_id` 默认值与文档示例 **只使用 canonical id**（不再在示例中展示 aliases）
    - catalog 继续保留 aliases（兼容输入），runner 解析逻辑不变

- Phase 1（T+14d → T+45d）：canonical-only 文档期（仍兼容 legacy 输入）
  - 目标：外部可见材料“只讲 canonical”，把 legacy 变成隐式兼容
  - DoD：
    - docs/runbook 不再出现“aliases 也可以填”的说明（只在需要时用一句“runner 会兼容 legacy”带过）
    - 新增场景/改名时：必须先写 canonical + aliases（如需要），且 Evidence（Actions runs）使用 canonical

- Phase 2（T+45d 之后，可选）：对 legacy 输入加告警/拒绝
  - 触发条件（满足任意一个即可推进）：
    - 连续 30 天的 suite Evidence（Actions runs）中均未出现 aliases 作为输入
    - 或：确认“无外部依赖”明确（例如仅内部使用且所有入口已改为 canonical）
  - DoD（两选一，保持最小）：
    - 方案 A（告警）：runner 检测到 aliases 输入时输出 warning（不失败）
    - 方案 B（拒绝）：runner 提供一个开关（默认关）用于拒绝 aliases；在切换前先跑一轮回归 Evidence

## Execution Plan（执行顺序）

1) 先落 C：加最小护栏脚本/CI（尽快让未来改动“先失败在 PR”）
2) 再落 B：把 suite 的 `options` 逐步减少/移除，转为 string + catalog 真相
3) 最后固化 A：在 log 里写下线 DoD 与时间窗口，并在后续 log 里持续补证据

## DoD（Definition of Done）

- 护栏（C）
  - 能在 CI 中执行并对以下情况给出明确失败信息：重复 id/alias、alias 与 id 冲突、workflow 引用缺失、catalog 结构错误
- suite 收口（B）
  - 至少一个 intent-suite 完成“去 options 化”（改为 string 输入），且仍能通过 runner 正常运行并产出 artifacts
- 证据
  - 在 S0C-4A（或本 log 的 Evidence 区）补充至少 1 条“收口后 suite 的 Actions run URL”

## Evidence（验证证据）

- 统一证据入口：见 S0C-4A 的“验证证据（migrate 后行为一致）”区。
- 本阶段新增证据（待补）：
  - [x] catalog 校验脚本在 CI 运行的证据（run URL）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22294126214
  - [x] 至少 1 个 suite 去 options 后的 run URL：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22294128437
  - [x] suite 收口后（string `scenario_id`）再次运行证据（drill-verify, scenario_id=verify/search/write_gate_idempotency）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22295698905

  - [x] suite 全量回归证据（统一为 string `scenario_id` 输入）：
    - drill-readiness（scenario_id=readiness/search/dual_run_gate）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22295848829
    - drill-dual-write（scenario_id=dual_write/search/canary_cleanup）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22295850035
    - drill-dual-run（scenario_id=dual_run/search/stage1_backfill）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22295851220
    - drill-shadow-verify-entries（scenario_id=verify/chronicle/entries）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22295855211
    - drill-write-gate（scenario_id=readiness/search/dual_run_gate）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22295856322
    - drill-failures（scenario_id=fault/obs_infra/all）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22295857276

  - [x] suite 全量回归证据（auto, 2026-02-23 07:03:28 UTC, ref=S0C-evolution/docs-management-v3, sha=edf2fbb0）：
    - drill-readiness（scenario_id=readiness/search/dual_run_gate）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22296114691 (status=completed, conclusion=success)
    - drill-dual-write（scenario_id=dual_write/search/canary_cleanup）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22296117202 (status=completed, conclusion=success)
    - drill-dual-run（scenario_id=dual_run/search/stage1_backfill）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22296119554 (status=completed, conclusion=success)
    - drill-shadow-verify-entries（scenario_id=verify/chronicle/entries）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22296123173 (status=completed, conclusion=success)
    - drill-write-gate（scenario_id=readiness/search/dual_run_gate）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22296125703 (status=completed, conclusion=success)
    - drill-verify（scenario_id=verify/search/write_gate_idempotency）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22296130393 (status=completed, conclusion=success)
    - drill-failures（scenario_id=fault/obs_infra/all）：https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22296133063 (status=completed, conclusion=success)

## Risks / Notes

- suite 从 choice → string 会牺牲 UI 下拉，但能显著降低维护成本；这是刻意选择。
- 护栏脚本要避免“过度强约束”导致摩擦：先做最小集合，后续再逐步加规则。

## References

- 基线 log：`docs/logs/log-S0C-4A-workflow-&-scenarios-taxonomy.md`
- Scenario catalog：`docs/labs/scenarios/catalog.yml`
- Operator runbook：`docs/runbook/run-S0C-scenarios-taxonomy.md`
- Workflows：
  - `.github/workflows/drill-verify.yml`
  - `.github/workflows/drill-write-gate.yml`
  - `.github/workflows/drill-shadow-verify-entries.yml`
  - `.github/workflows/drill-failures.yml`
- Reusable runners：
  - `.github/workflows/reusable-labs-scenario-runner.yml`
  - `.github/workflows/reusable-drill-write-gate-runner.yml`
  - `.github/workflows/reusable-drill-shadow-verify-entries-runner.yml`
- Helper scripts：
  - `backend/scripts/ci/list_scenarios.py`
  - `backend/scripts/ci/validate_scenario_catalog.py`
