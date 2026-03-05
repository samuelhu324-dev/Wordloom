# log-S6A-2A-unify-supply-creation（P2：Unify supply creation｜统一供给写入 outbox_events v1）

---

**id**: `S6A-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `unify scenario supply creation to outbox_events (projection-scoped) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S6`
**tags**: `EVOLUTION, Evidence, Drills, FailureContract, Scenarios, Outbox, Supply, epic/s6, sub/2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_1**: `docs/logs/log-S6A-1A-stable-entry-contract.md`
  **reference_log_2**: `docs/logs/log-S2B-3A-unified-consumer-framework.md`
  **reference_log_3**: `docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md`
**created**: `2026-03-05`
**updated**: `2026-03-05`

---

## Decision / Outcome（结论区）

**Decision（v1）**:

- 所有 drills/scenarios 的“供给创建（seed/insert/trigger）”默认写入 `outbox_events`（带 `projection`），避免出现“触发写旧表、消费读新表/反之”的漂移。
- 场景中仅描述 **要插入什么意图**（projection/entity/op/版本等），供给脚本/ helper 负责选择正确表结构与兼容字段。

## Problem（为什么要做）

- 现状常见风险：
  - 场景触发事件写到 legacy outbox 表，但 worker/consumer 读取的是 unified outbox（或相反），导致 drill 结果不可解释。
  - 迁移窗口中“供给与消费不一致”会让 verify 断言失真（看起来像 worker 坏了，实际上是 supply 打错了地方）。

## Constraints（约束）

- 不在场景里复制粘贴“插入 SQL”；优先提供一个稳定入口（脚本或 helper）统一处理。
- 不写入高基数 trace/log 信息到 DB/metrics 的 reason；供给侧只做最低限度字段。
- 兼容迁移窗口：如果 unified outbox 不存在/不可用，可显式 fallback，但必须写清楚 evidence（写入哪个表、为何 fallback）。

## Scope（本 log 范围）

- `P0`：明确 supply contract（默认写 `outbox_events` + projection）与 evidence 字段
- `P1`：将 `fault/obs_infra/*` 触发脚本与 verify 口径统一到 `outbox_events`
- `P2`：扩展到同类场景（例如 `shadow_verify_*` 中的供给/seed），减少“供给漂移”

## Success Criteria（DoD）

- `fault/obs_infra/*`：触发脚本默认写 `outbox_events`，并在 evidence 中明确：
  - `supply.target_table`、`supply.projection`、`supply.insert_count`
- verify 能在 DB 侧确认：事件确实进入 worker 读取的表（至少抽样校验 id/status）。
- 至少 1 份可追溯 evidence：headSha + 1 次 artifacts 路径（或 CI run URL）。

## Execution Checklist（unchecked）

- [ ] `P0-C1-S1`：Supply contract（默认写 outbox_events + projection）
- [ ] `P0-C1-S2`：Evidence 字段最小集（supply target + 兼容/fallback 说明）
- [ ] `P1-C1-S1`：迁移 `fault/obs_infra/*` 的 trigger/seed 逻辑到 unified outbox
- [ ] `P1-C1-S2`：verify 对齐（DB 侧校验 supply 与消费一致）
- [ ] `P2-C1-S1`：同类场景（shadow_verify_*）的 seed/supply 统一

## Evidence（预留）

- 以 artifacts 为事实源；记录 headSha + 参数 + artifacts 路径（或 CI run URL）。

## Notes（实施提示）

- 建议在 shared helper 或 `backend/scripts/labs/*` 中提供稳定供给入口，场景只调用它。
- 若遇到 schema 差异（列名/必填字段不同），应在供给层做兼容映射，而不是回流到每个 scenario。
