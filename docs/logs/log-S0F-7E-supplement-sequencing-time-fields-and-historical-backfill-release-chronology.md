# log-S0F-7E (Phase 7E: supplement sequencing time fields and historical backfill release chronology)

---

**id**: `S0F-7E`
**kind**: `log`
**title**: `supplement sequencing time fields and historical backfill release chronology`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Ledger, Records, Evidence, epic/s0, sub/7e`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-7D-ledger-supplement-admission-and-old-log-continuation.md`
  **reference_log_1**: `docs/logs/log-S0F-7D-ledger-supplement-admission-and-old-log-continuation.md`
  **reference_log_2**: `docs/governance/contracts/_template-contract-record.md`
  **reference_log_3**: `docs/logs/_template-support-only-contract-release-ledger.md`
  **reference_log_4**: `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
  **reference_log_5**: `docs/logs/_template-log-phase-drills-evidence.md`
**issue_keyword**: `records`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/7`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-12`
**updated**: `2026-04-12`

---

## Decision / Outcome

**Decision**:

- `S0F-7E` opens as the bounded follow-up after `S0F-7D` for four coupled chronology problems that `7D` exposed but did not yet fix: repeated supplement rounds on one parent source, artifact-lifecycle time versus historical-effective time, historical-backfill contract releases, and reader-safe chronology views that do not require family renumbering.
- This lane exists because `7D` proved parent-ledger-first supplement admission, but later review now needs a stricter second layer: each supplement round must stay separately identifiable, each artifact class must expose its own lifecycle timestamps, and historical backfill must not force renumbering or rewrite of already-admitted family releases.

**Default choices (phase defaults / v1)**:

- Treat supplement sequence identity as append-only within one parent source series; do not reuse one unnumbered supplement file for multiple later evidence rounds.
- Separate artifact-lifecycle timestamps from historical-effective timestamps; do not overload one `created` or `reviewed` field to mean both repository admission time and real historical rule time.
- Treat contract release ids as append-only registry ids, not as guaranteed historical-first ordering.
- Prefer explicit `historical-backfill` release handling plus lineage write-back over any attempt to renumber already-admitted family releases.
- Keep this lane focused on chronology contract and field rules first; do not widen immediately into global view automation until the timestamp and backfill model is fixed.

## Problem Statement

- `S0F-7D` now allows multiple rounds of later evidence admission, but the current supplement naming shape still risks mixing unrelated rounds into one file when the same parent source needs repeated supplementation.
- The current ledger and contract shapes also blur at least two distinct time meanings:
  - when a file or review artifact was created, reviewed, accepted, or written back in the repo
  - when the governed rule or historical state actually first became effective or stopped being effective
- Without a stricter model, later historical archaeology such as a pre-`LABS-0001` packet will force one false choice:
  - either renumber existing family releases
  - or lose the earlier history because the current numbering system cannot represent backfilled chronology safely
- The repo therefore needs one bounded lane that answers four questions before more backfill work continues broadly:
  - how repeated supplement rounds on one parent source are named and sequenced
  - which minimum time fields belong on ledgers, supplement ledgers, and contract releases
  - how one historical-backfill release may be admitted without renumbering later already-admitted family releases
  - how future reader views should distinguish registry order, recorded order, and effective historical order

## Exported Sections / Outlet Ownership

- This slice starts as one `contract-template + support-only ledger model + log-retained core` chronology-design lane.
- The expected landing is one fixed supplement-sequencing rule, one minimum timestamp-field set by artifact type, one historical-backfill release rule, and one explicit chronology-reading rule for future views.

**Outlet ownership**:

- `contract`: expected landing surface for contract-template chronology field rules once the lane is ready to write them
- `runbook`: no-op by default; operator procedure should wait until the chronology rules are stabilized
- `view`: no-op by default; the lane should first fix chronology semantics before emitting a reader-facing history view contract
- `index/front-door`: no-op by default
- `disposition/placement`: support-only ledger and supplement-ledger templates are the expected mutable landing surfaces for sequence and time-field rules
- `log-retained core`: expected landing surface for the lane boundary, chronology decisions, field rules, and evidence

## Definitions (optional)

- `supplement series id`: the stable unchanging family id for repeated supplement rounds on one parent source, for example `ledger-SUP-S0A-2A`.
- `supplement sequence`: the append-only round number inside one supplement series, for example `001`, `002`, or `003`.
- `artifact-lifecycle time`: repository-side timestamps such as file creation, review, acceptance, and write-back completion.
- `historical-effective time`: the real-world or source-historical time when a rule or contract state first became effective or ceased to apply.
- `historical-backfill release`: a later-recorded contract release that documents an earlier historical state without renumbering already-admitted later family releases.
- `registry order`: append-only contract-release numbering order inside one family.
- `recorded order`: the order in which records were actually created or admitted in the repo.
- `effective order`: the order in which rule states became historically effective.

## Constraints

- Do not renumber already-admitted family releases only because earlier history is discovered later.
- Do not let one supplement file accumulate multiple unrelated evidence rounds once separate review questions or write-back outcomes exist.
- Do not treat one timestamp field as sufficient for both repo-admission chronology and historical-effective chronology.
- Do not push chronology complexity into future views before the source records expose stable sequence and time semantics.
- Do not require every old source file to become a first-class contract release; evidence-only or support-only placement remains valid when direct rule ownership is not strong enough.

## Scope

- `P0`: open `S0F-7E`, fix the chronology problem statement after `7D`, and state why supplement sequencing and backfill chronology require their own bounded lane
- `P1`: define supplement-series naming, append-only sequence numbering, and minimum lifecycle fields for parent ledgers and supplement ledgers
- `P2`: define the minimum chronology fields for contracts, including registry order, recorded order, and historical-effective order
- `P3`: define the historical-backfill release rule, including how later-discovered earlier states enter a family without renumbering existing releases
- `P4`: define the downstream chronology-reading rule for future views, including how registry, recorded, and effective order should coexist without reader confusion

## Success Criteria (DoD)

- The repo has one explicit rule for repeated supplement rounds named as sequence-bearing files rather than as one unbounded supplement bucket.
- The repo has one minimum field set that distinguishes artifact-lifecycle time from historical-effective time across ledgers, supplement ledgers, and contracts.
- The repo has one explicit historical-backfill release rule that preserves existing family numbering.
- The repo has one explicit downstream reading rule stating how future views should sort registry order, recorded order, and effective order independently.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` have fixed supplement sequencing, minimum chronology fields, and the historical-backfill rule;
  - `P4` has either fixed the minimum downstream chronology-reading rule or explicitly deferred it into a narrower later follow-up.

