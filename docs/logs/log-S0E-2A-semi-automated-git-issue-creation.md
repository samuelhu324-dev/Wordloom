# log-S0E-2A (Phase 2: Semi-Automated Git Issue Creation Contract)

---

**id**: `S0E-2A`
**kind**: `log`
**title**: `semi-automated Git issue creation contract (title keywords, labels taxonomy, body scaffold, milestone mapping) v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Automation, epic/s0, sub/0e2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0D-6A-docs-management-v4.md`
  **reference_log_1**: `docs/logs/log-S4E-release-operating-model-and-governance.md`
  **reference_log_2**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_3**: `docs/roadmap/draft.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**created**: `2026-03-28`
**updated**: `2026-03-28`

---

## Decision / Outcome

**Decision**:

- `S0E-2A` 收口一版面向 structured logs 的半自动化 Git issue 创建合同，明确哪些字段可以 full-automation、哪些字段必须 semi-automation、哪些字段继续手工维护。
- v1 的目标不是直接生成高质量 issue 总结，而是优先稳定 title keyword vocabulary、labels taxonomy、body scaffold、milestone mapping 与 log frontmatter 的映射关系。
- 同步把 parent/phase log templates 增加 issue-aware frontmatter 字段，并明确“字段缺失时必须保守留空”的 fallback 规则。

**Default choices (phase defaults / v1)**:

- issue title 采用固定格式：`SxY-ZA: <fixed-keyword>/<specific subject>`；
- `SxY-ZA` 与 `<specific subject>` 优先从对应 log 直接复用，自动化重点放在 `<fixed-keyword>` 上；
- GitHub labels 必须先在仓库中预创建；automation 只选择既有 labels，不在运行时创建 ad-hoc labels；
- top-level labels 与 scope/sub labels 视为 full-automation，module labels 视为 semi-automation，priority labels 维持 zero-automation；
- issue body 只生成 scaffold：`Context`、`Definition of Done (DoD)` 与 `Links`，最终内容由人工确认；
- milestone 只有在 log frontmatter 存在明确字段且映射规则稳定时才自动带出，否则默认留空。

## Definitions (optional)

- **Fixed keyword**：issue title 中受控、有限词表的一层摘要词，例如 `policy`、`enforcement`、`workflow`。
- **Specific subject**：对应 log 本身的一句话主题，通常可从 log title/slug/summary 稳定复用。
- **Top-level label**：作用于 parent 与 child issue 的继承型 label，例如 `EVOLUTION`。
- **Scope label**：描述 issue 所属顶层系统层级的 label，例如 `s4/ops`、`s6/evidence & drills`。
- **Sub label**：描述 issue 在父子结构中的层级位置的 label，例如 `sub/0`、`sub/1`。
- **Module label**：描述受影响模块的 label，例如 `Search`、`Chronicle`、`Library`、`Tag`。
- **Issue scaffold**：自动生成的基础 issue 正文骨架，不等于最终人工完成的 issue 内容。

## Constraints

- 不允许通过自由文本猜测无限扩张 title keywords；关键词必须来自受控词表；
- 不允许在 automation 运行时创建新 labels；labels taxonomy 必须先在 GitHub 仓库中预创建；
- module labels 只能 best-effort 自动建议，不能假装已经知道最终改动范围；
- priority (`p0`/`p1`/...) 不纳入 v1 自动化；
- issue scaffold 不替代 log 的 `Decision / Outcome`、`DoD` 或 runbook 链接本身；
- 若 log frontmatter 未提供足够字段，automation 应回退为“保守留空 + 人工补充”，而不是冒险猜测。

## Scope

- `P0`: contract（title vocabulary、label taxonomy、body scaffold、milestone/frontmatter mapping）
- `P1`: template/frontmatter rollout（为 logs 增加 issue-aware fields 与命名约束）
- `P2`: scaffold generation path（定义最小生成入口与 sample 输出）
- `P3`: verify / rollout（用代表性 logs 验证 full/semi/zero automation 的边界）

## Success Criteria (DoD)

- 至少固定一版 `fixed-keyword` 受控词表，并说明每个词的使用边界；
- 至少固定一版 labels taxonomy，明确哪些 labels 属于 full / semi / zero automation；
- 至少明确回答“labels 是否需要预创建”：答案为是，并写入 contract；
- 至少定义一版 issue body scaffold，且能稳定回链对应 log；
- 至少定义一版 milestone mapping 规则，并明确“有字段才自动，没有字段就留空”；
- 至少给出一版 log frontmatter -> issue fields mapping；
- 至少保留 2~3 个代表性 sample（例如 `S4E-5B`、`S5B-4A`、`S6A-4A`）作为后续验证对象。

## Stability (what stable means)

- This log can be marked `stable` when:
  - The `P0-P3` contract, template changes, and representative scaffold samples have all been reviewed and accepted.
  - The title keyword vocabulary, label taxonomy, and body scaffold can be applied repeatedly without introducing ad-hoc naming drift.

## P0 (Contract | v1)

### P0-C1-S1 (Title keyword vocabulary and title mapping | v1)

- issue title 固定格式：`SxY-ZA: <fixed-keyword>/<specific subject>`；
- `<specific subject>` 默认复用对应 log 的现有主题表达，不把自由总结交给 automation；
- `<fixed-keyword>` 采用受控词表，v1 默认集合：
  - `contract`
  - `policy`
  - `authority`
  - `enforcement`
  - `records`
  - `workflow`
  - `automation`
  - `runtime`
  - `migration`
  - `evidence`
- parent/spine issue 允许额外受控词：
  - `governance`
  - `platform`
- keyword 选择原则：
  - 定义字段、接口、不变量、schema 边界时优先 `contract`；
  - 规则、允许/禁止条件、默认策略时优先 `policy`；
  - 角色边界、审批权、回滚权时优先 `authority`；
  - 实际 gate / block / allow / hard-stop 时优先 `enforcement`；
  - release/audit/evidence/action ledger 时优先 `records`；
  - operator path / step sequence 时优先 `workflow`；
  - GitHub Actions / CI / dispatch / orchestration 时优先 `automation`；
  - live execution / runtime package / worker/process 面时优先 `runtime`；
  - cutover / backfill / retirement / transition 时优先 `migration`；
  - structured proof / artifacts / result JSON 时优先 `evidence`；
  - control-plane / governance boundary 只在 parent 或少数 higher-level issues 中使用 `governance`；
  - framework/template/spec/harness reuse 主题才使用 `platform`。

### P0-C1-S2 (Labels taxonomy and automation-level matrix | v1)

- labels 在 GitHub 仓库中必须提前创建；v1 automation 不负责临时创建 label。
- v1 labels taxonomy 分三层：
  - top-level labels（全大写）
  - module labels（开头大写或 `module/...`）
  - scope/function labels（全小写）
- top-level labels：
  - 当前 baseline：`EVOLUTION`
  - 继承规则：parent issue 若带 `EVOLUTION`，child issues 默认也带 `EVOLUTION`
  - 自动化级别：`full-automation`
- module labels：
  - 例如：`Search`、`Chronicle`、`Library`、`Book`、`Bookshelf`、`Block`、`Tag`
  - 使用规则：只有在对应 log 已明确涉及该模块时才自动建议；若只是潜在影响面，则留给人工补充
  - 自动化级别：`semi-automation`
- scope/function labels：
  - scope labels：`s0/knowledge system`、`s1/sot`、`s2/projection`、`s3/observability`、`s4/ops`、`s5/security governance`、`s6/evidence & drills`
  - sub labels：`sub/0`、`sub/1`、`sub/2`、`sub/3`
  - function labels：当前 baseline 包括 `drills`
  - 使用规则：
    - `sX/...` 由 issue 的 `SxY` 前缀自动判定
    - `sub/n` 由 parent/child issue 层级自动判定
    - `drills` 可由 log 内容、title 或 tags 中出现 `drills/evidence` 时自动建议，若 parent/spine 未显式出现关键词则允许人工补
  - 自动化级别：
    - scope labels：`full-automation`
    - sub labels：`full-automation`
    - drills：`three-quarter automation`
- priority labels：
  - 例如：`p0`、`p1`
  - 自动化级别：`zero-automation`
  - 原因：priority 属于实际执行时的人为决策，不从 log 自动推断。

### P0-C1-S3 (Issue scaffold, milestone, and frontmatter mapping | v1)

- issue body scaffold v1：

```md
## Context
- <placeholder>

