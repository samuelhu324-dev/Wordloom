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
- `P3` is now complete: later cleanup now has one explicit history-aware admission rule and one explicit stop/no-op reason set, so old-log relocation can no longer rely on standing-loss and redirect-loss alone when key historical meaning still has no durable extracted surface.
- `P4` is now complete: the first bounded pilot source set and one defended major-chain reading path are now explicit, so later history publication can start from a compressed cross-era source packet instead of from open-ended archaeology.
- The next immediate work is `P5`: decide the first bounded write-back package across compact history blocks, one `DOC` lineage view, and any required front-door notes.

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

## P3 (Extraction-before-cleanup gate | v1)

### P3-C1-S1 (History-aware cleanup admission rule fixed | v1)

- Later old-log cleanup admission must now satisfy three questions instead of two:
  - has the candidate already lost `current standing`?
  - has the candidate already lost `redirect or root-path lineage duty`?
  - has the candidate's core historical meaning already been extracted into durable current or reader-facing history surfaces?
- The third question is now mandatory whenever the candidate still acts as one of the main readable explanations for how the current family surface emerged.
- The new admission rule is therefore:
  - a candidate old log may enter bounded cleanup only when `standing-loss`, `redirect-loss`, and `history extracted enough` are all true
- `history extracted enough` is now defined minimally as:
  - current rule meaning already reads through the active current contract or other current surface
  - compact history orientation is available at the current-contract layer when that current surface is family-owned
  - one lineage or equivalent bounded reader-facing history surface exists, or the retained source-owner log is no longer the only practical historical entrypoint
  - direct reader navigation toward deeper chronology remains explicit after the move
- Under this rule, a file may fail cleanup admission even after losing current standing and redirect duty if the repo would otherwise force future readers to reconstruct the key evolution chain from raw historical logs alone.
- This rule does not replace the existing triage model from `S0F-4D` or the null-candidate stop result from `S0F-3J`.
- It tightens the later admission bar by saying:
  - standing and redirect questions are necessary
  - history extraction is an additional necessary condition when the file still carries core explanatory value

### P3-C1-S2 (History-missing stop and no-op reasons fixed | v1)

- The first allowed history-aware stop and no-op reasons are now fixed as:
  - `history surface missing`:
    - no lineage view or equivalent bounded historical reader surface exists yet for the relevant family chain
  - `compact current-history missing`:
    - the active current contract still lacks the minimum compact history block needed to orient readers away from the old log
  - `source-owner still sole practical history entrypoint`:
    - the candidate old log still acts as the only efficient way to understand the major evolution chain
  - `navigation to deep chronology not yet explicit`:
    - a cleanup move would weaken discoverability because readers would not know where the detailed chronology now lives
  - `pilot extraction not published yet`:
    - the family has chosen extraction as the next step, but the first bounded write-back package is not yet landed
- These reasons are now valid even if:
  - the file is already deprecated
  - the file is no longer current-state-first
  - the directory looks tidy enough to move it
- The review outcome model is therefore tightened to three explicit classes:
  - `admissible for cleanup now`
  - `not admissible because redirect or standing still active`
  - `not admissible because history extraction still incomplete`
- This gives later cleanup lanes one explicit way to stop without pretending the candidate is still current and without pretending the relocation is already safe.
- For `S0F-4G`, the immediate consequence is straightforward:
  - later re-entry to old-log cleanup should not reopen merely from `DOC` current-surface stabilization alone
  - it should reopen after one family history package exists strongly enough that old explanatory logs are no longer the only durable historical reading path

## P4 (Pilot source inventory | v1)

### P4-C1-S1 (First bounded pilot source set inventoried across `S0B/S0C/S0D/S0E/S0F` | v1)

- The first pilot source set is now bounded by one inclusion rule:
  - include only the strongest cross-era surfaces that directly changed how current `DOC` contracts are authored, structured, bridged, normalized, promoted, or read
- The first included primary source set is now:
  - `S0B-3A`:
    - `docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md`
    - reason: fixes stable identifiers, frontmatter, and decoupled metadata as the earliest durable structural base for later doc-first contracts
  - `S0C-1A`:
    - `docs/logs/log-S0C-1A-log-extensions.md`
    - reason: turns logs from freeform notes into structured decision surfaces with stable outcome-first reading
  - `S0D-1A`:
    - `docs/logs/log-S0D-1A-log-entries-orchestration.md`
    - reason: fixes the parent-spine plus child-log model and the `P/C/S` execution ledger that later source-owner `DOC` logs inherit directly
  - `S0E-3A`:
    - `docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
    - reason: adds machine-readable roadmap bridging so log lineage no longer lives only in prose references
  - `S0E-6A`:
    - `docs/logs/log-S0E-6A-log-structure-normalization-and-dual-track-evidence-contract.md`
    - reason: fixes the dual-track split between automation-facing structure and human evidence ledger, which current contract and lineage surfaces now depend on indirectly
  - `S0F-4A`:
    - `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
    - reason: supplies the first major current-rule concentration later promoted into `DOC-DRB-0001`
  - `S0F-4B`:
    - `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
    - reason: fixes source-log compatibility and weak-structure export discipline later promoted into `DOC-SLC-0001`
  - `S0F-3I`:
    - `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
    - reason: fixes the seven-family taxonomy and placement model later promoted into `DOC-TAX-0001`
  - `S0F-4C`:
    - `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
    - reason: fixes family-first front-door transition later promoted into `DOC-FDT-0001`
  - `S0F-4D`:
    - `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
    - reason: fixes the physical current `DOC` contract home and the initial old-`GC-*` triage model
  - `S0F-4E`:
    - `docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md`
    - reason: records the actual promotion event that turns the source-owner quartet into active family-owned `DOC` contracts
  - `S0F-4F`:
    - `docs/logs/log-S0F-4F-doc-reader-surface-consolidation-after-first-promotion-quartet.md`
    - reason: fixes the stable post-promotion reader surface from which current `DOC` reading now starts
