# log-S0E-6C (Phase 6C: issue Context sentence contract and gate)

---

**id**: `S0E-6C`
**kind**: `log`
**title**: `issue Context sentence contract and gate v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Workflow, Automation, Contract, Formatting, epic/s0, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-6B-log-stability-and-gate-strategy.md`
  **reference_log_1**: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_3**: `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  **reference_log_4**: `docs/logs/log-S0E-6B-log-stability-and-gate-strategy.md`
  **reference_log_5**: `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
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

- `S0E-6C` is the dedicated follow-up for issue-body `Context` shape after `S0E-2D`, `S0E-2E`, `S0E-5D`, and `S0E-6B` fixed the broader issue-body and gate contracts.
- The new contract is now explicit and deterministic in two dimensions: parent/main-log issues must keep exactly five English `Context` sentences, child-log issues must keep exactly four English `Context` sentences, and each sentence must occupy its own bullet line.
- The sentence count remains fixed, but the sentence content must now be derived from the current source log instead of reusing one shared boilerplate block across unrelated issues.
- This rule now applies both when issue bodies are first scaffolded and when concluded issue bodies are rewritten after merged PR evidence is available.

**Default choices (phase defaults / v1)**:

- The `Context` section should remain English-only and should use one sentence per bullet line.
- The parent/main-log issue tier is now distinguished by source-log ownership: logs without `parent_log` use a 5-line `Context`, while child logs with `parent_log` use a 4-line `Context`.
- The sentence-count contract should be reused by both renderers and gates instead of being reimplemented separately per script.
- The rendered `Context` content must be source-log-derived: it should carry the current log ID, the current log subject/title, and the relevant follow-up position or delivery evidence instead of repeating a repo-wide generic paragraph.
- Lifecycle audit should now treat insufficient or malformed issue `Context` content as a gate failure rather than as a cosmetic warning.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.

**PR summary bullets**:

- Fix issue-body `Context` to a deterministic English sentence contract with `5` lines for main logs and `4` lines for child logs.
- Reuse the same sentence contract in issue draft generation, issue conclusion rendering, and lifecycle audit gate checks.
- Make the rendered `Context` sentences source-log-derived so different issues no longer receive the same generic wording.
- Re-run the real `S0E-5C/#309` conclusion path and audit so the new `Context` gate is exercised on a live concluded issue.

**PR checklist source**:

- Default source: reuse this log's execution checklist after `P0` is reviewed.

**PR links**:

- Log: `docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md`
- Issue: ``
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/lifecycle-audit-S0E-5C-context-gate-plan.json`

**PR body notes**:

- Keep `Context` deterministic and English-only, but do not widen this slice into a full prose-quality linter.
- Keep `Definition of Done (DoD)` ownership unchanged: this slice only fixes `Context` shape and its gate semantics.

## Constraints

- Do not turn the new sentence-count rule into open-ended NLP validation; this slice only fixes deterministic shape plus source-log-derived anchors.
- Do not weaken the broader issue-body contract already fixed by `S0E-5D`.
- Do not leave create-time and conclusion-time issue renderers with different `Context` rules once the new contract is fixed.
- Do not keep the new `Context` review as advisory-only when lifecycle audit is already acting as a gate for concluded issue integrity.

## Scope

- `P0`: fix the canonical `Context` sentence-count contract for main issues and child issues
- `P1`: wire the same canonical `Context` block into issue draft generation and issue conclusion rendering
- `P2`: add a lifecycle-audit gate check for issue `Context` sentence count and one-sentence-per-line shape
- `P3`: rerun one real issue conclusion and audit sample to verify the contract on a live concluded issue

## Success Criteria (DoD)

- The repo has one explicit issue-body `Context` contract with deterministic sentence counts for main and child logs.
- New issue drafts and conclusion previews reuse the same canonical `Context` source instead of hand-writing separate bodies.
- The rendered `Context` sentences carry source-log-specific anchors rather than one shared boilerplate block.
- Lifecycle audit blocks concluded issues whose `Context` section does not satisfy the canonical sentence-count rule.
- At least one real concluded issue has been rewritten and re-audited under the new contract.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` have fixed the `Context` sentence-count contract, rendering reuse, and lifecycle-audit gate
  - one real concluded issue has been rewritten and re-audited under the new contract
  - the Evidence section records traceable artifacts for the representative live sample

## Current Status

- `S0E-6C` is now opened as the dedicated follow-up for issue-body `Context` sentence shape.
- `P0` is now completed: the issue-body `Context` contract is fixed at `5` English bullet sentences for main logs and `4` English bullet sentences for child logs, with one sentence per line.
- `P1` is now completed: issue draft generation and issue conclusion planning now both reuse source-log-derived `Context` blocks instead of leaving the section blank, reducing it to one fallback line, or repeating one generic template.
- `P2` is now completed: lifecycle audit now fails when issue `Context` content does not satisfy the canonical sentence-count, one-sentence-per-line, and source-log-anchor rule.
- `P3` is now completed: live issue `#309` has been re-concluded under the new child-log `4`-sentence `Context` contract and then re-audited successfully.

## P0 (Context sentence contract | v1)

### P0-C1-S1 (Main-log vs child-log Context rule fixed | v1)

- Main-log issues now keep exactly five English `Context` sentences.
- Child-log issues now keep exactly four English `Context` sentences.
- The deciding surface is the source log itself:
  - logs without `parent_log` are treated as main-log issues;
  - logs with `parent_log` are treated as child-log issues.

### P0-C1-S2 (One-sentence-per-line rule fixed | v1)

- Each `Context` row must be rendered as one bullet line that carries exactly one English sentence.
- The rule is deterministic rather than stylistic:
  - the row must be a bullet line;
  - the content must be English-only at the sentence level;
  - the row must end with a single sentence terminator.

