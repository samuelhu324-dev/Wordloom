# Log-S0C/1A: tools/log extensions（让 log 像 log：结论区 + 可维护结构）

---

**id**: `S0C-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `tools/log extensions`
**status**: `stable`          # draft | stable | archived
**scope**: `S0C`
**tags**: `EVOLUTION, Docs, Observability, sub/1`
**links**: ``
  **issue**: `#55`
  **pr**: ``
  **adr**: ``
  **runbook**: ``
**created**: `2026-02-15`
**updated**: `2026-02-15`
**reviewed**: `pending`
**source_reader_model**: `mixed-source-v1`
**extraction_surface_version**: `extractable-rules-v1`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` own artifact lifecycle time for this source log.
- `source_reader_model` and `extraction_surface_version` version the source-log reader and extraction shape only; they do not replace any later logs-family contract release ids.
- Keep `source_reader_model` at `mixed-source-v1` while this source remains one narrative log with one explicit extraction surface.
- Keep `extraction_surface_version` at `extractable-rules-v1` while the candidate rows below remain the intended in-log handoff for later logs-family extraction.

## Background

随着 log/lab/runbook/adr 数量增长，如果每篇 log 都按“随笔”写法推进，会出现两个长期问题：

- 读者要自己总结“你到底决定了什么、做到哪一步了”（不可交接）
- 内容随着演进出现多套时间线（每节 draft/stable/archived），难维护、难检索

本 log 目标：给出一套**可复用的 log 扩展规则**，让 log 具备“30 秒可读”的结论区，并让结构长期可维护。

## Malfunction

- 现象：log 中 draft/stable 反复切换，结论不集中；读者需要自行归纳。
- 影响：复盘/交接成本高；同一主题会产生多个版本并存，难以维护。

## Decision / Outcome（结论区）

**Decision**:

- 为所有 log 引入统一的 “Decision / Outcome” 小节（置顶），并定义固定字段集合。
- 将状态机收口到文档顶部的 `status` 字段（`draft | stable | archived`），正文不再按每节复制三段时间线。

**Drivers**:

- 需要可交接的结论区（decision、non-goals、success criteria）
- 需要可维护结构（正文只有当前有效内容；历史通过 git diff/legacy 追溯）

**Non-goals**:

- 不要求一次性重写全部历史文档
- 不强制引入新的文档系统/站点生成器；先以 Markdown + front matter 为准

**Success criteria（DoD）**:

- 新写或重构的 log：读者在 30 秒内能回答：决定了什么 / 状态是什么 / 不做什么 / 怎么验收
- 文档演进不再产生“每节多时间线”；历史差异通过 git 审计或 legacy/stub 保留

## Extractable Rule Surface

- 这个 source 现在显式暴露可抽取面，而不是把 contract 候选、理由、例子继续混在叙事段落里等待 ledger 二次猜测。
- `candidate text` 只保留最小稳定规则语义；共享理由放到 `Shared Reason Groups`，例子/已执行落地仍保留在 source log。

| packet id | source anchor | extraction class | candidate text | downstream owner | split status | shared reason group | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R01` | `Decision / Outcome`; `What/How to do / 1)` | `contract-candidate` | Structured logs should expose one top-level `Decision / Outcome` section. | `contract` | `ready` | `RG-01` | `Decision / Outcome`; `What/How to do / 1)` | 这是结论区存在性的父规则。 |
| `R02` | `What/How to do / 1)` | `contract-candidate` | The top-level `Decision / Outcome` section should contain at least `Decision`, `Drivers`, `Non-goals`, and `Success criteria`. | `contract` | `ready` | `RG-01` | `What/How to do / 1)` | 这是结论区的最小字段约束；目前先保留为独立候选行。 |
| `R03` | `Decision / Outcome`; `What/How to do / 3)` | `contract-candidate` | Log lifecycle state should be owned by top-level frontmatter `status` rather than repeated as per-section draft/stable/archived timelines in the body. | `contract` | `ready` | `RG-02` | `Decision / Outcome`; `What/How to do / 3)` | 这是 frontmatter/body 边界规则。 |
| `R04` | `Decision / Outcome`; `What/How to do / 2)` | `contract-candidate` | Log bodies should retain current effective content, while historical drift should normally leave through git history, legacy, or stub paths. | `contract` | `ready` | `RG-02` | `Decision / Outcome`; `What/How to do / 2)` | 这是正文维护纪律规则。 |
| `R05` | `Applied`; `Template`; `Example` | `support-only` | Applied examples and copyable templates validate usability but do not by themselves define release-local logs-family contract meaning. | `support-only` | `ready` | `none` | `Applied`; `Template`; `Example` | 这些内容保留为 adoption/support evidence。 |

