# log-<ID> (Phase <n>: <Slice Title>)

---

**id**: `<ID>`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `<One-line title: deliverable + drills/evidence + v1>`
**status**: `draft`           # draft | stable | archived
**scope**: `<Sx>`
**tags**: `EVOLUTION, <domain>, Drills, Evidence, epic/<sx>, sub/<phase>`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: ``
  **parent_log**: `docs/logs/log-<PARENT>.md`
  **previous_log**: ``
  **reference_log_1**: ``
**issue_keyword**: ``        # controlled fixed keyword; allowed values include audit/automation/contract/evidence/enforcement/migration/policy/records/runtime/taxonomy/workflow
**issue_top_labels**: ``     # comma-separated existing labels only
**issue_scope_labels**: ``   # comma-separated labels usually derived from scope / hierarchy
**issue_module_labels**: ``  # comma-separated module labels; leave blank when impact is not explicit
**issue_milestone**: ``      # exact GitHub milestone name; if blank, automation must leave milestone empty
**issue_parent**: ``         # parent issue reference if already known; otherwise leave blank
**issue_projects**: ``       # defaults to `wordloom Board` for logs under docs/logs in this workspace unless a different explicit project list is provided
**roadmap_path**: ``         # exact roadmap file that owns this log's bridge, e.g. docs/roadmap/road-S1-...md
**roadmap_milestone**: ``    # exact roadmap milestone, e.g. M3
**roadmap_phase**: ``        # exact roadmap phase, e.g. M3-P2; parent/spine-only logs may leave this blank
**roadmap_bridge_refs**: ``  # optional exact-slot refs when one child log maps to multiple slots, e.g. docs/roadmap/road-S1-...md#M3-P2, docs/roadmap/road-S1-...md#M3-P3
**pr_labels**: ``            # extra PR labels beyond inherited issue_top_labels / issue_scope_labels / issue_module_labels; add `drills` whenever the log contains substantive evidence/drill execution; all labels must already exist in GitHub
**pr_projects**: ``          # exact GitHub Project names for the PR; if blank, PR automation leaves project assignment empty by default
**pr_milestone**: ``         # exact GitHub milestone name for the PR; if blank, automation must leave the PR milestone empty
**pr_base**: ``              # exact PR base branch, e.g. main; if blank, dry-run may report it missing but must not guess another base
**pr_development_issue**: `` # exact issue number/url the PR should record in Metadata as Development issue; if blank, automation must leave that metadata row empty
**created_at**: `YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown`
**updated_at**: `YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown`
**reviewed_at**: `YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|pending`   # optional minimum review-state timestamp for logs that are actually reviewed as bounded governance packets
**created**: `YYYY-MM-DD`
**updated**: `YYYY-MM-DD`

---

## Frontmatter Lifecycle-Time Rule

- `created_at` and `updated_at` are the canonical artifact-lifecycle fields for this template.
- Prefer canonical UTC-second timestamps such as `2026-04-13T08:15:30Z` when exact repo-side lifecycle audit matters.
- Legacy day-only values such as `2026-04-13` remain valid when finer precision is unnecessary or unavailable.
- `reviewed_at` stays optional and should be used only when the log is actually reviewed as one bounded governance packet; do not force it onto every scratch draft.
- `created` and `updated` remain compatibility mirrors during migration and should reflect the day-level view of `created_at` and `updated_at` rather than introducing a second conflicting clock.

## Decision / Outcome

**Decision**:

- <What this phase delivers>
- <Default behavior / default semantics>

**Default choices (phase defaults / v1)** (optional, but recommended):

- <For example: dev/test first; avoid production-grade complexity; do not commit generated artifacts; required evidence JSON fields>
- draft 阶段默认继续把 source log 当作集中面；如果问题边界、规则、过程、reader summary 或 front-door 影响仍在变化，不要过早把 weak-structure 内容拆到多个 outlets。
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.
- `Evidence Footer Source` does not replace `Evidence`: the footer source feeds PR/gate automation, while `Evidence` remains the human ledger.

**PR summary bullets**:

- <1-3 bullets that explain what changed and why>

**PR checklist source**:

- Default source: reuse the child log's execution checklist for the generated PR checklist block.
- If a generated PR should omit or reorder checklist items, note that override explicitly here.

**PR links**:

- Log: `docs/logs/log-<ID>.md`
- Runbook: ``
- Evidence artifact: ``

**Evidence Footer Source**:

- `P1-C1-S1` | artifact: ``

- Keep footer rows low-cardinality: prefer one representative artifact per relevant unit instead of replaying the full artifact inventory.
- Generated PR body should keep `Evidence Footer` as the only optional section; development issue identity stays in `Metadata`.
- `Evidence Footer` rows must be copied only from `Evidence Footer Source` and must keep the same line shape.

## Exported Sections / Outlet Ownership

