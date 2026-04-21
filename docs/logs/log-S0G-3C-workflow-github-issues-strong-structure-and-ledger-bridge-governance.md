# log-S0G-3C (Phase 3C: WORKFLOW-GITHUB-ISSUES strong-structure and ledger-bridge governance)

---

**id**: `S0G-3C`
**kind**: `log`
**title**: `workflow github issues strong-structure and ledger-bridge governance v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Automation, Evidence, epic/s0, sub/3c`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-3B-carrier-branch-cleanup-and-mainline-extraction-governance.md`
  **reference_log_1**: `docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md`
  **reference_log_2**: `docs/logs/log-S0G-2B-support-only-ledger-placement-and-patch-ledger-bridge.md`
  **reference_log_3**: `docs/logs/log-S0G-3A-runbook-release-issue-concentration-and-ledger-naming-governance.md`
  **reference_log_4**: `docs/runbook/support-only/_template-run-ledger-SUP.md`
**issue_keyword**: `workflow`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/3`
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
- Day-level precision is acceptable while the runbook-family identity and stage-granularity contract are still being fixed.
- `reviewed` should remain `pending` until the repo agrees on workflow profiles, batch identity rules, and the strong-structure bridge between parent run ledgers, SUP ledgers, and PATCH ledgers.

## Decision / Outcome

**Decision**:

- `S0G-3C` opens the next bounded follow-up after the initial `S0G-3A/3B` governance rounds: fix the strong-structure contract for the current GitHub Issues automation family before any broad template rewrite or follow-up refill execution starts.
- The current runbook-family token is too wide for the defended operator surface. This lane reopens the family identity question explicitly: the active workflow should be governed as `WORKFLOW-GITHUB-ISSUES`, not the broader `WORKFLOW-GITHUB`, unless later evidence proves a wider family boundary is still necessary.
- The current `Run Ledger Table` is too batch-only for this workflow family. This lane must define target-level and stage-level accounting so readers can tell which object ran which stage, what blocked, who ran it, and when.
- `child issue` and `parent issue` are not the same lifecycle. This lane must fix two workflow profiles with distinct stage sets instead of leaving both under one prose-only pipeline description.
- `ledger / SUP / PATCH` are all necessary for this family, but they currently lack one strong-structure bridge model. This lane must define which stable keys let a later `SUP` or `PATCH` row attach to one existing run, one target, and one stage without reopening packet identity by guesswork.
- Run sequence identity should mean one bounded admitted batch, not merely one button press. Later retries, refill rounds, completion passes, and evidence sharpening for the same bounded batch should normally attach through `SUP`, while `ledger-run-002` should open only when a genuinely new related batch begins.
- The child-issue workflow profile is now fixed to use `PR_MERGED` rather than a review-only or mixed PR stage name, because the defended lifecycle state here should distinguish pre-merge work from merged-state admission clearly.
- `SUP` and `PATCH` now follow an effect-based dual-surface rule instead of a forced single bucket: admitted-reading follow-up belongs in `SUP`, repair diffs belong in `PATCH`, and one follow-up packet may require both surfaces at once.

**Default choices (phase defaults / v1)**:

- Treat the current family identity question as fixed at contract level but not yet migrated in file identity: this lane now defends `WORKFLOW-GITHUB-ISSUES` as the narrower family while leaving rename execution to a later rewrite packet.
- Define workflow profiles before changing templates. Template rewrites should follow the agreed structure, not lead it.
- A parent run ledger for this family should own at least three accounting grains:
  - batch/run grain
  - target grain
  - target-stage grain
- `SUP` default boundary: later evidence, refill work, stage completion, and verdict sharpening for an already-open bounded batch.
- `PATCH` default boundary: bounded repair work that unblocks or corrects the workflow while the runbook release stays unchanged.
- If one change both repairs the workflow and changes the admitted reading of a previously opened batch, use both surfaces explicitly: `PATCH` for the repair packet, `SUP` for the later batch-level or stage-level write-back.
- Do not silently treat child-issue and parent-issue flows as the same just because both use GitHub issues.
- Do not open `ledger-run-002` only because a second pass was needed on the same bounded issue set.

## PR Summary Inputs (optional)

