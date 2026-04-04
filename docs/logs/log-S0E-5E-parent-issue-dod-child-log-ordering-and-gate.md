# log-S0E-5E (Phase 5E: Parent issue DoD child-log ordering and gate)

---

**id**: `S0E-5E`
**kind**: `log`
**title**: `parent issue DoD child-log ordering and gate v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Automation, Contract, Ordering, Gate, epic/s0, sub/0e5e`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/353`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/354`
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
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
**issue_milestone**: `road-002-projection-runtime-platformization-and-evidence-governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: `M5-P2`
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

- The old parent issue helper used issue-number order, but `P2` has already replaced that path with the shared source-log-owned ordering helper.
- `S0E-6F` already made the parent issue body family explicit, so `S0E-5E` has now closed the remaining ordering-semantics gap and verified it through one full live lifecycle.
- `S0E-5E` is now fully closed through the live chain: issue `#353` was created and attached under parent `#248`, PR `#354` was created and merged, and the final issue conclusion body has been written back in place.
- `P0` is now completed: the authoritative ordering source is fixed as child-log `created` ascending, and the rule is now explicitly scoped to top-level parent issue child ledgers rather than child issue merged-PR ledgers.
- `P1` is now completed: the fallback chain is fixed as `created -> phase_log_* declaration order -> child issue short ref`, and missing or invalid `created` is now explicitly classified as a fail-closed contract error rather than a warning-only drift.
- `P2` is now completed: parent issue draft generation and lifecycle audit now call the same shared child-ledger ordering helper, so both surfaces consume the same `created -> phase_log_* -> short ref` rule and fail closed on missing or invalid child-log `created` metadata.
- `P3` is now completed: lifecycle audit exposes parent child-ledger ordering drift as an explicit check, and one bounded parent replay sample for `#248` has been retained.
- The bounded `#248` sample still blocks live parent refresh: audit found stale child-ledger ordering, missing newer child refs in the live parent DoD, and a missing `Roadmap` link row, while the replay preview produced the full source-log-owned child ledger expected by the new contract.

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

- Follow-up work should now be handled as a bounded parent refresh/remediation step rather than by reopening the ordering contract or the child-slice lifecycle.

## Execution Checklist (unchecked)

- [x] `P0-C1-S1`: parent issue DoD ordering source fixed
- [x] `P1-C1-S1`: deterministic fallback chain fixed
- [x] `P2-C1-S1`: renderer and conclusion planner share one ordering helper
- [x] `P3-C1-S1`: parent DoD ordering drift checked in audit and replayed once

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

### P3 (explicit ordering audit surface and bounded parent replay sample | 2026-04-03)

- artifacts:
  - `scripts/issues/plan_lifecycle_audit.py`
  - `docs/issues/lifecycle-audit-S0E-5E-parent-ordering-replay-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-5E-parent-ordering-replay-manifest-plan.json`
  - `docs/issues/issue-S0E-5E-parent-ordering-replay-s0e-parent-body.md`
  - `docs/issues/issue-S0E-5E-parent-ordering-replay-s0e-parent-body.json`
  - `docs/logs/log-S0E-5E-parent-issue-dod-child-log-ordering-and-gate.md`
  - `docs/logs/log-S0E-docs-management-v5.md`
- expected:
  - lifecycle audit should expose parent child-ledger ordering as an explicit deterministic check rather than only an implicit ref comparison
  - one bounded parent replay sample should prove what the parent body now renders under the `created -> phase_log_* -> short ref` ordering rule
  - the first replay should be able to surface stale live parent body drift without broadening the gate to unrelated prose
- observed:
  - `plan_lifecycle_audit.py` now emits `parent-child-dod-ordering` so ordering drift is explicit in parent-side audit results
  - the bounded `#248` audit sample blocked as expected because the live parent issue still carries the older truncated child ledger and is also missing the canonical `Roadmap` link row
  - the bounded replay preview regenerated the parent DoD with the full source-log-owned child ledger in the new deterministic order, proving replay output is stable even though live refresh has not yet been applied

