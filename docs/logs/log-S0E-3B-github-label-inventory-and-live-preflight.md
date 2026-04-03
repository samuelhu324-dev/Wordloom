# log-S0E-3B (Phase 3B: GitHub label inventory and live preflight)

---

**id**: `S0E-3B`
**kind**: `log`
**title**: `GitHub label inventory and issue-label live preflight contract v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Labels, Automation, epic/s0, sub/1`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/322`
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
  **reference_log_1**: `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
  **reference_log_2**: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  **reference_log_3**: `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
**issue_keyword**: `contract`
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
**created**: `2026-04-03`
**updated**: `2026-04-03`

---

## Decision / Outcome

**Decision**:

- `S0E-3B` is the dedicated follow-up for the current labels problem in issue automation: it separates label inventory ownership and live-preflight behavior from the broader `S0E-2A` issue-creation contract.
- v1 keeps the boundary narrow: local derivation may still propose labels from log metadata, but GitHub remains the source of truth for which labels are actually usable at create/apply time.
- The issue draft path should support an explicit live label preflight before real issue creation so operators can detect taxonomy drift early instead of discovering missing labels only during `gh issue create`.

**Default choices (phase defaults / v1)**:

- Title keyword generation and label derivation remain separate concerns: `issue_keyword` still controls the fixed title prefix, while labels must come from the existing GitHub label catalog.
- Draft generation may run without GitHub access, but live label preflight must be opt-in and deterministic when requested.
- Advisory preflight should surface missing labels as structured warnings; real create mode remains fail-closed on missing GitHub labels.
- The repo should prefer one reusable live label preflight path instead of scattering `gh label list` checks across multiple scripts.
- Module labels remain best-effort and operator-confirmed; live preflight validates existence, not semantic correctness.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.
- `Evidence Footer Source` does not replace `Evidence`: the footer source feeds PR/gate automation, while `Evidence` remains the human ledger.

**PR summary bullets**:

- Split GitHub label inventory and live preflight into a dedicated `S0E-3B` slice instead of keeping it implicit inside `S0E-2A`.
- Add an explicit live label preflight path to `gen_issue_draft.py` so draft generation can warn or fail before real issue creation.
- Retain one representative issue-draft sample proving that the derived labels exist in the live GitHub repository label catalog.

**PR checklist source**:

- Default source: reuse this log's execution checklist for generated PR checklist blocks.

**PR links**:

- Log: `docs/logs/log-S0E-3B-github-label-inventory-and-live-preflight.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/issue-S0E-3B-github-label-inventory-and-live-preflight.json`

## Definitions (optional)

- `label inventory`: the live set of labels that already exists in the target GitHub repository.
- `derived labels`: the labels locally inferred from a structured log, including top/scope/sub/function/module labels.
- `live label preflight`: an explicit GitHub-backed check that compares derived labels against the live repository label inventory before issue creation.
- `advisory preflight`: a preflight run that records missing labels as warnings without creating an issue.
- `fail-closed create mode`: the rule that `gh issue create` must stop if any requested label is missing from GitHub.

## Constraints

- Do not silently invent or auto-create missing labels during issue draft generation.
- Do not conflate `label exists in GitHub` with `label is semantically the best one`; module-label selection still stays operator-reviewed.
- Do not require GitHub access for every local draft-generation call; live preflight is explicit rather than implicit.
- Keep live label preflight reusable from the same script that already owns derived issue labels.

## Scope

- `P0`: contract for label inventory ownership, advisory-vs-fail-closed semantics, and operator workflow
- `P1`: implement explicit live label preflight in the issue-draft generator
- `P2`: retain one representative draft-generation sample, then create and write back one live issue for the same label-preflight path
- `P3`: decide later rollout policy for whether selected higher-trust entrypoints should require live label preflight by default
- `P4`: record the controlled PR create/merge lifecycle for this slice without mixing it into the contract or draft-generation units

## Success Criteria (DoD)

- The repo has a written decision that GitHub's existing label catalog is the source of truth for issue-create label validity.
- Draft generation can perform an explicit live label preflight without needing to enter real create mode.
- Advisory preflight emits structured warnings when labels are missing instead of hiding the mismatch.
- Create mode still fails closed if any requested label does not exist in GitHub.
- At least one representative sample result shows the derived labels and the live-preflight outcome together in one structured artifact.
- The live issue creation and source-log write-back for this slice are recorded under explicit `P-C-S` units rather than only in narrative notes.
- The later controlled PR create/merge path has reserved `P-C-S` slots before execution starts so review-lifecycle evidence can be recorded without renumbering drift.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P4` have fixed the contract, the implementation path, the rollout boundary, and the controlled review-lifecycle accounting for live label preflight
  - the Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## Current Status

