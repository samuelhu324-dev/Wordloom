# log-S6B-1C（Tracked retained-summary coexistence migration：lookup migration + dual-read/fallback + legacy alias stop condition）

---

**id**: `S6B-1C`
**kind**: `log`
**title**: `tracked retained-summary coexistence migration (lookup migration + dual-read/fallback + legacy alias stop condition) v1`
**status**: `stable`
**scope**: `S6`
**tags**: `EVOLUTION, Evidence, Drills, Taxonomy, Naming, Coexistence, Retention, epic/s6, sub/1c`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/359`
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/_draft/road-S2-.md`
  **parent_log**: `docs/logs/log-S6B-evidence-drills-taxonomy.md`
  **previous_log**: `docs/logs/log-S6B-1B-evidence-naming-baseline.md`
  **reference_log_1**: `docs/logs/log-S6B-1B-evidence-naming-baseline.md`
  **reference_log_2**: `docs/logs/log-S6B-1A-evidence-surface-inventory-ledger.md`
  **reference_log_3**: `docs/logs/log-S2B-projection-table-merge.md`
**issue_keyword**: `coexistence`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s6/evidence & drills, sub/1`
**issue_module_labels**: ``
**issue_milestone**: `road-S2`
**issue_parent**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/356`
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/_draft/road-S2-.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: `P3`
**roadmap_bridge_refs**: `S6B-1C -> road-S2 / M5 / P3`
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: `road-S2`
**pr_base**: `main`
**pr_development_issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/359`
**created**: `2026-04-04`
**updated**: `2026-04-04`

---

## Decision / Outcome

**Decision**:

- `S6B-1C` 承接 `S6B-1B/P4-C4` 已经开启的 tracked retained-summary coexistence，继续处理真正会影响 repo-tracked paths 的迁移问题，而不是继续停留在 naming baseline 层。
- 当前首个治理对象固定为 `write_gate` retained-summary SoT：
  - new primary path: `artifacts/s2b.write-gate.runs.latest.json`
  - legacy alias: `artifacts/write_gate_runs.latest.json`
- 本 log 的 v1 目标不是立刻删除 legacy alias，而是先把三类边界固定清楚：
  - 哪些 lookup surfaces 需要迁到新 primary path
  - 哪些 generator / consumer 需要 dual-read 或 fallback
  - legacy alias 何时才允许停止继续写入或停止继续被引用

**Default choices (phase defaults / v1)**:

- 优先做 bounded coexistence，不做 breaking rename。
- 先覆盖高价值 operator lookup surfaces 和最关键 generator/consumer，再考虑全量清扫历史引用。
- legacy alias 的退出必须依赖 stop condition，而不是凭主观感觉“应该差不多都迁完了”。
- v1 先围绕 `write_gate` 这一条 tracked retained-summary SoT 展开，不同时打开多个 retained-summary family。

## Definitions (optional)

- `primary path`: 后续新的默认 lookup / write target。
- `legacy alias`: coexistence 期间继续保留的旧路径，用于兼容尚未迁移完的引用。
- `dual-read/fallback`: consumer 优先读新路径，必要时回退到旧路径；或在两者之间存在明确的读取优先级。
- `stop condition`: 允许移除 alias 或停止继续写旧路径前必须满足的条件集合。

## Constraints

- 不重开 `S6B-1B` 已经固定的 naming grammar；`S6B-1C` 只处理 repo-tracked retained-summary 的 coexistence 迁移实施。
- 不允许在没有 alias/fallback 的情况下直接删除 `artifacts/write_gate_runs.latest.json`。
- 不要求在 v1 一次性更新所有历史日志；优先更新高价值 operator lookup 和真实 generator/consumer surface。
- 任何 alias removal 都必须晚于 dual-write 验证和 lookup migration，而不是与它们并行硬切。

## Scope

- `P0`: coexistence contract（primary/alias/consumer boundary）
- `P1`: lookup migration inventory（高价值 lookup surfaces 分批迁移）
- `P2`: dual-read / fallback policy（generator/consumer 的读写优先级与兼容策略）
- `P3`: legacy alias retirement gate（stop condition、观察窗口与 removal boundary）

## Success Criteria (DoD)

- 至少明确回答 `write_gate` retained-summary 的 primary path 与 legacy alias 各自职责。
- 至少有一份高价值 lookup migration inventory，区分哪些文档/入口必须先迁，哪些历史引用可后迁。
- 至少明确回答 generator / consumer 的 dual-read 或 fallback 策略，而不只是一句“后面再切”。
- 至少明确 legacy alias removal 的 stop condition，避免 coexistence 无限期悬空。

## Stability (what stable means)

- This log can be marked `stable` when:
  - the first tracked retained-summary coexistence migration contract is retained
  - later rename/cutover work can reuse its migration, fallback, and stop-condition rules directly

## PR Summary Inputs (optional)

**PR summary bullets**:

- Fix the coexistence contract for the tracked `write_gate` retained-summary family by separating the new primary path from the legacy alias.
- Inventory the high-value lookup surfaces and split immediate primary-path migrations from bounded historical legacy references.
- Retain explicit dual-write, manual fallback, and alias-retirement gates so the tracked rename path can progress without a breaking cutover.

## P0 (Coexistence contract | v1)

### P0-C1-S1 (Primary and alias boundary fixed | v1)

- `artifacts/s2b.write-gate.runs.latest.json` 是新的 primary path。
- `artifacts/write_gate_runs.latest.json` 是 coexistence 期间保留的 legacy alias。
- coexistence 期间，新文档和新脚本应优先引用 primary path；legacy alias 只服务尚未完成迁移的旧引用。

### P0-C1-S2 (Migration unit fixed | v1)

- 本 log 的最小治理单元不是“所有 artifacts 命名”，而是单一 tracked retained-summary family：`write_gate` run mapping SoT。
- 后续若推广到其他 tracked retained-summary family，应复用本 log 的迁移框架，而不是重写一套规则。

## P1 (Lookup migration inventory | v1)

### P1-C1-S1 (High-value lookup surfaces identified | v1)

- 当前与 `write_gate` retained-summary SoT 直接相关的高价值 lookup surfaces，可先分为四类：
  - `generator entry`: `scripts/p1_write_gate_regression.ps1`
  - `operator runbook`: `docs/runbook/run-S2B-projection-table-merge.md`
  - `operator quick lookup`: `docs/QUICK_COMMANDS.md`
  - `family SoT logs`: `docs/logs/log-S2B-projection-table-merge.md`, `docs/logs/log-S2B-3A-unified-consumer-framework.md`, `docs/logs/log-S2B-4A-table-merge-migration.md`, `docs/logs/log-S2B-5A-table-merge-migration.md`, `docs/logs/log-S2B-5A-table-merge-migration-v2.md`, `docs/logs/log-S2B-6A-unified-outbox-table-merge.md`, `docs/logs/log-S0D-2A-drills-evidence-automation.md`
- 上述四类里，前 3 类直接决定 operator 会先看到哪个路径；`family SoT logs` 则决定 repo 级长期叙述会不会继续把旧路径当成唯一事实源。

### P1-C1-S2 (Must-migrate versus bounded-legacy references separated | v1)

| reference class | current examples | migration bucket | current rule |
| --- | --- | --- | --- |
| `generator entry` | `scripts/p1_write_gate_regression.ps1` | `must-migrate-now` | 已切到 primary path，并保留 legacy alias dual-write |
| `operator runbook` | `docs/runbook/run-S2B-projection-table-merge.md` | `must-migrate-now` | 新主路径应作为默认 lookup，旧路径只作为 coexistence alias |
| `operator quick lookup` | `docs/QUICK_COMMANDS.md` | `must-migrate-now` | 用户抄命令/查路径时应先看到 primary path |
| `family SoT log (active)` | `docs/logs/log-S2B-projection-table-merge.md` | `must-migrate-early` | active family log 应明确 primary path 已取代旧路径成为 SoT |
| `family SoT logs (broad historical set)` | `docs/logs/log-S2B-3A-unified-consumer-framework.md`, `docs/logs/log-S2B-4A-table-merge-migration.md`, `docs/logs/log-S2B-5A-table-merge-migration.md`, `docs/logs/log-S2B-5A-table-merge-migration-v2.md`, `docs/logs/log-S2B-6A-unified-outbox-table-merge.md`, `docs/logs/log-S0D-2A-drills-evidence-automation.md` | `bounded-legacy-allowed` | 允许短期保留旧路径文字引用，但后续应逐批补为 “primary path + legacy alias” 表达 |

- `must-migrate-now` 的标准是：这个 surface 会直接影响新的 operator 行为或 generator 默认出口。
- `must-migrate-early` 的标准是：这个 surface虽然不是命令入口，但它承担当前 family 的 SoT 叙述角色。
- `bounded-legacy-allowed` 的标准是：历史 log 仍可暂时保留旧路径文字，但不能再作为新增文档的默认写法。

## P2 (Dual-read / fallback policy | v1)

### P2-C1-S1 (Generator write priority fixed | v1)

- 当前 `write_gate` retained-summary family 的 generator baseline 以 `scripts/p1_write_gate_regression.ps1` 为准：
  - `artifacts/s2b.write-gate.runs.latest.json` 是 required primary write target
  - `artifacts/write_gate_runs.latest.json` 是 coexistence 期间 required legacy mirror target
- 写入顺序应保持为：先写 primary path，再写 legacy alias；primary path 决定 canonical SoT，legacy alias 只承担兼容镜像职责。
- coexistence 尚未结束前，dual-write 不应退化为“primary 成功即可、alias 失败可忽略”。原因是这会制造看不见的 split-brain：
  - 新入口看到的是 primary
  - 旧引用看到的是 alias
  - 一旦两者内容不同步，repo 会同时存在两个自称最新的 retained-summary 入口
- 因此 v1 generator 规则固定为：
  - primary write failure => 整次收集失败
  - legacy alias write failure => 同样视为 coexistence 失效，应修复后再宣称本轮 write-gate mapping 已成功刷新
- 新增 generator/wrapper 若需要消费这套规则，默认应把 primary path 暴露为主参数；legacy alias 只作为 coexistence 期间的兼容输出，不应再被设计成新的默认 SoT。

### P2-C1-S2 (Consumer read priority and fallback fixed | v1)

- 当前 repo 内对这条 SoT 的自动化读取面并不深；仓内已确认的硬实现主要是 generator dual-write，而不是第二个 repo-internal automated reader。
- 因此 v1 的 `dual-read/fallback` 应按 consumer 类型分层，而不是假装所有引用面都在主动读文件：

| consumer class | current examples | read priority | fallback rule |
| --- | --- | --- | --- |
| `operator/manual lookup` | `docs/runbook/run-S2B-projection-table-merge.md`, `docs/QUICK_COMMANDS.md` | 先读 primary path | 若外部笔记/旧 runbook 仍指向 alias，可临时回到 legacy alias，但应把 primary 当作当前 SoT |
| `active family log lookup` | `docs/logs/log-S2B-projection-table-merge.md` | 先认 primary path | 允许同时保留 alias 说明，帮助读者把旧 log 里的路径映射到新 SoT |
| `broad historical references` | `docs/logs/log-S2B-3A-unified-consumer-framework.md`, `docs/logs/log-S2B-4A-table-merge-migration.md`, `docs/logs/log-S2B-5A-table-merge-migration.md`, `docs/logs/log-S2B-5A-table-merge-migration-v2.md`, `docs/logs/log-S2B-6A-unified-outbox-table-merge.md`, `docs/logs/log-S0D-2A-drills-evidence-automation.md` | 不视为 active consumer | 可暂时继续保留旧路径文字，但其 fallback 语义仅限“历史文字仍可被理解”，不等于这些 log 继续定义当前 SoT |

- `operator/manual lookup` 的核心规则是：
  - 若 primary path 存在，则默认只看 primary
  - 只有当你是沿着旧文档、旧笔记、旧排障记录回溯时，legacy alias 才是允许的 fallback
- `active family log lookup` 的核心规则是：当前 family 的 active log 必须把 primary path 写成第一事实源，并显式说明 alias 仍在 coexistence。
- `broad historical references` 的核心规则是：它们不是“正在读 alias 的 consumer”，而是“仍记着旧路径的历史叙述”；因此后续治理重点是补注释和迁移表述，而不是给这些 log 发明代码级 fallback。
- v1 还固定一条防歧义规则：consumer 不应把 primary path 与 legacy alias 当成两个独立数据源同时比对或分别引用；在 coexistence 期间，它们表达的是同一份 run mapping 的两个入口名。

## P3 (Legacy alias retirement gate | v1)

### P3-C1-S1 (Dual-write stop conditions fixed | v1)

- 停止 `write_gate` retained-summary dual-write 的前提，不是“旧路径看起来很少用了”，而是以下条件同时满足：
  - `scripts/p1_write_gate_regression.ps1` 继续以 primary path 作为唯一 canonical output，且不存在第二个 repo-tracked generator 仍默认只写 alias
  - 高价值 active lookup surfaces 已全部以 primary path 为默认入口：`docs/runbook/run-S2B-projection-table-merge.md`、`docs/QUICK_COMMANDS.md`、`docs/logs/log-S2B-projection-table-merge.md`
  - repo 内未发现新的 repo-tracked automated reader 仍要求 alias 作为唯一读取入口；当前已确认的脚本面只有 generator dual-write，本仓内没有第二个明确自动 consumer 依赖 alias
  - 至少完成一个 bounded observation window，证明 operator 实际排障与 run lookup 已不再需要 alias 才能完成日常路径查找
- 在以上条件满足前，停止 alias 写入会把 coexistence 从“有界兼容”变成“名义兼容、实际断流”，因此不允许仅因为 primary 已稳定就提前停掉 legacy 写入。

### P3-C1-S2 (Dual-read / alias-reference stop conditions fixed | v1)

- 结束 alias 作为 active reference 的条件，应与“历史文本里仍保留旧名字”分开判断：
  - `active operator surfaces` 不再把 alias 当默认入口，且不再要求用户先查 alias 再映射回 primary
  - `active family log` 已把 primary path 固定为唯一当前 SoT；若仍提 alias，也只能以“historical alias / retired name”身份出现
  - `bounded-legacy-allowed` 那批历史 logs 可继续保留旧路径文字，但它们必须被明确视为 historical narrative，而不是当前 SoT contract
  - repo 中不得再新增把 `artifacts/write_gate_runs.latest.json` 当成当前默认 SoT 的新文档、新脚本参数默认值或新 helper surface
- 因此 v1 固定两条 retirement 语义：
  - `end dual-write`：表示 generator 不再继续刷新 alias 文件
  - `end active alias references`：表示 active docs/runbooks/logs 不再把 alias 当现行入口
- 这两个动作可以接近发生，但不应混成同一个开关；即使停止 dual-write，历史日志中的旧名字也可能继续存在，只是它们不再构成 active alias contract。

### P3-C1-S3 (Observation window and rollback boundary fixed | v1)

- alias removal 之前，至少需要一个最小观察窗口：
  - 连续 2 次成功的 `scripts/p1_write_gate_regression.ps1` refresh 周期中，primary path 都成功刷新
  - 这 2 次周期内未出现因为缺少 alias 而必须依赖旧路径才能完成 operator lookup 的新增证据
  - 这 2 次周期内 repo-tracked active surfaces 未重新引入把 alias 当默认 SoT 的新引用
- 若观察窗口内出现以下任一情况，则视为不满足 removal gate，应保持或恢复 coexistence：
  - operator/runbook/quick-command 仍需要 alias 才能完成主流程 lookup
  - 新增脚本、wrapper 或 helper surface 把 alias 当成唯一输入/输出约定
  - primary path 与 alias 的预期角色再次混淆，导致文档或日志把两者写成并列 SoT
- rollback boundary 也需要明确：
  - 若 alias 已停止写入但观察窗口内暴露出 active dependency，应优先恢复 generator dual-write，而不是要求 operator 先手工适配
  - 若 active docs 已去掉 alias，但仍发现真实 lookup 依赖，则应先恢复文档中的 alias compatibility note，再继续 migration
  - rollback 的目标不是长期回到旧路径，而是把 coexistence 恢复到可观测、可迁移、不会 silently break 的状态

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S6B-1C/P<phase>-C<cycle>-S<steps>: <summary>`