### Full-auto (live issue -> PR -> merge -> conclusion closure | 2026-04-03)

- artifacts:
  - `docs/issues/issue-S0E-5E-parent-issue-dod-child-log-ordering-and-gate.md`
  - `docs/issues/issue-S0E-5E-parent-issue-dod-child-log-ordering-and-gate.json`
  - `docs/issues/issue-relationship-S0E-5E-live-manifest.json`
  - `docs/issues/issue-relationship-S0E-5E-live-manifest-plan.json`
  - `docs/issues/issue-relationship-S0E-5E-live-manifest-parent-248-child-353-apply-result.json`
  - `docs/issues/lifecycle-audit-S0E-5E-live-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-5E-live-manifest-plan.json`
  - `docs/issues/pr-prep-S0E-5E-live-manifest.json`
  - `docs/issues/pr-prep-S0E-5E-live-plan.json`
  - `docs/issues/pr-prep-S0E-5E-live-body.md`
  - `docs/issues/pr-prep-S0E-5E-live-create-body.md`
  - `docs/issues/pr-prep-S0E-5E-live-create-result.json`
  - `docs/issues/pr-prep-S0E-5E-live-post-apply-live-body.md`
  - `docs/issues/pr-prep-S0E-5E-live-post-apply-verify-result.json`
  - `docs/issues/issue-conclusion-S0E-5E-live-manifest.json`
  - `docs/issues/issue-conclusion-S0E-5E-live-plan.json`
  - `docs/issues/issue-conclusion-S0E-5E-live-s0e-5e-body.md`
  - `docs/issues/issue-conclusion-S0E-5E-live-s0e-5e-apply-body.md`
  - `docs/issues/issue-conclusion-S0E-5E-live-s0e-5e-apply-result.json`
  - `docs/logs/log-S0E-5E-parent-issue-dod-child-log-ordering-and-gate.md`
  - `docs/logs/log-S0E-docs-management-v5.md`
- expected:
  - the slice should be able to run through one full live lifecycle without reopening the contract itself
  - the live issue should be created with the deterministic body contract, attached to parent `#248`, carried by one exact-ID PR, and concluded from exact-ID merged PR evidence
  - the final lifecycle audit should pass on the concluded live issue and retain both issue and PR write-back evidence
- observed:
  - live issue `#353` was created from the `S0E-5E` draft, attached to parent `#248`, and passed the issue-created lifecycle audit before PR prep
  - ready PR `#354` was created from the exact `S0E-5E` commit set, passed post-apply live PR body verification, and merged cleanly
  - final issue conclusion was applied in place after merge, and the refreshed live lifecycle audit now passes in `concluded` state with exact-ID merged PR evidence `#354` and matching `links.pr`

## Recent changes (for traceability, optional)

- 2026-04-03: created `S0E-5E` to isolate the parent issue `Definition of Done (DoD)` child-ledger ordering problem before replaying the top-level `S0E` parent issue conclusion.
- 2026-04-03: completed `P0-P1` by fixing the ordering contract to `created -> phase_log_* -> child issue short ref`, and by classifying missing or invalid child-log `created` as a fail-closed parent-ordering error rather than a warning-only drift.
- 2026-04-03: completed `P2` by centralizing parent child-ledger ordering in one shared helper and wiring both issue draft generation and lifecycle audit to the same fail-closed ordering implementation.
- 2026-04-03: completed `P3` by promoting parent child-ledger ordering into an explicit lifecycle-audit check and by retaining one bounded `#248` replay sample that shows the live parent issue is now stale against the new ordering contract.
- 2026-04-03: ran `S0E-5E` through full-auto end to end: created live issue `#353`, attached it under parent `#248`, created and merged PR `#354`, applied the final issue conclusion body, and re-audited the concluded live issue to a pass state.