### Shared Reason Groups

| reason group | applies to packet ids | reason summary | source refs | notes |
| --- | --- | --- | --- | --- |
| `RG-01` | `R01; R02` | Readers need one fast handoff surface that states the current decision cleanly instead of forcing reconstruction from narrative prose. | `Background`; `Malfunction`; `Decision / Outcome` | 这是结论区存在性和最小字段集合的共享 why。 |
| `RG-02` | `R03; R04` | Long-lived logs become hard to maintain when lifecycle state and historical drift are duplicated throughout the body instead of being separated into frontmatter plus current-effective prose. | `Background`; `Malfunction`; `Decision / Outcome` | 这是状态收口和正文只保留当前有效内容的共享 why。 |

## Source Reader Model / Versioning

| field | value | notes |
| --- | --- | --- |
| current source reader model | `mixed-source-v1` | Source log keeps narrative explanation, examples, and evidence while exposing one explicit extraction surface. |
| extraction surface version | `extractable-rules-v1` | Uses explicit rule/rationale/support separation for later logs-family extraction. |
| compatibility expectation | `requires-manual-bridge` | Older logs that predate this explicit extraction surface may still need manual extraction or one parent-ledger bridge. |
| migration note | `Later log/ADR packets should expose contract candidates directly in-source; older packets should not be silently reinterpreted as if they already had this table.` | The model evolves forward without forcing historical rewrite. |

## Applied（已执行落地）

本规范已用于本仓库近期 log 的结构化与交付，作为可追溯证据：

- `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
- `docs/logs/log-S3A-2A-4B-1A-git-actions.md`
- `docs/logs/log-S2B-projection-table-merge.md`

## What/How to do（落地规则）

### 1) 顶部必须有结论区（Decision / Outcome）

写法约定（最小集合）：

- `Decision`：本轮到底决定了什么（1~3 条）
- `Drivers`：为什么要做（驱动因素 2~5 条）
- `Non-goals`：明确不做什么（避免读者脑补）
- `Success criteria`：可验收清单（机器/人工都可）

### 2) 正文只保留“当前有效内容”

- 正文以“当前做法”为主：背景、问题、方案、DoD、后续工作。
- 历史版本/失败路线：
  - 优先依赖 `git diff`（天然审计）
  - 若确需保留，进入 `docs/legacy/` 或以 stub 指向新位置

### 3) 状态机只在顶部维护

- `status=draft`：结构未收敛或 DoD 未达成
- `status=stable`：结论与流程可复用，且有可验收的成功标准
- `status=archived`：不再演进；保留引用价值（必要时留 stub 指路）

## Template（最小骨架）

建议所有 log 至少包含：

- Background
- Malfunction（如果是故障/踩坑复盘型）或 Problem（如果是方案型）
- Decision / Outcome
- What/How to do
- DoD / Success criteria

### Example（最小示例，可直接复制）

```markdown
## Decision / Outcome

**Decision**:
- ...

**Drivers**:
- ...

**Non-goals**:
- ...

**Success criteria（DoD）**:
- ...
```

## Exported Sections / Outlet Ownership

- `S0C-1A` 现在显式回答 source 里哪些内容更适合离开 source、哪些内容应继续保留为 log-retained core。

**Outlet ownership**:

- `contract`: `R01` through `R04` are candidate logs-family contract meaning for a later `DOC-WORKFLOW-LOGS-0002`
- `runbook`: no-op；本 source 不是操作步骤型文档
- `view`: no-op；如果后面需要 logs-family summary，应从多个 source/corroborating samples 形成，而不是只从单一 source 直接导出
- `index/front-door`: no-op；本 source 当前不直接拥有导航入口变更
- `disposition/placement`: `R05` 保持 support-only，例子与模板片段继续留在 source / support surfaces
- `log-retained core`: Background, Malfunction, shared rationale, Applied examples, and copyable template remain here as source explanation and evidence

## References
- Structured logs (examples already applied):
  - `docs/logs/log-S0C-1A-log-extensions.md`