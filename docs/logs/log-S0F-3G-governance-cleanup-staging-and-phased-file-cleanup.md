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
- `P1` is now complete for the first bounded candidate family: the governance helper-view set under `docs/governance/views/` is now separated into keep-current, keep-legacy, and support-only sweep-helper classes without making destructive changes.
- `P2` is now complete for that same bounded helper-view family: one reusable workflow explainer remains `keep current`, two split-lineage aids remain `keep legacy`, and the eight support-only helper views now resolve into one later move lane toward an explicit support-only location with no defer queue.
- `P3` is now complete for that same bounded helper-view family: the first bounded cleanup manifest now fixes `docs/governance/views/support-only/` as the target location and records the exact planned rename paths plus reference-update set for the eight support-only helper views without moving files yet.
- `P4` is now complete for that same bounded helper-view family: the eight support-only helper views now live under `docs/governance/views/support-only/`, the bounded `S0F-3F` and helper-view cross-links are rewritten to the new location, and the first cleanup round now closes with reader paths revalidated.
- The immediate next follow-up is `P5`: decide whether a second bounded cleanup family is now defended strongly enough for another manifest-driven round.

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

## P1 First Bounded Candidate Inventory (`docs/governance/views/` helper-view family)

### Inventory Packet

- bounded candidate family:
  - `docs/governance/views/view-contract-sweep-workflow-v1.md`
  - `docs/governance/views/view-s0f-1-family-sweep-v1.md`
  - `docs/governance/views/view-remed-admission-package-v1.md`
  - `docs/governance/views/view-wf-family-sweep-v1.md`
  - `docs/governance/views/view-wf-admission-package-v1.md`
  - `docs/governance/views/view-attr-family-sweep-v1.md`
  - `docs/governance/views/view-attr-admission-package-v1.md`
  - `docs/governance/views/view-prb-split-package-v1.md`
  - `docs/governance/views/view-prb-follow-up-family-sweep-v1.md`
  - `docs/governance/views/view-issue-automation-follow-up-family-sweep-v1.md`
  - `docs/governance/views/view-iss-split-package-v1.md`
- excluded from this bounded family:
  - `docs/governance/views/_template-governance-view.md`
    - rationale:
      - it is an active authoring template rather than a cleanup candidate from lineage or residual sweep work
- exact question answered by this inventory:
  - which governance helper views under `docs/governance/views/` still act as reusable or legacy reader aids,
  - which now read only as support-only sweep helpers,
  - and which subset is safe to consider for one first bounded cleanup round without touching active contracts or `INDEX.md`
- stop condition for this inventory:
  - stop before any move or delete decision if a view still appears necessary for current workflow reuse, split-lineage interpretation, or deterministic redirect reading

### Candidate Inventory