## P0 (Lane boundary | v1)

### P0-C1-S1 (Chronology follow-up lane opened after supplement-ledger admission | v1)

- `S0F-7E` is now the bounded follow-up after `7D` for supplement sequencing, time-field separation, and historical-backfill chronology.
- Under this rule, `7D` remains the admission lane, while `7E` owns the next chronology-safe expansion of that model.

### P0-C1-S2 (Append-only family numbering preserved by default | v1)

- Already-admitted contract family release ids should remain append-only registry ids.
- Under this rule, later-discovered earlier history must not automatically force renumbering of `0001`, `0002`, `0003`, or later family releases.

### P0-C1-S3 (Three chronology layers distinguished up front | v1)

- The repo should now distinguish:
  - artifact-lifecycle chronology
  - recorded chronology
  - historical-effective chronology
- Under this rule, one later field design or view model must not collapse these into one ambiguous ordering surface.

## P1 (Supplement sequence and artifact-lifecycle fields | v1)

### P1-C1-S1 (Supplement series id and append-only sequence naming fixed | v1)

- Repeated supplement rounds attached to one parent source must now use one stable supplement series plus one append-only sequence-bearing file name.
- Under this rule:
  - the stable series id is `ledger-SUP-<source-id>`
  - the on-disk file id is `ledger-SUP-<source-id>-<sequence>-<source-summary>.md`
  - the `<sequence>` must use three-digit append-only numbering such as `001`, `002`, or `003`
  - later rounds may not reuse or rename earlier sequence numbers once one supplement file has been admitted into repo history

### P1-C1-S2 (Minimum lifecycle fields for parent ledgers and supplement ledgers fixed | v1)