## Definition of Done (DoD)
- <placeholder>

## Links
- Log: <log-path>
- Runbook: <optional>
- Parent issue: <optional>
```

- body scaffold 只负责生成结构，不负责替用户写 final summary 或完整 DoD；
- `Context` 与 `Definition of Done (DoD)` 默认保留手工确认，自动化只插入 placeholder；
- `Links` 至少必须带对应 `log-xxxx.md`；若 log frontmatter 已有 `runbook`、`parent_log` 或 future `issue_parent`，则可一并带出；
- milestone mapping v1：
  - 推荐在 log templates 中新增 issue-aware 字段，例如：
    - `issue_keyword`
    - `issue_top_labels`
    - `issue_scope_labels`
    - `issue_module_labels`
    - `issue_milestone`
    - `issue_parent`
  - automation 仅在 `issue_milestone` 明确存在且与 GitHub milestone 名称一一对应时自动填写；
  - 若 field 缺失，则留空并进入人工确认，不做猜测。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-2A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S0E-2A` belongs to `S0E`, so related documentation and implementation changes should usually land on an `S0E-*` branch such as `S0E-docs-management-v5`.
- If template rollout and scaffold-generation implementation later need to be separated, prefer short-lived child branches under the `S0E-*` branch rather than creating unrelated top-level branches.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, template changes, or sample validation, try to `commit/push` promptly on the matching `S0E-*` branch.
- The normal rhythm is: accumulate commits on the matching scope branch at `P*-C*-S*` granularity, then periodically open a PR from that branch into `main` for human review and merge.

