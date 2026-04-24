# log-S0G-2A (Phase 2: Runbook ledger-aware operator surface and execution accounting)

---

**id**: `S0G-2A`
**kind**: `log`
**title**: `runbook ledger-aware operator surface and execution accounting v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Automation, Evidence, epic/s0, sub/2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-1A-workspace-backfill-branch-road-registration-and-full-auto-close-out.md`
  **reference_log_1**: `docs/logs/log-S0D-3A-runbook-stub.md`
  **reference_log_2**: `docs/logs/log-S0F-7C-old-log-decomposition-application-lane.md`
  **reference_log_3**: `docs/governance/contracts/_template-contract-record.md`
**issue_keyword**: `workflow`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/2`
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
**created**: `2026-04-20`
**updated**: `2026-04-20`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this packet.
- Day-level precision is acceptable while the lane is being opened and the new naming surfaces are still being fixed.
- `reviewed` should remain `pending` until the new runbook and run-ledger template surfaces are explicit enough to guide the first pilot runbook release.

## Decision / Outcome

**Decision**:

- `S0G-2A` opens the next `S0G` lane after the retrospective branch close-out packet: rebuild the runbook surface so it is no longer only a log-first thin summary, but a ledger-aware thin operator surface with repeatable execution accounting.
- The lane will treat current raw artifacts (`json`, `result`, `log`, screenshot, workflow output) as insufficient by themselves for long-term audit unless one dedicated run-ledger surface records their admission, review, approval, and downstream consumption.
- The first sample family for this lane is the GitHub lifecycle automation path `creation -> pr -> conclusion`, which should ultimately read as one contract-like runbook family such as `run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`.

**Default choices (phase defaults / v1)**:

- New runbooks should adopt contract-like family/release naming rather than the older slice-shaped `run-SxY-*` pattern when the governed surface is one stable reusable workflow family.
- New runbook-ledger files should bind to one specific runbook release and one specific admitted run, rather than acting as generic support-only routing ledgers.
- Parent run ledgers own repeated execution accounting; SUP ledgers own later evidence sharpening, approval-facing attachments, and verdict refinement for one admitted run.
- Existing legacy runbooks already moved under `docs/runbook/legacy/` remain historical reference material during this lane; they should not be rewritten wholesale inside the scaffold phase.
- This lane should publish new templates first, then prove them on one pilot sample, rather than trying to migrate the whole runbook inventory in one pass.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- This packet is expected to drive the first real runbook-ledger-aware template set, so the review summary should focus on naming, binding, and accounting boundaries.

**PR summary bullets**:

- Rebuild the runbook surface from log-first thin summary into a ledger-aware thin operator contract.
- Introduce contract-like naming for new runbooks and explicit parent/SUP run-ledger templates for repeated execution accounting.
- Prepare the GitHub lifecycle automation chain as the first pilot family for the new runbook plus run-ledger model.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md`
- Runbook: `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
- Evidence artifact: `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`

**Evidence Footer Source**:

- `P1-C1-S1` | artifact: `docs/runbook/_template-runbook.md`
- `P1-C1-S2` | artifact: `docs/runbook/_template-run-ledger.md`
- `P2-C1-S1` | artifact: `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`

## Definitions (optional)

- **ledger-aware thin operator surface**: one runbook that stays short and operator-facing, but explicitly binds to run-ledger accounting, evidence admission, and downstream write-back rules.
- **parent run ledger**: the durable accounting surface for one specific admitted run under one stable runbook family.
- **SUP ledger**: one later supplement packet that refines or strengthens the verdict of an already-admitted run-ledger row.
- **contract-like runbook naming**: runbook naming that uses stable family plus append-only release numbering, for example `run-WORKFLOW-GITHUB-001-...`.

## Constraints

- Do not treat raw artifacts alone as the durable accounting surface for repeated operator execution.
- Do not turn the new runbook template into a second full execution log.
- Do not migrate the entire legacy runbook inventory inside the scaffold phase.
- Do not reuse support-only contract ledgers directly for run execution accounting when the real problem is run-level admission and audit, not source-routing.

## Scope

- `P0`: contract (naming model, runbook/run-ledger boundary, parent vs SUP accounting model)
- `P1`: template surfaces (`docs/runbook/_template-runbook.md`, parent run-ledger template, SUP template)
- `P2`: pilot binding decision for the GitHub lifecycle automation sample family
- `P3`: next-lane execution decision on whether to open the first real sample runbook and run ledger

## Success Criteria (DoD)

- The lane fixes one explicit naming model for new runbooks, parent run ledgers, and SUP ledgers.
- The new runbook template states how it binds to parent run-ledger accounting instead of only listing output roots.
- The parent run-ledger template states how one admitted run, its evidence items, and its provenance chain are recorded.
- The SUP template states how later evidence sharpens or revises one admitted run without bypassing the parent run ledger.
- The lane leaves one explicit pilot target family for the first real execution sample.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the naming and boundary model for the new runbook/run-ledger family is explicit;
  - the new template files exist at their defended canonical paths;
  - the next lane for the first real pilot sample is fixed explicitly.

## P0 (Contract | v1)

### P0-C1-S1 (Naming model fixed | v1)

- New runbooks should use `run-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`.
- Parent run ledgers should use `ledger-run-<RUN-SEQUENCE>-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`.
- SUP ledgers should use `ledger-run-SUP-<SUP-SEQUENCE>-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`.

### P0-C1-S2 (Operator surface vs accounting surface fixed | v1)

- The runbook owns operator entry, stable semantics, evidence admission rule, and ledger binding.
- The parent run ledger owns admitted run rows, extracted evidence rows, and provenance/review state.
- The SUP ledger owns later evidence refinement for one admitted run row.

### P0-C1-S3 (Pilot family fixed | v1)

- The first pilot target should be the GitHub lifecycle automation chain `creation -> pr -> conclusion`.
- The defended sample naming target is `run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md` plus corresponding parent/SUP run ledgers.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0G-2A/P<phase>-C<cycle>-S<steps>: <summary>`

