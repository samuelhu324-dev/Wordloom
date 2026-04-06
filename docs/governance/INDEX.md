# Governance Index

## Purpose

- This file is the front-door registry for governance contracts.
- It exists so readers do not need to scan long filenames or reconstruct current governance state from raw folder listings alone.

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
- Future area codes should stay short, stable, and explicitly documented here before broad reuse.

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