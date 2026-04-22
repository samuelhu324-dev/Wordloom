# log-S0G-3F (Phase 3F: runbook revision-sequence and release-board operational-register governance)

---

**id**: `S0G-3F`
**kind**: `log`
**title**: `runbook revision-sequence and release-board operational-register governance v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Contract, Evidence, epic/s0, sub/3f`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-3E-workflow-github-issues-round-attempt-chronology-and-family-template-governance.md`
  **reference_log_1**: `docs/logs/log-S0G-3A-runbook-release-issue-concentration-and-ledger-naming-governance.md`
  **reference_log_2**: `docs/logs/log-S0G-3B-carrier-branch-cleanup-and-mainline-extraction-governance.md`
  **reference_log_3**: `docs/logs/log-S0G-3E-workflow-github-issues-round-attempt-chronology-and-family-template-governance.md`
  **reference_log_4**: `docs/governance/contracts/workflow/github/issues/DOC-WORKFLOW-GITHUB-ISSUES-0001-github-issues-as-canonical-work-breakdown.md`
  **reference_log_5**: `docs/logs/_template-log-phase-drills-evidence.md`
**issue_keyword**: `workflow`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/3f`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-22`
**updated**: `2026-04-22`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this packet.
- Day-level precision is acceptable while the repo is fixing naming and release-register rules before any broader template or automation rewrite is attempted.
- `reviewed` should remain `pending` until the repo fixes one defended revision-sequence grammar and one defended release-board operating rule for active runbook-family releases.

## Decision / Outcome

**Decision**:

- `S0G-3F` opens the next bounded follow-up after the current runbook-family governance rounds: the repo already has object-first runbook naming and concentrated release issues, but it still lacks one explicit rule for how repeated updates to the same release, parent ledger, `SUP`, or `PATCH` object should be named and tracked over time.
- Stable runbook-family object identity, revision sequence, and commit/PR packet identity are not the same thing. This lane fixes those three layers explicitly so later readers do not confuse one stable artifact such as `RUN-LEDGER-PATCH-001` with one later revision or one specific commit packet.
- The current repo can often reconstruct the first appearance of a release or ledger object only indirectly through source-log commits and later PR merges. This lane accepts that historical limitation for old packets, but fixes the forward rule: active runbook-family releases should now also be tracked through one lightweight release-board operational register.
- The first defended revision grammar is now fixed as `R<n>` sequence tokens:
  - single revision: `R01`
  - consecutive span: `R01-R03`
  - discontinuous set: `R01/R03`
- Revision sequence should not be appended to stable file identity. File names and stable artifact ids remain unchanged, while revision sequence belongs in reader-facing issue, PR, commit, and release-register surfaces.
- The release board should be treated as one operational register for active or retained runbook-family releases, not as a replacement for source logs, ledgers, or git history.

**Default choices (phase defaults / v1)**:

- Keep stable artifact identity unchanged in files, for example `RUN-RELEASE/WORKFLOW-GITHUB-ISSUES-001`, `RUN-LEDGER-001`, `RUN-LEDGER-SUP-001`, and `RUN-LEDGER-PATCH-001` remain the defended object identities.
- Record revision sequence separately, for example `RUN-LEDGER-PATCH-001/R02: <summary>`.
- Treat revision sequence as local to one stable artifact identity; opening a genuinely new bounded packet still requires a new stable object id, not a larger revision number on the old one.
- Use revision spans only for reader-facing summaries when the grouped revisions are truly one continuous or intentionally discontinuous set; do not use `R01-R03` or `R01/R03` as a replacement for exact per-revision rows in the release register.
- The release board issue for one runbook-family release should prefer current effective state over full historical replay.
- The release board should track at least:
  - canonical artifacts
  - current revision register
  - current mainline state
  - open follow-up PRs
- Do not rewrite old file names just to encode revision sequence.
- Do not treat the release board as a second source-log system; source logs still own contract reasoning, packet boundaries, and execution evidence.

## PR Summary Inputs (optional)

- This packet is expected to fix later release-board and runbook-family update discipline, so review should focus on naming layers and the release-register boundary first.

**PR summary bullets**:

- Separate stable artifact identity, revision sequence, and commit/PR packet identity for runbook-family objects.
- Fix `R01`-style revision grammar and keep revision sequence out of stable file names.
- Define one lightweight release-board operational register so active runbook-family releases can be tracked without pretending the board replaces source-log or git truth.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0G-3F-runbook-revision-sequence-and-release-board-operational-register-governance.md`
- Runbook: `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
- Evidence artifact: `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`

**Evidence Footer Source**:

- `P0-C1-S1` | artifact: `docs/logs/log-S0G-3A-runbook-release-issue-concentration-and-ledger-naming-governance.md`
- `P0-C1-S2` | artifact: `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
- `P0-C1-S3` | artifact: `docs/governance/contracts/workflow/github/issues/DOC-WORKFLOW-GITHUB-ISSUES-0001-github-issues-as-canonical-work-breakdown.md`

