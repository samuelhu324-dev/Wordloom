# log-S0F-10D (Phase 10D: Scenario catalog and mock state machine replays)

---

**id**: `S0F-10D`
**kind**: `log`
**title**: `scenario-catalog and mock-state-machine replay packet boundary v1`
**status**: `stable`
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

### P0 Minimum Scenario Vocabulary Decision (v1)

- `P0` is now fixed as one vocabulary-and-boundary packet for realistic local simulations that follow the already-stable role, entitlement, and trigger-chain baselines.
- The minimum terms in this packet are now fixed as:
  - `scenario_catalog_entry`
  - `replay_unit`
  - `mock_state_machine_input`
  - `replay_invariant`
- The semantic boundary for those terms is now fixed as follows:
  - `scenario_catalog_entry` means one named realistic situation such as trial upgrade, renewal failure, cancellation then expiry, refund handling, or administrative correction
  - `replay_unit` means one bounded testable scenario record that includes initial standing, trigger sequence, expected lifecycle transition, and expected entitlement outcome
  - `mock_state_machine_input` means one local input shape that reuses stable `payment_event`, `subscription_state`, and plan context rather than inventing alternative billing concepts
  - `replay_invariant` means one rule that must remain true while the scenario is replayed, especially preserved role semantics and preserved platform override boundaries
- The minimum illustrative values in this packet are now fixed as:
  - `scenario_catalog_entry`: `trial_upgrade_success`, `active_renewal_failure`, `cancellation_then_expiry`, `refund_narrowing`, `admin_state_repair`
  - `mock_state_machine_input` fields: `starting_plan`, `starting_subscription_state`, `trigger_sequence`, `expected_subscription_state`, `expected_entitlement_outcome`
  - `replay_invariant`: `roles_unchanged`, `system_admin_override_unchanged`, `book_acl_unchanged`, `trigger_chain_vocab_reused`
- The `P0-C1-S1` success rule in this packet is:
  - one reader should be able to distinguish scenario naming from replay execution input
  - one reader should be able to explain why `10D` reuses `10C` trigger semantics instead of replacing them
  - one reader should be able to explain why scenario realism here still does not require provider realism

#### P0 Scenario Vocabulary Table (v1)

| term | fixed meaning in `S0F-10D` | not allowed to mean |
| --- | --- | --- |
| `scenario_catalog_entry` | one named realistic lifecycle situation that should be replayable locally | one provider-specific callback payload or one implementation-specific test fixture |
| `replay_unit` | one bounded scenario record with inputs, transitions, expected outcomes, and invariants | one full billing engine, full UI flow, or production orchestration |
| `mock_state_machine_input` | one local input shape built from stable plan and trigger-chain terms | a replacement for `payment_event`, `subscription_state`, or entitlement semantics |
| `replay_invariant` | one rule that must remain true across scenario replay | one entitlement outcome or one mutable scenario step |

### P0-C1-S2 (Replay invariant boundary)

- Fix the rules each replay must preserve, especially the `10A/10B/10C` baselines.
- Keep role standing and bounded platform override outside simulated commercial lifecycle changes.

### P0 Replay Invariant Boundary Decision (v1)

- `S0F-10D` now fixes the following replay order for this lane:
  - first choose one `scenario_catalog_entry`
  - then construct one `replay_unit` from stable plan context, stable starting lifecycle standing, and one bounded trigger sequence
  - then run the local mock-state-machine transition using `10C` vocabulary only
  - then verify expected entitlement outcome together with preserved invariants
- The first invariant boundary in this packet is now fixed as:
  - scenario replay may change lifecycle standing and effective entitlement outcome through the existing `10C` trigger chain
  - scenario replay may not change collaboration role standing from `10A`
  - scenario replay may not redefine entitlement meaning from `10B`
  - scenario replay may not bypass bounded `system_admin` override semantics
