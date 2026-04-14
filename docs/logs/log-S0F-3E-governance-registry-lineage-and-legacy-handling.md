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
- `P6`: execute the first bounded `ISS` split package inside this slice

## Current Status

- `S0F-3E` is now opened as the next `S0F` follow-up slice for governance-registry lineage and legacy handling.
- The immediate motivation is already concrete: the first landing batch under `S0F-3D` proved that coarse areas can carry multiple parallel active contracts, which now raises the need for explicit split and absorption handling before future registry growth continues.
- `P1` is now complete: the canonical registry-lineage verbs are now fixed, and the difference among `split into`, `absorbed into`, `superseded by`, and `retired` is now explicit enough to guide later legacy handling and migration work.
- `P2` is now complete: old areas now have one explicit `frozen legacy area` state, and split areas now stop receiving new sequence numbers once narrower current areas take over.
- `P3` is now complete: old records now have one explicit legacy disposition model, and non-active records with current successors now require deterministic reader redirection instead of silent historical drift.
- `P4` is now complete: `INDEX.md` is now fixed as the current-state-only front door, and historical discoverability is now routed through explicit legacy or view surfaces rather than raw folder scanning.
- `P5` is now complete: the repo now has one first bounded migration package for splitting the coarse `ISS` area into narrower current descendants while preserving old IDs, file paths, and references.
- `P6` is now complete: the first bounded `ISS` split package is now executed, successor current records now live under `ICR`, `ICL`, `ICT`, and `IID`, and old `GC-ISS-*` files now survive as deprecated legacy records with deterministic redirects.
- `P6-C3` is now complete: the old fused `PRB` front-door contract is now split into separate reviewer and gate current records, while `GC-PRB-0001` survives as a deprecated legacy umbrella record.
- The first bounded migration is now executed in this slice.

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

## P4 Baseline (Current versus historical surfaces)

### `INDEX.md` Current-Only Rule

- `docs/governance/INDEX.md` is the current-state front door and should be read as current interpretation only.
- `INDEX.md` should not try to become a complete archive ledger for every historical record that still exists on disk.
- A record belongs in `INDEX.md` only when at least one of the following is true:
  - it is currently `active`
  - it is intentionally shown there to explain a still-current one-to-one replacement relationship that readers must understand at front-door level
- Historical storage and historical discoverability are required, but they are not the primary job of `INDEX.md`.

### Front-Door Exclusion Rule

- `INDEX.md` should not ask readers to infer current meaning from mixed listings of active and historical files.
- In particular, the front door should not become a dump of:
  - frozen legacy areas
  - deprecated records whose current meaning now lives elsewhere
  - retired records that no longer govern a live surface
  - raw folder-presence evidence presented as if it were current-state admission
- If a historical item still matters to current interpretation, that connection should be expressed through redirects, lineage notes, or a dedicated legacy view rather than by diluting the front-door current tables.

### Historical Discoverability Rule

- Historical files must remain discoverable through explicit surfaces, not through reader guesswork.
- The allowed discovery surfaces are:
  - the old record file itself
  - lineage or redirect notes inside that file
  - future legacy-oriented view files under `docs/governance/views/`
  - migration logs and governance follow-up logs that explain how current and historical records relate
- This means the repo may preserve old files in `docs/governance/contracts/` while still teaching readers that folder presence alone does not imply current status.

### Folder-Scan Interpretation Rule

- A raw scan of `docs/governance/contracts/` must be treated as storage inspection, not as front-door interpretation.
- Readers should use `INDEX.md` first for current state.
- Readers should use record-local redirects, future legacy views, or migration logs when they need historical lineage.
- This rule prevents the coexistence of active files and historical files in one folder from being misread as one flat set of equally current contracts.

### P4 Consequences

- Old files can remain in place without forcing `INDEX.md` to mirror the entire archive.
- Current-state scanning becomes more trustworthy because front-door tables no longer need to double as historical storage.
- Historical discoverability remains explicit because old records, redirects, views, and logs now have distinct jobs.
- Later migration work can add legacy views without changing the rule that `INDEX.md` itself stays current-only.

## P5 Baseline (First bounded migration package)

### Package Goal

- The first bounded migration package targets the already-landed coarse `ISS` area only.
- The package exists because `GC-ISS-0001` through `GC-ISS-0005` are all current, but they already fall into multiple narrower governance surfaces that should not keep sharing one growing coarse namespace.
- The package is intentionally bounded: it defines one first practical split without reopening unrelated governance areas.

