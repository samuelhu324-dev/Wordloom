# log-S0F-7F (Phase 7F: log and roadmap frontmatter minimum time fields)

---

**id**: `S0F-7F`
**kind**: `log`
**title**: `log and roadmap frontmatter minimum time fields`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Records, Roadmap, epic/s0, sub/7f`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/462`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/471`
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-7E-supplement-sequencing-time-fields-and-historical-backfill-release-chronology.md`
  **reference_log_1**: `docs/logs/log-S0F-7E-supplement-sequencing-time-fields-and-historical-backfill-release-chronology.md`
  **reference_log_2**: `docs/logs/_template-log-phase-drills-evidence.md`
  **reference_log_3**: `docs/roadmap/road-template-main-roadmap.md`
  **reference_log_4**: `docs/roadmap/road-template-branch-roadmap.md`
  **reference_log_5**: `docs/roadmap/road-template-structured-roadmap.md`
**issue_keyword**: `records`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M2`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-13`
**updated**: `2026-04-14`

---

## PR Summary Inputs (optional)

- Use this block because `S0F-7F` is expected to standardize minimum lifecycle-time fields across logs and roadmaps.

**PR summary bullets**:

- Define the minimum frontmatter lifecycle-time fields for logs and roadmap artifacts.
- Land UTC-second and reviewed-state samples where chronology audit actually needs them.
- Keep the time contract minimal enough for routine docs work while still supporting governance replay.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the frontmatter minimum-time-fields lane.

**PR links**:

- Log: `docs/logs/log-S0F-7F-log-and-roadmap-frontmatter-minimum-time-fields.md`
- Previous log: `docs/logs/log-S0F-7E-supplement-sequencing-time-fields-and-historical-backfill-release-chronology.md`

## Decision / Outcome

**Decision**:

- `S0F-7F` opens as the bounded follow-up after `S0F-7E` for one narrower documentation-management problem: most governance logs and roadmap documents still carry `created` and `updated`, but the repo does not yet define one minimum frontmatter lifecycle-time contract aligned with the newer UTC-aware ledger and supplement model.
- This lane will fix only the minimum shared frontmatter contract for logs and roadmaps first; it will not widen immediately into contract chronology or evidence-audit fields that already belong to `S0F-7E` and the contract templates.

**Default choices (phase defaults / v1)**:

- Treat log and roadmap frontmatter time as `artifact-lifecycle` time only, not as historical-effective rule time.
- Keep the minimum shared contract narrow: `created`, `updated`, and later `reviewed` only where the document class actually needs review-state tracking.
- Prefer canonical UTC-second timestamps for new writes in those existing fields when exact lifecycle audit matters, while allowing day-only values when only day-level history is defended.
- Do not force every log or roadmap file to gain row-level or evidence-level time-audit tables; that stays reserved for ledgers, supplements, and other evidence-heavy packets.
- Start with a minimum sample set before any wider migration rule is declared.

## Minimum Frontmatter Lifecycle-Time Rule

- Ordinary `log` and `roadmap` frontmatter should now use `created`, `updated`, and optional `reviewed` as the minimum artifact-lifecycle fields.
- New writes should prefer canonical UTC-second timestamps such as `2026-04-13T08:15:30Z` in those existing fields when exact lifecycle audit matters.
- Legacy day-only values such as `2026-04-13` remain valid when second-level precision is unnecessary or unavailable.
- `reviewed` is optional and should appear only when a log or roadmap is reviewed as one bounded governance packet rather than as an ordinary iterative draft.
- Evidence-time audit and historical-effective time remain out of scope for ordinary log and roadmap frontmatter.

## Problem Statement

- The repo now has a stronger chronology model for support-only ledgers, supplement ledgers, and contract templates, but the ordinary `log` and `roadmap` frontmatter still uses older `created` and `updated` fields without one repo-wide minimum lifecycle-time rule.
- Without a bounded follow-up, later docs-management work will keep mixing at least three things:
  - older compatibility fields such as `created` and `updated`
  - newer UTC-aware lifecycle fields such as `created_at` and `reviewed_at`
  - evidence or historical-effective time that does not belong in ordinary log and roadmap frontmatter at all
