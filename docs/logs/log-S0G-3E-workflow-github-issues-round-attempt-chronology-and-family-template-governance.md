# log-S0G-3E (Phase 3E: WORKFLOW-GITHUB-ISSUES round-attempt chronology and family-template governance)

---

**id**: `S0G-3E`
**kind**: `log`
**title**: `workflow github issues round-attempt chronology and family-template governance v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Automation, Evidence, epic/s0, sub/3e`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-3D-workflow-github-issues-file-identity-rename-and-successor-release-governance.md`
  **reference_log_1**: `docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md`
  **reference_log_2**: `docs/logs/log-S0G-3C-workflow-github-issues-strong-structure-and-ledger-bridge-governance.md`
  **reference_log_3**: `docs/logs/log-S0G-3D-workflow-github-issues-file-identity-rename-and-successor-release-governance.md`
  **reference_log_4**: `docs/runbook/_template-runbook-WORKFLOW-GITHUB-ISSUES.md`
  **reference_log_5**: `docs/runbook/support-only/_template-run-ledger-WORKFLOW-GITHUB-ISSUES.md`
  **reference_log_6**: `docs/runbook/support-only/_template-run-ledger-SUP-WORKFLOW-GITHUB-ISSUES.md`
  **reference_log_7**: `docs/runbook/support-only/_template-run-ledger-PATCH-WORKFLOW-GITHUB-ISSUES.md`
**issue_keyword**: `workflow`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/3e`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-21`
**updated**: `2026-04-21`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this packet.
- Day-level precision is acceptable while the repo is still deciding the exact execution-round vocabulary, parent-ledger table split, and family-specific template naming surface.
- `reviewed` should remain `pending` until the repo fixes one defended round/attempt chronology model and one defended template-migration plan for the `WORKFLOW-GITHUB-ISSUES` family.

## Decision / Outcome

**Decision**:

- `S0G-3E` opens the next bounded follow-up after `S0G-3D`: file identity and strong-structure bridge semantics are no longer the main reader problem; the immediate gap is that current GitHub Issues run accounting still lacks one explicit chronology layer for real execution rounds and stage attempts.
- The current parent ledger mixes three different readings into the same tables:
  - original admitted run state;
  - later `SUP` write-back and verdict sharpening;
  - current latest defended state.
- This lane must stop using repeated stable rows to express history. The defended fix is to introduce one explicit `execution round` layer and one explicit `stage attempt` layer, then separate `current` tables from `history` tables.
- `SUP` sequence, `PATCH` sequence, and `run sequence` are not interchangeable numbers. This lane must define how readers see chronological round order independently from whether one write-back packet is a `SUP` or a `PATCH` surface.
- The current `Batch Run Table` is not carrying its weight as a reader surface. This lane must either replace it with an `Execution Round Table` or remove it in favor of a clearer chronology-first surface.
- The current `Target Table` and `Target Stage Table` should stop using duplicate stable ids to represent later sharpened readings. One current row should represent one current defended state, while a separate attempt/history surface should record chronology.
- `WORKFLOW-GITHUB-ISSUES` now needs family-specific live templates rather than relying on generic run-ledger templates that then drift locally. This lane must define and then execute a naming and ownership rule for a dedicated runbook + ledger + `SUP` + `PATCH` template quartet.
- The preferred template naming direction for this family is now explicit: append the family token as a suffix so the repo can distinguish family-specific templates from generic skeletons, for example `_template-run-ledger-WORKFLOW-GITHUB-ISSUES.md` and parallel `SUP` / `PATCH` surfaces.
- This lane must also define the migration order: fix chronology contract first, then fix parent-ledger table responsibilities, then rename and rewrite the family-specific templates, and only after that backfill the live `RUN-001` / `SUP-001` / `SUP-002` / `PATCH-001` / `PATCH-002` surfaces.

**Default choices (phase defaults / v1)**:

- Treat `execution round` as the missing reader-facing chronology grain for this family.
- Treat `stage attempt` as the history grain beneath one stable target-stage row when one stage is replayed, resumed, sharpened, or repaired.
- Keep `run row id`, `target row id`, and `target stage row id` stable; do not use repeated stable rows to fake time order.
- One `current` table should hold one stable row per object. History belongs in a dedicated chronology or attempt table.
- `SUP-002` should never need to be read as “the second run” by itself; if it belongs to chronological round 3, the reader should see round 3 explicitly.
- Family-specific template files should be named for the family they actually govern.
- Rename and rewrite the `WORKFLOW-GITHUB-ISSUES` template quartet together rather than patching one template at a time.
- Do not backfill live ledgers until the chronology vocabulary and table responsibilities are stable enough to prevent a second rewrite immediately after the first one.

## PR Summary Inputs (optional)

- This packet is expected to drive chronology-first run accounting and the family-specific template rewrite for `WORKFLOW-GITHUB-ISSUES`, so review should focus on the reader model first and the template rename/write-back plan second.

**PR summary bullets**:

- Add one explicit `execution round` and `stage attempt` model so GitHub Issues run accounting can show time order, stage scope, and packet attribution without repeating stable rows.
- Split `current` state from `history` state in the parent ledger so readers can tell what is latest versus what was merely earlier admitted.
- Define and migrate a family-specific template quartet for `WORKFLOW-GITHUB-ISSUES` instead of continuing with generic run-ledger templates plus local drift.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0G-3E-workflow-github-issues-round-attempt-chronology-and-family-template-governance.md`
- Runbook: `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
- Evidence artifact: `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`

**Evidence Footer Source**:

- `P0-C1-S1` | artifact: `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
- `P0-C1-S2` | artifact: `docs/runbook/support-only/_template-run-ledger-WORKFLOW-GITHUB-ISSUES.md`
- `P1-C1-S1` | artifact: `docs/runbook/support-only/_template-run-ledger-SUP-WORKFLOW-GITHUB-ISSUES.md`
- `P1-C1-S2` | artifact: `docs/runbook/support-only/_template-run-ledger-PATCH-WORKFLOW-GITHUB-ISSUES.md`
- `P2-C1-S1` | artifact: `docs/runbook/_template-runbook-WORKFLOW-GITHUB-ISSUES.md`

