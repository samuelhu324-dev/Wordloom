# log-S0E-6A (Phase 6A: Log Structure Normalization and Dual-Track Evidence Contract)

---

**id**: `S0E-6A`
**kind**: `log`
**title**: `log structure normalization and dual-track evidence contract v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Issues, PR, Automation, Contract, Formatting, Evidence, epic/s0, sub/0e6a`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/332`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/348`
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  **reference_log_1**: `docs/logs/log-S0E-5B-guarded-lifecycle-apply-expansion.md`
  **reference_log_2**: `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  **reference_log_3**: `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  **reference_log_4**: `docs/logs/_template-log-parent-epic-spine.md`
  **reference_log_5**: `docs/logs/_template-log-phase-drills-evidence.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: ``
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-03-31`
**updated**: `2026-03-31`

---

## Decision / Outcome

**Decision**:

- `S0E-6A` exists to normalize how logs expose machine-consumable structure without deleting the human ledger value that current `Evidence` sections already provide.
- The core contract of this slice is a dual-track model rather than a replacement model:
  - `PR Summary Inputs` plus `Evidence Footer Source` stay as the automation-facing contract;
  - `Evidence` stays as the human audit ledger and drill narrative record.
- `S0E-6A` will fix which log sections must become explicitly structured, which sections may remain prose-first, and how parent/phase templates should express that boundary.

**Default choices (phase defaults / v1)**:

- `S0E-5B` is the current representative sample for the canonical split between `PR links` and `Evidence Footer Source`.
- `Evidence Footer Source` and `Evidence` are complementary, not competing:
  - the footer source exists for deterministic PR/body automation and gate checks;
  - the evidence ledger exists for human traceability, investigation, and long-form drill accounting.
- The first normalization target is not every prose section in logs. It is only the sections that are already being consumed, or are likely to be consumed, by GitHub issue/PR automation.
- Template work should be contract-first and migration-second: fix the model, then update templates, then selectively migrate historical logs.

## Constraints

- Do not collapse `Evidence` into `Evidence Footer Source`; the two sections have different consumers and different acceptable density.
- Do not continue allowing mixed `PR links / evidence footer` blocks once the split contract is fixed.
- Do not over-structure narrative sections such as `Decision / Outcome`, `Background`, `Current Status`, or `Recent changes`; these remain prose-first unless a concrete automation need is proven.
- Do not let parent/spine logs fabricate footer rows when the underlying evidence belongs to child phase logs.

## Scope

- `P0`: define the dual-track evidence model and section ownership rules
- `P1`: fix which log blocks are mandatory structured inputs for GitHub issue/PR automation
- `P2`: define the minimum stable structure for human-facing `Evidence` ledger entries
- `P3`: update parent and phase template guidance so the structure boundary is explicit at authoring time
- `P4`: define migration priority for old logs that still use mixed or narrative-only evidence shapes

## Success Criteria (DoD)

- The repo has one explicit rule that separates automation-facing evidence source from human-facing evidence ledger.
- The contract clearly says which sections are machine-consumable inputs:
  - `PR summary bullets`;
  - `PR checklist source`;
  - `PR links`;
  - `Evidence Footer Source`.
- The contract clearly says which sections remain prose-first and must not be parsed as automation contract inputs.
- Parent and phase templates can be updated mechanically from this slice without inventing new semantics during template editing.
- Historical log migration can be prioritized by shape risk instead of by ad hoc cleanup preference.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Normalize logs to one dual-track structure where `PR Summary Inputs` stays automation-facing while `Evidence` remains the human ledger.
- Fix the structured-input boundary so `PR links` and `Evidence Footer Source` stop drifting into mixed legacy shapes.
- Retain template and migration guidance that lets later log families adopt the same structure without inventing new semantics per slice.

**PR checklist source**:

- Default source: reuse this log's checked execution checklist once the dual-track model, template guidance, and representative migration policy all verify cleanly.

**PR links**:

- Log: `docs/logs/log-S0E-6A-log-structure-normalization-and-dual-track-evidence-contract.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`

## Stability (what stable means)

- This log can be marked `stable` when:
  - the dual-track model is fixed;
  - parent and phase template guidance has been updated to express that model;
  - at least one migration policy exists for mixed `PR links / evidence footer` logs and for narrative-only `## Evidence` logs.

## Current Status