### Package Name

- `ISS split package v1`

### Target Current Areas

- When this package is executed later, `ISS` should split into these narrower current areas:
  - `ICR`: issue creation governance
  - `ICL`: issue conclusion governance
  - `ICT`: issue Context governance
  - `IID`: issue identity governance
- These area codes are intentionally short, uppercase, and stable enough to replace the coarse `ISS` bucket for future current growth.

### Record Mapping

- The first bounded mapping is:
  - `GC-ISS-0001` -> future `GC-ICR-0001`
  - `GC-ISS-0002` -> future `GC-ICL-0001`
  - `GC-ISS-0003` -> future `GC-ICT-0001`
  - `GC-ISS-0004` -> future `GC-IID-0001`
  - `GC-ISS-0005` -> future `GC-IID-0002`
- This mapping keeps semantic concentration aligned with the existing `governance_area` fields already present inside the landed `ISS` records.
- The package does not require semantic rewrites of the governed rules before the namespace split can happen.

### Migration Rules

- Execute this package only as one bounded batch.
- Do not leave the front door in a hybrid state where both `ISS` and all descendant areas are treated as equally current growth namespaces.
- The package should perform all of the following together:
  - publish the successor current records under `ICR`, `ICL`, `ICT`, and `IID`
  - freeze `ISS` as one legacy area
  - convert the old `GC-ISS-*` records into preserved historical files with deterministic legacy redirects
  - update `INDEX.md` so the current front door points only at the successor current areas

### Preservation Rules

- The package must preserve:
  - old record IDs such as `GC-ISS-0004`
  - old file paths under `docs/governance/contracts/`
  - old links from logs, notes, audits, and historical references
- Old `GC-ISS-*` files should stay in place and become `deprecated` historical records after successor publication.
- Each old `GC-ISS-*` file should gain one `Legacy Redirect` section that points to its successor current record or records.
- The new successor files should keep the same `contract_id` values so semantic identity survives the namespace migration.

### Front-Door Cleanup Rule

- After successor current records exist, `INDEX.md` should stop presenting `ISS` as one current area.
- The front door should instead present the narrower current areas and their successor records.
- Historical discoverability for old `ISS` IDs should live in the preserved files, redirect notes, migration logs, and governance views rather than in one mixed current-plus-legacy `ISS` table.

### P5 Consequences

- The repo now has one concrete example of how to split a coarse active area without deleting its history.
- Later migrations can reuse this package shape instead of improvising per-area exceptions.
- The package keeps old citations stable while making future current growth land in narrower areas.
- `ISS` now serves as the canonical first migration target for proving the lineage and legacy model end to end.

## P6 Execution (ISS split package v1)

### Execution Result

- `ISS split package v1` is now executed inside `S0F-3E` rather than being deferred to a later slice.
- The current front door no longer uses `ISS` as one active growth namespace.
- The successor current areas are now:
  - `ICR`: issue creation governance
  - `ICL`: issue conclusion governance
  - `ICT`: issue Context governance
  - `IID`: issue identity governance
- `ISS` now survives only as a frozen legacy area through preserved old files and migration views.

### Published Successor Records

- The executed successor current records are:
  - `GC-ICR-0001`: `ISSUE-CREATION-METADATA-ENGLISH-BODY`
  - `GC-ICL-0001`: `ISSUE-CONCLUSION-POST-MERGE-LINKAGE`
  - `GC-ICT-0001`: `ISSUE-CONTEXT-SENTENCE-COUNT-MAIN-VS-CHILD`
  - `GC-IID-0001`: `ISSUE-PARENT-SIDEBAR-ORDERING-OWNERSHIP`
  - `GC-IID-0002`: `ISSUE-TITLE-KEYWORD-CONTROLLED-VOCABULARY`

### Legacy Preservation Result

- The old `GC-ISS-*` files remain in place under `docs/governance/contracts/`.
- The old `GC-ISS-*` files now use `deprecated` status rather than `active` status.
- Each old `GC-ISS-*` file now contains one deterministic `Legacy Redirect` section that points readers to the current successor record.
- Old file paths, old record IDs, and old references remain valid.

### Front-Door Result

