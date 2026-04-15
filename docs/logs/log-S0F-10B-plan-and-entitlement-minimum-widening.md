# log-S0F-10B (Phase 10B: Plan and entitlement minimum widening)

---

**id**: `S0F-10B`
**kind**: `log`
**title**: `plan and entitlement minimum widening boundary after book-first access closure v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Access, Entitlement, Policy, Drills, Evidence, epic/s0, sub/10b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md`
  **reference_log_1**: `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md`
  **reference_log_2**: `docs/roadmap/_draft/road-S2-.md`
**issue_keyword**: `policy`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/10b`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M4`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-15`
**updated**: `2026-04-15`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this lane.
- Day-level precision is acceptable while this widening packet is still a policy-and-boundary scaffold.
- `reviewed` should remain `pending` until this lane is accepted as the next bounded `M4` widening packet after `S0F-10A`.

## Decision / Outcome

**Decision**:

- `S0F-10B` opens the next `M4` child lane as a bounded widening packet for `plan` and `entitlement` after the book-first minimum closure is already stable.
- The purpose of this lane is not to replace the `S0F-10A` role boundary; it is to decide which capabilities remain role-driven and which capabilities should later be granted or denied through entitlement semantics layered on top of that baseline.
- `mock billing` remains out of scope for this opening packet unless a later phase proves that subscription-state change is required to replay entitlement outcomes coherently.

**Default choices (phase defaults / v1)**:

- `S0F-10A` remains the stable access baseline and must not be rewritten by this widening packet.
- `plan` is a commercial packaging concept, not a substitute for `book_role` or `system_role`.
- `entitlement` is a capability-layer concept that may refine allowed actions after role checks, but it must not collapse ordinary collaboration roles into pricing tiers.
- `system_admin` remains a platform override concept and must not become a paid-plan alias.
- If a capability question can already be answered by `viewer / editor / owner / system_admin`, do not force it into `plan / entitlement` just to make the second lane look larger.

## PR Summary Inputs (optional)

- Use this block because `S0F-10B` is intended to become the next bounded `M4` widening packet after `S0F-10A`.

**PR summary bullets**:

- Open the next `M4` child lane for minimum `plan / entitlement` widening after the book-first access baseline is already stable.
- Fix the boundary between role-granted actions and entitlement-granted capabilities without introducing payment-provider or invoice realism.
- Keep `mock billing` explicitly deferred unless later phases prove that subscription-state change is required for replayable entitlement behavior.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
- Previous log: `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md`

## Exported Sections / Outlet Ownership

- This slice starts as one `log-retained core + entitlement-boundary contract-first` lane.
- The expected first landing is one stable contract that answers how `plan`, `entitlement`, and later `subscription_state` relate to the already-stable role baseline from `S0F-10A`.

**Outlet ownership**:

- `contract`: define `plan`, `entitlement`, `subscription_state`, and the layering rule between role checks and entitlement checks
- `runbook`: no-op at packet open; operator procedure should wait until the first entitlement replay drill exists
- `view`: no-op at packet open; reader-facing entitlement summaries should wait until the first action split is explicit
- `index/front-door`: no-op at packet open
- `disposition/placement`: no-op at packet open
- `log-retained core`: lane boundary, widening rules, phase plan, execution checklist, and later evidence ledger remain here

## Definitions

- `plan`: one commercial packaging label such as trial, standard, or vip that may later influence capability policy.
- `entitlement`: one executable capability grant or deny outcome that may later refine behavior after role checks.
- `subscription_state`: one later lifecycle state such as trialing, active, past_due, canceled, or expired.
- `role-granted action`: one action already decided by the stable role matrix from `S0F-10A`.
- `entitlement-granted capability`: one later capability question that cannot be defended by role semantics alone.
- `widening packet`: one bounded second-stage lane that layers new policy on top of a stable earlier packet instead of rewriting the earlier packet's boundary.

## Constraints

- Do not rewrite the `book`-first access baseline already fixed in `S0F-10A`.
- Do not treat paid plan level as a synonym for ordinary collaboration authority.
- Do not introduce real payment provider, tax, invoice, or enterprise-procurement realism in this opening packet.
- Do not reopen block-level ACL or monetized block-level gating unless a later drill proves book-level standing is insufficient.
- Do not ask `system_admin` to carry commercial-plan semantics.

## Scope

- `P0`: contract
- `P1`: action split and entitlement surface mapping
- `P2`: drill and replay
- `P3`: billing handoff decision

## Success Criteria (DoD)

- The lane fixes one minimum vocabulary for `plan`, `entitlement`, and later `subscription_state` without collapsing them into roles.
- The lane explains which actions stay governed only by `S0F-10A` role semantics and which questions deserve a later entitlement layer.
- The lane names at least one bounded entitlement surface that can be discussed without reopening block-level ACL.
- The lane keeps `mock billing` explicitly separate unless a replay drill proves it is necessary.
- The lane leaves one reader able to explain how later commercialization can widen from `S0F-10A` without rewriting that baseline.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the minimum `plan / entitlement` vocabulary and layering rules are explicit
  - at least one action split between role and entitlement semantics is explicit
  - at least one replayable entitlement drill exists without requiring real payment integration
  - the Evidence section includes traceable `headSha` values plus artifact paths
- `stable` for this widening packet does not require real billing integration; it requires a bounded and replayable entitlement boundary that preserves `S0F-10A` as the access baseline.

## P0 (Contract | v1)

### P0-C1-S1 (Plan and entitlement vocabulary)

- Fix one minimum vocabulary for `plan`, `entitlement`, and later `subscription_state`.
- Keep commercial packaging, executable capability policy, and lifecycle state as distinct concepts.

### P0 Minimum Vocabulary Decision (v1)

- `P0` is now fixed as one vocabulary-and-layering packet for second-stage capability policy after the `S0F-10A` access baseline.
- The minimum terms in this packet are now fixed as:
  - `plan`
  - `entitlement`
  - `subscription_state`
- The semantic boundary for those terms is now fixed as follows:
  - `plan` means one commercial packaging label that selects or constrains a default capability bundle; it does not grant ordinary collaboration authority by itself
  - `entitlement` means one executable capability grant or deny outcome that is evaluated only for questions the role matrix cannot already answer cleanly
  - `subscription_state` means one lifecycle state that may later activate, suspend, or expire entitlement outcomes; it does not replace `book_role` or `system_role`
- The minimum illustrative values in this packet are now fixed as:
  - `plan`: `trial`, `standard`, `vip`
  - `subscription_state`: `trialing`, `active`, `past_due`, `canceled`, `expired`
- The `P0-C1-S1` success rule in this packet is:
  - one reader should be able to distinguish packaging, capability, and lifecycle state without treating them as aliases
  - one reader should be able to explain why ordinary collaboration authority still comes from `viewer / editor / owner / system_admin`
  - later commercialization should have to add capability policy through `entitlement`, not by rewriting role names

#### P0 Vocabulary Table (v1)

| term | fixed meaning in `S0F-10B` | not allowed to mean |
| --- | --- | --- |
| `plan` | one commercial packaging label that selects a default capability bundle | ordinary collaboration authority, ownership, or platform override standing |
| `entitlement` | one executable capability grant or deny outcome layered after role checks | a replacement for the role matrix or a hidden billing record |
| `subscription_state` | one later lifecycle state that may change whether an entitlement bundle is active | a direct alias for role, plan, or payment-event history |

### P0-C1-S2 (Layering rule over the book-first baseline)

- `S0F-10A` remains the first access baseline.
- `plan / entitlement` may later refine capabilities only after the role boundary is checked.
- This lane must decide which capability questions are truly second-stage questions rather than backdoor rewrites of the original role matrix.

### P0 Layering Rule Decision (v1)

- `S0F-10A` remains the first gate for ordinary collaboration and platform override semantics.
- `S0F-10B` now fixes the following evaluation order for later capability policy:
  - first apply the stable role boundary from `S0F-10A`
  - only then evaluate whether a second-stage capability needs an entitlement decision
  - if the role boundary already denies an authority question such as `share_book`, `manage_book_members`, or `transfer_book_owner`, entitlement must not elevate that ordinary collaboration authority
- The minimum action split in this packet is now fixed as:
  - `role-only`: `read_book`, `edit_book`, `share_book`, `delete_book`, `transfer_book_owner`, `manage_book_members`
  - `entitlement-shaped candidates`: `copy_block_cross_book`, `export_book`, `create_template_from_book`, `bulk_book_operations`
- The `P0-C1-S2` success rule in this packet is:
  - one reader should be able to answer which questions stay inside the stable role matrix
  - one reader should be able to name which questions deserve later entitlement logic without reopening block-level ACL
  - entitlement should remain a capability filter layered on top of role checks rather than a path that silently turns one editor into one owner

#### P0 Role-First Layering Table (v1)

| policy question | first gate | second gate | boundary reason |
| --- | --- | --- | --- |
| ordinary collaboration authority on one book | `S0F-10A` role matrix | `none` | The first lane already answers who may read, edit, share, delete, transfer owner, and manage members. |
| premium or packaged capability on top of valid role standing | `S0F-10A` role matrix | entitlement check | Capability widening should only start after ordinary collaboration standing is already valid. |
| platform recovery or bounded override | `system_admin` override path from `S0F-10A` | `none` by default | Platform override is a governance/ops boundary, not a paid capability surface. |

### P0-C1-S3 (Deferred billing realism | v1)

- `mock billing` stays deferred at packet open.
- Any later subscription-state or payment-event model must be justified as a trigger surface for entitlement change, not as a replacement for the role baseline.

### P0 Billing Defer Decision (v1)

- `mock billing` remains deferred after `P0` and does not enter this contract packet as an implementation obligation.
- A later billing-shaped surface is allowed only under the following rule:
  - it may explain why `subscription_state` changes
  - it may not become the thing that directly defines ordinary collaboration standing
  - it should be modeled as an external trigger to entitlement activation, suspension, upgrade, or expiry rather than as one substitute for role or entitlement vocabulary
- The `P0-C1-S3` success rule in this packet is:
  - one reader should be able to explain why `subscription_state` is part of this vocabulary but `payment_event` is not yet required
  - one reader should be able to explain that the lane can still fix the second-stage policy boundary without simulating checkout, invoicing, or provider callbacks
  - later billing work should have to justify itself as a separate trigger packet instead of silently attaching itself to every entitlement sentence

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-10B/P<phase>-C<cycle>-S<steps>: <summary>`