| candidate path | candidate class | current reader value | current semantic owner, if any | proposed cleanup outcome | reason for outcome | preconditions before write | cleanup-round scope |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `docs/governance/views/view-contract-sweep-workflow-v1.md` | `current-state file` | reusable reader aid for the active `S0F-3F` sweep method | `S0F-3F` | `keep current` | this is the reusable workflow explainer rather than one one-off helper view, so later cleanup should not treat it as residual residue | none beyond ordinary reference validation | `views-round-1-inventory` |
| `docs/governance/views/view-iss-split-package-v1.md` | `legacy redirect file` | stable lineage aid for the executed `ISS -> ICR/ICL/ICT/IID` split | `S0F-3E` | `keep legacy` | it still explains one major namespace split and preserves reader-facing lineage value beyond one single sweep round | none beyond reference validation | `views-round-1-inventory` |
| `docs/governance/views/view-prb-split-package-v1.md` | `legacy redirect file` | stable lineage aid for the executed `PRB -> PRR/PRG` split | `S0F-3E` | `keep legacy` | it still explains one front-door split and is directly used by later residual `PRB` reading | none beyond reference validation | `views-round-1-inventory` |
| `docs/governance/views/view-s0f-1-family-sweep-v1.md` | `support-only sweep helper` | first-pilot family sweep explanation for already-closed `S0F-1` execution | `S0F-3F` | `move to support-only location` | it is no longer a reusable workflow contract and mainly records one closed pilot-family result, so it looks like a support-only helper candidate rather than a current reader surface | prove a stable support-only destination and update `S0F-3F` references safely | `views-round-1-inventory` |
| `docs/governance/views/view-remed-admission-package-v1.md` | `support-only sweep helper` | one-package explanation for the already-admitted `REMED` lane | `S0F-3F` | `move to support-only location` | the current front door and active contract already explain live `REMED`; this view mainly preserves one bounded admission explanation | prove replacement discoverability and update references from `S0F-3F` or related helper views | `views-round-1-inventory` |
| `docs/governance/views/view-wf-family-sweep-v1.md` | `support-only sweep helper` | one-family worksheet explanation for the already-closed `WF` lane | `S0F-3F` | `move to support-only location` | it records one closed bounded-family result rather than an active reusable workflow rule | prove support-only destination and update internal helper-view references safely | `views-round-1-inventory` |
| `docs/governance/views/view-wf-admission-package-v1.md` | `support-only sweep helper` | one-package explanation for the already-admitted `WF` lane | `S0F-3F` | `move to support-only location` | the active `WF` meaning now reads through `GC-WF-0001` and `INDEX.md`; this view mainly preserves one admission explanation surface | prove replacement discoverability and update references from `S0F-3F` and `view-wf-family-sweep-v1.md` safely | `views-round-1-inventory` |
| `docs/governance/views/view-attr-family-sweep-v1.md` | `support-only sweep helper` | one-family worksheet explanation for the already-closed `ATTR` lane | `S0F-3F` | `move to support-only location` | it records one closed bounded-family result rather than a reusable workflow rule or required lineage redirect | prove support-only destination and update internal helper-view references safely | `views-round-1-inventory` |
| `docs/governance/views/view-attr-admission-package-v1.md` | `support-only sweep helper` | one-package explanation for the already-admitted `ATTR` lane | `S0F-3F` | `move to support-only location` | the active `ATTR` meaning now reads through `GC-ATTR-0001` and `INDEX.md`; this view mainly preserves one admission explanation surface | prove replacement discoverability and update references from `S0F-3F` and `view-attr-family-sweep-v1.md` safely | `views-round-1-inventory` |
| `docs/governance/views/view-prb-follow-up-family-sweep-v1.md` | `support-only sweep helper` | no-op residual closure note for already-resolved `PRB` residue | `S0F-3F` | `move to support-only location` | it preserves one residual closure explanation, but it no longer participates in current front-door reading | prove support-only destination and update references from `S0F-3F` safely | `views-round-1-inventory` |
| `docs/governance/views/view-issue-automation-follow-up-family-sweep-v1.md` | `support-only sweep helper` | no-op residual closure note for already-resolved `S0E-2` precursor residue | `S0F-3F` | `move to support-only location` | it preserves one residual closure explanation, but it no longer participates in current front-door reading | prove support-only destination and update references from `S0F-3F` safely | `views-round-1-inventory` |

### P1 Inventory Result

- The first bounded cleanup inventory now separates the helper-view family into three defended classes:
  - `keep current`:
    - `view-contract-sweep-workflow-v1.md`
  - `keep legacy`:
    - `view-iss-split-package-v1.md`
    - `view-prb-split-package-v1.md`
  - `support-only sweep helper candidate`:
    - `view-s0f-1-family-sweep-v1.md`
    - `view-remed-admission-package-v1.md`
    - `view-wf-family-sweep-v1.md`
    - `view-wf-admission-package-v1.md`
    - `view-attr-family-sweep-v1.md`
    - `view-attr-admission-package-v1.md`
    - `view-prb-follow-up-family-sweep-v1.md`
    - `view-issue-automation-follow-up-family-sweep-v1.md`
- No file is deleted, moved, or rewritten during `P1`.
- The first bounded candidate family therefore exits inventory with one clear `P2` question:
  - whether the support-only helper subset should remain in place for now or move together into one explicit support-only location in a later bounded round

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

## P2 First Bounded Family Adjudication (`docs/governance/views/` helper-view family)

### Accepted Outcomes

