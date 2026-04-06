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

- [ ] `P2-C1-S1`: `frozen legacy area` rule fixed
- [ ] `P2-C1-S2`: old-area sequence-stop rule fixed

### P3 (Legacy records and references)

- [ ] `P3-C1-S1`: legacy record disposition model fixed
- [ ] `P3-C1-S2`: old-record redirection rule fixed

### P4 (Current versus historical surfaces)

- [ ] `P4-C1-S1`: `INDEX.md` current-only rule fixed
- [ ] `P4-C1-S2`: historical discoverability rule fixed

### P5 (Migration package)

- [ ] `P5-C1-S1`: first bounded migration package defined
- [ ] `P5-C1-S2`: old ID and old reference preservation rule fixed