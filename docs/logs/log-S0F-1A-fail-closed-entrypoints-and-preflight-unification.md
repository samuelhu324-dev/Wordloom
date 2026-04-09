# log-S0F-1A (Phase 1: fail-closed entrypoints and preflight unification)

---

**id**: `S0F-1A`
**kind**: `log`
**title**: `fail-closed entrypoints and preflight unification v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Automation, Drills, Evidence, epic/s0, sub/1a`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/364`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/365`
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/support-only/s0/log-S0E-7G-publish-verify-remediation-gate-workflow-dispatch-wrapper-surface.md`
  **reference_log_1**: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  **reference_log_2**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_3**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_4**: `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
  **reference_log_5**: `docs/logs/support-only/s0/log-S0E-7E-publish-verify-remediation-gate-thin-orchestration-entrypoint.md`
**issue_keyword**: `automation`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
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
**pr_development_issue**: `#364`
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
- Real `create-issue` may not proceed when `issue_keyword` is inferred or when controlled metadata does not pass preflight, but it only needs the `Context` section to exist structurally; create-time Context content may remain empty.
- Real PR publish may not proceed from plain `plan_pr_prep` output alone; it must pass the create-time front-half preflight gate first.
- Real issue conclusion / relationship / PR body rewrite may not proceed through raw family apply scripts when a thin gate or guarded wrapper exists for that family.
- Retry is reserved for transient execution surfaces such as GitHub/network/process failures; semantic failures must be corrected at the source contract and then rerun.
- GitHub Actions remains optional secondary enforcement, not the primary place where these invariants are first defined.
- `S0F-1A` 沿用 `S0F` 的 `road-002` milestone 归属；在 exact `M*-P*` slot 还未单独记账前，这里只补现有 roadmap/milestone 锚点，不新造 roadmap phase。
- 实质性的 `Context` prose generation and write-back belongs to issue conclusion, not issue creation; create-time `single-generate` remains optional one-item authoring help rather than a mandatory live-create gate.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.
- `Evidence Footer Source` does not replace `Evidence`: the footer source feeds PR/gate automation, while `Evidence` remains the human ledger.

**PR summary bullets**:

- Fix the first fail-closed boundary for real issue creation by stopping on inferred keyword and uncontrolled metadata gaps while keeping `Context` structurally present but create-time-empty.
- Make PR create front-half preflight the only allowed path before any live PR publish step.
- Converge issue conclusion, relationship attach, and PR body rewrite toward wrapper-only live mutation entrypoints instead of raw family apply calls.
- Narrow GitHub Actions and workflow_dispatch surfaces back to explicit secondary enforcement so local fail-closed entrypoints remain the primary ownership boundary.

**PR checklist source**:

- Default source: reuse the child log's execution checklist for the generated PR checklist block.
- If a generated PR should omit or reorder checklist items, note that override explicitly here.

**PR links**:

- Log: `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
- Runbook: ``
- Evidence artifact: `docs/issues/raw-live-mutation-S0F-1A-p3-inventory.json`

## Definitions (optional)

- `fail-closed entrypoint`: a real create/apply/publish surface that stops on missing or ambiguous contract inputs instead of guessing or silently downgrading.
- `preview-only warning`: a dry-run warning that is allowed to exist so long as it cannot cross the boundary into a real mutation.
- `wrapper-only mutation`: a rule that live state changes must pass through the contract-owned gate/wrapper surface rather than a lower-level family apply command.
- `transient retry`: a retry caused by process, network, or remote-service instability rather than by contract ambiguity.
- `semantic retry`: an invalid retry attempt that reruns the same ambiguous inputs without first correcting the source contract.

## Constraints

- Do not classify prose quality as replayable just to make the pipeline look more automated.
- Do not allow inferred title keyword, placeholder `Context` scaffold lines, or placeholder PR summary to cross into a real live mutation path.
- Do not let older family scripts remain de facto canonical just because they are convenient to call directly.
- Do not require GitHub Actions before local fail-closed boundaries exist.

## Scope

- `P0`: contract for fail-closed entrypoints, retry vocabulary, and wrapper-only mutation rules
- `P1`: real issue creation hard-fail boundary
- `P2`: PR create front-half preflight as the only allowed live publish entry
- `P3`: issue conclusion / relationship / PR body rewrite wrapper convergence
- `P4`: narrow secondary-enforcement policy for later CI/GitHub Actions rollout

## Success Criteria (DoD)

- Real issue creation fails closed when `issue_keyword` is inferred or when controlled metadata is missing, while still preserving an empty-but-present `Context` section at create time.
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
  - controlled metadata required for create-time mutation is missing, malformed, or conflicts with live prerequisites.
- Real `create-issue` must preserve the canonical `Context` section, but create-time content may remain intentionally empty; conclusion owns the first required substantive Context write-back.
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

- P1-C1-S1: define the exact create-time stop conditions for inferred keyword and placeholder Context scaffold lines
- P1-C1-S2: wire those conditions into the real issue creation entrypoint and retained result semantics

### P2 (PR preflight unification)

- P2-C1-S1: define the single mandatory live publish front-half preflight rule
- P2-C1-S2: retain one sample that proves preview warning does not imply publish eligibility

### P3 (Wrapper convergence)

- P3-C1-S1: inventory current raw family apply entrypoints versus wrapper-owned entrypoints
- P3-C1-S2: define canonical operator-facing entrypoints for issue conclusion, relationship attach, and PR body rewrite

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: issue creation hard-fail boundary fixed
- [x] `P0-C1-S2`: PR create front-half boundary fixed
- [x] `P0-C1-S3`: wrapper-only live mutation boundary fixed
- [x] `P0-C1-S4`: retry vocabulary fixed

### P1 (Issue creation hard-fail)

- [x] `P1-C1-S1`: exact create-time stop conditions defined
- [x] `P1-C1-S2`: create-time fail-closed enforcement implemented

### P2 (PR preflight unification)

- [x] `P2-C1-S1`: mandatory live publish preflight rule fixed
- [x] `P2-C1-S2`: representative preview-vs-publish sample retained

### P3 (Wrapper convergence)

- [x] `P3-C1-S1`: raw versus wrapped mutation entrypoints inventoried
- [x] `P3-C1-S2`: canonical operator-facing wrapper surfaces fixed

### P4 (Secondary-enforcement narrowing)

- [x] `P4-C1-S1`: local-primary versus GitHub-secondary boundary fixed

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1S2S3S4 (fail-closed entrypoint contract fixed | 2026-04-04)

- headSha: `ccdf702ff2d2c9aa12aeddff93cdaf0c0906aaae`
- artifacts:
  - `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - one explicit contract fixes create-time stop conditions, PR front-half preflight boundary, wrapper-only mutation, and retry vocabulary
  - the new v6 child slice is linked into the parent spine instead of staying as an isolated note
