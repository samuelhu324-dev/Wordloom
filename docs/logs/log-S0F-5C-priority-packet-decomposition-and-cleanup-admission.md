# log-S0F-5C (Phase 5C: priority-packet decomposition and cleanup admission)

---

**id**: `S0F-5C`
**kind**: `log`
**title**: `priority-packet decomposition and cleanup admission v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Records, Migration, Cleanup, Decomposition, epic/s0, sub/5c`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-6C-outlet-and-lifecycle-observability.md`
  **reference_log_1**: `docs/logs/log-S0F-5B-old-s0-migration-ledger-view-and-support-only-inventory-model.md`
  **reference_log_2**: `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
  **reference_log_3**: `docs/logs/log-S0F-6C-outlet-and-lifecycle-observability.md`
  **reference_log_4**: `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  **reference_log_5**: `docs/governance/views/view-old-s0-migration-ledger-v1.md`
  **reference_log_6**: `docs/governance/views/view-old-s0-series-s0e-standing-v1.md`
  **reference_log_7**: `docs/governance/views/view-old-s0-series-s0f-standing-v1.md`
**issue_keyword**: `migration`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/5`
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
**created**: `2026-04-09`
**updated**: `2026-04-09`

---

## Decision / Outcome

**Decision**:

- `S0F-5C` opens as the bounded follow-up for one specific gap now visible after `S0F-5B`, `S0F-6B`, and `S0F-6C`: several old-`S0` logs have clearly influenced current `DOC` or lifecycle reading, but they still remain outside the defended surfaced set as one unresolved remainder.
- This slice does not start by widening the surfaced set indiscriminately and does not start by cleaning historical logs mechanically.
- It first fixes one priority-first decomposition model so later work can separate:
  - high-value current-adjacent packets that should be decomposed into defended current homes first
  - lower-priority or mixed-standing rows that may later become retained-only, `no-op`, `non-doc`, or cleanup-admission candidates
  - cleanup candidates that are not yet safe to move, rehome, or demote because current-reader dependence is still mixed
- The first explicitly admitted priority packets for this slice are now:
  - `priority A`: the `S0F-1H` / `S0F-1I` / `S0F-1J` PR-body completeness packet
  - `priority B`: the `S0E-5A` plus `S0E-7D` / `S0E-7E` / `S0E-7F` / `S0E-7G` lifecycle-and-workflow packet
- The first cleanup question for this slice is intentionally deferred behind those packet decompositions: old logs should be considered for cleanup admission only after the current-adjacent packets above have either landed into defended current homes or been explicitly classified as retained-only / `no-op` / `non-doc`.
- `P1` is now complete: one reusable packet-priority test and one cleanup-admission gate are now fixed, so later packet work no longer needs to improvise whether a row should be decomposed first, deferred as mixed-standing, or admitted into a real cleanup lane.
- `P2` is now complete: the `S0F-1H` / `S0F-1I` / `S0F-1J` packet is no longer treated as one unresolved `DOC` candidate remainder, and its defended result is now fixed as `GC current registry` current-home concentration plus one retained convergence-evidence row rather than one next `DOC` surfaced packet.

**Default choices (phase defaults / v1)**:

- Do not treat `outside the surfaced set` as equivalent to `safe to clean up`.
- Prefer packet-level decomposition over row-by-row ad hoc reclassification when several logs already read as one shared current-adjacent story.
- Prefer resolving the strongest current-adjacent packets first, because they reduce future cleanup ambiguity more than early historical tail rows do.
- If a packet still mixes current-reader dependence, support-only operator dependence, and unresolved cleanup standing, keep the root file in place and record a defended non-write defer result instead of forcing relocation.
- Reuse the surfaced-set model from `S0F-5B` and the standing vocabulary from `S0F-6B`; do not invent a second migration vocabulary inside this slice.

## Problem Statement

- The repo now has one support-only migration working ledger, one reader-facing migration projection, one coverage overview, and one per-series standing layer for old `S0` material.
- Those surfaces make one gap newly visible: several logs have already been processed and clearly affect current reading, but they still sit in the unresolved remainder because no later slice has yet decomposed them into defended packet-level outcomes.
- Without that decomposition layer, the repo risks two weak moves:
  - cleaning old logs too early because they look historical even though current readers still depend on them indirectly
  - leaving current-adjacent packets unresolved indefinitely because they are buried inside one large `unreviewed` remainder
- `S0F-5C` therefore exists to decide which unresolved packets should be decomposed first and which rows are still not ready for cleanup admission.