### P0-C1-S3 (Source-log-derived content rule fixed | v1)

- `Context` content must no longer be a repo-wide generic boilerplate block.
- The rendered lines should carry source-log-specific anchors such as the current log ID, the current log subject, and the relevant follow-up position or delivery evidence.
- This keeps deterministic shape while still making the issue body explain why that particular issue exists and what that particular slice completed.

## P1 (Renderer reuse | v1)

### P1-C1-S1 (Issue draft Context renderer fixed | v1)

- `gen_issue_draft.py` no longer leaves `Context` blank.
- The draft generator now emits a canonical source-log-derived English `Context` block sized by main-log vs child-log tier.

### P1-C1-S2 (Issue conclusion Context renderer fixed | v1)

- `plan_issue_conclusion.py` no longer falls back to a single canonical conclusion line.
- The conclusion planner now rewrites `Context` to the canonical source-log-derived English block for the relevant issue tier whenever the live body does not already satisfy the sentence contract.

## P2 (Lifecycle-audit gate | v1)

### P2-C1-S1 (Issue Context sentence-count gate fixed | v1)

- `plan_lifecycle_audit.py` now validates issue-body `Context` shape against the canonical sentence-count contract.
- The new check fails when the `Context` section:
  - contains the wrong number of bullet sentences;
  - contains non-bullet drift;
  - contains non-English or multi-sentence rows;
  - omits the source-log-specific anchors that make the content belong to the current issue rather than to a generic template.

### P2-C1-S2 (Closed-issue gate alignment fixed | v1)

- For concluded issues, `closed-body-shape` now depends on the canonical `Context` sentence contract rather than on generic “substantive content” only.
- This keeps `S0E-6C` aligned with `S0E-6B`: the gate stays deterministic and contract-first.

## P3 (Representative live replay | v1)

### P3-C1-S1 (Real conclusion replay for `S0E-5C/#309` completed | v1)

- `#309` previously carried only one `Context` sentence after conclusion write-back.
- The issue conclusion plan was regenerated under the new contract, applied to the live issue, and re-audited so the child-log `4`-sentence rule is now evidenced on a real concluded issue.

## Plan (draft)

- `P0-C1-S1`: fix the main-log vs child-log sentence-count contract
- `P1-C1-S1`: reuse the same canonical `Context` blocks in issue draft and issue conclusion renderers
- `P2-C1-S1`: fail lifecycle audit when issue `Context` shape drifts from the canonical contract
- `P3-C1-S1`: re-run one live conclusion path and re-audit it under the new gate

## Execution Checklist (unchecked)

- [x] `P0-C1-S1`: main-log vs child-log Context sentence-count contract fixed
- [x] `P0-C1-S2`: one-sentence-per-line Context rule fixed
- [x] `P1-C1-S1`: issue draft Context renderer fixed
- [x] `P1-C1-S2`: issue conclusion Context renderer fixed
- [x] `P2-C1-S1`: issue Context sentence-count gate fixed
- [x] `P2-C1-S2`: closed-issue gate alignment fixed
- [x] `P3-C1-S1`: real conclusion replay and re-audit completed for `S0E-5C/#309`

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this section keeps the representative contract and live replay evidence visible.

### P0-C1-S1S2 + P1-C1-S1S2 + P2-C1-S1S2 (Context contract, renderer reuse, and gate fixed | 2026-04-01)

- headSha: `86f01bdb`
- artifacts:
  - `scripts/issues/body_contract.py`
  - `scripts/issues/gen_issue_draft.py`
  - `scripts/issues/plan_issue_conclusion.py`
  - `scripts/issues/plan_lifecycle_audit.py`
  - `artifacts/_tmp_s0e_6c_issue_conclusion_plan.json`
- expected:
  - the repo should have one deterministic issue `Context` sentence contract reused by both renderers and by lifecycle audit
- observed:
  - the repo now renders canonical `Context` blocks for issue draft and issue conclusion, and lifecycle audit now fails when the `Context` section does not satisfy the required sentence count and one-sentence-per-line rule

### P3-C1-S1 (real conclusion replay and re-audit for `S0E-5C/#309` completed | 2026-04-01)

- headSha: `86f01bdb`
- artifacts:
  - `docs/issues/issue-conclusion-S0E-5C-context-gate-manifest.json`
  - `docs/issues/issue-conclusion-S0E-5C-context-gate-plan.json`
  - `docs/issues/issue-conclusion-S0E-5C-context-gate-s0e-5c-body.md`
  - `docs/issues/issue-conclusion-S0E-5C-context-gate-s0e-5c-apply-body.md`
  - `docs/issues/issue-conclusion-S0E-5C-context-gate-s0e-5c-apply-result.json`
  - `docs/issues/lifecycle-audit-S0E-5C-context-gate-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-5C-context-gate-plan.json`
- expected:
  - the representative live concluded issue should be rewritten to the new child-log `4`-sentence contract and then pass lifecycle audit under the new gate
- observed:
  - `#309` was re-concluded with the canonical child-log `4`-sentence `Context` block and then re-audited successfully under the new lifecycle gate

## Recent changes (for traceability, optional)

- 2026-04-01: created `S0E-6C` as the dedicated follow-up for issue-body `Context` sentence count and gate semantics.
- 2026-04-01: fixed the deterministic `Context` sentence contract to `5` lines for main issues and `4` lines for child issues, with one English sentence per bullet row.
- 2026-04-01: wired the same canonical `Context` block into issue draft generation, issue conclusion planning, and lifecycle audit.
- 2026-04-01: revised the renderer and gate so `Context` content must be derived from the current source log instead of repeating one generic repo-wide template.
- 2026-04-01: replayed the real `S0E-5C/#309` conclusion path and re-audited the issue under the new gate.