**Branch convention**:

- This lane should execute on `S0G-docs-management-v7` after the branch has been updated to include the latest `S4F` content.

**Commit discipline (recommended)**:

- Template and scaffold changes should be committed at `P*-C*-S*` granularity, then the first pilot sample should land as its own bounded follow-up unit.

## Plan (draft)

### P1 (Template surfaces)

- P1-C1-S1: publish the new ledger-aware runbook template with contract-like naming and lineage fields
- P1-C1-S2: publish parent and SUP run-ledger templates for admitted run accounting

### P2 (Pilot binding)

- P2-C1-S1: bind the GitHub lifecycle automation chain as the first sample family for the new naming and accounting model

### P3 (Next-lane decision)

- P3-C1-S1: decide whether the next packet should open the first real `WORKFLOW-GITHUB-001` runbook and `ledger-run-001-...` pilot surfaces

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: naming model fixed
- [x] `P0-C1-S2`: operator surface vs accounting surface fixed
- [x] `P0-C1-S3`: first pilot family fixed

### P1 (Template surfaces)

- [x] `P1-C1-S1`: ledger-aware runbook template published
- [x] `P1-C1-S2`: parent and SUP run-ledger templates published

### P2 (Pilot binding)

- [x] `P2-C1-S1`: first real pilot sample family opened

### P3 (Next-lane decision)

- [x] `P3-C1-S1`: next sample-execution lane fixed explicitly

## Current Status (recommended)

- `S0G-2A` is now scaffolded as the source log for the runbook-ledger-aware rebuild lane.
- The naming rule, template surfaces, and first pilot family are explicit enough to stop treating runbooks as log-first summaries only.
- `P2` is now fixed: the first real sample family surfaces exist at `run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md` and `support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`.
- `P3` was initially fixed as a direct move to real full-auto samples, but the next bounded contract follow-up is now `S0G-2B`: support-only ledger placement and patch-ledger bridge hardening before the first live sample batch.

## Evidence (reserved)

- Artifacts are the source of truth for this scaffold phase; this log records the template paths that define the lane.

### P1-C1-S1 (ledger-aware runbook template published | 2026-04-20)

- headSha: `WORKTREE`
- artifacts:
  - `docs/runbook/_template-runbook.md`
- expected:
  - the new runbook template should adopt contract-like family/release naming and explicit run-ledger binding.
- observed:
  - the template now binds each runbook release to one parent run-ledger surface, one supplementary ledger series, and one explicit evidence-admission rule.

### P1-C1-S2 (parent and SUP run-ledger templates published | 2026-04-20)

- headSha: `WORKTREE`
- artifacts:
  - `docs/runbook/_template-run-ledger.md`
  - `docs/runbook/_template-run-ledger-SUP.md`
- expected:
  - the new ledger templates should distinguish admitted run accounting from later evidence refinement.
- observed:
  - the parent template now owns run rows, evidence extraction rows, and provenance review, while the SUP template owns later verdict refinement for one admitted run row.

### P2-C1-S1 (WORKFLOW-GITHUB-001 sample runbook and parent ledger opened | 2026-04-20)

- headSha: `WORKTREE`
- artifacts:
  - `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  - `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- expected:
  - the first pilot family should move from template-only naming into one real runbook release plus one bound parent run ledger.
- observed:
  - the family-level runbook now exists with contract-like release naming, explicit lifecycle semantics, and explicit parent/SUP ledger binding;
  - the first parent run ledger also now exists with `RUN-001` opened as the planned first admitted full-auto sample surface under the new model.

### P3-C1-S1 (Next lane fixed to real full-auto sample batch | 2026-04-20)

- headSha: `WORKTREE`
- artifacts:
  - `docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md`
  - `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  - `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- expected:
  - after the first sample family surfaces exist, the lane should state whether another template round is needed or whether execution should move to real sample runs.
- observed:
  - the next bounded step after `S0G-2A` is now `S0G-2B`, which will harden support-only ledger placement and the patch-ledger bridge before the first real full-auto sample batch updates `RUN-001`.

## Recent changes (for traceability, optional)

- 2026-04-20: opened `S0G-2A` as the next docs-management lane after `S0G-1A`, focused on rebuilding runbooks into ledger-aware operator surfaces.
- 2026-04-20: published the new runbook, parent run-ledger, and SUP template files under `docs/runbook/`.
- 2026-04-20: opened the first real pilot family surfaces at `run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md` and `ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`, then fixed the next step as a real full-auto sample batch rather than another template-only round.