- `keep current`:
  - `docs/governance/views/view-contract-sweep-workflow-v1.md`
- `keep legacy`:
  - `docs/governance/views/view-iss-split-package-v1.md`
  - `docs/governance/views/view-prb-split-package-v1.md`
- `move to support-only location`:
  - `docs/governance/views/view-s0f-1-family-sweep-v1.md`
  - `docs/governance/views/view-remed-admission-package-v1.md`
  - `docs/governance/views/view-wf-family-sweep-v1.md`
  - `docs/governance/views/view-wf-admission-package-v1.md`
  - `docs/governance/views/view-attr-family-sweep-v1.md`
  - `docs/governance/views/view-attr-admission-package-v1.md`
  - `docs/governance/views/view-prb-follow-up-family-sweep-v1.md`
  - `docs/governance/views/view-issue-automation-follow-up-family-sweep-v1.md`

### Decision Notes

- The helper subset is now defended strongly enough for one later move lane because:
  - none of the eight support-only helper views is a current front-door file
  - none of them acts as the primary split-lineage aid preserved by `S0F-3E`
  - their active references are bounded to `S0F-3F` and a small number of helper-view cross-links that can be rewritten together in one later round
- The intended support-only destination should remain inside the governance-views surface rather than moving into an unrelated docs area, so later readers can still find bounded sweep and admission history by convention.
- The current defended destination class is therefore:
  - one explicit support-only location under `docs/governance/views/`
- The exact target path and rename set remain `P3` work, not `P2` work.

### Defer Queue

- No row remains in `defer cleanup` for the first bounded helper-view family.
- This does not mean the move should happen immediately.
- It means the family now exits `P2` with one explicit later move lane and without any unresolved keep-versus-move ambiguity.

### P2 Result

- The first bounded helper-view family now exits decision with one clean split:
  - one reusable workflow explainer remains where it is
  - two split-lineage aids remain where they are
  - eight support-only helper views move together in one later bounded manifest
- `P3` should therefore define one move manifest rather than reopening candidate classification.

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

## P3 First Bounded Cleanup Manifest (`S0F-3G-views-round-1`)

### Manifest Decision

- The first bounded cleanup manifest is now fixed as:
  - `docs/governance/views/support-only/cleanup-manifest-S0F-3G-views-round-1.json`
- Chosen support-only target location:
  - `docs/governance/views/support-only/`
- Rationale:
  - the target stays inside the governance-view surface so later readers can still find sweep and admission helper history by one stable convention
  - the target remains distinct from current reusable workflow and split-lineage views that stay at the root of `docs/governance/views/`
  - the whole helper subset can move together without mixing in current or legacy redirect files

### Manifest Scope

- planned move set:
  - `view-s0f-1-family-sweep-v1.md`
  - `view-remed-admission-package-v1.md`
  - `view-wf-family-sweep-v1.md`
  - `view-wf-admission-package-v1.md`
  - `view-attr-family-sweep-v1.md`
  - `view-attr-admission-package-v1.md`
  - `view-prb-follow-up-family-sweep-v1.md`
  - `view-issue-automation-follow-up-family-sweep-v1.md`
- reference-update set recorded in the manifest:
  - `docs/logs/log-S0F-3F-governance-contract-sweep-workflow.md`
  - helper-view cross-links inside:
    - `view-s0f-1-family-sweep-v1.md`
    - `view-wf-family-sweep-v1.md`
    - `view-attr-family-sweep-v1.md`
- explicit non-move set:
  - `view-contract-sweep-workflow-v1.md`
  - `view-iss-split-package-v1.md`
  - `view-prb-split-package-v1.md`
  - `_template-governance-view.md`

### P3 Result

- The first bounded helper-view family now exits `P3` with one executable later move manifest rather than only one abstract move intention.
- No file is moved during `P3`.
- `P4` can therefore execute one bounded rename-and-reference-update round without reopening target-location design.

## P4 First Bounded Cleanup Round (`S0F-3G-views-round-1`)

### Executed Changes

