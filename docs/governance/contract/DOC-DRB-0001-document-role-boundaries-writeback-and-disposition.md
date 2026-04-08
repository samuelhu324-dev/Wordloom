# doc-contract-record: DOC-DRB-0001

- `record_id`: `DOC-DRB-0001`
- `contract_id`: `DOCUMENT-ROLE-BOUNDARIES-WRITEBACK-AND-DISPOSITION`
- `title`: `document role boundaries, write-back order, and disposition separation stay explicit across current DOC governance surfaces`

```yaml
doc_contract:
  record_id: DOC-DRB-0001
  contract_id: DOCUMENT-ROLE-BOUNDARIES-WRITEBACK-AND-DISPOSITION
  family: DOC
  area: DRB
  status: draft
  summary: Current documentation-governance surfaces must keep outlet role ownership explicit, export stable rule and procedure material out of source-owner logs in one fixed order, and treat disposition or placement as downstream state rather than as a peer document type.
  primary_source_owner: docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md
  applies_to: documentation-governance source-owner logs, promoted DOC contracts, stable runbooks, bounded views, directory front doors, and later placement decisions derived from the same close-out package
  enforcement_surface: source-owner log close-out review and family-owned contract landing decisions
  violation_semantics: warning
  introduced_by: S0F-4A/P1-P4
  last_changed_by: S0F-4E/P1-C1-S1S2
  source_refs:
    - docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md
    - docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md
  supersedes: []
  superseded_by: []
  notes:
    - This file is the first family-owned DOC contract body promoted out of its source-owner log.
    - S0F-4A remains the source-owner SoT while this record is still draft and before later close-out review completes under S0F-5A.
    - Later family-specific placement decisions may refine concrete paths without changing the role-boundary rule concentrated here.
```

## Current Rule

- Documentation-governance work must keep six outlet responsibilities explicit:
  - `log`
  - `contract`
  - `runbook`
  - `view`
  - `index/front-door`
  - `disposition/placement`
- A source-owner log may temporarily hold more than one responsibility while a lane is still forming, but it should not remain the long-term primary home for stable current rule text, stable operator procedure, or current front-door navigation once those outlet identities are explicit.
- Role identity and disposition state are separate axes:
  - role answers what the file is for
  - disposition answers the current standing or placement of that role-owned file

## Outlet Responsibilities

### `log`

- Owns slice-local decision history, execution boundary, checklist state, evidence, and bridge notes.
- Retains why the work happened and what remains slice-local after exports.
- Should not remain the durable reader home for stable current rule text or stable operator procedure when those surfaces have a clear current outlet.

### `contract`

- Owns stable current rule meaning, scope boundary, enforcement surface, and violation semantics.
- Retains minimum current traceability and successor lineage notes only.
- Should not expand into operator procedure or whole-family chronology.

### `runbook`

- Owns stable operator-facing procedure, required inputs, produced outputs, and troubleshooting path.
- Explains how to run the governed surface now.
- Should not redefine current semantic rule ownership.

### `view`

- Owns bounded reader-facing interpretation when a family, package, or transition needs one concentrated summary.
- May explain current versus legacy versus support-only reading boundaries.
- Should not become a second current rule surface.

### `index/front-door`

- Owns current navigation and directory entry boundaries only.
- May expose the current reading path for a directory or contract family.
- Should not absorb full chronology or export ledger detail.

### `disposition/placement`

- Owns standing and physical placement decisions for already-adjudicated files.
- Tracks states such as `keep current`, `keep legacy`, `support-only`, `deprecated`, `superseded`, `retired`, and `defer cleanup`.
- Must remain downstream of role separation rather than acting as a substitute role type.

## Close-Out Protocol

### Mandatory Questions

- Did the slice define or materially change one current rule?
- Did the slice define one stable operator procedure?
- Did the slice produce one reusable family or reader summary?
- Did the slice change any current front-door or local entry reading?
- Did the slice change any file disposition or placement state?
- What must remain in the log because it is still slice-local evidence, traceability, or bridge context only?

### Required Write Order

1. Update or create `contract` when stable current rule changed.
2. Update or create `runbook` when stable procedure changed.
3. Update `index/front-door` when current navigation changed.
4. Update or create `view` when one bounded reader summary is worth retaining.
5. Rewrite the `log` so it keeps only slice-local ledger, evidence, and bridge notes for exported material.
6. Record `disposition/placement` change only after the other outlets are explicit enough that cleanup is not guessing at meaning.

### Stop Rule

- Do not export content mechanically when the supposed target outlet still lacks a stable identity.
- In that case the source-owner log remains the temporary home until a later bounded slice fixes the missing target outlet.
- A valid close-out result may therefore include `no new runbook` or `no new view` when the operator or reader surface is not actually stable or necessary.

## Disposition And Placement Rules

- Disposition is not a peer to `contract`, `runbook`, `view`, or `log`; it is a downstream state applied after role ownership is clear.
- Physical placement follows role first and disposition second.
- Current family-owned `DOC` contracts land under `docs/governance/contract/`.
- Current `DOC` and governance reader summaries land under `docs/governance/views/`.
- Stable operator procedures land under `docs/runbook/`.
- Source-owner and execution ledgers remain under `docs/logs/` until later close-out or cleanup changes that standing explicitly.
- Support-only relocation is allowed only after discoverability, lineage, and role separation are already defended.

## Externalization Boundary

- Current contracts, current runbooks, current views, and parent or source-owner logs should remain readable in-repo.
- Future external object storage may hold heavy retained evidence bundles, large historical artifacts, or reproducible exported drill outputs.
- Any later externalization must keep one in-repo manifest or traceability surface so current reading never depends on mutable bucket listing.
- Do not create a repo-wide `archive/` placeholder merely to simulate future object storage.

## Reader Notes

- This file is the first draft of the family-owned current contract body mapped from `S0F-4A`.
- While this record remains `draft`, `S0F-4A` continues to own the strongest current source traceability for this rule set.
- Later `S0F-4E` phases should align this record with the `DOC` contract index, any necessary front doors, and the stable-first close-out questionnaire defined by `S0F-5A`.

## Traceability

- Source-owner log:
  - `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
- Promotion lane:
  - `docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md`