- Use this block only to split weak-structure content out of the source log after outlet ownership is explicit.
- Do not use outlet export to delete the source-log minimum core: `Decision / Outcome`, `PR Summary Inputs` when this log is an automation source, `Execution Checklist`, `Current Status`, and `Evidence` must remain readable here.
- Strong-structure sections stay owned by the source log unless a later contract explicitly authorizes a different automation reader model.
- Once the slice reaches stable close-out review, answer `contract / runbook / view / index/front-door / disposition/placement / log-retained core` explicitly; justified `no-op` is valid, but skipping the outlet decision is not.
- Do not export `runbook` or `view` mechanically; only export them when they have a stable reusable role beyond shortening one finished log.

**Outlet ownership**:

- `contract`: <stable rule text that should leave this log>
- `runbook`: <stable repeatable operator procedure that should leave this log>
- `view`: <reader-facing family or status summary that should leave this log>
- `index/front-door`: <navigation or entrypoint mutations that should leave this log>
- `disposition/placement`: <support-only / legacy / cleanup standing that should leave this log>
- `log-retained core`: <what must remain here as source-log strong structure plus bridge notes>

## Definitions (optional)

- <3-10 key terms so readers do not need to infer meaning>

## Constraints

- <For example: dumps are not committed to git; least privilege; low-cardinality reasons; machine-verifiable evidence>

## Scope

- `P0`: contract (default decisions, naming/fields, evidence contract)
- `P1`: <implementation / infra / scripts>
- `P2`: <drill / verify>
- `P3`: <drill / verify>
- (optional) `P4`: <single-command pipeline / hard gate>

## Success Criteria (DoD)

- <List 4-10 acceptance checks, ideally verifiable from evidence JSON / SQL / metrics>

## Stability (what stable means)

- This log can be marked `stable` when:
  - <The P0-Pn contract, entry scripts, and drills have all been exercised successfully>
  - The Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)
- `stable` is the normal gate for close-out review, not a command to emit every outlet; explicit `no-op` answers remain valid when `contract`, `runbook`, `view`, or `index/front-door` export is not warranted.

## P0 (Contract | v1)

### P0-C1-S1 (<Contract item 1>)

- <Naming / fields / semantics / constraints>

### P0-C1-S2 (<Contract item 2>)

- <Naming / fields / semantics / constraints>

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - <Input parameters>
  - <Output artifact paths>
  - <PASS/FAIL decision fields>

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `<ID>/P0-P3: <log title>`
  - discontinuous phases: `<ID>/P0+P3: <log title>`
  - mixed discontinuous + consecutive phases: `<ID>/P0+P3-P4: <log title>`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title: `<ID>/P*-C*-S*: <one-sentence summary>`.

**Branch convention**:

- For logs tied to a specific scope/index (for example, `S5B-3A` belongs to `S5B`, and `S0D-2A` belongs to `S0D`), prefer making P* code and documentation changes on a working branch with the same prefix:
  - For example, `S5B-3A` changes should usually land on an `S5B-*` branch such as `S5B-security-governance-hard-gates`.
  - `S0D-2A` style meta/docs/automation changes should usually land on an `S0D-*` branch such as `S0D-docs-management-v4`.
- If a single PR touches multiple scopes/indexes (for example both `S5B-3A` and `S0D-2A`), prefer splitting it into multiple PRs so each PR stays focused on one scope/index and its corresponding branch for easier aggregation and traceability.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, try to `commit/push` promptly on the matching scope branch:
  - For example, `S5B-4A` changes should normally land on an `S5B-*` top-level branch such as `S5B-security-governance-hard-gates`.
  - If a phase is unusually large or involves multiple contributors, you may open a short-lived child branch under the `S5B-*` branch, but the default is still not to create a separate branch for every log.
- The normal rhythm is: accumulate commits on the matching scope branch at `P*-C*-S*` granularity, then periodically open a PR from that branch into `main` for human review and merge.

## Plan (draft)

### P1 (<Implementation>)

- P1-C1-S1: ...
- P1-C1-S2: ...

### P2 (<Drill / Verify>)

- P2-C1-S1: ...
- P2-C1-S2: ...

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: ...
- [ ] `P0-C1-S2`: ...
- [ ] `P0-C1-S3`: ...

### P1 (...)

- [ ] `P1-C1-S1`: ...
- [ ] `P1-C1-S2`: ...

## Current Status (recommended)

- <One-line overall state for this source log>
- <What is already stable, what still remains open, and whether automation should still read this log as an active source>
- If the log is already stable or entering stable review, state whether the next step is a bounded `Pn+1` export package, direct log retention, or deferred export because target outlet identity is still not stable.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### <Pn-Cx-Sy> (<Drill name> | YYYY-MM-DD)

- headSha: `<git sha>`
- artifacts: `artifacts/_tmp_<...>/drills_<ts>.json`
- env (example, optional):
  - `<ENV>=<...>`
- expected:
  - ...
- observed:
  - ...

## Recent changes (for traceability, optional)

- YYYY-MM-DD: <What changed, why it is recorded, and how to trace it>
