# log-S0E-6D (Phase 6D: natural issue Context rendering and weak gate)

---

**id**: `S0E-6D`
**kind**: `log`
**title**: `natural issue Context rendering and weak gate v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Workflow, Automation, Contract, Formatting, epic/s0, sub/1`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/335`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/346`
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md`
  **reference_log_1**: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_3**: `docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md`
  **reference_log_4**: `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
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

- `S0E-6D` exists because `S0E-6C` fixed deterministic `Context` shape, but the renderer still produced text that felt too uniform and too machine-shaped when compared with the more natural historical issue bodies already used in the repo.
- v1 keeps a narrow gate, but it moves the renderer from rigid sentence slots to source-log facts plus natural summary prose.
- The new contract treats `Context` as a hand-kept ledger summary: it should explain why the issue existed, what boundary it owned, how it related to adjacent slices, and what was completed, without forcing every issue into the same wording pattern.

**Default choices (phase defaults / v1)**:

- `Context` should remain English-only and bullet-based, but it no longer needs one fixed sentence template per line.
- Draft rendering and conclusion rendering should both be built from source-log facts, then rendered as natural summary prose rather than as exact sentence-slot templates.
- The gate should stay weak and deterministic: it should require non-placeholder English bullet sentences, a bounded line-count range, and basic sentence completeness, but it should not require fixed rhetorical anchors or one shared prose structure.
- Concluded issue rewrites may still replace the full `Context` block when necessary, but the generated text should read like a concise human ledger summary rather than like a repeated system banner.
- The next revision should narrow the gate even further: prose remains for humans, while provenance and structured verification should stay on the source log, planner artifacts, and apply results rather than on the `Context` prose itself.
- The next renderer revision should move from weak sentence-slot assembly to `fact pool -> style family -> prose rendering`, so similar issues can still stay accurate without sounding like the same template.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Replace the rigid issue `Context` renderer with a natural summary builder driven by source-log facts and adjacent-slice relations.
- Relax the lifecycle gate from exact sentence-count slots to a bounded natural-summary contract that still checks English bullet rows, source-log anchors, and placeholder hygiene.
- Replay the recently audited closed `S0E` child issues so their live bodies reflect the new natural-summary `Context` style instead of the previous uniform template.

**PR checklist source**:

- Default source: reuse this log's execution checklist after the renderer, gate, and representative replay are reviewed.

**PR links**:

- Log: `docs/logs/log-S0E-6D-natural-issue-context-rendering-and-weak-gate.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/lifecycle-audit-S0E-7C-child-issues-context-natural-summary-refresh-manifest-plan.json`

## Constraints

- Do not turn `Context` generation into open-ended freeform summarization without any guardrails.
- Do not keep the exact sentence-slot contract from `S0E-6C` if it forces unrelated issues into visibly identical wording.
- Do not make the gate depend on subjective prose scoring; v1 still needs bounded deterministic checks.
- Do not leave draft and conclusion renderers on different `Context` styles once the new natural-summary rule is introduced.

## Scope

- `P0`: redefine the `Context` contract from rigid sentence slots to source-log-derived natural summary
- `P1`: implement natural-summary draft and conclusion renderers
- `P2`: replace the exact-count gate with a bounded weak gate for natural summary
- `P3`: replay representative live concluded issues under the new rule and re-audit them
- `P4`: replace template-shaped natural-summary rendering with fact-pool selection, style-family variation, and prose-first weak gate narrowing

## Success Criteria (DoD)