## Definitions (optional)

- **stable artifact identity**: the durable object identity for one runbook-family surface, such as `RUN-LEDGER-PATCH-001`, that should remain stable across later revisions.
- **revision sequence**: the ordered `R<n>` token that marks later defended revisions of the same stable artifact identity, such as `R01` or `R02`.
- **commit / PR packet**: one concrete delivery unit in git or GitHub that may implement part or all of one revision.
- **release-board operational register**: one lightweight GitHub issue plus board placement that tracks the currently effective artifact set and revision state for one active or retained runbook-family release.
- **mainline state**: the release-register standing of the current revision set, such as `branch-only`, `pr-open`, or `merged-to-main`.

## Constraints

- Do not encode revision sequence into stable file names or stable artifact ids.
- Do not treat one later update to the same artifact as proof that a new stable artifact identity is required.
- Do not keep repeated updates invisible inside unrelated source-log commit packets once the repo can instead register them on the release board.
- Do not force the release board to replay the full historical reasoning already owned by source logs, ledgers, and git history.
- Do not require parent/child issue topology for the release board when a lighter issue-plus-PR relation is sufficient.

## Scope

- `P0`: contract for stable artifact identity, revision-sequence grammar, and board-register boundary
- `P1`: minimum release-board issue template and required sections
- `P2`: operating-state rules for active versus retained releases and PR linkage
- `P3`: forward migration rule for new runbook-family packets and limited retrospective backfill for older packets

## Success Criteria (DoD)

- One explicit rule separates stable artifact identity, revision sequence, and commit/PR packet identity.
- One explicit revision grammar exists for single revision, consecutive spans, and discontinuous sets.
- One explicit rule states that revision sequence belongs in issue/PR/commit/register surfaces rather than file names.
- One explicit release-board issue model exists for active runbook-family releases.
- One explicit rule states what the board should track versus what must remain owned by source logs and git history.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the revision-sequence grammar is explicit;
  - the release-board register boundary is explicit;
  - the minimum section shape for release issues is explicit enough to guide the first live board write-back packet.

## P0 (Contract | v1)

### P0-C1-S1 (Stable artifact identity versus revision sequence | v1)

- Stable artifact identity and revision sequence are now fixed as separate reader concepts.
- Stable artifact identity answers: what durable object is being revised?
- Revision sequence answers: which later defended revision of that same object is this?
- The first defended examples are:
  - stable artifact identity: `RUN-LEDGER-PATCH-001`
  - single revision: `RUN-LEDGER-PATCH-001/R01`
  - later revision: `RUN-LEDGER-PATCH-001/R02`
- A later repair or update should continue the same stable artifact identity only when the bounded object itself remains the same.
- If the work opens a genuinely new bounded repair packet, open `PATCH-002` rather than inflating `PATCH-001/R03` into a second object.

### P0-C1-S2 (Revision grammar and reader-facing usage | v1)

- The defended revision grammar is now:
  - single revision: `R01`
  - consecutive span: `R01-R03`
  - discontinuous set: `R01/R03`
- Use `R01-R03` only when the grouped revisions are one continuous reader-facing range.
- Use `R01/R03` only when the grouped revisions are intentionally non-contiguous and the gap matters.
- Revision sequence should appear in:
  - issue titles when one issue update is revision-specific
  - PR titles when one PR carries one specific revision or grouped revision set
  - commit subjects when one commit packet is revision-specific
  - release-board revision registers
- Revision sequence should not appear in:
  - stable file paths
  - stable frontmatter object ids
  - canonical artifact filenames

### P0-C1-S3 (Release-board operational register boundary | v1)

- The release board is now defended as one lightweight operational register for active and retained runbook-family releases.
- One release-board issue should normally represent one stable runbook-family release, not one ledger packet or one patch packet.
- The minimum release-board issue sections are:
  - `Context`
  - `Definition of Done (DoD)`
  - `Canonical Artifacts`
  - `Revision Register`
  - `Mainline State`
  - `Open Follow-ups`
