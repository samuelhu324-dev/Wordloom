# log-S0E-2B (Phase 2B: Real GitHub Issue Creation Automation)

---

**id**: `S0E-2B`
**kind**: `log`
**title**: `real GitHub issue creation automation (draft-generation -> create-issue) v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Automation, epic/s0, sub/0e2b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
  **reference_log_1**: `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
  **reference_log_2**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **reference_log_3**: `docs/roadmap/draft.md`
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

- `S0E-2B` 作为 `S0E-2A` 的 follow-up slice，只处理真正的 issue creation automation：从稳定的 draft-generation 入口推进到显式 opt-in 的 `create-issue` 模式。
- v1 先固定模式边界、脚本输入输出 contract 与 creation-side evidence contract，再进入本地 draft 生成实现与 GitHub create issue 真正调用。
- `S0E-2B` 不回头改写 `S0E-2A` 的 contract；`S0E-2A` 继续作为命名、labels、body scaffold 与 sample validation 的事实源。

**Default choices (phase defaults / v1)**:

- 默认模式必须是 `draft-generation`，不是 `create-issue`。
- 只有显式传入 `--create` 或等价 opt-in 开关时，脚本才允许触发真实 GitHub issue creation。
- create-side automation 仍不得创建 labels、不得猜 milestone、不得猜 module labels；这些限制继承自 `S0E-2A`。
- create-side success 的最小证据必须包括：source log、generated draft path、mode、warnings，以及在 `create-issue` 模式下的 issue number/url。

## Definitions (optional)

- **draft-generation**: 从一个 source log 生成 issue draft markdown 和结构化输出，但不调用 GitHub 创建真实 issue。
- **create-issue**: 在已有 draft-generation contract 基础上，显式调用 GitHub 创建真实 issue 的 opt-in 模式。
- **fail-closed**: 当 keyword、labels、milestone、parent issue 或 GitHub-side prerequisites 不明确时，脚本必须停止或留下 warning，而不是猜测补齐。
- **creation-side evidence**: 描述一次 draft generation 或 create-issue 执行结果的最小结构化记录。

## Constraints

- 不允许把 `create-issue` 做成默认行为。
- 不允许在 automation 运行时创建 GitHub labels 或 milestone。
- 不允许绕过 `S0E-2A` 已固定的命名、labels、body scaffold contract。
- `create-issue` 模式必须建立在先成功完成 `draft-generation` 的前提上。
- 在未明确 GitHub token、repo context 或 label existence 前，不允许把 create-side 失败默默降级为“看起来成功”。

## Scope

- `P0`: contract（mode boundary、script I/O contract、creation evidence contract）
- `P1`: local draft-generation implementation（`log_path -> docs/issues/*.md`）
- `P2`: real GitHub create issue entry（explicit opt-in `--create` path）
- `P3`: verify / rollout（用真实 issue creation run 验证 evidence 与回写 discipline）

## Success Criteria (DoD)

- 至少固定一版 `draft-generation` vs `create-issue` mode boundary；
- 至少固定一版脚本最小输入/输出 contract，并说明哪些字段允许 override；
- 至少固定一版 creation-side evidence contract，明确 draft mode 与 create mode 各自必须留下什么；
- 至少明确声明：真正创建 GitHub issue 的实现阶段属于 `S0E-2B`，不再回头挤进 `S0E-2A`；
- 后续 `P1/P2` 实现不需要再回头争论默认模式和失败语义。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 mode boundary、脚本入口、真实 creation evidence 与回写纪律都已经被验证；
  - default `draft-generation` path and explicit `create-issue` path can run without reintroducing naming or label drift.

## P0 (Contract | v1)

### P0-C1-S1 (Mode boundary and default safety | v1)

- 脚本必须至少有两个显式模式：
  - `draft-generation`
  - `create-issue`
- 默认模式固定为 `draft-generation`；
- `create-issue` 只能通过显式 flag（例如 `--create`）进入，不能因环境变量、token 存在或 operator 忘记传参而隐式开启；
- 若 `create-issue` 所需前提不满足（例如 token 缺失、repo 上下文不明确、label 校验失败），脚本必须 fail-closed 并返回非零结果，而不是自动退回“看起来像成功”的状态。

### P0-C1-S2 (Script input/output contract | v1)

- 最小必需输入：
  - `log_path`
- 常见可选输入：
  - `output_path`
  - `parent_issue`
  - `milestone_override`
  - `module_labels_override`
  - `strict_label_check`
  - `--create`
  - `--repo`
- 最小必需输出：
  - `title`
  - `top_labels`
  - `scope_labels`
  - `function_labels`
  - `module_labels`
  - `milestone`
  - `parent_issue`
  - `body_markdown`
  - `warnings`
  - `mode`