- This packet is expected to drive later runbook-template and ledger-template rewrites, so the review summary should focus on workflow-family identity, stage granularity, and bridge semantics across `Run Ledger`, `SUP`, and `PATCH`.

**PR summary bullets**:

- Narrow the current workflow-family identity from broad `WORKFLOW-GITHUB` toward the defended `WORKFLOW-GITHUB-ISSUES` operator surface.
- Fix strong-structure accounting for batch, target, and target-stage rows so readers can tell what actually ran, what blocked, who ran it, and when.
- Define child-issue vs parent-issue workflow profiles and the bridge keys that let `SUP` and `PATCH` attach to the right existing run/state instead of floating as prose-only follow-up packets.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0G-3C-workflow-github-issues-strong-structure-and-ledger-bridge-governance.md`
- Runbook: `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- Evidence artifact: `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`

**Evidence Footer Source**:

- `P0-C1-S1` | artifact: `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- `P0-C1-S2` | artifact: `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- `P1-C1-S1` | artifact: `docs/runbook/support-only/_template-run-ledger-SUP.md`

## Definitions (optional)

- **workflow profile**: one defended lifecycle shape for a specific target kind, such as `child issue full lifecycle` or `parent issue light lifecycle`.
- **target grain**: one stable accounting row for a single operated object inside a bounded run, for example one child issue log or one parent issue log.
- **target-stage grain**: one stable accounting row for a single stage under one target, such as `CREATION`, `PR_PENDING`, `PR_REVIEWED_OR_MERGED`, or `CONCLUSION`.
- **batch identity**: the rule that one run-row sequence represents one bounded admitted issue set, not merely one operator invocation.
- **strong-structure bridge**: the stable key model that lets `Run Ledger`, `SUP`, and `PATCH` refer to the same run, target, and target-stage without prose-only matching.

## Constraints

- Do not treat the current `WORKFLOW-GITHUB` token as final if the defended workflow surface is actually GitHub Issues only.
- Do not rewrite templates or migrate file names before the target/stage model is fixed.
- Do not use `SUP` and `PATCH` as interchangeable names for "later work"; each must have a defended structural boundary.
- Do not let the parent run ledger remain only a batch-summary surface if later readers need target-stage accountability.
- Do not open new run-ledger sequences for ordinary completion/refill rounds on the same bounded batch.

## Scope

- `P0`: workflow-family identity and accounting-grain contract
- `P1`: workflow profiles and stage taxonomy for child issue vs parent issue
- `P2`: `Run Ledger` / `SUP` / `PATCH` strong-structure bridge keys and sequence rules
- `P3`: next-lane rewrite rule for runbook and template migration after the contract is fixed

## Success Criteria (DoD)

- One explicit rule states whether the defended family should be named `WORKFLOW-GITHUB-ISSUES` instead of the broader `WORKFLOW-GITHUB`.
- One explicit accounting model exists for batch, target, and target-stage grains under this family.
- One explicit workflow-profile split exists for child-issue lifecycle vs parent-issue lifecycle.
- One explicit bridge model exists for how `SUP` and `PATCH` attach to an existing run, target, and target-stage.
- One explicit sequence rule exists for when to stay inside `RUN-001 + SUP` versus when to open `ledger-run-002`.
- One explicit next step exists for rewriting the current runbook and template set after the contract is fixed.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the family identity rule is explicit;
  - the workflow-profile and stage taxonomy are explicit;
  - the batch/target/stage accounting grains are explicit;
  - the `SUP` / `PATCH` bridge rules are explicit enough to drive the first strong-structure template rewrite.

## P0 (Contract | v1)

### P0-C1-S1 (Workflow-family identity narrowing rule | v1)

- Re-evaluate the current family token as part of this lane.
- The defended target is `WORKFLOW-GITHUB-ISSUES`, because the current operator surface governs GitHub issue and PR lifecycle automation rather than an open-ended GitHub workflow family.
- This lane fixes the naming contract first; any file rename, successor release, or alias strategy should follow only after the naming contract is explicit.

### P0-C1-S2 (Accounting grain rule | v1)