- The following surfaces are now explicitly classified as secondary context, not first-pilot primary sources:
  - `S0B-2A`:
    - useful for scripts and snapshots governance, but not one direct prerequisite for reading current `DOC` contract lineage
  - `S0C-3A` and `S0C-4A`:
    - important for CLI and scenario operations, but not part of the first `DOC` structural-history chain
  - `S0D-6A`:
    - relevant as roadmap container evolution, but secondary to the more direct bridge contract in `S0E-3A`
  - `S0E-docs-management-v5`:
    - valuable as the `S0E` parent spine, but not the first cross-era milestone source because the pilot needs stronger phase-local structural anchors than one umbrella summary
  - `S0F-3J`:
    - remains an important downstream consumer of the history-extraction gate, but not one of the formative sources for the first `DOC` history surface itself

### P4-C1-S2 (First defended major-chain reading path fixed | v1)

- The first defended major-chain reading path is now fixed as one compressed sequence with one strongest source per structural turn:
  1. `S0B-3A`
     - stable identifiers, frontmatter, and metadata decoupling become the base document-management grammar
  2. `S0C-1A`
     - logs become structured decision surfaces instead of loose chronology
  3. `S0D-1A`
     - parent spine plus child-log orchestration and `P/C/S` ledger turn that structure into a reusable execution system
  4. `S0E-3A`
     - roadmap bridge makes milestone and log lineage machine-readable instead of prose-only
  5. `S0E-6A`
     - dual-track evidence normalization separates automation-facing structure from human evidence ledger
  6. `S0F-4A` plus `S0F-4B` plus `S0F-3I` plus `S0F-4C`
     - the core `DOC` source-owner quartet fixes role boundaries, source-log compatibility, taxonomy, and family-front-door transition
  7. `S0F-4D`
     - current `DOC` contract home and old-`GC-*` triage are fixed explicitly
  8. `S0F-4E`
     - the quartet is promoted into family-owned current contracts
  9. `S0F-4F`
     - the reader surface is consolidated into the stable current `DOC` front door
- The defended reading rule for this path is now:
  - use these sources as the first pilot `DOC` history skeleton
  - treat everything else as supporting deep-chronology material unless later publication proves one omitted surface is necessary for a reader to understand a major turn
- This means the first lineage view should not try to narrate every `S0` phase.
- It should narrate one bounded arc:
  - document identity and structure became explicit
  - logs became orchestrated and bridgeable
  - automation-facing structure was normalized
  - governance rules were concentrated into the source-owner quartet
  - that quartet was promoted and stabilized into the current `DOC` surface
- The immediate consequence for `P5` is now clear:
  - the first publication package should use this compressed source set and this major-chain path rather than reopening source selection from scratch

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

- [x] `P3-C1-S1`: history-aware cleanup admission rule fixed
- [x] `P3-C1-S2`: history-missing stop and no-op reasons fixed

### P4 (Pilot source inventory)

- [x] `P4-C1-S1`: first bounded pilot source set inventoried
- [x] `P4-C1-S2`: first defended major-chain reading path fixed

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

### P3-C1-S1S2 (History-aware cleanup admission and stop reasons fixed | 2026-04-08)

- headSha: `<pending commit for S0F-4G/P3-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-4G-doc-history-surface-and-extraction-before-cleanup-gate.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - later cleanup has one explicit third admission test beyond standing and redirect duty
  - later cleanup has one explicit stop-reason set when history extraction is still incomplete
- observed:
  - `S0F-4G/P3` now requires `history extracted enough` before a historical source log becomes a default cleanup candidate
  - the lane now fixes explicit stop and no-op reasons for cases where old logs still carry core explanatory value despite already losing current-state primacy

### P4-C1-S1S2 (First pilot source set and major-chain path fixed | 2026-04-08)

- headSha: `<pending commit for S0F-4G/P4-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-4G-doc-history-surface-and-extraction-before-cleanup-gate.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo has one bounded first-pilot source set for `DOC` history extraction
  - the repo has one defended major-chain reading path instead of an open-ended archive scan
- observed:
  - `S0F-4G/P4` now fixes the first cross-era pilot source packet and explicitly classifies secondary-context logs out of the primary extraction lane
  - later history publication can now start from one compressed `S0B -> S0C -> S0D -> S0E -> S0F` structural arc rather than from an unconstrained full-history dump

## Recent changes (for traceability, optional)

- 2026-04-08: opened `S0F-4G` as the next bounded follow-up so later history extraction and cleanup work can proceed through a reusable mechanism instead of ad hoc archaeology.
- 2026-04-08: completed `P1` so compact contract-history blocks now have one fixed minimum shape and one explicit source-owner-only chronology boundary.
- 2026-04-08: completed `P2` so the first `DOC` lineage-view shape and its navigation split are now explicit.
- 2026-04-08: completed `P3` so cleanup admission now includes one explicit history-extraction gate and one history-missing stop-reason set.
- 2026-04-08: completed `P4` so the first `DOC` history pilot now has one bounded source set and one defended major-chain reading path.