- observed:
  - `S0F-1A` now records the exact fail-closed entrypoint contract for issue creation, PR front-half preflight, wrapper-only live mutation, and transient-versus-semantic retry boundaries
  - `S0F` parent now treats `S0F-1A` as the first concrete child slice and records the first implementation evidence under the new spine

### P1-C1-S1S2 (real issue creation fail-closed enforcement landed | 2026-04-04)

- headSha: `ccdf702ff2d2c9aa12aeddff93cdaf0c0906aaae`
- artifacts:
  - `scripts/issues/gen_issue_draft.py`
  - `docs/issues/issue-S0F-1A-create-preflight-fail.md`
  - `docs/issues/issue-S0F-1A-create-preflight-fail.json`
  - `docs/issues/issue-S0F-1A-single-generate-draft.md`
  - `docs/issues/issue-S0F-1A-single-generate-draft.json`
- expected:
  - real `create-issue` stops before GitHub mutation when `issue_keyword` would be inferred
  - real `create-issue` stops when `Context` is scaffold/placeholder instead of a single-generated block
  - dry-run draft-generation still produces retained artifacts for review even when real creation would fail closed
- observed:
  - `gen_issue_draft.py` now treats inferred `issue_keyword` as a create-time stop condition and emits a non-zero exit before any live issue creation is attempted
  - the same entrypoint now treats scaffold/placeholder Context as a create-time stop condition for real creation
  - one retained `--create` sample for `S0F-1A` failed closed on the blank `issue_keyword` path, while one single-generated dry-run sample still produced the expected markdown and JSON artifacts for review

### P2-C1-S1S2 (mandatory PR front-half preflight boundary landed | 2026-04-04)

- headSha: `e2bf872b6bad67c4766ca15c0eebc496c27a8609`
- artifacts:
  - `scripts/issues/create_pr_from_plan.py`
  - `docs/issues/pr-prep-S0F-1A-p2-stop-manifest.json`
  - `docs/issues/pr-prep-S0F-1A-p2-stop-manifest-plan.json`
  - `docs/issues/pr-prep-S0F-1A-p2-stop-body.md`
  - `docs/issues/pr-prep-S0F-1A-p2-stop-manifest-front-half-preflight-result.json`
  - `docs/issues/pr-prep-S0F-1A-p2-stop-create-blocked-utf8.txt`
- expected:
  - live `create_pr_from_plan.py` stops unless a matching `pr-create-front-half-preflight` artifact exists and explicitly allows continuation
  - one retained stop sample proves `plan_pr_prep` preview generation can still succeed while live publish remains blocked before local branch materialization
- observed:
  - `create_pr_from_plan.py` now fails closed when the front-half preflight artifact is missing, points at a different plan item, or carries a non-allow decision
  - the retained `S0F-1A` stop sample still generated a valid PR-prep plan and body preview with `summary_bullet_count = 3`, but front-half preflight blocked continuation because `candidate_pr_branch` reused the occupied `S0F-docs-management-v6` branch
  - replaying `create_pr_from_plan.py` against that stop sample now exits non-zero with `PR create fail-closed preflight blocked publish before local branch materialization: Local branch already exists: S0F-docs-management-v6`, proving preview warning no longer implies publish eligibility

