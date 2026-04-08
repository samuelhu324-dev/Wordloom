# log-S0F-3L (Phase 3L: old GC root redirect replacement and stub model)

---

**id**: `S0F-3L`
**kind**: `log`
**title**: `old GC root redirect replacement and stub model v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Cleanup, Redirect, GC, epic/s0, sub/3l`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-3K-history-aware-old-gc-cleanup-recheck-after-doc-history-publication.md`
  **reference_log_1**: `docs/logs/log-S0F-3J-old-gc-cleanup-candidate-selection-after-doc-reader-stabilization.md`
  **reference_log_2**: `docs/logs/log-S0F-3K-history-aware-old-gc-cleanup-recheck-after-doc-history-publication.md`
  **reference_log_3**: `docs/logs/log-S0F-4G-doc-history-surface-and-extraction-before-cleanup-gate.md`
  **reference_log_4**: `docs/governance/views/view-gc-triage-and-retention-rule-v1.md`
  **reference_log_5**: `docs/governance/views/view-gc-first-cleanup-boundary-v1.md`
  **reference_log_6**: `docs/governance/views/view-doc-history-and-lineage-v1.md`
  **reference_log_7**: `docs/governance/contracts/support-only/INDEX.md`
  **reference_log_8**: `docs/governance/contracts/GC-ISS-0001-issue-creation-metadata-english-body.md`
  **reference_log_9**: `docs/governance/contracts/GC-PRB-0001-historical-drift-fail-on-findings.md`
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
**created**: `2026-04-09`
**updated**: `2026-04-09`

---

## Decision / Outcome

**Decision**:

- `S0F-3L` opens the next bounded follow-up after `S0F-3K` so the repo can test one concrete question that remains after the history-aware recheck: can preserved old root-level `GC-*` redirect records eventually stop carrying full retained bodies at root and move to a safer `root stub + replacement target` model without breaking old-ID landing, reader discoverability, or lineage reading?
- v1 of this slice is design-first and bounded:
  - it does not yet execute any file move
  - it does not reopen `GC-* -> DOC` promotion semantics
  - it does not assume a root-stub model is safe before one explicit replacement contract is defended
- The immediate job is to define what a valid redirect-preserving replacement would have to satisfy before later cleanup can reopen with a real move candidate.

**Default choices (phase defaults / v1)**:

- Treat the preserved old root-level subset from `S0F-3K` as the candidate family for this design lane, not the whole `GC-*` namespace.
- Preserve the already-defended rule that deprecated redirect contracts stay at `docs/governance/contracts/` root until discoverability is preserved by a stronger model, not by assumption.
- Prefer one explicit `root stub + target body + rewritten references + local index support` model over ad hoc redirect prose or silent path moves.
- Do not let the root stub become a second full retained body; if the model is valid, the stub should preserve landing and navigation, not duplicate the full historical text indefinitely.
- If no safe replacement model is defensible, the correct result for this slice may still be `no-op`; opening the slice does not commit the repo to relocation.

## PR Summary Inputs (optional)

- Use this block because `S0F-3L` is expected to define whether a later old-`GC-*` cleanup move can preserve redirect duty through a root-stub replacement model instead of through whole retained bodies at root.

**PR summary bullets**:

- Define the bounded replacement model for preserved old root-level `GC-*` redirect records.
- Test whether `root stub + replacement target` can preserve old-ID landing, discoverability, and lineage reading strongly enough for later cleanup admission.
- Separate design-time admissibility from actual relocation execution so later cleanup does not guess at reader safety.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the redirect-replacement design lane.

**PR links**:

- Log: `docs/logs/log-S0F-3L-old-gc-root-redirect-replacement-and-stub-model.md`
- Previous recheck: `docs/logs/log-S0F-3K-history-aware-old-gc-cleanup-recheck-after-doc-history-publication.md`
- First cleanup boundary: `docs/governance/views/view-gc-first-cleanup-boundary-v1.md`

## Exported Sections / Outlet Ownership

- This slice may end either in a retained design log or in one bounded support surface if the replacement model proves stable enough to reuse.

**Outlet ownership**:

- `contract`: only if this slice stabilizes one durable replacement admissibility rule beyond the current cleanup-boundary views
- `runbook`: only if a later operator-facing move procedure becomes stable enough to repeat
- `view`: only if later readers need one compact redirect-replacement summary beyond the existing cleanup-boundary views
- `index/front-door`: only the support-only index or local navigation mutations needed if a replacement target becomes real
- `disposition/placement`: actual keep / stub / target placement decisions for the selected old root-level subset if and only if the replacement model is defended strongly enough
- `log-retained core`: design constraints, comparison of replacement options, evidence, stop reasons, and any deferred execution boundary

## Definitions (optional)

- **root stub**: a minimal retained file at the old root path whose job is to preserve old-ID landing and point readers deterministically to the current replacement target
- **replacement target**: the non-root file that would hold the retained historical body if the repo stops keeping the full body at the old root path
- **redirect-preserving replacement**: a move model that keeps old path discoverability, reader orientation, and lineage reading explicit after the full retained body leaves the original root location

## Constraints

- Do not reopen the current `DOC` contract surface or the `S0F-4G` history package; this slice is about legacy redirect handling, not current-rule promotion.
- Do not move any preserved old root-level file merely because the stub model sounds plausible.
- Do not rely on one prose sentence in a root stub as the only discoverability mechanism if direct references or index surfaces would still break.
- Do not assume that the same replacement model must work for every preserved old root-level `GC-*` file.

## Scope

- `P0`: open `S0F-3L` and fix the next question as `redirect replacement model`, not as another generic cleanup scan
- `P1`: inventory what the preserved old root-level subset currently provides at root beyond raw file presence
- `P2`: define one bounded `root stub + replacement target` model and its minimum safety contract
- `P3`: test whether that model is defensible for the preserved `GC-ISS-*` and `GC-PRB-0001` subset or only for part of it
- `P4`: decide whether the next later slice should be a real execution package, a narrower pilot, or an explicit no-op because the replacement model is still unsafe

## Success Criteria (DoD)

- One reader can explain what the old root-level `GC-*` files still provide today besides simply existing at root.
- One reader can explain the minimum conditions a root-stub replacement would need to satisfy before any relocation becomes admissible.
- The repo has one explicit answer to whether redirect replacement should proceed as a full subset move, a narrower pilot, or a defended no-op.
- Later cleanup work no longer needs to improvise what `redirect duty safely replaced` would mean.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the preserved old root-level subset's remaining root duties are inventoried explicitly
  - one bounded replacement model and its minimum safety checks are explicit enough to defend
  - the next step is clear as `execute`, `pilot`, or `stop`

## P0 (Contract | v1)

### P0-C1-S1 (Problem boundary fixed | v1)

- `S0F-3L` is now opened as the redirect-replacement follow-up to `S0F-3K`.
- This slice does not ask whether history is extracted enough.
- It asks whether root-path redirect duty can be preserved by something weaker than a full retained body at root.

### P0-C1-S2 (Immediate sequencing fixed | v1)

- The immediate next work after scaffold is now:
  - first inventory the real jobs the preserved old root-level files still perform
  - then define a concrete root-stub replacement model
  - then decide whether that model is safe for the current preserved subset
- This keeps design proof ahead of any relocation attempt.

## P1 (Root-duty inventory | v1)

### P1-C1-S1 (Root-level redirect duties inventoried for the preserved subset | v1)

- The preserved subset still owns one real root-path reader job that has not yet been replaced elsewhere:
  - old-ID landing on the exact historical root path
  - deterministic redirect from that old path toward the current successor contract or successor pair
  - direct path discoverability for lineage and cleanup-boundary views that still enumerate the preserved legacy set explicitly
- For the `GC-ISS-*` subset, the strongest current evidence is now aligned across three surfaces:
  - the old `GC-ISS-*` records remain preserved with `Legacy Redirect` notes inside the files themselves
  - `view-iss-split-package-v1.md` explicitly says to keep all old `GC-ISS-*` file paths in place and keep the old record IDs valid
  - the first cleanup boundary still lists those exact root paths as preserved legacy redirects
- For `GC-PRB-0001`, the preserved root duty is similar but slightly stronger:
  - the file remains the old umbrella landing path after the `PRB -> PRR / PRG` split
  - it still carries the redirect to both current successors inside the file
  - it is still referenced as the canonical deprecated umbrella sample by split-package, cleanup-boundary, and early registry-model surfaces

### P1-C1-S2 (Root-only duties separated from already-replaced duties | v1)

- The preserved subset no longer owns the current effective rule meaning itself:
  - `GC-ISS-0001` through `GC-ISS-0005` already read currently through `GC-ICR-0001`, `GC-ICL-0001`, `GC-ICT-0001`, `GC-IID-0001`, and `GC-IID-0002`
  - `GC-PRB-0001` already reads currently through `GC-PRR-0001` and `GC-PRG-0001`
- The preserved subset also does not own the broad history-extraction function that blocked earlier cleanup debate:
  - `S0F-4G` already published the `DOC` lineage view and compact-history write-backs for that job
- The `GC-PRB-0001` paired support-only backtrace body is already separated successfully:
  - the backfill note now lives under `docs/governance/contracts/support-only/`
  - `docs/governance/contracts/support-only/INDEX.md` already gives it a local navigation home
- The remaining live question for this slice is therefore narrower than a whole-file semantic migration:
  - can the repo replace `root-path landing + deterministic redirect + direct path discoverability` with a stub model
  - without needing the full retained body to remain at root

## P2 (Replacement model | v1)

### P2-C1-S1 (Root-stub minimum shape fixed for preserved old GC redirects | v1)

- `S0F-3L/P2` now fixes one reusable root-stub minimum for this contract family.
- The stub must preserve the old root path as a readable landing surface rather than deleting the old file path outright.
- The minimum stub shape for preserved old `GC-*` records is now:
  - one stub heading that keeps the old record identity visible, for example `# governance-contract-stub: <record_id>`
  - one metadata block that records:
    - `record_id`
    - `contract_id`
    - `status: archived`
    - `moved_from`
    - `moved_to`
    - `moved_at`
  - one `This file moved` section that points readers to:
    - the current active successor record or successor pair
    - the moved support-only full-body target when the historical wording itself is needed
  - one `Reader Notes` block that states:
    - the root path remains occupied to preserve old-ID landing
    - current rule meaning should be read through the successor current records
    - the stub is not the editable retained body
    - `Do not edit here`
