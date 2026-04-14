# S0F Issue/PR Automation Coverage Inventory v1

## Purpose

- This support-only inventory is the continuously revisable working ledger for `S0F` issue/PR automation coverage review.
- It exists so later `S0F-8B` cycles can update one shared scan surface for coverage gaps, per-series readiness, and rollout notes without rewriting those fast-moving details into the source-owner phase log.

## Scan Scope

- Current scan target: `docs/logs/log-S0F-*.md`
- Scan timestamp: `2026-04-14T06:10:06Z`
- Retained artifact: `artifacts/_tmp_s0f_8b_p1_inventory_scan.json`

## Inventory Model

- Use this inventory when the question is `what is the current issue/PR automation coverage state for existing main S0F logs?`
- This file is allowed to carry:
  - coverage counts
  - per-series grouping
  - baseline-covered rows
  - missing-coverage rows
  - first rollout notes for later `S0F-8B/P2`
- This file must not be treated as the final rollout order, the final commit-readiness verdict, or the replacement for source-owner execution logs.

## Row Contract

| field | job |
| --- | --- |
| `series` | numeric `S0F-*` family or `parent` |
| `row type` | `baseline-covered`, `issue-only`, `missing-series`, or `active-meta-lane` |
| `source rows` | exact `S0F` log ids covered by the row |
| `total rows` | how many main `S0F` logs the row covers |
| `issue coverage` | whether issue linkage is already present |
| `pr coverage` | whether PR linkage is already present |
| `review bucket` | `historical-reviewable`, `active-meta-lane`, or `future-unopened-excluded` |
| `next rollout note` | first bounded note for later `P2` review |

## Coverage Values

- `issue+pr-linked`:
  - both frontmatter links already exist
- `issue-only`:
  - issue linkage exists but PR linkage does not
- `pr-only`:
  - PR linkage exists but issue linkage does not
- `missing-both`:
  - neither link exists yet

## Review Buckets

- `historical-reviewable`:
  - on-disk `S0F` logs that can be reviewed now for later automation
- `active-meta-lane`:
  - parent or current meta lanes that should not be mistaken for the first historical rollout packet
- `future-unopened-excluded`:
  - future `S0F` scope not yet materialized on disk and therefore intentionally excluded from this inventory

## Current Scan State

- `58` main `S0F` logs are currently on disk under `docs/logs/log-S0F-*.md`.
- Coverage counts currently stand at:
  - `8` rows with `issue+pr-linked`
  - `1` row with `issue-only`
  - `0` rows with `pr-only`
  - `49` rows with `missing-both`
- Coverage remains heavily concentrated in `S0F-1*`; every current historical series from `S0F-2*` through `S0F-7*` is still fully uncovered in frontmatter.
- `S0F-8A`, `S0F-8B`, and the `S0F` parent spine are counted separately as `active-meta-lane` rows and should not be used as the first historical automation packet.

## Series Summary

| series | total rows | issue+pr-linked | issue-only | pr-only | missing-both | review bucket | next rollout note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `9` | `8` | `0` | `0` | `1` | `historical-reviewable` | use as covered baseline first; only `S0F-1K` remains uncovered |
| `2` | `2` | `0` | `0` | `0` | `2` | `historical-reviewable` | first reviewed historical packet; admit before `S0F-6*` |
| `3` | `13` | `0` | `0` | `0` | `13` | `historical-reviewable` | dense governance packet; likely needs subdivision after `P2` starts |
| `4` | `9` | `0` | `0` | `0` | `9` | `historical-reviewable` | coherent docs-governance packet; candidate after `S0F-2*` |
| `5` | `10` | `0` | `0` | `0` | `10` | `historical-reviewable` | mixed migration/cleanup/history packet; defer until commit-readiness review |
| `6` | `3` | `0` | `0` | `0` | `3` | `historical-reviewable` | compact fallback packet, but denser and later than `S0F-2*` |
| `7` | `9` | `0` | `0` | `0` | `9` | `historical-reviewable` | chronology/provenance packet; likely later due recent active edits |
| `8` | `2` | `0` | `0` | `0` | `2` | `active-meta-lane` | exclude from first historical rollout; they are current meta lanes |
| `parent` | `1` | `0` | `1` | `0` | `0` | `active-meta-lane` | keep as spine/meta reference, not a first historical rollout row |

## Covered Baseline Rows

| series | row type | source rows | total rows | issue coverage | pr coverage | review bucket | next rollout note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `parent` | `issue-only` | `S0F-docs-management-v6` | `1` | `present` | `missing` | `active-meta-lane` | keep outside first historical rollout; parent spine issue already exists |
| `1` | `baseline-covered` | `S0F-1A, S0F-1B, S0F-1C, S0F-1D, S0F-1G, S0F-1H, S0F-1I, S0F-1J` | `8` | `present` | `present` | `historical-reviewable` | use as comparison baseline for later per-series rollout packets |

## Missing Coverage Rows By Series

| series | row type | source rows | total rows | issue coverage | pr coverage | review bucket | next rollout note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `missing-series` | `S0F-1K` | `1` | `missing` | `missing` | `historical-reviewable` | first uncovered remainder inside the otherwise covered baseline series |
| `2` | `missing-series` | `S0F-2A, S0F-2B` | `2` | `missing` | `missing` | `historical-reviewable` | first reviewed and admitted historical packet candidate after `P2-C1-S1S2`; bounded commit chain centered on lane policy, refined model, and direct support surfaces |
| `3` | `missing-series` | `S0F-3A, S0F-3B, S0F-3C, S0F-3D, S0F-3E, S0F-3F, S0F-3G, S0F-3H, S0F-3I, S0F-3J, S0F-3K, S0F-3L, S0F-3M` | `13` | `missing` | `missing` | `historical-reviewable` | dense contract/governance packet; likely needs sub-packets during `P2` |
| `4` | `missing-series` | `S0F-4A, S0F-4B, S0F-4C, S0F-4D, S0F-4E, S0F-4F, S0F-4G, S0F-4H, S0F-4I` | `9` | `missing` | `missing` | `historical-reviewable` | coherent docs-governance packet; likely second or third rollout candidate |
| `5` | `missing-series` | `S0F-5A, S0F-5B, S0F-5C, S0F-5D, S0F-5E, S0F-5F, S0F-5G, S0F-5H, S0F-5I, S0F-5J` | `10` | `missing` | `missing` | `historical-reviewable` | mixed migration/history packet; defer until commit extraction is checked carefully |
| `6` | `missing-series` | `S0F-6A, S0F-6B, S0F-6C` | `3` | `missing` | `missing` | `historical-reviewable` | reviewed as fallback comparator only; compact series but denser multi-commit view/history packet than `S0F-2*` |
| `7` | `missing-series` | `S0F-7A, S0F-7B, S0F-7C, S0F-7D, S0F-7E, S0F-7F, S0F-7G, S0F-7H, S0F-7I` | `9` | `missing` | `missing` | `historical-reviewable` | recent chronology/provenance work; likely later after commit-readiness review |
| `8` | `active-meta-lane` | `S0F-8A, S0F-8B` | `2` | `missing` | `missing` | `active-meta-lane` | exclude from first historical rollout; these are current meta lanes |

## Source Refs

- `docs/logs/log-S0F-8B-s0f-issue-pr-automation-inventory-and-per-series-rollout.md`
- `artifacts/_tmp_s0f_8b_p1_inventory_scan.json`
- `artifacts/_tmp_s0f_8b_p2_review_s0f2_vs_s0f6.json`