## Definitions (optional)

- **execution round**: one chronological operator round for the same bounded run, such as initial full lifecycle run, later creation write-back round, or later conclusion replay round.
- **stage attempt**: one defended stage-level attempt under one stable target-stage row, including replay, retry, sharpened write-back, or repair-driven reapply.
- **current table**: one table that holds the latest defended reading only, with one row per stable object.
- **history table**: one chronology-first table that records how the latest reading was reached over time.
- **packet attribution**: the explicit link from one chronology row or attempt row back to the file surface that admitted it, such as `ledger-run-001`, `SUP-001`, `SUP-002`, `PATCH-001`, or `PATCH-002`.
- **family-specific template quartet**: the `runbook`, `run ledger`, `SUP`, and `PATCH` template files that are explicitly owned by one workflow family instead of a generic support-only template namespace.

## Constraints

- Do not use duplicate stable target or stage rows to represent chronology.
- Do not overload `SUP` sequence or `PATCH` sequence as a substitute for execution-round order.
- Do not keep one ambiguous batch table if it cannot answer when a round ran, what stages that round attempted, and which packet wrote the reading.
- Do not rename templates cosmetically without also deciding who owns the family-specific deltas and how the live runbook family will consume them.
- Do not backfill `RUN-001` before the current-vs-history split is fixed clearly enough to survive the next follow-up packet.

## Scope

- `P0`: chronology-first contract for execution rounds, stage attempts, and current-vs-history separation
- `P1`: parent-ledger redesign for `Execution Round`, `Current Target`, `Target Stage Attempt`, and run summary surfaces
- `P2`: family-specific template naming and migration plan for `WORKFLOW-GITHUB-ISSUES`
- `P3`: bounded rewrite and backfill packet for live runbook, templates, and `RUN-001` family write-back

## Success Criteria (DoD)

- One explicit rule defines `execution round` as a chronology grain distinct from `run sequence`, `SUP sequence`, and `PATCH sequence`.
- One explicit rule defines when a later stage replay or sharpened write-back should become a `stage attempt` row.
- One explicit rule states which parent-ledger tables are `current` surfaces and which are `history` surfaces.
- One explicit table model shows how readers identify first-entry round, latest-update round, source packet, stage scope attempted, and round timing.
- One explicit naming rule exists for the `WORKFLOW-GITHUB-ISSUES` family-specific template quartet.
- One explicit migration order exists for updating runbook templates, support-only templates, and live `RUN-001` / `SUP` / `PATCH` surfaces without reopening the same design question twice.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the chronology layer is explicit;
  - the current-vs-history table split is explicit;
  - the family-specific template naming rule is explicit;
  - the rewrite order for runbook/template/live-writeback is explicit enough to drive one bounded execution packet.

## P0 (Contract | v1)

### P0-C1-S1 (Execution round contract | v1)

- Add `execution_round_id` as a reader-facing chronology key beneath one stable `run_row_id`.
- `execution_round_id` should express real chronological order for the same bounded run, for example `RUN-001-R01`, `RUN-001-R02`, `RUN-001-R03`.
- `execution_round_id` must remain distinct from:
  - `run_sequence`
  - `supplement_sequence`
  - `patch_sequence`
- A later `SUP` or `PATCH` packet may participate in one execution round, but packet sequence must not be used as the chronology key by itself.
- Open a new `execution_round_id` only when the parent ledger admits a new defended chronology event for the same bounded run, for example initial lifecycle execution, later creation write-back, later conclusion replay, or a repair-driven reapply that changes the admitted reading.
- Do not open a new `execution_round_id` for packet-local housekeeping alone, such as filename cleanup, artifact relocation, or repair notes that do not change parent-ledger chronology.
- One execution round may reference one or more source packets, but one round still needs one canonical `source_round_id` and one explicit round verdict in the parent ledger.
- The first explicit contract example for the current family is:
  - `RUN-001-R01`: initial admitted lifecycle round from `ledger-run-001`
  - `RUN-001-R02`: later creation write-back round admitted from `SUP-001`
  - `RUN-001-R03`: later conclusion convergence round admitted from `SUP-002`
- `PATCH-001` and `PATCH-002` should be treated as repair surfaces first. They only become round-entry surfaces if the parent ledger admits a changed chronology reading because of that repair.

### P0-C1-S2 (Current vs history separation rule | v1)

- A parent ledger should stop mixing latest defended state and earlier admitted state in the same stable table.
- `current` tables should keep one row per stable object only.
- `history` tables should record chronology, supersession, and attempt lineage.
- If a later `SUP` sharpens one existing stage, the parent ledger should update one current reading and append one history/attempt row instead of duplicating the stable row in-place.
- The parent-ledger table responsibility split is fixed as follows:
  - `Current Run Status Summary`: `current`
  - `Current Target Status Table`: `current`
  - `Execution Round Table`: `history`
  - `Target Stage Attempt Table`: `history`
