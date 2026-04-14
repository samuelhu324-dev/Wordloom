# Governance Index

## Purpose

- This file is the narrow front-door registry for governance contracts that currently remain admitted inside the governance-registry model.
- It exists so readers do not need to scan long filenames or reconstruct current governance state from raw folder listings alone.
- It also acts as the controlled admission surface for new governance area codes and for the minimum registry fields every live record must expose here.
- It is a current-state surface, not a full historical ledger of every governance-contract file preserved on disk.
- Repo-wide cross-family contract scanning now lives separately in `docs/governance/views/view-contract-family-inventory-v1.md`; this file remains the narrow front door for current registry-admitted governance contracts only.
- During the family-first transition, readers should not treat this file as the universal front door for every contract family; where a family front door already exists, read that family surface first and return here only for narrow registry meaning.

## Current-State Boundary

- Read this file as the current governance front door.
- Presence in this file means the record belongs to current-state interpretation at front-door level.
- Absence from this file does not mean an old record file was deleted; historical files may still exist under `docs/governance/contracts/`, including bounded support-only relocations under `docs/governance/contracts/support-only/`.
- When old records remain stored for lineage, redirects, or traceability, they should be discovered through the old file itself, dedicated legacy views under `docs/governance/views/`, or migration logs rather than by widening this file into a mixed current-plus-history index.
- The issue-governance surfaces formerly read here through `GC-ICR-0001`, `GC-ICL-0001`, `GC-ICT-0001`, `GC-IID-0001`, and `GC-IID-0002` now read first through the `DOC` family front door and the corresponding `DOC-*` family-owned current bodies.

## Old GC File Retention Rule

- Old `GC-*` files under `docs/governance/contracts/` should be read in three buckets:
  - `current narrow-registry`: current rows still admitted in this file
  - `legacy redirect`: old record IDs or split-package files preserved so readers can land on the old path and then follow the current successor
  - `support-only history or backtrace`: historical files kept only for bounded backtrace or cleanup evidence after current reading and redirect value have already moved elsewhere
- Practical retention rule:
  - `current narrow-registry` stays readable in `docs/governance/contracts/` root
  - `legacy redirect` also stays readable in `docs/governance/contracts/` root because its primary value is stable old-path discoverability
  - only `support-only history or backtrace` is a default candidate for later relocation into `docs/governance/contracts/support-only/`
- This means the contracts root is intentionally mixed between current registry rows and preserved redirect files during transition; that coexistence is not by itself a cleanup bug.

## Registry Model

- `record_id`:
  - short registry and file-system identifier
  - example: `GC-PRB-0001`
- `contract_id`:
  - semantic governance-contract identifier
  - example: `PR-BODY-HISTORICAL-DRIFT-FAIL-ON-FINDINGS`
- `title`:
  - short human-readable title for scanning
- `area`:
  - governance area grouping such as `pr-body-review`
- `status`:
  - current state such as `draft`, `active`, `deprecated`, `superseded`, or `retired`
- `violation_semantics`:
  - current result such as `fail`, `warning`, `report-only`, or `neutral`

## Abbreviation Glossary

- `GC`:
  - `Governance Contract` legacy registry prefix
  - used as the stable stored prefix for governance-registry records
  - not the umbrella name for the whole contract universe once family-first reading exists
- `COMPL`:
  - `Completeness`
  - used for lifecycle completeness audit contracts that classify create-time, PR-time, and conclusion-time completeness as distinct governance surfaces
- `ATTR`:
  - `Attribution`
  - used for source-log attribution and provenance resolution surfaces such as ordered ownership precedence, fail-closed ambiguity policy, and explicit consume-or-stop handoff before downstream verification
- `ICL`:
  - `Issue Conclusion`
  - used for issue-conclusion governance such as post-merge conclusion timing and exact delivery-PR linkage
- `ICR`:
  - `Issue Creation`
  - used for issue-creation governance such as deterministic creation metadata and English-only scaffold boundaries
- `ICT`:
  - `Issue Context`
  - used for issue-Context governance such as sentence count, one-sentence-per-line shape, and source-log-derived anchors
- `IID`:
  - `Issue Identity`
  - used for issue identity governance such as parent sidebar ordering ownership and controlled title keyword vocabulary
- `PRA`:
  - `PR Automation`
  - used for PR-creation governance such as exact ID-scoped commit selection, metadata precedence, and bounded create-time stage ownership
