# ledger-S0B-2A-tools-scripts-and-snapshots-management

```yaml
support_only_contract_release_ledger:
  ledger_id: ledger-S0B-2A-tools-scripts-and-snapshots-management
  ledger_kind: support-only-contract-release-ledger
  status: draft
  owner_lane: S0F-7B
  created_at: 2026-04-10
  reviewed_at: 2026-04-11
  accepted_at: pending
  source_id: S0B-2A
  source_ref: docs/logs/log-S0B-2A-scripts-snapshots-management.md
  source_scope: mixed source covering scripts taxonomy, stable entrypoint, snapshot policy, cutover, and stub routing
  target_reading_goal: show which slices of S0B-2A should update the LABS family now, which slices remain future-family candidates, and which slices stay support-only or deferred until later review
```

## Decision Frame

- This ledger treats `S0B-2A` as one mixed source rather than as one single-family contract candidate.
- The current draft default is:
  - promote the snapshot-policy slice into the existing `DOC-WORKFLOW-LABS` family as one later release candidate
  - keep scripts taxonomy and stable entrypoint as one unresolved `workflow/scripts governance` candidate rather than forcing them into `LABS`
  - keep the runbook snapshot-root distinction as one possible OPS-side evidence candidate, but still deferred for now
  - keep cutover, stub, and legacy-routing mechanics as support-only unless a narrower future family is later justified
- This ledger is now both a routing draft and a future consumption tracker; later review should be able to say exactly which slices were consumed and which were not.

## Current Governance State

| governed surface | owner team | current steward | approval state | reviewed by | approved by | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `ledger-S0B-2A-tools-scripts-and-snapshots-management` | `docs-governance` | `role:workflow-ledger-maintainer` | `parent-review-pending-final-acceptance` | `role:workflow-reviewer` | `role:docs-governance-approver` | This mixed-source ledger remains the current routing surface for how `S0B-2A` is interpreted, including which slices are applied, deferred, or support-only. |
| `DOC-WORKFLOW-LABS-0002` | `docs-governance` | `delegated:workflow-labs-contract-maintainer` | `reviewed-awaiting-approval` | `role:workflow-reviewer` | `role:docs-governance-approver` | The labs child is the current-state governance surface for the consumed `R03` labs sub-slice while durable ownership remains with `docs-governance`. |

- This block records current effective governance state for the parent ledger and the one child contract that this mixed source currently resolves into.
- Deferred scripts-governance and OPS-evidence candidates remain routing outcomes rather than current governed contract surfaces until separate families are actually opened.

## Routing And Consumption Table

