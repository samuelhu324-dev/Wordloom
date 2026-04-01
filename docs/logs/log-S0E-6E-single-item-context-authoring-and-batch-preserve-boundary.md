# log-S0E-6E (Phase 6E: single-item Context authoring and batch-preserve boundary)

---

**id**: `S0E-6E`
**kind**: `log`
**title**: `single-item Context authoring and batch-preserve boundary v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Workflow, Automation, Contract, Formatting, epic/s0, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-6D-natural-issue-context-rendering-and-weak-gate.md`
  **reference_log_1**: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_3**: `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  **reference_log_4**: `docs/logs/log-S0E-6D-natural-issue-context-rendering-and-weak-gate.md`
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
**created**: `2026-04-01`
**updated**: `2026-04-01`

---

## Decision / Outcome

**Decision**:

- `S0E-6E` exists because `S0E-6D` successfully weakened the gate, but it still kept `Context` generation inside batch-capable draft/conclusion replay paths.
- v1 moves `Context` ownership to a clearer split: batch tools may discover, preserve, and warn, while actual `Context` prose generation should happen one log at a time.
- The human-facing `Context` block is no longer treated as a bulk rewrite surface; only the weak gate remains batch-verifiable.

**Default choices (phase defaults / v1)**:

- `Context` generation should default to single-item authoring from one source log, not batch replay across many issues.
- Issue draft generation should default back to scaffold mode for `Context`, leaving authoring to a later one-item pass.
- Issue conclusion planning should preserve the live `Context` block by default, even when it is weak or drifted, and should report that drift instead of auto-writing replacement prose.
- Batch tooling may still be used to discover missing or malformed `Context` blocks, but it should not claim ownership of the prose itself.
- The gate remains minimal: `3-5` readable English bullet sentences, basic sentence completeness, and placeholder hygiene.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Define a new ownership boundary where `Context` prose is generated one log at a time while batch tools only preserve, discover, and warn.
- Add one explicit single-item `Context` draft entrypoint and move issue draft generation back to scaffold-first behavior by default.
- Change batch issue-conclusion planning so it preserves the live `Context` block unless an operator explicitly opts into single-item regeneration.

**PR checklist source**:

- Default source: reuse this log's execution checklist after the single-item generator, scaffold defaults, and batch-preserve sample are validated.

**PR links**:

- Log: `docs/logs/log-S0E-6E-single-item-context-authoring-and-batch-preserve-boundary.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/issue-context-S0E-6E-sample-draft.json`

## Constraints

- Do not let batch issue planning or batch issue conclusion replay silently author new `Context` prose by default.
- Do not strengthen the `Context` gate beyond readable English sentence rows, bounded line count, and placeholder hygiene.
- Do not turn single-item `Context` generation into a requirement for all issue creation paths; scaffold-first draft generation remains allowed.
- Do not hide drift findings: when a live `Context` block is malformed, batch tools should preserve and warn rather than auto-fix it.

## Scope

- `P0`: define the single-item versus batch-preserve ownership boundary for issue `Context`
- `P1`: add a single-item `Context` draft entrypoint and restore scaffold-first issue draft defaults
- `P2`: change batch issue-conclusion planning to preserve live `Context` by default and only single-generate on explicit opt-in
- `P3`: retain representative one-item and batch-preserve sample artifacts that prove the new boundary works in practice
- `P4`: apply one-item live Context refreshes to representative closed issues and re-audit them under the same weak gate

## Success Criteria (DoD)

- `Context` authoring is no longer coupled to batch draft/conclusion replay by default.
- One explicit script can generate a `Context` draft from exactly one source log at a time.
- Issue draft generation returns to scaffold-first behavior unless an operator explicitly requests single-item generation.
- Batch issue-conclusion planning preserves the current live `Context` block by default and warns when the block is missing or malformed.
- Representative retained artifacts show both sides of the new rule: one single-item Context draft and one batch-preserve conclusion plan.
- At least one pair of real closed issues proves that the new one-item path can improve live `Context` prose without reopening batch rewrite ownership.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P4` have fixed the ownership boundary, single-item generator, scaffold-first draft behavior, batch-preserve conclusion planning, and representative one-item live refreshes;
  - the Evidence section records one single-item draft artifact, one batch-preserve plan artifact, and one re-audited live refresh pair.