- `PRG`:
  - `PR Gate`
  - used for current gate semantics that turn reviewer findings into pass or non-pass standard-check outcomes
- `PRR`:
  - `PR Review`
  - used for reviewer-owned PR body completeness classification and canonical drift interpretation
- `REMED`:
  - `Remediation`
  - used for multi-item remediation governance such as preview-first batch staging, family-owned guarded apply delegation, split-before-mutation, and mandatory preserve-existing post-verify
- `WF`:
  - `Workflow Failure Handling`
  - used for publish-verify-remediation failure taxonomy, ordered replay/backfill handling, and explicit block/replayable/manual/reconciliation workflow semantics

## Controlled Area-Code Dictionary

- New area codes are not free-form.
- A new area code is admitted only when all of the following are true:
  - the code is added to this glossary before the first live registry record uses it
  - the code is short, uppercase, and stable enough for long-term reuse
  - the code names one governance area, not one temporary implementation detail, branch name, or one-off fix
  - the code is not reused retroactively for a different governance surface
- Current admitted area codes:
  - `ATTR`: source-log attribution and provenance resolution governance
  - `COMPL`: lifecycle completeness audit governance
  - `ICL`: issue conclusion governance
  - `ICR`: issue creation governance
  - `ICT`: issue Context governance
  - `IID`: issue identity governance
  - `PRA`: PR creation and PR automation governance
  - `PRG`: PR body standard-check gate governance
  - `PRR`: PR body reviewer and review-classification governance
  - `REMED`: multi-item remediation stage governance
  - `WF`: workflow failure handling governance

## Filename Model

- `record_id` is the short registry/file-system identifier.
- The baseline governance-contract filename model is:
  - `GC-<AREA>-<NNNN>-<summary>.md`
- Example:
  - `GC-PRB-0001-historical-drift-fail-on-findings.md`
- Under this model:
  - `GC` identifies the record family as a governance-contract registry item
  - `PRB` identifies the governance area
  - `0001` identifies the record sequence inside that area
  - `<summary>` keeps the filename human-scannable without forcing the long semantic `contract_id` to carry the whole file-system burden

## Sequence Rule

- `0001`, `0002`, `0003`, and later numbers are sequence numbers inside one governance area code.
- The number answers: which registry entry this is within that area.
- The number does not by itself prove whether the later entry is:
  - a new independent rule,
  - a refinement of an earlier rule,
  - or a replacement for an earlier rule.
- That distinction should be expressed through the record body and index columns such as `supersedes`, `superseded_by`, and `notes`.

## Required Index Columns

- Every area table in this file should expose the same minimum column set:
  - `record_id`
  - `contract_id`
  - `title`
  - `status`
  - `violation_semantics`
  - `relation`
  - `what it currently solves`
  - `record`
- These columns are mandatory because they answer the minimum front-door questions:
  - what this record is
  - whether it is current
  - how it behaves on violation
  - whether it stands alone, refines another record, or replaces another record
  - where the active file lives

## Sort Rule

- Area sections should be ordered by area code.
- Records inside one area should be ordered by numeric sequence ascending: `0001`, `0002`, `0003`, and so on.
- Do not reorder rows to tell a story or to keep the newest semantic change at the top.
- If a reader needs semantic interpretation beyond scan order, that meaning should come from `status`, `relation`, and the contract record body rather than from manual row reshuffling.

## Relationship Rule

- `relation` tells the reader how this record relates to earlier records in the same area.
- Use one of these baseline readings:
  - `independent`: a distinct contract with no direct replacement relationship to an earlier record
  - `refines <record_id>`: narrows, clarifies, or layers onto an earlier record without automatically retiring it
  - `supersedes <record_id>`: replaces the earlier record for the overlapping governed scope
- Refinement and supersede should be read differently:
  - refinement means the earlier record can remain semantically active unless an explicit later record retires or supersedes it
  - supersede means the earlier record is no longer the current effective rule for the overlapping scope and should be reflected in both index relations and record-level `supersedes` or `superseded_by` fields

## Area Grouping

### Attribution (`ATTR`)

