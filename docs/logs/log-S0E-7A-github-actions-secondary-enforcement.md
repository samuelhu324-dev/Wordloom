# log-S0E-7A (Phase 7A: GitHub Actions secondary enforcement)

---

**id**: `S0E-7A`
**kind**: `log`
**title**: `workflow/github actions secondary enforcement v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Actions, Automation, epic/s0, sub/1`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/338`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/350`
  **runbook**: ``
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-6B-log-stability-and-gate-strategy.md`
  **reference_log_1**: `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  **reference_log_2**: `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  **reference_log_3**: `docs/logs/log-S3A-2A-4B-1A-git-actions.md`
**issue_keyword**: `workflow`
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
**created**: `2026-03-31`
**updated**: `2026-03-31`

---

## Decision / Outcome

**Decision**:

- `S0E-7A` is now the dedicated follow-up for GitHub Actions integration after `S0E-5C/P4` wired post-apply verification into the local live create path.
- This slice is GitHub-side only: it owns mirror verification in Actions, artifact publishing, and failure surfacing policy in CI.

**Default choices (phase defaults / v1)**:

- GitHub Actions remains `secondary enforcement`, not the primary publish-time owner.
- The primary publish-time owner stays the local create path fixed in `S0E-5C/P4`: `S6 -> live verify -> S7`.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.
- `Evidence Footer Source` does not replace `Evidence`: the footer source feeds PR/gate automation, while `Evidence` remains the human ledger.

**PR summary bullets**:

- Define GitHub Actions as a mirror verifier for live PR body contract checks instead of a replacement for local publish-time verification.
- Define the first minimal workflow shape for mirrored live PR verification in CI.
- Decide how Actions should publish artifacts and surface failures without pretending it prevented the original publish.

**PR checklist source**:

- Default source: reuse this log's execution checklist after `P0` is reviewed.

**PR links**:

- Log: `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
- Issue: ``
- Runbook: ``
- Evidence artifact: `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`

- Keep footer rows low-cardinality: prefer one representative artifact per relevant unit instead of replaying the full artifact inventory.
- Generated PR body should keep `Evidence Footer` and `Development Link` as separate sections.
- `Evidence Footer` rows must be copied only from `Evidence Footer Source` and must keep the same line shape.

## Definitions (optional)

- `primary publish-time owner`: the entrypoint that decides whether live publication proceeds before the mutation happens.
- `secondary enforcement`: a later verifier that re-checks live state after publication and emits machine-readable findings without claiming it prevented the original write.
- `mirror verifier`: a CI-side replay of the same live PR verification logic already fixed in the local create path.

## Constraints

- Do not move live publish authority from the local create path into GitHub Actions without a separate explicit decision slice.
- Do not mix local log gate policy into this slice; that now belongs to `S0E-6B`.
- Any later GitHub Actions workflow must reuse the same verifier semantics already fixed locally instead of inventing a second contract.

## Scope

- `P0`: fix the boundary between local primary verification and GitHub Actions secondary enforcement
- `P1`: define the first minimal GitHub Actions workflow shape and artifact contract for mirrored live verification
- `P2`: define failure surfacing, artifact publishing, and operator feedback rules for mirrored CI verification
- `P3`: define rollout boundary and success criteria for adopting the mirrored workflow in CI

## Success Criteria (DoD)

