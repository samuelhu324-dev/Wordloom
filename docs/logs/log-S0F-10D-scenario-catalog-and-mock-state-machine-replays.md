# log-S0F-10D (Phase 10D: Scenario catalog and mock state machine replays)

---

**id**: `S0F-10D`
**kind**: `log`
**title**: `scenario-catalog and mock-state-machine replay packet boundary v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Access, Billing, Entitlement, Scenarios, Drills, Evidence, epic/s0, sub/10d`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`
  **reference_log_1**: `docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`
  **reference_log_2**: `docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
**issue_keyword**: `policy`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/10d`
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
- Day-level precision is acceptable while this scenario packet is still a policy-and-replay scaffold.
- `reviewed` should remain `pending` until this lane is accepted as the next bounded `M4` child packet after the stable trigger semantics in `S0F-10C`.

## Decision / Outcome

**Decision**:

- `S0F-10D` opens the next `M4` child lane as a bounded scenario packet for realistic subscription and entitlement simulations after `S0F-10C` has already fixed the minimum trigger-chain boundary.
- The purpose of this lane is not to redefine `payment_event`, `subscription_state`, or entitlement semantics; it is to turn those stable terms into replayable scenario catalogs and mock-state-machine transitions that look like real product situations.
- The opening packet should still avoid real provider integration, checkout implementation, invoice realism, tax logic, or production billing orchestration; it should stay on scenario shape, replay rules, and mock-state-machine inputs.

**Default choices (phase defaults / v1)**:

- `S0F-10A` remains the stable role baseline.
- `S0F-10B` remains the stable entitlement-boundary baseline.
- `S0F-10C` remains the stable trigger-chain baseline.
- `S0F-10D` may simulate realistic subscription situations, but it must not redefine what `payment_event`, `subscription_state`, `entitlement_snapshot`, `viewer`, `editor`, `owner`, or `system_admin` already mean.
- If one realistic scenario can be explained by replaying bounded state transitions locally, prefer the simpler mock-state-machine approach and defer provider adapters again.

## PR Summary Inputs (optional)

- Use this block because `S0F-10D` is intended to become the next bounded `M4` scenario packet after `S0F-10C`.

**PR summary bullets**:

- Open the next `M4` child lane for realistic scenario catalogs and mock-state-machine replays after the trigger boundary is already stable.
- Fix the difference between scenario inputs, mock lifecycle transitions, and expected entitlement outcomes without reopening the `10A/10B/10C` baselines.
- Keep provider adapters, checkout UX, invoice logic, and tax detail out of the opening packet unless later replay evidence proves they are required.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
- Previous log: `docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`

## Exported Sections / Outlet Ownership

- This slice starts as one `log-retained core + scenario-catalog contract-first` lane.
- The expected first landing is one stable contract that answers which realistic scenarios must be replayed locally, how mock transitions are represented, and which invariants those replays must preserve.

**Outlet ownership**:

- `contract`: define the scenario catalog vocabulary, mock-state-machine input shape, replay invariants, and allowed scenario families
- `runbook`: no-op at packet open; operator procedure should wait until one stable replay sequence exists
- `view`: no-op at packet open; reader-facing scenario summaries should wait until one stable catalog table exists
- `index/front-door`: no-op at packet open
- `disposition/placement`: no-op at packet open
- `log-retained core`: lane boundary, scenario rules, phase plan, execution checklist, and later evidence ledger remain here

## Definitions

- `scenario catalog`: one bounded list of realistic lifecycle situations that should be replayable without real payment providers.
- `mock state machine`: one local transition model that accepts bounded trigger inputs and produces bounded lifecycle and entitlement outcomes.
- `replay unit`: one named scenario with initial state, trigger sequence, expected state transition, and expected entitlement outcome.
- `invariant`: one rule that must remain true across all replay units, such as preserved role semantics or bounded platform override behavior.
- `provider adapter`: one later packet that may translate real external callbacks into trusted trigger inputs, but does not belong to this lane at open.

## Constraints

- Do not rewrite the role baseline already fixed in `S0F-10A`.
- Do not rewrite the entitlement boundary already fixed in `S0F-10B`.
- Do not rewrite the trigger-chain vocabulary already fixed in `S0F-10C`.
- Do not require real payment-provider integration in this opening packet.
- Do not mix scenario replay rules with checkout UX, invoice rendering, settlement logic, or tax handling.
- Do not let scenario simulation mutate collaboration roles or bypass bounded platform override semantics.

## Scope

- `P0`: scenario contract and replay vocabulary
- `P1`: scenario catalog and transition matrix
- `P2`: replay drills and invariant checks
- `P3`: provider-adapter handoff and later-packet boundary

## Success Criteria (DoD)

- The lane fixes one minimum vocabulary for scenario catalog entries, replay units, mock-state-machine inputs, and replay invariants.
- The lane defines one stable catalog of representative lifecycle situations that look like real product behavior without depending on real providers.
- The lane proves that replayed lifecycle changes do not rewrite `S0F-10A` role semantics or `S0F-10B` entitlement boundaries.
- The lane proves that `S0F-10C` trigger semantics are sufficient to power realistic local simulations.
- The lane keeps provider adapters, checkout, invoice, tax, and settlement detail explicitly separate unless replay evidence proves they are required.
- The lane leaves one reader able to explain how to simulate trial, upgrade, failure, cancellation, expiry, refund, and correction scenarios locally.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the scenario vocabulary and replay input shape are explicit
  - at least one stable scenario catalog table exists
  - at least one replayable mock-state-machine drill exists with invariant checks
  - the Evidence section includes traceable `headSha` values plus artifact paths
- `stable` for this scenario packet does not require real provider callbacks; it requires a bounded and replayable explanation of realistic state simulations.

## P0 (Contract | v1)

### P0-C1-S1 (Scenario-catalog vocabulary)

- Fix one minimum vocabulary for scenario entries, replay units, and mock-state-machine input shape.
- Keep scenario naming, trigger sequence, lifecycle transition, and entitlement outcome as distinct fields.

### P0-C1-S2 (Replay invariant boundary)

- Fix the rules each replay must preserve, especially the `10A/10B/10C` baselines.
- Keep role standing and bounded platform override outside simulated commercial lifecycle changes.

### P0-C1-S3 (Deferred provider adapters | v1)

- Real provider adapters, webhook trust, checkout orchestration, invoice detail, and tax logic remain deferred at packet open.
- The opening scenario packet should stay coherent even if those external systems are left unmodeled.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-10D/P<phase>-C<cycle>-S<steps>: <summary>`

