# log-S0D-4A-UI-layered-fix-notes（Phase 4：UI layered fix notes｜前端轻轨证据链 v1）

---

**id**: `S0D-4A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `UI layered fix notes（前端轻轨证据链 + 分层升级规则 + note 模板） v1`
**status**: `stable`          # draft | stable | archived
**scope**: `S0`
**tags**: `EVOLUTION, Docs, UI, UX, Workflow, Evidence, Layered, Frontend, epic/s0, sub/4a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S0D-1A-log-entries-orchestration.md`
  **previous_log**: `docs/logs/log-S0D-2A-drills-evidence-automation.md`
  **reference_log_1**: `docs/UI&UX/README.md`
  **reference_log_2**: `docs/UI&UX/UI-FIX-NOTE-TEMPLATE.md`
  **reference_log_3**: `docs/UI&UX/UI-FIX-20260313-book-timeline-chronicle-empty.md`
  **reference_log_4**: `docs/UI&UX/UI-FIX-20260313-library-context-propagation.md`
  **reference_log_5**: `docs/UI&UX/UI-FIX-20260313-bookshelf-link-recovery.md`
  **reference_log_6**: `docs/UI&UX/UI-FIX-20260313-library-tags-limit-guard.md`
  **reference_log_7**: `docs/UI&UX/assets/README.md`
**created**: `2026-03-13`
**updated**: `2026-03-13`

---

## Decision / Outcome（结论区）

**Decision**:

- 为前端问题建立一条独立于 backend drills/hard-gate 的轻量证据链，命名为 `UI evidence-lite`。
- 采用“分层记录 + 条件升级”的方式处理前端修复：普通 UI 小修不进重流程；workflow / state / consistency 类问题进入轻轨；只有关键 workflow、权限、tenant scope、系统状态一致性等问题才升级到主证据链。
- 在仓库内正式落地一组可持续复用的前端轻轨资产：
  - `docs/UI&UX/README.md`：前端轻轨规则与升级条件；
  - `docs/UI&UX/UI-FIX-NOTE-TEMPLATE.md`：单条 UI 修复 note 模板；
  - `docs/UI&UX/assets/README.md`：截图/GIF 资产命名与归档规则；
  - 一组 `UI-FIX-20260313-*.md`：近期真实前端问题样例。

**Default choices（本 phase 默认决策 / v1）**:

- 前端证据默认使用 markdown note，而不是 result JSON / artifact zip / CI hard gate。
- 前端 note 默认字段固定为：`Issue / Impact / Reproduction / Fix / Evidence / Validation / Escalation`。
- 视觉差异优先用 before/after screenshot 或短 GIF；状态/流程问题优先用复现路径 + 验证 checklist。
- 前端 note 存放在 `docs/UI&UX/`，命名优先采用：`UI-FIX-YYYYMMDD-short-name.md`。

## Definitions（概念定义）

- **UI evidence-lite**：针对前端修复的轻量证据轨道，用于记录问题、影响、修复、截图和验证结果。
- **heavy track**：现有 backend / system evolution 主证据链，包括 logs、drills、hard gates、artifacts、CI summaries。
- **layered fix note**：带有升级判断的 UI note，不要求每条都进入系统级 evidence 流程。
- **escalation**：当 UI 问题影响关键 workflow、权限、scope 或前后端状态一致性时，从 evidence-lite 升级到 heavier flow。

## Constraints（约束）

- 不把所有前端问题强行塞入 backend 重型流程，避免流程成本淹没修复收益。
- 不允许“完全不记”：凡是 demo、README、面试、关键 workflow 会用到的前端修复，至少要有一条轻量 note。
- 轻轨文档应保持低成本、可复用、可追溯，不复制大段日志或终端输出。
- 重轨与轻轨必须边界清晰：轻轨负责表层 workflow / 状态正确性与展示证据；重轨负责系统性 contract / drills / hard gates。

## Scope（本 log 范围）

- `P0`：contract（前端轻轨的边界、升级条件、note 字段、命名规则）
- `P1`：实现（`docs/UI&UX/README.md` + `UI-FIX-NOTE-TEMPLATE.md` + repo guide 入口）
- `P2`：sample adoption（近期真实前端问题按该模板批量入账）
- `P3`：future adoption（assets 规则 + 后续前端修复按该 note 模式持续积累；必要时升级到主证据链）

## Success Criteria（DoD）

- 仓库内存在一份正式的前端轻轨规则文档，明确“什么时候记录 / 什么时候升级”。
- 仓库内存在一份可复制的 UI 修复 note 模板，能够支持日常前端问题入账。
- 仓库主 README 或导览入口能够发现这套 UI 轻轨文档，而不是悬空存在。
- 至少 3 个真实前端问题已经按该模板入账，证明流程不是空文档。
- 存在一个明确的 `assets/` 命名规则，方便截图、GIF、录屏和 note 对齐。
- 该规则明确说明：前端问题不默认进入 hard gate，但在 workflow、scope、consistency 风险出现时可以升级。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - P0 contract 已在 `docs/UI&UX/README.md` 中落地；
  - P1 的模板与 README 入口已经建立；
  - P2 已有多条真实 UI 修复 note 入账，可作为后续复用样例；
  - P3 已补充 `assets/` 规则，便于后续持续收集 before/after 证据；
  - 后续新增前端问题无需重新设计流程，只需复制模板并按升级条件判断即可。

## P0（Contract｜v1）

### P0-C1-S1（前端轻轨边界｜v1）

- 前端问题分三层处理：
  - 普通小修：仅 commit/PR 或可选截图，不强制 note；
  - workflow/state/rendering 问题：进入 `UI evidence-lite` note；
  - 关键 workflow / permission / tenant / consistency 问题：升级进 heavier evidence flow。
- 默认原则：不把前端全部纳入重型流程，但也不允许完全没有可复述记录。

### P0-C1-S2（UI fix note 字段 contract｜v1）

- 每条 UI note 至少包含：
  - `Summary`
  - `Issue`
  - `Impact`
  - `Reproduction`
  - `Fix`
  - `Evidence`
  - `Validation Checklist`
  - `Code References`
  - `Escalation Decision`
  - `Demo Value`
- 视觉差异优先记录截图或 GIF；流程差异优先记录复现步骤和验证状态。

### P0-C1-S3（升级条件 contract｜v1）

- 满足任一条件时，UI 问题应从轻轨升级：
  - 影响 create / edit / search / save / navigation 主链路；
  - 影响 permission、tenant scope、可见性或安全理解；
  - UI 呈现与 backend 真值不一致，并可能误导操作；
  - 高概率回归且回归代价较高；
  - 适合作为 README、demo、portfolio、interview 的系统级故事。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`，即 `...-S1`），也可以是在同一 phase / cycle 下连续的多个 step 合并（如 `1S2`，即 `...-S1S2`）。

