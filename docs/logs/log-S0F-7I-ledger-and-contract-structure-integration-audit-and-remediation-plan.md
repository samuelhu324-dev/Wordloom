# log-S0F-7I (Phase 7I: ledger and contract structure integration audit and remediation plan)

---

**id**: `S0F-7I`
**kind**: `log`
**title**: `ledger and contract structure integration audit and remediation plan`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Contract, Records, epic/s0, sub/7i`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-7H-actor-and-provenance-fields-for-evidence-review-governance.md`
  **reference_log_1**: `docs/logs/log-S0F-7E-supplement-sequencing-time-fields-and-historical-backfill-release-chronology.md`
  **reference_log_2**: `docs/logs/log-S0F-7F-log-and-roadmap-frontmatter-minimum-time-fields.md`
  **reference_log_3**: `docs/logs/log-S0F-7G-approval-facing-screenshot-evidence-review-and-attachment-protocol.md`
  **reference_log_4**: `docs/logs/log-S0F-7H-actor-and-provenance-fields-for-evidence-review-governance.md`
  **reference_log_5**: `docs/governance/contracts/_template-contract-record.md`
  **reference_log_6**: `docs/logs/_template-support-only-contract-release-ledger.md`
  **reference_log_7**: `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/7`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-14`
**updated**: `2026-04-14`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this log.
- Day-level values remain acceptable for this scaffold because the lane is being opened as one bounded audit-and-remediation packet rather than one second-precision operational run.

## Decision / Outcome

**Decision**:

- `S0F-7I` opens as the bounded follow-up after `S0F-7H` for one narrower docs-management problem: a mixed set of ledgers and chronology-first contracts now coexist in different maturity states, and the repo needs one explicit audit packet that first classifies which records already satisfy the current structure contract versus which records still lag on chronology, release, lineage, or statement-model requirements.
- This lane will first inventory and classify the current state, then ask for user review on the repair order, and only after that start the actual file-by-file remediation batches.

**Default choices (phase defaults / v1)**:

- Treat this lane as an integration audit first, not as an immediate mass rewrite lane.
- Separate `already-complete-enough`, `partially-aligned`, and `old-shape-needs-repair` records explicitly so later edits stay reviewable.
- Use the newer contract/ledger/SUP templates and the recent `S0A-1A` / `S0A-2A` samples as the active comparison baseline.
- Prefer one bounded review checkpoint with the user before beginning repair batches.
- Do not assume every older file must be rewritten to the newest maximum shape if the current repo contract does not actually require it for that file class.

## Audit Contract

- Contracts are evaluated against the current chronology-first contract baseline: family/release identity, chronology frontmatter, source/write-back chain, and statement/evolution structure where the family shape now expects it.
- Parent ledgers are evaluated against the current support-only ledger baseline: lifecycle header, routing/resolution structure, and row chronology audit when defended chronology is already known or explicitly carried by a linked SUP.
- SUP ledgers are evaluated against the current supplement baseline: sequence identity, lifecycle header, evidence table, attachment/review surfaces when applicable, time audit where defended, and actor/provenance surfaces when the current lane set now requires them.
- The first output of this lane is one classification matrix and one repair order proposal, not immediate mutation of every flagged file.

## Problem Statement

- The repo now has stronger rules from `7E`, `7F`, `7G`, and `7H`, but many existing ledgers and contracts were created before the current minimum structure was stabilized.
- As a result, the current corpus is mixed:
  - some files are already close to the current contract and mainly need retention
  - some files have partial alignment but still miss chronology or statement-model surfaces
  - some files remain older-shape records that need explicit upgrade before the repo can claim consistent structure
- Without one explicit audit packet, later repair work risks becoming opportunistic, inconsistent, or hard to review.

## Exported Sections / Outlet Ownership

- This slice starts as one `log-retained core + support-only audit planning` governance lane.
- The expected first landing is one stable audit matrix and one user-approved remediation order; actual file repairs remain later phases in the same lane or explicitly linked follow-ups.

**Outlet ownership**:

- `contract`: no-op by default; this lane audits existing contracts rather than opening one new substantive family contract
- `runbook`: no-op by default
- `view`: no-op by default; if a reader-facing audit index becomes necessary later, decide it after the first matrix exists
- `index/front-door`: no-op by default
- `disposition/placement`: audit grouping and repair order remain here until the user approves execution order
- `log-retained core`: the audit baseline, classification matrix, review checkpoints, and remediation plan remain here

## Definitions (optional)

- `already-complete-enough`: a file that materially satisfies the current repo contract for its document class and needs no immediate structural rewrite.
- `partially-aligned`: a file that already follows the intended family shape but still misses one or more currently required structural surfaces.
- `old-shape-needs-repair`: a file that still reads as an older contract or ledger shape and should be upgraded before being treated as current.
- `comparison baseline`: the current templates plus the newer live samples already accepted under `7E` through `7H`.

## Constraints

- Do not mix this audit lane with unrelated semantic rewrites of contract meaning.
- Do not force all older files into one identical maximum-shape pattern if the current document-class contract does not require it.
- Do not start a large repair batch before the audit matrix and user review checkpoint are recorded.
- Do not rewrite issue-only historical records to invent chronology or provenance detail that the source cannot defend.

## Scope

- `P0`: open `S0F-7I`, define the audit baseline, and identify the candidate file set for first-pass review
- `P1`: classify the selected ledgers and contracts into `already-complete-enough`, `partially-aligned`, and `old-shape-needs-repair`
- `P2`: present the first-pass findings, ask for user preference on repair order, and freeze one bounded remediation sequence
- `P3`: begin the actual structure-remediation batches only after the user approves the first repair order

## Success Criteria (DoD)

- The repo has one explicit first-pass classification for the selected ledgers and contracts.
- The audit packet explains which current rules are being used as the comparison baseline.
- The lane records which files already meet the current contract well enough to retain.
- The lane records which files still need repair and in what order they should be addressed.
- The first remediation batch does not start until the user has reviewed the classification and order.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the audit baseline is explicit
  - the selected file set is classified
  - the remediation order is reviewed and fixed
- `stable` for this lane does not require all repairs to be complete; it requires the audit and repair plan to be explicit enough for later execution.

## P0 (Audit boundary | v1)

### P0-C1-S1 (Open `S0F-7I` as the integration-audit follow-up)

- Open one bounded follow-up lane after `S0F-7H` for structure integration audit across selected ledgers and chronology-first contracts.

### P0-C1-S2 (Fix the comparison baseline before file-by-file repair)

- The active comparison baseline is the current contract record template, the parent-ledger template, the SUP template, and the newer `S0A-1A` / `S0A-2A` samples already aligned under `7E` through `7H`.

### P0-C1-S3 (Fix the first audit file set)

- First-pass file set under review in this lane:
  - `docs/governance/contracts/workflow/DOC-WORKFLOW-0001-structured-doc-refinement-pipeline.md`
  - `docs/governance/contracts/workflow/logs/DOC-WORKFLOW-LOGS-0001-structured-log-identity-and-front-matter.md`
  - `docs/governance/contracts/workflow/lifecycle/DOC-WORKFLOW-LIFECYCLE-0001-legacy-taxonomy-cutover-and-stub-preservation.md`
  - `docs/governance/contracts/workflow/labs/DOC-WORKFLOW-LABS-0001-tools-labs-and-snapshots.md`
  - `docs/governance/contracts/workflow/labs/DOC-WORKFLOW-LABS-0002-labs-snapshot-evidence-package-governance.md`
  - `docs/governance/contracts/workflow/runbook/DOC-WORKFLOW-RUNBOOK-0001-projection-operator-rebuild-replay-and-failure-recovery.md`
  - `docs/governance/contracts/workflow/github/issues/DOC-WORKFLOW-GITHUB-ISSUES-0001-github-issues-as-canonical-work-breakdown.md`
  - `docs/governance/contracts/workflow/github/issues/title/DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-issue-title-encodes-level-and-category.md`
  - `docs/governance/contracts/workflow/github/issues/tags/DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-issue-tags-follow-role-based-naming.md`
  - `docs/governance/contracts/workflow/github/projects/DOC-WORKFLOW-GITHUB-PROJECTS-0001-project-views-support-execution-priority.md`
  - `docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md`
  - `docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md`
  - `docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md`
  - `docs/logs/support-only/ledger-SUP-S0A-2A-001-tools-workflow-log-lab-runbook-adr.md`
  - `docs/logs/support-only/ledger-SUP-S0A-2A-002-labs-early-failure-management-and-pre-drills-shape.md`
  - `docs/logs/support-only/ledger-S0B-1A-tools-labs-and-snapshots.md`
  - `docs/logs/support-only/ledger-S0B-2A-tools-scripts-and-snapshots-management.md`
  - `docs/logs/support-only/ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter.md`

## Plan (draft)

### P1 (First-pass classification)

- `P1-C1-S1`: classify selected chronology-first contracts against the current contract baseline
- `P1-C1-S2`: classify selected parent ledgers and SUP ledgers against the current ledger/SUP baseline

### P2 (Review checkpoint and repair order)

- `P2-C1-S1`: summarize which files already look complete enough versus partial versus old-shape
- `P2-C1-S2`: ask the user to confirm the repair order before mutation begins

### P3 (Remediation batches)

- `P3-C1-S1`: repair the first approved batch of contracts or ledgers
- `P3-C1-S2`: validate and write back the first approved remediation batch
- `P3-C2-S1`: repair the second approved batch of contracts or ledgers
- `P3-C2-S2`: validate and write back the second approved remediation batch

## Execution Checklist (unchecked)

### P0 (Audit boundary)

- [x] `P0-C1-S1`: open `S0F-7I` as the integration-audit follow-up
- [x] `P0-C1-S2`: fix the comparison baseline before file-by-file repair
- [x] `P0-C1-S3`: fix the first audit file set

### P1 (First-pass classification)

- [x] `P1-C1-S1`: classify selected chronology-first contracts against the current contract baseline
- [x] `P1-C1-S2`: classify selected parent ledgers and SUP ledgers against the current ledger/SUP baseline

### P2 (Review checkpoint and repair order)

- [x] `P2-C1-S1`: summarize which files already look complete enough versus partial versus old-shape
- [x] `P2-C1-S2`: ask the user to confirm the repair order before mutation begins

### P3 (Remediation batches)

- [x] `P3-C1-S1`: repair the first approved batch of contracts or ledgers
- [x] `P3-C1-S2`: validate and write back the first approved remediation batch
- [x] `P3-C2-S1`: repair the second approved batch of contracts or ledgers
- [x] `P3-C2-S2`: validate and write back the second approved remediation batch

## Verified First-Pass Classification

### Already Complete Enough

- `docs/governance/contracts/workflow/runbook/DOC-WORKFLOW-RUNBOOK-0001-projection-operator-rebuild-replay-and-failure-recovery.md`
  - already carries `contract_family`, `contract_release`, chronology frontmatter, and statement-table structure expected by the current contract baseline
- `docs/governance/contracts/workflow/github/projects/DOC-WORKFLOW-GITHUB-PROJECTS-0001-project-views-support-execution-priority.md`
  - now carries chronology frontmatter, statement/evolution tables, and the current `S0A-1A` write-back chain
- `docs/governance/contracts/workflow/labs/DOC-WORKFLOW-LABS-0002-labs-snapshot-evidence-package-governance.md`
  - already carries release identity, chronology frontmatter, and statement/evolution structure; any remaining work is optional polish, not first-pass structural repair
- `docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md`
  - now carries lifecycle fields, explicit routing table, and row chronology audit for the defended screenshot-backed row
- `docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md`
  - now carries sequence identity, lifecycle header, attachment review surfaces, evidence time audit, and actor/provenance review
- `docs/logs/support-only/ledger-SUP-S0A-2A-002-labs-early-failure-management-and-pre-drills-shape.md`
  - already carries sequence identity, lifecycle header, and evidence time audit with direct-evidence verdicts

### Partially Aligned And Needing Bounded Upgrade

- `docs/governance/contracts/workflow/logs/DOC-WORKFLOW-LOGS-0001-structured-log-identity-and-front-matter.md`
  - has release-family identity but still reads as a lighter contract shape without the full chronology-first statement/evolution structure now used by current workflow children
- `docs/governance/contracts/workflow/lifecycle/DOC-WORKFLOW-LIFECYCLE-0001-legacy-taxonomy-cutover-and-stub-preservation.md`
  - has release-family identity but still needs confirmation against the current chronology-first statement/evolution baseline
- `docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md`
  - now has row chronology audit, but its header and row surfaces still need one bounded review against the newer lifecycle-field baseline already applied on `S0A-1A`
- `docs/logs/support-only/ledger-SUP-S0A-2A-001-tools-workflow-log-lab-runbook-adr.md`
  - already has sequence identity and lifecycle header, but it still predates the newer attachment-review and actor/provenance surfaces and should be checked for whether those are required for its evidence type

### Older Shape Or Structure-Light Relative To Current Rules

- `docs/governance/contracts/workflow/DOC-WORKFLOW-0001-structured-doc-refinement-pipeline.md`
  - still reads as an early broad workflow contract without current release-family identity, chronology frontmatter, or statement/evolution structure
- `docs/governance/contracts/workflow/labs/DOC-WORKFLOW-LABS-0001-tools-labs-and-snapshots.md`
  - remains materially older than `LABS-0002` and should be checked for full alignment to the current chronology-first family grammar
- `docs/governance/contracts/workflow/github/issues/DOC-WORKFLOW-GITHUB-ISSUES-0001-github-issues-as-canonical-work-breakdown.md`
  - has family/release identity but still reads as structure-light against the newer chronology-first contract pattern now used by `PROJECTS-0001`
- `docs/governance/contracts/workflow/github/issues/title/DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-issue-title-encodes-level-and-category.md`
  - still lacks the stronger chronology-first structure expected by current child-family contracts
- `docs/governance/contracts/workflow/github/issues/tags/DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-issue-tags-follow-role-based-naming.md`
  - still lacks the stronger chronology-first structure expected by current child-family contracts
- `docs/logs/support-only/ledger-S0B-1A-tools-labs-and-snapshots.md`
  - remains an older parent-ledger shape without the newer lifecycle header and chronology-surfaces now used by current active parents
- `docs/logs/support-only/ledger-S0B-2A-tools-scripts-and-snapshots-management.md`
  - remains an older parent-ledger shape without the newer lifecycle header and chronology-surfaces now used by current active parents
- `docs/logs/support-only/ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter.md`
  - remains an older parent-ledger shape and still needs explicit review against the newer lifecycle-field baseline

## Proposed Repair Order For User Review

- Batch A: older workflow contracts with the biggest structure gap
  - `DOC-WORKFLOW-0001`
  - `DOC-WORKFLOW-GITHUB-ISSUES-0001`
  - `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001`
  - `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001`
- Batch B: older and partial support-only ledgers
  - `ledger-S0B-1A`
  - `ledger-S0B-2A`
  - `ledger-S0B-3A`
  - `ledger-S0A-2A`
- Batch C: bounded follow-up polish only if still needed after A and B
  - `DOC-WORKFLOW-LABS-0001`
  - `DOC-WORKFLOW-LOGS-0001`
  - `DOC-WORKFLOW-LIFECYCLE-0001`
  - `ledger-SUP-S0A-2A-001`

- Preferred default execution order:
  - start with Batch A because the broadest contract-shape mismatch sits there and it will sharpen the comparison target for the ledgers that follow
  - then run Batch B because the older parent-ledger surfaces still lag the newer active lifecycle pattern
  - leave Batch C as conditional cleanup after the larger mismatches are repaired

## Current Status (recommended)

- `S0F-7I` is now opened as the bounded follow-up after `S0F-7H` for structure integration audit across selected ledgers and chronology-first contracts.
- The lane is intentionally audit-first: it should classify current state and freeze repair order before editing the older records.
- `P1-C1-S1` is now complete: the selected chronology-first contracts are now classified against the current family/release, chronology, and statement-model baseline.
- `P1-C1-S2` is now complete: the selected parent ledgers and SUP ledgers are now classified against the current lifecycle, sequence, chronology, and review-surface baseline.
- `P2-C1-S1` is now complete: the first-pass findings are now grouped into `already-complete-enough`, `partially-aligned`, and `old-shape-needs-repair`.
- `P2-C1-S2` is now complete: the lane now records one proposed repair order for user review before any actual remediation batch starts.
- `P3-C1-S1` is now complete: the first approved repair batch now upgrades the Batch B ledgers with current lifecycle-header structure, and `S0B-3A` now also exposes stable row ids aligned to the current parent-ledger template.
- `P3-C1-S2` is now complete: the repaired ledgers now give the later contract batch a cleaner bridge surface for chronology, routing, and row-level source references.
- `P3-C2-S1` is now complete in workspace: the second approved repair batch now upgrades the broad workflow parent and GitHub-Issues family files to the current chronology-first contract structure without reopening their owned meaning.
- `P3-C2-S2` is now complete in workspace: the repaired contract files now expose defended release chronology, clause ids, and stable source-basis anchors aligned to the repaired `S0A-2A` and `S0A-1A` ledger bridge.
- The next step is to decide whether `Batch C` is still needed for bounded polish on the partially-aligned `DOC-WORKFLOW-LOGS-0001` and `DOC-WORKFLOW-LIFECYCLE-0001` files.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths when the lane starts mutating contracts or ledgers.
- This section stays empty until the first audit or remediation patch is actually landed.

### P1-C1-S1S2 + P2-C1-S1S2 (First-pass structure classification and repair-order proposal fixed | 2026-04-14)

- headSha: `132150235`

- artifacts:
  - `docs/logs/log-S0F-7I-ledger-and-contract-structure-integration-audit-and-remediation-plan.md`
- expected:
  - the lane should convert the initial file set into one explicit first-pass classification using the current contract, parent-ledger, and SUP baselines
  - the lane should record one repair-order proposal so later remediation batches can start only after user review
- observed:
  - the selected corpus now reads as one three-way split between already-complete-enough files, partially-aligned files, and older-shape records with larger structure gaps
  - the broadest first-pass repair pressure currently sits on the early workflow parent/child contracts and the older `S0B` parent ledgers, while newer `S0A-1A`, `PROJECTS-0001`, `RUNBOOK-0001`, and `LABS-0002` surfaces are already materially close to the active baseline

### P3-C1-S1S2 (Batch B ledger repair and contract-bridge readiness fixed in workspace | 2026-04-14)

- headSha: `094acac97`

- artifacts:
  - `docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md`
  - `docs/logs/support-only/ledger-S0B-1A-tools-labs-and-snapshots.md`
  - `docs/logs/support-only/ledger-S0B-2A-tools-scripts-and-snapshots-management.md`
  - `docs/logs/support-only/ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter.md`
  - `docs/logs/log-S0F-7I-ledger-and-contract-structure-integration-audit-and-remediation-plan.md`
- expected:
  - the first approved ledger batch should repair the structural bridge surfaces most needed by the later contract batch without reopening contract meaning itself
  - older ledgers should at least expose defended lifecycle headers, and any missing stable row-id surface should be repaired before contract-side statement/basis cleanup continues
- observed:
  - `ledger-S0A-2A`, `ledger-S0B-1A`, `ledger-S0B-2A`, and `ledger-S0B-3A` now expose current lifecycle headers using defended repo-side dates or explicit `pending` acceptance where current parent acceptance is not yet defended
  - `ledger-S0B-3A` now also exposes stable `row id` values and a row-id map, bringing its routing table materially closer to the active parent-ledger template before later contract repair begins

### P3-C2-S1S2 (Batch A broad-parent and GitHub-Issues family repair fixed in workspace | 2026-04-14)

- artifacts:
  - `docs/governance/contracts/workflow/DOC-WORKFLOW-0001-structured-doc-refinement-pipeline.md`
  - `docs/governance/contracts/workflow/github/issues/DOC-WORKFLOW-GITHUB-ISSUES-0001-github-issues-as-canonical-work-breakdown.md`
  - `docs/governance/contracts/workflow/github/issues/title/DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-issue-title-encodes-level-and-category.md`
  - `docs/governance/contracts/workflow/github/issues/tags/DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-issue-tags-follow-role-based-naming.md`
  - `docs/logs/log-S0F-7I-ledger-and-contract-structure-integration-audit-and-remediation-plan.md`
- expected:
  - the second approved repair batch should align the oldest workflow parent and GitHub-Issues family files to the current chronology-first contract structure without changing their owned rule meaning
  - the repaired contracts should expose defended release chronology fields, explicit clause ids, and stable source-basis anchors that match the now-repaired ledger bridge
- observed:
  - `DOC-WORKFLOW-0001`, `DOC-WORKFLOW-GITHUB-ISSUES-0001`, `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001`, and `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` now expose release chronology fields, contract statement tables, and statement-evolution tables aligned to the current contract template
  - the repaired contract clauses now point back to stable ledger row ids from `S0A-2A` and `S0A-1A`, making the parent boundary and child-rule ownership easier to audit before any optional `Batch C` polish begins