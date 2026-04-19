# ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter

```yaml
support_only_contract_release_ledger:
  ledger_id: ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter
  ledger_kind: support-only-contract-release-ledger
  status: completed
  owner_lane: S0F-7C
  created_at: 2026-04-10
  reviewed_at: 2026-04-10
  accepted_at: 2026-04-10
  source_id: S0B-3A
  source_ref: docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
  source_scope: mixed source covering logs-facing unified indices, logs-facing front matter, legacy taxonomy, cutover, and stub preservation
  target_reading_goal: show how S0B-3A should split into first-pass LOGS and LIFECYCLE child candidates while preserving later parent synthesis and same-source cutover splitting
```

## Decision Frame

- This ledger treats `S0B-3A` as one mixed source rather than one already-generalized parent contract.
- The current draft default is:
  - promote logs-facing unified indices, logs-facing front matter, and logs-intake cutover into one first `DOC-WORKFLOW-LOGS` child candidate
  - promote legacy taxonomy, lifecycle cutover, and stub preservation into one first `DOC-WORKFLOW-LIFECYCLE` child candidate
  - keep later parent synthesis explicitly open rather than pretending the first child extraction already owns the final generalized workflow parent shape
- This ledger now acts as a completed first routing-and-consumption record for the initial `S0B-3A` split into `LOGS` and `LIFECYCLE`.

## Current Governance State

| governed surface | owner team | current steward | approval state | reviewed by | approved by | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter` | `docs-governance` | `role:workflow-ledger-maintainer` | `accepted-current-state` | `role:workflow-reviewer` | `role:docs-governance-approver` | This parent ledger remains the current routing surface for the mixed `S0B-3A` packet and now also acts as the current-state governance surface for the family because no dedicated supplement packet has been opened. |
| `DOC-WORKFLOW-LOGS-0001` | `docs-governance` | `delegated:workflow-logs-contract-maintainer` | `reviewed-awaiting-approval` | `role:workflow-reviewer` | `role:docs-governance-approver` | The logs child is the narrow current-state governance surface for the logs-facing `R01/R02/R04` slices while durable ownership remains with `docs-governance`. |
| `DOC-WORKFLOW-LIFECYCLE-0001` | `docs-governance` | `delegated:workflow-lifecycle-contract-maintainer` | `reviewed-awaiting-approval` | `role:workflow-reviewer` | `role:docs-governance-approver` | The lifecycle child is the narrow current-state governance surface for the legacy-taxonomy and lifecycle-boundary `R03/R05/R06` slices while durable ownership remains with `docs-governance`. |

- This block records current effective governance state for the parent ledger and the two child contracts.
- Because this family currently has no accepted supplement packet, packet-level accountability is not split into a separate evidence surface here; current routing state and family-level governance events therefore stay on the parent ledger until a later supplement exists.

## Routing And Consumption Table

| row id | source slice | meaning owned here | target family | target release action | contract lineage impact | retained-only action | resolution status | resolved by contract id | consumed scope | resolution notes | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S0B-3A-R01` | `1) Unified indices` in [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md) | logs-facing workflow identifiers, title identity grammar, and index-entry semantics for structured log intake | `DOC-WORKFLOW-LOGS` | `new-family` | `none-source-only` | `keep-in-log` | `applied` | `DOC-WORKFLOW-LOGS-0001` | `full` | consumed by `DOC-WORKFLOW-LOGS-0001` as the initial logs-facing identifier and title-identity rule body | Although unified identifiers later span more than logs, this earliest owned wording is still logs-facing enough that the first extraction stays narrow. |
| `S0B-3A-R02` | `3) Front matter` in [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md) | mechanically managed metadata fields as first stated in a logs-facing operational surface | `DOC-WORKFLOW-LOGS` | `new-family` | `none-source-only` | `keep-in-log` | `applied` | `DOC-WORKFLOW-LOGS-0001` | `full` | consumed by `DOC-WORKFLOW-LOGS-0001` as the first narrow logs-facing front matter rule body, while broader future widening remains reserved | This row is intentionally narrow on first extraction so the repo does not over-generalize front matter before repeated cross-kind evidence proves the wider parent shape. |
| `S0B-3A-R03` | `2) Legacy taxonomy` in [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md) | classify, freeze, and explicitly reference legacy material without forcing immediate rewrite or deletion | `DOC-WORKFLOW-LIFECYCLE` | `new-family` | `none-source-only` | `keep-in-log` | `applied` | `DOC-WORKFLOW-LIFECYCLE-0001` | `full` | consumed by `DOC-WORKFLOW-LIFECYCLE-0001` as the first explicit lifecycle legacy-management rule body | This slice also sharpens how earlier `S0B-2A` legacy and cutover material may later be re-routed from support-only into the same lifecycle family. |
| `S0B-3A-R04` | `4) Cutover & Stub` logs-intake sub-slice in [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md) | from the cutover boundary onward, new structured log content must follow the new identifier, title, and logs-facing metadata discipline | `DOC-WORKFLOW-LOGS` | `new-family` | `none-source-only` | `keep-in-log` | `applied` | `DOC-WORKFLOW-LOGS-0001` | `full` | consumed by `DOC-WORKFLOW-LOGS-0001` as the logs-intake half of the same-source cutover split | The ledger intentionally splits cutover before any explicit multi-consumption model so the logs intake rule can be judged independently. |
| `S0B-3A-R05` | `4) Cutover & Stub` lifecycle-boundary sub-slice in [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md) | legacy material remains frozen by default, and only re-enters the active system through migration-on-demand under the new management boundary | `DOC-WORKFLOW-LIFECYCLE` | `new-family` | `none-source-only` | `keep-in-log` | `applied` | `DOC-WORKFLOW-LIFECYCLE-0001` | `full` | consumed by `DOC-WORKFLOW-LIFECYCLE-0001` as the lifecycle half of the same-source cutover split | This is the lifecycle half of the same cutover source text; the split is deliberate so later consumption can stay explicit. |
| `S0B-3A-R06` | `4) Cutover & Stub` stub-preservation sub-slice in [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md) | preserve old links and old entry paths through stub documents when active material moves into the new managed system | `DOC-WORKFLOW-LIFECYCLE` | `new-family` | `none-source-only` | `keep-in-log` | `applied` | `DOC-WORKFLOW-LIFECYCLE-0001` | `full` | consumed by `DOC-WORKFLOW-LIFECYCLE-0001` as the continuity-preservation rule for moved legacy entry points | Stub preservation is grouped with lifecycle rather than logs because its primary concern is continuity across movement and freeze boundaries, not log-body structure itself. |