- The repo therefore needs one narrow lane that answers three questions before broader migration starts:
  - what the minimum shared frontmatter lifecycle-time fields should be for logs and roadmaps
  - how those fields should relate to older compatibility fields already present in templates and live files
  - which smallest sample set is sufficient to test the contract before any repo-wide rewrite

## Exported Sections / Outlet Ownership

- This slice starts as one `log-template + roadmap-template + log-retained core` field-governance lane.
- The expected landing is one minimum frontmatter lifecycle-time rule for ordinary logs and roadmap files plus one compatibility policy for older day-only fields.

**Outlet ownership**:

- `contract`: no-op by default; this lane should not widen into contract chronology because that surface is already owned elsewhere
- `runbook`: no-op by default
- `view`: no-op by default
- `index/front-door`: no-op by default
- `disposition/placement`: the log and roadmap templates are the first mutable landing surfaces; later live-file migration should remain sample-first
- `log-retained core`: the lane boundary, field contract, compatibility rule, and sample verdicts remain here

## Definitions (optional)

- `artifact-lifecycle time`: the repo-side time when a document was created, updated, reviewed, or accepted.
- `minimum frontmatter lifecycle-time contract`: the smallest shared field set that ordinary logs and roadmaps must carry before any document-class-specific timing extensions are considered.
- `compatibility field`: one older field shape, such as `created` or `updated`, that may remain temporarily while the repo transitions toward one newer standard.
- `local-time mirror field`: one optional display-only local timestamp derived from a canonical UTC timestamp; it is not the primary stored time value.

## Constraints

- Do not widen ordinary logs or roadmaps into evidence-audit packets by default.
- Do not require ordinary log frontmatter to carry historical-effective fields that belong to contracts.
- Do not break existing template compatibility before the minimum replacement rule is tested on a small sample set.
- Do not attempt a repo-wide timestamp rewrite before the migration rule is proven on a few controlled files.

## Scope

- `P0`: open `S0F-7F`, bound the problem to ordinary log and roadmap frontmatter lifecycle-time fields, and separate it from `S0F-7E` evidence/chronology work
- `P1`: define the minimum shared lifecycle-time frontmatter rule for logs and roadmaps plus compatibility handling for older `created` and `updated` fields
- `P2`: test the rule on one minimum sample set consisting of the log template, the main-roadmap template, and the branch-roadmap template
- `P3`: if the sample passes, decide whether one first live log sample and one first live roadmap sample should be migrated next
- `P4`: apply the fixed timing rule to one existing ledger plus one existing supplement-ledger sample, including one first screenshot-time audit and one first sequence-bearing SUP rename

## Success Criteria (DoD)

- The repo has one explicit minimum frontmatter lifecycle-time rule for ordinary logs and roadmaps.
- The repo has one compatibility rule that explains how older `created` and `updated` fields relate to any newer lifecycle-time fields.
- The repo has one small proved sample set before any broader migration guidance is declared.
- The lane stays separate from evidence-time audit and contract chronology, so document classes do not collapse back into one mixed time model.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the minimum frontmatter lifecycle-time contract is explicitly written
  - the minimum sample set has been updated and reviewed
  - the lane records whether the next step is a bounded live-file migration or direct retention
- `stable` does not require repo-wide migration in the same lane; one accepted sample-first rule is sufficient.

## P0 (Lane boundary | v1)

### P0-C1-S1 (Open `S0F-7F` as the log/roadmap frontmatter timing follow-up)

- Open one bounded follow-up lane after `S0F-7E` for ordinary log and roadmap lifecycle-time fields.

### P0-C1-S2 (Fix the minimum sample set before wider migration)

- The first bounded sample set is:
  - `docs/logs/_template-log-phase-drills-evidence.md`
  - `docs/roadmap/road-template-main-roadmap.md`
  - `docs/roadmap/road-template-branch-roadmap.md`

