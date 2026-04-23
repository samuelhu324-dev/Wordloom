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
**created**: `YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown`
**updated**: `YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown`
**reviewed**: `YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|pending`   # optional minimum review-state timestamp for logs that are actually reviewed as bounded governance packets
**source_reader_model**: `mixed-source-v1` # source-log reader shape, not contract semantics; bump only when this log family's in-log extraction model changes materially
**extraction_surface_version**: `extractable-rules-v1|none` # version of the in-log extraction surface; use `none` only when this log is intentionally not an extraction source

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this template.
- These frontmatter fields own `artifact lifecycle time` only; they should not be overloaded to answer `semantic effective time` or `reader/routing validity time` for downstream contracts or ledgers.
- Prefer canonical UTC-second timestamps such as `2026-04-13T08:15:30Z` when exact repo-side lifecycle audit matters.
- Legacy day-only values such as `2026-04-13` remain valid when finer precision is unnecessary or unavailable.
- If a later packet needs contract-effective dates, keep that rule on the contract surface rather than widening log frontmatter with duplicate semantic-effective fields by default.
- If a later packet needs ledger-validity dates, treat those as routing/verdict fields on the ledger surface rather than as new log-lifecycle timestamps.
- `reviewed` should be used only when the log is actually reviewed as one bounded governance packet; do not force it onto every scratch draft.
- `source_reader_model` and `extraction_surface_version` version the source-log reader/extraction shape only; they do not version release semantics and should not replace contract release ids.
- Bump `source_reader_model` only when a reader or extractor would have to interpret this log differently from earlier logs in the same family.
- Bump `extraction_surface_version` when the in-log extraction table/labels/classification rules change materially; do not bump it for ordinary narrative edits.

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

## Extractable Rule Surface (recommended)

- Use this section when the log may later feed `contract`, `view`, `runbook`, or other downstream reader surfaces.
- The goal is not to make the whole log hard-structured; the goal is to expose one explicit extraction surface so later contract work does not depend on re-interpreting mixed narrative prose.
- Normalize candidate text to the smallest stable rule statement that could stand alone in a later contract or view.
- Do not embed long rationale or evidence prose inside `candidate text`; keep rationale and evidence references separate so one shared reason can support multiple candidate rows.
- `contract-candidate` rows should read as present-tense stable rule candidates.
- `rationale-only` rows explain why a rule cluster exists but should not become standalone contract statements.
- `support-only` rows may stay useful for adoption, examples, or evidence without becoming contract meaning.
- `mixed-awaiting-split` is valid when the source still blends rule text with reason/evidence; use it as an explicit warning rather than forcing premature extraction.
- `view-candidate` and `runbook-candidate` are valid when the stable downstream owner is not a contract.