- `S0E-5D` already fixed the PR-side canonical footer contract, but that contract currently applies to a mixed log corpus rather than to one uniformly normalized log structure family.
- `S0E-5B` is the clearest real sample of the intended split model because it keeps `PR links`, `Evidence Footer Source`, and `Evidence` as separate layers.
- The parent and phase templates have now been updated so the dual-track boundary is explicit at authoring time: `PR Summary Inputs` is the automation contract, while `Evidence` remains the human ledger.
- The first migration batch is now completed on representative mixed-shape `S0E` logs: `S0E-5C` and `S0E-4C` now use split `PR links` plus `Evidence Footer Source` instead of the legacy mixed block.
- A local `S0E-6A` issue draft and JSON sidecar have now been scaffolded so the slice also leaves one direct `log -> issue draft` sample under the normalized structure contract.
- `S0E-6A` is now `stable`: the contract, template guidance, representative migration policy, and one draft-generation sample are all in place.

## P0 (Dual-track structure model | v1)

### P0-C1-S1 (Automation contract vs human ledger boundary fixed | v1)

- Logs now need one explicit two-layer evidence model:
  - automation-facing source layer;
  - human-facing ledger layer.
- The automation-facing source layer is limited to compact, low-ambiguity blocks under `PR Summary Inputs (optional)`.
- The human-facing ledger layer remains the `Evidence` section, where drill context, expected/observed detail, and auxiliary artifact lists can stay visible to readers.
- The presence of `artifacts:` inside `Evidence` does not imply that those rows are valid `Evidence Footer Source` rows.

### P0-C1-S2 (Section ownership fixed | v1)

- Machine-consumable ownership:
  - `PR Summary Inputs` owns PR summary bullets, checklist source, explicit PR links, and footer-source rows.
- Human-ledger ownership:
  - `Evidence` owns drill accounting, traceability prose, expected/observed outcomes, and any wider artifact set that should remain visible to operators.
- Prose-only ownership:
  - `Decision / Outcome`, `Constraints`, `Current Status`, and `Recent changes` remain explanation surfaces and must not be treated as source blocks for automation extraction.

## P1 (Structured blocks for automation | v1)

### P1-C1-S1 (Mandatory structured input blocks fixed | v1)

- The recommended structured blocks for GitHub issue/PR automation are now fixed as:
  - `PR summary bullets`;
  - `PR checklist source`;
  - `PR links`;
  - `Evidence Footer Source`.
- The old mixed block name `PR links / evidence footer` should now be treated as a transitional legacy shape to be migrated away from.
- `Evidence Footer Source` should keep the current single canonical line shape introduced by `S0E-5D` and should not carry prose or non-footer link rows.

### P1-C1-S2 (Non-goal structured blocks explicitly excluded | v1)

- The following sections should not be promoted into machine-consumable contract inputs in this slice:
  - `Decision / Outcome`;
  - `Background`;
  - `Current Status`;
  - `Notes`;
  - `Recent changes`.
- These sections may remain rich prose because their value is explanation, not deterministic parsing.

## P2 (Human-facing evidence ledger minimum shape | v1)

### P2-C1-S1 (Minimum evidence ledger fields fixed | v1)

- `Evidence` remains required for drill/evidence-heavy phase logs even when `Evidence Footer Source` already exists.
- Each evidence unit should keep a stable minimal ledger shape:
  - unit heading with `P*-C*-S*` and date;
  - `headSha` when applicable;
  - `artifacts` as a list;
  - `expected`;
  - `observed`.
- This is intentionally a semi-structured human ledger rather than a fully normalized machine schema.

### P2-C1-S2 (Footer-to-ledger relationship fixed | v1)

- `Evidence Footer Source` rows should usually point at one representative artifact per relevant unit, not replay the entire artifact inventory from `Evidence`.
- `Evidence` may include many more artifacts than the footer source because its audience includes later debugging and audit review.
- Therefore keeping both sections is recommended, and the repo should not force authors to choose between them.

## P3 (Template optimization boundary | v1)

### P3-C1-S1 (Parent template guidance target fixed | v1)

- Parent/spine templates should state more clearly that they are usually aggregators, not the primary home of execution evidence.
- Parent/spine `PR Summary Inputs` should remain optional and should only be filled when the parent log itself is the intended PR contract source.
- When parent/spine logs aggregate child evidence, they should reference child log sources rather than synthesizing footer rows from prose.

### P3-C1-S2 (Phase template guidance target fixed | v1)

- Phase/drill templates should state more clearly that:
  - `Evidence Footer Source` is the automation contract;
  - `Evidence` is the human ledger.
- Phase templates should explicitly discourage mixing explanation prose into `PR links` or footer-source blocks.
- Phase templates should also keep the minimum stable `Evidence` ledger shape visible so authors do not drift back to purely narrative evidence paragraphs.

## P4 (Migration policy | v1)

### P4-C1-S1 (Historical log migration priority fixed | v1)