**Branch 约定**:

- `S0D-4A` 这类 docs/workflow 类改动优先落在 `S0D-*` 系列分支上推进。
- 若某次 PR 同时包含 UI 实际修复与 UI 轻轨 note，建议按“修复”和“记录体系”拆分，以便后续按 scope 回溯。

## Plan（draft）

### P1（实现：轻轨文档与模板）

- P1-C1-S1：新增 `docs/UI&UX/README.md`，定义前端轻轨边界、升级条件、最小执行规则。
- P1-C1-S2：新增 `docs/UI&UX/UI-FIX-NOTE-TEMPLATE.md`，作为日常前端修复记录模板。
- P1-C1-S3：在 repo guide 中加入 `docs/UI&UX/` 入口，避免轻轨文档变成悬空资产。

### P2（sample adoption：首条真实 note）

- P2-C1-S1：用 Book Timeline 空白问题作为首条真实样例，验证该模板可用。
- P2-C1-S2：补齐 library context propagation、bookshelf old-link recovery、library tags limit guard 三条近期问题 note。

### P3（future adoption：后续滚动使用）

- P3-C1-S1：新增 `docs/UI&UX/assets/README.md`，固化截图/GIF 命名与归档规则。
- P3-C1-S2：后续把值得讲述的前端修复持续纳入 `docs/UI&UX/`，形成一批可复用的 demo/interview 证据。

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：前端轻轨边界定义完成
- [x] `P0-C1-S2`：UI fix note 字段 contract 固化
- [x] `P0-C1-S3`：升级条件 contract 固化

### P1（实现：轻轨文档与模板）

- [x] `P1-C1-S1`：新增 UI evidence-lite 规则文档
- [x] `P1-C1-S2`：新增 UI fix note 模板
- [x] `P1-C1-S3`：repo guide 增加 UI 轻轨入口

