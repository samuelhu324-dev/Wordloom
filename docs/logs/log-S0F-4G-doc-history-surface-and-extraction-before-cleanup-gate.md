# log-S0F-4G (Phase 4G: DOC history surface and extraction-before-cleanup gate)

---

**id**: `S0F-4G`
**kind**: `log`
**title**: `DOC history surface and extraction-before-cleanup gate v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Contract, History, Lineage, epic/s0, sub/4g`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-3J-old-gc-cleanup-candidate-selection-after-doc-reader-stabilization.md`
  **reference_log_1**: `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
  **reference_log_2**: `docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md`
  **reference_log_3**: `docs/logs/log-S0F-4F-doc-reader-surface-consolidation-after-first-promotion-quartet.md`
  **reference_log_4**: `docs/logs/log-S0F-5A-stable-first-close-out-protocol-and-post-stable-outlet-export.md`
  **reference_log_5**: `docs/logs/log-S0C-1A-log-extensions.md`
  **reference_log_6**: `docs/logs/log-S0D-1A-log-entries-orchestration.md`
  **reference_log_7**: `docs/logs/log-S0D-6A-structured-roadmap-and-demo.md`
  **reference_log_8**: `docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
  **reference_log_9**: `docs/logs/log-S0E-6A-log-structure-normalization-and-dual-track-evidence-contract.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/4`
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
**created**: `2026-04-08`
**updated**: `2026-04-08`

---

## Decision / Outcome

**Decision**:

- `S0F-4G` opens the next bounded follow-up because `S0F-4F` already stabilized the first current `DOC` reader surface and `S0F-3J` already proved that old-`GC-*` cleanup is locally safe only in a narrow standing sense, but the repo still lacks one durable answer for how current contracts should expose historical evolution without forcing readers back into long source-owner logs.
- v1 fixes one missing history layer above the current `DOC` contract surface:
  - one compact contract-history block that current family-owned contracts may carry without collapsing back into full chronology
  - one family-owned lineage or evolution view that lets a reader click through the major historical chain instead of replaying scattered logs manually
  - one extraction-before-cleanup gate so old logs do not downgrade into support-only or deferred-cleanup standing before their core historical ideas are surfaced elsewhere
- This slice therefore does not reopen `DOC` promotion semantics, does not reopen the already-adjudicated `S0F-3J` no-op result, and does not attempt one-off historical summarization inside the parent spine. It fixes the reusable mechanism that later history extraction and cleanup lanes should follow.

**Default choices (phase defaults / v1)**:

- Keep current `DOC` contracts current-state-first; add compact history blocks rather than turning contract bodies into long narrative ledgers.
- Treat family-owned lineage views as the main reader-facing `medical history` surface; do not make the parent spine or one temporary review note the only history entrypoint.
- Require `history extracted enough for future readers` before an old source-owner log becomes a default cleanup or support-only candidate.
- Preserve the source-owner log as the strongest historical SoT until the compact history block and lineage view for that material are explicit enough to read directly.
- Do not reopen old `GC-*` file relocation merely because the current `DOC` quartet is stable; cleanup must now satisfy both standing rules and history-extraction rules.
- Prefer one bounded pilot family first, likely `DOC`, before generalizing the mechanism across other families such as `OPS`.

## Problem Statement

- The repo now has a much stronger current-state surface than it had before:
  - `S0F-4D` fixed the current `DOC` contract home
  - `S0F-4E` promoted the first `DOC` quartet
  - `S0F-4F` consolidated the reader surfaces
  - `S0F-3J` rechecked old `GC-*` cleanup and correctly stopped with an explicit no-op
- But the current system is still globally weak in one place:
  - current contracts explain `what is true now`
  - old logs still explain `how this structure evolved and why the current surface looks this way`
  - cleanup review currently answers standing, redirect, and placement questions much better than it answers `has the important historical chain already been extracted into a durable reader surface?`
- Without one explicit mechanism, later readers still need human memory and long log archaeology to understand:
  - why structured logs gained decision blocks and stable status fields
  - how `P/C/S`, roadmap bridging, evidence packaging, and frontmatter normalization evolved
  - why source-owner logs, `DOC` contracts, views, runbooks, and support-only placement now have their current boundaries

## PR Summary Inputs (optional)

- Use this block because `S0F-4G` fixes the missing history surface between stable current contracts and later cleanup.
- `PR Summary Inputs` remains automation-facing; later family views or contract-history blocks should not reconstruct this boundary from scattered prose.

**PR summary bullets**:

- Add a durable history layer above the current `DOC` contract surface instead of relying on one-off log archaeology.
- Define compact contract-history blocks, family-owned lineage views, and an extraction-before-cleanup gate.
- Make later old-log cleanup depend on historical extraction, not only on standing-loss and redirect-loss.

**PR checklist source**:

- Default source: reuse this log's execution checklist for any later history-surface and cleanup-gate PR.

**PR links**:

- Log: `docs/logs/log-S0F-4G-doc-history-surface-and-extraction-before-cleanup-gate.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`
- Previous log: `docs/logs/log-S0F-3J-old-gc-cleanup-candidate-selection-after-doc-reader-stabilization.md`

## Exported Sections / Outlet Ownership (optional)

- This slice is expected to end in a history mechanism, not in another current-rule promotion lane.

**Outlet ownership**:

- `contract`: compact contract-history block contract for family-owned current surfaces
- `view`: family-owned lineage or evolution view that concentrates the major historical chain
- `index/front-door`: any family front-door or index note that needs to point readers to the new lineage surface
- `disposition/placement`: extraction-before-cleanup rule for old logs and support-only eligibility
- `log-retained core`: bounded historical-source inventory, pilot selection, extraction ledger, and close-out evidence for this lane

## Definitions (optional)

- **compact contract-history block**: a short, stable section inside a current contract that records the minimum evolution chain needed to explain the current surface without reproducing the full source-owner chronology
- **family-owned lineage view**: a bounded reader-facing view that explains the major evolution path, predecessor surfaces, and current reading order for one family
- **extraction-before-cleanup gate**: the rule that old logs cannot be downgraded by default until their core ideas are represented in durable current or reader-facing history surfaces
- **historical SoT**: the retained source-owner log set that still owns the detailed chronology and evidence until extraction is complete enough

## Constraints

- Do not reopen `DOC-DRB-0001`, `DOC-SLC-0001`, `DOC-TAX-0001`, or `DOC-FDT-0001` current-rule semantics unless the history-layer design proves that one of them lacks the minimum current-state boundary.
- Do not treat one temporary summary or one parent-spine paragraph as a substitute for a durable family history surface.
- Do not let compact history blocks grow into full duplicate logs.
- Do not reopen already-adjudicated `S0F-3J` file moves merely because some history is still trapped in logs; first define the extraction rule, then later apply it.
- Do not require every family to adopt the mechanism at once; one defended pilot should come first.

## Scope

- `P0`: open `S0F-4G`, wire it into the `S0F` spine, and fix the missing problem as `history surface + cleanup gate` work
- `P1`: define the compact contract-history block contract for current family-owned surfaces
- `P2`: define one family-owned lineage or evolution view contract for reader-facing historical navigation
- `P3`: define the extraction-before-cleanup gate and how it modifies later old-log cleanup admission
- `P4`: inventory the first pilot source set across `S0B`, `S0C`, `S0D`, `S0E`, and `S0F` that should feed the initial `DOC` history surface
- `P5`: decide the first bounded publication package for that pilot history surface and its write-backs

## Success Criteria (DoD)

- One reader can explain the difference among `current contract body`, `compact contract history`, `family lineage view`, and `retained source-owner log`.
- One reader can navigate from a current `DOC` contract to the major historical chain without replaying whole source directories manually.
- Later cleanup can explicitly say whether a candidate old log fails because history has not been extracted yet, instead of answering only standing and redirect questions.
- The repo has one defended pilot mechanism that future families can reuse instead of relying on human memory.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the compact history block contract, lineage-view contract, and extraction-before-cleanup gate are all explicit enough to reuse
  - one first pilot source set is bounded clearly enough that later extraction work no longer depends on ad hoc archaeology
  - the next execution lane after `S0F-4G` is obvious enough that later cleanup or family work does not need to reopen the same design debate

## P0 (Contract | v1)

### P0-C1-S1 (Problem boundary fixed | v1)

- `S0F-4G` is now opened to fix the missing history layer between stable current `DOC` reading and later old-log cleanup.
- This slice does not create the first history package yet.
- It first fixes what kind of durable surfaces must exist before history extraction and cleanup can proceed coherently.

### P0-C1-S2 (Immediate sequencing fixed | v1)

- The immediate next step after scaffold is now:
  - first define the compact history block and lineage-view contract
  - then define the extraction-before-cleanup gate
  - only after that select the first bounded pilot source set for real extraction
- This keeps the reusable mechanism ahead of any specific history rewrite or cleanup re-entry.

## Current Status (recommended)

- `S0F-4G` is now opened as the next bounded follow-up after `S0F-3J` and the stabilized `DOC` reader surface.
- `P0` is now complete: the missing problem is fixed as `history surface + extraction-before-cleanup gate`, not as another old-`GC-*` scan and not as one temporary history note inside the parent spine.
- `P1` is now complete: the repo now has one explicit minimum field set, one fixed section shape, and one retained-chronology boundary for compact contract-history blocks, so later history extraction no longer needs to improvise what may enter a current contract body.
- `P2` is now complete: the repo now has one explicit `DOC` lineage-view shape and one fixed navigation split among current contract, family front door, promotion map, lineage view, and retained source-owner logs, so later history publication no longer needs to improvise where historical reading should begin.
- The next immediate work is `P3`: define the extraction-before-cleanup gate and how later old-log cleanup must fail or stop when history surfaces are still missing.

## P1 (Compact history block contract | v1)

### P1-C1-S1 (Minimum compact-history field and section set fixed | v1)

- A compact contract-history block is now fixed as one optional but controlled section inside a current family-owned contract.
- The block should use one stable heading:
  - `## Compact History`
