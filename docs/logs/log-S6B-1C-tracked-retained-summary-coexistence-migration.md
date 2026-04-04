# log-S6B-1C（Tracked retained-summary coexistence migration：lookup migration + dual-read/fallback + legacy alias stop condition）

---

**id**: `S6B-1C`
**kind**: `log`
**title**: `tracked retained-summary coexistence migration (lookup migration + dual-read/fallback + legacy alias stop condition) v1`
**status**: `draft`
**scope**: `S6`
**tags**: `EVOLUTION, Evidence, Drills, Taxonomy, Naming, Coexistence, Retention, epic/s6, sub/1c`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S6B-evidence-drills-taxonomy.md`
  **previous_log**: `docs/logs/log-S6B-1B-evidence-naming-baseline.md`
  **reference_log_1**: `docs/logs/log-S6B-1B-evidence-naming-baseline.md`
  **reference_log_2**: `docs/logs/log-S6B-1A-evidence-surface-inventory-ledger.md`
  **reference_log_3**: `docs/logs/log-S2B-projection-table-merge.md`
**issue_keyword**: ``
**issue_top_labels**: ``
**issue_scope_labels**: ``
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: ``
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: ``
**pr_development_issue**: ``
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

- [ ] `P2-C1-S1`: generator write priority fixed
- [ ] `P2-C1-S2`: consumer read priority and fallback fixed

### P3 (Legacy alias retirement gate)

- [ ] `P3-C1-S1`: dual-write stop conditions fixed
- [ ] `P3-C1-S2`: dual-read / alias-reference stop conditions fixed
- [ ] `P3-C1-S3`: observation window and rollback boundary fixed

## Evidence (reserved)

- This log is the human-facing migration ledger for tracked retained-summary coexistence. Later code changes, docs migrations, and alias-removal steps should reference this log rather than re-deciding the coexistence policy ad hoc.
- Prefer explicit migration state (`primary`, `alias`, `dual-write`, `dual-read`, `stop-condition-open`) over vague phrases like “partially migrated”.

## Recent changes (for traceability, optional)

- 2026-04-04: opened `S6B-1C` to continue the tracked retained-summary migration work after `S6B-1B/P4-C4` enabled the first dual-write coexistence baseline for `write_gate` run mappings.
- 2026-04-04: fixed `P0` v1 by retaining the primary-vs-alias boundary for `artifacts/s2b.write-gate.runs.latest.json` versus `artifacts/write_gate_runs.latest.json`, and by scoping the migration unit to one tracked retained-summary family before wider rollout.
- 2026-04-04: completed `P1` v1 by identifying the first high-value lookup surfaces around `write_gate` retained-summary SoT and separating them into must-migrate-now, must-migrate-early, and bounded-legacy-allowed buckets.