- Stable identity rows must remain singular:
  - one `run_row_id` for one bounded run
  - one `target_row_id` for one defended target
  - one `target_stage_row_id` for one defended stage slot under that target
- A later replay, sharpened conclusion, or backfilled omission must update the current row and add one history row rather than clone the stable row with a later timestamp.
- The current `Target Stage Table` should no longer be treated as a mixed surface. Under the defended split, stage chronology belongs in `Target Stage Attempt Table`, while the current target-facing result belongs in `Current Target Status Table` and the top-level summary.
- Evidence extraction and reader notes may continue to exist as support surfaces, but they must not serve as the only chronology carrier for current-vs-history decisions.

### P0-C1-S3 (Packet attribution rule | v1)

- Every current or history row that depends on later write-back must expose the packet surface that admitted that reading.
- Minimum attribution fields should include:
  - `source_packet_id`
  - `source_packet_kind`
  - `source_packet_sequence`
  - `source_round_id`
- Readers should be able to answer all of these questions from parent-ledger structure alone:
  - which file admitted this reading?
  - during which chronology round did it land?
  - was it a `ledger`, `SUP`, or `PATCH` packet?
- The minimum attribution vocabulary is fixed as:
  - `source_packet_id`: exact packet identity such as `RUN-001`, `SUP-001`, `SUP-002`, `PATCH-001`, `PATCH-002`
  - `source_packet_kind`: one of `ledger`, `SUP`, `PATCH`
  - `source_packet_sequence`: family-local ordinal such as `001`, `002`
  - `source_round_id`: chronology id such as `RUN-001-R03`
- The minimum row-level admission rule is:
  - every `history` row must carry all four attribution fields;
  - every `current` row must carry at least `latest_updated_from_packet` and `latest_updated_in_round`, and should retain `first_seen_from_packet` and `first_seen_in_round` when the object predates the latest update.
- Packet attribution must be explicit even when the same packet touches multiple stages. Readers should not have to infer packet origin from prose, nearby notes, or filename similarity.
- The first defended example mapping for the active family is:
  - creation write-back admitted from `SUP-001` should point to `source_packet_kind: SUP`, `source_packet_sequence: 001`, `source_round_id: RUN-001-R02`
  - conclusion convergence admitted from `SUP-002` should point to `source_packet_kind: SUP`, `source_packet_sequence: 002`, `source_round_id: RUN-001-R03`
  - repair-only evidence rows from `PATCH-002` may appear in evidence/support surfaces without becoming current-status rows unless the parent ledger explicitly changes an admitted stage or run reading because of that repair.

### P0-C1-S3A (Chronology admission example for `RUN-001` | v1)

- The defended chronology example for the current live family is:

| execution round id | admitted from packet | packet kind | chronology meaning | current-state effect |
| --- | --- | --- | --- | --- |
| `RUN-001-R01` | `RUN-001` | `ledger` | initial admitted child and parent lifecycle execution for the bounded batch | establishes first current rows |
| `RUN-001-R02` | `SUP-001` | `SUP` | later creation-stage write-back and parent/child binding convergence | updates current creation reading and appends history |
| `RUN-001-R03` | `SUP-002` | `SUP` | later conclusion-stage convergence, milestone correction, and dual-PR DoD sharpening | updates current conclusion reading and appends history |

- The defended attempt example under one stable stage row is:
  - stable stage row: `RUN-001-T01-STG-CONCLUSION`
  - attempt `A01`: initial conclusion reading admitted in `RUN-001-R01`
  - attempt `A02`: sharpened conclusion reading admitted in `RUN-001-R03`, marked as current and superseding `A01`
- This example fixes the reader question that the current ledger cannot answer cleanly today: the reader should see that `SUP-002` is not “another run” but the packet that admitted round `R03`, and that `R03` superseded one earlier conclusion attempt under the same stable stage row.

## P1 (Parent-ledger redesign | v1)

### P1-C1-S1 (Execution Round Table replaces ambiguous batch summary | v1)

- Replace or rewrite the current `Batch Run Table` into an `Execution Round Table`.
- One row should represent one chronology round.
- Minimum columns should include:
  - `execution round id`
  - `run row id`
  - `round sequence`
  - `entry packet id`
  - `entry packet kind`
  - `target scope`
  - `stage scope attempted`
  - `round started at`
  - `round completed at`
  - `round verdict`
  - `notes`
- This table is the canonical chronology carrier for the parent ledger. It answers when one admitted round happened, what scope it touched, and which packet opened that round.
- `Execution Round Table` should not repeat one row per target or one row per stage. Its grain is one chronology round only.
- The defended minimum row contract is:
  - `execution round id`: stable chronology key such as `RUN-001-R03`
  - `run row id`: stable bounded-run key such as `RUN-001`
  - `round sequence`: ordinal inside the run, such as `03`
  - `entry packet id`: packet that admitted the round, such as `SUP-002`
  - `entry packet kind`: `ledger`, `SUP`, or `PATCH`
  - `target scope`: concise set summary such as `T01-T04 + parent`
  - `stage scope attempted`: concise stage set such as `CONCLUSION`
  - `round started at` and `round completed at`: best defended timing for that chronology round
  - `round verdict`: `completed`, `partial`, `blocked`, `superseded`, or later family-approved equivalent
  - `notes`: bounded explanation only when the other columns are insufficient
