# log-S0F-3G (Phase 3G: governance cleanup staging and phased file cleanup)

---

**id**: `S0F-3G`
**kind**: `log`
**title**: `governance cleanup staging and phased file cleanup v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Governance, Cleanup, Legacy, Registry, epic/s0, sub/3g`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-3F-governance-contract-sweep-workflow.md`
  **reference_log_1**: `docs/logs/log-S0F-3E-governance-registry-lineage-and-legacy-handling.md`
  **reference_log_2**: `docs/logs/log-S0F-3F-governance-contract-sweep-workflow.md`
  **reference_log_3**: `docs/governance/INDEX.md`
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
**created**: `2026-04-06`
**updated**: `2026-04-06`

---

## Decision / Outcome

**Decision**:

- `S0F-3G` opens the next follow-up slice for staged governance-file cleanup after the registry lineage model and bounded sweep workflow are already in place.
- This slice exists because `S0F-3E` and `S0F-3F` deliberately preserved many legacy, support-only, and helper files so current-state meaning stayed safe during admission and residual sweeps, but that same preservation now leaves a later cleanup problem that should not be solved by ad hoc bulk deletion.
- v1 therefore treats cleanup as a governed staging problem rather than as a one-shot folder tidy-up:
  - one bounded cleanup inventory
  - one safety model for keep or move or delete decisions
  - one explicit round manifest per cleanup pass so larger file sets can be reduced in multiple defended rounds

**Default choices (phase defaults / v1)**:

- Clean up one bounded file family or one explicit manifest at a time; do not run one repo-wide deletion pass.
- Current-state readability is more important than file-count reduction.
- If a file still carries active reader value, redirect value, or traceability value that cannot yet be relocated safely, keep it.
- If uncertainty remains about references, ownership, or later audit value, classify the file as `defer cleanup` rather than deleting it.
- Generated, scratch, and reproducible helper outputs may be removed earlier than legacy contract, lineage, or sweep history files.
- `INDEX.md`, active current contracts, and the stable source-owner logs for admitted semantics are out of scope for destructive cleanup unless a later bounded round proves otherwise.

## Scope

- `P0`: open `S0F-3G`, wire it into the `S0F` spine, and define the cleanup problem boundary explicitly
- `P1`: inventory cleanup candidate classes and distinguish current-state files from legacy/support-only/reproducible residue
- `P2`: fix the cleanup decision model, including `keep current`, `keep legacy`, `move`, `delete reproducible`, and `defer cleanup`
- `P3`: define one bounded cleanup manifest shape and evidence contract for multi-round execution
- `P4`: execute the first bounded cleanup round only after the manifest and stop rules are explicit
- `P5`: repeat bounded cleanup rounds until the candidate set converges without harming current-state readability

## Current Status

- `S0F-3G` is now opened as the next `S0F` follow-up slice for staged governance-file cleanup after the bounded sweep workflow has already closed the currently defended admission and residual-family questions.
- The immediate motivation is already concrete: `S0F-3E` preserved legacy lineage files and `S0F-3F` preserved residual-family sweep views so the front door stayed safe, which now means later cleanup must distinguish what is still reader-facing history from what is only bounded helper residue.
- `P0` is now complete: the cleanup problem is now separated from admission work, and future file reduction can proceed in explicit rounds instead of reopening `S0F-3F` for mixed cleanup-plus-judgment passes.
- The immediate next follow-up is `P1`: inventory one first candidate cleanup set without making destructive changes yet.

## Problem Statement

- The governance registry is now readable, but the repo intentionally retains more than one class of non-current file:
  - deprecated legacy contracts with redirects
  - support-only sweep views
  - backfill notes and helper files
  - reproducible scratch or generated outputs that may no longer need first-class placement
- These file classes do not all deserve the same treatment.
- If the repo deletes too aggressively, it can break lineage, sweep traceability, or future audit defensibility.
- If the repo never cleans up at all, support-only and reproducible residue will keep obscuring the current governance model.
- The system therefore needs one explicit cleanup discipline that decides what to keep, what to move, what to delete, and what to defer.

## Cleanup Boundary v1

### In Scope

- governance files under `docs/governance/contracts/` that are already non-current and may later be relocated, consolidated, or left in place by explicit rule
- governance views under `docs/governance/views/` that may now be support-only or one-round helper surfaces
- directly related sweep or legacy helper notes under `docs/logs/` when later rounds prove they are redundant rather than source-owned semantic records
- directly related reproducible helper outputs or scratch artifacts when they are no longer required as first-class checked-in files

### Out of Scope

- `docs/governance/INDEX.md`
- active current contracts still used as front-door readers
- the source-owner logs for currently admitted governance semantics
- unrelated repo cleanup outside the governance and docs lifecycle surface

## P1 Baseline (Candidate classes)

### Candidate File Classes

- `current-state file`:
  - active reader-facing file that must remain in place for current interpretation
- `legacy redirect file`:
  - non-current file that still preserves old IDs, old links, or deterministic redirect meaning
- `support-only sweep helper`:
  - view or note that explains one bounded adjudication or migration result but may later be movable or consolidatable
- `reproducible helper output`:
  - generated or scratch-like output that can be recreated from source logs, manifests, or scripts
- `unclear cleanup candidate`:
  - file whose reader value or replacement path is not yet defended strongly enough for movement or deletion

### Required Inventory Fields

- Every cleanup candidate row should record at least:
  - `candidate path`
  - `candidate class`
  - `current reader value`
  - `current semantic owner, if any`
  - `proposed cleanup outcome`
  - `reason for outcome`
  - `preconditions before write`
  - `cleanup-round scope`

## P2 Baseline (Cleanup outcomes)

### Allowed Outcomes

- `keep current`:
  - the file remains in place because it is still part of current-state reading
- `keep legacy`:
  - the file remains in place because it still preserves redirects, old IDs, or stable lineage value
- `move to support-only location`:
  - the file may be relocated only when the new location preserves discoverability and all in-repo references can be updated safely
- `delete reproducible file`:
  - the file may be removed only when it is reproducible and no longer needed as checked-in evidence
- `defer cleanup`:
  - stop without deleting or moving because current reader value, references, or replacement safety are not yet defended

### Stop Rules

- Stop if a candidate still appears in a current front-door reading path.
- Stop if a candidate is still cited by active contracts, current views, or parent-spine navigation and no safe rewrite plan exists.
- Stop if a candidate preserves an old ID or redirect that would become ambiguous after deletion.
- Stop if one cleanup round tries to mix governance cleanup with unrelated repo hygiene.
- Stop if the round cannot prove how readers will still discover the same history after the proposed move or deletion.

## P3 Baseline (Round manifest and evidence)

### Cleanup Manifest Shape

- Every cleanup round should run from one explicit manifest that records:
  - `round_id`
  - `bounded candidate set`
  - `defaults`
  - `items`
- Each manifest item should record:
  - `candidate_path`
  - `candidate_class`
  - `proposed_cleanup_outcome`
  - `required_reference_updates`
  - `evidence_of_reproducibility_or_reader_replacement`
  - `status`

### Evidence Contract

- Every cleanup round should leave one auditable result that records:
  - which files were reviewed
  - which files were changed
  - which files were explicitly kept
  - which files were deferred and why
- Cleanup evidence must make it possible to explain later why a preserved file still exists or why a removed file was safe to remove.

## Plan (draft)

### P0 (Slice opening and cleanup boundary)

- P0-C1-S1: create `S0F-3G` and wire it into the `S0F` parent spine
- P0-C1-S2: define the staged cleanup boundary so future rounds do not reopen `S0F-3F` for mixed cleanup and adjudication

### P1 (Candidate inventory)

- P1-C1-S1: inventory one first bounded candidate cleanup family
- P1-C1-S2: separate current-state files from legacy redirects, support-only helpers, reproducible outputs, and unclear candidates

### P2 (Cleanup decision model)

- P2-C1-S1: resolve the first candidate family through the allowed cleanup outcomes
- P2-C1-S2: isolate any unresolved cleanup rows into one explicit defer queue

### P3 (Cleanup manifest)

- P3-C1-S1: define one bounded cleanup manifest for the first round
- P3-C1-S2: reject any round that mixes safe cleanup with unclear reader-value loss

### P4 (First cleanup round)

- P4-C1-S1: execute only the file changes justified by the first bounded manifest
- P4-C1-S2: validate that reader paths, redirects, and current-state surfaces still read cleanly after the round

### P5 (Later rounds)

- P5-C1-S1: repeat bounded cleanup rounds while the candidate set remains defended and finite
- P5-C1-S2: stop the slice when the remaining files are all either current, legacy-needed, or explicitly deferred

## Execution Checklist (unchecked)

### P0 (Slice opening and cleanup boundary)

- [x] `P0-C1-S1`: `S0F-3G` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: staged cleanup boundary defined without mixing cleanup execution into slice opening

### P1 (Candidate inventory)

- [ ] `P1-C1-S1`: first bounded candidate cleanup family inventoried
- [ ] `P1-C1-S2`: current-state files separated from legacy, support-only, reproducible, and unclear candidates

### P2 (Cleanup decision model)

- [ ] `P2-C1-S1`: first candidate family resolved to allowed cleanup outcomes
- [ ] `P2-C1-S2`: unresolved cleanup rows isolated into one explicit defer queue

### P3 (Cleanup manifest)

- [ ] `P3-C1-S1`: first bounded cleanup manifest defined
- [ ] `P3-C1-S2`: mixed or unsafe cleanup rejected before file writes begin

### P4 (First cleanup round)

- [ ] `P4-C1-S1`: only justified file changes executed from the bounded manifest
- [ ] `P4-C1-S2`: reader paths, redirects, and current-state cleanliness revalidated after the round

### P5 (Later rounds)

- [ ] `P5-C1-S1`: later bounded cleanup rounds executed only while the candidate set remains defended
- [ ] `P5-C1-S2`: slice closed when the remaining set converges to keep, legacy, or defer standing only

## Evidence (reserved)

- This opening step records only the cleanup contract and staging boundary.
- Later rounds should retain manifest artifacts, changed-file lists, and post-cleanup verification evidence here rather than treating deletion itself as self-explaining.

### P0-C1-S1S2 (cleanup slice opened and bounded | 2026-04-06)

- headSha: `<TBD-after-first-commit>`
- artifacts:
  - `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - cleanup work is separated from admission and residual adjudication
  - later file reduction can proceed in explicit, reviewable rounds
- observed:
  - `S0F-3G` now fixes the cleanup boundary, outcome vocabulary, and first-round staging model without deleting any files yet