### P2（sample adoption：首条真实 note）

- [x] `P2-C1-S1`：Book Timeline 空白问题完成首条 note 入账
- [x] `P2-C1-S2`：近期前端问题 note 集合已补齐首批样例

### P3（future adoption：后续滚动使用）

- [x] `P3-C1-S1`：新增 assets 命名与归档规则
- [ ] `P3-C1-S2`：继续补齐后续已修复的前端问题 note 集合

## Evidence（预留）

- Evidence 以 repo 内实际文档为事实源；本 log 记录：`headSha + 关键文件路径 + 已入账样例`。

### P1-C1-S1S2S3（UI evidence-lite 规则 + 模板 + repo 入口落地｜2026-03-13）

- headSha：`c7527a231f3b578442fb58ba31b571b1cf1d42a4`
- artifacts：
  - `docs/UI&UX/README.md`
  - `docs/UI&UX/UI-FIX-NOTE-TEMPLATE.md`
  - `README.md`
- 期望（expected）：
  - 仓库内存在一条正式、可复用的前端轻轨证据规则；
  - 存在可复制模板；
  - repo guide 能发现该入口。
- 观测（observed）：
  - `docs/UI&UX/README.md` 已定义分层规则、升级条件和最小执行规则；
  - `docs/UI&UX/UI-FIX-NOTE-TEMPLATE.md` 已提供标准字段与 checklist；
  - `README.md` 已新增 `docs/UI&UX/` 入口说明。

### P2-C1-S1S2（首条真实 UI fix note 入账｜2026-03-13）

- headSha：`c7527a231f3b578442fb58ba31b571b1cf1d42a4`
- artifacts：
  - `docs/UI&UX/UI-FIX-20260313-book-timeline-chronicle-empty.md`
- 期望（expected）：
  - 至少 1 条真实前端问题按新模板完成入账；
  - note 中写明 fix、validation、demo value 和 escalation decision。
- 观测（observed）：
  - Book Timeline 空白问题已按模板入账；
  - note 中已写明其兼具前端表现层修复与后端 read-path 根因，并说明当前保留在 light track、何时再升级。

### P2-C1-S2（近期前端问题批量入账｜2026-03-13）

- headSha：`c7527a231f3b578442fb58ba31b571b1cf1d42a4`
- artifacts：
  - `docs/UI&UX/UI-FIX-20260313-library-context-propagation.md`
  - `docs/UI&UX/UI-FIX-20260313-bookshelf-link-recovery.md`
  - `docs/UI&UX/UI-FIX-20260313-library-tags-limit-guard.md`
- 期望（expected）：
  - 把近期已经修过、且值得 demo/interview 复述的前端问题补成一批 note；
  - 每条 note 都带 fix、validation、demo value、escalation decision。
- 观测（observed）：
  - 已补齐 3 条近期真实问题 note，分别覆盖：tenant/library context 传播、旧链接恢复、frontend/backend limit contract 对齐；
  - `S0D-4A` 不再只有单条样例，而是具备一组可复用的前端问题档案。

### P3-C1-S1（assets 命名与归档规则｜2026-03-13）

- headSha：`c7527a231f3b578442fb58ba31b571b1cf1d42a4`
- artifacts：
  - `docs/UI&UX/assets/README.md`
- 期望（expected）：
  - 补齐 before/after screenshot、GIF、录屏的命名规则，降低后续证据收集摩擦。
- 观测（observed）：
  - `docs/UI&UX/assets/README.md` 已定义 `before/after/flow/mobile` 命名方式，并给出文件名示例，可直接用于后续补图。

## Recent changes（for traceability，可选）

- 2026-03-13：基于 `docs/UI&UX/UI-ISSUE-1.md` 的分析结果，正式建立 UI evidence-lite 轻轨，避免前端问题在“全部走重流程”和“完全不记录”之间摇摆。
- 2026-03-13：以 Book Timeline Chronicle 空白问题作为首条真实样例，证明该机制不是空模板，而是可直接承接近期前端修复的记录体系。
- 2026-03-13：补齐三条近期前端问题 note，并新增 `assets/` 命名规则，使 `S0D-4A` 从“单条样例”进化为“可持续使用的前端证据入口”。