- `docs/governance/INDEX.md` now exposes the narrower current areas only.
- The front door no longer presents one active `ISS` area table.
- Historical `ISS` discovery now routes through the preserved old files and governance views instead of the current front door.

### P6 Consequences

- The lineage model is now exercised end to end on a real already-landed area, not just on future planning text.
- The repo now has one working example of current-state cleanup without destructive history loss.
- Later area splits can follow the same execution shape with less ambiguity.

### P6-C2 Adjacent Review Result

- `GC-PRA-0001` does not need immediate split or refactor.
  - Reason: exact ID-scoped commit selection, metadata precedence, and stage-aware create-time ownership still read as one coherent PR-creation boundary rather than as parallel current contracts.
  - Consequence: keep `PRA` unchanged for now.
- `GC-PRB-0001` is a real future split candidate, but should not be split in the same move as `ISS`.
  - Reason: the current record still answers one fused current question cleanly: whether historical merged-PR substantive drift remains a fail-on-findings non-pass condition in the live standard check.
  - Future split target: one live-gate contract plus one historical-audit or reporting contract, but only after successor current records are explicitly authored.
  - Consequence: keep `PRB` current-state shape unchanged for now, but treat it as the next likely concentration follow-up.
- `GC-PRB-0001` backfill remains a support-only historical note, not a second current contract surface.
  - Reason: it exists to justify `introduced_by`, `last_changed_by`, and source backtrace for the active record, not to express an additional active rule.
  - Consequence: keep it outside the front door and treat later `PRB` split work as a contract-and-backfill refresh rather than as promotion of the backfill note itself.

### P6-C3 PRB Split Result

- `GC-PRB-0001` no longer remains the front-door current record for PR-body semantics.
- The current active successor contracts are now:
  - `GC-PRR-0001`: reviewer-owned classification of exact match, formatting-only drift, and substantive drift against canonical source-log-derived PR body expectations
  - `GC-PRG-0001`: standard-check gate semantics that remain non-pass when reviewer findings contain substantive drift under `fail_on_findings=true`
- The old `GC-PRB-0001` file remains stored as a deprecated historical umbrella record with deterministic redirects to both successors.
- The `GC-PRB-0001` backfill note remains support-only history and now supports the deprecated umbrella record rather than a current front-door contract.

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

### P6 (Execute first bounded migration package)

- P6-C1-S1: publish successor current records under `ICR`, `ICL`, `ICT`, and `IID`
- P6-C1-S2: convert legacy `GC-ISS-*` records into deprecated redirect files
- P6-C1-S3: update the current front door and migration view after the split executes
- P6-C2-S1: review whether `GC-PRA-0001` still reads cleanly as one concentrated current contract
- P6-C2-S2: review whether `GC-PRB-0001` should split into live-gate and historical-audit successor contracts
- P6-C2-S3: classify the `GC-PRB-0001` backfill note as support-only history rather than a second current contract surface
- P6-C3-S1: publish successor current records for PR-body review classification and PR-body gate semantics
- P6-C3-S2: convert `GC-PRB-0001` into a deprecated legacy umbrella record with redirects
- P6-C3-S3: update the current front door and governance views after the PRB split executes

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

- [x] `P4-C1-S1`: `INDEX.md` current-only rule fixed
- [x] `P4-C1-S2`: historical discoverability rule fixed

### P5 (Migration package)

- [x] `P5-C1-S1`: first bounded migration package defined
- [x] `P5-C1-S2`: old ID and old reference preservation rule fixed

### P6 (Execute first bounded migration package)

- [x] `P6-C1-S1`: successor current records published under `ICR`, `ICL`, `ICT`, and `IID`
- [x] `P6-C1-S2`: legacy `GC-ISS-*` records converted to deprecated redirect files
- [x] `P6-C1-S3`: current front door and migration view updated after split execution
- [x] `P6-C2-S1`: `GC-PRA-0001` reviewed and retained as one concentrated current contract
- [x] `P6-C2-S2`: `GC-PRB-0001` reviewed as a deferred future split candidate rather than immediate split work
- [x] `P6-C2-S3`: `GC-PRB-0001` backfill classified as support-only history, not a second current contract surface
- [x] `P6-C3-S1`: PR-body reviewer and gate successor current records published
- [x] `P6-C3-S2`: `GC-PRB-0001` converted into a deprecated redirect umbrella record
- [x] `P6-C3-S3`: front door and governance view updated after the PRB split execution