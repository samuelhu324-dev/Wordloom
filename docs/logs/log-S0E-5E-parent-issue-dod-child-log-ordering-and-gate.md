# log-S0E-5E (Phase 5E: Parent issue DoD child-log ordering and gate)

---

**id**: `S0E-5E`
**kind**: `log`
**title**: `parent issue DoD child-log ordering and gate v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Automation, Contract, Ordering, Gate, epic/s0, sub/0e5e`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-6F-issue-body-metadata-links-boundary-follow-up.md`
  **reference_log_1**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  **reference_log_3**: `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  **reference_log_4**: `docs/logs/log-S0E-6F-issue-body-metadata-links-boundary-follow-up.md`
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
**created**: `2026-04-03`
**updated**: `2026-04-03`

---

## Decision / Outcome

**Decision**:

- `S0E-5E` exists to fix one unresolved ordering question in the parent-issue conclusion contract: the top-level parent `Definition of Done (DoD)` child-issue ledger should not keep inheriting issue-number order when the intended reading order is the child log creation sequence.
- This slice is intentionally narrower than `S0E-6F`: `6F` fixed which fields belong in `Metadata`, `Links`, and the parent-aware body family, while `5E` fixes the ordering rule for the parent issue's child ledger and the gate that should protect it.
- The goal is to make parent issue conclusion output deterministic, explainable, and replayable from source logs without relying on whichever GitHub issue number happened to be allocated first.

**Default choices (phase defaults / v1)**:

- The parent issue `Definition of Done (DoD)` child ledger should be ordered by the referenced child log's `created` field in ascending order.
- If multiple child logs share the same `created` value, the first tie-breaker should be the parent log's explicit `phase_log_*` declaration order; the final tie-breaker should be the child issue short ref.
- If any child log participating in the parent ledger is missing a valid `created` value, that item should become a fail-closed contract error for parent-ledger rendering and audit rather than silently falling back to issue-number order.
- The ordering rule should stay source-log-owned rather than GitHub-timestamp-owned, because parent issue rendering is derived from repo logs rather than from mutable board views.
- Lifecycle audit should treat parent DoD ordering as a deterministic contract surface, not as cosmetic prose.

## Constraints

- Do not silently reinterpret parent issue ordering from board position, project view order, or manual GitHub drag-and-drop state.
- Do not rely only on issue numbers as the semantic order for parent issue ledgers once a source-log-owned ordering rule exists.
- Do not make the new ordering rule depend on prose parsing from `Decision / Outcome` or `Recent changes`.
- Do not let missing child-log `created` values pass invisibly if the rule is promoted to authoritative contract.
- Do not silently downgrade missing or invalid child-log `created` metadata into a warning-only condition once parent-ledger ordering is declared deterministic.

## Scope

- `P0`: define the canonical ordering contract for top-level parent issue child ledgers
- `P1`: decide the deterministic fallback chain when child-log `created` values tie or are missing
- `P2`: update parent issue rendering and conclusion planning to reuse the same ordering helper
- `P3`: extend lifecycle audit so parent DoD ordering drift is caught explicitly

## Success Criteria (DoD)

- The repo has one explicit rule for ordering top-level parent issue child refs in `Definition of Done (DoD)`.
- Parent issue draft generation, parent issue refresh, and lifecycle audit all reuse the same ordering source instead of each choosing their own sort.
- The rule clearly distinguishes primary key, tie-breakers, and missing-data behavior.
- A parent issue replay sample proves the resulting child ledger is stable across regeneration.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Fix the parent issue `Definition of Done (DoD)` child ledger to sort by child log `created` order instead of defaulting to issue-number order.
- Define one deterministic fallback chain for equal or missing child-log dates so replay remains stable.
- Add a bounded parent-body gate check so conclusion refreshes cannot silently drift back to a different child ordering.

**PR checklist source**:

- Default source: reuse this log's checked execution checklist once the ordering rule, renderer reuse, and lifecycle audit check all verify cleanly.

**PR links**:

- Log: `docs/logs/log-S0E-5E-parent-issue-dod-child-log-ordering-and-gate.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`

## Current Status

- The current parent issue helper still collects child issue refs and then sorts them by issue number, which is deterministic but not aligned to the child log creation sequence.
- `S0E-6F` already made the parent issue body family explicit, so the remaining gap is no longer field ownership; it is ordering semantics.
- The ordering question is now important because `S0E-docs-management-v5/#248` is close to needing a fresh parent conclusion body, and the current child ledger order will look arbitrary if replay keeps following issue number allocation.
- `P0` is now completed: the authoritative ordering source is fixed as child-log `created` ascending, and the rule is now explicitly scoped to top-level parent issue child ledgers rather than child issue merged-PR ledgers.
- `P1` is now completed: the fallback chain is fixed as `created -> phase_log_* declaration order -> child issue short ref`, and missing or invalid `created` is now explicitly classified as a fail-closed contract error rather than a warning-only drift.
- `P2` is now completed: parent issue draft generation and lifecycle audit now call the same shared child-ledger ordering helper, so both surfaces consume the same `created -> phase_log_* -> short ref` rule and fail closed on missing or invalid child-log `created` metadata.
- `S0E-5E` now moves to bounded audit/replay work under `P3` before the parent issue conclusion is replayed again.

## P0 (Parent child-ledger ordering contract | v1)

### P0-C1-S1 (Parent issue DoD ordering source fixed | v1)