- The repo has a written decision that GitHub Actions is secondary enforcement and not the primary publish owner for PR create.
- The future Actions workflow shape reuses the same live PR verifier and produces explicit artifact paths instead of screenshot-only evidence.
- The future Actions workflow has explicit failure surfacing and artifact retention semantics.
- The first executable Actions scaffold now exists with explicit workflow inputs, mirror-verifier artifact outputs, and secondary-enforcement wording in the workflow summary.
- The retained artifact set is now explicit and machine-readable enough for later CI policy or audits to reason about a mirror-verifier run without reading screenshots or raw logs only.
- The rollout boundary and adoption criteria are now explicit enough to justify why automatic `pull_request` rollout is deferred and what evidence would be required before widening that boundary.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` have fixed the contract, workflow shape, and rollout boundary
  - at least one representative GitHub Actions mirror-verifier sample exists with traceable artifacts
  - the Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## Current Status

- `S0E-7A` is now opened as the next narrow slice after `S0E-5C/P4`.
- `P0` is now completed: GitHub Actions is explicitly scoped as secondary enforcement, not as the primary publish-time owner.
- `P1` is now completed: the first minimal mirror-verifier workflow shape is now fixed and scaffolded in GitHub Actions, with explicit manual inputs, explicit artifact outputs, and summary wording that preserves the secondary-enforcement boundary.
- `P2` is now completed: retained artifacts, artifact-manifest shape, and check-surface failure signaling are now fixed for the first mirror-verifier workflow.
- `P3` is now completed: the first rollout boundary remains intentionally manual-only, and the success criteria for later automatic CI adoption are now fixed.

## P0 (Boundary contract | v1)

### P0-C1-S1 (GitHub Actions ownership boundary fixed | v1)

- GitHub Actions should mirror the same live PR verifier already fixed in `S0E-5C/P4`; it should not become a replacement for the local create-path verification chain.
- The main reason is temporal: Actions runs after the publish event already exists, so it can detect drift and raise a machine-readable failure, but it cannot honestly claim that it prevented the original live PR creation.
- `S0E-7A` therefore keeps the ownership split explicit:
  - local create path = primary publish-time verification owner;
  - GitHub Actions = secondary post-publish enforcement and visibility layer.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-7A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `S0E-7A/P0-P3: github actions secondary enforcement`
  - discontinuous phases: `S0E-7A/P0+P3: github actions secondary enforcement`
  - mixed discontinuous + consecutive phases: `S0E-7A/P0+P3-P4: github actions secondary enforcement`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title: `S0E-7A/P*-C*-S*: <one-sentence summary>`.

**Branch convention**:

- `S0E-7A` changes should usually stay on the existing `S0E-*` working branch because this slice belongs to the same docs-management spine and is still closing automation/governance boundaries rather than a separate domain family.

## Plan (draft)

### P1 (GitHub Actions mirror-verifier workflow)

- [x] `P1-C1-S1`: define event triggers, workflow inputs, and artifact outputs for mirrored live PR verification
- [x] `P1-C1-S2`: decide how Actions should surface failure state without pretending it prevented publish

### P2 (Failure surfacing and artifacts)

- [x] `P2-C1-S1`: define artifact publishing shape for mirrored live verification
- [x] `P2-C1-S2`: define failure surfacing in workflow summary, checks, and retained artifacts

### P3 (Rollout boundary)

- [x] `P3-C1-S1`: define which PR events and branches should run mirrored verification first
- [x] `P3-C1-S2`: define success criteria for adopting the mirrored workflow in CI

## Execution Checklist (unchecked)

### P0 (Boundary contract)

- [x] `P0-C1-S1`: GitHub Actions ownership boundary fixed

### P1 (GitHub Actions mirror-verifier workflow)

- [x] `P1-C1-S1`: define event triggers, workflow inputs, and artifact outputs
- [x] `P1-C1-S2`: decide failure surfacing and operator feedback shape

### P2 (Failure surfacing and artifacts)

- [x] `P2-C1-S1`: define artifact publishing shape
- [x] `P2-C1-S2`: define failure surfacing and retained evidence

### P3 (Rollout boundary)

- [x] `P3-C1-S1`: define initial workflow trigger boundary
- [x] `P3-C1-S2`: define CI adoption success criteria

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1 (GitHub Actions secondary-enforcement boundary fixed | 2026-03-31)

- headSha: `9832ca0d`
- artifacts:
  - `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  - `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  - `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  - `docs/logs/log-S3A-2A-4B-1A-git-actions.md`
- expected:
  - the next GitHub-side slice should open without collapsing GitHub Actions into the primary publish owner
- observed:
  - `S0E-7A` now fixes that boundary: Actions remains secondary enforcement and is limited to post-publish enforcement plus visibility rather than primary publish-time ownership

## P1 (First minimal GitHub Actions mirror-verifier workflow | v1)

### P1-C1-S1 (Workflow trigger, input, and artifact contract fixed | v1)

- The first executable GitHub Actions workflow for this slice should bootstrap with `workflow_dispatch` only.
- The reason is sequencing: `S0E-7A/P1` should prove the reusable workflow shape and verifier wiring first, while `P3` should separately decide which PR events and branch scopes deserve automatic rollout.
- The first workflow contract is now fixed as:
  - workflow file: `.github/workflows/s0e-pr-body-secondary-enforcement.yml`;
  - trigger surface: manual `workflow_dispatch`;
  - required inputs: `source_log_path`, `pr_ref`;
  - optional input: `repo` override, otherwise the workflow uses the current repository;
  - execution surface: `ubuntu-latest` with `bash`, `actions/checkout`, `actions/setup-python`, and the existing `scripts/issues/verify_live_pr_body_contract.py` entrypoint.