## PR Summary Inputs (optional)

- Use this block because `S0F-5C` is expected to fix the next bounded decomposition priorities for unresolved old-`S0` packets before later cleanup work begins.

**PR summary bullets**:

- Define the priority-first packet model for decomposing already-processed but not-yet-surfaced old-`S0` logs.
- Separate current-adjacent packet decomposition from later cleanup admission so unresolved logs are not cleaned mechanically.
- Sequence the first two bounded packet families before any broader old-`S0` cleanup lane opens.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the decomposition-priority lane.

**PR links**:

- Log: `docs/logs/log-S0F-5C-priority-packet-decomposition-and-cleanup-admission.md`
- Previous log: `docs/logs/log-S0F-6C-outlet-and-lifecycle-observability.md`

## Exported Sections / Outlet Ownership

- This slice starts as a source-log-first prioritization and packet-boundary lane.
- No new outlet family is exported by default here; later phases may justify updates to the support-only migration inventory, reader-facing views, or cleanup standing only after packet outcomes are defended.

**Outlet ownership**:

- `contract`: no-op for now; `S0F-5C` starts by classifying packet destinations rather than drafting new current rule bodies
- `runbook`: no-op for now; this slice starts as decomposition and cleanup-admission triage rather than repeatable operator procedure
- `view`: existing shared standing view updates are now allowed when one packet result is defended strongly enough to replace `unreviewed` with a bounded reader-facing standing
- `index/front-door`: no-op for now; no broader navigation mutation is warranted before packet decomposition is complete
- `disposition/placement`: existing support-only inventory or retained-placement updates are now allowed when packet review proves one stable retained-only or non-write-defer standing worth writing back
- `log-retained core`: keep this source log for priority model, packet boundaries, cleanup-admission gate, and evidence ledger

## Definitions (optional)

- **priority packet**: one bounded cluster of old-`S0` logs that should be decomposed together because they share one current-adjacent reading problem or one cleanup decision boundary
- **current-adjacent packet**: a packet whose logs already shape current `DOC`, lifecycle, runbook, or observability reading even if the old logs are not yet surfaced directly
- **cleanup admission**: the explicit judgment that a row or packet is safe to enter a real cleanup lane because current-reader dependence has already been replaced or bounded safely
- **non-write defer**: a defended result that no file move or cleanup mutation is safe yet even though the packet has been reviewed

## Constraints

- Do not open cleanup execution before the first priority packets have explicit current-home or retained-only decisions.
- Do not force packet decomposition to end in `DOC` absorption; `runbook`, `retained-evidence`, `no-op`, and `non-doc` remain valid outcomes when defended.
- Do not widen to whole-series exhaustive review inside this slice; this lane is about priority packets, not repo-wide reclassification.
- Do not relocate mixed-standing logs simply because part of their meaning has already been extracted elsewhere.

## Scope

- `P0`: open `S0F-5C`, fix the priority-first decomposition boundary, and wire it into the parent spine
- `P1`: define the packet-priority model and the admission rule for `priority A` versus `priority B`
- `P2`: decompose the `S0F-1H` / `S0F-1I` / `S0F-1J` PR-body completeness packet into defended current-home outcomes
- `P3`: decompose the `S0E-5A` plus `S0E-7D` / `S0E-7E` / `S0E-7F` / `S0E-7G` lifecycle-and-workflow packet into defended current-home outcomes
- `P4`: define the first cleanup-admission rule and first candidate subset after the higher-priority packets have been adjudicated

## Success Criteria (DoD)

- One reader can explain why `S0F-1H` / `S0F-1I` / `S0F-1J` are handled as one priority packet instead of three isolated unresolved rows.
- One reader can explain why `S0E-5A` and `S0E-7D` through `S0E-7G` form the next lifecycle/workflow packet instead of being cleaned independently.
- Later widening work can classify packet outcomes without reopening `S0F-5B` ledger semantics or `S0F-6B` standing vocabulary.
- Later cleanup work can distinguish `not yet surfaced` from `safe to clean` using one explicit admission rule.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the packet-priority model is explicit enough to reuse
  - the first two admitted packets have defended current-home outcomes or defended non-write defer outcomes
  - the first cleanup-admission rule is explicit enough that a later cleanup slice can start from it without reopening packet-priority rationale

## P0 (Contract | v1)

### P0-C1-S1 (Priority-first decomposition boundary fixed | v1)

