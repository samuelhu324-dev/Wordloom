# log-S0D-1A-log-entries-orchestration（Workflow：log entries orchestration｜主 log + 子 logs 闭环 v1）

---

**id**: `S0D-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `workflow: log entries orchestration (parent spine + phase logs) v1`
**status**: `stable`          # draft | stable | archived
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Logs, Workflow, Evidence, Orchestration, Templates, SoT`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **templates**: `docs/logs/_template-log-parent-epic-spine.md` ; `docs/logs/_template-log-phase-drills-evidence.md`
  **reference_log_1**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_2**: `docs/logs/log-S6A-4A-hard-gate-evidence-json.md`
  **reference_log_3**: `docs/logs/log-S0C-5A-Git-commit+push-descriptions.md`
**created**: `2026-03-06`
**updated**: `2026-03-15`

---

## Decision / Outcome（结论区）

- 采用“主 log（epic spine）+ 子 logs（phase / drills / evidence）”的组织方式，解决 logs 数量增长后“入口漂移、命名漂移、证据链断裂”的结构性问题。
- 采用 `P<phase>-C<cycle>-S<step>` 的编号与记账习惯，在不继续加长 log id 前缀的前提下，实现：可追索、可复盘、可演进、可机械识别。
- 固化两份模板：
  - 主 log 模板：`_template-log-parent-epic-spine`（epic spine / indexing / checklist）
  - 子 log 模板：`_template-log-phase-drills-evidence`（phase / drills / evidence / closure）
- 闭环验证：以 `S6A`（spine）及其子 logs 作为真实样本，验证该组织方式可以长期扩展而不退化为“第二份 SoT”。

## Background（背景）

- logs 数量持续增长后，常见失控模式是：每遇到一个新切片就不断开“子 log 的子 log”，最终导致 id 前缀无限叠加（例如出现 `S6A-1A-1A-1A` 一类的结构噪声）。
- 另一个失控模式是：同一主题在多个 log 中重复叙述，形成“第二份 SoT”，造成口径不一致与证据链难以追溯。
- 因此需要一套**机械可识别**、对人也**高度可读**的组织框架：
  - 读者能快速定位“入口在哪里 / 现在做到哪一步 / 证据在哪里 / headSha 或 artifacts 指向哪里”。
  - 写作者能用一致的结构快速产出，不必每次重新发明目录。

## Principles（原则 / 设计要点）

- **不让 id 前缀继续增长**：log id 只表达主题归属（epic / sub），进度与证据用 `P/C/S` 表达。
- **以 checklist 驱动可演进闭环**：计划（Plan）与执行（Execution Checklist）必须对齐，能逐步打勾并附带证据。
- **证据链可追溯**：Evidence 以 artifacts / CI run / headSha 为事实源；log 只记录低基数字段与入口链接。
- **结构可复制**：用模板把“写作结构”产品化，降低写作成本、提高一致性。

## Numbering（编号约定）

- `P<n>`：Phase（切片 / 里程碑）。
- `C<n>`：Cycle（循环轮次 / 重试 / 扩展轮）。
- `S<n>`：Step（步骤）。

建议的 commit / PR 命名：

- `S<epic>/P<phase>-C<cycle>-S<step>: <summary>`

## Templates（模板）

### P0（Templates extraction）

目标：把既有成熟样本（S5A、S2B）里“可扩展的 log 结构”抽取为两份模板。

- P0-C1-S1：基于 S5A 与 S2B 的写作结构，形成主 log（epic spine）模板：`_template-log-parent-epic-spine`。
- P0-C1-S2：基于 S5A 的四个子 log（S5A-1A/2A/3A/3B）结构，形成子 log（phase drills evidence）模板：`_template-log-phase-drills-evidence`。

### P1（Closed-loop verification）

目标：用两份模板完成一个“主 log + 子 logs*”的真实闭环，并用真实工程演进样本验证其有效性。

- P1-C1-S1：按主 log 模板创建一个 spine log（例如 `S6A`），只做索引、约束、切片与 checklist，不搬运旧 SoT。
- P1-C1-S2：按子 log 模板创建多个 phase logs（例如 `S6A-1A/2A/3A/4A`），每个子 log 含 plan、checklist、evidence 与 closure。
- P1-C1-S3：以子 log 的 evidence/closure 反向支撑 spine log 的完成度（spine log 的 checklist 可以被子 log 的“记账条目”证明）。

## Evidence（记账 / closure）

### P1-C1-S3（Closure sample｜S6A closed-loop verified｜2026-03-06）

- 真实闭环样本：
  - spine：`docs/logs/log-S6A-evidence-drills-spine.md`
  - phase logs：`docs/logs/log-S6A-1A-stable-entry-contract.md`、`docs/logs/log-S6A-2A-unify-supply-creation.md`、`docs/logs/log-S6A-3A-failure-taxonomy-hard-interface.md`、`docs/logs/log-S6A-4A-hard-gate-evidence-json.md`
- 说明：S6A spine log 通过 P0–P4 的 checklist + 子 log evidence 的记账条目形成可追索闭环，并最终可提升为 `stable`。

### P1-C1-S4 (Closure sample | S0D-5A stable bookkeeping verified | 2026-03-15)

- Real closure sample:
  - parent/index log: `docs/logs/log-S0D-1A-log-entries-orchestration.md`
  - phase log: `docs/logs/log-S0D-5A-drills-evidence-packing-unification.md`
  - child-log template: `docs/logs/_template-log-phase-drills-evidence.md`
- Notes:
  - `S0D-5A` now demonstrates the full child-log lifecycle on top of the template structure: contract definition, implementation landing, drill validation, legacy-doc audit, evidence bookkeeping, and stable promotion.
  - The child-log template is now normalized to pure English wording so future phase logs do not drift into mixed-language structure while still preserving repo-specific naming conventions.

## Notes（可选）

- 本 log 关注“组织与流程”，不取代任何领域 log 的细节内容。
- 若未来出现新的主题 epic，优先复制模板并在 spine log 中链接旧 SoT，而不是复制旧 SoT 的内容。