## Plan (draft)

### P1 (Scenario catalog and transition matrix)

- `P1-C1-S1`: fix one minimum scenario catalog that covers representative local simulations such as trial upgrade, renewal failure, cancellation then expiry, refund narrowing, and admin correction
- `P1-C1-S2`: map each scenario to trigger sequence, lifecycle transition, and entitlement outcome without rewriting role or entitlement boundaries

### P2 (Replay drills and invariant checks)

- `P2-C1-S1`: define replay drills that run representative scenarios through the mock state machine and verify expected entitlement outcomes
- `P2-C1-S2`: verify invariants that role standing, platform override, and ownership semantics remain unchanged across the scenario set

### P3 (Provider-adapter handoff)

- `P3-C1-S1`: define what later provider-adapter work is allowed to add without changing the scenario contract
- `P3-C1-S2`: define entry conditions for a later provider-realism packet if local scenario replay proves insufficient

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: fix the minimum scenario-catalog vocabulary
- [ ] `P0-C1-S2`: fix replay invariants and preserved boundaries
- [ ] `P0-C1-S3`: defer provider-adapter realism explicitly

### P1 (Scenario catalog and transition matrix)

- [ ] `P1-C1-S1`: fix the first representative realistic scenario catalog
- [ ] `P1-C1-S2`: map scenario inputs to lifecycle and entitlement outcomes

### P2 (Replay drills and invariant checks)

- [ ] `P2-C1-S1`: define replayable mock-state-machine drills
- [ ] `P2-C1-S2`: verify invariant preservation across the drill set

### P3 (Provider-adapter handoff)

- [ ] `P3-C1-S1`: define later provider-adapter permissions and limits
- [ ] `P3-C1-S2`: define later-packet entry conditions

## Current Status (recommended)

- `S0F-10D` is now opened as the next bounded packet after the stable trigger-chain baseline in `S0F-10C`.
- The lane is still a `draft` source log: the boundary and phase plan are now explicit, but the concrete scenario catalog, replay drills, and later handoff rules still remain open.
- The next step should be `P0`, followed by one first scenario matrix in `P1`; automation should still read this log as the active source for this packet.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

## Recent changes (for traceability, optional)

- 2026-04-15: Opened `S0F-10D` as the next `M4` scenario-catalog and mock-state-machine replay packet after `S0F-10C` stabilized the trigger-chain boundary.