- The minimum replay-family rules in this packet are now fixed as:
  - `trial_upgrade_success` should demonstrate widened entitlement through `trialing -> active`
  - `active_renewal_failure` should demonstrate narrowed or suspended entitlement through `active -> past_due`
  - `cancellation_then_expiry` should demonstrate deferred expiry through `active -> canceled -> expired`
  - `refund_narrowing` should demonstrate bounded entitlement rollback without role mutation
  - `admin_state_repair` should demonstrate explicit correction that restores model consistency rather than bypassing it
- The `P0-C1-S2` success rule in this packet is:
  - one reader should be able to explain which scenario fields are allowed to vary and which invariants must remain fixed
  - one reader should be able to explain that realistic simulation still stops at lifecycle and entitlement change rather than mutating membership or ownership
  - one reader should be able to explain that `10D` is a replay surface on top of `10C`, not a second trigger model

#### P0 Replay Invariant Table (v1)

| replay surface | allowed to change during replay | must remain unchanged | boundary reason |
| --- | --- | --- | --- |
| lifecycle standing | `subscription_state` according to bounded trigger sequence | role standing and membership semantics | Scenario realism is about commercial state change, not collaboration authority mutation. |
| entitlement outcome | effective capability bundle for the current plan and lifecycle standing | entitlement meaning defined in `10B` | Replay may exercise entitlement outcomes but may not redefine capability categories. |
| trigger sequence | representative `payment_event` ordering per scenario | trigger vocabulary defined in `10C` | Scenario replay must reuse the stable trigger-chain contract instead of inventing a new model. |
| administrative repair | bounded corrective transition to restore consistency | `system_admin` override boundary and ordinary role semantics | Correction is allowed only to repair lifecycle consistency, not to bypass governance or access rules. |

### P0-C1-S3 (Deferred provider adapters | v1)

- Real provider adapters, webhook trust, checkout orchestration, invoice detail, and tax logic remain deferred at packet open.
- The opening scenario packet should stay coherent even if those external systems are left unmodeled.

### P0 Provider-Adapter Defer Decision (v1)

- Real provider-adapter work remains deferred after `P0` and does not enter this scenario contract packet as an implementation obligation.
- The following surfaces are explicitly out of scope in this packet:
  - provider webhook schemas or signature-verification realism
  - checkout session creation or UI flow
  - invoice, tax, settlement, or accounting detail
  - live retry timing, provider idempotency, or asynchronous delivery guarantees
- A later provider-shaped packet is allowed only under the following rule:
  - it may explain how real external signals are translated into trusted `payment_event` inputs for the replay surface
  - it may not redefine the scenario vocabulary, replay invariants, or trigger semantics already fixed here and in `S0F-10C`
  - it should act as an upstream trigger source for the mock-state-machine contract rather than folding scenario replay back into provider detail
