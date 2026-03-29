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
  **phase_log_4**: ``
  **phase_log_5**: ``
  **phase_log_6**: ``
**issue_keyword**: ``        # controlled fixed keyword; leave blank if title keyword should stay manual
**issue_top_labels**: ``     # comma-separated existing labels only
**issue_scope_labels**: ``   # comma-separated labels usually derived from scope / hierarchy
**issue_module_labels**: ``  # comma-separated module labels; leave blank when impact is not explicit
**issue_milestone**: ``      # exact GitHub milestone name; if blank, automation must leave milestone empty
**issue_parent**: ``         # parent issue reference if already known; otherwise leave blank
**issue_projects**: ``       # defaults to `wordloom Board` for logs under docs/logs in this workspace unless a different explicit project list is provided
**roadmap_path**: ``         # exact roadmap file that owns this spine's bridge, if any
**roadmap_milestone**: ``    # exact roadmap milestone, e.g. M3; leave blank when the spine spans multiple milestones
**roadmap_phase**: ``        # exact roadmap phase, e.g. M3-P2; leave blank when only child logs are ledgered in the roadmap
**roadmap_bridge_refs**: ``  # optional exact-slot refs when one spine/log needs to point at multiple roadmap slots; child-log extraction uses this as the exact multi-slot source
**pr_labels**: ``            # extra PR labels beyond inherited issue_top_labels / issue_scope_labels / issue_module_labels; add `drills` whenever the log contains substantive evidence/drill execution; all labels must already exist in GitHub
**pr_projects**: ``          # exact GitHub Project names for the PR; if blank, PR automation leaves project assignment empty by default
**pr_milestone**: ``         # exact GitHub milestone name for the PR; if blank, automation must leave the PR milestone empty
**pr_base**: ``              # exact PR base branch, e.g. main; if blank, dry-run may report it missing but must not guess another base
**pr_development_issue**: `` # exact issue number/url the PR should link in Development; if blank, automation must leave Development linkage empty
**created**: `YYYY-MM-DD`
**updated**: `YYYY-MM-DD`

---

## Decision / Outcome（结论区）

**Decision**:

- <本轮核心决定 1>
- <本轮核心决定 2>

**Default choices（默认基线 / v1）**（可选，但推荐在 parent/spine 明确）:

- <默认认证/默认存储/默认入口/默认环境/默认语义……>
- 若 `issue_*` 字段为空，automation 必须保守留空并要求人工确认，而不是猜测 title keyword、labels 或 milestone。
- 若 `pr_*` 字段为空，PR automation 必须保守留空并显式报告缺口，而不是复制 issue metadata 或猜测 base / milestone / development link。
- roadmap 与 logs 的机械桥接必须通过 `roadmap_path + roadmap_milestone + roadmap_phase` 明确声明；roadmap 内的正式 bridge ledger 默认只计入 child logs，而不是 parent/spine prose。

## PR Summary Inputs（可选）

- 仅当 parent/spine log 本身会作为 PR contract source 时填写；多数情况下，真正的 PR 描述仍应来自 child phase log。

**PR summary bullets**:

- <1-3 条面向 reviewer 的简短说明>

**PR checklist source**:

- 默认应指向具体 child log 的 execution checklist，而不是 parent/spine 自己重新发明一套 checklist。
- 若 parent/spine 只做聚合，应在这里写明“由哪些 child logs 组成该 PR”。

**PR links / evidence footer**:

- Parent log: `docs/logs/log-<ID>.md`
- Child log source(s): ``
- Issue: ``
- Evidence artifact: ``

- Generated PR body should keep `Evidence Footer` and `Development Link` as separate sections.
- `Evidence Footer` lines should prefer: `sha / ID / P*-C*-S* : summary`.

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

## Numbering & Commit Naming（编号与提交命名）

- 编号约定：`P<n>` 表示 Phase，`C<n>` 表示 Cycle，`S<n>` 表示 Step。
- Commit / PR 命名：
  - 基础形式：`<ID>/P<phase>-C<cycle>-S<steps>: <summary>`；
  - `<steps>` 可以是单个 step（`1`，即 `...-S1`），也可以是在同一 phase / cycle 下连续的多个 step 合并（如 `1S2`，即 `...-S1S2`）。
  - Multi-step 规则：只允许在 **同一 Phase + 同一 Cycle** 下合并多个 step；一旦跨 Phase 或跨 Cycle，必须拆成多次 commit。
  - 若一个 PR 一次性汇总多个完整 phase，应优先压缩成 phase 范围标题：
    - 连续 phase：`<ID>/P0-P3: <log title>`
    - 离散 phase：`<ID>/P0+P3: <log title>`
    - 离散 + 连续混合：`<ID>/P0+P3-P4: <log title>`
  - 若是后续补充型 PR，而不是一次性 phase 汇总，则直接使用精确 unit：`<ID>/P*-C*-S*: <一句话 summary>`。

**Branch 约定（建议）**:

- parent/spine log 负责一个 scope/index（例如 `S5B`、`S0D`），对应的实现/phase logs（如 `S5B-3A`、`S0D-2A`）在默认情况下应当：
  - 在与该 scope/index 同名前缀的分支上推进 P* 相关改动（例如：`S5B-*`、`S0D-*`）；
  - S5 系列安全治理工作优先落在 `S5B-...` 系列分支，S0 系列 docs/automation 工作优先落在 `S0D-...` 系列分支。
- 若一次演进同时涉及多个 scope/index，推荐拆分为多条分支/PR：每条分支聚焦一个 scope/index，便于回溯 `scope → branch → commits → artifacts` 的证据链。

**Commit 纪律（建议）**:

- 对于归属于某个 scope/index 的 phase log（例如 `S5B-4A` 隶属于 `S5B`）：
  - 完成每个 `P*-C*-S*` 的关键内容后，应在该 scope 的顶层工作分支（如 `S5B-security-governance-hard-gates`）上及时 `commit/push`；
  - 仅当某个 phase 体量较大、需要多人协同时，才在顶层分支之下再建短生命周期子分支，避免碎片化。
- 推荐节奏：按 `P*-C*-S*` 粒度在 scope 分支上积累小而清晰的 commit → 由 parent/spine 的维护人定期从这些 scope 分支向 `main` 发起 PR，并通过 Review/合并把证据链收口到主干。

## Recent changes（for traceability，可选）

- YYYY-MM-DD：<发生了什么变更，为什么要记录，如何追溯（commit/PR/run URL）>