- Parent ledgers and supplement ledgers must now expose minimum artifact-lifecycle timestamps directly in their headers.
- Under this rule:
  - parent ledgers must carry `created_at`, `reviewed_at`, and `accepted_at`
  - supplement ledgers must carry `supplement_series_id`, `supplement_sequence`, `created_at`, `reviewed_at`, `accepted_at`, `writeback_started_at`, and `writeback_completed_at`
  - these fields record repository-side artifact lifecycle only and do not stand in for historical-effective rule time
  - historical-effective timing remains reserved for later contract chronology fields under `P2`

## P2 (Contract chronology fields | v1)

### P2-C1-S1 (Minimum contract chronology fields fixed | v1)

- Contracts must now expose one minimum chronology field set that keeps append-only registry order distinct from recorded and historical-effective time.
- Under this rule:
  - `contract_release` remains the append-only registry order inside one family
  - `recorded_at` records when the release entered the repo as one defended contract record
  - `reviewed_at` records when the release reached its current defended review state
  - `effective_from` and `effective_until` record the best currently known historical-effective range for the release state
  - these chronology fields may use `unknown`, `pending`, or `ongoing` where the repo does not yet have a stronger time reconstruction

### P2-C1-S2 (Statement-table chronology range fields fixed | v1)

- Contract statement tables and statement-evolution tables must now distinguish clause-state ranges from change-event times when time-bound reading matters.
- Under this rule:
  - the `Contract Statement Table` should add `first effective at`, `last changed at`, `effective from`, and `effective until`
  - the `Statement Evolution Table` should add `effective at` and `recorded at`
  - `first effective release` and `last changed release` stay as release ids, while the new time columns carry best-known chronology separate from registry numbering
  - time-bound clause reading may therefore represent later-recorded earlier states without forcing release renumbering

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-7E/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle.

**Branch convention**:

- `S0F-7E` work should continue on the top-level `S0F-docs-management-v6` branch unless the lane later opens one narrower bounded follow-up that warrants its own child branch.

**Commit discipline (recommended)**:

- Keep sequence-model, time-field, historical-backfill, and chronology-view commits separated when practical so future archaeology can read which chronology rule changed at which step.

## Plan (draft)

### P1 (Supplement sequence and artifact-lifecycle fields)

- `P1-C1-S1`: define supplement series id plus append-only sequence naming
- `P1-C1-S2`: define minimum lifecycle fields for parent ledgers and supplement ledgers

### P2 (Contract chronology fields)

- `P2-C1-S1`: define minimum contract chronology fields for registry order, recorded order, and historical-effective order
- `P2-C1-S2`: define how the contract statement tables should carry chronology range fields when time-bound rule reading matters

### P3 (Historical-backfill release rule)

- `P3-C1-S1`: define `historical-backfill` release action and the no-renumber rule
- `P3-C1-S2`: define minimum lineage updates when a later-recorded earlier state is admitted into an existing family

### P4 (Future chronology-reading rule)

- `P4-C1-S1`: define how future views should sort registry order, recorded order, and effective order separately

## Execution Checklist (unchecked)

### P0 (Lane boundary)

- [x] `P0-C1-S1`: open `S0F-7E` as the chronology follow-up after `7D`
- [x] `P0-C1-S2`: preserve append-only family numbering by default
- [x] `P0-C1-S3`: distinguish artifact-lifecycle, recorded, and historical-effective chronology up front

### P1 (Supplement sequence and artifact-lifecycle fields)

- [x] `P1-C1-S1`: define supplement series id plus append-only sequence naming
- [x] `P1-C1-S2`: define minimum lifecycle fields for parent ledgers and supplement ledgers

### P2 (Contract chronology fields)

- [x] `P2-C1-S1`: define minimum contract chronology fields for registry order, recorded order, and historical-effective order
- [x] `P2-C1-S2`: define statement-table chronology range fields when time-bound reading matters

### P3 (Historical-backfill release rule)

- [ ] `P3-C1-S1`: define `historical-backfill` release action and no-renumber handling
- [ ] `P3-C1-S2`: define minimum lineage updates for later-recorded earlier states

### P4 (Future chronology-reading rule)

- [ ] `P4-C1-S1`: define chronology-view sorting across registry, recorded, and effective order