- Migration priority should be driven by automation risk rather than by age alone.
- First priority:
  - `S0E` logs that already have `PR Summary Inputs` but still use `PR links / evidence footer`.
- Second priority:
  - logs expected to continue driving GitHub PR/issue automation soon.
- Third priority:
  - narrative-only evidence families such as `S4C` and `S4D`, after a separate decision is made on whether they need machine-consumable footer-source blocks or may remain human-ledger-first.

## Plan (draft)

- `P0-C1-S1`: fix the dual-track evidence model and ownership boundary
- `P1-C1-S1`: fix the mandatory structured blocks for GitHub automation inputs
- `P2-C1-S1`: fix the minimum stable shape for human-facing evidence ledger entries
- `P3-C1-S1`: translate the contract into parent/phase template guidance
- `P4-C1-S1`: prioritize migration targets across mixed and narrative-only log families

## Execution Checklist (unchecked)

- [x] `P0-C1-S1`: dual-track evidence model fixed
- [x] `P0-C1-S2`: section ownership fixed
- [x] `P1-C1-S1`: mandatory structured input blocks fixed
- [x] `P1-C1-S2`: prose-only non-goal blocks fixed
- [x] `P2-C1-S1`: minimum evidence ledger shape fixed
- [x] `P2-C1-S2`: footer-to-ledger relationship fixed
- [x] `P3-C1-S1`: parent template guidance target fixed
- [x] `P3-C1-S2`: phase template guidance target fixed
- [x] `P4-C1-S1`: historical migration priority fixed

## Evidence (reserved)

- This slice is contract-first. The recorded evidence now includes template delta anchors, representative mixed-log normalization samples, and one local issue-draft scaffold sample.

### P3-C1-S1S2 (parent and phase template guidance updated | 2026-03-31)

- artifacts:
  - `docs/logs/_template-log-parent-epic-spine.md`
  - `docs/logs/_template-log-phase-drills-evidence.md`
  - `docs/logs/log-S0E-6A-log-structure-normalization-and-dual-track-evidence-contract.md`
- expected:
  - parent/spine template guidance should clarify that `PR Summary Inputs` is the automation contract while execution evidence usually remains in child logs or explicit evidence sections
  - phase/drill template guidance should preserve `Evidence Footer Source` and `Evidence` as separate layers with explicit authoring rules
- observed:
  - the parent template now states that automation-facing footer rows should not be synthesized from prose aggregates and adds an optional aggregator-style `Evidence` note
  - the phase template now states that `Evidence Footer Source` is the automation contract, `Evidence` is the human ledger, and the minimum evidence ledger shape should stay visible to authors

### P4-C1-S1 (representative mixed-log migration and issue-draft scaffold completed | 2026-03-31)

- artifacts:
  - `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  - `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
  - `docs/issues/issue-S0E-6A-log-structure-normalization-and-dual-track-evidence-contract.md`
  - `docs/issues/issue-S0E-6A-log-structure-normalization-and-dual-track-evidence-contract.json`
- expected:
  - the first migration batch should remove legacy mixed `PR links / evidence footer` blocks from representative `S0E` logs and replace them with split `PR links` plus `Evidence Footer Source`
  - the normalized contract should remain usable by existing issue-draft generation without requiring a separate one-off draft shape
- observed:
  - `S0E-5C` and `S0E-4C` now expose separate `PR links` and `Evidence Footer Source` blocks, eliminating the mixed source shape that previously polluted footer extraction inputs
  - `gen_issue_draft.py` now generates a local `S0E-6A` issue draft and JSON sidecar directly from the normalized source log, leaving one concrete `log -> issue draft` sample for later real create-mode work

## Recent changes (for traceability, optional)

- 2026-04-03: wrote back live issue `#332`, created and merged PR `#348`, applied the final issue-conclusion body, and confirmed the live issue is closed.
- 2026-03-31: created `S0E-6A` to separate log-structure normalization from the already-stabilized PR body contract work in `S0E-5D`.
- 2026-03-31: fixed the initial position that `Evidence Footer Source` and `Evidence` should both remain, with explicit split ownership instead of replacement semantics.
- 2026-03-31: updated parent/phase log templates so the dual-track evidence boundary is explicit at authoring time rather than staying as informal guidance.
- 2026-03-31: normalized the first representative mixed-shape `S0E` logs, `S0E-5C` and `S0E-4C`, from legacy `PR links / evidence footer` blocks to split `PR links` plus `Evidence Footer Source`.
- 2026-03-31: scaffolded `S0E-6A` local issue draft artifacts under `docs/issues/` so the slice leaves one direct sample for the normalized log-to-issue path.