- Issue `Context` no longer renders as one shared boilerplate block across unrelated issues.
- Draft and conclusion renderers both derive their material from the current source log and adjacent-slice references.
- Lifecycle audit still enforces a bounded deterministic contract, but it no longer requires rigid per-line sentence slots.
- A representative live replay proves the recently audited `S0E` child issues can be rewritten to the new natural-summary style and still pass audit.
- The next renderer revision no longer relies on fixed opening / relation / scope / completion sentence slots, and similar issues may vary lightly in ordering and tone while still staying faithful to the source log.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P4` have fixed the natural-summary contract, renderer, weak gate, prose-first gate narrowing, and representative replay;
  - the Evidence section records the replay and re-audit artifacts for the representative live issue set.

## Current Status

- `S0E-6D` is now opened as the natural-summary follow-up to `S0E-6C`.
- `P0` is now completed: `Context` is treated as a source-log-derived ledger summary instead of as an exact sentence-slot template.
- `P1` is now completed: draft and conclusion renderers now build `Context` from source-log facts, adjacent-slice relation, scope summary, and completion evidence.
- `P2` is now completed: lifecycle audit now enforces a bounded natural-summary contract instead of an exact line-slot contract.
- `P3` is now completed: the recently replayed closed `S0E` child-issue set has been rewritten again under the new rule and re-audited successfully.
- `P4-C1-S1` is now completed: the `Context` gate has been narrowed to prose-first checks only, so lifecycle audit now enforces line count, readable English sentence rows, and placeholder hygiene without requiring hard prose anchors.
- `P4-C1-S2` is now completed: the renderer now selects from a source-log fact pool and renders through deterministic style families instead of forcing one shared `opening -> relation -> scope -> completion` sentence order.
- `P4-C1-S3` is now completed: the representative closed child-issue replay has been refreshed under the new fact-pool/style-family renderer, and the live replay still passes lifecycle audit under the prose-first gate.

## P0 (Natural-summary contract | v1)

### P0-C1-S1 (Natural ledger-summary rule fixed | v1)

- `Context` should read like a concise human ledger summary of the issue's purpose and outcome.
- The text should explain why the issue existed, what boundary it owned, and how it relates to adjacent slices or parent records.
- The contract no longer requires identical rhetorical slots across unrelated issues.

### P0-C1-S2 (Weak deterministic gate fixed | v1)

- The gate still requires English bullet sentences with no placeholders.
- Main issues may use a bounded `4-5` line range, while child issues may use a bounded `3-4` line range.
- The gate requires only readable English bullet sentences, placeholder hygiene, and bounded line count; provenance remains on the source log and retained artifacts rather than in hard-coded prose anchors.

## P1 (Renderer implementation | v1)

### P1-C1-S1 (Draft renderer switched to natural summary | v1)

- Draft `Context` now combines an opening sentence, an adjacent-slice relation sentence, a source-log scope sentence, and one supporting line drawn from source-log facts.
- The rendered text is still deterministic enough for replay, but it is no longer tied to one repo-wide wording block.

### P1-C1-S2 (Conclusion renderer switched to natural summary | v1)

- Conclusion `Context` now combines the same source-log opening and relation with a merged-PR evidence sentence and a finished-path ledger sentence.
- This keeps conclusion bodies aligned with the actual slice while still making the completed state explicit.

## P2 (Weak gate | v1)

### P2-C1-S1 (Line-range gate fixed | v1)

- Lifecycle audit now checks bounded line-count ranges instead of exact sentence counts.
- This keeps the gate deterministic without forcing every issue into the same exact shape.

### P2-C1-S2 (Anchor and placeholder gate fixed | v1)

- Lifecycle audit still rejects non-English rows, multi-sentence rows, and placeholder drift.
- The gate now focuses on prose integrity and readability rather than on hard-coded rhetorical anchors inside the rendered `Context` text.

## P3 (Representative live replay | v1)

### P3-C1-S1 (Closed `S0E` child-issue batch replayed | v1)

- The recently audited closed `S0E` child issues were replayed under the new natural-summary renderer.
- The re-audit confirmed that the new Context style remains issue-specific and still passes the bounded gate.

## P4 (Prose-first gate narrowing and fact-pool renderer | v1)

### P4-C1-S1 (Prose-first weak gate narrowed | v1)

- `Context` gate should only require `3-5` readable English bullet sentences, placeholder hygiene, and basic sentence completeness.
- Provenance and machine-readable verification should stay on the source log, planner outputs, and apply/audit artifacts rather than being forced back into the `Context` prose.
- Lifecycle audit should stop checking for fixed rhetorical slots or hard prose anchors inside the rendered `Context` text.

### P4-C1-S2 (Fact-pool selection and style-family rendering introduced | v1)

- The renderer should first extract a fact pool from source-log sections such as `Decision / Outcome`, `Scope`, `Current Status`, `Success Criteria`, `previous_log`, and merged-PR evidence.
- The renderer should then select `3-5` facts under minimal coverage rules instead of forcing one fixed `opening -> relation -> scope -> completion` sentence order.
- The final prose should be rendered through a small style family such as `ledger-first`, `follow-up-first`, `boundary-first`, or `outcome-first`, with deterministic per-issue variation so similar issues do not all read the same.

### P4-C1-S3 (Representative replay refreshed under the prose-first rule | v1)

- After the renderer and gate are revised, the representative closed `S0E` child-issue batch should be replayed again.
- The follow-up audit should prove that the new prose-first contract still passes mechanically while reading closer to manual ledger notes than to template output.

## Execution Checklist (unchecked)

- [x] `P0-C1-S1`: natural ledger-summary rule fixed
- [x] `P0-C1-S2`: weak deterministic gate fixed
- [x] `P1-C1-S1`: draft renderer switched to natural summary
- [x] `P1-C1-S2`: conclusion renderer switched to natural summary
- [x] `P2-C1-S1`: line-range gate fixed
- [x] `P2-C1-S2`: anchor and placeholder gate fixed
- [x] `P3-C1-S1`: representative live replay completed
- [x] `P4-C1-S1`: prose-first weak gate narrowed
- [x] `P4-C1-S2`: fact-pool selection and style-family rendering introduced
- [x] `P4-C1-S3`: representative replay refreshed under the prose-first rule

### P4-C1-S1 (prose-first weak gate narrowed | 2026-04-01)

- headSha: `5a4ff04d`
- artifacts:
  - `scripts/issues/body_contract.py`
  - `scripts/issues/plan_issue_conclusion.py`
  - `scripts/issues/plan_lifecycle_audit.py`
  - `docs/logs/log-S0E-6D-natural-issue-context-rendering-and-weak-gate.md`
  - `docs/issues/lifecycle-audit-S0E-7C-child-issues-context-natural-summary-refresh-manifest-plan.json`
- expected:
  - lifecycle audit should reduce `Context` validation to line count, readable English sentence rows, and placeholder hygiene instead of enforcing hard prose anchors inside the rendered text
- observed:
  - the `Context` gate now accepts prose-first variation as long as the block stays within `3-5` rows, remains readable in English, and contains no placeholder scaffolding; the representative lifecycle audit replay still returns no blocked or fail findings under the narrowed gate

### P4-C1-S2 (fact-pool selection and style-family rendering introduced | 2026-04-01)

- headSha: `f554bb78`
- artifacts:
  - `scripts/issues/body_contract.py`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-natural-summary-refresh-plan.json`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-natural-summary-refresh-s0e-2a-body.md`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-natural-summary-refresh-s0e-4d-body.md`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-natural-summary-refresh-s0e-5c-body.md`
  - `docs/logs/log-S0E-6D-natural-issue-context-rendering-and-weak-gate.md`
- expected:
  - the renderer should stop assembling `Context` through one shared sentence-slot skeleton and instead build issue summaries from a source-log fact pool plus deterministic style-family variation
- observed:
  - regenerated preview bodies now vary in sentence ordering and lead sentence choice by issue, while still staying inside the same bounded prose-first gate and remaining traceable to source-log facts

### P4-C1-S3 (representative replay refreshed under the prose-first rule | 2026-04-01)

- headSha: `5f2eca80`
- artifacts:
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-fact-pool-refresh-manifest.json`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-fact-pool-refresh-plan.json`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-fact-pool-refresh-item0-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-fact-pool-refresh-item1-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-fact-pool-refresh-item2-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-fact-pool-refresh-item3-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-fact-pool-refresh-item4-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-fact-pool-refresh-item5-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-fact-pool-refresh-item6-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-fact-pool-refresh-item7-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-fact-pool-refresh-item8-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-fact-pool-refresh-item9-apply-result.json`
  - `docs/issues/lifecycle-audit-S0E-7C-child-issues-context-fact-pool-refresh-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-7C-child-issues-context-fact-pool-refresh-manifest-plan.json`