- `S0E-3B` is now opened as the dedicated slice for GitHub label inventory ownership and issue-label live preflight.
- `P0` is complete: the repo now has an explicit contract that live GitHub labels are authoritative, advisory preflight is separate from real create mode, and missing labels must never be auto-created on the fly.
- `P1` is complete: `scripts/issues/gen_issue_draft.py` now supports explicit live label preflight outside create mode, with separate warning-vs-fail behavior.
- `P2` is complete: one representative issue-draft sample was retained as `P2-C1-S1`, then live GitHub issue `#322` was created and written back to the source log as `P2-C1-S2`.
- `P3` remains open: the repo has not yet decided which higher-trust entrypoints, if any, should require live label preflight by default.
- `P4` remains open: the dedicated controlled PR create/merge lifecycle for `S0E-3B` has not been executed yet, but its accounting slots are now fixed in advance.

## P0 (Contract | v1)

### P0-C1-S1 (Label inventory ownership fixed | v1)

- Structured logs and draft-generation scripts may derive candidate labels locally, but GitHub remains the authority for whether those labels are valid for real issue creation.
- Live preflight therefore validates existence against the repository label catalog; it does not mutate GitHub state.

### P0-C1-S2 (Advisory vs fail-closed behavior fixed | v1)

- Draft generation may run in advisory mode, where missing labels are reported but no create/apply mutation happens.
- Real create mode remains fail-closed: missing labels must stop execution before `gh issue create` runs.
- Operators may optionally request fail-on-missing behavior during preflight when they want draft generation to behave like a gate.

### P0-C1-S3 (Evidence contract | v1)

- Representative evidence for this slice should retain:
  - the derived label set for one draft-generation sample;
  - the GitHub repository used for live preflight;
  - whether labels were missing or fully matched;
  - the generated draft path and structured result path.

## P1 (Implementation | v1)

### P1-C1-S1 (Issue draft live label preflight implemented | v1)

- `gen_issue_draft.py` should support an explicit live label preflight mode that can run without `--create`.
- The preflight should reuse the same repository-resolution and `gh label list` plumbing used by create mode so the validation surface does not drift.
- The result JSON should record whether live preflight ran, which repository it checked, and which labels were missing.

## P2 (Representative verification | v1)

### P2-C1-S1 (Representative issue draft sample retained | v1)

- Run the issue-draft generator on `S0E-3B` itself with live label preflight enabled.
- Retain the generated draft markdown and JSON result so later slices can reuse the sample when discussing rollout policy.

### P2-C1-S2 (Live issue creation and source-log write-back retained | v1)

- Run the same `S0E-3B` sample through explicit `--create` after live label preflight passes.
- Record the resulting live issue number/URL in the JSON sidecar and write the issue URL back to `links.issue` in a later tracked docs update.

## P4 (Controlled PR lifecycle accounting | v1)

### P4-C1-S1 (Dedicated controlled PR creation recorded | v1)

- When `S0E-3B` enters review, create one dedicated controlled PR that scopes only this slice's commits.
- Record the PR number/URL and the exact PR title/body scope used for the review unit.

### P4-C1-S2 (Merge and post-merge write-back recorded | v1)