- executed move set:
  - `docs/governance/views/view-s0f-1-family-sweep-v1.md` -> `docs/governance/views/support-only/view-s0f-1-family-sweep-v1.md`
  - `docs/governance/views/view-remed-admission-package-v1.md` -> `docs/governance/views/support-only/view-remed-admission-package-v1.md`
  - `docs/governance/views/view-wf-family-sweep-v1.md` -> `docs/governance/views/support-only/view-wf-family-sweep-v1.md`
  - `docs/governance/views/view-wf-admission-package-v1.md` -> `docs/governance/views/support-only/view-wf-admission-package-v1.md`
  - `docs/governance/views/view-attr-family-sweep-v1.md` -> `docs/governance/views/support-only/view-attr-family-sweep-v1.md`
  - `docs/governance/views/view-attr-admission-package-v1.md` -> `docs/governance/views/support-only/view-attr-admission-package-v1.md`
  - `docs/governance/views/view-prb-follow-up-family-sweep-v1.md` -> `docs/governance/views/support-only/view-prb-follow-up-family-sweep-v1.md`
  - `docs/governance/views/view-issue-automation-follow-up-family-sweep-v1.md` -> `docs/governance/views/support-only/view-issue-automation-follow-up-family-sweep-v1.md`
- executed reference rewrites:
  - `docs/logs/log-S0F-3F-governance-contract-sweep-workflow.md`
  - helper-view cross-links inside:
    - `docs/governance/views/support-only/view-s0f-1-family-sweep-v1.md`
    - `docs/governance/views/support-only/view-wf-family-sweep-v1.md`
    - `docs/governance/views/support-only/view-attr-family-sweep-v1.md`
  - `docs/governance/views/support-only/cleanup-manifest-S0F-3G-views-round-1.json` status fields

### Validation Result

- post-move reader-path validation confirms that the bounded `S0F-3F` reference set now points at `docs/governance/views/support-only/` for all eight helper views.
- helper-view internal cross-links now resolve within the same `support-only/` location for the `S0F-1`, `WF`, and `ATTR` pairs.
- the explicit non-move set remains unchanged:
  - `view-contract-sweep-workflow-v1.md`
  - `view-iss-split-package-v1.md`
  - `view-prb-split-package-v1.md`
  - `_template-governance-view.md`

### P4 Result

- The first bounded helper-view cleanup round is now executed without widening scope beyond the manifest.
- The root of `docs/governance/views/` now keeps only the reusable workflow view, the two lineage aids, the template, and the `support-only/` folder for closed-lane helper history.
- `P5` can now focus on whether another bounded cleanup family exists, rather than revisiting the already-executed first move lane.

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

- [x] `P1-C1-S1`: first bounded candidate cleanup family inventoried
- [x] `P1-C1-S2`: current-state files separated from legacy, support-only, reproducible, and unclear candidates

### P2 (Cleanup decision model)

- [x] `P2-C1-S1`: first candidate family resolved to allowed cleanup outcomes
- [x] `P2-C1-S2`: unresolved cleanup rows isolated into one explicit defer queue

### P3 (Cleanup manifest)

- [x] `P3-C1-S1`: first bounded cleanup manifest defined
- [x] `P3-C1-S2`: mixed or unsafe cleanup rejected before file writes begin

### P4 (First cleanup round)

- [x] `P4-C1-S1`: only justified file changes executed from the bounded manifest
- [x] `P4-C1-S2`: reader paths, redirects, and current-state cleanliness revalidated after the round

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

### P1-C1-S1S2 (first helper-view cleanup family inventoried | 2026-04-06)