- This shape intentionally does not copy the whole legacy contract body into the stub.
- The stub is a bridge surface, not a second retained full-body clone.

### P2-C1-S2 (Replacement-target and navigation-support contract fixed | v1)

- The replacement target for any moved full retained body is now fixed to the existing contracts-side support-only surface:
  - `docs/governance/contracts/support-only/<same-basename>.md`
- `P2` reuses the existing support-only contract-location model rather than inventing a special-case directory for preserved old `GC-*` redirects.
- The navigation split is now fixed as follows:
  - keep old root-path citations unchanged when the reader job is old-ID landing, split-package lineage, or cleanup-boundary enumeration of the preserved legacy set
  - rewrite direct references only when a surface is supposed to open the full retained historical body rather than merely land on the old ID and follow successor guidance
  - list every moved full-body target in `docs/governance/contracts/support-only/INDEX.md` so support-only discoverability remains explicit
  - record the final keep-root-citation versus retarget-to-support-only decision in one bounded cleanup manifest during later execution
- The execution gate for any later move is now explicit:
  - one cleanup-execution owner must reopen before any preserved old root-level file is rewritten
  - the support-only index must already remain the stable local front door for moved bodies
  - the move must prove that bounded direct-navigation rewrites are sufficient and that mass lineage-view rewrites are not required
