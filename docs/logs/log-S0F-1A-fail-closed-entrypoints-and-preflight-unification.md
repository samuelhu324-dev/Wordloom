# log-S0F-1A (Phase 1: fail-closed entrypoints and preflight unification)

---

**id**: `S0F-1A`
**kind**: `log`
**title**: `fail-closed entrypoints and preflight unification v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Automation, Drills, Evidence, epic/s0, sub/1a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0E-7G-publish-verify-remediation-gate-workflow-dispatch-wrapper-surface.md`
  **reference_log_1**: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  **reference_log_2**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_3**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_4**: `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
  **reference_log_5**: `docs/logs/log-S0E-7E-publish-verify-remediation-gate-thin-orchestration-entrypoint.md`
**issue_keyword**: ``
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: ``
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-04`
**updated**: `2026-04-04`

---

## Decision / Outcome

**Decision**:

- `S0F-1A` is the first follow-up slice under `S0F`, and it directly addresses the still-soft entrypoints exposed by the current docs/GitHub lifecycle: issue creation, PR create front-half, and post-merge issue/PR live mutation.
- v1 will not add new automation families first; it will make existing real-mutation entrypoints fail-closed, narrow, and explicitly preflighted.
- The immediate target is one consistent rule: preview may warn, but create/apply/publish must stop when the required contract is missing or ambiguous.

**Default choices (phase defaults / v1)** (optional, but recommended):

- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.
- Real `create-issue` may not proceed when `issue_keyword` is inferred, when `Context` is still scaffold/placeholder, or when controlled metadata does not pass preflight.
- Real PR publish may not proceed from plain `plan_pr_prep` output alone; it must pass the create-time front-half preflight gate first.
- Real issue conclusion / relationship / PR body rewrite may not proceed through raw family apply scripts when a thin gate or guarded wrapper exists for that family.
- Retry is reserved for transient execution surfaces such as GitHub/network/process failures; semantic failures must be corrected at the source contract and then rerun.
- GitHub Actions remains optional secondary enforcement, not the primary place where these invariants are first defined.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.
- `Evidence Footer Source` does not replace `Evidence`: the footer source feeds PR/gate automation, while `Evidence` remains the human ledger.

**PR summary bullets**:

- Fix the first fail-closed boundary for real issue creation by stopping on inferred keyword, scaffold Context, and uncontrolled metadata gaps.
- Make PR create front-half preflight the only allowed path before any live PR publish step.
- Converge issue conclusion, relationship attach, and PR body rewrite toward wrapper-only live mutation entrypoints instead of raw family apply calls.

**PR checklist source**:

- Default source: reuse the child log's execution checklist for the generated PR checklist block.
- If a generated PR should omit or reorder checklist items, note that override explicitly here.

**PR links**:

