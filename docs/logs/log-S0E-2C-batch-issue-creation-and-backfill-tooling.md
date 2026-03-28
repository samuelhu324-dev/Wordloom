# log-S0E-2C (Phase 2C: Batch Issue Creation and Backfill Tooling)

---

**id**: `S0E-2C`
**kind**: `log`
**title**: `batch issue creation and issue relationship backfill tooling v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Automation, epic/s0, sub/0e2c`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  **reference_log_1**: `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
  **reference_log_2**: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  **reference_log_3**: `docs/runbook/run-S0E-log-to-issue-creation.md`
**issue_keyword**: `automation`
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

- `S0E-2C` 作为 `S0E-2B` 之后的新 follow-up slice，处理单条 issue creation 已经跑通之后的批量化与回填问题。
- v1 先把 batch selection、parent-child linking、milestone/backfill tooling 的 contract 收口，再决定是否进入单命令 bulk pipeline。
- `S0E-2C` 只扩展 operator tooling，不回头修改 `S0E-2A` 的命名合同，也不重做 `S0E-2B` 的单条 create path。

**Default choices (phase defaults / v1)**:

- 默认入口仍然必须是 dry-run / plan-first，而不是直接批量创建或批量回写。
- batch tooling 只允许消费已经符合 `S0E-2A` contract 的 source logs，不负责修复命名、labels 或 body 质量问题。
- parent-child linking、milestone apply、historical backfill 都必须是显式 opt-in 子动作，不能因为发现 issue 已存在就自动补写。
- 如果任何一条记录缺少受控输入（例如 issue number、parent issue、milestone 名称、source log 路径），工具必须留下 warning 或 fail-closed，而不是猜测补齐。

## Definitions (optional)

- **batch manifest**: 一组待处理 log/issue 项的显式输入清单，可来自文件、CLI 参数或筛选结果。
- **parent-child linking**: 在已存在 issue 之间补充父子关系或跟踪关系的受控操作。
- **backfill**: 对历史 issue 或 source log 进行受控补录，例如补 milestone、补 URL 回写或补 relationship evidence。
- **reconciliation**: 对 source log、draft artifact 与 GitHub 实际状态做差异检查，输出待确认计划而不是直接修复。

## Constraints

- 不允许把 bulk create、bulk link 或 bulk backfill 做成默认行为。
- 不允许在未建立 dry-run evidence 的情况下直接执行批量写操作。
- 不允许根据标题相似度或正文语义自动猜测 parent issue。
- 不允许批量工具在运行时创建 labels、milestones 或修改 `S0E-2A` 的受控 vocabulary。
- 一次批量执行必须能留下逐项结果，不能只返回一个模糊的整体成功状态。

## Scope

- `P0`: contract（batch manifest、dry-run semantics、bulk evidence contract）
- `P1`: batch draft/create planning（selection、filtering、plan output）
- `P2`: parent-child linking and relationship backfill
- `P3`: milestone/backfill/reconciliation tooling
- `P4`: optional single-command bulk pipeline after drills succeed

## Success Criteria (DoD)

- 至少固定一版 batch manifest 和 dry-run contract；
- 至少固定一版逐项结果输出 contract，区分 create/link/backfill 三类操作；
- 至少明确 parent-child linking 不做语义猜测，只接受显式输入或受控映射；
- 至少明确 milestone/backfill tooling 的 apply boundary 与回写边界；
- 至少有一轮 representative dry-run evidence，证明批量工具不会绕过 `S0E-2A/S0E-2B` 的 fail-closed 语义。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 batch contract、relationship tooling、milestone/backfill contract 已固定；
  - 至少一轮 dry-run 和一轮受控 apply 已留下逐项 evidence，且没有重新引入命名漂移或隐式写入。

## P0 (Contract | v1)

### P0-C1-S1 (Batch manifest and dry-run boundary | v1)

- 批量工具最小输入必须是显式 manifest 或等价的受控选择结果；
- v1 manifest 形状固定为：
  - `version`
  - `selection_filters`
  - `defaults`
  - `items`
- 默认模式固定为 dry-run / plan-only；
- dry-run 输出必须逐项列出建议动作，例如 `create`, `link-parent`, `apply-milestone`, `write-back`, `skip`, `error`；
- 任何会修改 GitHub 或 source log 的动作都必须通过显式 apply flag 单独开启。

### P0-C1-S2 (Relationship and backfill safety | v1)

- parent-child linking 只接受以下两类输入：
  - 显式 issue number / URL
  - 受控 mapping 文件中的稳定引用
- milestone/backfill 只允许对 manifest 中明确列出的对象生效；
- 若某条记录已存在冲突状态（例如不同 parent、不同 milestone、source log 与 GitHub URL 不一致），工具必须停在 reconciliation 结果，而不是自动覆盖。

### P0-C1-S3 (Bulk evidence contract | v1)

- 每次批量运行至少应留下一个结构化结果，最小字段包括：
  - `mode`
  - `manifest_path` 或 `selection_input`
  - `operation`
  - `total_items`
  - `planned_items`
  - `warnings`
  - `result`
- 逐项结果至少应包括：
  - `source_log`
  - `draft_path`
  - `result_path`
  - `issue_number`
  - `issue_url`
  - `planned_action`
  - `applied_action`
  - `status`
  - `title`
  - `warnings`

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-2C/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S0E-2C` 相关改动默认继续落在 `S0E-*` 分支上（当前为 `S0E-docs-management-v5`），直到 bulk tooling 需要独立实现窗口为止。