- After the controlled PR is merged, record the merged PR reference back into `links.pr` and any exact-ID evidence rows needed by downstream lifecycle work.
- Keep merge accounting as a distinct step from PR creation so review and post-merge follow-through remain separately traceable.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-3B/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S0E-3B` changes should normally stay on the active `S0E-*` docs-management branch because the slice belongs to the same issue-automation spine.

**Commit discipline (recommended)**:

- Fix the label inventory contract first, then land the script change, then retain a live-preflight sample, then record the live issue creation/write-back before widening the rollout policy or opening the controlled PR.

## Plan (draft)

### P3 (Rollout policy)

- `P3-C1-S1`: decide which entrypoints should require live label preflight by default
- `P3-C1-S2`: decide whether missing-label advisory mode should stay available after rollout hardening

### P4 (Controlled PR lifecycle accounting)

- `P4-C1-S1`: create one dedicated controlled PR for `S0E-3B`
- `P4-C1-S2`: merge the dedicated PR and write back the merged PR reference

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: label inventory ownership fixed
- [x] `P0-C1-S2`: advisory vs fail-closed behavior fixed
- [x] `P0-C1-S3`: label-preflight evidence contract fixed

### P1 (Implementation)

- [x] `P1-C1-S1`: issue draft live label preflight implemented

### P2 (Representative verification)

- [x] `P2-C1-S1`: representative issue draft sample retained
- [x] `P2-C1-S2`: live issue creation and source-log write-back retained

### P3 (Rollout policy)

- [ ] `P3-C1-S1`: default-required entrypoints decided
- [ ] `P3-C1-S2`: advisory-mode retention policy decided

### P4 (Controlled PR lifecycle accounting)

- [ ] `P4-C1-S1`: dedicated controlled PR creation recorded
- [ ] `P4-C1-S2`: merge and post-merge write-back recorded

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.

### P0-C1-S1S2 / P1-C1-S1 (Label inventory contract and live preflight path retained | 2026-04-03)

- headSha: `<git sha>`
- artifacts:
  - `docs/logs/log-S0E-3B-github-label-inventory-and-live-preflight.md`
  - `scripts/issues/gen_issue_draft.py`
- expected:
  - `S0E-3B` should separate label inventory ownership and live-preflight behavior from the broader issue-creation contract.
  - The issue-draft generator should support explicit live label checking before real create mode.
- observed:
  - `S0E-3B` now records the narrow label-inventory contract, advisory/fail-closed split, and representative evidence expectations.
  - `scripts/issues/gen_issue_draft.py` now exposes a reusable live label preflight path so draft generation can detect missing GitHub labels before `gh issue create`.

### P2-C1-S1 (Representative live-preflight draft sample retained | 2026-04-03)

- headSha: `<git sha>`
- artifacts:
  - `docs/issues/issue-S0E-3B-github-label-inventory-and-live-preflight.md`
  - `docs/issues/issue-S0E-3B-github-label-inventory-and-live-preflight.json`
- expected:
  - The repo should retain one issue-draft sample that includes both derived labels and a live-preflight result against the repository's actual GitHub labels.
- observed:
  - Running `gen_issue_draft.py` on `S0E-3B` with live label preflight produced a draft plus structured JSON result under `docs/issues/`, proving the derived label set resolved against the repository's live GitHub labels before any real create mutation ran.

### P2-C1-S2 (Live issue creation and source-log write-back retained | 2026-04-03)

- headSha: `<git sha>`
- artifacts:
  - `docs/issues/issue-S0E-3B-github-label-inventory-and-live-preflight.json`
  - `docs/logs/log-S0E-3B-github-label-inventory-and-live-preflight.md`
- issue_url: `https://github.com/samuelhu324-dev/wordloom-v3/issues/322`
- issue_number: `322`
- expected:
  - After the representative live-preflight sample passes, the same slice should be able to create one real GitHub issue and then write the resulting issue URL back to the source log in a later tracked update.
- observed:
  - Explicit `--create` created live issue `#322`, the JSON sidecar retained the creation result fields, and this source log now records the same issue URL in `links.issue` as a separate tracked write-back step.

## Recent changes (for traceability, optional)

- 2026-04-03: opened `S0E-3B` to isolate GitHub label inventory ownership and issue-label live preflight from the broader `S0E-2A` issue-creation contract.
- 2026-04-03: extended `gen_issue_draft.py` with explicit live label preflight so draft generation can warn or fail before real issue creation.
- 2026-04-03: completed `P2-C1-S1` by retaining one representative `S0E-3B` draft-generation sample that records the live GitHub label check outcome alongside the derived draft metadata.
- 2026-04-03: completed `P2-C1-S2` by creating live GitHub issue `#322` through the automated `gen_issue_draft.py --create` path and writing the resulting issue URL back to this source log.