# log-S0F-4D (Phase 4D: doc current contract surface and legacy GC triage model)

---

**id**: `S0F-4D`
**kind**: `log`
**title**: `doc current contract surface and legacy GC triage model v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Contract, Taxonomy, epic/s0, sub/4d`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
  **reference_log_1**: `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
  **reference_log_2**: `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
  **reference_log_3**: `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
  **reference_log_4**: `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
  **reference_log_5**: `docs/governance/views/view-doc-current-front-door-v1.md`
  **reference_log_6**: `docs/governance/views/view-gc-dual-reading-transition-v1.md`
  **reference_log_7**: `docs/governance/views/view-disposition-role-in-family-transition-v1.md`
  **reference_log_8**: `docs/governance/INDEX.md`
  **reference_log_9**: `docs/governance/contract/INDEX.md`
  **reference_log_10**: `docs/governance/contract/_template-doc-contract-record.md`
  **reference_log_11**: `docs/governance/views/view-doc-contract-promotion-map-v1.md`
  **reference_log_12**: `docs/governance/views/view-gc-triage-and-retention-rule-v1.md`
  **reference_log_13**: `docs/governance/views/view-gc-first-cleanup-boundary-v1.md`
**issue_keyword**: `taxonomy`
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

- `S0F-4D` opens the next bounded follow-up because `S0F-4C` already separated family, front door, legacy-registry vocabulary, and disposition, but the repo still lacks one explicit answer for where new `DOC` contracts should physically live and how old `GC-*` files should be triaged over time.
- v1 fixes one practical placement decision:
  - new `DOC` current contracts should land first under `docs/governance/contract/`
  - `docs/governance/views/` remains the reader-summary and front-door layer
  - `docs/governance/contracts/` remains the old narrow-registry and legacy-lineage layer during transition
- Under this model, `docs/governance/` remains the overall control-plane container, but it no longer means that every document under it belongs to the same role or standing.

**Default choices (phase defaults / v1)** (optional, but recommended):

- Do not place new `DOC` current contracts directly into `docs/governance/contracts/` by default once `docs/governance/contract/` exists as the new family-owned current contract surface.
- Keep `views` and `contract` separate:
  - `views` explain how to read
  - `contract` stores stable current rule text
- Keep `contracts/` plural as the old narrow-registry and legacy-lineage surface until later cleanup explicitly retires or relocates old files.
- Old `GC-*` files should be triaged into three buckets rather than mass-archived:
  - current narrow-registry
  - legacy redirect
  - support-only history or backtrace
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block because `S0F-4D` fixes the next practical storage and triage model after the family-first reading transition.
- `PR Summary Inputs` remains the automation-facing source block; later file moves or contract extraction work should not reconstruct this storage model from scattered notes.

**PR summary bullets**:

- Fix `docs/governance/contract/` as the new family-owned current contract surface for `DOC`.
- Keep `views/` as the front-door and reader-summary layer, and keep old `contracts/` as narrow-registry and legacy-lineage storage during transition.
- Replace archive-first thinking with a three-way triage model for old `GC-*` files.

**PR checklist source**:

- Default source: reuse this log's execution checklist for any later `DOC` contract extraction or GC triage PR.

**PR links**:

- Log: `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`
- Contract index: `docs/governance/contract/INDEX.md`

## Exported Sections / Outlet Ownership (optional)

- This slice should end in a usable family-owned `DOC` contract home rather than in one more abstract taxonomy note.

**Outlet ownership**:

- `contract`: new `DOC` current contract bodies under `docs/governance/contract/`
- `view`: current `DOC` family front door and reader transition aids under `docs/governance/views/`
- `index/front-door`: local entrypoint under `docs/governance/contract/INDEX.md` plus existing family-front-door views
- `disposition/placement`: standing and relocation decisions for old `GC-*` files
- `log-retained core`: decision, checklist, current status, evidence, and phase sequencing for this placement lane

## Definitions (optional)

- **family-owned current contract**: a stable current contract body that belongs to one family and is not forced into the old registry namespace first
- **narrow registry**: the older concentrated governance-record surface that still exists for admitted registry records and their lineage
- **legacy redirect**: an old file that should stay readable and traceable, but no longer acts as the current primary reading surface
- **support-only history**: a file retained only for bounded historical or backtrace value after the current reader path has already moved elsewhere

## Constraints

- Do not use `docs/governance/contracts/` as the automatic home for every new `DOC` contract now that the family-first transition exists.
- Do not collapse `views/` and `contract/` into one directory.
- Do not archive old `GC-*` files in bulk before they are triaged by current standing.
- Do not treat the existence of both `contract/` and `contracts/` as a bug by itself; the distinction is intentional during transition.

