# ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter

```yaml
support_only_contract_release_ledger:
  ledger_id: ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter
  ledger_kind: support-only-contract-release-ledger
  status: draft
  owner_lane: S0F-7C
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
- This ledger is intentionally a first routing draft only; no `S0B-3A` slice is marked consumed yet because the receiving child contracts do not exist in workspace yet.

## Routing And Consumption Table

| source slice | meaning owned here | target family | target release action | contract lineage impact | retained-only action | resolution status | resolved by contract id | consumed scope | resolution notes | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1) Unified indices` in [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md) | logs-facing workflow identifiers, title identity grammar, and index-entry semantics for structured log intake | `DOC-WORKFLOW-LOGS` | `new-family` | `none-source-only` | `keep-in-log` | `draft` | `none` | `none` | first child extraction should route this slice into the logs-oriented candidate rather than widen immediately into a generalized workflow parent | Although unified identifiers later span more than logs, this earliest owned wording is still logs-facing enough that the first extraction stays narrow. |
| `3) Front matter` in [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md) | mechanically managed metadata fields as first stated in a logs-facing operational surface | `DOC-WORKFLOW-LOGS` | `new-family` | `none-source-only` | `keep-in-log` | `draft` | `none` | `none` | first extraction keeps this slice in the logs-oriented child while later widening into a broader parent or sibling-spanning family remains explicitly reserved | This row is intentionally narrow on first extraction so the repo does not over-generalize front matter before repeated cross-kind evidence proves the wider parent shape. |
| `2) Legacy taxonomy` in [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md) | classify, freeze, and explicitly reference legacy material without forcing immediate rewrite or deletion | `DOC-WORKFLOW-LIFECYCLE` | `new-family` | `none-source-only` | `keep-in-log` | `draft` | `none` | `none` | first extraction should route this slice into the lifecycle-oriented child because it owns the durable legacy management boundary rather than a logs-only mechanism | This slice also sharpens how earlier `S0B-2A` legacy and cutover material may later be re-routed from support-only into the same lifecycle family. |
| `4) Cutover & Stub` logs-intake sub-slice in [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md) | from the cutover boundary onward, new structured log content must follow the new identifier, title, and logs-facing metadata discipline | `DOC-WORKFLOW-LOGS` | `new-family` | `none-source-only` | `keep-in-log` | `draft` | `none` | `none` | this row is one same-source split from the broader cutover wording and should travel with the logs child rather than remain entangled with lifecycle-only meaning | The ledger intentionally splits cutover before any explicit multi-consumption model so the logs intake rule can be judged independently. |
| `4) Cutover & Stub` lifecycle-boundary sub-slice in [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md) | legacy material remains frozen by default, and only re-enters the active system through migration-on-demand under the new management boundary | `DOC-WORKFLOW-LIFECYCLE` | `new-family` | `none-source-only` | `keep-in-log` | `draft` | `none` | `none` | this row is the paired same-source cutover split that should move with lifecycle ownership rather than logs intake mechanics | This is the lifecycle half of the same cutover source text; the split is deliberate so later consumption can stay explicit. |
| `4) Cutover & Stub` stub-preservation sub-slice in [log-S0B-3A-unified-indices-legacy taxonomy -front matter.md](d:/Project/wordloom-v3/docs/logs/log-S0B-3A-unified-indices-legacy%20taxonomy%20-front%20matter.md) | preserve old links and old entry paths through stub documents when active material moves into the new managed system | `DOC-WORKFLOW-LIFECYCLE` | `new-family` | `none-source-only` | `keep-in-log` | `draft` | `none` | `none` | first extraction should route stub preservation with lifecycle ownership because it governs how legacy material survives relocation without re-entering the active body directly | Stub preservation is grouped with lifecycle rather than logs because its primary concern is continuity across movement and freeze boundaries, not log-body structure itself. |

## First Draft Outcome

- The first `S0B-3A` routing draft now expects two new child-family candidates:
  - `DOC-WORKFLOW-LOGS-0001`
  - `DOC-WORKFLOW-LIFECYCLE-0001`
- No slice is yet marked `applied` because the receiving child contracts have not been drafted yet.
- The cutover wording is intentionally represented as two separate same-source rows:
  - one logs-intake rule
  - one lifecycle-boundary rule

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

- unified indices
- front matter
- legacy taxonomy
- cutover as logs intake rule
- cutover as lifecycle boundary
- stub preservation

## Deferred Slices

- whether front matter should later widen beyond `DOC-WORKFLOW-LOGS-0001` into a broader parent or sibling-spanning workflow surface
- whether earlier mixed packets such as `S0B-2A` now need partial ledger repair so their legacy and cutover rows can re-route cleanly into `DOC-WORKFLOW-LIFECYCLE`
- whether explicit multi-consumption support is ever needed after narrow same-source splitting is attempted first

## Reader Notes

- This ledger is intentionally a routing draft, not a final adjudication.
- The immediate review target is whether the slicing itself is right:
  - whether `LOGS` owns the correct narrow first-pass body
  - whether `LIFECYCLE` owns the correct narrow first-pass body
  - whether the two cutover rows are split at the right boundary