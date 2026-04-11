# log-S0F-7D (Phase 7D: ledger supplement admission and old-log continuation)

---

**id**: `S0F-7D`
**kind**: `log`
**title**: `ledger supplement admission and old-log continuation`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Ledger, Evidence, Migration, epic/s0, sub/7d`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-7C-old-log-decomposition-application-lane.md`
  **reference_log_1**: `docs/logs/log-S0F-7C-old-log-decomposition-application-lane.md`
  **reference_log_2**: `docs/logs/_template-support-only-contract-release-ledger.md`
  **reference_log_3**: `docs/governance/contracts/_template-contract-record.md`
  **reference_log_4**: `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
**issue_keyword**: `evidence`
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
**created**: `2026-04-11`
**updated**: `2026-04-11`

---

## Decision / Outcome

**Decision**:

- `S0F-7D` opens as the bounded follow-up after `S0F-7C` for supplement-ledger admission and future old-log continuation.
- This lane exists because `7C` has already proved one first application packet, and later work now needs one stricter continuation rule: mixed later evidence must attach to an existing source-owned ledger before it can influence contract meaning.

**Default choices (phase defaults / v1)**:

- Do not let later code, markdown, screenshots, oral recall, or operator validation material write directly into contracts.
- Admit later evidence only through one bounded supplement ledger that is anchored to an existing parent source-owned ledger.
- Prefer current logs or new bounded logs for future extraction work; reopen older sources only when an existing ledger lacks enough evidence to defend or revise one already-known slice.
- Keep `7D` focused on supplement-ledger admission and continuation discipline first; broader provenance, approval, and organizational authority fields remain out of scope for this first scaffold.

## Problem Statement

- `S0F-7C` proved that one old mixed source can be decomposed into ledgers and child contracts, but it also exposed the next missing control surface: later evidence is now likely to arrive from code, old markdown, screenshots, or verified oral explanation rather than from the original source packet alone.
- If that later evidence writes directly into contracts, the repo loses the defended `source packet -> ledger -> contract` chain that `7B` and `7C` just established.
- The repo therefore needs one bounded continuation lane that answers three questions before more old-log work continues broadly:
  - how supplement evidence is admitted without bypassing the parent source-owned ledger
  - how one supplement ledger can strengthen, sharpen, or reopen an existing routing verdict without inventing arbitrary new contract meaning
  - when future old-log continuation should prefer current or new bounded logs instead of repeatedly extending the first `7C` packet

## Exported Sections / Outlet Ownership

- This slice starts as one `contract + support-only ledger + log-retained core` governance-design lane.
- The default expected landing is one supplement-ledger admission model, one first supplement-ledger template or pilot shape, and one explicit continuation rule for future old-log reopening.

**Outlet ownership**:

- `contract`: no-op by default; this lane should first fix supplement-ledger and continuation rules before emitting any family-owned contract
- `support-only ledger`: expected landing surface for the supplement-ledger template and later pilot instances
- `view`: no-op by default; reader projection is not the first missing boundary here
- `index/front-door`: no-op by default; front-door work should wait until supplement-ledger practice stabilizes
- `disposition/placement`: no-op by default
- `log-retained core`: expected landing surface for the lane boundary, admission rules, pilot decisions, and evidence

## Definitions (optional)

- `parent ledger`: the existing source-owned support-only ledger that already records source slices and their routing verdicts.
- `parent ledger row id`: the stable per-slice identifier inside one parent ledger, used as the anchor for later supplement evidence.
- `supplement ledger`: a bounded evidence-admission ledger that attaches to one parent ledger and may strengthen, sharpen, or reopen one existing routing verdict.
- `supplement item id`: the stable per-evidence identifier inside one supplement ledger, scoped beneath one parent-ledger row.
- `attachment or shot id`: the stable per-asset identifier beneath one supplement item, used for screenshots, exports, transcripts, or similar attached evidence.
- `admitted supplement evidence`: later evidence that is tied to one existing parent-ledger slice and has passed the required verification rule for this lane.
- `continuation packet`: a later bounded old-log follow-up that reopens a source only because one explicit ledger gap or supplement-evidence need has been identified.

## Constraints

- Do not bind supplement ledgers directly to contracts as the primary owner; they must attach to one parent source-owned ledger first.
- Do not allow a supplement ledger to introduce entirely new free-floating slices that never appeared in the parent ledger review surface.
- Do not reopen old logs mechanically; a continuation packet should require one explicit unresolved ledger need.
- Do not fold broader provenance, approval, or organizational-attestation modeling into this first lane unless the supplement-ledger pilot proves the smaller boundary insufficient.

## Scope

- `P0`: open `S0F-7D`, fix the supplement-ledger continuation boundary, and state why future old-log continuation moves here rather than staying in `7C`
- `P1`: define the supplement-ledger model, including its naming, minimum header, table shape, and parent-ledger attachment rule
- `P2`: pilot the first supplement-ledger application on one real packet, expected first on the `S0A-1A` Projects slice
- `P3`: define the continuation rule for when future old-log work should use current logs, new bounded logs, or explicit supplement-ledger reopening instead of broad historical replay
- `P4`: reserve any later provenance or approval-interface expansion only if the supplement-ledger pilot proves the current minimal evidence-admission model too weak

## Success Criteria (DoD)

- The repo has one explicit rule that supplement evidence attaches to a parent ledger before it can influence contracts.
- The repo has one reusable supplement-ledger shape that can admit code, markdown, or other verified later evidence without bypassing source accountability.
- The repo has one first real pilot showing how a supplement ledger affects an existing parent-ledger verdict.
- The repo has one explicit continuation rule that keeps future old-log extraction from repeatedly extending `7C` or re-consuming older logs casually.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` have fixed the supplement-ledger model, first pilot, and continuation boundary;
  - any broader provenance or approval expansion has either been explicitly deferred or opened as a separate bounded follow-up rather than left implicit here.