## Current Status

- `S0E-6E` is now opened as the ownership follow-up to `S0E-6D`.
- `P0` is now completed: `Context` is split into single-item authoring versus batch-preserve discovery, rather than one shared automation-owned rewrite surface.
- `P1` is now completed: the repo now has a dedicated single-item `Context` draft script, and `gen_issue_draft.py` now defaults back to scaffold-first `Context` output.
- `P2` is now completed: `plan_issue_conclusion.py` now preserves live `Context` by default and only regenerates it on explicit `single-generate` opt-in.
- `P3` is now completed: representative sample artifacts now prove both one-item generation and batch-preserve conclusion planning under the new boundary.
- `P4-C1-S1` is now completed: `S0E-2B/#288` and `S0E-2A/#289` have now been refreshed through one-item `Context` authoring and then re-audited successfully.

## P0 (Ownership boundary | v1)

### P0-C1-S1 (Single-item authoring versus batch-preserve boundary fixed | v1)

- `Context` prose belongs to one-item authoring, not to batch replay.
- Batch tools may audit, preserve, and warn, but they no longer own the wording of `Context` by default.

### P0-C1-S2 (Weak gate retained and narrowed to discovery use | v1)

- The `Context` gate still checks bounded readable English bullet rows, placeholder hygiene, and basic sentence completeness.
- Batch planning may use that gate to discover drift, but it should not auto-author replacement prose just because the gate fails.

## P1 (Single-item entrypoint and scaffold-first draft behavior | v1)

### P1-C1-S1 (Single-item `Context` draft entrypoint added | v1)

- `scripts/issues/generate_issue_context_draft.py` now generates one `Context` draft from exactly one source log at a time.
- The script supports both `draft` and `conclusion` phases but stays explicitly one-item in scope.

### P1-C1-S2 (Issue draft generation returned to scaffold-first default | v1)

- `scripts/issues/gen_issue_draft.py` now defaults `Context` back to scaffold mode with a placeholder row.
- Operators may still opt into `--context-mode single-generate`, but authoring is no longer implicit in the main draft-generation path.

## P2 (Batch-preserve conclusion planning | v1)

### P2-C1-S1 (Batch conclusion planning preserves live Context by default | v1)

- `scripts/issues/plan_issue_conclusion.py` now defaults to `--context-mode preserve-existing`.
- Preview bodies keep the live `Context` block in place and report drift through warnings instead of replacing the prose.

### P2-C1-S2 (Explicit single-generate opt-in retained for targeted cases | v1)

- Batch conclusion planning may still regenerate `Context`, but only when `--context-mode single-generate` or an equivalent manifest override is explicitly requested.
- This keeps targeted single-item rewrites available without letting them remain the default batch behavior.

## P3 (Representative samples | v1)

### P3-C1-S1 (Single-item draft sample retained | v1)

- One retained artifact should show the output of the dedicated single-item `Context` draft script.
- The sample should be traceable to one source log and should not depend on a batch manifest.

### P3-C1-S2 (Batch-preserve conclusion sample retained | v1)

- One retained artifact should show a conclusion plan produced under `preserve-existing` mode.
- The sample should prove that batch tooling now preserves the live `Context` block and reports drift or blank state through warnings.

## P4 (Representative one-item live refreshes | v1)

### P4-C1-S1 (Two representative closed issues refreshed and re-audited | v1)

- After the new ownership boundary is fixed, the repo should still prove that live issue improvement remains possible through one-item authoring.
- The representative proof set for v1 is `S0E-2B/#288` and `S0E-2A/#289`, refreshed one issue at a time instead of through batch replay.

## Execution Checklist (unchecked)

### P0 (Ownership boundary)

- [x] `P0-C1-S1`: single-item authoring versus batch-preserve boundary fixed
- [x] `P0-C1-S2`: weak gate retained for discovery instead of batch authoring

### P1 (Single-item entrypoint and scaffold-first draft behavior)

- [x] `P1-C1-S1`: single-item `Context` draft entrypoint added
- [x] `P1-C1-S2`: issue draft generation returned to scaffold-first default