## Plan (draft)

### P1 (Action split and entitlement surface mapping)

- `P1-C1-S1`: decide one minimum set of capability questions that stay role-only versus those that should widen into entitlement semantics
- `P1-C1-S2`: map those capability questions onto the current SoT without rewriting the `book`-first baseline or reopening block-level ACL

### P2 (Drill / Replay)

- `P2-C1-S1`: prove one bounded entitlement drill where role standing remains valid but one later capability is gated differently by plan or entitlement state
- `P2-C1-S2`: prove one replay where entitlement change does not accidentally mutate ordinary collaboration roles or platform override semantics

### P3 (Billing handoff decision)

- `P3-C1-S1`: decide whether `mock billing` is now required as a trigger surface for entitlement change or should remain deferred beyond this lane
- `P3-C1-S2`: decide whether any billing-shaped work belongs in a separate later packet instead of inside `S0F-10B`

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: fix one minimum vocabulary for `plan`, `entitlement`, and later `subscription_state`
- [x] `P0-C1-S2`: fix the layering rule between `S0F-10A` role checks and later entitlement checks
- [x] `P0-C1-S3`: keep billing realism explicitly deferred at packet open

### P1 (Action split and entitlement surface mapping)

- [ ] `P1-C1-S1`: decide one minimum capability split between role-only and entitlement-shaped questions
- [ ] `P1-C1-S2`: map that split onto the current SoT without reopening block-level ACL