## P0 (Lane boundary | v1)

### P0-C1-S1 (Supplement-ledger continuation lane opened after `7C` | v1)

- `S0F-7D` is now the bounded continuation lane after `7C` for supplement-ledger admission and future old-log reopening.
- Under this rule, `7C` remains the first defended application packet while `7D` owns future continuation discipline.

### P0-C1-S2 (Parent-ledger-first supplement rule fixed | v1)

- Later evidence must now attach to one existing parent source-owned ledger before it can influence contract reading.
- Under this rule, supplement evidence does not write straight into child contracts or parent contracts.

## P1 (Supplement-ledger model | v1)

### P1-C1-S1 (Supplement-ledger naming and parent-ledger attachment fixed | v1)

- A supplement ledger must now be named as `ledger-SUP-<source-id>-<source-summary>.md`.
- The `<source-id>` and `<source-summary>` must match the existing parent source-owned ledger rather than inventing one contract-first naming scheme.
- Under this rule:
  - one supplement ledger always attaches to one parent ledger
  - the parent ledger remains the owner of routing verdicts
  - the supplement ledger may sharpen or reopen a parent-ledger row, but it does not replace the parent ledger as the packet owner

### P1-C1-S2 (Minimum supplement-ledger header and row contract fixed | v1)

- The minimum supplement-ledger header is now fixed as:
  - `supplement_id`
  - `supplement_kind`
  - `status`
  - `owner_lane`
  - `parent_ledger_id`
  - `parent_source_id`
  - `parent_source_ref`
  - `supplement_scope`
  - `target_reading_goal`
- The minimum evidence row contract is now fixed as:
  - `parent ledger slice`
  - `evidence ref`
  - `evidence type`
  - `verification status`
  - `effect on current verdict`
  - `proposed parent-ledger action`
  - `contract impact`
  - `notes`
- Under this rule, supplement rows record how later evidence should be judged against an already-existing parent-ledger slice rather than redoing the original routing table.