## Plan (draft)

### P1 (Lookup migration inventory)

- P1-C1-S1: identify the first high-value lookup surfaces that must migrate to the primary path
- P1-C1-S2: separate must-migrate references from bounded legacy references

### P2 (Dual-read / fallback)

- P2-C1-S1: define generator write priority between primary path and legacy alias
- P2-C1-S2: define consumer read priority and fallback behavior

### P3 (Legacy alias retirement gate)

- P3-C1-S1: define stop conditions for ending dual-write
- P3-C1-S2: define stop conditions for ending dual-read / alias references
- P3-C1-S3: define observation window and rollback boundary before alias removal

## Execution Checklist (unchecked)

### P0 (Coexistence contract)

- [x] `P0-C1-S1`: primary and alias boundary fixed
- [x] `P0-C1-S2`: migration unit fixed

### P1 (Lookup migration inventory)

- [x] `P1-C1-S1`: high-value lookup surfaces identified
- [x] `P1-C1-S2`: must-migrate versus bounded-legacy references separated

### P2 (Dual-read / fallback)

- [x] `P2-C1-S1`: generator write priority fixed
- [x] `P2-C1-S2`: consumer read priority and fallback fixed

### P3 (Legacy alias retirement gate)

- [x] `P3-C1-S1`: dual-write stop conditions fixed
- [x] `P3-C1-S2`: dual-read / alias-reference stop conditions fixed
- [x] `P3-C1-S3`: observation window and rollback boundary fixed