## Plan (draft)

### P1 (Minimum frontmatter rule)

- `P1-C1-S1`: define the minimum shared lifecycle-time field set for logs and roadmaps
- `P1-C1-S2`: define compatibility with existing `created` and `updated` fields

### P2 (Template samples)

- `P2-C1-S1`: update the log template sample
- `P2-C1-S2`: update the main-roadmap and branch-roadmap template samples

### P3 (First live-file migration decision)

- `P3-C1-S1`: decide whether one live log sample should migrate next
- `P3-C1-S2`: decide whether one live roadmap sample should migrate next

### P4 (Ledger and SUP timing samples)

- `P4-C1-S1`: add lifecycle fields to `ledger-S0A-1A` and normalize the first Projects SUP file as sequence `001`
- `P4-C1-S2`: add screenshot-backed time audit for the three `2026-02-12` Projects screenshots without overclaiming second-level precision
- `P4-C1-S3`: align `ledger-S0A-1A` and `PROJECTS-0001` to the more complete chronology-first structure already demonstrated by the `S0A-2A` plus `LABS-0002` sample set

## Execution Checklist (unchecked)

### P0 (Lane boundary)

- [x] `P0-C1-S1`: open `S0F-7F` as the log/roadmap frontmatter timing follow-up
- [x] `P0-C1-S2`: fix the minimum sample set before wider migration

### P1 (Minimum frontmatter rule)

- [x] `P1-C1-S1`: define the minimum shared lifecycle-time field set for logs and roadmaps
- [x] `P1-C1-S2`: define compatibility with existing `created` and `updated` fields

### P2 (Template samples)

- [x] `P2-C1-S1`: update the log template sample
- [x] `P2-C1-S2`: update the main-roadmap and branch-roadmap template samples

### P4 (Ledger and SUP timing samples)

- [x] `P4-C1-S1`: add lifecycle fields to `ledger-S0A-1A` and normalize the first Projects SUP file as sequence `001`
- [x] `P4-C1-S2`: add screenshot-backed time audit for the three `2026-02-12` Projects screenshots without overclaiming second-level precision
- [x] `P4-C1-S3`: align `ledger-S0A-1A` and `PROJECTS-0001` to the more complete chronology-first structure already demonstrated by the `S0A-2A` plus `LABS-0002` sample set

## Current Status (recommended)

- `S0F-7F` is now opened as the bounded follow-up after `S0F-7E` for ordinary log and roadmap frontmatter lifecycle-time fields.
- The minimum sample set is fixed as the log template plus the main-roadmap and branch-roadmap templates.
- `P1-C1-S1` is now complete: the lane now defines `created`, `updated`, and optional `reviewed` as the minimum lifecycle-time fields for ordinary logs and roadmaps.
- `P1-C1-S2` is now complete: the lane now allows future UTC-second writes in those existing fields instead of introducing a second pair of `*_at` field names.
- `P2-C1-S1` is now complete: the phase-drills-evidence log template now uses the revised `created/updated/reviewed` contract.
- `P2-C1-S2` is now complete: the main-roadmap and branch-roadmap templates now use the same revised `created/updated/reviewed` contract.
- `P3-C1-S1` is now complete: `log-S0F-7D` now carries one first live-log sample of the revised `created/updated/reviewed` contract.
- `P3-C1-S2` is now complete: `road-001` now carries one first live-roadmap sample of the revised `created/updated/reviewed` contract.
- `P4-C1-S1` is now complete: `ledger-S0A-1A` now carries explicit lifecycle fields, and the first Projects supplement sample now uses the sequence-bearing `SUP-001` filename plus the full supplement lifecycle header.
- `P4-C1-S2` is now complete: the three Projects screenshots now carry one explicit day-precision evidence-time audit fixed at `2026-02-12` without inventing second-level timestamps.
- `P4-C1-S3` is now complete: `ledger-S0A-1A` now also exposes one row-level chronology audit for `R02`, and `PROJECTS-0001` now carries the minimum chronology-first contract structure that was still missing relative to the more complete `LABS-0002` sample.
- The next step is to review whether this revised log/roadmap contract together with the first ledger/SUP timing sample is sufficient before any broader live-file migration continues.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths when the lane starts mutating templates.
- This section stays empty until the first template-sample patch is actually landed.