- `S0F-5C` is now opened as the lane for decomposing unresolved old-`S0` logs by priority packet rather than by generic age or series alone.
- This slice does not claim that all unresolved old-`S0` rows now need immediate classification.
- It fixes that the next work should begin where current reading value is strongest and cleanup ambiguity is highest.

### P0-C1-S2 (Initial packet queue fixed | v1)

- The initial packet queue for this slice is now fixed as:
  - `priority A`: `S0F-1H` / `S0F-1I` / `S0F-1J`
  - `priority B`: `S0E-5A` / `S0E-7D` / `S0E-7E` / `S0E-7F` / `S0E-7G`
- The queue is intentionally current-adjacent first:
  - the PR-body completeness packet already touches current reviewer, runbook, task, and CI reading
  - the lifecycle/workflow packet already touches current lifecycle and failure semantics, but still needs sharper packet-level current-home judgment

## Plan (draft)

### P1 (Priority model)

- `P1-C1-S1`: fix the packet-priority criteria and why packet-level decomposition beats generic row-ordering here
- `P1-C1-S2`: fix the admission test for `priority A`, `priority B`, and later cleanup candidates

### P1-C1-S1 (Packet-priority criteria fixed | v1)

- Packet priority is now fixed by five coordinated criteria rather than by age or series position alone:
  - `current-reading leverage`
  - `packet coherence`
  - `bounded current-home hypothesis`
  - `shared-surface write-back leverage`
  - `cleanup-risk reduction`
- `current-reading leverage` answers whether the packet already shapes present-day reading through current contracts, runbooks, repo tasks, CI gates, or lifecycle/observability surfaces even though the source logs themselves are still outside the surfaced set.
- `packet coherence` answers whether the rows form one real bounded story that should be adjudicated together rather than as isolated leftovers.
- `bounded current-home hypothesis` answers whether the likely current-home family and outlet set is already narrow enough to test without reopening whole-repo taxonomy.
- `shared-surface write-back leverage` answers whether one defended packet result can later update shared views, inventory, or packet-local retained surfaces without widening to a whole-series rewrite.
- `cleanup-risk reduction` answers whether decomposing this packet first will materially reduce the chance of premature cleanup or misclassification later.
- The packet-priority rule is now:
  - `priority A` when all five criteria are strong and the packet already has one narrow current-adjacent reading concentration
  - `priority B` when current-reading leverage and packet coherence are already strong, but bounded current-home judgment still mixes rule, runbook, wrapper, or retained-history separation that must be adjudicated next
  - later cleanup candidates only after packet-level current-home ambiguity has been reduced enough that cleanup risk no longer dominates the next decision
- The current admitted queue now reads as:
  - `priority A`: `S0F-1H` / `S0F-1I` / `S0F-1J` because this packet already concentrates one PR-body completeness story across reviewer, convergence, operator runbook, repo task, CI gate, and completed live lifecycle packaging
  - `priority B`: `S0E-5A` plus `S0E-7D` / `S0E-7E` / `S0E-7F` / `S0E-7G` because this packet already concentrates one lifecycle-and-workflow story, but still mixes current contract meaning with planner, thin-gate, wrapper, and transport history that must be separated before any later surfaced write-back

### P1-C1-S2 (Packet and cleanup-admission tests fixed | v1)

- A packet is now admitted into decomposition only when all of the following are true:
  - the candidate rows form one bounded packet with a defensible shared reading problem
  - the packet already has current-adjacent leverage outside the retained source logs
  - the likely current-home outcomes are narrow enough to adjudicate within one bounded follow-up
  - later write-back targets are already known in class, even if not yet fixed in exact row form
  - decomposing the packet first reduces future cleanup ambiguity more than direct cleanup would
- A packet should be held as `non-write defer` rather than forced into premature write-back when any of the following remain true:
  - current-reader dependence is still mixed across contract, runbook, parent navigation, retained lifecycle surfaces, or issue/PR-prep surfaces
  - the root file is still consumed as one readable current-adjacent source rather than as dead history only
  - the remaining blockers are upstream ownership changes rather than cleanup-local moves
- Cleanup admission is now allowed only when all of the following are true:
  - the relevant higher-priority packet has already been adjudicated
  - current-reader dependence has already moved to defended current homes or to defended retained-only standing
  - the candidate row or packet no longer mixes current-adjacent and cleanup-local responsibilities inside the same root file
  - the remaining outcome is narrow enough to classify as retained-only, `no-op`, `non-doc`, or explicit cleanup candidate without reopening packet taxonomy
