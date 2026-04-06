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