- Log: `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
- Runbook: ``
- Evidence artifact: ``

## Definitions (optional)

- `fail-closed entrypoint`: a real create/apply/publish surface that stops on missing or ambiguous contract inputs instead of guessing or silently downgrading.
- `preview-only warning`: a dry-run warning that is allowed to exist so long as it cannot cross the boundary into a real mutation.
- `wrapper-only mutation`: a rule that live state changes must pass through the contract-owned gate/wrapper surface rather than a lower-level family apply command.
- `transient retry`: a retry caused by process, network, or remote-service instability rather than by contract ambiguity.
- `semantic retry`: an invalid retry attempt that reruns the same ambiguous inputs without first correcting the source contract.

## Constraints

- Do not classify prose quality as replayable just to make the pipeline look more automated.
- Do not allow inferred title keyword, scaffold Context, or placeholder PR summary to cross into a real live mutation path.
- Do not let older family scripts remain de facto canonical just because they are convenient to call directly.
- Do not require GitHub Actions before local fail-closed boundaries exist.

## Scope

- `P0`: contract for fail-closed entrypoints, retry vocabulary, and wrapper-only mutation rules
- `P1`: real issue creation hard-fail boundary
- `P2`: PR create front-half preflight as the only allowed live publish entry
- `P3`: issue conclusion / relationship / PR body rewrite wrapper convergence
- (optional) `P4`: narrow secondary-enforcement policy for later CI/GitHub Actions rollout

## Success Criteria (DoD)

- Real issue creation fails closed when `issue_keyword` is inferred, when `Context` is scaffold/placeholder, or when controlled metadata is missing.
- A plain PR-prep dry-run preview can no longer be mistaken for an allowed live publish path.
- Live mutation families with existing wrappers/gates can no longer be called through softer raw apply entrypoints without explicit operator opt-in and retained evidence.
- Retry semantics clearly distinguish transient execution failures from semantic contract failures.
- The resulting contract can explain why GitHub Actions is optional secondary enforcement rather than the primary fix.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the `P0-P3` contract and entrypoint cleanup have all been exercised successfully;
  - the Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## P0 (Contract | v1)

### P0-C1-S1 (Issue creation hard-fail boundary fixed | v1)

- Real `create-issue` must stop when:
  - `issue_keyword` would be inferred instead of read from an allowed explicit source;
  - `Context` is still scaffold/placeholder;
  - controlled metadata required for create-time mutation is missing, malformed, or conflicts with live prerequisites.
- Dry-run issue draft generation may still surface the same defects as warnings, but those warnings may not cross into real creation.

### P0-C1-S2 (PR create front-half boundary fixed | v1)

- `plan_pr_prep` remains a preview/planning surface, not a publish authorization surface.
- Any real PR create path must pass the create-time front-half preflight gate before branch materialization, remote publish, or live PR creation.
- Placeholder summary/checklist/body defects must remain stop conditions for live PR creation.

### P0-C1-S3 (Wrapper-only live mutation boundary fixed | v1)

- When a guarded adapter or thin gate exists for `issue-conclusion`, `issue-relationship`, or `pr-body-rewrite`, that wrapped surface becomes the canonical live mutation entrypoint.
- Lower-level apply scripts may remain for bounded internal reuse, but they should no longer be treated as the operator-facing default path.

### P0-C1-S4 (Retry vocabulary fixed | v1)

- `transient retry` is valid only for execution instability such as process timeout, CLI auth hiccup, or remote API/network failure.
- `semantic retry` is invalid when the source contract is still ambiguous; the operator must first fix the source log/manifest/metadata and then rerun from the top.
- Failure artifacts must make this distinction explicit so operators do not respond to semantic drift with blind reruns.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-1A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `S0F-1A/P0-P3: fail-closed entrypoints and preflight unification`
  - discontinuous phases: `S0F-1A/P0+P3: fail-closed entrypoints and preflight unification`
  - mixed discontinuous + consecutive phases: `S0F-1A/P0+P3-P4: fail-closed entrypoints and preflight unification`

**Branch convention**:

- `S0F-1A` related changes should stay on `S0F-*` working branches, currently `S0F-docs-management-v6`.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, commit and push promptly on `S0F-docs-management-v6` so the new spine does not drift ahead of origin.

## Plan (draft)

### P1 (Issue creation hard-fail)

- P1-C1-S1: define the exact create-time stop conditions for inferred keyword and scaffold Context
- P1-C1-S2: wire those conditions into the real issue creation entrypoint and retained result semantics

### P2 (PR preflight unification)

- P2-C1-S1: define the single mandatory live publish front-half preflight rule
- P2-C1-S2: retain one sample that proves preview warning does not imply publish eligibility

### P3 (Wrapper convergence)

- P3-C1-S1: inventory current raw family apply entrypoints versus wrapper-owned entrypoints
- P3-C1-S2: define canonical operator-facing entrypoints for issue conclusion, relationship attach, and PR body rewrite

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: issue creation hard-fail boundary fixed
- [ ] `P0-C1-S2`: PR create front-half boundary fixed
- [ ] `P0-C1-S3`: wrapper-only live mutation boundary fixed
- [ ] `P0-C1-S4`: retry vocabulary fixed

### P1 (Issue creation hard-fail)

- [ ] `P1-C1-S1`: exact create-time stop conditions defined
- [ ] `P1-C1-S2`: create-time fail-closed enforcement implemented

### P2 (PR preflight unification)

- [ ] `P2-C1-S1`: mandatory live publish preflight rule fixed
- [ ] `P2-C1-S2`: representative preview-vs-publish sample retained

### P3 (Wrapper convergence)

- [ ] `P3-C1-S1`: raw versus wrapped mutation entrypoints inventoried
- [ ] `P3-C1-S2`: canonical operator-facing wrapper surfaces fixed

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

## Recent changes (for traceability, optional)

- 2026-04-04: created `S0F-1A` as the first v6 slice to address fail-closed issue creation, PR preflight, wrapper-only live mutation, and retry semantics.