## Scope

- `P0`: fix the practical storage split among `contract/`, `contracts/`, and `views/`
- `P1`: define the first `DOC` current contract surface under `docs/governance/contract/`
- `P2`: define the three-way triage rule for old `GC-*` files
- `P3`: define how future source-owner `DOC` logs promote into the new contract surface
- `P4`: define the first cleanup boundary for old `GC-*` relocation versus retention in place

## Success Criteria (DoD)

- One reader can explain why new `DOC` current contracts should land under `docs/governance/contract/` rather than under old `docs/governance/contracts/` by default.
- One reader can explain why `views/` stays separate from contract bodies.
- One reader can explain the three triage buckets for old `GC-*` files without collapsing them into `archive`.
- The repo has one explicit storage answer for new `DOC` family contracts, one explicit reading answer for `views/`, and one explicit standing answer for old `GC-*` files.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the new `DOC` contract home and old `GC-*` triage model are explicit enough that later extraction work can proceed without reopening the directory question first
  - the repo has at least one usable front door for `docs/governance/contract/`
  - the repo has at least one concrete old-`GC-*` cleanup boundary that shows which already-triaged files stay root-readable and which already belong to support-only

## P0 (Contract | v1)

### P0-C1-S1 (DOC current contract home rule | v1)

- New `DOC` current contracts should now land first under:
  - `docs/governance/contract/`
- This directory is the family-owned current contract surface for `DOC`, not the old registry directory.

### P0-C1-S2 (Old GC triage rule | v1)

- Old `GC-*` files should be triaged into:
  - `current narrow-registry`
  - `legacy redirect`
  - `support-only history or backtrace`
- Only the third bucket should be a default candidate for later relocation into deeper support-only handling.

### P0-C1-S3 (Views coexistence rule | v1)

- `docs/governance/views/` remains the reader-summary, family-front-door, and transition-rule layer.
- It should not be merged into `contract/` because current explanation and current rule body are different responsibilities.

## P1 (DOC current contract surface | v1)

### P1-C1-S1 (DOC contract naming model and template | v1)

- New `DOC` family-owned current contracts now use the filename model:
  - `DOC-<AREA>-<NNNN>-<summary>.md`
- The repo now keeps one dedicated template for this surface at:
  - `docs/governance/contract/_template-doc-contract-record.md`
- New `DOC` contracts should therefore stop defaulting to `GC-*` prefixes and should not use bare area-only identifiers such as `ICR-001-...`.

### P1-C1-S2 (DOC area-code dictionary fixed | v1)

- The first admitted `DOC` area codes are now:
  - `DRB`: document role boundaries
  - `SLC`: source-log compatibility
  - `TAX`: taxonomy and placement
  - `FDT`: front-door transition
- These are now fixed in `docs/governance/contract/INDEX.md` as the first candidate areas for promoted `DOC` current contracts.

## P2 (Old GC triage | v1)

### P2-C1-S1 (Three-bucket interpretation rule fixed | v1)

- Old `GC-*` files must now be interpreted through three practical standing buckets:
  - `current narrow-registry`
  - `legacy redirect`
  - `support-only history or backtrace`
- The bucket is decided by current reader function, not by file age alone.
- `current narrow-registry` means the file is still admitted by `docs/governance/INDEX.md` as a current governance-registry row.
- `legacy redirect` means the old root path still matters because it preserves stable old-ID lineage and redirects readers to a current successor.
- `support-only history or backtrace` means the file remains only for bounded historical explanation or cleanup traceability after current reading and redirect value already moved elsewhere.

### P2-C1-S2 (Relocation-versus-retention rule fixed | v1)

- `current narrow-registry` files remain in `docs/governance/contracts/` root.
- `legacy redirect` files also remain in `docs/governance/contracts/` root because that old root path is part of the redirect contract.
- Only `support-only history or backtrace` is a default candidate for later relocation into `docs/governance/contracts/support-only/`.
- No old `GC-*` file should move to support-only merely because it is deprecated or has a newer successor; relocation begins only after direct references and reader discoverability can survive the move explicitly.

## P4 (Cleanup boundary | v1)

### P4-C1-S1 (First old-GC cleanup boundary fixed | v1)

- The first concrete old-`GC-*` cleanup boundary is now fixed as follows:
  - keep the preserved legacy redirect set at the contracts root:
    - `GC-ISS-0001` through `GC-ISS-0005`
    - `GC-PRB-0001`
  - keep the already-relocated support-only backtrace note in the support-only contracts surface:
    - `GC-PRB-0001-backfill-historical-drift-fail-on-findings.md`