- `P2` therefore fixes the model boundary clearly:
  - root stub preserves landing and redirect duty
  - support-only target preserves the full retained body
  - only a bounded direct-navigation set should move to the support-only target
  - broad lineage and old-ID readers may continue to cite the root path through the stub

## Plan (draft)

### P1 (Root-duty inventory)

- P1-C1-S1: inventory old-ID landing, direct link discoverability, and lineage-reading functions for the preserved root subset
- P1-C1-S2: separate duties already covered elsewhere from duties still owned only by the root paths

### P2 (Replacement model)

- P2-C1-S1: define the minimum shape of a valid root stub
- P2-C1-S2: define the required replacement target, reference rewrites, and index support surfaces

### P3 (Applicability test)

- P3-C1-S1: test whether one model works for `GC-ISS-*` and `GC-PRB-0001` together or whether the subset splits further
- P3-C1-S2: record explicit fail reasons if the model is not yet safe

### P4 (Next-lane decision)

- P4-C1-S1: choose among full execution package, narrower pilot, or defended no-op

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: problem boundary fixed
- [x] `P0-C1-S2`: immediate sequencing fixed

### P1 (Root-duty inventory)

- [x] `P1-C1-S1`: root-level redirect duties inventoried
- [x] `P1-C1-S2`: root-only versus already-replaced duties separated

### P2 (Replacement model)

- [x] `P2-C1-S1`: root-stub minimum shape fixed
- [x] `P2-C1-S2`: replacement-target and navigation support contract fixed

