# log-S0E-6D (Phase 6D: natural issue Context rendering and weak gate)

---

**id**: `S0E-6D`
**kind**: `log`
**title**: `natural issue Context rendering and weak gate v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Workflow, Automation, Contract, Formatting, epic/s0, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
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
- The gate should stay weak and deterministic: it should require non-placeholder English bullet sentences, a bounded line-count range, and source-log-specific anchors, but it should not require every issue to use the same rhetorical structure.
- Concluded issue rewrites may still replace the full `Context` block when necessary, but the generated text should read like a concise human ledger summary rather than like a repeated system banner.

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

## Success Criteria (DoD)

- Issue `Context` no longer renders as one shared boilerplate block across unrelated issues.
- Draft and conclusion renderers both derive their material from the current source log and adjacent-slice references.
- Lifecycle audit still enforces a bounded deterministic contract, but it no longer requires rigid per-line sentence slots.
- A representative live replay proves the recently audited `S0E` child issues can be rewritten to the new natural-summary style and still pass audit.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` have fixed the natural-summary contract, renderer, weak gate, and representative replay;
  - the Evidence section records the replay and re-audit artifacts for the representative live issue set.

## Current Status

- `S0E-6D` is now opened as the natural-summary follow-up to `S0E-6C`.
- `P0` is now completed: `Context` is treated as a source-log-derived ledger summary instead of as an exact sentence-slot template.
- `P1` is now completed: draft and conclusion renderers now build `Context` from source-log facts, adjacent-slice relation, scope summary, and completion evidence.
- `P2` is now completed: lifecycle audit now enforces a bounded natural-summary contract instead of an exact line-slot contract.
- `P3` is now completed: the recently replayed closed `S0E` child-issue set has been rewritten again under the new rule and re-audited successfully.

## P0 (Natural-summary contract | v1)

### P0-C1-S1 (Natural ledger-summary rule fixed | v1)

- `Context` should read like a concise human ledger summary of the issue's purpose and outcome.
- The text should explain why the issue existed, what boundary it owned, and how it relates to adjacent slices or parent records.
- The contract no longer requires identical rhetorical slots across unrelated issues.

### P0-C1-S2 (Weak deterministic gate fixed | v1)

- The gate still requires English bullet sentences with no placeholders.
- Main issues may use a bounded `4-5` line range, while child issues may use a bounded `3-4` line range.
- The gate requires source-log-specific anchors such as the current log ID and title subject, but it does not require a fixed sentence template.

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

- Lifecycle audit still rejects non-English rows, multi-sentence rows, placeholder drift, and missing source-log anchors.
- The gate now focuses on integrity and issue specificity rather than on rigid prose choreography.

## P3 (Representative live replay | v1)

### P3-C1-S1 (Closed `S0E` child-issue batch replayed | v1)

- The recently audited closed `S0E` child issues were replayed under the new natural-summary renderer.
- The re-audit confirmed that the new Context style remains issue-specific and still passes the bounded gate.

## Execution Checklist (unchecked)

- [x] `P0-C1-S1`: natural ledger-summary rule fixed
- [x] `P0-C1-S2`: weak deterministic gate fixed
- [x] `P1-C1-S1`: draft renderer switched to natural summary
- [x] `P1-C1-S2`: conclusion renderer switched to natural summary
- [x] `P2-C1-S1`: line-range gate fixed
- [x] `P2-C1-S2`: anchor and placeholder gate fixed
- [x] `P3-C1-S1`: representative live replay completed

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

- 2026-04-01: created `S0E-6D` as the follow-up that replaces `S0E-6C`'s rigid Context slotting with a natural-summary renderer and weak gate.
- 2026-04-01: switched issue draft and issue conclusion Context generation to source-log-derived natural summary prose.
- 2026-04-01: relaxed lifecycle audit from exact sentence-count slots to bounded natural-summary integrity checks.
- 2026-04-01: replayed the representative closed `S0E` child-issue batch and re-audited it under the new rule.