- 仅在 `create-issue` 模式下新增的必需输出：
  - `issue_number`
  - `issue_url`
  - `created_at`
- 若运行在 `draft-generation` 模式，以上 create-only 字段必须返回 `null` 或缺省，而不是伪造值。

### P0-C1-S3 (Creation evidence and write-back contract | v1)

- 每次脚本运行至少应留下一个结构化结果，最小字段包括：
  - `mode`
  - `log_path`
  - `draft_path`
  - `warnings`
  - `result`
- 当 `mode=create-issue` 时，结构化结果还必须包括：
  - `issue_number`
  - `issue_url`
  - `repo`
  - `labels_applied`
  - `milestone_applied`
- write-back contract 固定为：
  - draft-generation 不改 source log；
  - create-issue 成功后，允许在后续受控 docs update 中把 issue URL 回写到 source log `links.issue`；
  - create-issue 失败时不得产生半真半假的 write-back。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-2B/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S0E-2B` 相关改动默认继续落在 `S0E-*` 分支上（当前为 `S0E-docs-management-v5`），直到真正需要拆出实现分支为止。

**Commit discipline (recommended)**:

- 完成每个 `P*-C*-S*` 的关键内容后，应在 `S0E-*` 分支上及时 `commit/push`；
- 推荐顺序：先 `P0` 固定模式/IO/证据合同，再进入 `P1` 本地 draft 生成，最后进入 `P2` 真实 GitHub create issue。

## Plan (draft)

### P1 (Local draft-generation implementation)

- P1-C1-S1: implement local script path from `log_path` to `docs/issues/*.md`
- P1-C1-S2: emit a structured result for draft-generation mode

### P2 (Real GitHub create issue entry)

- P2-C1-S1: add explicit `--create` mode and repo/token prerequisite checks
- P2-C1-S2: create a real GitHub issue and emit creation-side evidence without implicit write-back

### P3 (Verify / Rollout)

- P3-C1-S1: validate one real draft-generation run and one real create-issue run
- P3-C1-S2: record write-back discipline and operator follow-up after successful creation

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: mode boundary and default safety fixed
- [x] `P0-C1-S2`: script input/output contract fixed
- [x] `P0-C1-S3`: creation evidence and write-back contract fixed

### P1 (Local draft-generation implementation)

- [x] `P1-C1-S1`: local draft-generation path implemented
- [x] `P1-C1-S2`: structured draft result emitted

### P2 (Real GitHub create issue entry)

- [ ] `P2-C1-S1`: explicit create mode and prerequisite checks implemented
- [ ] `P2-C1-S2`: real GitHub issue creation path implemented

### P3 (Verify / Rollout)

- [ ] `P3-C1-S1`: one draft-generation run and one create-issue run validated
- [ ] `P3-C1-S2`: write-back discipline recorded after successful creation

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P0-C1-S1S2S3 (real issue creation automation contract fixed | 2026-03-28)

- headSha: `<git sha>`
- artifacts:
  - `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  - `docs/runbook/run-S0E-log-to-issue-creation.md`
- expected:
  - default mode is `draft-generation`
  - real issue creation is opt-in only
  - input/output and evidence contracts are fixed before implementation starts
- observed:
  - `S0E-2B` opened as the dedicated follow-up slice for true GitHub issue creation automation
  - `P0` fixed mode boundary, script IO contract, and creation-side evidence/write-back discipline

### P1-C1-S1S2 (local draft-generation path implemented and emitted structured result | 2026-03-28)

- headSha: `<git sha>`
- artifacts:
  - `scripts/issues/gen_issue_draft.py`
  - `docs/issues/issue-S0E-2B-real-github-issue-creation-automation.md`
  - `docs/issues/issue-S0E-2B-real-github-issue-creation-automation.json`
- expected:
  - local script can generate a draft markdown file from `log_path`
  - local script emits a structured JSON result for `draft-generation` mode
  - `S0E-2B` self-sample keeps milestone and module labels blank without guessing
- observed:
  - `scripts/issues/gen_issue_draft.py` now generates markdown drafts under `docs/issues/`
  - the same run emits a JSON sidecar with `mode`, labels, warnings, and body markdown
  - the `S0E-2B` self-sample kept milestone, parent issue, and module labels blank while preserving `automation` as the fixed keyword

## Recent changes (for traceability, optional)

- 2026-03-28: `S0E-2B` opened as the dedicated follow-up slice for real GitHub issue creation automation after `S0E-2A` closed contract, samples, and manual procedure.
- 2026-03-28: `P1` added a local `log_path -> docs/issues/*.md` draft-generation script and JSON sidecar output for `draft-generation` mode.