### P1-C1-S3 (Allowed verdict effects and escalation rule fixed | v1)

- Allowed `effect on current verdict` values are now fixed as:
  - `supports-existing`
  - `sharpens-existing`
  - `narrows-existing`
  - `revises-existing`
  - `conflicts-needs-review`
- Allowed `proposed parent-ledger action` values are now fixed as:
  - `no-change`
  - `add-supporting-evidence`
  - `rewrite-parent-row`
  - `split-parent-row`
  - `reopen-routing`
- Under this rule:
  - supplement evidence may update or reopen a parent-ledger row
  - supplement evidence may not write directly into contract lineage or release fields first
  - any contract rewrite must happen only after the parent ledger has absorbed or rejected the supplement verdict

### P1-C2-S1 (Parent-ledger row-id model fixed | v1)

- Parent-ledger rows must now carry one stable `row_id` per routed slice.
- The naming rule is now fixed as `<source-id>-R<n>`, using zero-padded sequence numbers inside one parent ledger.
- Under this rule:
  - `S0A-1A-R01` means the first stable routed slice inside the `S0A-1A` parent ledger
  - row ids stay ledger-scoped rather than becoming contract ids
  - wording in `source slice` may later tighten without breaking supplement references, because the stable anchor is the `row_id`

### P1-C2-S2 (Supplement item-id and attachment-id model fixed | v1)

- Supplement evidence items must now carry one stable `supplement_item_id` beneath one parent-ledger row.
- The naming rule is now fixed as `<parent-row-id>-SUP-<n>`.
- Attachments or screenshots beneath one supplement item must now carry one stable `attachment_id`, using `ATT` as the generic asset suffix and `SHOT` when the asset is specifically a screenshot.
- Under this rule:
  - `S0A-1A-R02-SUP-01` means the first supplement item attached to parent row `S0A-1A-R02`
  - `S0A-1A-R02-SUP-01-SHOT-01` means the first screenshot asset beneath that supplement item
  - attachment ids remain evidence-layer identifiers and do not become contract ids

### P1-C2-S3 (ID boundary versus contract boundary fixed | v1)

- `row_id`, `supplement_item_id`, and `attachment_id` are now fixed as ledger-layer and evidence-layer identifiers rather than contract identifiers.
- Under this rule:
  - contracts may cite these ids when needed for auditability or reader traceability
  - contracts should not promote these ids into primary release identity fields
  - the stable identity split is now: `ledger_id` for the file, `row_id` for the routed slice, `supplement_item_id` for the admitted evidence item, and `attachment_id` for attached assets such as screenshots

### P1-C3-S1 (On-disk supplement naming normalized to `SUP` | v1)

- The on-disk artifact naming for supplement-ledger records is now normalized from `ledger-supplement-...` to `ledger-SUP-...`.
- Under this rule:
  - `SUP` is the on-disk abbreviation for supplement-ledger records
  - the conceptual boundary still remains `supplement ledger`, but filenames and `supplement_id` values now use the shorter `SUP` prefix
  - existing and future supplement-ledger references should prefer the `ledger-SUP-<source-id>-<source-summary>.md` shape

## Plan (draft)

### P1 (Supplement-ledger model)

- `P1-C1-S1`: define supplement-ledger naming and parent-ledger attachment
- `P1-C1-S2`: define the minimum supplement-ledger header and evidence row contract
- `P1-C1-S3`: define allowed verdict effects such as `supports-existing`, `sharpens-existing`, `revises-existing`, and `reopen-routing`
- `P1-C2-S1`: define stable row ids for parent-ledger slices
- `P1-C2-S2`: define supplement item ids plus screenshot or attachment ids
- `P1-C2-S3`: define the boundary between ledger-layer ids and contract-layer ids
- `P1-C3-S1`: normalize on-disk supplement-ledger naming to the `SUP` prefix

### P2 (First pilot)