- headSha: `<TBD-after-inventory-commit>`
- artifacts:
  - `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  - `docs/governance/views/view-contract-sweep-workflow-v1.md`
  - `docs/governance/views/view-iss-split-package-v1.md`
  - `docs/governance/views/view-prb-split-package-v1.md`
  - `docs/governance/views/view-s0f-1-family-sweep-v1.md`
  - `docs/governance/views/view-remed-admission-package-v1.md`
  - `docs/governance/views/view-wf-family-sweep-v1.md`
  - `docs/governance/views/view-wf-admission-package-v1.md`
  - `docs/governance/views/view-attr-family-sweep-v1.md`
  - `docs/governance/views/view-attr-admission-package-v1.md`
  - `docs/governance/views/view-prb-follow-up-family-sweep-v1.md`
  - `docs/governance/views/view-issue-automation-follow-up-family-sweep-v1.md`
- expected:
  - one first bounded cleanup family is separated into keep-current, keep-legacy, and support-only helper candidates before any file moves begin
  - the next cleanup round can focus on the support-only helper subset without relitigating current workflow and split-lineage aids
- observed:
  - the first bounded helper-view family is now explicitly inventoried, with one reusable workflow view kept current, two split-lineage aids kept legacy, and eight closed-lane helper views carried forward as support-only cleanup candidates only

### P2-C1-S1S2 (first helper-view cleanup family adjudicated | 2026-04-06)

- headSha: `<TBD-after-adjudication-commit>`
- artifacts:
  - `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  - `docs/governance/views/view-contract-sweep-workflow-v1.md`
  - `docs/governance/views/view-iss-split-package-v1.md`
  - `docs/governance/views/view-prb-split-package-v1.md`
  - `docs/governance/views/view-s0f-1-family-sweep-v1.md`
  - `docs/governance/views/view-remed-admission-package-v1.md`
  - `docs/governance/views/view-wf-family-sweep-v1.md`
  - `docs/governance/views/view-wf-admission-package-v1.md`
  - `docs/governance/views/view-attr-family-sweep-v1.md`
  - `docs/governance/views/view-attr-admission-package-v1.md`
  - `docs/governance/views/view-prb-follow-up-family-sweep-v1.md`
  - `docs/governance/views/view-issue-automation-follow-up-family-sweep-v1.md`
- expected:
  - the first helper-view family resolves cleanly to keep-current, keep-legacy, and later-move outcomes without reopening current-state or split-lineage ambiguity
  - the next phase can define one bounded move manifest instead of relitigating which views are still eligible for cleanup
- observed:
  - the first helper-view family now exits adjudication with one `keep current` workflow explainer, two `keep legacy` split-lineage aids, eight views assigned to one later support-only move lane, and no defer queue

### P3-C1-S1S2 (first helper-view cleanup manifest fixed | 2026-04-06)

- headSha: `<TBD-after-manifest-commit>`
- artifacts:
  - `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  - `docs/governance/views/support-only/cleanup-manifest-S0F-3G-views-round-1.json`
- expected:
  - the first support-only helper subset has one explicit target location and one exact planned reference-update set before any rename round begins
  - `P4` can execute one bounded move round without reopening destination design
- observed:
  - the first helper-view move lane now has one concrete manifest under `docs/governance/views/support-only/`, with eight planned target paths, one bounded reference-update set, and an explicit non-move set for current, legacy, and template files

### P4-C1-S1S2 (first helper-view cleanup round executed | 2026-04-06)

- headSha: `<TBD-after-cleanup-round-commit>`
- artifacts:
  - `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  - `docs/logs/log-S0F-3F-governance-contract-sweep-workflow.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
  - `docs/governance/views/support-only/cleanup-manifest-S0F-3G-views-round-1.json`
  - `docs/governance/views/support-only/view-s0f-1-family-sweep-v1.md`
  - `docs/governance/views/support-only/view-remed-admission-package-v1.md`
  - `docs/governance/views/support-only/view-wf-family-sweep-v1.md`
  - `docs/governance/views/support-only/view-wf-admission-package-v1.md`
  - `docs/governance/views/support-only/view-attr-family-sweep-v1.md`
  - `docs/governance/views/support-only/view-attr-admission-package-v1.md`
  - `docs/governance/views/support-only/view-prb-follow-up-family-sweep-v1.md`
  - `docs/governance/views/support-only/view-issue-automation-follow-up-family-sweep-v1.md`
- expected:
  - the first helper-view support-only subset is moved as one bounded round without breaking `S0F-3F` navigation or helper-view cross-links
  - root-level governance views stay focused on reusable workflow and stable lineage reading
- observed:
  - all eight manifest-listed helper views now live under `docs/governance/views/support-only/`
  - `S0F-3F` reference logs and the three helper-view cross-links now point to the new location
  - no additional current, legacy, or template file is moved during this round