- `Definition of Done (DoD)` may group release, parent ledger, `SUP`, and `PATCH` rows, but each row should point to the relevant PR and current standing rather than replaying full source-log reasoning.
- The release board should track current effective release state, not serve as a second full historical ledger.
- The first defended operating states are:
  - `Drafting`
  - `Active`
  - `Retained`
- If a simpler board starts with only `Active` and `Done`, treat that as transitional UI shape rather than the final semantic contract.

### P0-C1-S4 (Historical backfill and forward rule | v1)

- Older releases whose first creation was buried inside source-log packets may be reconstructed partially from source-log commits, later PR merges, and git history.
- The repo does not need to perfectly backfill every old release before using the new release-board rule.
- The defended forward rule is stricter than the historical reconstruction rule:
  - old packets may be backfilled selectively;
  - new active packets should record stable artifact identity plus revision sequence explicitly on the release board.
- Retrospective backfill priority should prefer:
  - currently active releases
  - high-value retained releases
  - releases still receiving `SUP` or `PATCH` updates

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- Source-log work inside this lane uses `S0G-3F/P<phase>-C<cycle>-S<steps>: <summary>`.
- Reader-facing runbook-family object updates that later adopt the revision rule should prefer object identity plus revision sequence, for example `RUN-LEDGER-PATCH-001/R02: <summary>`.

**Branch convention**:

- Keep this lane on the active `S0G-*` docs-management branch until the revision-sequence and release-board operating rules are fixed.
- Do not open a separate board-only branch while the core rule is still moving.

**Commit discipline (recommended)**:

- Fix the contract first.
- Then publish the minimum release-board issue template or issue-body rule.
- Then backfill one live sample release issue with revision-register sections only after the rule is stable enough to survive one bounded execution packet.

## Plan (draft)

### P0 (Contract)

- P0-C1-S1: separate stable artifact identity from revision sequence
- P0-C1-S2: fix `R01` / `R01-R03` / `R01/R03` grammar and reader usage
- P0-C1-S3: define the release-board issue boundary and minimum sections
- P0-C1-S4: define limited historical backfill and stricter forward usage rules

### P1 (Board template / issue-body rule)

- P1-C1-S1: define the minimum release-board issue body shape for active runbook-family releases
- P1-C1-S2: define how DoD rows should point to PRs and current standing without recreating source-log hierarchy

### P2 (Operating-state rule)

- P2-C1-S1: fix active versus retained release states
- P2-C1-S2: fix how branch-only, PR-open, and merged-to-main states should appear in the release register

### P3 (First live write-back)

- P3-C1-S1: choose one active runbook-family release as the first board-register sample
- P3-C1-S2: backfill the first issue body using canonical artifacts, revision register, and mainline state only

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: separate stable artifact identity from revision sequence
- [x] `P0-C1-S2`: fix `R01` / `R01-R03` / `R01/R03` grammar and reader usage
- [x] `P0-C1-S3`: define the release-board issue boundary and minimum sections
- [x] `P0-C1-S4`: define limited historical backfill and stricter forward usage rules

### P1 (Board template / issue-body rule)

- [ ] `P1-C1-S1`: define the minimum release-board issue body shape for active runbook-family releases
- [ ] `P1-C1-S2`: define how DoD rows should point to PRs and current standing without recreating source-log hierarchy

### P2 (Operating-state rule)

- [ ] `P2-C1-S1`: fix active versus retained release states
- [ ] `P2-C1-S2`: fix how branch-only, PR-open, and merged-to-main states should appear in the release register

### P3 (First live write-back)

- [ ] `P3-C1-S1`: choose one active runbook-family release as the first board-register sample
- [ ] `P3-C1-S2`: backfill the first issue body using canonical artifacts, revision register, and mainline state only

## Current Status (recommended)

- `S0G-3F` is now opened as the next bounded runbook-governance follow-up under `S0G`.
- The repo now has one explicit contract for separating stable artifact identity, revision sequence, and commit/PR packet identity.
- The repo also now has one explicit rule that the release board should act as an operational register for active runbook-family releases rather than as a replacement for source logs or git history.
- The next step under this lane is to publish one minimum release-board issue-body rule and then test it on one live release issue sample.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

## Recent changes (for traceability, optional)

- 2026-04-22: Opened `S0G-3F` to fix revision-sequence grammar and release-board operational-register rules after the repo proved that stable runbook-family object identity and repeated updates were still easy to confuse in commit history and board tracking.