- The minimum required rows inside that block are now:
  - `Current source-owner origin`:
    - the retained primary source-owner log or contract from which the current rule set was concentrated
  - `Why this current contract exists`:
    - one short statement of the structural pressure or transition that made the current contract necessary
  - `Major evolution chain`:
    - a short ordered list of the bounded predecessor surfaces that a future reader must know to understand the current shape
  - `Read history in full`:
    - one lineage-view or retained-source entry that carries the broader historical reading path
  - `Cleanup dependency`:
    - whether old source-owner or legacy surfaces still remain protected because history extraction is not yet complete elsewhere
- The minimum semantic rules for those rows are now fixed:
  - keep each row short and reader-oriented
  - prefer stable links over prose-heavy retelling
  - point to bounded predecessor surfaces rather than to every intermediate edit
  - make the block sufficient to answer `where did this come from?` without forcing the current contract to retell the full lane chronology

### P1-C1-S2 (Retained source-owner-only chronology boundary fixed | v1)

- The following historical content must stay outside the compact contract-history block and remain source-owner-log or lineage-view material:
  - full phase-by-phase `P/C/S` execution ledger
  - detailed evidence and artifact bookkeeping
  - abandoned alternatives, temporary blockers, and iterative wording churn
  - broad cross-era archaeology that spans more than the current contract's direct chain
  - package-local cleanup debate, stop-state rationale, or open inventory rows that are not needed to read the current contract