- Cleanup admission is now blocked when any of the following remain true:
  - only partial support-only standing exists while current-adjacent reading still depends on the root file
  - blocker inventory still spans contract, runbook, parent/adjacent logs, or lifecycle surfaces that have not yet been rehomed or bounded
  - the packet would need speculative relocation rather than one defended current-home or retained-only answer
- When cleanup admission is blocked but the blocker set is explicit, the required result is now one defended `non-write defer` with:
  - one blocker split between cleanup-local blockers and upstream ownership blockers
  - one explicit unblock condition list for later re-entry
  - no speculative file move merely to make the backlog look smaller

### P2 (Priority A packet)

- `P2-C1-S1`: classify the `S0F-1H` / `S0F-1I` / `S0F-1J` packet by current-home and retained-only boundaries
- `P2-C1-S2`: write back the defended packet result to the appropriate shared surfaces without over-widening the lane

### P2-C1-S1 (PR-body completeness packet classified | v1)

- The `S0F-1H` / `S0F-1I` / `S0F-1J` packet is now fixed as one coherent PR-body completeness packet rather than three independent unresolved `S0F` rows.
- The packet stays current-adjacent because it already shapes:
  - reviewer classification semantics
  - the stable operator runbook
  - formatting-only convergence history
  - packaged local-task and workflow-dispatch gate usage
  - the completed live lifecycle packaging proof
- The defended packet split is now:
  - `S0F-1H`:
    - current family outcome: `GC current registry`
    - current-home outcome: `GC-PRR-0001`
    - standing outcome inside old-`S0` review: `non-doc`
    - reason: the row no longer reads first through `DOC`; current rule meaning now concentrates in the active reviewer-classification record, while the reviewer-owned runbook remains the stable operator path rather than a second current contract
  - `S0F-1I`:
    - current family outcome: `GC current registry` with retained support-only evidence
    - current-home outcome: `GC-PRG-0001` plus the reviewer-owned runbook as the enduring operator path
    - standing outcome inside old-`S0` review: `retained-evidence`
    - reason: the formatting-only convergence lane is no longer the stable current source for gate semantics or operator procedure; it now survives mainly as bounded convergence evidence and historical bridge context
  - `S0F-1J`:
    - current family outcome: `GC current registry`
    - current-home outcome: `GC-PRG-0001`
    - standing outcome inside old-`S0` review: `non-doc`
    - reason: the packet's current gate meaning now concentrates in the active standard-check governance record, while repo task and workflow-dispatch packaging remain enforcement surfaces and retained execution proof rather than a separate new family-owned current rule surface
- The packet-level judgment is therefore explicit:
  - this is not the next `DOC` absorption packet
  - this is one resolved non-`DOC` current-adjacent packet with one retained-evidence middle row
  - later cleanup should not treat the packet as one open `DOC` widening candidate anymore

### P2-C1-S2 (Priority A packet written back to shared surfaces | v1)

- The defended packet result is now written back only to existing shared surfaces that match the packet's real job:
  - the `S0F` series standing view now stops presenting `S0F-1H`, `S0F-1I`, and `S0F-1J` as unresolved remainder rows
  - the support-only migration working ledger now records the packet outcome explicitly so later cleanup review can distinguish finished non-`DOC` adjudication from still-open remainder
- No new reader-facing migration ledger row is added to the `DOC` surfaced projection because this packet does not widen the current `DOC` surfaced set.
- No broader front-door mutation is warranted at this stage because the packet result sharpens standing, not family navigation.

### P3 (Priority B packet)

- `P3-C1-S1`: classify the `S0E-5A` / `S0E-7D` / `S0E-7E` / `S0E-7F` / `S0E-7G` packet by current-home and retained-only boundaries
- `P3-C1-S2`: write back the defended packet result to the appropriate shared surfaces without treating wrapper/orchestration history as parallel current rule surfaces

### P4 (Cleanup admission)

- `P4-C1-S1`: fix the first cleanup-admission rule after current-adjacent packets are adjudicated
- `P4-C1-S2`: admit one first safe cleanup-candidate subset or explicit non-write defer result

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: priority-first decomposition boundary fixed
- [x] `P0-C1-S2`: initial packet queue fixed

### P1 (Priority model)

- [x] `P1-C1-S1`: packet-priority criteria fixed
- [x] `P1-C1-S2`: priority and cleanup-admission test fixed

### P2 (Priority A packet)

- [x] `P2-C1-S1`: PR-body completeness packet classified
- [x] `P2-C1-S2`: PR-body completeness packet written back to shared surfaces