- `P2-C1-S1`: pilot the first supplement-ledger against `S0A-1A` Projects evidence
- `P2-C1-S2`: decide whether the first pilot only sharpens the current Projects child or actually reopens its parent-ledger row

### P3 (Future continuation discipline)

- `P3-C1-S1`: define when future work should prefer current logs or new bounded logs instead of old-log reopening
- `P3-C1-S2`: define when an older packet may be reopened only through explicit supplement-ledger need

## Execution Checklist (unchecked)

### P0 (Lane boundary)

- [x] `P0-C1-S1`: open `S0F-7D` as the supplement-ledger continuation lane after `7C`
- [x] `P0-C1-S2`: fix the parent-ledger-first supplement rule

### P1 (Supplement-ledger model)

- [x] `P1-C1-S1`: define supplement-ledger naming and attachment
- [x] `P1-C1-S2`: define header and row contract
- [x] `P1-C1-S3`: define allowed verdict effects
- [x] `P1-C2-S1`: define stable row ids for parent-ledger slices
- [x] `P1-C2-S2`: define supplement item ids plus screenshot or attachment ids
- [x] `P1-C2-S3`: define the boundary between ledger-layer ids and contract-layer ids
- [x] `P1-C3-S1`: normalize on-disk supplement-ledger naming to the `SUP` prefix

### P2 (First pilot)

- [x] `P2-C1-S1`: pilot the first supplement-ledger on `S0A-1A` Projects evidence
- [ ] `P2-C1-S2`: decide whether the pilot sharpens or reopens the parent-ledger verdict

### P3 (Future continuation discipline)

- [ ] `P3-C1-S1`: define current-log or new-log preference for future work
- [ ] `P3-C1-S2`: define explicit reopen conditions for older packets

## Current Status

- `S0F-7D` is now opened as the bounded continuation lane after `S0F-7C`.
- The lane now fixes one immediate baseline: supplement evidence must attach to a parent source-owned ledger before it can affect contract meaning.
- `P1-C1-S1S2S3` are now complete: supplement-ledger naming, minimum header, evidence row shape, and allowed verdict effects are now fixed, and the first reusable template is now ready for direct pilot work.
- `P1-C2-S1S2S3` are now complete: stable row ids, supplement item ids, and screenshot or attachment ids are now fixed across the ledger layer, and the contract boundary is now explicit enough for real pilot intake.
- `P1-C3-S1` is now complete in workspace: on-disk supplement-ledger naming now uses the shorter `SUP` prefix, and the reusable template plus first pilot file now follow that same artifact naming model.
- `P2-C1-S1` is now complete in workspace: the first screenshot-backed Projects SUP pilot now exists at a stable repo-local path and reads as one sharpen-the-draft supplement rather than as one routing-reversal packet.
- The next execution step is `P2-C1-S2`: decide how much parent-ledger and `PROJECTS-0001` write-back should happen now that the first SUP pilot is reviewable.

## Evidence (reserved)

### P0-C1-S1S2 (Supplement-ledger continuation lane scaffolded | 2026-04-11)

- headSha: `54d4f529e`
- artifacts:
  - `docs/logs/log-S0F-7D-ledger-supplement-admission-and-old-log-continuation.md`
- expected:
  - the repo should gain one new bounded lane after `7C` for supplement-ledger admission and future old-log continuation
  - the lane should explicitly keep supplement evidence attached to a parent source-owned ledger instead of letting it write directly into contracts
- observed:
  - `S0F-7D` now exists as the next bounded follow-up after `7C`
  - the lane now fixes the parent-ledger-first supplement rule as its opening boundary

### P1-C1-S1S2S3 (Supplement-ledger model fixed and templated | 2026-04-11)