## Row Id Map

- `S0B-3A-R01`: Unified indices
- `S0B-3A-R02`: Front matter
- `S0B-3A-R03`: Legacy taxonomy
- `S0B-3A-R04`: Cutover and stub logs-intake sub-slice
- `S0B-3A-R05`: Cutover and stub lifecycle-boundary sub-slice
- `S0B-3A-R06`: Cutover and stub stub-preservation sub-slice

## First Draft Outcome

- The first `S0B-3A` routing draft now expects two new child-family candidates:
  - `DOC-WORKFLOW-LOGS-0001`
  - `DOC-WORKFLOW-LIFECYCLE-0001`
- Every first-pass slice is now marked `applied` because the receiving child contracts have been drafted and review-approved.
- The cutover wording is intentionally represented as two separate same-source rows:
  - one logs-intake rule
  - one lifecycle-boundary rule

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S0B-3A-GOV-01` | `contribution-event` | `S0B-3A mixed source` | `unknown` | `none-current-state` | `2026-04-10` | `docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md` | The original mixed source remains the defended contribution source, but it does not by itself prove the current steward or approval chain for the narrower logs and lifecycle children. |
| `S0B-3A-GOV-02` | `routing-writeback-event` | `ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter` | `role:packet-reviewer` | `current-routing-state-fixed` | `2026-04-10` | `S0B-3A-R01` through `S0B-3A-R06` | The completed parent ledger fixed the current routing state for the mixed packet without turning row-level source history into current ownership metadata. |
| `S0B-3A-GOV-03` | `delegated-stewardship-event` | `DOC-WORKFLOW-LOGS-0001` | `role:docs-governance-approver` | `current-steward-delegated` | `2026-04-15` | `S0F-9A/P4 second-cycle round` | The logs child now records one explicit delegated steward under the same durable owner team so day-to-day maintenance does not collapse back into undeclared team-wide ownership. |
| `S0B-3A-GOV-04` | `delegated-stewardship-event` | `DOC-WORKFLOW-LIFECYCLE-0001` | `role:docs-governance-approver` | `current-steward-delegated` | `2026-04-15` | `S0F-9A/P4 second-cycle round` | The lifecycle child now records one explicit delegated steward under the same durable owner team so day-to-day maintenance does not collapse back into undeclared team-wide ownership. |
| `S0B-3A-GOV-05` | `governance-role-separation-event` | `S0B-3A sample family without supplement` | `role:workflow-reviewer; role:docs-governance-approver` | `review-approve-separated-without-supplement` | `2026-04-15` | `S0F-9A/P4 second-cycle round` | This family now proves that current review and final approval can still be separated on parent and child governance surfaces even when no supplement packet exists yet. |

## New Releases Expected

- immediate candidates:
  - `DOC-WORKFLOW-LOGS-0001`
  - `DOC-WORKFLOW-LIFECYCLE-0001`
- later widening candidates after repeated child use:
  - one broader parent or sibling-spanning workflow surface if front matter and identifier rules are later proven to generalize beyond the first logs-oriented extraction

## Cumulative Sources To Carry Forward

- If `DOC-WORKFLOW-LOGS-0001` is emitted, it should likely carry forward at least:
  - [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md)
  - issue `44` as sharpening support for why stable identifiers and front matter mattered in the docs-management line
- If `DOC-WORKFLOW-LIFECYCLE-0001` is emitted, it should likely carry forward at least:
  - [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md)
  - issue `44` as sharpening support for why legacy taxonomy, cutover, and stub preservation were treated as durable management rules rather than ad hoc cleanup notes
  - possibly [log-S0B-2A-scripts-snapshots-management.md](d:/Project/wordloom-v3/docs/logs/log-S0B-2A-scripts-snapshots-management.md) later, if the lifecycle family explicitly absorbs the older legacy/cutover pressure from that mixed source

## Unconsumed Slices

- none

## Deferred Slices

- whether front matter should later widen beyond `DOC-WORKFLOW-LOGS-0001` into a broader parent or sibling-spanning workflow surface
- whether earlier mixed packets such as `S0B-2A` now need partial ledger repair so their legacy and cutover rows can re-route cleanly into `DOC-WORKFLOW-LIFECYCLE`
- whether explicit multi-consumption support is ever needed after narrow same-source splitting is attempted first

## Reader Notes

- This ledger is now the reviewed and completed first routing record for the `S0B-3A` split.
- The immediate review target is whether the slicing itself is right:
  - whether `LOGS` owns the correct narrow first-pass body
  - whether `LIFECYCLE` owns the correct narrow first-pass body
  - whether the two cutover rows are split at the right boundary
- Under `S0F-9A/P4` second-cycle work, this parent ledger now also acts as the current-state governance surface for the mixed `S0B-3A` family while no dedicated supplement packet exists.