- The compact history block must therefore not become:
  - a second source-owner log
  - a family-wide chronology dump
  - a substitute for evidence or close-out ledger
- The retained source-owner log keeps ownership of:
  - detailed chronology
  - proof and evidence
  - slice-local decision sequence
  - exact bridge notes used during promotion, consolidation, or cleanup adjudication
- The lineage view will later sit between those two layers:
  - compact history block gives the minimum historical orientation inside the current contract
  - lineage view gives the bounded reader-facing evolution chain
  - retained source-owner logs keep the detailed chronology and proof

## P2 (Family lineage view contract | v1)

### P2-C1-S1 (First `DOC` lineage-view shape fixed | v1)

- The first family-owned lineage surface is now fixed as one bounded `view`, not as one new `contract`, not as one expansion of the current `DOC` front door, and not as one source-owner-log rewrite.
- The recommended filename model is now:
  - `view-<family>-history-and-lineage-v<version>.md`
- The first expected concrete target for this lane is therefore:
  - `view-doc-history-and-lineage-v1.md`
- The lineage view owns one distinct reader job:
  - explain the major evolution chain that produced the current `DOC` surface
  - show which current contracts came out of which source-owner logs
  - point readers from current-state surfaces into historical reading without forcing a full archaeology pass
- The minimum section shape for that lineage view is now fixed as:
  - `Purpose`:
    - why this history surface exists and what it is not
  - `Current Reading First`:
    - a short reminder that current rule meaning still starts at the active `DOC` contract and current front door
  - `Major Evolution Chain`:
    - one ordered chain of the few predecessor surfaces a reader actually needs
  - `Current Contract To Source-Owner Map`:
    - current active `DOC` contracts paired with retained source-owner logs
  - `Historical Milestones`:
    - bounded milestone rows such as `structure`, `bridge`, `automation`, `promotion`, `cleanup boundary`, each linked to the strongest source surface
  - `Read Next`:
    - a compact navigation block for readers who want either current meaning, family history, or full chronology
- The lineage view should prefer:
  - milestone compression over exhaustive chronology
  - source links over retelling
  - family-level reading over slice-local execution detail

### P2-C1-S2 (Current-contract to lineage-view navigation split fixed | v1)

- The repo now fixes one explicit navigation split among the five nearby reader surfaces:
  - `current contract body`:
    - owns current effective rule meaning plus the compact history block
  - `DOC front door`:
    - owns family-first current reading and tells readers where to start for present meaning
  - `promotion map`:
    - owns deterministic source-owner-to-contract mapping and future extension semantics
  - `lineage view`:
    - owns bounded historical interpretation and major evolution-chain reading
  - `retained source-owner logs`:
    - own detailed chronology, evidence, and slice-local decision sequence