## Evidence (reserved)

- This log is the human-facing migration ledger for tracked retained-summary coexistence. Later code changes, docs migrations, and alias-removal steps should reference this log rather than re-deciding the coexistence policy ad hoc.
- Prefer explicit migration state (`primary`, `alias`, `dual-write`, `dual-read`, `stop-condition-open`) over vague phrases like “partially migrated”.

## Recent changes (for traceability, optional)

- 2026-04-04: opened `S6B-1C` to continue the tracked retained-summary migration work after `S6B-1B/P4-C4` enabled the first dual-write coexistence baseline for `write_gate` run mappings.
- 2026-04-04: fixed `P0` v1 by retaining the primary-vs-alias boundary for `artifacts/s2b.write-gate.runs.latest.json` versus `artifacts/write_gate_runs.latest.json`, and by scoping the migration unit to one tracked retained-summary family before wider rollout.
- 2026-04-04: completed `P1` v1 by identifying the first high-value lookup surfaces around `write_gate` retained-summary SoT and separating them into must-migrate-now, must-migrate-early, and bounded-legacy-allowed buckets.
- 2026-04-04: completed `P2` v1 by fixing generator write priority for primary-versus-alias dual-write, separating manual/operator lookup from historical text references, and retaining explicit fallback rules for coexistence.
- 2026-04-04: completed `P3` v1 by fixing stop conditions for ending dual-write and active alias references, and by retaining a bounded observation window plus rollback boundary before alias removal.