- The current family needs at least three strong-structure grains:
  - one run/batch row for the bounded admitted issue set;
  - one target row per operated object;
  - one target-stage row per lifecycle stage under that target.
- Batch-only status is insufficient for this family because later readers need to see which targets completed which stages, which stages were blocked, and which stages still need follow-up.

### P0-C1-S3 (Batch identity rule | v1)

- `ledger-run-001` should represent one bounded admitted issue set, not merely one operator pass.
- Later completion passes, refill rounds, and evidence sharpening for that same set should normally stay under the same run row and attach through `SUP`.
- Open `ledger-run-002` only when the operated issue set is materially new rather than a continuation of the existing bounded batch.

## P1 (Workflow profiles | v1)

### P1-C1-S1 (Child-issue workflow profile | fixed target)

- Fixed profile name: `child-issue-full-lifecycle`.
- Fixed stage set:
  - `CREATION`
  - `PR_PENDING`
  - `PR_MERGED`
  - `CONCLUSION`
- This profile should support explicit blocked or partial outcomes at any stage, including metadata gaps such as missing milestone or missing parent-issue linkage.

### P1-C1-S2 (Parent-issue workflow profile | fixed target)

- Fixed profile name: `parent-issue-light-lifecycle`.
- Fixed stage set:
  - `CREATION`
  - `CONCLUSION`
- This profile should still support explicit stage status, blockers, and follow-up requirements even though it does not traverse a child-style PR stage chain.

### P1-C1-S3 (Stage-row minimum fields | fixed target)

- Each target-stage row must express at least:
  - `run_row_id`
  - `target_id`
  - `target_kind`
  - `workflow_profile`
  - `stage_name`
  - `stage_status`
  - `blocking_reason_class`
  - `attempt_started_at`
  - `attempt_completed_at`
  - `executed_by`
  - `artifact_ref`
  - `needs_follow_up`

## P2 (Ledger / SUP / PATCH bridge | v1)

### P2-C1-S1 (SUP boundary rule | fixed target)

- `SUP` is the default follow-up surface when the bounded batch stays the same and the work primarily sharpens, completes, narrows, or revises the admitted reading of an existing run/target/stage.
- Typical `SUP` cases include:
  - later stage completion on an already-open batch;
  - refill of omitted issue or conclusion write-back;
  - explanation of why an earlier stage was omitted or blocked;
  - later evidence that changes how the parent ledger should read an existing stage result.

### P2-C1-S2 (PATCH boundary rule | fixed target)

- `PATCH` is the default follow-up surface when bounded repair work changes scripts, manifests, docs, or workflow mechanics while the runbook release stays unchanged.
- A `PATCH` row should still point back to the affected run/target/stage set instead of floating only as a repair note.
- If one follow-up both changes the workflow implementation and changes how an admitted stage should now be read, record both surfaces explicitly: `PATCH` for the repair packet, `SUP` for the parent-ledger follow-up.

### P2-C1-S3 (Dual-surface effect rule | fixed target)

- `SUP` vs `PATCH` is not a forced single-choice classification for this family.
- The boundary should follow effect, not packet vanity:
  - admitted-reading follow-up belongs in `SUP`;
  - repair diff belongs in `PATCH`.
- One follow-up packet may legitimately bind to both surfaces when it contains both kinds of effect.

### P2-C1-S4 (Bridge key rule | draft target)

- The strong-structure bridge should let `Run Ledger`, `SUP`, and `PATCH` all refer to:
  - one `run_row_id`
  - one `target_row_id`
  - one `target_stage_row_id`
- Later template rewrites should not rely on prose-only matching such as file names or comments to decide which run or stage a `SUP` or `PATCH` entry belongs to.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- Source-log work inside this lane still uses `S0G-3C/P<phase>-C<cycle>-S<steps>: <summary>`.
- Any later template or runbook rewrite packet opened because of this lane should use the naming surface that matches the rewritten object, not a generic governance title.

**Branch convention**:

- Keep this lane as source-log governance work until the strong-structure contract is fixed.
- Do not start broad runbook/ledger/template rewrites from this scaffold alone.

**Commit discipline (recommended)**:

- Fix naming, workflow profiles, and bridge keys first.
- Only after that should later packets rewrite the current runbook family, run-ledger table shapes, or `SUP/PATCH` templates.

