# log-S0F-5A (Phase 5A: stable-first close-out protocol and post-stable outlet export)

---

**id**: `S0F-5A`
**kind**: `log`
**title**: `stable-first close-out protocol and post-stable outlet export v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Workflow, Closeout, Runbook, Contract, Views, epic/s0, sub/5a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
  **reference_log_1**: `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
  **reference_log_2**: `docs/logs/log-S0F-3H-recurring-governance-run-model-and-ledger-split.md`
  **reference_log_3**: `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
  **reference_log_4**: `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
**issue_keyword**: `governance`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/5`
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
**created**: `2026-04-08`
**updated**: `2026-04-08`

---

## Decision / Outcome

**Decision**:

- `S0F-5A` opens the next bounded follow-up after `S0F-4D` to fix one missing operating rule above the six-outlet model: when a slice should stay concentrated in its source log during draft iteration, and when it should export stable material into `contract`, `runbook`, `view`, `index/front-door`, and disposition write-backs.
- This slice exists because the repo already has:
  - one six-outlet role model in `S0F-4A`
  - one recurring-run packaging model in `S0F-3H`
  - one weak-structure compatibility boundary in `S0F-4B`
- But the repo still lacks one explicit `stable-first` close-out rule that answers three practical questions together:
  - why draft logs should usually not trigger broad outlet export too early
  - when a stable log should open a post-stable export step instead of carrying long-term mixed responsibility
  - when exporting nothing is the correct answer because no stable target outlet is justified yet

**Default choices (phase defaults / v1)**:

- Do not require every draft log to export six outlets while its boundary is still moving.
- Do not require every stable log to produce all six outlets mechanically.
- Treat `stable` as the normal decision gate for close-out review unless a narrower stable surface was already separated earlier by explicit bounded choice.
- Prefer one explicit post-stable export step or follow-up phase over many incremental draft-stage write-backs that churn multiple files repeatedly.
- Do not update the parent or phase-log templates from `P1` alone; template hardening should wait until the close-out questionnaire and export-packaging rules are explicit enough to avoid baking half-settled guidance into authoring scaffolds.
- A stable log should answer the full close-out questionnaire, but the result may legitimately be:
  - export one or two outlets only
  - rewrite only the log and one front door
  - or export nothing yet because the supposed target outlet still lacks stable identity

## Problem Statement

- `S0F-4A` already explains the six outlet roles and the export order.
- `S0F-3H` already explains why stable recurring procedure should move toward runbook or packet surfaces instead of staying in one ever-growing log.
- `S0F-4B` already protects the source-log family from being replaced by a premature outlet-first authoring format.
- The missing piece is a timing and trigger rule:
  - when should one slice stop iterating inside the draft source log and start exporting stable material?
  - should every stable slice open one fixed `Pn+1` style export pass?
  - how should the repo avoid both extremes:
    - premature runbook or view proliferation during draft churn
    - never-exported mixed-role logs that remain overloaded after the slice is already stable

## Scope

- `P0`: open `S0F-5A`, wire the new slice into the parent spine, and fix the problem as `stable-first close-out protocol` work rather than immediate contract promotion work
- `P1`: define the `stable-first` gate for outlet export, including when draft slices should stay concentrated in the source log
- `P2`: define the mandatory post-stable close-out questionnaire and the allowed answers when some outlets are intentionally no-op
- `P3`: define the default export packaging rule, including when a stable slice should use one bounded follow-up phase such as `Pn+1` rather than scattered draft-stage writes
- `P4`: define the no-proliferation rule for `runbook`, `view`, and other outlets so stable close-out does not become a mechanical file explosion
- `P5`: pilot the protocol on a recent stable governance lane and determine whether later `DOC` promotion slices such as a future `S0F-4E` should use this close-out pattern directly

## Success Criteria (DoD)

- One reader can explain why draft logs normally remain concentrated during active iteration.
- One reader can explain why `stable` is the normal gate for export review, not a signal that every possible outlet must now be created.
- One reader can explain when a stable slice should open one bounded post-stable export step instead of spreading write-backs across the draft period.
- One reader can explain why `runbook` extraction depends on stable repeated procedure rather than on the mere presence of operational prose inside a log.

## P0 (Scaffold | v1)

### P0-C1-S1 (Problem boundary fixed | v1)

- `S0F-5A` is now opened to fix `stable-first close-out protocol` as a repo operating rule.
- This slice does not yet promote `DOC-AREA-0001` bodies.
- That later promotion lane should follow after the close-out trigger and export discipline are explicit enough to avoid reopening timing and file-churn debates during the first real `DOC` promotion.

### P0-C1-S2 (Default sequencing fixed | v1)

- The current recommended sequence is now:
  - first finish `S0F-5A`
  - then open `S0F-4E` for the first real `DOC` promoted contract body
- This keeps the close-out trigger, export timing, and anti-proliferation rule ahead of the first real `DOC-...` contract extraction.

## P1 (Stable-first gate | v1)

### P1-C1-S1 (Draft-stage concentration rule fixed | v1)

- During active draft iteration, the source log remains the default concentration surface when any of the following is still moving materially:
  - the problem boundary or owned question
  - the current rule or successor rule text
  - the stable operator sequence
  - the reader-facing summary shape
  - the front-door mutation or placement consequence
- Under this rule, draft slices should usually avoid broad outlet export because repeated multi-file write-backs during active boundary churn create unstable `runbook`, `view`, or `contract` surfaces too early.
- Early export is allowed only when a narrower stable surface is already explicit and bounded enough that later draft changes will not repeatedly reopen that outlet.

### P1-C1-S2 (Stable-entry close-out gate fixed | v1)

- A slice enters formal close-out review when both of these become true:
  - its primary semantic or operational question is already converged enough that later work is mostly packaging, export, or bounded consequence handling rather than redefinition
  - one reader can explain the slice-local answer and the remaining next step without needing draft-only reconstruction across many scattered edits
- `stable` is therefore the normal export-review gate, not a command to emit every possible outlet.
- The required next action at that gate is: answer the close-out questionnaire explicitly and then decide whether the correct result is `export`, `partial export`, `log-only retention`, or `defer because target outlet identity is still not stable`.
- Template hardening is not part of this `P1` gate; it should follow later once the mandatory questionnaire and post-stable export packaging rules are fixed.

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

## Plan (draft)

### P1 (Stable-first gate)

- P1-C1-S1: define when draft slices should remain concentrated in the source log
- P1-C1-S2: define when a stable slice enters formal close-out review

### P2 (Mandatory close-out questionnaire)

- P2-C1-S1: define the mandatory outlet questions a stable slice must answer
- P2-C1-S2: define allowed no-op answers when some outlets are intentionally not exported

### P3 (Post-stable export packaging)

- P3-C1-S1: define when one bounded `Pn+1` style export phase is preferred over repeated draft-stage multi-file write-backs
- P3-C1-S2: define the minimum write-back set and stop rule for that export phase

### P4 (Anti-proliferation rule)

- P4-C1-S1: define when `runbook` extraction is justified and when it is not
- P4-C1-S2: define when `view` or other summary surfaces are justified and when the retained log should remain the only reader surface
- P4-C1-S3: apply the converged close-out rule to the parent and phase-log templates only after `P1` through `P3` are explicit enough to freeze authoring guidance safely

### P5 (Pilot)

- P5-C1-S1: pilot the protocol on one recent stable governance lane
- P5-C1-S2: decide whether the first `DOC` promotion lane should use this close-out pattern directly

## Execution Checklist (unchecked)

### P0 (Scaffold)

- [x] `P0-C1-S1`: problem boundary fixed
- [x] `P0-C1-S2`: default sequencing fixed

### P1 (Stable-first gate)

- [x] `P1-C1-S1`: draft-stage concentration rule fixed
- [x] `P1-C1-S2`: stable-entry close-out gate fixed

### P2 (Mandatory close-out questionnaire)

- [ ] `P2-C1-S1`: mandatory outlet questions fixed
- [ ] `P2-C1-S2`: allowed no-op answers fixed

### P3 (Post-stable export packaging)

- [ ] `P3-C1-S1`: `Pn+1` style export packaging rule fixed
- [ ] `P3-C1-S2`: minimum write-back and stop rule fixed

### P4 (Anti-proliferation rule)

- [ ] `P4-C1-S1`: runbook extraction gate fixed
- [ ] `P4-C1-S2`: view and summary extraction gate fixed
- [ ] `P4-C1-S3`: template hardening gate fixed for parent and phase-log scaffolds

### P5 (Pilot)

- [ ] `P5-C1-S1`: one recent stable lane piloted
- [ ] `P5-C1-S2`: follow-up `DOC` promotion lane sequencing fixed

## Current Status

- `S0F-5A` is now opened as the next bounded follow-up after `S0F-4D`.
- `P0` is now complete: the problem is fixed as `stable-first close-out protocol` work rather than immediate `DOC` promotion work.
- `P1` is now complete: the repo now has one explicit draft-stage concentration rule and one explicit stable-entry close-out gate, so later outlet export can begin from a defended review boundary instead of from ongoing draft churn.
- Template hardening is intentionally deferred: the parent and phase-log templates should not be rewritten from `P1` alone, because they still need the later `P2` questionnaire and `P3` export-packaging rules before that guidance is safe to freeze into scaffolds.
- The next immediate step is now `P2`: define the mandatory close-out questionnaire and the allowed no-op answers for stable slices.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.

### P0-C1-S1 through P0-C1-S2 (stable-first close-out protocol slice opened | 2026-04-08)

- headSha: `e4fc27f13bb7a91aa0bdfe697bd757bb8da22953`
- artifacts: `docs/logs/log-S0F-5A-stable-first-close-out-protocol-and-post-stable-outlet-export.md`
- artifacts: `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - one reader should be able to explain why the next governance step is a close-out protocol slice rather than the first real `DOC` promotion body
- observed:
  - the repo now has one explicit next slice dedicated to `stable-first` close-out timing, anti-proliferation rules, and post-stable export sequencing before the first real `DOC` contract promotion lane opens

### P1-C1-S1 through P1-C1-S2 (stable-first gate fixed | 2026-04-08)

- headSha: `e4fc27f13bb7a91aa0bdfe697bd757bb8da22953`
- artifacts: `docs/logs/log-S0F-5A-stable-first-close-out-protocol-and-post-stable-outlet-export.md`
- artifacts: `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - one reader should be able to explain why draft slices usually stay concentrated in the source log and why `stable` is the normal gate for close-out review rather than a mechanical six-outlet export command
- observed:
  - the repo now has one explicit draft-stage concentration rule, one explicit stable-entry close-out gate, and one explicit deferral of template hardening until the later questionnaire and packaging rules are fixed

## Recent changes (for traceability, optional)

- 2026-04-08: opened `S0F-5A` to formalize stable-first close-out timing and post-stable outlet export before the first real `DOC` promoted contract body.
- 2026-04-08: completed `P1` by fixing the draft-stage concentration rule, the stable-entry close-out gate, and the decision to defer template hardening until later `P2/P3/P4` rules converge.