### P3-C1-S1S2 (wrapper-only live mutation convergence landed | 2026-04-04)

- headSha: `e123c71f3ccb35ef07fd7a4c3ee0bde103ef7c52`
- artifacts:
  - `scripts/issues/raw_live_mutation_guard.py`
  - `scripts/issues/apply_issue_conclusion_from_plan.py`
  - `scripts/issues/apply_issue_relationships.py`
  - `scripts/issues/apply_pr_body_scope_with_pre_gate.py`
  - `scripts/issues/apply_pr_body_rewrite_batch.py`
  - `docs/issues/raw-live-mutation-S0F-1A-p3-inventory.json`
  - `docs/issues/issue-conclusion-S0F-1A-p3-raw-blocked.txt`
  - `docs/issues/issue-relationship-S0F-1A-p3-raw-blocked.txt`
  - `docs/issues/pr-body-rewrite-S0F-1A-p3-raw-blocked.txt`
- expected:
  - raw family apply scripts remain available only for bounded internal reuse and can no longer act as operator-facing default live mutation entrypoints
  - issue conclusion, relationship attach, and single-PR body rewrite each point operators to a canonical guarded wrapper or thin-gate delegated surface instead of allowing direct raw apply
- observed:
  - `raw_live_mutation_guard.py` now centralizes one internal-only guard and raw issue-conclusion plus issue-relationship apply scripts enforce it before any GitHub mutation path starts
  - `apply_pr_body_scope_with_pre_gate.py` now treats its inner live rewrite function as internal-only and the historical batch rewrite script also fails closed unless an internal-only flag is supplied for bounded reuse
  - the retained `S0F-1A` inventory plus three block samples now show the exact canonical surfaces for `issue-conclusion`, `issue-relationship`, and `pr-body-rewrite`, and each raw entrypoint exits with a wrapper-only guidance message instead of behaving like a default operator path

### P4-C1-S1 (GitHub Actions secondary-enforcement boundary narrowed | 2026-04-04)

- artifacts:
  - `docs/issues/github-actions-secondary-enforcement-S0F-1A-p4-boundary.json`
  - `.github/workflows/s0e-publish-verify-remediation-gate-read-only-wrapper-dispatch.yml`
  - `.github/workflows/s0e-pr-body-secondary-enforcement.yml`
- expected:
  - GitHub Actions surfaces remain explicitly optional secondary enforcement after local fail-closed entrypoints have already decided whether create/apply/publish may continue
  - workflow summaries and retained manifests can no longer be read as if `workflow_dispatch` or mirror verification owned publish authorization
- observed:
  - the new `S0F-1A` boundary artifact records local fail-closed wrappers and the thin gate as the primary ownership surface, while both GitHub workflows are explicitly classified as read-only or post-publish secondary enforcement only
  - the read-only wrapper dispatch workflow now states `local fail-closed family entrypoint` as the primary mutation owner and retains the same artifact-first failure semantics without claiming publish prevention
  - the PR body mirror workflow now states `local create path` as the primary publish owner, treats attribution failure as `skipped-before-verifier`, and records its workflow role as post-publish secondary enforcement rather than publish authorization

## Recent changes (for traceability, optional)

- 2026-04-04: created `S0F-1A` as the first v6 slice to address fail-closed issue creation, PR preflight, wrapper-only live mutation, and retry semantics.
- 2026-04-04: completed `P0` by fixing the first explicit contract for create-time stop conditions, PR front-half preflight language, wrapper-only mutation boundaries, and transient-versus-semantic retry vocabulary.
- 2026-04-04: completed `P1` by hardening `scripts/issues/gen_issue_draft.py` so real `create-issue` fails closed on inferred keyword and scaffold/placeholder Context while still preserving reviewable draft/result artifacts.
- 2026-04-04: completed `P2` by hardening `scripts/issues/create_pr_from_plan.py` so live PR publish now requires a matching successful front-half preflight artifact, then retained one `S0F-1A` stop sample that proves preview generation does not imply publish eligibility.
- 2026-04-04: completed `P3` by hardening raw issue-conclusion, issue-relationship, and PR body rewrite mutation paths behind one internal-only guard, then retaining one inventory artifact plus one raw-block sample per family to prove guarded wrapper convergence.
- 2026-04-04: completed `P4` by fixing one explicit local-primary versus GitHub-secondary boundary artifact and tightening both GitHub workflow summaries/manifests so `workflow_dispatch` and mirror verification remain secondary enforcement only.
- 2026-04-04: corrected the lifecycle contract so create-time issue bodies keep an empty-but-present `Context` section while the first substantive `Context` prose is generated only during issue conclusion.
- 2026-04-04: completed the corrected `S0F-1A` full-auto rerun end-to-end with live parent issue `#363`, live child issue `#364`, merged PR `#365`, and guarded post-merge issue conclusion that now allows targeted conclusion-owned remediation instead of self-blocking at `stop-for-remediation`.