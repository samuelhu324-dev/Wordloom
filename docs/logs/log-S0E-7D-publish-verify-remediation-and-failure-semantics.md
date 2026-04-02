# log-S0E-7D (Phase 7D: publish, verify, remediation, and failure semantics)

---

**id**: `S0E-7D`
**kind**: `log`
**title**: `publish, verify, remediation, and failure semantics v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Drills, Evidence, epic/s0, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: ``
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

- `S0E-7D` has now completed `P0-P1` at the contract and taxonomy-mapping level.
- The first retained taxonomy artifact now fixes the ordered replay/backfill pipeline, the four handling semantics, and the strong-structure versus weak-structure family split for the current docs/GitHub workflow.
- The same artifact now maps the currently known issue/PR/log failure surfaces into default semantics rather than leaving operators to infer whether a given drift should block, replay, stay manual, or enter reconciliation.
- Recent `S0E-4F` and `S0E-7C` findings are now explicitly covered by that taxonomy, especially PR development linkage, deterministic labels, source-log write-back, parent relationships, exact DoD refs, Context prose drift, and source-block note contamination.

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

- [ ] `P2-C1-S1`: representative manifest retained across all four handling classes
- [ ] `P2-C1-S2`: structured audit summary retained

### P3 (Remediation contract)

- [ ] `P3-C1-S1`: replayable remediation/apply contract fixed
- [ ] `P3-C1-S2`: post-apply verify and incomplete-convergence stop rules fixed

### P4 (Future gate surface)

- [ ] `P4-C1-S1`: future publish/verify/remediation gate surface scoped and named

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1S2S3S4 / P1-C1-S1S2 (Failure taxonomy and mapping retained | 2026-04-02)

- headSha: `<pending-next-commit>`
- artifacts: `docs/issues/failure-semantics-S0E-7D-p0-p1-taxonomy.json`
- expected:
  - `S0E-7D` should retain one explicit taxonomy artifact covering strong-structure versus weak-structure families.
  - The same artifact should retain the ordered replay/backfill pipeline and default handling semantics.
  - Current issue/PR/log failure surfaces should be mapped to one default semantic instead of left implicit.
- observed:
  - `docs/issues/failure-semantics-S0E-7D-p0-p1-taxonomy.json` now records the ordered replay pipeline, four handling semantics, two structural families, and the current mapped surfaces.
  - The owner log now marks `P0-P1` complete and cites the retained taxonomy artifact as the first bounded evidence surface for this slice.

### <Pn-Cx-Sy> (<Drill name> | YYYY-MM-DD)

- headSha: `<git sha>`
- artifacts: `artifacts/_tmp_<...>/drills_<ts>.json`
- expected:
  - ...
- observed:
  - ...

## Recent changes (for traceability, optional)

- 2026-04-02: opened `S0E-7D` to separate failure taxonomy, replay/backfill order, and remediation semantics from the already-landed `S0E-7C` review planner and `S0E-4F` historical metadata backfill work.
- 2026-04-02: completed `P0-P1` by retaining the first structured failure taxonomy/mapping artifact for the current docs/GitHub workflow, covering strong versus weak structure, ordered replay/backfill, and default handling semantics per known failure surface.