## Current Status

- `S0F-7E` is now opened as the chronology follow-up after `S0F-7D`.
- The lane boundary is now fixed: supplement sequencing, time-field separation, historical-backfill releases, and chronology-safe reader ordering should no longer remain implicit inside ad hoc contract or supplement edits.
- `P1-C1-S1` is now complete: repeated supplement rounds now have one append-only sequence-bearing naming model under one stable supplement series id.
- `P1-C1-S2` is now complete: parent ledgers and supplement ledgers now expose distinct minimum artifact-lifecycle fields without overloading them as historical-effective rule timestamps.
- `P2-C1-S1` is now complete: contracts now separate append-only registry order from recorded and historical-effective time through one minimum chronology field set.
- `P2-C1-S2` is now complete: the contract template now distinguishes clause-state ranges from change-event times, and `DOC-WORKFLOW-RUNBOOK-0001` now demonstrates the new statement-table chronology columns on one live draft.
- The next step is to define the historical-backfill release rule before opening the next labs-oriented supplement round.

## Evidence (reserved)

### P0-C1-S1S2S3 (Chronology follow-up lane scaffolded | 2026-04-12)

- artifacts:
  - `docs/logs/log-S0F-7E-supplement-sequencing-time-fields-and-historical-backfill-release-chronology.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo should gain one new bounded lane after `S0F-7D` for supplement sequencing, time-field separation, and historical-backfill chronology
  - the lane should preserve append-only family numbering while reserving a later rule for earlier historical states discovered after current releases already exist
  - the lane should give the next labs-oriented supplement round one explicit home before any template or contract rewrite starts
- observed:
  - `S0F-7E` now exists as the next chronology-focused follow-up lane after `S0F-7D`
  - the lane now fixes append-only family numbering and separated chronology layers as its opening boundary

### P1-C1-S1S2 (Supplement sequencing and ledger lifecycle fields fixed | 2026-04-12)

- headSha: `3dce87b5b`
- artifacts:
  - `docs/logs/log-S0F-7E-supplement-sequencing-time-fields-and-historical-backfill-release-chronology.md`
  - `docs/logs/_template-support-only-contract-release-ledger.md`
  - `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - repeated supplement rounds should gain one stable series id plus append-only sequence numbering so future `001`, `002`, and `003` rounds do not collapse into one file
  - parent ledger and supplement-ledger templates should expose minimum artifact-lifecycle timestamps without claiming to describe historical-effective rule time
  - the lane should record these sequence and lifecycle rules explicitly before the next labs-oriented supplement round is opened
- observed:
  - supplement-ledger naming now distinguishes `supplement_series_id`, `supplement_sequence`, and one sequence-bearing on-disk file id
  - the parent ledger template now exposes `created_at`, `reviewed_at`, and `accepted_at` as the minimum artifact-lifecycle fields
  - the supplement-ledger template now exposes `created_at`, `reviewed_at`, `accepted_at`, `writeback_started_at`, and `writeback_completed_at` in addition to stable series and sequence fields

### P2-C1-S1S2 (Contract chronology fields and statement-table time ranges fixed | 2026-04-12)

- headSha: `4a472d92c`
- artifacts:
  - `docs/governance/contracts/_template-contract-record.md`
  - `docs/governance/contracts/workflow/runbook/DOC-WORKFLOW-RUNBOOK-0001-projection-operator-rebuild-replay-and-failure-recovery.md`
  - `docs/logs/log-S0F-7E-supplement-sequencing-time-fields-and-historical-backfill-release-chronology.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - contracts should gain one minimum chronology field set that separates registry order from recorded and historical-effective time
  - statement tables should gain chronology range fields without overloading release ids to act as time proxies
  - the lane should prove the new contract chronology columns on one live draft before later historical-backfill work continues
- observed:
  - the contract template now exposes `recorded_at`, `reviewed_at`, `effective_from`, and `effective_until` as the minimum contract chronology fields
  - the contract template now distinguishes clause-state range fields from change-event time fields across the two optional contract tables
  - `DOC-WORKFLOW-RUNBOOK-0001` now demonstrates the new statement-table chronology columns while keeping unknown historical timing explicit rather than guessed