### P3 (Priority B packet)

- [ ] `P3-C1-S1`: lifecycle/workflow packet classified
- [ ] `P3-C1-S2`: lifecycle/workflow packet written back to shared surfaces

### P4 (Cleanup admission)

- [ ] `P4-C1-S1`: cleanup-admission rule fixed
- [ ] `P4-C1-S2`: first cleanup candidate subset or non-write defer admitted

## Current Status (recommended)

- `S0F-5C` is now opened as the bounded follow-up for priority-first decomposition of unresolved old-`S0` packets.
- `P0` is now complete: the lane boundary and the first two admitted priority packets are fixed.
- `P1` is now complete: one reusable packet-priority test and one cleanup-admission gate now distinguish `priority A`, `priority B`, `non-write defer`, and real cleanup admission.
- `P2` is now complete: the PR-body completeness packet is adjudicated as `GC current registry` current-home concentration plus one retained-evidence bridge row, and the shared standing surfaces no longer treat that packet as unresolved `DOC` remainder.
- The immediate next step is `P3`: classify the `S0E-5A` plus `S0E-7D` / `S0E-7E` / `S0E-7F` / `S0E-7G` lifecycle-and-workflow packet by current-home and retained-only boundaries.

## Evidence (reserved)

### P0-C1-S1S2 (S0F-5C scaffold and initial packet queue landed | 2026-04-09)

- headSha: `<pending commit for S0F-5C/P0-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-5C-priority-packet-decomposition-and-cleanup-admission.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo has one explicit lane for priority-first packet decomposition before later cleanup admission
  - later work no longer needs to improvise whether current-adjacent unresolved logs should be absorbed, retained, deferred, or cleaned first
- observed:
  - `S0F-5C` is now opened as the bounded packet-decomposition and cleanup-admission lane
  - the first admitted queue is now fixed as the PR-body completeness packet first and the lifecycle/workflow packet second

### P1-C1-S1S2 (Packet-priority criteria and cleanup-admission gate fixed | 2026-04-09)

- headSha: `<pending commit for S0F-5C/P1-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-5C-priority-packet-decomposition-and-cleanup-admission.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - later packet work should be able to explain why one packet is decomposed now while another row stays deferred for later cleanup review
  - cleanup should stay blocked whenever current-reader dependence is still mixed, even if a row already looks historical
- observed:
  - `priority A` is now fixed around the PR-body completeness packet because its current-adjacent reading concentration is already strong and bounded
  - `priority B` is now fixed around the lifecycle/workflow packet because its current reading value is strong but still mixes current-rule and wrapper-history separation
  - cleanup admission is now explicitly gated behind packet adjudication plus mixed-standing clearance, with defended `non-write defer` required when only upstream ownership blockers remain

### P2-C1-S1S2 (PR-body completeness packet adjudicated and written back to shared standing surfaces | 2026-04-09)

- headSha: `<pending commit for S0F-5C/P2-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-5C-priority-packet-decomposition-and-cleanup-admission.md`
  - `docs/governance/views/view-old-s0-series-s0f-standing-v1.md`
  - `docs/governance/views/support-only/inventory-old-s0-migration-working-ledger-v1.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the first priority packet should stop reading as unresolved old-`S0` remainder once its current homes are already defensible outside the `DOC` surfaced set
  - later cleanup review should be able to distinguish active non-`DOC` current-home concentration from true unresolved backlog
- observed:
  - `S0F-1H` and `S0F-1J` now read as non-`DOC` current-adjacent rows whose current rule meaning concentrates in `GC-PRR-0001` and `GC-PRG-0001`
  - `S0F-1I` now reads as retained convergence evidence rather than as an unresolved current-home candidate
  - the packet now resolves as one completed non-`DOC` adjudication rather than as the next `DOC` widening candidate

## Recent changes (for traceability, optional)

- 2026-04-09: opened `S0F-5C` as the bounded follow-up for priority-first decomposition of unresolved old-`S0` packets before any broader cleanup lane opens.
- 2026-04-09: completed `S0F-5C/P1` by fixing the reusable packet-priority criteria and the cleanup-admission gate before any packet write-back or cleanup execution begins.
- 2026-04-09: completed `S0F-5C/P2` by adjudicating the `S0F-1H` / `S0F-1I` / `S0F-1J` packet as non-`DOC` current-home concentration plus retained convergence evidence, and by writing that result back to the shared `S0F` standing surfaces.