**Commit discipline (recommended)**:

- 完成每个 `P*-C*-S*` 的关键内容后，应在 `S0E-*` 分支上及时 `commit/push`；
- 推荐顺序：先固定 `P0` 的 manifest / dry-run / evidence contract，再进入 `P1-P3` 的 batch planning、relationship backfill 与 milestone tooling。

## Plan (draft)

### P1 (Batch planning)

- P1-C1-S1: define manifest shape and selection filters for multiple logs/issues
- P1-C1-S2: implement `scripts/issues/plan_issue_batch.py` and emit a dry-run plan artifact with per-item planned actions

### P2 (Parent-child linking)

- P2-C1-S1: define explicit relationship input contract and sample relationship manifest
- P2-C1-S2: implement and verify controlled parent-child linking/backfill flow

### P3 (Milestone / backfill / reconciliation)

- P3-C1-S1: define milestone and write-back reconciliation rules
- P3-C1-S2: implement and verify controlled backfill/apply flow

### P4 (Optional bulk pipeline)

- P4-C1-S1: combine validated subcommands into a single operator-facing bulk pipeline

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: batch manifest and dry-run boundary fixed
- [x] `P0-C1-S2`: relationship and backfill safety fixed
- [x] `P0-C1-S3`: bulk evidence contract fixed

### P1 (Batch planning)

- [x] `P1-C1-S1`: manifest shape and selection filters defined
- [x] `P1-C1-S2`: dry-run bulk plan artifact emitted

### P2 (Parent-child linking)

- [x] `P2-C1-S1`: explicit relationship input contract fixed
- [ ] `P2-C1-S2`: controlled parent-child linking/backfill flow verified

### P3 (Milestone / backfill / reconciliation)

- [ ] `P3-C1-S1`: milestone and write-back reconciliation rules fixed
- [ ] `P3-C1-S2`: controlled backfill/apply flow verified

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P0-C1-S1S2S3 (batch manifest, safety boundary, and evidence contract fixed | 2026-03-28)

- headSha: `a696f181715df1121d83d0b67969ebb66ff834b0`
- artifacts:
  - `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
  - `docs/runbook/run-S0E-log-to-issue-creation.md`
  - `docs/issues/issue-batch-S0E-2C-sample-manifest.json`
- expected:
  - one explicit manifest shape exists for batch planning
  - dry-run stays the default path
  - bulk evidence fields are fixed before any relationship or backfill apply mode starts
- observed:
  - `S0E-2C/P0` fixed the manifest shape as `version + selection_filters + defaults + items`
  - parent-child linking, milestone apply, and write-back remain explicit later phases
  - the runbook now includes a conservative batch manifest and plan contract

### P1-C1-S1S2 (batch planning script implemented and one dry-run plan artifact emitted | 2026-03-28)

- headSha: `a696f181715df1121d83d0b67969ebb66ff834b0`
- artifacts:
  - `scripts/issues/plan_issue_batch.py`
  - `docs/issues/issue-batch-S0E-2C-sample-manifest.json`
  - `docs/issues/issue-batch-S0E-2C-sample-plan.json`
  - `docs/issues/issue-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
  - `docs/issues/issue-S0E-2C-batch-issue-creation-and-backfill-tooling.json`
- expected:
  - batch planning can select logs from a manifest without creating GitHub issues
  - one dry-run plan artifact records per-item actions and warnings
  - logs that already have `links.issue` would be marked as `skip-existing-issue`
- observed:
  - `scripts/issues/plan_issue_batch.py` now consumes a manifest and reuses the single-log draft generator for per-item planning
  - one `S0E-2C` sample manifest can emit a dry-run plan artifact and fresh draft artifacts without any GitHub write action
  - the planner recorded `planned_action=create-issue`, `status=planned`, and conservative warnings for blank milestone / parent / module labels in a machine-readable JSON result

### P2-C1-S1 (explicit relationship input contract fixed | 2026-03-28)

- headSha: `<git sha>`
- artifacts:
  - `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
  - `docs/runbook/run-S0E-log-to-issue-creation.md`
  - `docs/issues/issue-relationship-S0E-2C-sample-manifest.json`
- expected:
  - relationship linking accepts only explicit parent/child issue references
  - `log_path` can be retained for traceability but not used as the resolution source
  - title similarity and body similarity stay out of scope for v1
- observed:
  - `S0E-2C/P2-C1-S1` fixed a narrow relationship manifest contract around explicit `parent_issue_*` and `child_issue_*` inputs
  - accepted relationship types were constrained to `child-of` and `parent-of`
  - a sample relationship manifest was added so the next implementation step can target a stable input shape

## Recent changes (for traceability, optional)

- 2026-03-28: created `S0E-2C` as the post-`S0E-2B` follow-up slice for batch issue creation, parent-child linking, and milestone/backfill tooling.
- 2026-03-28: completed `P0` and `P1` by fixing the batch manifest/evidence contract and adding a dry-run batch planning script plus sample manifest.
- 2026-03-28: completed `P2-C1-S1` by fixing a narrow relationship manifest contract that only accepts explicit parent/child issue references.