### P3 (Applicability test)

- [ ] `P3-C1-S1`: preserved subset applicability tested
- [ ] `P3-C1-S2`: stop reasons or split rules fixed if needed

### P4 (Next-lane decision)

- [ ] `P4-C1-S1`: next execution boundary decided

## Current Status (recommended)

- `S0F-3L` is now opened as the bounded follow-up after `S0F-3K`.
- The repo now has one explicit place to answer whether root-level legacy redirect reading can be preserved through a stub model instead of through whole retained bodies.
- `P1` is now complete: the preserved root-level subset still owns old-path landing, deterministic redirect, and some direct path discoverability, but it no longer owns the current effective rule meaning itself.
- `P2` is now complete: the repo now has one explicit root-stub minimum shape, one fixed support-only replacement-target model, and one navigation split between root-stub citations and moved full-body citations.
- No relocation result is assumed yet; this slice remains design-first, but it is now ready to enter `P3`.
- The immediate next step is `P3`: test whether this one model can cover both the `GC-ISS-*` split set and the `GC-PRB-0001` umbrella cleanly, or whether the preserved subset must split into a narrower pilot.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this section will hold the source inventory and model-comparison results for the replacement design lane.
- This scaffold records the opening event and bounded next-step contract for `S0F-3L`.

### P0-C1-S1S2 (Redirect-replacement design lane opened | 2026-04-09)

- headSha: `<pending commit for S0F-3L/P0-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-3L-old-gc-root-redirect-replacement-and-stub-model.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo has one explicit bounded slice for redirect-replacement design after the `S0F-3K` recheck
  - later work no longer needs to overload `S0F-3K` with stub-model design questions
- observed:
  - `S0F-3L` is now opened with a design-first boundary, fixed P1-P4 sequence, and explicit non-goal of immediate relocation

### P1-C1-S1S2 (Preserved root-duty inventory fixed | 2026-04-09)

- headSha: `<pending commit for S0F-3L/P1-C1-S1S2>`
- artifacts:
  - `artifacts/_tmp_s0f_3l_p1_root_duty_inventory_20260409.json`
  - `docs/governance/INDEX.md`
  - `docs/governance/views/view-iss-split-package-v1.md`
  - `docs/governance/views/view-prb-split-package-v1.md`
  - `docs/governance/views/view-gc-first-cleanup-boundary-v1.md`
  - `docs/governance/contracts/support-only/INDEX.md`
  - `docs/logs/log-S0F-3L-old-gc-root-redirect-replacement-and-stub-model.md`
- expected:
  - the repo has one explicit inventory of what the preserved old root-level subset still provides at root
  - the repo has one explicit separation between root-only duties and duties already replaced elsewhere
- observed:
  - the preserved subset still owns old-path landing, deterministic redirect, and direct path discoverability for some legacy boundary views
  - current semantics, broad family history orientation, and the PRB support-only backtrace body are already owned by newer surfaces outside the preserved root files

### P2-C1-S1S2 (Root-stub and replacement-target contract fixed | 2026-04-09)

- headSha: `<pending commit for S0F-3L/P2-C1-S1S2>`
- artifacts:
  - `docs/logs/support-only/s0f-3l-gc-root-stub-preview.md`
  - `docs/governance/contracts/support-only/INDEX.md`
  - `docs/governance/views/view-gc-triage-and-retention-rule-v1.md`
  - `docs/logs/log-S0F-1K-lifecycle-exact-path-successor-package.md`
  - `docs/logs/log-S0F-3L-old-gc-root-redirect-replacement-and-stub-model.md`
- expected:
  - the repo has one explicit minimum root-stub shape for preserved old `GC-*` redirects
  - the repo has one explicit support-only replacement-target and navigation-support contract for any later move round
- observed:
  - the root-stub preview now shows both single-successor and multi-successor preserved old-`GC-*` cases
  - the replacement model now reuses the existing contracts-side support-only surface and keeps mass reader rewrites out of bounds by default

## Recent changes (for traceability, optional)

- 2026-04-09: opened `S0F-3L` as the redirect-replacement and stub-model follow-up after the `S0F-3K` refined no-op result.
- 2026-04-09: completed `P1` by inventorying the preserved subset's remaining root-path duties and separating them from duties already replaced by current successors, lineage views, or support-only backtrace surfaces.
- 2026-04-09: completed `P2` by fixing the minimum root-stub shape, the support-only replacement-target model, and the navigation split that a later cleanup-execution round would have to preserve.