- This means `P4` does not open a new move round.
- It fixes the first stable keep-versus-support-only boundary so later cleanup does not keep reopening the same adjudicated old-file subset.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `<ID>/P0-P3: <log title>`
  - discontinuous phases: `<ID>/P0+P3: <log title>`
  - mixed discontinuous + consecutive phases: `<ID>/P0+P3-P4: <log title>`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title: `<ID>/P*-C*-S*: <one-sentence summary>`.

**Branch convention**:

- For logs tied to a specific scope/index, prefer making P* code and documentation changes on a working branch with the same prefix.
- If a single PR touches multiple scopes/indexes, prefer splitting it into multiple PRs so each PR stays focused on one scope/index and its corresponding branch for easier aggregation and traceability.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, try to `commit/push` promptly on the matching scope branch.
- The normal rhythm is: accumulate commits on the matching scope branch at `P*-C*-S*` granularity, then periodically open a PR from that branch into `main` for human review and merge.

## Plan (draft)

### P1 (DOC current contract surface)

- P1-C1-S1: define the first `docs/governance/contract/INDEX.md` front door
- P1-C1-S2: define how current `DOC` family contracts should land there without reusing `GC-*` as default prefix

### P2 (Old GC triage)

- P2-C1-S1: define the three triage buckets for old `GC-*` files
- P2-C1-S2: define which bucket may later move or archive and which should remain readable in place

### P3 (Promotion path from source-owner logs)

- P3-C1-S1: define how current source-owner `DOC` logs later promote into the new contract surface

### P4 (Cleanup boundary)

- P4-C1-S1: define the first cleanup boundary between keeping old `GC-*` in place and relocating deeper support-only history

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: `DOC` current contract home rule fixed
- [x] `P0-C1-S2`: old `GC-*` triage rule fixed
- [x] `P0-C1-S3`: views coexistence rule fixed

### P1 (DOC current contract surface)

- [x] `P1-C1-S1`: first `docs/governance/contract/INDEX.md` front door defined
- [x] `P1-C1-S2`: new `DOC` contract landing rule defined

### P2 (Old GC triage)

- [x] `P2-C1-S1`: three triage buckets defined for old `GC-*`
- [x] `P2-C1-S2`: relocation-versus-retention boundary fixed for those buckets

### P3 (Promotion path from source-owner logs)

- [x] `P3-C1-S1`: source-owner `DOC` log promotion rule fixed

### P4 (Cleanup boundary)

- [x] `P4-C1-S1`: first cleanup boundary fixed for old `GC-*`

## Current Status (recommended)

- `S0F-4D` is now opened as the next bounded follow-up after `S0F-4C`: the repo already has family-first front doors, but it still needs one explicit storage answer for new `DOC` contracts and one triage answer for old `GC-*` files.
- `P0` is now fixed: new `DOC` contracts should first land under `docs/governance/contract/`, `views/` remains the reader-summary layer, and old `GC-*` files should be triaged before any later archive or relocation decision.
- `P1` is now complete: the repo now has one explicit `DOC` contract naming model, one template, and one first `DOC` area-code dictionary under `docs/governance/contract/`, so future promoted `DOC` contracts no longer need to reuse `GC-*` naming by default.
- `P2` is now complete: the repo now has one explicit practical triage rule for old `GC-*` files, and the retention-versus-relocation boundary is fixed so only `support-only history or backtrace` becomes a later relocation candidate while `current narrow-registry` and `legacy redirect` stay readable in the contracts root.
- `P3` is now complete: the repo now has one explicit source-owner promotion rule and one first mapping set, so future `DOC` contract extraction can follow deterministic targets such as `S0F-4A -> DOC-DRB-0001` and `S0F-3I -> DOC-TAX-0001`.
- `P4` is now complete: the repo now has one first concrete old-`GC-*` cleanup boundary, so the already-adjudicated legacy redirect set no longer re-enters relocation debate and the existing `GC-PRB-0001` backfill note remains the first explicit support-only exception.
- `S0F-4D` is now stable: the new `DOC` contract home, naming model, promotion path, old-`GC-*` triage rule, and first cleanup boundary are explicit enough that later promotion or cleanup work can proceed without reopening the same storage model questions.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.

### P0-C1-S1 through P0-C1-S3 (DOC contract home and old GC triage model fixed | 2026-04-08)