- A later repair packet may be listed in notes or evidence, but it should not become an execution-round row unless that repair changed the admitted chronology reading.
- The first defended example shape for the current family is:

| execution round id | run row id | round sequence | entry packet id | entry packet kind | target scope | stage scope attempted | round verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-001-R01` | `RUN-001` | `01` | `RUN-001` | `ledger` | `T01-T04 + parent` | `CREATION, PR_PENDING, PR_MERGED, CONCLUSION` | `completed_with_follow_up` |
| `RUN-001-R02` | `RUN-001` | `02` | `SUP-001` | `SUP` | `T01-T04 + parent` | `CREATION` | `completed` |
| `RUN-001-R03` | `RUN-001` | `03` | `SUP-002` | `SUP` | `T01-T04` | `CONCLUSION` | `completed` |
- Under the defended redesign, the old `Batch Run Table` should either be removed or reduced to a very short current summary surface. It should not remain as a second implicit chronology table.

### P1-C1-S2 (Current Target Status Table and Target Stage Attempt Table | v1)

- The current `Target Table` should become a `Current Target Status Table` with one row per target only.
- The parent ledger should also add a `Target Stage Attempt Table` for chronology and replay history.
- Minimum target-status fields should include:
  - `first_seen_in_round`
  - `first_seen_from_packet`
  - `current_status`
  - `latest_updated_in_round`
  - `latest_updated_from_packet`
  - `latest_updated_at`
- Minimum stage-attempt fields should include:
  - `attempt id`
  - `stage row id`
  - `round id`
  - `source packet id`
  - `attempt ordinal`
  - `started at`
  - `completed at`
  - `status`
  - `blocking reason`
  - `supersedes attempt id`
  - `current?`
- `Current Target Status Table` answers one question only: what is the latest defended reading for each target right now?
- `Target Stage Attempt Table` answers the complementary history question: how did each target-stage reach that current reading over time?
- The defended current-target row contract is:
  - one row per `target_row_id`
  - no duplicate target rows to represent chronology
  - `current_status` should summarize the target as a whole, not one isolated stage
  - `latest_updated_in_round` and `latest_updated_from_packet` must point to the chronology source of the current reading
- The defended stage-attempt row contract is:
  - one row per admitted attempt beneath one stable `target_stage_row_id`
  - `attempt id` shape: `RUN-001-T01-STG-CONCLUSION-A02`
  - `attempt ordinal` is local to one stable stage row and resets for each different stage row
  - `current?` marks whether this attempt is the currently defended attempt for that stable stage row
  - `supersedes attempt id` expresses direct replacement lineage when one later attempt sharpens or replaces an earlier attempt
- Minimum current-target fields should be expanded to:
  - `target row id`
  - `target ref key`
  - `target kind`
  - `workflow profile`
  - `first_seen_in_round`
  - `first_seen_from_packet`
  - `current_status`
  - `current_stage_completion`
  - `latest_updated_in_round`
  - `latest_updated_from_packet`
  - `latest_updated_at`
  - `notes`
- Minimum stage-attempt fields should be expanded to:
  - `attempt id`
  - `target row id`
  - `stage row id`
  - `stage name`
  - `round id`
  - `source packet id`
  - `source packet kind`
  - `attempt ordinal`
  - `started at`
  - `completed at`
  - `status`
  - `blocking reason`
  - `supersedes attempt id`
  - `current?`
  - `notes`
- The first defended current-target example for the active family is:

| target row id | target ref key | current_status | current_stage_completion | latest_updated_in_round | latest_updated_from_packet |
| --- | --- | --- | --- | --- | --- |
| `RUN-001-T01` | `S4F-2A` | `converged` | `CREATION, PR_PENDING, PR_MERGED, CONCLUSION` | `RUN-001-R03` | `SUP-002` |
| `RUN-001-T02` | `S4F-2B` | `converged` | `CREATION, PR_PENDING, PR_MERGED, CONCLUSION` | `RUN-001-R03` | `SUP-002` |

- The first defended stage-attempt example for the active family is:

| attempt id | stage row id | round id | source packet id | attempt ordinal | status | supersedes attempt id | current? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-001-T01-STG-CONCLUSION-A01` | `RUN-001-T01-STG-CONCLUSION` | `RUN-001-R01` | `RUN-001` | `01` | `partial` | `` | `no` |
| `RUN-001-T01-STG-CONCLUSION-A02` | `RUN-001-T01-STG-CONCLUSION` | `RUN-001-R03` | `SUP-002` | `02` | `completed` | `RUN-001-T01-STG-CONCLUSION-A01` | `yes` |

- Old-to-new mapping is fixed as:
  - old `Target Table` current meaning moves to `Current Target Status Table`
  - old `Target Stage Table` chronology meaning moves to `Target Stage Attempt Table`
  - any target-stage facts that are only current-state summaries should be rolled up into `current_stage_completion` or the top-level run summary rather than duplicated in both places

### P1-C1-S3 (Current Run Status Summary | v1)

- Add one short reader-facing summary surface near the top of the parent ledger.
- This summary should distinguish:
  - operational convergence
  - accounting status
  - approval status
  - target convergence count
  - latest chronology round
- The goal is to let one reader answer “is this run operationally done, partially done, or still open?” without reading all downstream tables first.
- This summary is a `current` surface, not a history log. It should present only the latest defended reading for the bounded run.
- The defended minimum fields are:
  - `run row id`
  - `operational convergence`
  - `accounting status`
  - `approval status`
  - `target convergence count`
  - `target partial count`
  - `target blocked count`
  - `latest chronology round`
  - `latest updated from packet`
  - `reader verdict`
  - `notes`