- The first artifact outputs are now fixed as:
  - fetched live PR body markdown;
  - structured verifier result JSON;
  - console JSON emitted by the verifier run.

### P1-C1-S2 (Secondary-enforcement failure surfacing shape fixed | v1)

- The first workflow should fail visibly when mirrored verification detects drift, but its wording must not imply that CI blocked the original publish.
- The failure surfacing shape is now fixed as:
  - the workflow always writes a `GITHUB_STEP_SUMMARY` section that explicitly labels the run as `secondary enforcement`;
  - the summary must state that a failure means post-publish drift was detected rather than prevented;
  - artifacts must be uploaded even on verifier failure so operators can inspect the live body and result payload before acting;
  - the job should fail only after summary + artifact publication steps have had a chance to run.
- This keeps CI honest: it can become a strong mirror and alerting surface without rewriting the ownership boundary already fixed in `S0E-5C/P4`.

### P1-C1-S1S2 (minimal mirror-verifier workflow shape fixed and scaffolded | 2026-03-31)

- headSha: `09cf513a`
- artifacts:
  - `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  - `.github/workflows/s0e-pr-body-secondary-enforcement.yml`
  - `scripts/issues/verify_live_pr_body_contract.py`
  - `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
- expected:
  - the repo should define the first minimal GitHub Actions workflow shape for mirrored live PR verification without prematurely expanding rollout scope or pretending CI is the primary publish owner
- observed:
  - `S0E-7A/P1` now fixes both the workflow contract and the first operator-facing failure shape: a manual mirror-verifier workflow exists, it reuses the local verifier entrypoint, emits explicit artifacts, and fails with secondary-enforcement wording only after summary + artifact publication

## P2 (Failure surfacing and retained artifact contract | v1)

### P2-C1-S1 (Retained artifact publishing shape fixed | v1)

- The mirror-verifier workflow should retain a bounded artifact set that is useful both to a human operator and to later machine-side policy checks.
- The first retained artifact shape is now fixed as:
  - `live-pr-body.md`: the fetched live PR body used as the verification subject;
  - `verify-result.json`: the structured verifier result payload;
  - `verify-console.json`: the console-emitted verifier output for direct replay/debugging;
  - `workflow-summary.md`: a retained copy of the exact summary text written to `GITHUB_STEP_SUMMARY`;
  - `artifact-manifest.json`: a machine-readable manifest that records run identity, result, retained artifact paths, and failure semantics.
- This artifact set stays intentionally small. It captures the live subject, the contract verdict, the operator-facing explanation, and a single machine-readable index without turning the workflow into a generic log archive.

### P2-C1-S2 (Failure surfacing across summary, checks, and retained evidence fixed | v1)

- Failure surfacing should now exist on three distinct surfaces, each with a clear role:
  - workflow summary: human-readable explanation with explicit `secondary enforcement` wording and non-deceptive phrasing about post-publish drift;
  - check annotations: `::notice` on pass and `::error` on failure or missing retained evidence, so the GitHub run UI exposes the verdict without opening artifacts first;
  - retained evidence: `workflow-summary.md` plus `artifact-manifest.json`, so later review or automation can reconstruct what the workflow concluded.
- The first failure contract is now fixed as:
  - the job still fails on non-pass result or missing result artifact;
  - summary + retained artifacts + annotations must all be produced before the terminal failure step runs;
  - retained evidence must explicitly classify the failure as `post-publish drift detected` rather than any language implying pre-publish prevention.
- This gives `S0E-7A` a cleaner enforcement stack: operators get immediate UI feedback, artifacts remain inspectable after the run, and later policy slices can consume the manifest without scraping step text.

### P2-C1-S1S2 (retained artifacts and failure surfacing contract fixed | 2026-03-31)

- headSha: `84892992`
- artifacts:
  - `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  - `.github/workflows/s0e-pr-body-secondary-enforcement.yml`
  - `scripts/issues/verify_live_pr_body_contract.py`
  - `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