- headSha: `54d4f529e`
- artifacts:
  - `docs/logs/log-S0F-7D-ledger-supplement-admission-and-old-log-continuation.md`
  - `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
- expected:
  - the repo should gain one explicit supplement-ledger naming and attachment rule that stays anchored to an existing parent source-owned ledger
  - the repo should gain one reusable supplement-ledger template with a fixed header and evidence-row contract
  - the repo should fix the allowed verdict effects and parent-ledger escalation rule before any real pilot starts
- observed:
  - supplement-ledger naming is now fixed as `ledger-SUP-<source-id>-<source-summary>.md` with mandatory parent-ledger attachment
  - one reusable template now exists for supplement-ledger work with explicit header and evidence-row fields
  - the lane now fixes a narrow verdict set and requires any later contract rewrite to happen only after the parent ledger absorbs or rejects the supplement result

### P1-C2-S1S2S3 (Ledger-layer item and asset ids fixed | 2026-04-11)

- headSha: `5d7c70b84`
- artifacts:
  - `docs/logs/log-S0F-7D-ledger-supplement-admission-and-old-log-continuation.md`
  - `docs/logs/_template-support-only-contract-release-ledger.md`
  - `docs/logs/_template-support-only-contract-release-ledger-supplement.md`
  - `docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md`
- expected:
  - parent ledgers should gain one stable per-row id so supplement evidence can anchor to routed slices without depending on mutable prose labels
  - supplement items and screenshot or attachment assets should gain stable ids at the evidence layer
  - the repo should state clearly that these ids remain below the contract layer rather than becoming release identifiers
- observed:
  - parent ledger rows now have one stable `row_id` model
  - supplement items plus screenshot or attachment assets now have one stable id model beneath the parent row
  - the lane now keeps those ids ledger-scoped and evidence-scoped rather than promoting them into contract identity

### P1-C3-S1 (SUP artifact naming normalized | 2026-04-11)

- headSha: `<workspace not committed yet for S0F-7D/P1-C3-S1>`
- artifacts:
  - `docs/logs/log-S0F-7D-ledger-supplement-admission-and-old-log-continuation.md`
  - `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
  - `docs/logs/support-only/ledger-SUP-S0A-1A-tools-github-issues-projects-and-tags.md`
- expected:
  - the repo should normalize on-disk supplement-ledger naming to the shorter `SUP` prefix without changing the underlying conceptual boundary
  - the reusable template and first pilot should use the same naming shape
- observed:
  - the on-disk supplement-ledger naming now uses the `ledger-SUP-...` prefix
  - the reusable template and first pilot now match that same artifact naming rule

### P2-C1-S1 (First screenshot-backed Projects SUP pilot stabilized | 2026-04-11)

- headSha: `<workspace not committed yet for S0F-7D/P2-C1-S1>`
- artifacts:
  - `docs/logs/support-only/ledger-SUP-S0A-1A-tools-github-issues-projects-and-tags.md`
  - `docs/logs/support-only/S0A-1A-R02-SUP-01-SHOT-01-projects-status-board.png`
  - `docs/logs/support-only/S0A-1A-R02-SUP-02-SHOT-01-projects-table-view.png`
  - `docs/logs/support-only/S0A-1A-R02-SUP-03-SHOT-01-projects-timeline-view.png`
- expected:
  - the first Projects supplement should move from chat-only placeholder evidence to stable repo-local screenshot-backed evidence
  - the pilot should remain a sharpening supplement rather than an outright routing reversal
- observed:
  - the first Projects SUP pilot now cites stable repo-local screenshot paths and records the three screenshots as verified evidence items
  - the current reading still keeps `S0A-1A-R02 -> DOC-WORKFLOW-GITHUB-PROJECTS-0001` unchanged while preparing write-back that sharpens the parent row and widens the current Projects draft wording

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-7D/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle.

**Branch convention**:

- `S0F-7D` work should continue on the top-level `S0F-docs-management-v6` branch unless the lane later opens one narrower bounded follow-up that warrants its own child branch.

**Commit discipline (recommended)**:

- Keep scaffold, template, and first pilot commits separated so supplement-ledger model changes do not get buried inside one larger old-log continuation packet.