- `operational convergence` answers whether the operated GitHub issue family has reached the claimed lifecycle state.
- `accounting status` answers whether parent ledger, `SUP`, `PATCH`, evidence rows, and current/history write-back are structurally caught up enough for defended reading.
- `approval status` remains the governance decision state and must not be used as a substitute for operational completion.
- `reader verdict` is the one-line answer for readers who do not want to reconstruct the run from all downstream tables, for example `operationally converged; accounting backfill in progress` or `operationally and accountingly converged`.
- The first defended example shape for the active family is:

| run row id | operational convergence | accounting status | approval status | target convergence count | latest chronology round | latest updated from packet | reader verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-001` | `converged` | `converged_with_follow_up_packets` | `pending` | `4/4` | `RUN-001-R03` | `SUP-002` | `operationally converged; chronology-first parent-ledger redesign still pending` |

- Placement rule is fixed as:
  - place `Current Run Status Summary` near the top of the parent ledger, ahead of chronology/history tables
  - place `Execution Round Table` next, because it is the shortest path from current state to defended chronology
  - place `Current Target Status Table` after that
  - place `Target Stage Attempt Table` after current target status
  - keep evidence/support tables later in the file

### P1-C1-S4 (Parent-ledger surface order and migration rule | v1)

- The defended parent-ledger surface order is:
  - `Current Run Status Summary`
  - `Execution Round Table`
  - `Current Target Status Table`
  - `Target Stage Attempt Table`
  - evidence/support tables
- Migration from the current parent ledger should follow this order:
  - rewrite the top-level run summary first so readers stop depending on the old batch table for current state
  - rewrite chronology into `Execution Round Table`
  - roll the old target table into `Current Target Status Table`
  - convert replay/sharpened stage history into `Target Stage Attempt Table`
  - only after those four surfaces are stable should the repo rewrite template examples and live family templates
- `P1` is considered fixed when one reader can answer all of these without prose reconstruction:
  - what is the current defended run state?
  - what chronology rounds happened and in what order?
  - what is the current defended state of each target?
  - which stage attempt is current, and which attempt did it supersede?

## P2 (Family-specific template naming and migration | v1)

### P2-C1-S1 (Family-specific template naming rule | v1)

- The current template filenames are too generic for a workflow family that already carries local structural deltas.
- For this family, append the family token as a suffix to the template filename.
- Preferred canonical names:
  - `docs/runbook/_template-runbook-WORKFLOW-GITHUB-ISSUES.md`
  - `docs/runbook/support-only/_template-run-ledger-WORKFLOW-GITHUB-ISSUES.md`
  - `docs/runbook/support-only/_template-run-ledger-SUP-WORKFLOW-GITHUB-ISSUES.md`
  - `docs/runbook/support-only/_template-run-ledger-PATCH-WORKFLOW-GITHUB-ISSUES.md`
- If the repo still wants generic templates later, keep them as separate generic skeletons rather than pretending the family-specific deltas do not exist.
- The runbook template must use the existing repo naming grammar. The canonical family-specific runbook template is therefore `_template-runbook-WORKFLOW-GITHUB-ISSUES.md`, not a newly invented `_template-run-...` stem.
- The defended quartet ownership split is:
  - `docs/runbook/_template-runbook.md`: generic skeleton only
  - `docs/runbook/support-only/_template-run-ledger.md`: generic parent-ledger skeleton only
  - `docs/runbook/support-only/_template-run-ledger-SUP.md`: generic SUP skeleton only
  - `docs/runbook/support-only/_template-run-ledger-PATCH.md`: generic PATCH skeleton only
  - `docs/runbook/_template-runbook-WORKFLOW-GITHUB-ISSUES.md`: family-specific runbook authority for this workflow family
  - `docs/runbook/support-only/_template-run-ledger-WORKFLOW-GITHUB-ISSUES.md`: family-specific parent-ledger authority
  - `docs/runbook/support-only/_template-run-ledger-SUP-WORKFLOW-GITHUB-ISSUES.md`: family-specific SUP authority
  - `docs/runbook/support-only/_template-run-ledger-PATCH-WORKFLOW-GITHUB-ISSUES.md`: family-specific PATCH authority
- Generic skeletons may remain in the repo, but the active `WORKFLOW-GITHUB-ISSUES` family should stop deriving live structure from those generic files once the family-specific quartet is created.
- The family-specific quartet is justified because the current family already has defended deltas in all four surfaces:
  - long-path family naming narrowed to `WORKFLOW-GITHUB-ISSUES`
  - chronology-first `Execution Round` and `Target Stage Attempt` requirements
  - strong-structure run/target/stage/attempt bridge keys
  - explicit `SUP` and `PATCH` dual-surface write-back behavior
- The first defended template-ownership mapping is:

| surface role | generic skeleton retained? | family-specific authority required? | canonical family-specific path |
| --- | --- | --- | --- |
| runbook | `yes` | `yes` | `docs/runbook/_template-runbook-WORKFLOW-GITHUB-ISSUES.md` |
| parent ledger | `yes` | `yes` | `docs/runbook/support-only/_template-run-ledger-WORKFLOW-GITHUB-ISSUES.md` |
| SUP ledger | `yes` | `yes` | `docs/runbook/support-only/_template-run-ledger-SUP-WORKFLOW-GITHUB-ISSUES.md` |
| PATCH ledger | `yes` | `yes` | `docs/runbook/support-only/_template-run-ledger-PATCH-WORKFLOW-GITHUB-ISSUES.md` |

### P2-C1-S2 (Template migration order | v1)

- Migration order should be:
  - fix chronology and table-responsibility contract;
  - create the family-specific template quartet under canonical names;
  - update the live runbook family to reference those templates;
  - backfill the current live parent ledger and bound `SUP` / `PATCH` files.
- Do not rename template files first and then discover that the structure still changes underneath them.
- The defended migration sequence is fixed as:
  - preserve the current generic skeleton templates in place;
  - create the family-specific quartet under the canonical names above;
  - copy only the reusable generic baseline into each family-specific template, then apply the `WORKFLOW-GITHUB-ISSUES` deltas from `P0` and `P1`;
  - update template examples, naming examples, and ledger-binding examples so they reference `WORKFLOW-GITHUB-ISSUES-001` rather than the compatibility-era family token;
  - update the active live runbook body and live `RUN-001` family packet surfaces only after the family-specific quartet is internally consistent.
- The repo should not physically rename the generic skeleton templates into family-specific templates. They serve different roles after this lane:
  - generic skeletons remain cross-family starting points;
  - family-specific templates become the authoritative source for this one workflow family.
- The defended migration dependency rule is:
  - the family-specific runbook template must land with the family-specific parent-ledger template in the same bounded packet;
  - the family-specific SUP and PATCH templates must land in that same packet or immediately adjacent packet only if review explicitly needs a split;
  - do not ship one isolated template first, because the quartet shares one ledger-binding and chronology contract.
- The first migration check must verify that all four family-specific templates encode the same structural vocabulary:
  - `WORKFLOW-GITHUB-ISSUES` family token
  - `RUN-001` / `target_row_id` / `target_stage_row_id` / optional `attempt id` grammar
  - `execution round` terminology
  - `current` versus `history` table split in the parent-ledger surface
- The defended template rewrite sequence inside that bounded packet is:
  - family-specific runbook template
  - family-specific parent-ledger template
  - family-specific SUP template
  - family-specific PATCH template
  - live example references that depend on those templates

### P2-C1-S3 (Live write-back scope rule | v1)

- Once the family-specific templates are fixed, the first bounded write-back packet should update at least:
  - the active `WORKFLOW-GITHUB-ISSUES` runbook body;
  - the parent run ledger;
  - the `SUP` template;
  - the `PATCH` template;
  - the currently admitted `RUN-001` family packet surfaces that depend on those templates.
- The write-back should be treated as one bounded family packet, not as scattered template-only edits.
- The defended live write-back scope for the first post-template packet is:
  - active runbook body: `run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
  - active parent ledger: `ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
  - active `SUP` packet surfaces currently admitted under that family
  - active `PATCH` packet surfaces currently admitted under that family
  - any exact-path template examples or header snippets that would otherwise keep teaching the old structure
- The first post-template packet should not reopen compatibility-era `WORKFLOW-GITHUB-001` bodies except where an exact-path stub, lineage note, or bounded compatibility landing is still required by the earlier identity-governance lane.
- The defended live write-back order is:
  - rewrite the live runbook binding first so readers know the authoritative family surface;
  - rewrite the parent ledger next using the new current/history model;
  - rewrite the admitted `SUP` and `PATCH` files so they bind cleanly to the new parent-ledger structure;
  - only then update downstream examples, summaries, and reference notes that quote those live files.
- The first bounded packet must be reviewable as one family migration unit. It should let a reviewer answer all of these without cross-packet reconstruction:
  - which template files are now authoritative for `WORKFLOW-GITHUB-ISSUES`?
  - which live files were rewritten because of that template change?
  - which compatibility-era files, if any, remain as stubs or lineage landings only?
- The defended no-split rule is:
  - do not land template creation in one commit and live family write-back in a distant later commit without an explicit bounded successor packet;
  - if review needs a split, the second packet must be the immediate successor and must reference the first packet as the template-authority source.

### P2-C1-S4 (Template authority and compatibility rule | v1)

- After `P2` lands, the repo should treat the family-specific quartet as the only authoritative template source for newly opened `WORKFLOW-GITHUB-ISSUES` artifacts.
- Generic templates remain available for other families and as reduced skeletons, but they should stop being cited as the decisive source for `WORKFLOW-GITHUB-ISSUES` examples, docs, or future packet generation.
- Compatibility-era live files under `WORKFLOW-GITHUB-001` remain governed by the earlier identity lane; `P2` does not itself decide whether they are deleted, stubbed, or retained long-term.
- `P2` is considered fixed when one reviewer can answer all of these directly from the repo structure:
  - what are the canonical template paths for the `WORKFLOW-GITHUB-ISSUES` family?
  - which generic templates remain as generic skeletons only?
  - what is the exact migration order from template authority to live file rewrite?
  - what is the bounded scope of the first post-template live write-back packet?

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- Source-log work inside this lane uses `S0G-3E/P<phase>-C<cycle>-S<steps>: <summary>`.
- Later implementation work driven by this lane may still use the same source-log naming until the family-specific template packet is separated into its own extraction unit.

**Branch convention**:

- Keep this lane on the active `S0G-*` docs-management branch until the chronology contract and template migration order are fixed.
- Do not split template renames away from the contract work if the reader model is still changing.

**Commit discipline (recommended)**:

- Stabilize chronology vocabulary first.
- Then land the family-specific template rename and structure rewrite.
- Then backfill the live `RUN-001` family surfaces under the same bounded execution packet or the immediately adjacent packet if review needs a split.

## Plan (draft)

### P0 (Chronology contract)

- P0-C1-S1: define `execution round` as a chronology layer distinct from run/supplement/patch sequence
- P0-C1-S2: define `current` vs `history` parent-ledger table responsibilities
- P0-C1-S3: define packet attribution fields required for current and history rows

### P1 (Ledger redesign)

- P1-C1-S1: replace ambiguous batch summary with `Execution Round Table`
- P1-C1-S2: split target current state from stage-attempt chronology
- P1-C1-S3: add one top-level current run summary surface
- P1-C1-S4: fix parent-ledger surface order and migration sequence for live rewrite

### P2 (Template family migration)

- P2-C1-S1: fix canonical template names for the `WORKFLOW-GITHUB-ISSUES` family
- P2-C1-S2: rewrite the live template quartet around chronology-first structure
- P2-C1-S3: define the first bounded write-back packet for runbook + templates + live `RUN-001` family surfaces
- P2-C1-S4: fix template authority and compatibility boundaries after family-specific migration

### P3 (Backfill and verify)

- P3-C1-S1: backfill `RUN-001` chronology rounds and stage attempts from `ledger`, `SUP`, and `PATCH` packets
- P3-C1-S2: verify that one reader can answer time order, stage scope, packet attribution, and current status without prose-only reconstruction
- P3-C1-S3: create the family-specific template quartet and wire live runbook authority to it
- P3-C1-S4: rewrite live `RUN-001` family surfaces as one bounded chronology-first packet

## P4 (SUP delta-first supplement model | v1)

### P4-C1-S1 (SUP packet-round summary rule | v1)

- A `SUP` ledger for this family must do more than admit evidence; it must also explain one defended round-level delta against the parent ledger.
- Every `SUP` packet should expose one short `Packet Round Summary` surface near the top of the file.
- The grain of `Packet Round Summary` is one supplement packet, not one target and not one evidence attachment.
- Minimum fields should include:
  - `supplement id`
  - `source_round_id`
  - `round sequence`
  - `parent run row id`
  - `target scope`
  - `stage scope`
  - `packet verdict`
  - `current-state effect`
  - `notes`
- This surface exists so a reader can answer all of these without opening the parent ledger first:
  - which chronology round is this packet part of?
  - which targets and stages did it touch?
  - did it sharpen current state, reopen state, or merely append evidence?

### P4-C1-S2 (SUP stage-delta table rule | v1)

- The existing `Evidence Table` in a `SUP` ledger is not sufficient by itself for this family because it admits proof but does not fully explain the before-and-after effect on one stage reading.
- A `SUP` ledger for this family should therefore expose one dedicated `Stage Delta Table` in addition to evidence admission.
- The grain of `Stage Delta Table` is one target-stage change admitted by this `SUP` packet.
- Minimum fields should include:
  - `supplement item id`
  - `target row id`
  - `target stage row id`
  - `source_round_id`
  - `prior_attempt_id`
  - `new_attempt_id`
  - `new_attempt_ordinal`
  - `prior_stage_status`
  - `new_stage_status`
  - `prior_blocking_reason`
  - `new_blocking_reason`
  - `effect_on_current_target_status`
  - `parent_ledger_writeback`
  - `primary_evidence_ref`
  - `notes`
- `Stage Delta Table` should answer the questions that the parent ledger answers globally but that a `SUP` packet must answer locally for its own round:
  - was this the second or third admitted attempt for this stage?
  - what did the prior defended stage reading say?
  - what is the newly admitted stage reading?
  - what exact parent-ledger change should follow from this packet?
- `new_attempt_ordinal` is local to the stable `target_stage_row_id`; it is not the same as `round sequence`.
- A stage should reach ordinal `03` only if that same stage row is admitted again in a third distinct round. The existence of `RUN-001-R03` alone does not force every stage to reach `A03`.

### P4-C1-S3 (SUP evidence-table boundary rule | v1)

- `Evidence Table` should remain in the `SUP` ledger, but its role should be narrowed to evidence admission, attachment review, and verification support.
- `Evidence Table` should stop carrying the full burden of explaining ledger delta by itself.
- The defended role split is:
  - `Packet Round Summary`: packet-level chronology and scope
  - `Stage Delta Table`: target-stage before/after delta and parent-ledger effect
  - `Evidence Table`: proof, attachments, verification status, and retained evidence references
- If one `SUP` packet only appends evidence and does not change current stage reading, `Stage Delta Table` may still exist with explicit `no-current-state-change` rows rather than disappearing entirely.

### P4 (SUP delta-first follow-up)

- P4-C1-S1: fix the `SUP` packet contract so each supplement exposes packet-level chronology and per-stage before/after delta
- P4-C1-S2: rewrite the family-specific `SUP` template around `Packet Round Summary`, `Stage Delta Table`, and narrowed evidence support
- P4-C1-S3: backfill live `SUP-001` and `SUP-002` so readers can see round sequence, attempt lineage, and parent-ledger writeback directly from the packet

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: define `execution round` as a chronology layer distinct from run/supplement/patch sequence
- [x] `P0-C1-S2`: define `current` vs `history` table responsibilities in the parent ledger
- [x] `P0-C1-S3`: define minimum packet attribution fields for chronology-aware run accounting

### P1 (Ledger redesign)

- [x] `P1-C1-S1`: replace ambiguous batch summary with `Execution Round Table`
- [x] `P1-C1-S2`: add `Current Target Status Table` and `Target Stage Attempt Table`
- [x] `P1-C1-S3`: add `Current Run Status Summary`
- [x] `P1-C1-S4`: fix parent-ledger surface order and migration sequence for live rewrite

### P2 (Template family migration)

- [x] `P2-C1-S1`: rename the live template quartet with `WORKFLOW-GITHUB-ISSUES` suffixes
- [x] `P2-C1-S2`: rewrite the family-specific template quartet around chronology-first structure
- [x] `P2-C1-S3`: define the first bounded live write-back packet for runbook + templates + `RUN-001` family surfaces
- [x] `P2-C1-S4`: fix template authority and compatibility boundaries after family-specific migration

### P3 (Backfill / verify)

- [x] `P3-C1-S1`: backfill `RUN-001` chronology rounds and stage attempts
- [x] `P3-C1-S2`: verify that the new reader model answers time order, stage scope, packet attribution, and current status directly
- [x] `P3-C1-S3`: create the family-specific template quartet and wire live runbook authority to it
- [x] `P3-C1-S4`: rewrite live `RUN-001` family surfaces as one bounded chronology-first packet

### P4 (SUP delta-first follow-up)

- [x] `P4-C1-S1`: fix the `SUP` packet contract so each supplement exposes packet-level chronology and per-stage before/after delta
- [x] `P4-C1-S2`: rewrite the family-specific `SUP` template around `Packet Round Summary`, `Stage Delta Table`, and narrowed evidence support
- [x] `P4-C1-S3`: backfill live `SUP-001` and `SUP-002` so readers can see round sequence, attempt lineage, and parent-ledger writeback directly from the packet

## Current Status (recommended)

- `S0G-3E` is now opened as the chronology-and-template-governance successor to `S0G-3D`.
- The missing execution-round / stage-attempt layer is now the primary reader and template gap for the `WORKFLOW-GITHUB-ISSUES` family.
- `P0` is now fixed at the contract level: execution-round admission, current-vs-history split, and packet attribution are explicit enough to drive the parent-ledger redesign.
- `P1` is now fixed at the parent-ledger model level: the chronology table, current target table, stage-attempt table, top-level run summary, and surface order are explicit enough to drive template migration.
- `P2` is now fixed at the template-governance level: the family-specific quartet names, ownership boundaries, migration order, compatibility boundary, and first live write-back scope are explicit enough to drive one bounded implementation packet.
- `P3` is now executed as one bounded family packet: the `WORKFLOW-GITHUB-ISSUES` template quartet exists, the live runbook points to that quartet, the parent ledger now separates current state from chronology history, and the active `SUP` / `PATCH` packets are aligned to the new read model.
- `P4` is now fixed as the first post-`P3` follow-up under `S0G-3E`: `SUP` packets for this family now expose packet-level chronology plus per-stage delta, the family-specific `SUP` template teaches that structure, and live `SUP-001` / `SUP-002` now explain round-versus-attempt semantics locally instead of forcing readers back to the parent ledger.
- The immediate next step is no longer to reinterpret `SUP` packets; it is optional downstream adoption work, such as mirroring the same delta-first discipline into any future family-specific `PATCH` packet that changes admitted chronology, or adding cross-links from the parent ledger into the new `SUP` delta rows.
- No further live backfill should bypass the family-specific quartet, because template authority and live write-back scope are now fixed together.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

## Recent changes (for traceability, optional)

- 2026-04-22: Executed `P4` delta-first SUP follow-up under `S0G-3E`, fixing the `SUP` contract, rewriting the family-specific `SUP` template around `Packet Round Summary` and `Stage Delta Table`, and backfilling live `SUP-001` / `SUP-002` so round sequence and stage-attempt lineage are explicit inside each packet.
- 2026-04-21: Executed the first post-`P3` adoption cleanup for `S0G-3E`, switching this governance log's decisive template references to the `WORKFLOW-GITHUB-ISSUES` quartet and removing family-specific teaching examples from the generic runbook and ledger skeletons.
- 2026-04-21: Executed `P3` bounded implementation for `S0G-3E`, creating the `WORKFLOW-GITHUB-ISSUES` family-specific template quartet, wiring live runbook template authority, rewriting `RUN-001` into current/history surfaces, and aligning active `SUP` / `PATCH` packet notes with the chronology-first model.
- 2026-04-21: Completed `P2` template-governance contract for `S0G-3E`, fixing the `WORKFLOW-GITHUB-ISSUES` family-specific quartet names, generic-versus-family authority split, migration order, compatibility boundary, and first live write-back scope.
- 2026-04-21: Completed `P1` parent-ledger redesign contract for `S0G-3E`, fixing `Current Run Status Summary`, `Execution Round Table`, `Current Target Status Table`, `Target Stage Attempt Table`, and the surface-order migration rule.
- 2026-04-21: Completed `P0` contract fixation for `S0G-3E`, including explicit `execution_round_id` admission rules, current-vs-history table split, packet attribution fields, and a defended `RUN-001` chronology example.
- 2026-04-21: Opened `S0G-3E` to formalize chronology-first run accounting and family-specific template governance for `WORKFLOW-GITHUB-ISSUES` after reader confusion in the active `RUN-001` ledger exposed the missing round/attempt layer.