- expected:
  - the fact-pool/style-family renderer should be proven on the same representative closed `S0E` child-issue batch in live GitHub, with the replay remaining inside the prose-first `3-4` child-line gate
- observed:
  - all ten closed child issues were rewritten in place under the fact-pool/style-family renderer, each apply returned `result: ok`, and the follow-up lifecycle audit returned `pass` across the full batch with the prose-first Context gate still satisfied

## Evidence (reserved)

### P0-P3 (natural-summary Context contract, renderer, weak gate, and replay | 2026-04-01)

- headSha: `fb3c6022`
- artifacts:
  - `scripts/issues/body_contract.py`
  - `scripts/issues/gen_issue_draft.py`
  - `scripts/issues/plan_issue_conclusion.py`
  - `scripts/issues/plan_lifecycle_audit.py`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-natural-summary-refresh-manifest.json`
  - `docs/issues/issue-conclusion-S0E-7C-child-issues-context-natural-summary-refresh-plan.json`
  - `docs/issues/lifecycle-audit-S0E-7C-child-issues-context-natural-summary-refresh-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-7C-child-issues-context-natural-summary-refresh-manifest-plan.json`
- expected:
  - the repo should replace the rigid Context template with a source-log-derived natural-summary renderer and then prove the revised gate on the representative closed `S0E` child-issue batch
- observed:
  - the renderer now produces issue-specific natural ledger summaries, the gate now enforces bounded natural-summary integrity instead of exact slots, and the representative closed `S0E` child-issue batch was replayed and re-audited successfully

## Recent changes (for traceability, optional)

- 2026-04-03: wrote back live issue `#335`, merged PR `#346`, applied the final issue-conclusion body, and confirmed the live issue is closed.
- 2026-04-01: created `S0E-6D` as the follow-up that replaces `S0E-6C`'s rigid Context slotting with a natural-summary renderer and weak gate.
- 2026-04-01: switched issue draft and issue conclusion Context generation to source-log-derived natural summary prose.
- 2026-04-01: relaxed lifecycle audit from exact sentence-count slots to bounded natural-summary integrity checks.
- 2026-04-01: replayed the representative closed `S0E` child-issue batch and re-audited it under the new rule.
- 2026-04-01: reopened `S0E-6D` with `P4` after operator review confirmed that the current renderer still reads too template-shaped for a human-facing `Context` block.
- 2026-04-01: completed `P4-C1-S1` by narrowing the `Context` gate to prose-first checks only, removing hard prose-anchor validation from lifecycle audit.
- 2026-04-01: completed `P4-C1-S2` by replacing sentence-slot assembly with a source-log fact pool and deterministic style-family rendering for issue Context previews.
- 2026-04-01: completed `P4-C1-S3` by replaying the representative closed `S0E` child-issue batch under the fact-pool/style-family renderer and re-auditing the live issues with `10/10 pass` under the prose-first gate.