- The navigation rule is now:
  - if the reader asks `what is true now?`, start at the `DOC` front door and then open the active current contract
  - if the reader asks `how did this current shape emerge?`, start at the lineage view
  - if the reader asks `which source-owner produced which contract?`, use the promotion map
  - if the reader asks `what exactly happened in detail?`, open the retained source-owner logs
- The compact history block inside a current contract should therefore point outward like this:
  - `Read history in full` should prefer the lineage view first
  - the lineage view should then point to the retained source-owner logs for deep chronology
- The lineage view must not duplicate the existing front door or promotion map:
  - do not restate the whole active contract inventory as if it were a second front door
  - do not restate only source-owner-to-contract mapping as if it were just a history-flavored promotion map
  - do not replay detailed `P/C/S` closure as if it were a source-owner log
- Under this split, later history publication can add one real historical reader surface without blurring the already-stabilized `DOC` current-reading surfaces.

## Plan (draft)

### P1 (Compact history block contract)

- P1-C1-S1: define the minimum field and section set for a compact contract-history block
- P1-C1-S2: define what kinds of chronology must stay out of the current contract body and remain source-owner-only

### P2 (Family lineage view contract)

- P2-C1-S1: define the first family-owned lineage-view shape for `DOC`
- P2-C1-S2: define reader navigation from current contract -> lineage view -> retained source-owner logs

### P3 (Extraction-before-cleanup gate)

- P3-C1-S1: define how later cleanup admission adds `history extracted enough` to the standing and redirect model
- P3-C1-S2: define explicit no-op and stop reasons when history extraction is still missing

### P4 (Pilot source inventory)

- P4-C1-S1: inventory the first bounded `S0B/S0C/S0D/S0E/S0F` source set for `DOC` history extraction
- P4-C1-S2: reduce that source set to one defended major-chain reading path rather than a full-archive dump

### P5 (First publication package)

- P5-C1-S1: decide the first write-back package across contract-history block, lineage view, and any front-door notes

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: problem boundary fixed
- [x] `P0-C1-S2`: immediate sequencing fixed

### P1 (Compact history block contract)

- [x] `P1-C1-S1`: minimum compact-history field set fixed
- [x] `P1-C1-S2`: retained source-owner-only chronology boundary fixed

### P2 (Family lineage view contract)

- [x] `P2-C1-S1`: first `DOC` lineage-view shape fixed
- [x] `P2-C1-S2`: current-contract to lineage-view navigation fixed

### P3 (Extraction-before-cleanup gate)

- [ ] `P3-C1-S1`: history-aware cleanup admission rule fixed
- [ ] `P3-C1-S2`: history-missing stop and no-op reasons fixed

### P4 (Pilot source inventory)

- [ ] `P4-C1-S1`: first bounded pilot source set inventoried
- [ ] `P4-C1-S2`: first defended major-chain reading path fixed

### P5 (First publication package)

- [ ] `P5-C1-S1`: first history-surface write-back package fixed

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths or later CI references.
- This scaffold commit is the first traceable opening event for the history-surface lane.

### P1-C1-S1S2 (Compact contract-history block contract fixed | 2026-04-08)

- headSha: `<pending commit for S0F-4G/P1-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-4G-doc-history-surface-and-extraction-before-cleanup-gate.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo has one explicit minimum section shape for compact contract history
  - the repo has one explicit rule for what history must stay in retained source-owner logs instead of expanding current contracts
- observed:
  - `S0F-4G/P1` now fixes the minimum compact-history block rows and the retained source-owner-only chronology boundary directly in the lane contract
  - later history extraction can now reuse one bounded definition instead of improvising contract-local history prose

### P2-C1-S1S2 (DOC lineage-view contract and navigation split fixed | 2026-04-08)

- headSha: `<pending commit for S0F-4G/P2-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-4G-doc-history-surface-and-extraction-before-cleanup-gate.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo has one explicit history-view shape for `DOC`
  - the repo has one explicit navigation split among front door, current contract, promotion map, lineage view, and retained source-owner logs
- observed:
  - `S0F-4G/P2` now fixes the first `DOC` lineage-view section model and the outward navigation rule from current contracts into family history
  - later history publication can now create one bounded reader-facing historical surface without reopening the jobs already owned by the `DOC` front door or promotion map

## Recent changes (for traceability, optional)

- 2026-04-08: opened `S0F-4G` as the next bounded follow-up so later history extraction and cleanup work can proceed through a reusable mechanism instead of ad hoc archaeology.
- 2026-04-08: completed `P1` so compact contract-history blocks now have one fixed minimum shape and one explicit source-owner-only chronology boundary.
- 2026-04-08: completed `P2` so the first `DOC` lineage-view shape and its navigation split are now explicit.