- The `P0-C1-S3` success rule in this packet is:
  - one reader should be able to explain why `10D` can model realistic product situations without live provider callbacks
  - one reader should be able to explain what later provider work is still allowed to add
  - later realism should have to open or extend one separate bounded packet instead of silently broadening this scenario lane

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-10D/P<phase>-C<cycle>-S<steps>: <summary>`

## Plan (draft)

### P1 (Scenario catalog and transition matrix)

- `P1-C1-S1`: fix one minimum scenario catalog that covers representative local simulations such as trial upgrade, renewal failure, cancellation then expiry, refund narrowing, and admin correction
- `P1-C1-S2`: map each scenario to trigger sequence, lifecycle transition, and entitlement outcome without rewriting role or entitlement boundaries

### P1 Minimum Scenario-Catalog Decision (v1)

- `P1` is now fixed as one minimum scenario-catalog packet rather than as one full billing test harness design.
- The stable vocabulary from `P0` remains authoritative for scenario naming, replay units, input shape, and invariant boundaries.
- The first representative scenario set is now fixed as:
  - `trial_upgrade_success`
  - `active_renewal_failure`
  - `cancellation_then_expiry`
  - `refund_narrowing`
  - `admin_state_repair`
- The first outcome set is now fixed as:
  - `activate-current-plan-bundle`
  - `narrow-current-plan-bundle`
  - `suspend-current-plan-bundle`
  - `expire-current-plan-bundle`
  - `repair-current-plan-bundle`
- The `P1` success rule in this packet is:
  - one reader should be able to answer which realistic situations must be replayed first without guessing missing scenario families
  - one reader should be able to answer how each scenario reuses `10C` trigger semantics to reach a resulting lifecycle standing
  - the packet should keep `S0F-10A`, `S0F-10B`, and `S0F-10C` semantics stable while widening only the local replay surface

#### P1 Scenario Catalog Table (v1)

| scenario entry | realistic situation covered | why it belongs in the first catalog | excluded from scope |
| --- | --- | --- | --- |
| `trial_upgrade_success` | one tenant upgrades from trial into an active paid standing | It proves the most basic positive path from restricted trial behavior to active entitlement. | provider checkout transport, payment method UX |
| `active_renewal_failure` | one active subscription fails renewal and degrades into impaired standing | It proves that capability narrowing or suspension follows lifecycle degradation rather than role mutation. | retry cadence, collections workflow |
| `cancellation_then_expiry` | one active subscription requests cancellation and later reaches end-of-term expiry | It proves delayed closure across more than one lifecycle step. | customer messaging, notice delivery |
| `refund_narrowing` | one active paid standing is narrowed after one bounded refund reversal path | It proves bounded rollback without reopening full refund-accounting semantics. | invoice reversal bookkeeping, settlement detail |
| `admin_state_repair` | one incorrect lifecycle record is corrected back to the intended standing | It proves bounded repair semantics without bypassing the model. | operator UI implementation, audit storage format |

#### P1 Scenario-to-State-Machine Matrix (v1)

| scenario entry | starting `subscription_state` | trigger sequence | resulting `subscription_state` | transition standing | notes |
| --- | --- | --- | --- | --- | --- |
| `trial_upgrade_success` | `trialing` | `upgrade_success` | `active` | `allow` | Successful upgrade widens lifecycle standing through the normal positive trigger path. |
| `active_renewal_failure` | `active` | `renewal_failed` | `past_due` | `allow` | Failed renewal degrades lifecycle standing without touching collaboration roles. |
| `cancellation_then_expiry` | `active` | `cancellation_requested`, then end-of-term lapse | `canceled`, then `expired` | `allow` | This scenario needs two ordered transitions to show deferred closure. |
| `refund_narrowing` | `active` | `refund_applied` | `canceled` or bounded degraded standing | `allow-bounded` | Refund-backed narrowing is allowed only through a bounded rollback path already compatible with `10C`. |
| `admin_state_repair` | any incorrect state | `admin_correction` | corrected state | `allow-bounded` | Administrative repair exists only to restore intended lifecycle reality. |

#### P1 Scenario-to-Outcome Matrix (v1)

| scenario entry | resulting entitlement effect | invariant checks emphasized | notes |
| --- | --- | --- | --- |
| `trial_upgrade_success` | `activate-current-plan-bundle` | `roles_unchanged`, `book_acl_unchanged`, `trigger_chain_vocab_reused` | Activation should widen entitlement-shaped capabilities while leaving ordinary standing intact. |
| `active_renewal_failure` | `suspend-current-plan-bundle` or `narrow-current-plan-bundle` | `roles_unchanged`, `system_admin_override_unchanged` | Degradation should impair effective capabilities without changing role semantics. |
| `cancellation_then_expiry` | `narrow-current-plan-bundle`, then `expire-current-plan-bundle` | `roles_unchanged`, `system_admin_override_unchanged`, `book_acl_unchanged` | Cancellation and expiry must close paid capability in phases rather than via direct role removal. |
| `refund_narrowing` | `narrow-current-plan-bundle` | `roles_unchanged`, `trigger_chain_vocab_reused` | Refund handling may contract entitlement, but only within bounded replay semantics. |
| `admin_state_repair` | `repair-current-plan-bundle` | `roles_unchanged`, `system_admin_override_unchanged`, `trigger_chain_vocab_reused` | Repair restores the bundle that should have matched corrected standing. |

#### P1 Scenario Mapping Notes (v1)

- The scenario replay surface now maps as follows:
  - one named scenario selects one initial lifecycle standing and one bounded trigger sequence
  - the trigger sequence reuses `10C` to produce one resulting `subscription_state`
  - the resulting lifecycle standing produces one entitlement effect that remains inside the `10B` boundary
  - the replay then checks invariant preservation to prove the scenario stayed inside the intended model
- The minimum mapping back to earlier packets is now fixed as:
  - `trial_upgrade_success` proves the simplest positive widening path after a narrower trial standing
  - `active_renewal_failure` proves capability impairment under lifecycle degradation rather than access-role mutation
  - `cancellation_then_expiry` proves that end-of-term closure can be simulated as one ordered multi-step scenario
  - `refund_narrowing` proves bounded rollback semantics without importing accounting or settlement realism
  - `admin_state_repair` proves that explicit correction restores consistency rather than bypassing model boundaries
- This packet still does not decide provider callback trust, checkout implementation, invoice detail, or tax detail.
- This packet still does not mutate:
  - `viewer / editor / owner` standing from `S0F-10A`
  - the role-only vs entitlement-shaped action split from `S0F-10B`
  - the `payment_event -> subscription_state -> entitlement` semantics from `S0F-10C`
  - bounded `system_admin` override semantics

### P2 (Replay drills and invariant checks)

- `P2-C1-S1`: define replay drills that run representative scenarios through the mock state machine and verify expected entitlement outcomes
- `P2-C1-S2`: verify invariants that role standing, platform override, and ownership semantics remain unchanged across the scenario set

### P2 Drill Decision (v1)

- `P2` now stays on the same scenario packet and proves replayability through named scenario drills rather than widening into provider realism or implementation detail.
- The first replay drill family is now fixed as:
  - start from one explicit scenario entry already fixed in `P1`
  - replay one bounded trigger sequence through the local mock state machine
  - observe resulting lifecycle standing and entitlement outcome
  - check that required invariants remain unchanged throughout the replay
- The first scenario drill set in this packet is now fixed as:
  - one widening-and-degradation replay using `trial_upgrade_success` and `active_renewal_failure`
  - one closure-and-repair replay using `cancellation_then_expiry`, `refund_narrowing`, and `admin_state_repair`
- The `P2` success rule in this packet is:
  - one reader should be able to replay one full positive-to-negative lifecycle chain without guessing hidden billing logic
  - one reader should be able to replay one closure-or-repair chain without confusing entitlement change with role mutation
  - the lane should still avoid provider webhook, checkout, invoice, or tax realism

#### P2 Replay Drill A (Upgrade success and renewal failure replay through the local state machine)

| drill step | actor or trigger source | precondition | intended transition or action | expected result | why it matters |
| --- | --- | --- | --- | --- | --- |
| `A1` | scenario selector `trial_upgrade_success` | one tenant is on `starting_plan = trial`, `subscription_state = trialing`, and one user holds valid ordinary standing such as `editor` on one book | load the `trial_upgrade_success` replay unit into the local mock state machine | replay unit is ready with stable `10C` trigger vocabulary and stable invariants | The drill must start from one explicit scenario entry rather than one ad hoc imaginary case. |
| `A2` | bounded trigger `upgrade_success` | same role standing unchanged; current entitlement bundle is still trial-shaped | apply `upgrade_success` | `trialing -> active` and `activate-current-plan-bundle` | The drill must show that activation is produced by lifecycle transition first and entitlement effect second. |
| `A3` | same user after activation | same role standing and same book ACL unchanged | attempt one entitlement-shaped capability such as `copy_block_cross_book` or `export_book` under the active bundle | `allow-via-entitlement` according to the now-active plan bundle | The drill must show widened capability without mutating collaboration role semantics. |
| `A4` | scenario selector `active_renewal_failure` | subscription is now `active`; ordinary standing and ownership semantics remain unchanged | load the `active_renewal_failure` replay unit and apply `renewal_failed` | `active -> past_due` and `suspend-current-plan-bundle` or `narrow-current-plan-bundle` | The drill must show lifecycle degradation as the direct source of entitlement contraction. |
| `A5` | same user after degradation | same role standing unchanged; same entitlement-shaped capability is attempted again | replay the same capability check under the degraded standing | `deny-via-entitlement` or narrower behavior, while role standing still remains valid | The drill must show that entitlement impairment does not rewrite book collaboration standing. |

#### P2 Replay Drill B (Cancellation, refund narrowing, expiry, and repair preserve invariants)

| drill step | actor or trigger source | precondition | intended transition or action | expected result | why it matters |
| --- | --- | --- | --- | --- | --- |
| `B1` | scenario selector `cancellation_then_expiry` | one subscription is currently `active`; one user still has valid ordinary standing on one book | load the `cancellation_then_expiry` replay unit and apply `cancellation_requested` | `active -> canceled` and `narrow-current-plan-bundle` pending expiry | The drill must show that cancellation changes lifecycle and entitlement but not collaboration role assignment. |
| `B2` | end-of-term lapse | subscription currently `canceled` and not recovered | advance the replay to its terminal lifecycle step | `canceled -> expired` and `expire-current-plan-bundle` | The drill must show clean capability closure without rewriting owner, editor, or viewer standing. |
| `B3` | scenario selector `refund_narrowing` | one active paid standing is still represented inside the mock-state-machine input | load the `refund_narrowing` replay unit and apply `refund_applied` through the bounded rollback path | bounded degraded standing and `narrow-current-plan-bundle` | The drill must show that refund-backed contraction stays inside the replay contract rather than importing accounting semantics. |
| `B4` | scenario selector `admin_state_repair` | one lifecycle state was previously recorded incorrectly | load the `admin_state_repair` replay unit and apply `admin_correction` | corrected lifecycle standing and `repair-current-plan-bundle` | Administrative repair should restore model consistency rather than bypassing the model. |
| `B5` | invariant checker and `system_admin` override path | same lifecycle scenarios as above have already been replayed | verify `roles_unchanged`, `book_acl_unchanged`, `trigger_chain_vocab_reused`, and inspect one override path | invariants remain true and `allow-via-override` does not depend on paid lifecycle state | The drill must prove that platform override stays outside subscription-trigger semantics and that scenario replay does not leak into access-role mutation. |

### P3 (Provider-adapter handoff)

- `P3-C1-S1`: define what later provider-adapter work is allowed to add without changing the scenario contract
- `P3-C1-S2`: define entry conditions for a later provider-realism packet if local scenario replay proves insufficient

### P3 Provider-Handoff Decision (v1)

- `P3` is now fixed as one close-out boundary decision rather than as the start of an embedded provider integration stream.
- `S0F-10D` now explicitly concludes that provider-adapter realism is not required to make the first scenario catalog and replay packet coherent or replayable.
- The minimum closure delivered by `P0-P2` is now sufficient to stand on its own because:
  - the scenario vocabulary, replay-unit input shape, and invariant boundaries are explicit
  - the first representative scenario catalog and scenario mapping tables are explicit
  - the first replayable scenario drills already prove lifecycle-driven entitlement change and invariant preservation without provider callbacks or checkout realism
- Provider-shaped work is now explicitly split to a later packet under the following rule:
  - a later packet may model webhook trust, checkout success, invoice issuance, refund transport, or provider callback verification only if it needs to explain how a trusted upstream signal becomes one bounded replay input
  - that later packet must treat provider realism as the source of bounded `payment_event` inputs for the replay surface, not as a replacement for the `10D` scenario catalog or the `10C` trigger chain
  - that later packet must not redefine the role baseline from `S0F-10A`, the entitlement boundary from `S0F-10B`, the trigger-chain semantics from `S0F-10C`, or the scenario and invariant contract fixed in `S0F-10D`
- The `P3` success rule in this packet is:
  - one reader should be able to explain why `10D` can close without implementing provider callbacks, checkout, invoice, or tax flows
  - one reader should be able to explain what future provider work is still allowed to do
  - later realism should have to open one separate bounded packet instead of silently broadening this scenario lane

#### P3 Keep-vs-Split Decision Table (v1)

| topic | decision in `S0F-10D` | reason |
| --- | --- | --- |
| scenario catalog vocabulary | `keep-in-lane` | This packet needs explicit scenario naming and replay input semantics to explain realistic local simulations. |
| replay invariant rules | `keep-in-lane` | This packet needs explicit invariant checks to prove role and override boundaries survive scenario replay. |
| replay drill definitions | `keep-in-lane` | This packet needs replay steps to show how scenario semantics are actually exercised. |
| provider webhook or checkout realism | `split-to-later-packet` | Provider transport is not required to prove the first scenario packet or replay the current drills. |
| invoice, tax, settlement, or retry detail | `split-to-later-packet` | Those surfaces belong to later external-system packets, not to the minimum scenario replay closure. |

#### P3 Later-Packet Entry Conditions (v1)

- A later provider-shaped packet may open only when at least one of these conditions becomes concrete:
  - one replay requires proving how a real provider callback, checkout success, or refund notice becomes one trusted `payment_event` input for the mock-state-machine surface
  - one downstream implementation packet needs one bounded source-of-truth rule for provider-originated retry, invoice, refund, or tax-bearing signals
  - one integration packet needs one concrete `provider signal -> payment_event -> subscription_state -> entitlement outcome -> scenario replay` chain rather than the abstract local model fixed here
- Until one of those conditions is real, later work should treat `S0F-10D` as the stable scenario-replay baseline and should not reopen this lane just to host speculative provider detail.

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: fix the minimum scenario-catalog vocabulary
- [x] `P0-C1-S2`: fix replay invariants and preserved boundaries
- [x] `P0-C1-S3`: defer provider-adapter realism explicitly

### P1 (Scenario catalog and transition matrix)

- [x] `P1-C1-S1`: fix the first representative realistic scenario catalog
- [x] `P1-C1-S2`: map scenario inputs to lifecycle and entitlement outcomes

### P2 (Replay drills and invariant checks)

- [x] `P2-C1-S1`: define replayable mock-state-machine drills
- [x] `P2-C1-S2`: verify invariant preservation across the drill set

### P3 (Provider-adapter handoff)

- [x] `P3-C1-S1`: define later provider-adapter permissions and limits
- [x] `P3-C1-S2`: define later-packet entry conditions

## Current Status (recommended)

- `S0F-10D` now has a stable `P0` contract for scenario-catalog vocabulary, replay invariants, and provider-adapter defer rules on top of the stable trigger-chain baseline in `S0F-10C`.
- `P1` is now complete: the lane now fixes one first representative realistic scenario catalog, one scenario-to-state-machine matrix, and one scenario-to-outcome matrix that preserve the `10A/10B/10C` baselines.
- `P2` is now complete: the lane now carries one widening-and-degradation replay drill plus one closure-and-repair replay drill that together prove entitlement change and invariant preservation across the first scenario set.
- `P3` is now complete: the lane now explicitly splits provider callback, checkout, invoice, tax, and retry realism into later dedicated packets instead of embedding them into the minimum scenario-replay closure.
- `S0F-10D` now stands as the stable minimum scenario-catalog and mock-state-machine replay baseline after `S0F-10C`: later work may widen from it, but should not reopen it just to host provider integration detail.
- Automation may now read this log as the stable scenario-replay source packet and treat provider-shaped follow-up as separate later work.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1S2S3 (Scenario contract boundary and defer rules | 2026-04-15)

- headSha: `1195dd544`
- artifacts: `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
- expected:
  - `P0` fixes one minimum vocabulary for realistic scenario entries, replay units, mock-state-machine inputs, and replay invariants.
  - `P0` fixes preserved-boundary rules proving that scenario replay does not rewrite `10A/10B/10C` semantics.
  - `P0` defers provider-adapter realism explicitly into a later bounded packet.
