# log-S0F-1C (Phase 1C: guarded multi-item live mutation remediation)

---

**id**: `S0F-1C`
**kind**: `log`
**title**: `guarded multi-item live mutation remediation v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Automation, Drills, Evidence, epic/s0, sub/1c`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`
  **reference_log_1**: `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
  **reference_log_2**: `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`
  **reference_log_3**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_4**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_5**: `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
  **reference_log_6**: `docs/logs/log-S0E-7E-publish-verify-remediation-gate-thin-orchestration-entrypoint.md`
**issue_keyword**: `automation`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-04`
**updated**: `2026-04-04`

---

## Decision / Outcome

**Decision**:

- `S0F-1C` is the next follow-up slice under `S0F`, and it turns the already-proven single-item guarded mutation model into a manifest-driven multi-item remediation workflow.
- v1 should not reopen the old raw-apply surfaces just because the target set becomes larger; batch or multi-item operation must still remain wrapper-owned, pre-gated, and fail-closed.
- The first target is deliberately narrow: historical issue-conclusion Context refresh is the proving ground, but the contract should be written so the same batch discipline can later cover other issue / PR live mutation families.

**Default choices (phase defaults / v1)** (optional, but recommended):

- Multi-item work must begin with preview planning, not live apply.
- A batch manifest may describe multiple targets, but each target must still preserve exact source-log grounding, explicit merged-PR evidence, and family-specific eligibility checks.
- Guarded remediation remains the only operator-facing live mutation path for already-closed issues or equivalent historical refreshes.
- `preserve-existing` post-verify is mandatory after any live refresh batch so drift can be measured against the live body that was just written.
- Batch throughput is not a reason to weaken sentence-count, placeholder-hygiene, or ownership checks.
- If one target needs special handling, the batch must stop or split; v1 does not permit a soft fallback that silently downgrades one item while the rest continue.
- The first batch sample should stay small and representative so retained artifacts remain reviewable by hand.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.

**PR summary bullets**:

- Define a manifest-driven batch remediation contract for guarded multi-item live mutation work.
- Keep preview, guarded apply, and preserve-existing post-verify as three separate owned stages instead of collapsing them into one replay command.
- Require per-target evidence retention so multi-item runs do not hide which item drifted, stopped, or needed remediation.
- Use historical issue-conclusion Context refresh as the first representative sample without reopening raw mutation entrypoints.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.
- If the implementation work lands in multiple review units, keep each PR scoped to the exact `P*-C*-S*` unit.

**PR links**:

- Log: `docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md`
- Runbook: ``
- Evidence artifact: ``

## Definitions (optional)

- `multi-item remediation`: a workflow that refreshes or repairs more than one live target under one manifest while still preserving per-target gate and evidence outputs.
- `guarded batch`: a batch surface that may orchestrate several items, but only by delegating each real mutation through the family-owned guarded apply path.
- `post-refresh preserve-existing verify`: a non-mutating verification run that confirms the freshly written live body still satisfies the canonical contract when preserved as-is.

## Constraints

- Do not turn batch support into a justification for reintroducing raw apply entrypoints as operator defaults.
- Do not treat aggregate success as sufficient evidence; each target still needs traceable per-item outputs.
- Do not allow batch tooling to hide semantic failures behind retry language meant for transient execution problems.
- Do not broaden the first rollout beyond a reviewable representative set.

## Scope

- `P0`: define the guarded multi-item remediation contract and wire `S0F-1C` into the `S0F` spine
- `P1`: preview-only batch planning contract for representative historical targets
- `P2`: guarded live apply contract for multi-item historical refresh
- `P3`: preserve-existing post-verify and drift-report contract after live refresh
- `P4`: operator runbook and representative retained sample for repeatable batch remediation

## Success Criteria (DoD)

- Multi-item historical refresh can be described through one manifest without losing per-target gate ownership or evidence traceability.
- No batch path can bypass the existing guarded family apply surfaces.
- Post-refresh verification can distinguish a clean preserved live body from a drifted or malformed one on a per-target basis.
- Operators can tell from retained artifacts which stage stopped: preview planning, guarded apply, or preserve-existing re-verify.
- The first representative batch sample remains small enough for hand review while still proving the contract is reusable.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the batch contract is implemented without reopening raw mutation entrypoints;
  - at least one representative multi-item remediation sample retains preview, guarded apply, and preserve-existing post-verify artifacts;
  - failure semantics remain per-target and fail-closed rather than aggregate-only.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-1C/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit.

**Branch convention**:

- `S0F-1C` related changes should stay on `S0F-*` working branches, currently `S0F-docs-management-v6`.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, commit and push promptly on `S0F-docs-management-v6` so the new spine does not drift ahead of origin.

## Plan (draft)

### P0 (Contract and spine wiring)

- P0-C1-S1: create `S0F-1C` and wire it into the `S0F` parent spine as the next follow-up slice
- P0-C1-S2: define the batch-stage vocabulary covering preview, guarded apply, and preserve-existing post-verify

### P1 (Preview planning)

- P1-C1-S1: define the representative multi-item manifest shape for historical refresh targets
- P1-C1-S2: retain a preview-only sample proving multiple targets can be planned without live mutation

### P2 (Guarded apply)

- P2-C1-S1: define the per-target eligibility and remediation handoff rules for multi-item guarded apply
- P2-C1-S2: retain a live sample proving multi-item refresh still routes through family-owned guarded surfaces

### P3 (Post-refresh verification)

- P3-C1-S1: define preserve-existing post-verify as the mandatory follow-up stage after batch live refresh
- P3-C1-S2: retain a sample drift report that shows clean preserve versus stop-worthy drift at per-target granularity

### P4 (Operator repeatability)

- P4-C1-S1: publish a small-scope runbook for repeatable historical refresh batches without reopening raw apply entrypoints

## Execution Checklist (unchecked)

### P0 (Contract and spine wiring)

- [x] `P0-C1-S1`: `S0F-1C` created and wired into the `S0F` parent spine
- [ ] `P0-C1-S2`: batch-stage vocabulary fixed for preview, guarded apply, and preserve-existing post-verify

### P1 (Preview planning)

- [ ] `P1-C1-S1`: representative multi-item manifest shape fixed
- [ ] `P1-C1-S2`: preview-only multi-item sample retained

### P2 (Guarded apply)

- [ ] `P2-C1-S1`: per-target eligibility and remediation handoff rules fixed
- [ ] `P2-C1-S2`: representative guarded multi-item live sample retained

### P3 (Post-refresh verification)

- [ ] `P3-C1-S1`: preserve-existing post-verify fixed as mandatory batch follow-up
- [ ] `P3-C1-S2`: representative per-target drift report retained

### P4 (Operator repeatability)

- [ ] `P4-C1-S1`: repeatable operator runbook retained

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1 (child log created and parent wired | 2026-04-04)

- artifacts:
  - `docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - `S0F-1C` should exist as the next `S0F` child slice with a clear handoff from the single-item `S0F-1B` proof to multi-item guarded remediation
  - the `S0F` parent spine should point to the new child log and describe its role briefly enough that later phase work can be located without reopening branch archaeology
- observed:
  - `S0F-1C` now exists as a draft child log with explicit `P0-P4` scope for preview planning, guarded multi-item live apply, preserve-existing post-verify, and operator repeatability
  - the `S0F` parent spine now points `phase_log_3` at this child slice and records it as the next follow-up after the `S0F-1B` historical refresh proof set