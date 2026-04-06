# PRB Split Package v1

## Purpose

- This view explains the executed split of the old fused `PRB` current contract into separate reviewer and gate current contracts.
- It exists so readers can inspect the new current-state separation without treating `INDEX.md` as a mixed current-plus-history ledger.

## Current Model

- The current front door now separates PR-body semantics into:
  - `PRR`: reviewer-owned PR body classification
  - `PRG`: PR body standard-check gate semantics
- The old `GC-PRB-0001` file remains preserved as a deprecated legacy umbrella record.

## Executed Mapping

- Executed package:
  - `PRB split package v1`
- Successor mapping:
  - `GC-PRB-0001` -> `GC-PRR-0001`
  - `GC-PRB-0001` -> `GC-PRG-0001`

## Preservation Status

- `GC-PRB-0001` remains on disk as a deprecated legacy umbrella file.
- The backfill note for `GC-PRB-0001` remains support-only history and does not become a front-door current record.
- The current front door now exposes the two narrower current contracts instead of the fused umbrella.

## Reader Notes

- Use `GC-PRR-0001` when the question is how PR body completeness is classified.
- Use `GC-PRG-0001` when the question is how those findings affect pass or non-pass gate semantics.

## Source Refs

- `docs/logs/log-S0F-3E-governance-registry-lineage-and-legacy-handling.md`
- `docs/logs/log-S0F-1H-pr-body-completeness-reviewer.md`
- `docs/logs/log-S0F-1I-formatting-only-pr-body-convergence.md`
- `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
- `docs/logs/patch/log-S0F-P1-s0f-pr-body-completeness-standard-check-dispatch-failure-triage.md`
- `docs/governance/contracts/GC-PRB-0001-historical-drift-fail-on-findings.md`
- `docs/governance/contracts/GC-PRR-0001-pr-body-canonical-review-classification.md`
- `docs/governance/contracts/GC-PRG-0001-pr-body-standard-check-fail-on-substantive-drift.md`