### P2 (Drill / Replay)

- [ ] `P2-C1-S1`: prove one bounded entitlement drill where role standing and later capability policy remain distinct
- [ ] `P2-C1-S2`: prove one replay where entitlement change does not mutate role or system-admin semantics

### P3 (Billing handoff decision)

- [ ] `P3-C1-S1`: decide whether `mock billing` is required as a trigger surface for entitlement change
- [ ] `P3-C1-S2`: decide whether billing-shaped work belongs in a separate later packet

## Current Status (recommended)

- `S0F-10B` is now scaffolded as the intended next `M4` widening packet after the stable minimum closure in `S0F-10A`.
- `P0` is now complete: the lane now fixes one minimum vocabulary for `plan`, `entitlement`, and `subscription_state`, plus one explicit layering rule that keeps `S0F-10A` as the role-first access baseline.
- The lane is still `draft`: it now has a concrete contract packet, but it does not yet prove the first replayable entitlement split or any billing handoff decision.
- `roadmap_milestone` is already fixed to `M4`, but `roadmap_phase` remains blank on purpose because the current `road-002` `M4-P0..P3` bridge is already fully occupied by `S0F-10A`; this scaffold should not guess a new roadmap slot before that widening is made explicit.
- Automation should still read this log as an opening source scaffold rather than as a stable policy artifact.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths when the lane begins making real bounded changes.
- This section now begins with `P0` because the vocabulary-and-layering contract is complete, even though replay drills are still open.

### P0-C1-S1S2S3 (Minimum plan-entitlement vocabulary and role-first layering fixed | 2026-04-15)

- headSha: `working-tree-uncommitted`
- artifacts:
  - `docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
- expected:
  - the lane should stop using `plan`, `entitlement`, and `subscription_state` as loose placeholders and should fix one minimum contract vocabulary
  - the lane should state clearly that `S0F-10A` remains the first role boundary and that entitlement only applies to second-stage capability questions
  - the lane should keep `mock billing` deferred while still explaining why `subscription_state` belongs in the vocabulary
- observed:
  - `S0F-10B` now fixes one minimum vocabulary where `plan` is packaging, `entitlement` is executable capability policy, and `subscription_state` is lifecycle standing rather than a role alias
  - the lane now fixes one role-first layering rule that keeps ordinary collaboration authority in `S0F-10A` and reserves entitlement for later capability questions such as export, cross-book copy, template creation, or bulk operations
  - the lane now explicitly defers billing realism while allowing later billing-shaped work only as a trigger surface for entitlement-state change

## Recent changes (for traceability, optional)

- 2026-04-15: opened `S0F-10B` as the next intended `M4` widening packet so `plan / entitlement` can be modeled as a bounded second-stage lane instead of being pushed back into `S0F-10A`.
- 2026-04-15: fixed the opening default that `S0F-10A` remains the stable access baseline while `S0F-10B` handles the next boundary between role-shaped access and later entitlement-shaped capability policy.
- 2026-04-15: completed `P0-C1-S1S2S3` by fixing the minimum `plan / entitlement / subscription_state` vocabulary, the role-first layering rule over `S0F-10A`, and the explicit defer rule for billing realism.