| record_id | contract_id | title | status | violation_semantics | relation | what it currently solves | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GC-ATTR-0001` | `PR-EVENT-SOURCE-LOG-ATTRIBUTION-PRECEDENCE` | PR-event source-log attribution resolves through ordered precedence, fail-closed ambiguity policy, and explicit consume-or-stop handoff | `active` | `fail` | `independent` | Concentrates source-log attribution ownership, ambiguity-stop handling, and downstream consume-or-stop gating without turning later implementation or workflow wiring into separate current records | `docs/governance/contracts/GC-ATTR-0001-pr-event-source-log-attribution-precedence.md` |

### Completeness Audit (`COMPL`)

| record_id | contract_id | title | status | violation_semantics | relation | what it currently solves | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GC-COMPL-0001` | `LIFECYCLE-THREE-STAGE-COMPLETENESS-AUDIT` | Lifecycle completeness is audited separately at creation, PR, and conclusion stages | `active` | `fail` | `independent` | Makes lifecycle completeness a stage-owned audit surface instead of one final-state-only review | `docs/governance/contracts/GC-COMPL-0001-lifecycle-three-stage-completeness-audit.md` |

### PR Automation (`PRA`)

| record_id | contract_id | title | status | violation_semantics | relation | what it currently solves | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GC-PRA-0001` | `PR-CREATION-ID-SCOPED-COMMIT-SELECTION` | PR creation uses exact ID-scoped commit selection and explicit metadata precedence | `active` | `fail` | `independent` | Concentrates the PR-create boundary around exact scope selection, explicit metadata precedence, and bounded create-time staging | `docs/governance/contracts/GC-PRA-0001-pr-creation-id-scoped-commit-selection.md` |

### PR Gate (`PRG`)

| record_id | contract_id | title | status | violation_semantics | relation | what it currently solves | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GC-PRG-0001` | `PR-BODY-STANDARD-CHECK-FAIL-ON-SUBSTANTIVE-DRIFT` | Standard PR body check stays non-pass when reviewer findings include substantive drift | `active` | `fail` | `independent` | Separates the gate decision from reviewer classification so local and CI standard checks stay fail-closed on substantive PR body drift | `docs/governance/contracts/GC-PRG-0001-pr-body-standard-check-fail-on-substantive-drift.md` |

### PR Review (`PRR`)

| record_id | contract_id | title | status | violation_semantics | relation | what it currently solves | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GC-PRR-0001` | `PR-BODY-CANONICAL-REVIEW-CLASSIFICATION` | PR body reviewer classifies exact match, formatting-only drift, and substantive drift against canonical expectations | `active` | `report-only` | `independent` | Separates read-only PR body review classification from downstream gate behavior and historical rewrite actions | `docs/governance/contracts/GC-PRR-0001-pr-body-canonical-review-classification.md` |

### Remediation (`REMED`)

| record_id | contract_id | title | status | violation_semantics | relation | what it currently solves | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GC-REMED-0001` | `GUARDED-BATCH-MULTI-ITEM-REMEDIATION-STAGES` | Multi-item remediation keeps preview planning, guarded apply, and preserve-existing post-verify as separate fail-closed stages | `active` | `fail` | `independent` | Concentrates the current remediation-stage boundary so multi-item repair stays preview-first, family-owned at apply time, and split before mixed-family mutation | `docs/governance/contracts/GC-REMED-0001-guarded-batch-multi-item-remediation-stages.md` |

### Workflow Failure Handling (`WF`)

| record_id | contract_id | title | status | violation_semantics | relation | what it currently solves | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GC-WF-0001` | `PUBLISH-VERIFY-REMEDIATION-FAILURE-TAXONOMY-AND-HANDLING` | Publish-verify-remediation failures stay split into strong-versus-weak structure families with explicit handling semantics | `active` | `fail` | `independent` | Concentrates workflow failure taxonomy, ordered replay/backfill, and explicit block/replayable/manual/reconciliation handling without turning thin-gate or wrapper packaging into separate current records | `docs/governance/contracts/GC-WF-0001-publish-verify-remediation-failure-taxonomy-and-handling.md` |

## Reader Notes

- Start here before opening individual governance-contract files.
- Use `record_id` to scan the registry quickly.
- Use `contract_id` to understand semantic identity.
- Use the `relation` column first to tell whether `0001`, `0002`, or later entries are independent, refinements, or replacements.
- Use the `what it currently solves` column to understand the current problem boundary solved by that record.
- Do not treat a raw folder scan of `docs/governance/contracts/` as the current registry; that folder may contain preserved historical files as well as current ones.
- When historical lineage matters, follow the record-local redirect notes, migration logs, or dedicated governance views rather than expecting this file to duplicate the full archive.
- When deciding whether an old root-level `GC-*` file should still remain in place, use `docs/governance/views/view-gc-triage-and-retention-rule-v1.md` instead of guessing from filename age alone.