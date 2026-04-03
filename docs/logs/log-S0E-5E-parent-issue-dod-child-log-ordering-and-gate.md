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
- The ordering rule should stay source-log-owned rather than GitHub-timestamp-owned, because parent issue rendering is derived from repo logs rather than from mutable board views.
- Lifecycle audit should treat parent DoD ordering as a deterministic contract surface, not as cosmetic prose.

## Constraints

- Do not silently reinterpret parent issue ordering from board position, project view order, or manual GitHub drag-and-drop state.
- Do not rely only on issue numbers as the semantic order for parent issue ledgers once a source-log-owned ordering rule exists.
- Do not make the new ordering rule depend on prose parsing from `Decision / Outcome` or `Recent changes`.
- Do not let missing child-log `created` values pass invisibly if the rule is promoted to authoritative contract.

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
- `S0E-5E` is the dedicated place to fix that ordering rule before the parent issue conclusion is replayed again.

## P0 (Parent child-ledger ordering contract | v1)

### P0-C1-S1 (Parent issue DoD ordering source fixed | v1)

- Top-level parent issue child refs should be ordered from source-log facts, not from project view position and not from issue number allocation.
- The primary ordering key should be the child log's `created` field.
- The ordering rule applies only to parent issue child ledgers, not to child issue merged-PR ledgers.

## P1 (Fallback and tie-break chain | v1)

### P1-C1-S1 (Deterministic fallback chain fixed | v1)

- If two child logs share the same `created` value, the first tie-breaker should be the explicit `phase_log_*` order declared by the parent log.
- If child logs still cannot be distinguished after that, the final tie-breaker should be the child issue short ref.
- Missing `created` should be handled explicitly rather than guessed from later evidence blocks or issue timestamps.

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

- `P0-C1-S1`: fix the parent child-ledger ordering contract
- `P1-C1-S1`: fix tie-break and missing-data rules
- `P2-C1-S1`: reuse one shared helper across renderer and conclusion planning
- `P3-C1-S1`: add audit coverage and one replay sample

## Execution Checklist (unchecked)

- [ ] `P0-C1-S1`: parent issue DoD ordering source fixed
- [ ] `P1-C1-S1`: deterministic fallback chain fixed
- [ ] `P2-C1-S1`: renderer and conclusion planner share one ordering helper
- [ ] `P3-C1-S1`: parent DoD ordering drift checked in audit and replayed once

## Evidence (reserved)

- This slice will retain the contract note, implementation file diffs, and one bounded parent replay sample once the ordering rule is implemented.

## Recent changes (for traceability, optional)

- 2026-04-03: created `S0E-5E` to isolate the parent issue `Definition of Done (DoD)` child-ledger ordering problem before replaying the top-level `S0E` parent issue conclusion.
