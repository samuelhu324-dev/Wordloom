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
  **reference_log_4**: `docs/runbook/support-only/_template-run-ledger.md`
  **reference_log_5**: `docs/runbook/support-only/_template-run-ledger-SUP.md`
  **reference_log_6**: `docs/runbook/support-only/_template-run-ledger-PATCH.md`
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
- `P0-C1-S2` | artifact: `docs/runbook/support-only/_template-run-ledger.md`
- `P1-C1-S1` | artifact: `docs/runbook/support-only/_template-run-ledger-SUP.md`
- `P1-C1-S2` | artifact: `docs/runbook/support-only/_template-run-ledger-PATCH.md`

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

### P1-C1-S3 (Current Run Status Summary | v1)

- Add one short reader-facing summary surface near the top of the parent ledger.
- This summary should distinguish:
  - operational convergence
  - accounting status
  - approval status
  - target convergence count
  - latest chronology round
- The goal is to let one reader answer “is this run operationally done, partially done, or still open?” without reading all downstream tables first.

## P2 (Family-specific template naming and migration | v1)

### P2-C1-S1 (Family-specific template naming rule | v1)

- The current template filenames are too generic for a workflow family that already carries local structural deltas.
- For this family, append the family token as a suffix to the template filename.
- Preferred canonical names:
  - `docs/runbook/_template-run-WORKFLOW-GITHUB-ISSUES.md`
  - `docs/runbook/support-only/_template-run-ledger-WORKFLOW-GITHUB-ISSUES.md`
  - `docs/runbook/support-only/_template-run-ledger-SUP-WORKFLOW-GITHUB-ISSUES.md`
  - `docs/runbook/support-only/_template-run-ledger-PATCH-WORKFLOW-GITHUB-ISSUES.md`
- If the repo still wants generic templates later, keep them as separate generic skeletons rather than pretending the family-specific deltas do not exist.

### P2-C1-S2 (Template migration order | v1)

- Migration order should be:
  - fix chronology and table-responsibility contract;
  - create the family-specific template quartet under canonical names;
  - update the live runbook family to reference those templates;
  - backfill the current live parent ledger and bound `SUP` / `PATCH` files.
- Do not rename template files first and then discover that the structure still changes underneath them.

### P2-C1-S3 (Live write-back scope rule | v1)

- Once the family-specific templates are fixed, the first bounded write-back packet should update at least:
  - the active `WORKFLOW-GITHUB-ISSUES` runbook body;
  - the parent run ledger;
  - the `SUP` template;
  - the `PATCH` template;
  - the currently admitted `RUN-001` family packet surfaces that depend on those templates.
- The write-back should be treated as one bounded family packet, not as scattered template-only edits.

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

### P2 (Template family migration)

- P2-C1-S1: fix canonical template names for the `WORKFLOW-GITHUB-ISSUES` family
- P2-C1-S2: rewrite the live template quartet around chronology-first structure
- P2-C1-S3: define the first bounded write-back packet for runbook + templates + live `RUN-001` family surfaces

### P3 (Backfill and verify)

- P3-C1-S1: backfill `RUN-001` chronology rounds and stage attempts from `ledger`, `SUP`, and `PATCH` packets
- P3-C1-S2: verify that one reader can answer time order, stage scope, packet attribution, and current status without prose-only reconstruction

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: define `execution round` as a chronology layer distinct from run/supplement/patch sequence
- [x] `P0-C1-S2`: define `current` vs `history` table responsibilities in the parent ledger
- [x] `P0-C1-S3`: define minimum packet attribution fields for chronology-aware run accounting

### P1 (Ledger redesign)

- [ ] `P1-C1-S1`: replace ambiguous batch summary with `Execution Round Table`
- [ ] `P1-C1-S2`: add `Current Target Status Table` and `Target Stage Attempt Table`
- [ ] `P1-C1-S3`: add `Current Run Status Summary`

### P2 (Template family migration)

- [ ] `P2-C1-S1`: rename the live template quartet with `WORKFLOW-GITHUB-ISSUES` suffixes
- [ ] `P2-C1-S2`: rewrite the family-specific template quartet around chronology-first structure
- [ ] `P2-C1-S3`: define the first bounded live write-back packet for runbook + templates + `RUN-001` family surfaces

### P3 (Backfill / verify)

- [ ] `P3-C1-S1`: backfill `RUN-001` chronology rounds and stage attempts
- [ ] `P3-C1-S2`: verify that the new reader model answers time order, stage scope, packet attribution, and current status directly

## Current Status (recommended)

- `S0G-3E` is now opened as the chronology-and-template-governance successor to `S0G-3D`.
- The missing execution-round / stage-attempt layer is now the primary reader and template gap for the `WORKFLOW-GITHUB-ISSUES` family.
- `P0` is now fixed at the contract level: execution-round admission, current-vs-history split, and packet attribution are explicit enough to drive the parent-ledger redesign.
- The next step is `P1`: translate the fixed `P0` contract into concrete `Execution Round`, `Current Target Status`, `Target Stage Attempt`, and top-level run-summary surfaces before any template rename or live backfill lands.
- No live runbook/template/ledger backfill should land until `P1` fixes the parent-ledger table responsibilities against this `P0` contract.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

## Recent changes (for traceability, optional)

- 2026-04-21: Completed `P0` contract fixation for `S0G-3E`, including explicit `execution_round_id` admission rules, current-vs-history table split, packet attribution fields, and a defended `RUN-001` chronology example.
- 2026-04-21: Opened `S0G-3E` to formalize chronology-first run accounting and family-specific template governance for `WORKFLOW-GITHUB-ISSUES` after reader confusion in the active `RUN-001` ledger exposed the missing round/attempt layer.