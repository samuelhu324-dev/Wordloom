# log-S0E-7D (Phase 7D: publish, verify, remediation, and failure semantics)

---

**id**: `S0E-7D`
**kind**: `log`
**title**: `publish, verify, remediation, and failure semantics v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Drills, Evidence, epic/s0, sub/1`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/341`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/352`
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
  **reference_log_1**: `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
  **reference_log_2**: `docs/logs/log-S0E-4F-pr-body-metadata-links-redundancy-follow-up.md`
  **reference_log_3**: `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  **reference_log_4**: `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: `road-002-projection-runtime-platformization-and-evidence-governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: `M5-P3`
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-02`
**updated**: `2026-04-02`

---

## Decision / Outcome

**Decision**:

- `S0E-7D` is the dedicated follow-up slice for making `publish -> verify -> remediation -> failure handling` semantics explicit across the current docs/GitHub automation family.
- v1 focuses on the contract first: failure classes, replay/backfill ownership, and apply-time decision semantics must be explicit before more automation is added.
- The same slice also owns the structural distinction between failures that must hard-block publish/apply and failures that may remain human-owned or reconciliation-only.

**Default choices (phase defaults / v1)**:

- Failure handling must be split into two layers rather than one flat bucket:
  - strong-structure failures: deterministic fields and live-contract surfaces that must stay fail-closed;
  - weak-structure failures: prose or human-authored surfaces that may remain warning/manual.
- Strong-structure failures include at least: labels, development linkage, parent relationship, source-log write-back, canonical body sections, and exact DoD PR refs.
- Weak-structure failures include at least: Context prose quality, summary wording, and other explicitly human-authored explanatory rows.
- Replay/backfill stays manifest-driven and ordered: `source log -> deterministic derive -> live audit -> remediation manifest -> apply -> post-apply verify`.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.
- `Evidence Footer Source` does not replace `Evidence`: the footer source feeds PR/gate automation, while `Evidence` remains the human ledger.

**PR summary bullets**:

- Define one explicit failure taxonomy for the current docs/GitHub automation path, split into strong-structure and weak-structure failure families.
- Fix one ordered replay/backfill contract so issue and PR remediation can be replayed through the same deterministic pipeline instead of ad hoc manual repair.
- Define the handling semantics for each failure class, including `block`, `replayable`, `manual`, and `reconciliation`.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.
- If later implementation work splits planner, apply, and gate ownership across multiple follow-up PRs, the generated PR should keep only the units explicitly selected by title scope.

**PR links**:

- Log: `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
- Runbook: ``
- Evidence artifact: ``

## Definitions (optional)

- `strong-structure failure`: a deterministic structured contract failure whose expected value can be derived mechanically and therefore must stay fail-closed.
- `weak-structure failure`: a bounded prose or human-authored quality failure that may remain warning/manual without invalidating the whole publish/apply pipeline.
- `replay`: rerunning deterministic derive plus bounded apply from an explicit manifest rather than repairing live state ad hoc.
- `backfill`: creating or repairing missing historical state so older issues/PRs converge to the current contract.
- `reconciliation`: a conflict state where live GitHub state and source-log intent disagree and automation must stop instead of overwriting one side blindly.
- `post-apply verify`: the final live audit pass run after mutation, used to confirm that the exact target set converged to the intended contract.

## Constraints

- Do not collapse all failures into one generic `fix later` bucket; operator action must depend on the failure family.
- Do not let weak-structure failures silently widen into strong-structure contract breaks.
- Do not let strong-structure failures proceed into publish/apply without an explicit blocking or replay path.
- Do not treat live GitHub state as the sole source of truth when the source log carries an explicit conflicting contract; that state must enter reconciliation instead.
- Do not allow replay/backfill order to vary per operator memory; the ordered manifest pipeline must stay explicit and auditable.

## Scope

