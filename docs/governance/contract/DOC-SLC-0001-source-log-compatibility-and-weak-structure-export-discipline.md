# doc-contract-record: DOC-SLC-0001

- `record_id`: `DOC-SLC-0001`
- `contract_id`: `SOURCE-LOG-COMPATIBILITY-AND-WEAK-STRUCTURE-EXPORT-DISCIPLINE`
- `title`: `source-log compatibility and weak-structure export discipline stay explicit across current DOC governance surfaces`

```yaml
doc_contract:
  record_id: DOC-SLC-0001
  contract_id: SOURCE-LOG-COMPATIBILITY-AND-WEAK-STRUCTURE-EXPORT-DISCIPLINE
  family: DOC
  area: SLC
  status: active
  summary: Current documentation-governance source logs must keep the old two canonical source-log templates as the only default strong-structure families, while six outlets operate only as export ownership for weak-structure content rather than as permission to replace source-log strong structure.
  primary_source_owner: docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md
  applies_to: documentation-governance parent and phase logs, source-log slimming decisions, template compatibility guidance, and weak-structure export decisions derived from the same source-log family
  enforcement_surface: source-log authoring guidance, weak-structure export review, and future source-log admission decisions
  violation_semantics: warning
  introduced_by: S0F-4B/P0-P2
  last_changed_by: S0F-4E/P3-C2-S1S2
  source_refs:
    - docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md
    - docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md
  supersedes: []
  superseded_by: []
  notes:
    - This file is the second family-owned DOC contract body promoted out of a source-owner log.
    - S0F-4B remains the retained source-owner traceability log for this rule set after stable close-out review completed under S0F-5A.
    - S0F-1K remains a bounded historical restructuring sample and is not elevated by this record into a default source-log template precedent.
```

## Current Rule

- The only canonical source-log families for current documentation-governance work remain the two old templates:
  - `docs/logs/_template-log-parent-epic-spine.md`
  - `docs/logs/_template-log-phase-drills-evidence.md`
- The six-outlet model remains valid, but only as export ownership for weak-structure content.
- The six-outlet model does not authorize replacing source-log strong structure with a mixed-role or hollowed-out ledger shape.
- Weak-structure content should export first, while the source-log strong-structure skeleton remains automation-safe and lifecycle-safe.

## Strong Structure And Weak Structure

- **Strong structure** means the source-log blocks that automation or lifecycle readers depend on directly.
- **Weak structure** means repeated narrative, explanations, summaries, or placement detail that may be exported without breaking automation.
- Current source logs must retain, at minimum, their automation-facing strong-structure core:
  - `Decision / Outcome`
  - `PR Summary Inputs`
  - `Execution Checklist`
  - `Current Status`
  - `Evidence`
- Old logs may slim by moving repeated narrative, operator detail, family summary, or placement discussion into the correct outlets, but they should not delete or semantically hollow out the retained strong-structure core.

## Outlet Compatibility Rule

- `contract` owns stable current rule text and long-form normative semantics.
- `runbook` owns stable repeatable operator procedure and troubleshooting steps.
- `view` owns bounded reader summary or family interpretation.
- `index/front-door` owns current navigation and entrypoint discovery.
- `disposition/placement` owns support-only, legacy, stub, and cleanup standing.
- `log-retained core` owns source-log metadata, decision blocks, automation-facing source blocks, checklist, status, evidence, and minimum bridge notes.
- Under this rule, six outlets are downstream ownership targets for weak-structure export, not a third default source-log family.

## Historical Sample Boundary

- `S0F-1K` remains valid only as one bounded restructuring ledger for the executed `S0F-1I` exact-path package.
- `S0F-1K` must not be reused as a positive template precedent for future issue-source or PR-source logs.
- Future readers may cite `S0F-1K` only for its bounded restructuring result, not for source-log template selection.

## Constraints

- Do not treat six outlets as permission to invent a third default source-log template.
- Do not delete or hollow out automation-facing source blocks during weak-structure export.
- Do not reuse `S0F-1K` as the default source-log shape for new slices.
- If a future automation reader wants field-level extraction instead of whole-section reading, that change must land first as an explicit automation contract rather than as silent documentation drift.

## Reader Notes

- This file is the second active family-owned current contract body mapped from `S0F-4B`.
- `S0F-4B` remains the retained source-owner traceability log for lineage, evidence, and concentrated historical source context, but current reader-facing rule ownership now reads here.
- Stable close-out review for the second promotion lane has completed under `S0F-5A`, and no bounded post-stable export tail was required.

## Traceability

- Source-owner log:
  - `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
- Promotion lane:
  - `docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md`