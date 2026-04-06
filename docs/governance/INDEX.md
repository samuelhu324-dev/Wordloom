# Governance Index

## Purpose

- This file is the front-door registry for governance contracts.
- It exists so readers do not need to scan long filenames or reconstruct current governance state from raw folder listings alone.
- It also acts as the controlled admission surface for new governance area codes and for the minimum registry fields every live record must expose here.

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
  - `Governance Contract`
  - used as the stable front prefix for governance-contract registry records
- `PRB`:
  - `PR Body`
  - used for governance contracts primarily about PR body completeness review, drift semantics, rewrite, or packaging surfaces

## Controlled Area-Code Dictionary

- New area codes are not free-form.
- A new area code is admitted only when all of the following are true:
  - the code is added to this glossary before the first live registry record uses it
  - the code is short, uppercase, and stable enough for long-term reuse
  - the code names one governance area, not one temporary implementation detail, branch name, or one-off fix
  - the code is not reused retroactively for a different governance surface
- Current admitted area codes:
  - `PRB`: PR body completeness review and closely related PR-body governance surfaces

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

### PR Body Review (`PRB`)

| record_id | contract_id | title | status | violation_semantics | relation | what it currently solves | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GC-PRB-0001` | `PR-BODY-HISTORICAL-DRIFT-FAIL-ON-FINDINGS` | Historical merged PR substantive drift still fails the standard check | `active` | `fail` | `independent` | Makes the current non-pass behavior explicit when historical merged PRs remain substantive drift inside the review-owned set | `docs/governance/contracts/GC-PRB-0001-historical-drift-fail-on-findings.md` |

## Reader Notes

- Start here before opening individual governance-contract files.
- Use `record_id` to scan the registry quickly.
- Use `contract_id` to understand semantic identity.
- Use the `relation` column first to tell whether `0001`, `0002`, or later entries are independent, refinements, or replacements.
- Use the `what it currently solves` column to understand the current problem boundary solved by that record.