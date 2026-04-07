# log-S0F-3H (Phase 3H: recurring governance run model and ledger split)

---

**id**: `S0F-3H`
**kind**: `log`
**title**: `recurring governance run model and ledger split v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Governance, Runbook, Cleanup, Ledger, Template, epic/s0, sub/3h`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  **reference_log_1**: `docs/logs/log-S0F-3F-governance-contract-sweep-workflow.md`
  **reference_log_2**: `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  **reference_log_3**: `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
**issue_keyword**: `governance`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/3`
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
**created**: `2026-04-07`
**updated**: `2026-04-07`

---

## Decision / Outcome

**Decision**:

- `S0F-3H` opens the next follow-up slice for turning repeat governance work from long-lived origin logs into one reusable operating model.
- This slice exists because `S0F-3F` and `S0F-3G` proved two different kinds of recurring work, but both slices still carry a mixed burden:
  - they preserve the original design decisions for the workflow,
  - and they also keep accumulating later execution rounds as if they were the permanent operator surface.
- v1 therefore fixes one explicit split:
  - stable recurring method belongs in runbooks, packet shapes, and bounded templates,
  - per-run accounting belongs in logs, manifests, and evidence entries,
  - origin slices such as `S0F-3F` and `S0F-3G` remain the place where the model was established, but they should no longer be the only place where every future run is narrated.

**Default choices (phase defaults / v1)**:

- Keep logs as the ledger of what was done, not as the only evergreen operator manual.
- If the repo needs the same judgment or cleanup sequence more than once, extract the stable method into a runbook or a fixed packet template before opening more replay rounds.
- Open new bounded logs freely for materially distinct execution packages; do not force every later run back into `S0F-3F` or `S0F-3G` merely because those slices originated the method.
- Use `role first, disposition second` when splitting old structured logs: first decide where stable rule or procedure belongs, then decide whether the retained source log is `keep current`, `keep legacy`, `support-only`, or `defer cleanup`.
- A template is a reusable migration workflow, not a new filename convention or a requirement that every outlet always exist.
- `S0F-3F` and `S0F-3G` remain valid historical control slices, but future recurring execution should prefer smaller child ledgers, manifests, and runbook-driven packets.

## Scope

- `P0`: open `S0F-3H`, wire it into the `S0F` spine, and fix the boundary between origin logs, evergreen operator surfaces, and execution ledgers
- `P1`: define the recurring-run artifact set for governance work, including which responsibilities belong in runbook, packet template, log, manifest, and view
- `P2`: define naming and opening rules for future bounded execution logs so recurring work can branch into small ledgers without losing discoverability
- `P3`: define the first reusable templates for old structured-log extraction, including one clean sample lane and one mixed-role transformation lane
- `P4`: pilot the model on the next `S0F-1I` follow-up package so lifecycle-surface successor work no longer has to reopen `S0F-3G` as the primary operator worksheet

## Current Status

- `S0F-3H` is now opened as the next `S0F` follow-up slice because the repo has now outgrown the pattern where recurring governance work is driven mainly by appending more rounds to the original `3F` and `3G` logs.
- `P0` is now complete: the boundary is explicit that `S0F-3F` and `S0F-3G` are origin and control slices, while future recurring operation should move toward runbook-driven packets plus smaller per-run ledgers.
- `P1` is now complete: one artifact responsibility map now aligns recurring governance operation with the `S0F-4A` six-outlet model, so future work can decide consistently what belongs in `runbook`, `packet template`, `log`, `manifest`, and `view` without collapsing role and disposition back into the same file.
- `P2` is now complete: one naming and opening rule set now fixes how recurring governance work should open bounded execution logs without colliding with `S0F-2A` maintenance lanes, `S0F-2B` family-patch lanes, or the original control slices.
- The immediate next follow-up is now `P3`: publish the first reusable extraction templates so future mixed-role cleanup can start from one fixed packet shape rather than restating the same boundaries again.
- The first practical pilot after `P3` should still be the remaining `S0F-1I` lifecycle exact-path successor problem, but that work should now open as one bounded execution log under the `3H` naming model and only write consequence deltas back to `S0F-3G` if cleanup status actually changes.

## Problem Statement

- `S0F-3F` successfully fixed how families are swept and adjudicated, but repeated future use of that method should not require one ever-growing slice log.
- `S0F-3G` successfully fixed how cleanup rounds are staged and defended, but repeated future use of that method should not require one ever-growing slice log either.
- `S0F-4A` now gives a role-boundary and disposition model, but the repo still needs one operating layer that says how those rules get reused across many future packages.
- Without that operating layer, the repo keeps mixing three responsibilities in the same place:
  - defining the stable method,
  - recording one bounded execution,
  - and preserving long-tail historical context.
- The result is that logs become both the design spec and the operator console, which makes them harder to reuse cleanly and harder to thin later.

## Operating Split v1

### Stable Surfaces

- `runbook`: repeatable operator procedure, stop rules, checks, and ordered execution steps
- `packet template`: bounded input shape for one family or one cleanup/rewrite run
- `view`: optional reader-facing snapshot for current state, family map, or outcome table when a stable summary is useful

### Ledger Surfaces

- `log`: what was decided and executed for one bounded package or one materially distinct round
- `manifest`: machine-readable or audit-friendly file list, candidate set, or dependency set for that run
- `evidence`: exact verification notes, commands, outputs, commit hashes, and publish state

### Legacy Handling Rule

- If an older structured log still mixes enduring procedure with historical run detail, export the enduring procedure first, then thin the original log to its slice-local convergence ledger before deciding its placement.
- The repo may open more than one log for the same broad area when that improves auditability; the constraint is not "one area, one endless log", but "one bounded purpose per log".

## P1 Artifact Responsibility Map

### Alignment With `S0F-4A`

- `S0F-4A` remains the role-boundary source of truth:
  - `contract` owns stable current rule
  - `runbook` owns stable operator procedure
  - `view` owns bounded reader-facing summary
  - `index/front-door` owns current navigation
  - `log` owns slice-local ledger
  - `disposition/placement` owns file state only after role export is settled
- `S0F-3H/P1` does not replace that model.
- `S0F-3H/P1` fixes the recurring-operation layer that sits on top of it:
  - how one repeatable governance run should package its procedure, inputs, execution record, and optional reader summary
  - how to avoid putting all of that back into one endlessly growing log
- `packet template` is therefore not a seventh document role.
- It is one execution support artifact that helps later runs update the six `S0F-4A` outlets in a controlled order.

### Artifact Responsibilities

#### `runbook`

- use when:
  - the repo expects the same operator sequence to be replayed more than once
  - the stop rules, checks, or branch points are stable enough to survive beyond one package
- must own:
  - ordered operator steps
  - preflight checks
  - stop or continue rules
  - verification expectations
  - references to the current contract or current front-door reader surfaces
- must not own:
  - per-run candidate sets
  - one-off file lists
  - evolving historical narration of each execution round
- relation to `S0F-4A`:
  - this is the stable `runbook` outlet, not a support-only annex inside a log

#### `packet template`

- use when:
  - a recurring lane needs one bounded reusable input shape before execution begins
  - the repo must know exactly which files, outlets, and stop conditions a run is allowed to touch
- must own:
  - package boundary
  - required inputs
  - expected outlet targets
  - allowed writes and explicit non-writes
  - closure checks for the package
- must not own:
  - final evidence of what happened in a specific run
  - stable semantic rule text that belongs in a contract
  - disposition decisions that have not yet passed role export
- relation to `S0F-4A`:
  - the packet enforces `contract -> runbook -> index/front-door -> view -> log rewrite -> disposition/placement` as the default export order when a run actually closes

#### `log`

- use when:
  - one materially distinct package or round needs an auditable ledger
  - the repo needs to explain why a bounded run was opened, what changed, and what remained unresolved
- must own:
  - package-local decision record
  - execution narrative
  - retained bridge notes
  - evidence references
  - bounded next-step statement
- must not own permanently:
  - evergreen operator instructions
  - stable current rule concentration
  - repeatable packet shape once that shape is already reusable
- relation to `S0F-4A`:
  - this is the retained `log` outlet after exports, not the temporary dumping ground for every enduring responsibility

#### `manifest`

- use when:
  - one run needs an exact machine-readable or audit-friendly inventory
  - later readers must reconstruct candidate scope, dependency scope, move sets, or non-write sets without replaying prose
- must own:
  - exact file or candidate inventory
  - dependency or blocker set
  - explicit changed, kept, deferred, or non-write rows
- must not own:
  - the human explanation of why the package exists
  - stable operator guidance
  - front-door reader interpretation that belongs in a view
- relation to `S0F-4A`:
  - manifest is supporting ledger infrastructure; it helps execute and defend disposition but does not itself become a new role or new file-state class

#### `view`

- use when:
  - a bounded family or package now benefits from one reader-facing summary that should survive beyond the execution log
  - the repo needs a compact current-vs-support-only-vs-legacy reading surface
- must own:
  - bounded family summary
  - readable outcome table or family map
  - current-reader interpretation where replaying the full ledger would be wasteful
- must not own:
  - operator procedure
  - current rule enforcement semantics
  - raw execution evidence
- relation to `S0F-4A`:
  - this is the stable `view` outlet and should be created only when a genuine reader-facing summary exists, not to satisfy a matrix mechanically

### Responsibility Split Rules

- first question:
  - is this content a stable operating method, a bounded execution input, a run ledger, a machine-readable inventory, or a reader summary?
- second question:
  - if the content is stable and current, which `S0F-4A` outlet owns it?
- third question:
  - only after those ownership questions are resolved, does `disposition/placement` decide whether the retained file stays current, moves to `support-only`, remains `keep legacy`, or remains `defer cleanup`
- consequence:
  - do not solve mixed-role drift by inventing a new folder first
  - solve it by exporting stable responsibilities out of the log first

### Open-New-Log Rule v1

- open a new bounded log when any of these become true:
  - the package has a materially different candidate set or dependency set
  - the allowed writes differ from the prior run
  - the operator is answering a new question rather than replaying the same packet unchanged
  - the retained evidence would otherwise obscure the previous round's close-out
- do not open a new log merely because one more evidence line exists for the same unchanged package
- do not append a new long-lived replay series back into `S0F-3F` or `S0F-3G` once the method itself is already stable

### `S0F-1I` Pilot Preparation Rule

- for the remaining `S0F-1I` lifecycle exact-path successor package, the intended split is now:
  - `runbook`:
    - only if the lifecycle-successor resolution sequence is defended as repeatable beyond this one package
  - `packet template`:
    - exact-path consumer inventory, successor target, allowed writes, explicit non-writes, and close-out checks
  - `log`:
    - one bounded package ledger for why this successor run exists and what it changes
  - `manifest`:
    - exact lifecycle artifact list plus blocker resolution set
  - `view`:
    - only if later readers need a compact standing summary after the package closes
- therefore the next pilot should not begin by reopening `S0F-3G` as the primary worksheet.
- it should begin by opening one smaller package under the `3H` operating split and only then write cleanup consequences back to `3G` if relocation status actually changes.

## P2 Bounded Execution Log Naming And Opening Rules

### Naming Boundary

- bounded execution logs remain `log` role documents under the `S0F-4A` naming baseline.
- they do not create a new top-level role, a new folder class, or a replacement for maintenance or patch notes.
- the purpose of `P2` is therefore not to invent a new ontology.
- the purpose is to make recurring-run logs discoverable, narrow, and non-colliding.

### Canonical Filename Rule

- default filename shape:
  - `log-<owner-id>-run-<n>-<slug>.md`
- where:
  - `<owner-id>` is the narrowest family, slice, or target identifier that a reader would actually search first
  - `run-<n>` is the bounded execution-log sequence for that owner, starting at `run-1`
  - `<slug>` is the concrete package purpose, not a restatement of the whole origin workflow
- rationale:
  - keep the file clearly inside the existing `log` naming universe
  - distinguish recurring execution ledgers from full slice logs, maintenance logs, and patch notes
  - make it possible to open multiple logs for one owner without pretending they are new phases of the original origin slice

### Owner Selection Rule

- choose `<owner-id>` by reader lookup priority, not by historical credit:
  - use the target family or deferred row when the package is really about one target
  - use the workflow family only when the package truly spans more than one target under the same stable method
- examples:
  - use `S0F-1I` for a package that exists only to resolve the remaining `S0F-1I` lifecycle exact-path successor problem
  - use `S0F-3G` only if one later package again covers multiple cleanup rows as one genuine cleanup-family run rather than one target-specific follow-up
- do not default to `S0F-3H` as the owner id merely because the operating model came from this slice
- `S0F-3H` owns the method, not every later package filename

### Sequence Rule

- increment `run-<n>` only when the new log is materially distinct for the same owner.
- a materially distinct run means at least one of the following changed:
  - candidate set
  - dependency set
  - allowed writes
  - governing question
  - close-out consequence surface
- do not increment the sequence merely for one more evidence line or one small same-package replay.
- if the package is unchanged, keep adding evidence to the same bounded log or the same manifest set.

### Collision-Avoidance Rule

- do not use `run-<n>` logs where `S0F-2A` or `S0F-2B` already provide a better lane:
  - use `docs/logs/maintenance/` for real ops-maintenance work
  - use `docs/logs/patch/` for family patch or tiny direct patch lanes
- bounded execution logs under this `3H` model are for recurring governance packages that still need a substantive auditable ledger but no longer deserve to reopen the original control slice.
- do not use `P<n>` in the filename of these logs.
- `P/C/S` remain body-level execution markers and commit-subject notation, not the filename discriminator for recurring-run ledgers.

### Placement Rule

- keep bounded execution logs under `docs/logs/` by default.
- do not create a new top-level `runs/`, `packets/`, or `operations/` folder for this lane.
- if a future repo-wide volume problem appears, solve that later with an explicit placement slice rather than preemptively fragmenting discoverability now.
- support-only relocation remains a later disposition question, not part of the opening rule.

### Required Link Set At Open

- every bounded execution log should declare at least:
  - `parent_log`: the active spine or direct parent family log that keeps the high-level storyline readable
  - `reference_log`: the origin control slice or source-owner log whose method or standing produced this package
  - packet or manifest references when those files exist for the package
- rationale:
  - parent spine stays readable without becoming the operator notebook
  - origin slices keep traceability without needing to host every replay
  - the bounded package remains independently auditable

### Parent-Spine And Control-Slice Write-Back Rule

- parent spine:
  - always gets one concise status line when a bounded execution log opens or closes with a meaningful result
- origin control slice such as `S0F-3F` or `S0F-3G`:
  - gets a consequence write-back only when the package changes the standing of that slice's open row, blocker model, or cleanup/admission state
- do not mirror the full execution ledger back into the control slice once the method is already stable.
- this is the main mechanism that prevents `3F` and `3G` from turning back into endless operator notebooks.

### Opening Checklist v1

- before opening a bounded execution log, confirm all of the following:
  - the stable method already exists in a runbook, packet rule, or control slice
  - the package is narrower than reopening the full origin slice
  - the owner id is the narrowest reader-meaningful search key
  - the package needs an auditable ledger and is not just a patch or maintenance note
  - parent-spine write-back expectations are clear
- if those checks fail, either:
  - keep the work in the existing bounded log if the package is not actually new
  - escalate to a full slice if the work introduces a new stable method or policy
  - route to maintenance or patch lanes if the work is really small-work policy territory

### First Concrete Naming Example

- the next `S0F-1I` lifecycle-successor package should default to a filename of the form:
  - `log-S0F-1I-run-1-lifecycle-exact-path-successor-package.md`
- why this is the right example:
  - readers will search for `S0F-1I`, not for `S0F-3H`, when they want the target standing
  - the package is one bounded successor-resolution run, not a new full slice
  - the name makes clear that `S0F-3H` supplied the method while `S0F-1I` remains the target owner

## First Template Direction

- Clean sample lane: use the `WF` family as the positive-control example where one source can mostly map cleanly into current contract plus light retained history.
- Mixed-role transformation lane: use `S0F-1I` as the example where stable rule and procedure must be exported first, the original log then thinned, and cleanup only judged after exact-path consumers are reduced.
- Reusable sequence:
  - map outlet ownership
  - export stable current rule and procedure
  - thin the original log to slice-local ledger
  - classify disposition only after remaining consumers are explicit

## Execution Checklist

- [x] `P0`: open `S0F-3H` and fix the origin-log versus recurring-operation boundary
- [x] `P1`: define the artifact responsibility map for runbook, packet, log, manifest, and view
- [x] `P2`: fix naming and opening rules for future bounded execution logs
- [ ] `P3`: publish the first reusable extraction templates
- [ ] `P4`: pilot the model on the next `S0F-1I` lifecycle-successor package

## Evidence

- `2026-04-07`: Opened `S0F-3H` to separate recurring governance operating method from the historical origin ledgers in `S0F-3F` and `S0F-3G`, wired the new slice into the `S0F` parent spine as the next process-structure follow-up, and published the opening boundary at `headSha: 9cd6806ad79e0fd8d9ab16f4887cf5602f07f8e2`.
- `2026-04-07`: Completed `S0F-3H/P1` by fixing one recurring-run artifact responsibility map aligned with `S0F-4A`, including the `runbook` / `packet template` / `log` / `manifest` / `view` split, one open-new-log rule, and one `S0F-1I` pilot-preparation rule for the remaining lifecycle exact-path successor package at `headSha: fb1d1fa0eb490f2375d5386d4f50b1f8c1fd68e1`.
- `2026-04-07`: Completed `S0F-3H/P2` by fixing one bounded execution-log naming and opening model, including the canonical `log-<owner-id>-run-<n>-<slug>.md` rule, owner-selection and collision-avoidance rules against maintenance and patch lanes, parent-spine/control-slice write-back rules, and the first concrete filename model for the next `S0F-1I` lifecycle-successor package at `headSha: d8955db073660baa37c526f1cb9f3e740491208c`.