### P2 (Batch-preserve conclusion planning)

- [x] `P2-C1-S1`: batch conclusion planning preserves live Context by default
- [x] `P2-C1-S2`: explicit single-generate opt-in retained for targeted cases

### P3 (Representative samples)

- [x] `P3-C1-S1`: single-item draft sample retained
- [x] `P3-C1-S2`: batch-preserve conclusion sample retained

### P4 (Representative one-item live refreshes)

- [x] `P4-C1-S1`: `S0E-2B` and `S0E-2A` refreshed one item at a time and re-audited

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the key retained sample paths and observed boundary behavior.

### P0-P3 (single-item authoring and batch-preserve boundary implemented | 2026-04-01)

- headSha: `c8b0a0b8`
- artifacts:
  - `scripts/issues/generate_issue_context_draft.py`
  - `scripts/issues/gen_issue_draft.py`
  - `scripts/issues/plan_issue_conclusion.py`
  - `docs/issues/issue-context-S0E-6E-sample-draft.md`
  - `docs/issues/issue-context-S0E-6E-sample-draft.json`
  - `docs/issues/issue-S0E-6E-sample.md`
  - `docs/issues/issue-S0E-6E-sample.json`
  - `docs/issues/issue-conclusion-S0E-6E-context-preserve-sample-manifest.json`
  - `docs/issues/issue-conclusion-S0E-6E-context-preserve-sample-plan.json`
  - `docs/issues/issue-conclusion-S0E-6E-context-preserve-sample-s0e-2a-body.md`
- expected:
  - the repo should stop treating batch draft/conclusion flows as the default author of `Context` prose while still retaining one explicit one-item generation path and one batch-preserve planning path
- observed:
  - issue draft generation now defaults to scaffold-first `Context`, a new one-item `Context` generator retains dedicated draft artifacts, and batch issue-conclusion planning now preserves live `Context` by default while warning about drift instead of auto-rewriting it

### P4-C1-S1 (representative one-item live refresh pair applied and re-audited | 2026-04-01)

- artifacts:
  - `docs/issues/issue-context-S0E-2A-6E-refresh.md`
  - `docs/issues/issue-context-S0E-2A-6E-refresh.json`
  - `docs/issues/issue-context-S0E-2B-6E-refresh.md`
  - `docs/issues/issue-context-S0E-2B-6E-refresh.json`
  - `docs/issues/issue-conclusion-S0E-6E-single-item-refresh-s0e-2a-body.md`
  - `docs/issues/issue-conclusion-S0E-6E-single-item-refresh-s0e-2a-live.json`
  - `docs/issues/issue-conclusion-S0E-6E-single-item-refresh-s0e-2b-body.md`
  - `docs/issues/issue-conclusion-S0E-6E-single-item-refresh-s0e-2b-live.json`
  - `docs/issues/lifecycle-audit-S0E-6E-single-item-refresh-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-6E-single-item-refresh-manifest-plan.json`
- expected:
  - the new `6E` boundary should still allow real live issue improvement, but only through one-item authoring and re-audit rather than through another batch rewrite family
- observed:
  - `S0E-2B/#288` and `S0E-2A/#289` were rewritten one at a time with manually reviewed Context prose, the post-refresh live issue snapshots were retained, and the pair then re-audited successfully under the same prose-first gate

## Recent changes (for traceability, optional)

- 2026-04-01: created `S0E-6E` to separate single-item `Context` authoring from batch issue replay and conclusion planning.
- 2026-04-01: added `scripts/issues/generate_issue_context_draft.py` as the dedicated one-log-at-a-time `Context` generation entrypoint.
- 2026-04-01: changed `scripts/issues/gen_issue_draft.py` so `Context` returns to scaffold-first output by default unless `--context-mode single-generate` is explicitly requested.
- 2026-04-01: changed `scripts/issues/plan_issue_conclusion.py` so batch conclusion planning now preserves live `Context` by default and reports drift through warnings instead of auto-writing replacement prose.
- 2026-04-01: refreshed `S0E-2B/#288` and `S0E-2A/#289` one item at a time under the new boundary, proving that live improvement now happens through single-item authoring rather than batch Context replay.