- observed:
  - Added explicit `P0` contract decisions, vocabulary and invariant tables, checklist completion, and updated packet status for the next `P1` scenario-matrix phase.

### P1-C1-S1S2 (First realistic scenario catalog and mapping fixed | 2026-04-15)

- headSha: `9925d9d52`
- artifacts: `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
- expected:
  - `P1` fixes one first representative catalog of realistic local lifecycle simulations.
  - `P1` maps each scenario to bounded trigger sequence, resulting lifecycle standing, and resulting entitlement effect.
  - `P1` keeps role, entitlement-boundary, and trigger-chain semantics unchanged while widening only the replay surface.
- observed:
  - Added the first scenario catalog table, scenario-to-state-machine matrix, scenario-to-outcome matrix, completed `P1` checklist items, and updated packet status for the next `P2` drill phase.

### P2-C1-S1S2 (Replayable scenario drills and invariant checks fixed | 2026-04-16)

- headSha: `8513007c3`
- artifacts: `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
- expected:
  - `P2` fixes replayable drill steps for the first representative scenario set.
  - `P2` proves that lifecycle and entitlement results can be replayed locally without provider realism.
  - `P2` proves that role standing, book ACL standing, and bounded override semantics remain unchanged across the replay set.
- observed:
  - Added one widening-and-degradation replay drill, one closure-and-repair replay drill, completed `P2` checklist items, and updated packet status for the next `P3` provider-handoff phase.

