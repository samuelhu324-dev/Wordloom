# log-S0F-7F (Phase 7F: log and roadmap frontmatter minimum time fields)

---

**id**: `S0F-7F`
**kind**: `log`
**title**: `log and roadmap frontmatter minimum time fields`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Records, Roadmap, epic/s0, sub/7f`
**links**: ``
  **issue**: ``
  **pr**: ``
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
**created**: `2026-04-13`
**updated**: `2026-04-13`

---

## Decision / Outcome

**Decision**:

- `S0F-7F` opens as the bounded follow-up after `S0F-7E` for one narrower documentation-management problem: most governance logs and roadmap documents still carry `created` and `updated`, but the repo does not yet define one minimum frontmatter lifecycle-time contract aligned with the newer UTC-aware ledger and supplement model.
- This lane will fix only the minimum shared frontmatter contract for logs and roadmaps first; it will not widen immediately into contract chronology or evidence-audit fields that already belong to `S0F-7E` and the contract templates.

**Default choices (phase defaults / v1)**:

- Treat log and roadmap frontmatter time as `artifact-lifecycle` time only, not as historical-effective rule time.
- Keep the minimum shared contract narrow: `created_at`, `updated_at`, and later `reviewed_at` only where the document class actually needs review-state tracking.
- Prefer canonical UTC-second timestamps for new writes when exact lifecycle audit matters, while allowing compatibility with legacy day-only `created` and `updated` during migration.
- Do not force every log or roadmap file to gain row-level or evidence-level time-audit tables; that stays reserved for ledgers, supplements, and other evidence-heavy packets.
- Start with a minimum sample set before any wider migration rule is declared.

## Minimum Frontmatter Lifecycle-Time Rule

- Ordinary `log` and `roadmap` frontmatter should now treat `created_at` and `updated_at` as the canonical minimum artifact-lifecycle fields.
- `reviewed_at` is optional and should appear only when a log or roadmap is reviewed as one bounded governance packet rather than as an ordinary iterative draft.
- New writes should prefer canonical UTC-second timestamps such as `2026-04-13T08:15:30Z` when exact lifecycle audit matters.
- Legacy day-only values such as `2026-04-13` remain valid when second-level precision is unnecessary or unavailable.
- Existing `created` and `updated` fields remain compatibility mirrors during migration and should reflect the day-level view of `created_at` and `updated_at` rather than introducing an independent second time model.
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

## Current Status (recommended)

- `S0F-7F` is now opened as the bounded follow-up after `S0F-7E` for ordinary log and roadmap frontmatter lifecycle-time fields.
- The minimum sample set is fixed as the log template plus the main-roadmap and branch-roadmap templates.
- `P1-C1-S1` is now complete in workspace: the lane now defines `created_at` and `updated_at` as the canonical minimum lifecycle-time fields for ordinary logs and roadmaps, with `reviewed_at` kept optional.
- `P1-C1-S2` is now complete in workspace: the lane now fixes `created` and `updated` as compatibility mirrors rather than as an independent competing time model.
- `P2-C1-S1` is now complete in workspace: the phase-drills-evidence log template now carries the minimum lifecycle-time fields plus one explicit compatibility rule.
- `P2-C1-S2` is now complete in workspace: the main-roadmap and branch-roadmap templates now carry the same minimum lifecycle-time fields plus the same compatibility rule.
- The next step is to decide whether one first live log sample and one first live roadmap sample should migrate under the same compatibility model.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths when the lane starts mutating templates.
- This section stays empty until the first template-sample patch is actually landed.

### P1-C1-S1S2 + P2-C1-S1S2 (Minimum frontmatter lifecycle-time rule and template samples fixed in workspace | 2026-04-13)

- artifacts:
  - `docs/logs/_template-log-phase-drills-evidence.md`
  - `docs/roadmap/road-template-main-roadmap.md`
  - `docs/roadmap/road-template-branch-roadmap.md`
  - `docs/logs/log-S0F-7F-log-and-roadmap-frontmatter-minimum-time-fields.md`
- expected:
  - ordinary logs and roadmap templates should gain one minimum lifecycle-time rule without collapsing into evidence-audit or contract chronology semantics
  - `created_at` and `updated_at` should become canonical while `created` and `updated` remain compatibility mirrors during migration
  - the first bounded sample set should prove the rule on one log template and two roadmap templates before any live-file rewrite is attempted
- observed:
  - the log, main-roadmap, and branch-roadmap templates now all expose `created_at`, `updated_at`, and optional `reviewed_at` ahead of the legacy day-only fields
  - each sample template now documents UTC-second preference, legacy day-only compatibility, and the mirror role of `created` and `updated`
  - `S0F-7F` now records `P1` and `P2` as complete in workspace and narrows the next step to one bounded live-file migration decision