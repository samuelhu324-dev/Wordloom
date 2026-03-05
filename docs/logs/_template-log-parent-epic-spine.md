# log-<ID>（<EPIC/THEME 名称>）

---

**id**: `<ID>`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `<一句话标题：领域/平台 + 目标 + v1>`
**status**: `draft`           # draft | stable | archived
**scope**: `<Sx>`
**tags**: `EVOLUTION, <domain>, epic/<sx>, sub/<xx>`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **roadmap**: ``
  **reference_log_1**: ``
  **reference_log_2**: ``
  **phase_log_1**: ``
  **phase_log_2**: ``
  **phase_log_3**: ``
**created**: `YYYY-MM-DD`
**updated**: `YYYY-MM-DD`

---

## Decision / Outcome（结论区）

**Decision**:

- <本轮核心决定 1>
- <本轮核心决定 2>

**Default choices（默认基线 / v1）**（可选，但推荐在 parent/spine 明确）:

- <默认认证/默认存储/默认入口/默认环境/默认语义……>

**Non-goals（不做什么）**（可选，但建议写）:

- <明确本 epic/spine 不覆盖的内容，防止读者脑补>

## Background（背景）

- <为何需要这个 epic/spine：历史演进导致的痛点/规模化后的结构问题>

## Constraints（约束）

- <例如：先收口契约再工程化；不引入生产级复杂度；reason 低基数；证据机器可判定>

## Scope（本 log 范围）

- 本 log 负责：
  - <定义：目标边界、默认基线、切片拆分、里程碑清单>
  - <索引：链接到旧 SoT / runbook / 稳定入口>
- 本 log 不负责：
  - <各切片的具体实现细节与证据 run（落在 phase logs / artifacts）>

## Success Criteria（DoD）

- 结构层面：
  - <读者 30 秒能理解：决定了什么、现在状态、下一步是什么>
  - <INDEX/links 能导航到稳定入口>
- 工程层面：
  - <最少 2~5 条可验收标准（可机器判定更好）>
- 证据层面：
  - <每个 phase 至少 1 条可追溯 evidence（headSha + artifacts 路径 / CI run）>

## Phases（切片）

- `<SxA-1A>`（Phase 1）：<一句话目标>
  - 详见：`docs/logs/log-<...>.md`
- `<SxA-2A>`（Phase 2）：<一句话目标>
  - 详见：`docs/logs/log-<...>.md`
- `<SxA-3A>`（Phase 3）：<一句话目标>
  - 详见：`docs/logs/log-<...>.md`

## Execution Checklist（当前骨架里程碑汇总）

- [ ] `P0`：<contract/indexing>
- [ ] `P1`：<phase 1 的里程碑摘要>
- [ ] `P2`：<phase 2 的里程碑摘要>
- [ ] `P3`：<phase 3 的里程碑摘要>

## Current Status（进展摘要）

- <一句话：整体到哪了>
- <哪些 phase stable/draft>
- <最近 1~2 个关键风险/变更>

## Notes（落地原则，可选）

- <例如：默认 404 vs 403；证据纪律；入口稳定面>

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - <默认基线/phase 拆分/证据口径稳定>
  - <稳定入口（单命令/工作流/CLI）明确>

## Recent changes（for traceability，可选）

- YYYY-MM-DD：<发生了什么变更，为什么要记录，如何追溯（commit/PR/run URL）>