- expected:
  - the repo should define a bounded retained-artifact contract and a multi-surface failure-signaling policy for the mirror-verifier workflow without broadening rollout scope yet
- observed:
  - `S0E-7A/P2` now fixes both: the workflow retains five explicit evidence files, emits a machine-readable artifact manifest, writes GitHub check annotations, and preserves secondary-enforcement wording across summary and retained artifacts

## P3 (Rollout boundary and CI adoption criteria | v1)

### P3-C1-S1 (Initial rollout boundary fixed | v1)

- The first rollout boundary should remain intentionally narrow: the mirror-verifier workflow stays `workflow_dispatch`-only in v1 rather than auto-subscribing to `pull_request` events.
- The reason is input determinism, not lack of confidence in GitHub Actions itself:
  - the current verifier requires an explicit `source_log_path` plus `pr_ref`;
  - the repository does not yet have a stable machine rule that can derive the correct source log from every PR event without risking false attribution or multi-log ambiguity;
  - widening the trigger surface before that mapping is explicit would create noisy or misleading enforcement instead of trustworthy secondary enforcement.
- The initial eligible run boundary is therefore fixed as:
  - manually triggered runs only;
  - operator supplies the exact source log path and PR ref;
  - preferred first-class use is PRs created through the local `S0E-5C/P4` path, because that path already treats one source log as the contract owner for the live PR body.
- `P3` therefore does not widen the trigger boundary yet. It explicitly chooses correctness of attribution over early automation breadth.

### P3-C1-S2 (CI adoption success criteria fixed | v1)

- Automatic CI rollout should be considered only after the manual mirror-verifier path proves that its attribution, evidence retention, and UI surfacing are stable enough to trust.
- The first adoption criteria are now fixed as:
  - at least one representative `pass` run exists with complete retained artifacts: live body, verify result JSON, console JSON, workflow summary markdown, and artifact manifest JSON;
  - at least one representative `drift-detected` or non-pass run exists whose summary wording, check annotations, manifest classification, and terminal job result all agree on the same outcome;
  - operators can determine the verdict from summary/check surfaces plus retained artifacts without needing raw runner logs as the primary evidence source;
  - a future automatic trigger proposal must also explain how `source_log_path` will be derived or supplied deterministically for `pull_request` events.
- Only after those conditions are met should a later slice widen the workflow from manual replay into automatic PR-event mirroring.
- This keeps the rollout honest: CI adoption is gated on attribution and evidence quality, not merely on the existence of a runnable workflow.

### P3-C1-S1S2 (manual-only rollout boundary and CI adoption criteria fixed | 2026-03-31)

- headSha: `ecc21e6a`
- artifacts:
  - `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  - `.github/workflows/s0e-pr-body-secondary-enforcement.yml`
  - `scripts/issues/verify_live_pr_body_contract.py`
  - `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
- expected:
  - the repo should decide whether the first rollout should auto-subscribe to PR events or remain manual, and it should state what evidence is required before widening that boundary
- observed:
  - `S0E-7A/P3` now fixes both points: the initial rollout remains manual-only because `source_log_path` is not yet deterministically derivable from PR events, and future automatic CI adoption now has explicit pass/fail evidence and attribution criteria

## Recent changes (for traceability, optional)

- 2026-04-03: wrote back live issue `#338`, remediated the required sidebar parent relationship, created and merged PR `#350`, applied the final issue-conclusion body, and confirmed the live issue is closed.
- 2026-03-31: re-scoped `S0E-7A` to GitHub-side concerns only, leaving Actions as secondary enforcement and moving local log stability / gate policy to `S0E-6B`.
- 2026-03-31: completed `P0` by fixing the GitHub Actions ownership boundary in one place: Actions is not the primary publish owner and should mirror the same verifier semantics already fixed in the local create path.
- 2026-03-31: completed `P1` by fixing and scaffolding the first manual mirror-verifier workflow in GitHub Actions, including explicit inputs, explicit artifacts, and summary wording that preserves the secondary-enforcement boundary.
- 2026-03-31: completed `P2` by fixing the retained artifact set, adding a machine-readable artifact manifest, and surfacing mirror-verifier results through workflow summary, GitHub check annotations, and artifact-first retained evidence.
- 2026-03-31: completed `P3` by explicitly keeping the first rollout manual-only, deferring automatic PR-event mirroring until source-log attribution is deterministic, and fixing the first CI adoption success criteria.