| row id | source slice | meaning owned here | target family | target release action | contract lineage impact | retained-only action | resolution status | resolved by contract id | consumed scope | resolution notes | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S0B-2A-R01` | `1) Directory taxonomy` in [log-S0B-2A-scripts-snapshots-management.md](d:/Project/wordloom-v3/docs/logs/log-S0B-2A-scripts-snapshots-management.md) | classify scripts by lifecycle and risk: `ops/labs/migrations/dev/legacy`; keep new scripts inside the governed taxonomy rather than by author memory | `DOC-WORKFLOW-SCRIPTS` candidate | `new-family` | `none-source-only` | `defer` | `deferred` | `none` | `none` | no receiving family is opened yet; this slice remains intentionally unresolved until the user decides whether scripts governance deserves its own DOC-owned family | This slice is broader than `LABS` and still reads as docs-owned workflow/scripts governance rather than labs-only or operator-only semantics. |
| `S0B-2A-R02` | `2) Stable entrypoint` in [log-S0B-2A-scripts-snapshots-management.md](d:/Project/wordloom-v3/docs/logs/log-S0B-2A-scripts-snapshots-management.md) | stable CLI/router semantics, naming inference, default safety switches, and legacy reuse boundary | `DOC-WORKFLOW-SCRIPTS` candidate | `new-family` | `none-source-only` | `defer` | `deferred` | `none` | `none` | this slice travels with the unresolved scripts-governance question and should not be forced into `LABS-0002` by default | This still reads as scripts-governance rather than the narrower labs evidence contract. |
| `S0B-2A-R03` | `3) Snapshots policy` labs sub-slice in [log-S0B-2A-scripts-snapshots-management.md](d:/Project/wordloom-v3/docs/logs/log-S0B-2A-scripts-snapshots-management.md) | labs evidence-root semantics, run folder shape, retention, and auditability for lab snapshot outputs | `DOC-WORKFLOW-LABS` | `new-release` | `none-source-only` | `keep-in-log` | `applied` | `DOC-WORKFLOW-LABS-0002` | `full` | consumed by the drafted `DOC-WORKFLOW-LABS-0002` release, which merges `LABS-0001` with the labs-only `S0B-2A` snapshot-policy slice while leaving non-labs slices unresolved | This now acts as the first concrete proof that one ledger slice can be consumed by one later release without forcing the rest of the source into the same family. |
| `S0B-2A-R04` | `3) Snapshots policy` runbook sub-slice in [log-S0B-2A-scripts-snapshots-management.md](d:/Project/wordloom-v3/docs/logs/log-S0B-2A-scripts-snapshots-management.md) | distinguish `docs/runbook/_snapshot/` from `docs/labs/_snapshot/` as operator-evidence semantics, not just labs evidence semantics | `DOC-OPS-RUNBOOK-EVIDENCE` candidate | `new-family` | `none-source-only` | `defer` | `deferred` | `none` | `none` | keep deferred until a stronger operator-owned source proves that this should become one OPS-side family rather than one side-note inside scripts governance | This slice may later justify one OPS-side evidence family, but the current source is still mixed and not yet strong enough to force that split. |
| `S0B-2A-R05` | `4) Legacy taxonomy + cutover` in [log-S0B-2A-scripts-snapshots-management.md](d:/Project/wordloom-v3/docs/logs/log-S0B-2A-scripts-snapshots-management.md) | migration boundary, what becomes frozen legacy, and from-when the new rules apply | `none` | `no-contract` | `none-source-only` | `support-only` | `retained-support-only` | `none` | `none` | retained as routing support and migration context; no later contract consumption is planned in the current draft | This slice currently reads more like migration/disposition support than one standalone stable contract family. |
| `S0B-2A-R06` | `5) Stub policy` in [log-S0B-2A-scripts-snapshots-management.md](d:/Project/wordloom-v3/docs/logs/log-S0B-2A-scripts-snapshots-management.md) | preserve old links after relocation through stub documents | `none` | `no-contract` | `none-source-only` | `support-only` | `retained-support-only` | `none` | `none` | retained as link-preservation support; not currently targeted for contract promotion through this ledger | This is important support logic but not the first target for a release-based contract sample here. |

## Row Id Map

- `S0B-2A-R01`: Directory taxonomy
- `S0B-2A-R02`: Stable entrypoint
- `S0B-2A-R03`: Snapshots policy labs sub-slice
- `S0B-2A-R04`: Snapshots policy runbook sub-slice
- `S0B-2A-R05`: Legacy taxonomy + cutover
- `S0B-2A-R06`: Stub policy

## First-Sample Outcome

- The first active release sample from this ledger is now one later release in the `DOC-WORKFLOW-LABS` family:
  - earlier release: `DOC-WORKFLOW-LABS-0001`
  - drafted later release: `DOC-WORKFLOW-LABS-0002`
- `DOC-WORKFLOW-LABS-0002` consumes only the `S0B-2A` slice that materially strengthens labs snapshot governance:
  - unified labs evidence root
  - run-folder shape
  - retention or archival guidance for labs outputs
  - clearer evidence-package semantics
- The drafted release still does not absorb the scripts taxonomy, stable CLI entrypoint, or cutover/stub slices into `LABS-0002`.

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S0B-2A-GOV-01` | `contribution-event` | `S0B-2A mixed source` | `unknown` | `none-current-state` | `2026-04-10` | `docs/logs/log-S0B-2A-scripts-snapshots-management.md` | The source log remains the defended contribution source, but it does not by itself prove the current steward or approval chain for the mixed-source routing state. |
| `S0B-2A-GOV-02` | `routing-writeback-event` | `ledger-S0B-2A-tools-scripts-and-snapshots-management` | `role:packet-reviewer` | `current-routing-state-fixed` | `2026-04-10` | `S0B-2A-R01` through `S0B-2A-R06` | The parent ledger fixed that only the labs sub-slice currently resolves into an active child contract while scripts, OPS evidence, and cutover/stub remain deferred or support-only. |
| `S0B-2A-GOV-03` | `delegated-stewardship-event` | `DOC-WORKFLOW-LABS-0002` | `role:docs-governance-approver` | `current-steward-delegated` | `2026-04-15` | `S0F-9A/P4 scoped backfill round` | The consumed labs child now records one explicit delegated steward under the same durable owner team so day-to-day maintenance does not collapse back into undeclared team-wide ownership. |
| `S0B-2A-GOV-04` | `governance-role-separation-event` | `S0B-2A current routing state` | `role:workflow-reviewer; role:docs-governance-approver` | `review-approve-separated` | `2026-04-15` | `S0F-9A/P4 third-cycle round` | The mixed-source routing ledger now records review and approval as distinct governance acts even though only one child contract is currently resolved from this packet. |

## New Releases Expected

- Immediate sample candidate:
  - `DOC-WORKFLOW-LABS-0002`
- Later family candidates after review:
  - `DOC-WORKFLOW-SCRIPTS-0001` if the user later decides that scripts naming, entrypoint, and taxonomy really form one docs-owned workflow/scripts family
  - `DOC-OPS-RUNBOOK-EVIDENCE-0001` only if later evidence makes the OPS-owned operator-evidence boundary explicit enough

## Cumulative Sources To Carry Forward

- If the first sample becomes `DOC-WORKFLOW-LABS-0002`, the release should likely carry forward at least:
  - GitHub issue `S0B/1A (#36)` from the current `DOC-WORKFLOW-LABS-0001` draft
  - [log-S0B-2A-scripts-snapshots-management.md](d:/Project/wordloom-v3/docs/logs/log-S0B-2A-scripts-snapshots-management.md) for the newly absorbed labs snapshot semantics
- The first sample should not carry forward the whole scripts-taxonomy or stable-entrypoint slice unless that content is actually promoted into the release body.

## Unconsumed Slices

- directory taxonomy
- stable entrypoint
- runbook snapshot-root distinction

## Deferred Slices

- whether scripts taxonomy and stable entrypoint should open one explicit docs-owned `workflow/scripts governance` family now or wait until another source reinforces the same boundary
- whether the runbook snapshot root and ops-safe defaults justify one OPS-owned family now or should remain deferred until a stronger operator-owned source appears

## Reader Notes

- This ledger is intentionally a routing-and-consumption draft, not a final adjudication.
- The purpose of this revised draft is to let the user review two things separately:
  - whether the slice-to-family split is right
  - whether the consumption-tracking fields are sufficient to tell later what `LABS-0002` actually consumed and what remained unresolved
- Under `S0F-9A/P4` third-cycle work, this ledger now also acts as the current-state governance surface for the mixed `S0B-2A` packet while `DOC-WORKFLOW-LABS-0002` remains the only active child governance surface currently resolved from it.