- `P0`: define the failure taxonomy, replay/backfill order, and handling semantics contract
- `P1`: map current issue/PR/log failure surfaces into strong-structure versus weak-structure families
- `P2`: validate representative failure samples and retained audit outputs across all four handling classes
- `P3`: define the guarded remediation/apply contract and post-apply verify requirements
- `P4`: consolidate the same semantics into a future publish/verify/remediation gate entrypoint without widening beyond the current docs/GitHub workflow family

## Success Criteria (DoD)

- The repo has one explicit taxonomy that distinguishes strong-structure and weak-structure failures for the docs/GitHub automation path.
- The repo has one explicit ordered replay/backfill contract covering source-log derive, live audit, manifest planning, bounded apply, and post-apply verify.
- Each failure class is mapped to one handling semantic: `block`, `replayable`, `manual`, or `reconciliation`.
- Representative failures can be classified without relying on operator prose interpretation.
- The same semantics can explain the recent historical issue/PR backfill cases without ad hoc exceptions.
- Later follow-up slices can attach to this contract without redefining the same failure language again.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` have fixed the taxonomy, replay/backfill order, representative samples, and remediation semantics with retained evidence
  - the Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## Current Status

- `S0E-7D` has now completed `P0-P4` at the contract, representative-validation, remediation-semantics, and future-gate-surface level.
- The first retained taxonomy artifact now fixes the ordered replay/backfill pipeline, the four handling semantics, and the strong-structure versus weak-structure family split for the current docs/GitHub workflow.
- The same artifact now maps the currently known issue/PR/log failure surfaces into default semantics rather than leaving operators to infer whether a given drift should block, replay, stay manual, or enter reconciliation.
- Recent `S0E-4F` and `S0E-7C` findings are now explicitly covered by that taxonomy, especially PR development linkage, deterministic labels, source-log write-back, parent relationships, exact DoD refs, Context prose drift, and source-block note contamination.
- `P2` now retains one bounded representative manifest and one structured audit summary across all four handling semantics, so the repo no longer needs operator prose to explain how `block`, `replayable`, `manual`, and `reconciliation` differ in practice.
- `P3` now fixes the guarded remediation/apply contract: only replayable items may enter apply, mixed-semantics batches must split before mutation, and post-apply verify must stop incomplete convergence rather than looping with ad hoc live edits.
- `P4` now names the future gate surface itself as one explicit `publish-verify-remediation gate`, and fixes how it should delegate to the current pre-gate/adaptor family without flattening PR create, PR rewrite, relationship attach, conclusion apply, or historical backfill into one unsafe generic command.

## P0 (Contract | v1)

### P0-C1-S1 (Failure taxonomy fixed | v1)

- Failure handling is split into two structural layers:
  - strong-structure failures: deterministic, mechanically derivable contract breaks;
  - weak-structure failures: bounded prose or operator-authored quality drift.
- Strong-structure failures include at least:
  - labels;
  - development linkage;
  - parent relationship;
  - source-log write-back;
  - canonical issue/PR body sections;
  - exact DoD PR refs.
- Weak-structure failures include at least:
  - Context prose quality;
  - summary wording;
  - manual explanatory notes that remain outside deterministic contract surfaces.

### P0-C1-S2 (Replay / backfill order fixed | v1)

- Replay and backfill must follow one explicit ordered pipeline:
  - `source log -> deterministic derive -> live audit -> remediation manifest -> apply -> post-apply verify`.
- Both issue-side and PR-side remediation must be expressible through the same ordered manifest pipeline, even if they later use different apply entrypoints.
- If a repair cannot be represented through that ordered pipeline, it must be treated as manual or reconciliation rather than disguised as ordinary replay.

### P0-C1-S3 (Handling semantics fixed | v1)

- `block`: the failure must stop publish/apply immediately until the structured contract is corrected.
- `replayable`: the failure is mechanically repairable through deterministic derive plus bounded replay/apply.
- `manual`: the failure requires human confirmation or authoring and should remain explicit instead of being guessed.
- `reconciliation`: live state and source-log contract conflict, so automation must stop and surface the mismatch instead of overwriting either side blindly.

### P0-C1-S4 (Evidence contract | v1)

- Evidence JSON must include:
  - target object kind and identifiers (`log`, `issue`, `pr`, or mixed manifest item set);
  - expected deterministic values versus live observed values;
  - failure family (`strong-structure` / `weak-structure`) and handling semantic (`block` / `replayable` / `manual` / `reconciliation`);
  - downstream artifact paths for remediation manifest, apply result, and post-apply verify result when applicable.

## P1 (Taxonomy mapping | v1)

### P1-C1-S1 (Current failure surfaces split into structural families | v1)

- The current docs/GitHub workflow now distinguishes the following strong-structure surfaces as deterministic and fail-closed by default:
  - PR labels;
  - PR development linkage;
  - issue parent relationship;
  - source-log write-back;
  - canonical issue/PR body sections;
  - exact DoD PR refs;
  - explicit live-versus-source conflicts.
- The current workflow now distinguishes the following weak-structure surfaces as bounded but still human-owned:
  - issue `Context` prose quality;
  - issue/PR summary wording;
  - explanatory notes outside canonical source blocks.

### P1-C1-S2 (Default handling semantics mapped per family | v1)

- Default semantics are now fixed per known failure surface rather than guessed ad hoc:
  - `block`: canonical body section failures;
  - `replayable`: PR labels, PR development linkage, issue parent relationship, source-log write-back, and exact DoD PR refs;
  - `manual`: `Context` prose, summary wording, and freeform explanatory notes;
  - `reconciliation`: explicit live-versus-source conflicts such as mismatched write-back references or incompatible live relationships.
- This mapping does not prevent future follow-up slices from refining a surface's semantics, but v1 now fixes the default decision path that operators and later automation should follow.

## P2 (Representative validation | v1)

### P2-C1-S1 (Representative manifest retained across all four handling classes | v1)

- The retained representative manifest now carries one bounded sample for each handling semantic:
  - `block`: canonical PR body section drift;
  - `replayable`: PR development linkage / deterministic label backfill;
  - `manual`: issue `Context` prose quality drift;
  - `reconciliation`: explicit live-versus-source reference conflict.
- Each sample now records the target kind, source owner surface, expected versus observed values, semantic classification, next action, and retained evidence paths.
- The representative set is intentionally mixed so the later audit summary can prove that only the replayable subset is eligible for remediation-manifest planning.

### P2-C1-S2 (Structured audit summary retained | v1)

- The retained audit summary now normalizes the same four representative samples into one machine-readable gate summary.
- The summary explicitly records:
  - family counts;
  - semantic counts;
  - the mixed-stop overall gate outcome;
  - the exact subset that may proceed into remediation-manifest planning.
- This keeps `P2` as validation rather than mutation: the output proves classification and stop/split behavior before any replay/apply step begins.

## P3 (Remediation contract | v1)

### P3-C1-S1 (Replayable remediation/apply contract fixed | v1)

- Replay/apply is now explicitly restricted to items already classified as `replayable`.
- A remediation manifest row must carry exact target identity, source-log ownership, surface name, family/semantic classification, expected versus observed values, and explicit downstream apply/verify artifact paths.
- Mixed batches must split before mutation:
  - `block` findings must stop and return to contract correction;
  - `manual` findings must remain human-authored;
  - `reconciliation` findings must stop for operator resolution.

### P3-C1-S2 (Post-apply verify and incomplete-convergence stop rules fixed | v1)

- Post-apply verify must re-fetch the same targets mutated by apply and compare them against the same expected deterministic values used during planning.
- Verify must stop the cycle, not silently retry live edits, when any of the following occurs:
  - incomplete convergence;
  - new deterministic drift introduced by apply;
  - missing or inconsistent apply/verify evidence.
- Any such stop result must open a new bounded audit/remediation cycle instead of being folded into the original apply attempt.

## P4 (Future gate surface | v1)

### P4-C1-S1 (Future publish/verify/remediation gate surface scoped and named | v1)

- The future unified surface is now explicitly named `publish-verify-remediation gate`.
- Its first implementation target is one thin orchestration entrypoint that normalizes:
  - input kinds;
  - decision vocabulary;
  - remediation artifact emission;
  - apply delegation;
  - post-apply verify outcomes.
- v1 keeps this surface narrow by reusing the current mutation-family adapters instead of replacing them:
  - issue conclusion stays behind `apply_issue_conclusion_with_pre_gate.py`;
  - relationship attach stays behind `apply_issue_relationships_with_pre_gate.py`;
  - PR body rewrite stays behind `apply_pr_body_scope_with_pre_gate.py`;
  - PR create remains front-half preflight only through `plan_pr_create_preflight_with_gate.py`.
- The new surface therefore consolidates naming and orchestration, not mutation semantics: it must not collapse branch materialization, remote publish, live PR publish, prose QA, or GitHub Actions secondary enforcement into one flat gate decision.

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

- `S0E-7D` changes should normally accumulate on the active `S0E-*` docs-management branch so the spine and child slice remain traceable together.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, commit/push promptly on the matching scope branch so later replay semantics can cite exact IDs and head SHAs.

## Plan (draft)

### P1 (Taxonomy mapping)

- `P1-C1-S1`: enumerate the current docs/GitHub automation failure surfaces and split them into strong-structure versus weak-structure families
- `P1-C1-S2`: map each family to the first default handling semantic (`block`, `replayable`, `manual`, `reconciliation`)

### P2 (Representative validation)

- `P2-C1-S1`: retain a representative manifest covering all four handling classes
- `P2-C1-S2`: retain one structured audit summary showing the chosen failure family plus handling semantic per sample

### P3 (Remediation contract)

- `P3-C1-S1`: define the guarded remediation/apply contract for replayable failures
- `P3-C1-S2`: define the post-apply verify contract and stop conditions for incomplete convergence

### P4 (Future gate surface)

- `P4-C1-S1`: define how the same taxonomy and semantics should surface in a future publish/verify/remediation gate entrypoint without widening beyond the current workflow family

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: failure taxonomy fixed
- [x] `P0-C1-S2`: replay / backfill order fixed
- [x] `P0-C1-S3`: handling semantics fixed
- [x] `P0-C1-S4`: evidence contract fixed

### P1 (Taxonomy mapping)

- [x] `P1-C1-S1`: failure surfaces split into strong-structure versus weak-structure families
- [x] `P1-C1-S2`: default handling semantic mapped per failure family

### P2 (Representative validation)

- [x] `P2-C1-S1`: representative manifest retained across all four handling classes
- [x] `P2-C1-S2`: structured audit summary retained

### P3 (Remediation contract)

- [x] `P3-C1-S1`: replayable remediation/apply contract fixed
- [x] `P3-C1-S2`: post-apply verify and incomplete-convergence stop rules fixed

### P4 (Future gate surface)

- [x] `P4-C1-S1`: future publish/verify/remediation gate surface scoped and named

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1S2S3S4 / P1-C1-S1S2 (Failure taxonomy and mapping retained | 2026-04-02)

- headSha: `d25b1991`
- artifacts: `docs/issues/failure-semantics-S0E-7D-p0-p1-taxonomy.json`
- expected:
  - `S0E-7D` should retain one explicit taxonomy artifact covering strong-structure versus weak-structure families.
  - The same artifact should retain the ordered replay/backfill pipeline and default handling semantics.
  - Current issue/PR/log failure surfaces should be mapped to one default semantic instead of left implicit.
- observed:
  - `docs/issues/failure-semantics-S0E-7D-p0-p1-taxonomy.json` now records the ordered replay pipeline, four handling semantics, two structural families, and the current mapped surfaces.
  - The owner log now marks `P0-P1` complete and cites the retained taxonomy artifact as the first bounded evidence surface for this slice.

### P2-C1-S1S2 (Representative failure samples and audit summary retained | 2026-04-02)

- headSha: `51210152`
- artifacts:
  - `docs/issues/failure-semantics-S0E-7D-p2-c1-representative-manifest.json`
  - `docs/issues/failure-semantics-S0E-7D-p2-c1-audit-summary.json`
- expected:
  - `S0E-7D` should retain one bounded representative sample for each handling semantic.
  - The same retained audit output should prove that only replayable samples may continue into remediation-manifest planning.
- observed:
  - `docs/issues/failure-semantics-S0E-7D-p2-c1-representative-manifest.json` now records one sample each for `block`, `replayable`, `manual`, and `reconciliation`.
  - `docs/issues/failure-semantics-S0E-7D-p2-c1-audit-summary.json` now records a mixed-stop gate outcome and the exact replayable subset eligible for the next stage.

### P3-C1-S1S2 (Remediation/apply and post-apply verify contract retained | 2026-04-02)

- headSha: `51210152`
- artifacts: `docs/issues/failure-semantics-S0E-7D-p3-c1-remediation-and-verify-contract.json`
- expected:
  - `S0E-7D` should fix one guarded replay/apply contract that only admits replayable findings.
  - The same contract should retain explicit stop rules for mixed-semantics batches and incomplete post-apply convergence.
- observed:
  - `docs/issues/failure-semantics-S0E-7D-p3-c1-remediation-and-verify-contract.json` now fixes stage-by-stage entry conditions, manifest row requirements, allowed/forbidden apply targets, and post-apply verify stop rules.
  - The owner log now marks `P3` complete and leaves gate-surface consolidation as the final open phase for this slice.

### P4-C1-S1 (Future gate surface scoped and named | 2026-04-02)

- headSha: `53bd8fa3`
- artifacts: `docs/issues/failure-semantics-S0E-7D-p4-c1-gate-surface.json`
- expected:
  - `S0E-7D` should fix one explicit future gate name and one narrow orchestration surface for the current docs/GitHub workflow family.
  - The same artifact should say which existing pre-gate adapters are reused and which boundaries remain out of scope.
- observed:
  - `docs/issues/failure-semantics-S0E-7D-p4-c1-gate-surface.json` now names the unified surface as `publish-verify-remediation gate`, fixes its decision vocabulary, and records how it delegates to the existing issue/relationship/PR/body/create pre-gate adapters.
  - The same artifact now explicitly excludes prose QA, generic blank-field inference, branch materialization, remote publish, live PR publish, and GitHub Actions secondary enforcement from the v1 gate surface.

### <Pn-Cx-Sy> (<Drill name> | YYYY-MM-DD)

- headSha: `<git sha>`
- artifacts: `artifacts/_tmp_<...>/drills_<ts>.json`
- expected:
  - ...
- observed:
  - ...

## Recent changes (for traceability, optional)

- 2026-04-03: wrote back live issue `#341`, remediated the required sidebar parent relationship, created and merged PR `#352`, applied the final issue-conclusion body, and confirmed the live issue is closed.
- 2026-04-02: opened `S0E-7D` to separate failure taxonomy, replay/backfill order, and remediation semantics from the already-landed `S0E-7C` review planner and `S0E-4F` historical metadata backfill work.
- 2026-04-02: completed `P0-P1` by retaining the first structured failure taxonomy/mapping artifact for the current docs/GitHub workflow, covering strong versus weak structure, ordered replay/backfill, and default handling semantics per known failure surface.
- 2026-04-02: completed `P2` by retaining one representative manifest and one structured audit summary across `block`, `replayable`, `manual`, and `reconciliation`, making the stop/split behavior explicit before apply.
- 2026-04-02: completed `P3` by fixing the guarded replay/apply contract, explicit manifest-row requirements, and post-apply verify stop rules for incomplete convergence.
- 2026-04-02: completed `P4` by naming the future `publish-verify-remediation gate`, fixing its decision vocabulary and reuse boundaries, and constraining it to orchestration rather than generic mutation flattening.