## Plan (draft)

### P1 (Template / Frontmatter Rollout)

- P1-C1-S1: add issue-aware frontmatter fields to parent/phase log templates
- P1-C1-S2: define fallback behavior when issue-specific fields are absent

### P2 (Scaffold Generation Path)

- P2-C1-S1: generate the first self-sample `log -> issue scaffold` artifact from `S0E-2A`
- P2-C1-S2: validate title, labels, and milestone fallback against the `S0E-2A` sample output

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: title keyword vocabulary and title mapping fixed
- [x] `P0-C1-S2`: labels taxonomy and automation-level matrix fixed
- [x] `P0-C1-S3`: issue scaffold, milestone, and frontmatter mapping fixed

### P1 (Template / Frontmatter Rollout)

- [x] `P1-C1-S1`: issue-aware fields added to log templates
- [x] `P1-C1-S2`: fallback behavior documented in templates or runbook notes

### P2 (Scaffold Generation Path)

- [x] `P2-C1-S1`: first self-sample issue scaffold artifact generated from `S0E-2A`
- [x] `P2-C1-S2`: title, labels, and milestone fallback validated against the `S0E-2A` sample

## Evidence (reserved)

- For this log, representative sample logs and future scaffold outputs will serve as the source of truth for validation evidence.

### P0-C1-S1S2S3 (contract scaffolded | 2026-03-28)

- headSha: `<git sha>`
- artifacts: `docs/roadmap/draft.md`
- expected:
  - title keywords are controlled rather than ad-hoc
  - labels taxonomy is split by automation level
  - body scaffold and milestone behavior are explicit
- observed:
  - first contract draft recorded in this phase log

### P1-C1-S1S2 (issue-aware template fields added | 2026-03-28)

- headSha: `<git sha>`
- artifacts:
  - `docs/logs/_template-log-parent-epic-spine.md`
  - `docs/logs/_template-log-phase-drills-evidence.md`
- expected:
  - parent/phase templates expose issue-aware frontmatter fields
  - blank fields explicitly mean "leave empty and request human confirmation"
- observed:
  - templates now document `issue_keyword`, labels, milestone, and parent issue fallback behavior

### P2-C1-S1S2 (first self-sample issue scaffold validated | 2026-03-28)

- headSha: `<git sha>`
- artifacts:
  - `docs/issues/issue-S0E-2A-semi-automated-git-issue-creation.md`
- expected:
  - title should be `S0E-2A: contract/semi-automated Git issue creation contract`
  - labels should include `EVOLUTION`, `s0/knowledge system`, and `sub/1`
  - module labels should remain blank because `issue_module_labels` is blank
  - milestone should remain blank because `issue_milestone` is blank
- observed:
  - first concrete `log -> issue scaffold` sample was generated from `S0E-2A`
  - title keyword, top-level label, and scope/sub labels matched the frontmatter-driven contract
  - blank module-label and milestone fields correctly stayed blank instead of being guessed

## Recent changes (for traceability, optional)

- 2026-03-28: first scaffold of `S0E-2A` created from the docs-management-v5 issue automation plan and normalized into a reusable phase-log contract.
- 2026-03-28: parent/phase log templates gained issue-aware frontmatter fields and explicit blank-field fallback guidance.
- 2026-03-28: first `S0E-2A -> issue scaffold` sample artifact was generated and validated under `P2`.