- headSha: `1861d1d0e24e7e276f08a76f7f7e60bd227099f1`
- artifacts: `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
- artifacts: `docs/governance/contract/INDEX.md`
- artifacts: `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - one reader should be able to explain where new `DOC` current contracts should live and why old `GC-*` files should be triaged before any later archive decision
- observed:
  - `S0F-4D` now fixes the first storage and triage boundary, and the new `docs/governance/contract/` directory now has an explicit front door instead of remaining an empty folder

### P1-C1-S1 through P1-C1-S2 (DOC naming model, template, and area dictionary fixed | 2026-04-08)

- headSha: `26b30c0e6a6c87dd2d1062abafcba64260896fb7`
- artifacts: `docs/governance/contract/INDEX.md`
- artifacts: `docs/governance/contract/_template-doc-contract-record.md`
- artifacts: `docs/governance/views/view-doc-current-front-door-v1.md`
- artifacts: `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
- expected:
  - one reader should be able to explain how future `DOC` current contracts are named and why they no longer default to `GC-*`
- observed:
  - the repo now has one explicit `DOC-<AREA>-<NNNN>-<summary>.md` naming model, one first `DOC` area-code dictionary, and one reusable template for future promoted `DOC` contracts

### P2-C1-S1 through P2-C1-S2 (old GC triage and retention rule fixed | 2026-04-08)

- headSha: `0bfee7479fe9c3e57030c78da04ce8df86926c9e`
- artifacts: `docs/governance/views/view-gc-triage-and-retention-rule-v1.md`
- artifacts: `docs/governance/INDEX.md`
- artifacts: `docs/governance/contracts/support-only/INDEX.md`
- artifacts: `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
- expected:
  - one reader should be able to explain why deprecated old `GC-*` files do not automatically move to support-only and why only the support-only bucket becomes a default relocation candidate
- observed:
  - the repo now has one explicit three-bucket triage rule and one practical retention rule that keeps current registry rows and legacy redirects at the root while reserving support-only relocation for bounded backtrace-only files

### P3-C1-S1 (source-owner DOC log promotion rule fixed | 2026-04-08)

- headSha: `195a08c842e96da6483118017a0139deff22460a`
- artifacts: `docs/governance/contract/INDEX.md`
- artifacts: `docs/governance/views/view-doc-contract-promotion-map-v1.md`
- artifacts: `docs/governance/views/view-doc-current-front-door-v1.md`
- artifacts: `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
- expected:
  - one reader should be able to explain how the first promoted `DOC` contracts will map from existing source-owner logs without improvising IDs or reusing `GC-*` naming
- observed:
  - the repo now has one explicit first promotion map from source-owner `DOC` logs to deterministic `DOC-<AREA>-<NNNN>` targets

### P4-C1-S1 (first old-GC cleanup boundary fixed | 2026-04-08)

- headSha: `b0dc43a4d75a50465bc4b98f1b2adbe8c5a6c21b`
- artifacts: `docs/governance/views/view-gc-first-cleanup-boundary-v1.md`
- artifacts: `docs/governance/views/view-gc-triage-and-retention-rule-v1.md`
- artifacts: `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
- expected:
  - one reader should be able to explain which already-triaged old `GC-*` files are now explicitly frozen at the contracts root and which existing file is the first explicit support-only exception
- observed:
  - the repo now has one stable first cleanup boundary: `GC-ISS-*` and `GC-PRB-0001` remain root-readable as preserved legacy redirects, while `GC-PRB-0001-backfill` remains the bounded support-only backtrace exception

## Recent changes (for traceability, optional)

- 2026-04-08: opened `S0F-4D` to fix the new `DOC` current contract home and the old `GC-*` triage model after the family-first transition in `S0F-4C`.
- 2026-04-08: completed `P1` by fixing the `DOC` contract naming model, the first `DOC` area-code dictionary, and one reusable family-owned contract template under `docs/governance/contract/`.
- 2026-04-08: completed `P2` by fixing the practical three-bucket triage rule for old `GC-*` files and by stating that only `support-only history or backtrace` becomes a default relocation candidate while `current narrow-registry` and `legacy redirect` remain root-readable.
- 2026-04-08: completed `P4` by fixing the first concrete old-`GC-*` cleanup boundary, freezing the preserved legacy redirect set at the contracts root, and confirming the existing `GC-PRB-0001` backfill note as the first explicit support-only exception.
- 2026-04-08: completed `P3` by fixing the source-owner `DOC` log promotion rule and the first deterministic promotion map into `DOC-DRB-0001`, `DOC-SLC-0001`, `DOC-TAX-0001`, and `DOC-FDT-0001`.