### P1-C1-S1S2 + P2-C1-S1S2 + P3-C1-S1S2 (Revised `created/updated/reviewed` contract and first live samples fixed | 2026-04-13)

- headSha: `dc7a027f6`

- artifacts:
  - `docs/logs/_template-log-phase-drills-evidence.md`
  - `docs/roadmap/road-template-main-roadmap.md`
  - `docs/roadmap/road-template-branch-roadmap.md`
  - `docs/logs/log-S0F-7F-log-and-roadmap-frontmatter-minimum-time-fields.md`
  - `docs/logs/log-S0F-7D-ledger-supplement-admission-and-old-log-continuation.md`
  - `docs/roadmap/road-001-systems-platform-ops-roadmap.md`
- expected:
  - ordinary logs and roadmap templates should keep the existing `created` and `updated` field names, gain one optional `reviewed` field, and avoid a duplicated `*_at` naming layer
  - future writes should still be allowed to use UTC-second values inside those existing fields when finer lifecycle audit is needed
  - the first live samples should prove that one existing log and one existing roadmap can adopt `reviewed` without any wider chronology surface change
- observed:
  - the log, main-roadmap, and branch-roadmap templates now expose `created`, `updated`, and optional `reviewed` only, while still allowing UTC-second or day-level values in those fields
  - `log-S0F-7D` now uses `reviewed: 2026-04-11`, aligned to its current `updated` value as the first live-log sample
  - `road-001` now uses `reviewed: 2026-03-29`, aligned to its current `updated` value as the first live-roadmap sample

### P4-C1-S1S2S3 (First live ledger/SUP timing sample and Projects-0001 structure alignment fixed | 2026-04-13)

- headSha: `6b4eaf13e`

- artifacts:
  - `docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md`
  - `docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md`
  - `docs/governance/contracts/workflow/github/projects/DOC-WORKFLOW-GITHUB-PROJECTS-0001-project-views-support-execution-priority.md`
  - `docs/logs/log-S0F-7D-ledger-supplement-admission-and-old-log-continuation.md`
  - `docs/logs/log-S0F-7F-log-and-roadmap-frontmatter-minimum-time-fields.md`
- expected:
  - the first existing ledger/SUP sample should expose lifecycle fields without confusing them with row-level or evidence-level historical time
  - the first older unsequenced Projects SUP file should be normalized to one explicit `001` round under the newer append-only supplement naming rule
  - the three Projects screenshots should record the defended day-level capture date `2026-02-12` without claiming second-level timestamps that the archive does not preserve
  - the Projects trio should also close the structure gap against the more complete `S0A-2A` plus `LABS-0002` sample by adding one parent-row chronology audit and one minimum chronology-first contract statement/evolution surface
- observed:
  - `ledger-S0A-1A` now exposes `created_at`, `reviewed_at`, and `accepted_at`, while the Projects supplement sample now exposes sequence-bearing identity plus the full supplement lifecycle header
  - the Projects SUP file now reads as `ledger-SUP-S0A-1A-001-...`, and all supporting references now point to the sequence-bearing filename
  - the three screenshot evidence items now share one explicit day-precision time audit anchored at `2026-02-12`, with observation and recording both limited to defended day-level capture timing
  - `ledger-S0A-1A` now also exposes one optional row chronology audit for `S0A-1A-R02`, and `PROJECTS-0001` now carries `recorded_at/reviewed_at/effective_from/effective_until` plus one minimum contract statement table and one statement evolution table so the Projects trio now reads much closer to the `S0A-2A` plus `LABS-0002` structure level