- Top-level parent issue child refs should be ordered from source-log facts, not from project view position and not from issue number allocation.
- The primary ordering key is the child log's frontmatter `created` field parsed as the canonical repo-side creation date for that child slice.
- The ordering rule applies only to parent issue child ledgers, not to child issue merged-PR ledgers.
- Issue number order is no longer considered semantic order for parent DoD ledgers; it is only an implementation-detail fallback of the old helper that this slice replaces.

## P1 (Fallback and tie-break chain | v1)

### P1-C1-S1 (Deterministic fallback chain fixed | v1)

- If two child logs share the same `created` value, the first tie-breaker should be the explicit `phase_log_*` order declared by the parent log.
- If child logs still cannot be distinguished after that, the final tie-breaker should be the child issue short ref.
- Neither GitHub issue timestamps nor board order are valid tie-break inputs for this rule.

### P1-C1-S2 (Missing `created` becomes a fail-closed contract error | v1)

- A child log included in the parent ledger must carry a valid frontmatter `created` value if parent-ledger ordering is being rendered or audited under this contract.
- Missing or invalid `created` is a strong-structure failure for parent issue ordering and should stop deterministic parent-ledger rendering rather than degrading to warning-only output.
- Parent issue draft generation, parent issue refresh, and lifecycle audit should all surface the same fail-closed outcome for that case so operators repair the child log metadata instead of accepting guessed order.

## P2 (Renderer and planner reuse | v1)

### P2-C1-S1 (Parent renderer and conclusion planner share one ordering helper | v1)

- Parent issue draft generation and any later parent issue refresh path should consume one shared child-ledger ordering helper.
- The helper should read child log metadata once and emit one stable ordered short-ref ledger.
- The parent issue conclusion path must not keep a second private ordering rule.

## P3 (Gate and replay sample | v1)

### P3-C1-S1 (Parent DoD ordering drift becomes an explicit audit surface | v1)

- Lifecycle audit should expose parent child-ledger ordering drift as a deterministic contract check.
- The first rollout only needs one bounded parent replay sample under `S0E` to prove regeneration stays stable.
- The gate should validate ordering, not broader prose around the parent issue body.

## Plan (draft)

- `P3-C1-S1`: add audit coverage and one replay sample

## Execution Checklist (unchecked)

- [x] `P0-C1-S1`: parent issue DoD ordering source fixed
- [x] `P1-C1-S1`: deterministic fallback chain fixed
- [x] `P2-C1-S1`: renderer and conclusion planner share one ordering helper
- [ ] `P3-C1-S1`: parent DoD ordering drift checked in audit and replayed once

## Evidence (reserved)

- This slice will retain the contract note, implementation file diffs, and one bounded parent replay sample once the ordering rule is implemented.

### P0-P1 (ordering source and fail-closed fallback chain fixed | 2026-04-03)

- artifacts:
  - `docs/logs/log-S0E-5E-parent-issue-dod-child-log-ordering-and-gate.md`
  - `docs/logs/log-S0E-docs-management-v5.md`
  - `docs/issues/issue-S0E-5E-parent-issue-dod-child-log-ordering-and-gate.md`
  - `docs/issues/issue-S0E-5E-parent-issue-dod-child-log-ordering-and-gate.json`
- expected:
  - parent issue child-ledger ordering should stop using issue-number order as the semantic default
  - the contract should fix one tie-break chain for equal dates and one explicit outcome for missing dates before implementation starts
- observed:
  - the contract now fixes parent DoD ordering as child-log `created` ascending, then parent `phase_log_*` declaration order, then child issue short ref
  - missing or invalid child-log `created` is now explicitly classified as a fail-closed strong-structure error for parent-ledger rendering and audit

### P2 (shared ordering helper wired into renderer and planner | 2026-04-03)

- artifacts:
  - `scripts/issues/body_contract.py`
  - `scripts/issues/gen_issue_draft.py`
  - `scripts/issues/plan_lifecycle_audit.py`
  - `docs/logs/log-S0E-5E-parent-issue-dod-child-log-ordering-and-gate.md`
  - `docs/logs/log-S0E-docs-management-v5.md`
- expected:
  - parent issue draft generation and lifecycle audit should stop carrying separate child-ledger sort implementations
  - both surfaces should reuse one helper that orders child issue refs by `created -> phase_log_* declaration order -> short ref`
  - missing or invalid child-log `created` should now fail closed from the shared helper instead of leaving one caller to drift independently
- observed:
  - `ordered_parent_child_issue_refs(...)` now centralizes the parent child-ledger ordering rule in `body_contract.py`
  - `gen_issue_draft.py` and `plan_lifecycle_audit.py` now both consume the same helper rather than reimplementing issue-number sort locally
  - the shared helper now raises a deterministic stop if a participating child log lacks valid `YYYY-MM-DD` `created` metadata

## Recent changes (for traceability, optional)

- 2026-04-03: created `S0E-5E` to isolate the parent issue `Definition of Done (DoD)` child-ledger ordering problem before replaying the top-level `S0E` parent issue conclusion.
- 2026-04-03: completed `P0-P1` by fixing the ordering contract to `created -> phase_log_* -> child issue short ref`, and by classifying missing or invalid child-log `created` as a fail-closed parent-ordering error rather than a warning-only drift.
- 2026-04-03: completed `P2` by centralizing parent child-ledger ordering in one shared helper and wiring both issue draft generation and lifecycle audit to the same fail-closed ordering implementation.