### P3-C1-S1S2 (Provider realism split beyond the minimum scenario-replay closure | 2026-04-16)

- headSha: `working-tree-uncommitted`
- artifacts: `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
- expected:
  - `P3` stops leaving provider realism as an unresolved ambiguity after the scenario catalog and replay drills are already explicit and replayable.
  - `P3` decides whether provider-style detail belongs inside `S0F-10D` or in one later dedicated packet.
  - the result preserves the `10A` role baseline, the `10B` entitlement boundary, the `10C` trigger-chain semantics, and the `10D` replay contract.
- observed:
  - `S0F-10D` now explicitly concludes that provider realism is not required for the first scenario-replay closure.
  - the lane now splits webhook, checkout, invoice, tax, retry, and settlement-style integration detail to later dedicated packets.
  - the first scenario packet can now be treated as a stable minimum closure rather than as a partially finished provider-and-replay hybrid.

## Recent changes (for traceability, optional)

- 2026-04-15: Opened `S0F-10D` as the next `M4` scenario-catalog and mock-state-machine replay packet after `S0F-10C` stabilized the trigger-chain boundary.
- 2026-04-15: Completed `S0F-10D/P0` by fixing scenario vocabulary, replay invariant boundaries, and explicit provider-adapter defer rules.
- 2026-04-15: Completed `S0F-10D/P1` by fixing the first realistic scenario catalog and mapping it to lifecycle and entitlement outcomes.
- 2026-04-16: Completed `S0F-10D/P2` by fixing the first replayable scenario drills and invariant checks on top of the `P1` catalog.
- 2026-04-16: Completed `S0F-10D/P3` by explicitly splitting provider callback, checkout, invoice, tax, retry, and settlement realism into later dedicated packets and marking `S0F-10D` as the stable minimum scenario-replay closure.