# log-S0F-3H (Phase 3H: recurring governance run model and ledger split)

---

**id**: `S0F-3H`
**kind**: `log`
**title**: `recurring governance run model and ledger split v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Governance, Runbook, Cleanup, Ledger, Template, epic/s0, sub/3h`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  **reference_log_1**: `docs/logs/log-S0F-3F-governance-contract-sweep-workflow.md`
  **reference_log_2**: `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  **reference_log_3**: `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
**issue_keyword**: `governance`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/3`
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
**created**: `2026-04-07`
**updated**: `2026-04-07`

---

## Decision / Outcome

**Decision**:

- `S0F-3H` opens the next follow-up slice for turning repeat governance work from long-lived origin logs into one reusable operating model.
- This slice exists because `S0F-3F` and `S0F-3G` proved two different kinds of recurring work, but both slices still carry a mixed burden:
  - they preserve the original design decisions for the workflow,
  - and they also keep accumulating later execution rounds as if they were the permanent operator surface.
- v1 therefore fixes one explicit split:
  - stable recurring method belongs in runbooks, packet shapes, and bounded templates,
  - per-run accounting belongs in logs, manifests, and evidence entries,
  - origin slices such as `S0F-3F` and `S0F-3G` remain the place where the model was established, but they should no longer be the only place where every future run is narrated.

**Default choices (phase defaults / v1)**:

- Keep logs as the ledger of what was done, not as the only evergreen operator manual.
- If the repo needs the same judgment or cleanup sequence more than once, extract the stable method into a runbook or a fixed packet template before opening more replay rounds.
- Open new bounded logs freely for materially distinct execution packages; do not force every later run back into `S0F-3F` or `S0F-3G` merely because those slices originated the method.
- Use `role first, disposition second` when splitting old structured logs: first decide where stable rule or procedure belongs, then decide whether the retained source log is `keep current`, `keep legacy`, `support-only`, or `defer cleanup`.
- A template is a reusable migration workflow, not a new filename convention or a requirement that every outlet always exist.
- `S0F-3F` and `S0F-3G` remain valid historical control slices, but future recurring execution should prefer smaller child ledgers, manifests, and runbook-driven packets.

## Scope

- `P0`: open `S0F-3H`, wire it into the `S0F` spine, and fix the boundary between origin logs, evergreen operator surfaces, and execution ledgers
- `P1`: define the recurring-run artifact set for governance work, including which responsibilities belong in runbook, packet template, log, manifest, and view
- `P2`: define naming and opening rules for future bounded execution logs so recurring work can branch into small ledgers without losing discoverability
- `P3`: define the first reusable templates for old structured-log extraction, including one clean sample lane and one mixed-role transformation lane
- `P4`: pilot the model on the next `S0F-1I` follow-up package so lifecycle-surface successor work no longer has to reopen `S0F-3G` as the primary operator worksheet

## Current Status

- `S0F-3H` is now opened as the next `S0F` follow-up slice because the repo has now outgrown the pattern where recurring governance work is driven mainly by appending more rounds to the original `3F` and `3G` logs.
- `P0` is now complete: the boundary is explicit that `S0F-3F` and `S0F-3G` are origin and control slices, while future recurring operation should move toward runbook-driven packets plus smaller per-run ledgers.
- The immediate next follow-up is `P1`: fix one artifact responsibility map so later work can answer, without ad hoc debate, which content belongs in a runbook, which content belongs in a template or packet, and which content belongs only in a run log.
- The first practical pilot after `P1` should still be the remaining `S0F-1I` lifecycle exact-path successor problem, but that work should be opened under the new `3H` operating model rather than by continuing to stretch `3G` into an indefinite operator notebook.

## Problem Statement

- `S0F-3F` successfully fixed how families are swept and adjudicated, but repeated future use of that method should not require one ever-growing slice log.
- `S0F-3G` successfully fixed how cleanup rounds are staged and defended, but repeated future use of that method should not require one ever-growing slice log either.
- `S0F-4A` now gives a role-boundary and disposition model, but the repo still needs one operating layer that says how those rules get reused across many future packages.
- Without that operating layer, the repo keeps mixing three responsibilities in the same place:
  - defining the stable method,
  - recording one bounded execution,
  - and preserving long-tail historical context.
- The result is that logs become both the design spec and the operator console, which makes them harder to reuse cleanly and harder to thin later.

## Operating Split v1

### Stable Surfaces

- `runbook`: repeatable operator procedure, stop rules, checks, and ordered execution steps
- `packet template`: bounded input shape for one family or one cleanup/rewrite run
- `view`: optional reader-facing snapshot for current state, family map, or outcome table when a stable summary is useful

### Ledger Surfaces

- `log`: what was decided and executed for one bounded package or one materially distinct round
- `manifest`: machine-readable or audit-friendly file list, candidate set, or dependency set for that run
- `evidence`: exact verification notes, commands, outputs, commit hashes, and publish state

### Legacy Handling Rule

- If an older structured log still mixes enduring procedure with historical run detail, export the enduring procedure first, then thin the original log to its slice-local convergence ledger before deciding its placement.
- The repo may open more than one log for the same broad area when that improves auditability; the constraint is not "one area, one endless log", but "one bounded purpose per log".

## First Template Direction

- Clean sample lane: use the `WF` family as the positive-control example where one source can mostly map cleanly into current contract plus light retained history.
- Mixed-role transformation lane: use `S0F-1I` as the example where stable rule and procedure must be exported first, the original log then thinned, and cleanup only judged after exact-path consumers are reduced.
- Reusable sequence:
  - map outlet ownership
  - export stable current rule and procedure
  - thin the original log to slice-local ledger
  - classify disposition only after remaining consumers are explicit

## Execution Checklist

- [x] `P0`: open `S0F-3H` and fix the origin-log versus recurring-operation boundary
- [ ] `P1`: define the artifact responsibility map for runbook, packet, log, manifest, and view
- [ ] `P2`: fix naming and opening rules for future bounded execution logs
- [ ] `P3`: publish the first reusable extraction templates
- [ ] `P4`: pilot the model on the next `S0F-1I` lifecycle-successor package

## Evidence

- `2026-04-07`: Opened `S0F-3H` to separate recurring governance operating method from the historical origin ledgers in `S0F-3F` and `S0F-3G`, and wired the new slice into the `S0F` parent spine as the next process-structure follow-up.