| packet id | source anchor | extraction class | candidate text | downstream owner | split status | shared reason group | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R01` | `<section / heading / bullet range>` | `contract-candidate|rationale-only|support-only|mixed-awaiting-split|view-candidate|runbook-candidate` | `<normalized rule or summary text>` | `contract|view|runbook|log-retained|support-only` | `ready|needs-corroboration|needs-split|not-for-extraction` | `RG-01|none` | `<artifact, source slice, or none>` | `<short extraction note>` |

- If one row is really one parent rule plus several child details, prefer either:
  - one parent `contract-candidate` row plus child rows that are also `contract-candidate`, when the children may evolve independently
  - one combined `contract-candidate` row, when the parent and details are not expected to evolve independently
- If a candidate row still contains both rule and reason, keep it as `mixed-awaiting-split` until the normalized rule text can be stated cleanly.

### Shared Reason Groups (optional, recommended when multiple rows share one rationale)

- Use shared reason groups when several candidate rows exist for one common why.
- This section prevents repeating the same rationale prose inside multiple candidate rows or later contract clauses.
- Reason groups are explanation surfaces, not contract rows.

| reason group | applies to packet ids | reason summary | source refs | notes |
| --- | --- | --- | --- | --- |
| `RG-01` | `R01; R02` | `<one shared rationale for this packet cluster>` | `<source sections or artifacts>` | `<why this is shared rather than repeated>` |

## Source Reader Model / Versioning (recommended for reusable log families)

- Use this section when a log family is expected to grow large enough that readers, extractors, or review workflows need explicit source-shape compatibility notes.
- Version the source reader model forward; do not try to retroactively rewrite every historical log into the newest shape.
- Contract release ids still own semantic release history; source-reader versions only explain how to read and extract from the source log itself.
- When the log family changes materially, prefer opening a new `source_reader_model` generation and documenting compatibility here rather than silently changing extraction assumptions across many existing logs.

| field | value | notes |
| --- | --- | --- |
| current source reader model | `mixed-source-v1` | `<current in-log reader/extractor shape>` |
| extraction surface version | `extractable-rules-v1|none` | `<classification/table version used by this log>` |
| compatibility expectation | `forward-readable|requires-manual-bridge|n/a` | `<whether older logs can still be read/extracted under the current model>` |
| migration note | `<optional bounded note>` | `<how later logs should transition without reopening all older logs>` |

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
- When `Extractable Rule Surface` is present, treat it as the primary source-log handoff for downstream contract/view/runbook extraction; do not force reviewers to reconstruct candidate rules only from narrative sections.
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

## Optional Required Processing Chain

Use this section when the source log may emit, revise, reopen, or reconcile contract work and reviewers need one explicit pre-execution declaration of which write-back steps must run.

| chain step | required state | primary owner surface | trigger question | completion evidence | notes |
| --- | --- | --- | --- | --- | --- |
| `source extraction` | `<required>` | `<source log>` | `<has the bounded packet and source slice been identified tightly enough to route?>` | `<bounded scope plus source anchors or artifacts>` | `<entry step for the packet>` |
| `SUP` | `<required|conditional|not-required|already-satisfied>` | `<supplement ledger or n/a>` | `<is this packet later evidence against one existing source-owned row?>` | `<accepted SUP row or explicit no-SUP verdict>` | `<why SUP is or is not entered>` |
| `parent ledger` | `<required|conditional|not-required|already-satisfied>` | `<parent support-only ledger or n/a>` | `<does the packet change one source-owned routing verdict?>` | `<parent-ledger write-back or explicit no-parent-ledger verdict>` | `<why routing ownership does or does not apply>` |
| `contract impact decision` | `<required>` | `<source log>` | `<is the packet evidence-only sharpening, routing rewrite, semantic-release change, or family-boundary change?>` | `<explicit classified verdict>` | `<decision gate before downstream mutation>` |
| `contract mutation` | `<required|conditional|not-required|already-satisfied>` | `<release contract or family-level contract decision>` | `<does the packet change defended rule meaning or family boundary standing?>` | `<new release, revised note, or explicit no-contract-mutation verdict>` | `<meaning changed normally implies new release>` |
| `transition register update` | `<required|conditional|not-required|already-satisfied>` | `<family transition register or n/a>` | `<did family-level reader standing change, with or without one new release?>` | `<register row or explicit no-register-change verdict>` | `<reader-standing change, not release creation alone, is the trigger>` |
| `bridged contract reconciliation` | `<required|conditional|not-required|already-satisfied>` | `<affected parent or bridged contract surfaces>` | `<do other current readers now need reconciliation or redirect notes?>` | `<reconciled bridge note or explicit no-bridge-impact verdict>` | `<keep broad parent and narrow current readers coherent>` |

- Use the section only when contract-facing write-back steps are materially in scope; do not force it into logs that have no contract or reader-surface consequences.
- If `Extractable Rule Surface` exists, `source extraction` should point to that table first rather than to broad prose-only sections.
- `required state` must be declared before execution and should stay one of:
  - `required`
  - `conditional`
  - `not-required`
  - `already-satisfied`
- `contract impact decision` should remain mandatory whenever the log may affect contract or family reader standing.
- If the packet is later evidence against one existing source-owned row, the source log must answer explicitly whether `SUP` and `parent ledger` are required rather than leaving that path implicit.
- If the packet may change family-level reader standing, `transition register update` should default to at least `conditional` before execution.
- A short packet-specific decision note may follow the table, but the table is the minimum reusable declaration surface.

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