## Plan (draft)

### P3 (Next-lane rewrite rule)

- P3-C1-S1: fix the next rewrite sequence for `WORKFLOW-GITHUB-ISSUES` runbook identity, parent run-ledger table shape, and `SUP/PATCH` template upgrades after the contract is stable

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: workflow-family identity narrowing rule fixed
- [x] `P0-C1-S2`: accounting grain rule fixed
- [x] `P0-C1-S3`: batch identity rule fixed

### P1 (Workflow profiles)

- [x] `P1-C1-S1`: child-issue workflow profile fixed
- [x] `P1-C1-S2`: parent-issue workflow profile fixed
- [x] `P1-C1-S3`: target-stage minimum fields fixed

### P2 (Ledger / SUP / PATCH bridge)

- [x] `P2-C1-S1`: SUP boundary rule fixed
- [x] `P2-C1-S2`: PATCH boundary rule fixed
- [x] `P2-C1-S3`: dual-surface effect rule fixed
- [ ] `P2-C1-S4`: bridge key rule fixed

### P3 (Next-lane rewrite rule)

- [ ] `P3-C1-S1`: post-contract rewrite sequence fixed

## Current Status (recommended)

- `S0G-3C` is now the bounded discussion surface for the strong-structure gap in the current GitHub Issues automation family.
- The immediate problem is no longer only packet extraction or branch cleanup; it is that the current runbook/ledger shape is too weakly structured for a multi-stage, multi-target workflow family.
- The current contract direction is now narrower and more concrete: the defended family token is `WORKFLOW-GITHUB-ISSUES`, the child-issue PR stage is `PR_MERGED`, target-stage rows now have a minimum required field set, and `SUP/PATCH` may dual-bind when one follow-up changes both admitted reading and repair implementation.
- The next discussion step should now finish the remaining bridge-key and rewrite-sequencing questions before any rewrite execution starts:
  - the exact `run_row_id / target_row_id / target_stage_row_id` bridge-key shape;
  - whether any additional actor/review fields must be mandatory beyond the current minimum;
  - the rewrite sequence for runbook identity, parent ledger table shape, and `SUP/PATCH` template upgrades.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this packet records the current weak-structure surfaces that now need stronger batch/target/stage and bridge contracts.

### P0-C1-S1 (current runbook family and parent ledger are strong enough to start, but too weak for stage-granular follow-up governance | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  - `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- expected:
  - the current surfaces should already show where runbook identity, parent run accounting, and later `SUP/PATCH` binding exist, so this lane can refine them rather than inventing them from zero.
- observed:
  - the current runbook already binds parent, supplement, and patch ledger series, but the parent ledger still reads mainly at batch summary grain and does not yet make child-vs-parent workflow profiles or target-stage accountability explicit.

### P1-C1-S1 (existing SUP template proves later-evidence follow-up is already modeled, but not yet tied to strong target-stage keys | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/runbook/support-only/_template-run-ledger-SUP.md`
- expected:
  - the current template should already show whether later evidence refinement is intended to exist as its own ledger class.
- observed:
  - the template already models later-evidence follow-up through `SUP`, including parent-ledger actions such as `append-evidence`, `rewrite-run-row`, and `reopen-run-verdict`, but it does not yet define the stronger target-stage bridge keys this family now needs.

### P2-C1-S3 (SUP and PATCH dual-binding rule fixed at effect level | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  - `docs/runbook/support-only/_template-run-ledger-SUP.md`
  - `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- expected:
  - the current family should be able to express later admitted-reading follow-up and bounded repair follow-up without collapsing both effects into one fake bucket.
- observed:
  - the current runbook already separates `SUP` from `PATCH`, and this lane now fixes the stronger reading rule: admitted-reading follow-up goes to `SUP`, repair diff goes to `PATCH`, and one real follow-up may require both surfaces simultaneously.

## Recent changes (for traceability, optional)

- 2026-04-21: opened `S0G-3C` to govern workflow-family identity narrowing, child-vs-parent workflow profiles, batch/target/stage accounting granularity, and strong-structure bridge rules across `Run Ledger`, `SUP`, and `PATCH`.