# log-S0F-3E (Phase 3E: governance registry lineage and legacy handling)

---

**id**: `S0F-3E`
**kind**: `log`
**title**: `governance registry lineage and legacy handling v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Governance, Contract, Registry, Legacy, Lineage, epic/s0, sub/3e`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-3D-first-governance-contract-landing-batch.md`
  **reference_log_1**: `docs/logs/log-S0F-3B-governance-contract-registry-and-naming-model.md`
  **reference_log_2**: `docs/logs/log-S0F-3C-governance-contract-series-audit-and-admission.md`
  **reference_log_3**: `docs/logs/log-S0F-3D-first-governance-contract-landing-batch.md`
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

- `S0F-3E` opens the next follow-up slice for governance-registry lineage and legacy handling.
- This slice exists because the registry now needs one explicit answer for two different evolutionary moves:
  - `split into`: one prior area or record is broken into multiple narrower current surfaces
  - `absorbed into`: one prior area or record is folded into a newer current surface without remaining as an independent active rule
- v1 treats these moves as registry-lineage problems rather than as ad hoc file-renaming chores.
- The target is not to delete historical files. The target is to keep current-state reading clean while preserving old files, old IDs, and old references as traceable history.

**Default choices (phase defaults / v1)**:

- `INDEX.md` remains the only front-door current-state registry surface.
- Old contract files are not deleted merely because a later split or absorption happened.
- When one area is replaced by narrower areas, the old area should become `frozen legacy` rather than remain an active area that still receives new sequence numbers.
- When one record is absorbed into another current record, the old file should remain readable as history but should stop acting as a current active explanation surface.
- Legacy preservation and current-state readability must be solved together; either one without the other will turn the registry into noise.
- Registry lineage verbs must be mutually legible: readers should be able to tell whether a change created multiple descendants, one replacement, one absorption into a broader current rule, or a pure end-of-life with no active successor.

## Scope

- `P0`: open `S0F-3E`, wire it into the `S0F` spine, and define the lineage/legacy problem explicitly
- `P1`: define the canonical lineage verbs for registry evolution, including `split into` and `absorbed into`
- `P2`: define how old areas become `frozen legacy` and stop receiving new numbers after a split
- `P3`: define how old records remain stored, cited, and redirected after absorption or split
- `P4`: define how current-state indexing and historical storage stay separated so old references remain usable without polluting the front door
- `P5`: define the first migration package that can later apply these rules to already-landed coarse areas such as `ISS`

## Current Status

- `S0F-3E` is now opened as the next `S0F` follow-up slice for governance-registry lineage and legacy handling.
- The immediate motivation is already concrete: the first landing batch under `S0F-3D` proved that coarse areas can carry multiple parallel active contracts, which now raises the need for explicit split and absorption handling before future registry growth continues.
- `P1` is now complete: the canonical registry-lineage verbs are now fixed, and the difference among `split into`, `absorbed into`, `superseded by`, and `retired` is now explicit enough to guide later legacy handling and migration work.
- `P2` is now complete: old areas now have one explicit `frozen legacy area` state, and split areas now stop receiving new sequence numbers once narrower current areas take over.
- `P3` is now complete: old records now have one explicit legacy disposition model, and non-active records with current successors now require deterministic reader redirection instead of silent historical drift.
- No migration has been executed yet in this slice.

## Problem Statement

- The registry cannot assume that one area code remains the best long-term grouping forever.
- Later understanding may show that one coarse area should be split into multiple narrower current areas.
- Later understanding may also show that one old record no longer deserves independent active status because its semantics have been absorbed into a newer current record.
- The system therefore needs one explicit model for:
  - how old files survive,
  - how old references remain meaningful,
  - how current-state reading avoids being polluted by historical files in the same folder,
  - and how repeated later splits do not turn the registry into a garbage heap.

## Baseline Questions

- What is the exact difference between `split into`, `absorbed into`, `superseded by`, and `retired` at registry level?
- What status should an old area receive after it is no longer allowed to grow but must still remain historically visible?
- What status or disposition should an old record receive when it is still historically important but no longer participates in current-state interpretation?
- How should `INDEX.md` surface current state only, while still giving readers a deterministic path to legacy files and old references?

## P1 Baseline (Lineage verbs)

### `split into`

- Use `split into` when one prior active area or record is no longer the best current grouping because its semantics are now better represented by multiple narrower current descendants.
- The old item does not become meaningless. It becomes a historical umbrella that has been decomposed.
- A `split into` result therefore implies:
  - more than one current descendant
  - the old item should stop receiving new sequence numbers or new active interpretation
  - readers should be redirected from the old umbrella to the newer narrower descendants

### `absorbed into`

- Use `absorbed into` when one prior item no longer deserves independent active interpretation because its semantics are now fully carried inside one newer current item.
- The key point is not replacement-by-version. The key point is loss of independent active standing.
- An `absorbed into` result therefore implies:
  - one primary current destination
  - the old item remains historically traceable
  - the old item should no longer be read as a parallel active rule beside the absorbing item

### `superseded by`

- Use `superseded by` when one newer record becomes the current effective version for the same governed surface, replacing the older record as the active explanation surface.
- This is the closest lineage verb to an ordinary version upgrade.
- A `superseded by` result therefore implies:
  - one successor remains the current effective rule for the overlapping surface
  - the older record is historical and should normally not remain active for that same surface
  - the relationship is primarily versional, not decompositional

### `retired`

- Use `retired` when a prior area or record no longer remains active and no current descendant needs to carry its meaning forward as a live rule.
- Retirement may happen because the governed behavior disappeared, the rule became irrelevant, or the repo no longer needs to represent that contract as a current surface.
- A `retired` result therefore implies:
  - no active successor is required
  - the old item remains historical only
  - readers should not expect a current replacement unless one is stated explicitly elsewhere

## P1 Distinction Rules

- `split into`:
  - one old thing becomes multiple narrower current things
- `absorbed into`:
  - one old thing loses independent standing because one newer current thing fully carries it
- `superseded by`:
  - one old thing is replaced by one newer current version for the same surface
- `retired`:
  - one old thing ends without requiring a current active successor

- The registry should not use these verbs interchangeably.
- In particular:
  - do not use `superseded by` when the real situation is decomposition into multiple descendants
  - do not use `absorbed into` when the real situation is version replacement of the same surface
  - do not use `retired` as a vague synonym for any non-current state when a more specific lineage verb is actually known

## P2 Baseline (Frozen legacy areas)

### `frozen legacy area`

- Use `frozen legacy area` when an older area code must remain historically visible but is no longer allowed to act as a growing current namespace.
- A frozen legacy area is not deleted.
- A frozen legacy area is also not current-growth-eligible.
- This state exists specifically to solve the case where an older coarse area has been split into narrower current areas, but the old files and old references must still survive.

### Trigger Rule

- An area should enter `frozen legacy` when all of the following are true:
  - the old area is no longer the preferred current grouping for new contract admission
  - one or more newer current areas now carry the active interpretation that the old area used to group
  - the repo still needs the old area code and old files for historical traceability or reference preservation
- The most common trigger is `split into`, but a similar freeze may also happen after a large migration that leaves the old area historically important but no longer current.

### Sequence-Stop Rule

- Once an area becomes `frozen legacy`, that area stops receiving new sequence numbers.
- In practical terms:
  - no new `GC-<OLDAREA>-000N` records should be created under that old area after freeze
  - all new current records must land under the newer current areas instead
  - the old area's existing sequence remains as a closed historical namespace rather than an open active line
- This rule exists to prevent dual-track drift where the repo continues to grow both the old coarse area and the newer narrower areas at the same time.

### Allowed Actions After Freeze

- After an area is frozen, the repo may still:
  - preserve the old files in place
  - add lineage notes or redirection notes to old files
  - cite old record IDs in migration notes, traceability notes, or historical references
  - index the frozen area in a future historical or legacy view if one is introduced
- After an area is frozen, the repo should not:
  - admit new active records into that area
  - keep treating the old area as the preferred current registry grouping in `INDEX.md`
  - reopen the old area for growth just because one later edge case appears easier to file there

### P2 Consequences

- Future splits can preserve old area files without letting old area namespaces continue to compete with current ones.
- Old references remain valid because the old files still exist.
- Current-state readability improves because area growth now has one explicit stop rule instead of silent namespace drift.
- Later `P3` and `P4` can build on this rule by deciding how frozen areas and frozen records should be surfaced outside the current front-door index.

## P3 Baseline (Legacy records and references)

### Legacy Record Disposition Model

- `active`:
  - use when the record is still part of current-state interpretation
  - an `active` record should not behave like a redirect shell
- `deprecated`:
  - use when the old record must remain stored and citable, but should no longer be read as an independently active rule because its meaning has been absorbed into one newer current record or decomposed across multiple newer current records
  - this is the default legacy disposition for `absorbed into` and `split into`
- `superseded`:
  - use when one newer record replaces the older record as the current effective rule for the same governed surface
  - this remains the right status for one-to-one versional replacement
- `retired`:
  - use when the old record remains historical only and no current successor needs to carry its meaning forward

### Disposition Rules

- Do not force every old record into `superseded`.
- Use `deprecated` when the old record still exists mainly to preserve traceability while readers should now interpret one or more different current records instead.
- In particular:
  - `absorbed into` normally yields `deprecated`, not `superseded`, because the old record lost independent standing rather than being replaced by a same-surface version
  - `split into` normally yields `deprecated`, not `superseded`, because multiple current descendants now carry the old meaning
  - `superseded` should stay reserved for one older record replaced by one newer current record for the same surface
  - `retired` should stay reserved for historical-only records with no required current destination

### Old-Record Redirection Rule

- Any stored non-active record that still has one or more current successors should contain one deterministic reader-facing redirect near the top of the file.
- That redirect should answer three questions immediately:
  - what this old record's current standing is
  - which lineage verb explains why it is no longer current
  - where the reader should go now for current interpretation
- The old file remains the stable home for old IDs and old references.
- The redirect exists so readers do not need to infer current meaning from filename age, folder order, or surrounding historical notes.

### Redirect Shape by Lineage

- For `absorbed into`:
  - point to one primary current record
  - state that the old record remains historical and no longer stands independently beside the absorbing record
- For `split into`:
  - list all current descendant records that now carry the narrower live meaning
  - state that the old record remains a historical umbrella only
- For `superseded by`:
  - point to the one successor record
  - keep record-level `superseded_by` aligned with that successor
- For `retired`:
  - state explicitly that no current successor is required
  - do not invent a redirect target just to avoid an empty destination

### P3 Consequences

- Old record IDs remain resolvable because their files stay in place.
- Current readers no longer need to guess whether a historical file is still active.
- Split and absorption cases no longer have to misuse `superseded_by` just to express that newer current records exist.
- Later migration work can update coarse historical records without deleting them and without leaving their current meaning ambiguous.

## Plan (draft)

### P0 (Slice opening and problem boundary)

- P0-C1-S1: create `S0F-3E` and wire it into the `S0F` parent spine
- P0-C1-S2: define the registry-lineage and legacy-handling problem as distinct from ordinary record admission

### P1 (Lineage verbs)

- P1-C1-S1: define `split into` as one current-to-legacy transition that yields multiple narrower active descendants
- P1-C1-S2: define `absorbed into` as one current-to-legacy transition where the old record no longer stands independently because its semantics now live inside a newer current record
- P1-C1-S3: define how these verbs differ from `superseded by` and `retired`

### P2 (Frozen legacy areas)

- P2-C1-S1: define the `frozen legacy area` rule
- P2-C1-S2: define how old area codes stop receiving new sequence numbers after a split

### P3 (Legacy records and references)

- P3-C1-S1: define one legacy disposition model for old records that remain stored but no longer act as current active records
- P3-C1-S2: define how old record files should point readers toward newer active records after split or absorption

### P4 (Current versus historical surfaces)

- P4-C1-S1: define how `INDEX.md` remains current-state only
- P4-C1-S2: define how historical files remain discoverable without turning folder scans into current-state interpretation

### P5 (Migration package)

- P5-C1-S1: define the first bounded migration package that can later apply these rules to coarse areas already landed in the registry
- P5-C1-S2: define how that package should preserve old IDs, old file paths, and old references while still cleaning up the current-state view

## Execution Checklist (unchecked)

### P0 (Slice opening and problem boundary)

- [x] `P0-C1-S1`: `S0F-3E` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: registry-lineage and legacy-handling boundary fixed

### P1 (Lineage verbs)

- [x] `P1-C1-S1`: `split into` defined at registry level
- [x] `P1-C1-S2`: `absorbed into` defined at registry level
- [x] `P1-C1-S3`: distinction from `superseded by` and `retired` fixed

### P2 (Frozen legacy areas)

- [x] `P2-C1-S1`: `frozen legacy area` rule fixed
- [x] `P2-C1-S2`: old-area sequence-stop rule fixed

### P3 (Legacy records and references)

- [x] `P3-C1-S1`: legacy record disposition model fixed
- [x] `P3-C1-S2`: old-record redirection rule fixed

### P4 (Current versus historical surfaces)

- [ ] `P4-C1-S1`: `INDEX.md` current-only rule fixed
- [ ] `P4-C1-S2`: historical discoverability rule fixed

### P5 (Migration package)

- [ ] `P5-C1-S1`: first bounded migration package defined
- [ ] `P5-C1-S2`: old ID and old reference preservation rule fixed