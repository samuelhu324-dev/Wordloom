# log-S0F-3B (Phase 3B: governance contract registry and naming model)

---

**id**: `S0F-3B`
**kind**: `log`
**title**: `governance contract registry and naming model v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Governance, Contract, Index, Naming, epic/s0, sub/3b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-3A-governance-contract-index-and-delta-model.md`
  **reference_log_1**: `docs/logs/log-S0F-3A-governance-contract-index-and-delta-model.md`
  **reference_log_2**: `docs/governance/INDEX.md`
  **reference_log_3**: `docs/governance/contracts/GC-PRB-0001-historical-drift-fail-on-findings.md`
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

- `S0F-3B` opens the next `S0F` follow-up slice for governance-contract registry ergonomics: the repo now needs one front-door index plus one short, stable file-naming model so contract concentration does not collapse under long filenames and unscannable contract lists.
- v1 adopts a dual-identifier model:
  - `record_id` for registry/file-system scanning
  - `contract_id` for semantic contract identity
- v1 adopts the baseline record filename convention `GC-<AREA>-<NNNN>-<summary>.md`, where `GC` means governance contract, `<AREA>` is a short governance area code such as `PRB`, and `<NNNN>` is the sequence number inside that area.
- `P5` tightens the registry into a controlled front door instead of a loose listing surface:
  - area codes now require one explicit controlled-vocabulary admission rule
  - the index now has one required column set and deterministic sort rule
  - refinement versus supersede reading rules are now explicit enough that later entries can be interpreted without guesswork

**Default choices (phase defaults / v1)**:

- `docs/governance/INDEX.md` becomes the front-door registry surface for active governance contracts, abbreviations, and area grouping.
- Contract files should optimize for scanability first and full semantic identity second:
  - short `record_id` in the filename
  - long `contract_id` inside the file body
- Sequence numbers such as `0001`, `0002`, `0003` should describe registry order inside one area, not claim that later numbers are always semantically larger or globally newer than all earlier contracts in all areas.
- The registry must explain abbreviations explicitly. Readers should not need tribal knowledge to decode `GC`, `PRB`, or similar short codes.
- New area codes must be declared in the front-door glossary before the first live contract record uses them.
- The index should sort for deterministic scanability rather than storytelling: by area code first, then by numeric sequence within each area.
- Refinement and supersede are not interchangeable:
  - refinement keeps the earlier contract semantically current unless the record body says otherwise
  - supersede replaces the earlier contract for the overlapping governed scope and must be visible in both index and record relationships

## Scope

- `P0`: open `S0F-3B`, wire it into the `S0F` spine, and fix the naming/registry boundary
- `P1`: define the front-door governance index structure and abbreviation glossary
- `P2`: define the `record_id` and filename model for governance-contract records
- `P3`: define sequence semantics so `0001`, `0002`, and later entries are readable and traceable
- `P4`: rehome the first real contract sample under the new naming model and index it
- `P5`: tighten registry policy around area-code vocabulary, required index fields, deterministic sorting, and refinement-versus-supersede reading rules

## Current Status

- `S0F-3B` is now opened as the next `S0F` follow-up slice for governance-contract registry and naming ergonomics.
- `P0` is now complete: `S0F-3B` is wired into the `S0F` spine and the boundary is fixed around front-door registry ergonomics rather than around deeper contract semantics already owned by `S0F-3A`.
- `P1` is now complete: `docs/governance/INDEX.md` now exists as the front-door governance registry and glossary surface.
- `P2` is now complete: `record_id` is now fixed as the short registry/file-system identifier, and the baseline filename model is now `GC-<AREA>-<NNNN>-<summary>.md`.
- `P3` is now complete: the index now explains what `0001`, `0002`, and later sequence numbers mean inside one area, and how readers should distinguish registry order from semantic replacement.
- `P4` is now complete: the first real sample has been rehomed under `GC-PRB-0001-<summary>` naming and indexed from the front-door governance registry.
- `P5` is now complete: the front-door registry is now tightened with a controlled area-code admission rule, one required index-column set, one deterministic sort rule, and one explicit refinement-versus-supersede interpretation rule.
- The slice remains `draft` because this is still the first controlled baseline only: broader area-code rollout and additional indexed samples are still future follow-up work.

## Plan (draft)

### P0 (Slice opening and boundary)

- P0-C1-S1: create `S0F-3B` and wire it into the `S0F` parent spine
- P0-C1-S2: fix the boundary around governance-contract registry and naming ergonomics

### P1 (Front-door governance index)

- P1-C1-S1: create `docs/governance/INDEX.md` as the front-door registry surface
- P1-C1-S2: define the glossary for `GC`, area abbreviations, and registry fields

### P2 (Record ID and filename model)

- P2-C1-S1: define `record_id` as the short registry/file-system identifier
- P2-C1-S2: define `GC-<AREA>-<NNNN>-<summary>.md` as the baseline filename model

### P3 (Sequence semantics)

- P3-C1-S1: define what `0001`, `0002`, and later numbers mean within one governance area
- P3-C1-S2: define how readers can tell whether a later entry is a new rule, a refinement, or a replacement

### P4 (Sample rehoming)

- P4-C1-S1: rehome the first real sample under the new filename model
- P4-C1-S2: index that sample in the front-door governance registry

### P5 (Registry tightening)

- P5-C1-S1: define one controlled-vocabulary admission rule for new area codes
- P5-C1-S2: define one required index-column set and deterministic sorting rule
- P5-C1-S3: define one explicit refinement-versus-supersede reading rule for later records

## Execution Checklist (unchecked)

### P0 (Slice opening and boundary)

- [x] `P0-C1-S1`: `S0F-3B` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: governance-contract registry and naming boundary fixed

### P1 (Front-door governance index)

- [x] `P1-C1-S1`: `docs/governance/INDEX.md` created as the front-door registry surface
- [x] `P1-C1-S2`: glossary for abbreviations and registry fields fixed

### P2 (Record ID and filename model)

- [x] `P2-C1-S1`: `record_id` fixed as the short registry/file-system identifier
- [x] `P2-C1-S2`: baseline filename model fixed

### P3 (Sequence semantics)

- [x] `P3-C1-S1`: sequence meaning fixed within one governance area
- [x] `P3-C1-S2`: refinement versus replacement reading rule fixed

### P4 (Sample rehoming)

- [x] `P4-C1-S1`: first real contract sample rehomed under the new filename model
- [x] `P4-C1-S2`: first real contract sample indexed from the front-door registry

### P5 (Registry tightening)

- [x] `P5-C1-S1`: controlled-vocabulary admission rule fixed for new area codes
- [x] `P5-C1-S2`: required index-column set and deterministic sorting rule fixed
- [x] `P5-C1-S3`: refinement versus supersede reading rule fixed