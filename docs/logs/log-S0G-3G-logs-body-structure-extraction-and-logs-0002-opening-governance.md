# log-S0G-3G (Phase 3G: logs body-structure extraction and LOGS-0002 opening governance)

---

**id**: `S0G-3G`
**kind**: `log`
**title**: `logs body-structure extraction and LOGS-0002 release-opening governance v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Contract, Evidence, epic/s0, sub/3g`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-5A-time-semantics-and-effective-window-governance.md`
  **reference_log_1**: `docs/logs/log-S0C-1A-log-extensions.md`
  **reference_log_2**: `docs/logs/log-S0G-1B-legacy-logs-historical-backfill-and-logs-family-bridge-governance.md`
  **reference_log_3**: `docs/governance/contracts/workflow/logs/DOC-WORKFLOW-LOGS-0001-structured-log-identity-and-front-matter.md`
  **reference_log_4**: `docs/logs/_template-log-phase-drills-evidence.md`
  **reference_log_5**: `docs/logs/support-only/ledger-S0C-1A-log-extensions.md`
  **reference_log_6**: `docs/governance/contracts/workflow/logs/DOC-WORKFLOW-LOGS-0002-body-structure-and-reader-facing-log-shape.md`
  **reference_log_7**: `docs/governance/contracts/workflow/logs/register-DOC-WORKFLOW-LOGS.md`
  **reference_log_8**: `docs/logs/log-S0C-2A-legacy-integration-suite-retired.md`
  **reference_log_9**: `docs/logs/support-only/ledger-S0C-2A-legacy-integration-suite-retired.md`
  **reference_log_10**: `docs/governance/contracts/workflow/lifecycle/DOC-WORKFLOW-LIFECYCLE-0001-legacy-taxonomy-cutover-and-stub-preservation.md`
  **reference_log_11**: `docs/governance/contracts/workflow/lifecycle/DOC-WORKFLOW-LIFECYCLE-0002-continuity-test-retirement-and-replacement-coverage.md`
  **reference_log_12**: `docs/governance/contracts/workflow/lifecycle/register-DOC-WORKFLOW-LIFECYCLE.md`
**issue_keyword**: `contract`
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
**created**: `2026-04-23`
**updated**: `2026-04-24`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are artifact-lifecycle fields only.
- This lane may later backfill contract semantic-effective dates, but those dates must remain on contract surfaces rather than being widened into this log frontmatter.
- `reviewed` stays `pending` until the repo has enough repeated post-cutover log samples to decide whether the `DOC-WORKFLOW-LOGS` family should advance from `0001` to `0002`.

## Decision / Outcome

**Decision**:

- `S0G-3G` opens the bounded lane for extracting repeated log body-structure rules from structured logs and deciding whether those rules justify `DOC-WORKFLOW-LOGS-0002` as the next release in the same `DOC-WORKFLOW-LOGS` family.
- This lane uses `log -> source-owned support-only ledger (or + SUP if later evidence sharpening becomes necessary) -> contract release -> conditional register writeback` as the operating chain: source logs remain the extraction surface, each extracted source gets its own ledger named after the source id, and contract mutation is deferred until repeated evidence makes the next release defensible.
- Later log samples should enter this lane as new `C` items by default; do not open a new sibling source log every time one more sample is added unless the new sample clearly opens a materially different source-log extraction problem.
- `P2-C1` is now completed for the first sample only: `S0C-1A` is clustered into provisional `candidate LOGS-0002 clauses`, `candidate LOGS-0001 boundary amendments`, and `support-only` material, with the explicit current verdict `no-contract-mutation-for-now` until corroborating evidence exists.
- `P3-C1-S1` now fixes the direct-opening verdict as positive and emits `DOC-WORKFLOW-LOGS-0002` plus `register-DOC-WORKFLOW-LOGS.md`, so the family now has one explicit current-primary release and one historical-retained earlier release.
- `P1-C2-S1` now admits `S0C-2A` as one negative-control sample after the `0002` opening: it is structured enough to extract cleanly, but its retirement and replacement-coverage rules do not contribute reusable logs body-structure meaning, so the verdict is `no logs-family impact now`.
- `P3-C2-S1` now fixes the downstream non-logs verdict as positive: `S0C-2A` still has no logs-family impact, but its reusable retirement rows are strong enough to open `DOC-WORKFLOW-LIFECYCLE-0002` as one later integrated lifecycle release, with `DOC-WORKFLOW-LIFECYCLE-0001` retained as the earlier narrower release.

**Default choices (phase defaults / v1)**:

- `DOC-WORKFLOW-LOGS-0002` is now the current logs-family release: it carries forward stable identifier and cutover-intake meaning from `0001`, amends the frontmatter/body boundary, and introduces explicit body-structure governance from `S0C-1A`.
- The first concrete sample under this lane is `S0C-1A`, because it states a reusable `Decision / Outcome` block and `single top-level status field` rule clearly enough to test whether body-structure ownership is becoming stable across modern logs.
- New samples should first open or update one source-owned ledger named after the extracted source id before any contract text is drafted or revised.
- A sample that shows only local stylistic preference should remain ledger evidence and should not trigger contract mutation by itself.
- A well-structured sample may still remain out of family if its extracted rows govern some other boundary, such as testing retirement, lifecycle, or repo-local operator practice rather than reader-facing structured-log body shape.
- An out-of-family sample that does not mutate `DOC-WORKFLOW-LOGS` may still trigger one downstream non-logs release if the packet yields current-reader-worthy clauses strong enough for another existing family.
- Do not use the old `six outlets` model as the extraction driver for this lane; borrow only its ownership-separation discipline where useful, and do any later close-out/export review only after the release boundary is fixed.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- This lane is expected to drive a later contract-opening packet, so the summary surface should stay focused on boundary evidence and repeatability rather than replaying each sample verbatim.

**PR summary bullets**:

- Extract repeated body-structure rules from post-cutover structured logs instead of patching `LOGS-0001` ad hoc from one sample at a time.
- Record sample-by-sample rule rows in one dedicated parent ledger before deciding whether `DOC-WORKFLOW-LOGS-0002` should open.
- Keep future samples inside `S0G-3G` as new cycles by default so the lane can accumulate evidence without proliferating sibling source logs.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0G-3G-logs-body-structure-extraction-and-logs-0002-opening-governance.md`
- Runbook: ``
- Evidence artifact: `docs/logs/support-only/ledger-S0C-1A-log-extensions.md`

**Evidence Footer Source**:

- `P1-C1-S1` | artifact: `docs/logs/log-S0C-1A-log-extensions.md`
- `P2-C1-S1` | artifact: `docs/logs/support-only/ledger-S0C-1A-log-extensions.md`

## Definitions

- **body-structure rule**: one reusable rule about how a structured log organizes its reader-facing body, such as mandatory conclusion blocks, section ordering, or status ownership.
- **sample cycle**: one bounded pass that extracts rules from one additional source log and writes the result into the parent ledger.
- **source-owned ledger**: the support-only ledger named after the extracted source id that records routed slices, chronology audit, and later consumption tracking for one source sample.
- **contract release decision**: the explicit verdict on whether repeated ledger evidence is strong enough to open `DOC-WORKFLOW-LOGS-0002` as the next same-family release or whether the evidence should remain below contract level.

## Constraints

- Do not widen `DOC-WORKFLOW-LOGS-0001` simply because one sample looks persuasive.
- Do not treat `Decision / Outcome` as automatically contract-worthy without one explicit lane verdict that direct family opening is preferable to waiting for additional corroborating samples.
- Do not skip the parent-ledger write-back when a new sample is reviewed.
- Do not split this lane into sibling logs for every new sample unless the source-log extraction problem itself changes materially.

## Optional Required Processing Chain

| chain step | required state | primary owner surface | trigger question | completion evidence | notes |
| --- | --- | --- | --- | --- | --- |
| `source extraction` | `required` | `S0G-3G` | `Has one bounded source log been selected tightly enough for rule extraction?` | `sample-specific extraction note or retained source anchor` | `Entry step for each new cycle` |
| `SUP` | `not-required` | `n/a` | `Is this lane sharpening one already-admitted row with later evidence only?` | `explicit no-SUP verdict` | `Default path is direct extraction plus parent ledger write-back` |
| `parent ledger` | `required` | `source-owned support-only ledger for the extracted sample` | `Does the extracted sample add or sharpen one candidate body-structure rule row?` | `ledger rows added or updated in the sample-owned ledger` | `This is the mandatory accumulation layer before contract mutation` |
| `contract impact decision` | `required` | `S0G-3G` | `Does the cross-sample evidence justify no-op, `LOGS-0001` note-only reconciliation, or opening `LOGS-0002` as the next same-family release?` | `explicit classified verdict in log plus ledger` | `Boundary gate before downstream mutation` |
| `contract mutation` | `conditional` | `DOC-WORKFLOW-LOGS-*`, downstream non-logs family, or `n/a` | `Has the reviewed packet made one same-family logs release or one downstream non-logs release boundary defensible?` | `new release draft or explicit no-contract-mutation verdict` | `Default remains no mutation until one defended family-level reader change exists` |
| `transition register update` | `conditional` | `register-DOC-WORKFLOW-LOGS.md`, one downstream family register, or `n/a` | `Would the decision change which release is first-open now or how an earlier release remains reader-relevant in the affected family?` | `register row or explicit no-register-change verdict` | `Needed whenever family-level release standing changes in either the logs family or one downstream family` |
| `bridged contract reconciliation` | `conditional` | `affected family contracts` | `Do current readers need redirect or release-bridge notes after the decision?` | `bridge note or explicit no-bridge-impact verdict` | `Keep the affected family releases coherent without forcing all downstream routing back into the logs family` |

## Scope

- `P0`: contract boundary for `LOGS-0001` versus next-release `LOGS-0002`, plus the multi-sample lane rule
- `P1`: sample-by-sample extraction cycles from source logs into the dedicated parent ledger
- `P2`: cross-sample clustering, repeatability verdicts, and family-boundary testing
- `P3`: contract opening decision and first downstream write-back only if justified, including one defended non-logs family write-back when the sample is out of family for logs but current-reader-worthy elsewhere

## Success Criteria (DoD)

- The lane states one explicit rule for when a new sample stays inside `S0G-3G` as a new cycle instead of opening a sibling log.
- A source-owned ledger exists for each extracted sample and is the mandatory accumulation surface for extracted sample rules.
- `S0C-1A` is fixed as the first concrete sample under this lane.
- The lane records one explicit boundary test for `LOGS-0001` versus next-release `LOGS-0002`.
- The lane records one explicit downstream decision path: `no-op`, `LOGS-0001` note-only reconciliation, or `LOGS-0002` opening.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the sample-ingestion rule is explicit;
  - the parent-ledger accumulation model is explicit;
  - the next-release test for `LOGS-0002` is explicit;
  - the next downstream mutation rule is explicit.
- `stable` for this lane does not require `LOGS-0002` to exist yet; it requires the repo to know how new samples are admitted and how the contract decision will be made.

## P0 (Contract | v1)

### P0-C1-S1 (LOGS-0001 versus next-release LOGS-0002 boundary fixed | v1)

- `LOGS-0001` remains the current first release owner of log identity, front matter, and cutover intake.
- Candidate body-structure rules such as `Decision / Outcome`, body section ordering, or `single top-level status ownership` should be tested here for a possible next release `LOGS-0002` in the same family rather than patched into `LOGS-0001` one sample at a time.

### P0-C1-S2 (Multi-sample lane rule fixed | v1)

- New samples should normally enter `S0G-3G` as new cycles under the same lane.
- Open a new sibling source log only if later samples prove a materially different source-log extraction problem than `logs body structure` itself.

### P0-C1-S3 (Evidence contract fixed | v1)

- Each admitted sample must write at least one parent-ledger row that records:
  - the source log path and sample identifier
  - the extracted candidate rule
  - the repeatability verdict
  - the contract impact verdict for `LOGS-0001` vs `LOGS-0002`
  - the next write-back target
  - and that row set should live in a support-only ledger named after the extracted source id rather than the control-lane id

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0G-3G/P<phase>-C<cycle>-S<steps>: <summary>`

**Branch convention**:

- This lane should stay on `S0G-docs-management-v7` while it remains one bounded follow-up inside the current `S0G` docs-management spine.

**Commit discipline (recommended)**:

- Keep the scaffold, each new sample cycle, the ledger clustering pass, and any later contract opening decision in separate commits when practical.

## Plan (draft)

### P1 (Sample extraction cycles)

- `P1-C1-S1`: extract the first candidate body-structure rule set from `S0C-1A`
- `P1-C1-S2`: write the corresponding row(s) into the `S0C-1A` source-owned ledger
- `P1-C2-S1`: reserve the next cycle for one additional post-cutover log sample without opening a sibling source log by default

### P1-C2-S1 (S0C-2A admitted as one structured negative-control sample | v1)

- `S0C-2A` is now admitted as the second sample cycle under `S0G-3G`, but only as one boundary-check sample after `DOC-WORKFLOW-LOGS-0002` already exists.
- The sample is useful because it now exposes a clean extraction surface and therefore tests the lane's family boundary, not just the source-log formatting discipline.
- Extracted rows from `S0C-2A` govern legacy-suite retirement, explicit skip messaging, replacement coverage, and retained pytest evidence.
- The explicit verdict is `no logs-family impact now`: none of those rows amend `DOC-WORKFLOW-LOGS-0002`, reopen `DOC-WORKFLOW-LOGS-0001`, or change `register-DOC-WORKFLOW-LOGS.md`.
- The sample therefore remains one negative-control packet for the logs family: it proves that `well-structured source` is necessary for extraction but not sufficient for logs-family admission.

### P3-C2-S1 (S0C-2A routed into the later integrated lifecycle release | v1)

- `S0C-2A` remains out of the logs family, but its reusable retirement and replacement-coverage rows are now admitted into `DOC-WORKFLOW-LIFECYCLE-0002` as one later integrated lifecycle release.
- `DOC-WORKFLOW-LIFECYCLE-0002` carries forward the earlier continuity, freeze, migration, cutover, and stub-preservation clauses from `DOC-WORKFLOW-LIFECYCLE-0001`, amends the family boundary clause, and introduces explicit retirement, traceability, and replacement-coverage clauses from `S0C-2A`.
- `register-DOC-WORKFLOW-LIFECYCLE.md` now records that `DOC-WORKFLOW-LIFECYCLE-0002` is current-primary and `DOC-WORKFLOW-LIFECYCLE-0001` remains historical-retained as the earlier narrower release.
- `S0C-2A-R04` remains retained support-only evidence; reproducible pytest counts are not admitted into primary lifecycle contract text.
- Later split is allowed if repeated evidence makes test-retirement lifecycle independently judgeable from the broader integrated lifecycle reader.

### P2 (Boundary test)

- `P2-C1-S1`: cluster the admitted sample rows into provisional rule buckets
- `P2-C1-S2`: decide whether the current evidence supports `no-op`, `LOGS-0001` note-only reconciliation, or `LOGS-0002` as the next same-family release

### P2-C1-S1 (S0C-1A provisional rule buckets fixed | v1)

- The first admitted sample now yields one explicit provisional split rather than one undifferentiated `LOGS-0002` candidate blob.
- Provisional `candidate LOGS-0002 clause` bucket:
  - `S0C-1A-R01`: top-level `Decision / Outcome` conclusion surface
  - `S0C-1A-R02`: minimum conclusion fields
  - `S0C-1A-R04`: current-effective body-content discipline
- Provisional `candidate LOGS-0001 boundary amendment` bucket:
  - `S0C-1A-R03`: top-level frontmatter `status` ownership versus per-section lifecycle repetition in the body
- Provisional `support-only` bucket:
  - `S0C-1A-R05`: applied examples and copyable template snippets
- This split is intentionally provisional because it is still based on one sample only.

### P2-C1-S2 (First-sample contract impact verdict fixed explicitly | v1)

- The current explicit verdict is `no-contract-mutation-for-now`.
- `LOGS-0001` should not be patched immediately from `S0C-1A`, because the body-structure material is still first-sample evidence rather than repeated family evidence.
- `LOGS-0002` should not be scaffolded yet, because the current candidate rows have not been corroborated by one second post-cutover sample.
- `LOGS-0001 note-only reconciliation` is also deferred for now: the boundary interaction is now understood, but the repo does not yet need one live note-only patch on `0001` before the second sample clarifies which rows are truly stable family meaning.
- Under this rule, `S0C-1A` is now a completed first-sample packet: extraction plus provisional clustering plus explicit no-mutation verdict are fixed, and the next lane action returns to sample selection rather than reopening this sample's boundary test.

### P3 (Downstream write-back)

- `P3-C1-S1`: if the boundary test passes, scaffold the downstream `LOGS-0002` release-opening packet and any required bridge notes
- `P3-C2-S1`: if one out-of-family packet is still current-reader-worthy elsewhere, scaffold the downstream non-logs release-opening packet and any required family register notes

### P3-C1-S1 (DOC-WORKFLOW-LOGS-0002 and family register emitted | v1)

- The direct-opening verdict is now positive: `S0C-1A` is sufficient to open `DOC-WORKFLOW-LOGS-0002` as the next same-family release.
- The emitted release lives at `docs/governance/contracts/workflow/logs/DOC-WORKFLOW-LOGS-0002-body-structure-and-reader-facing-log-shape.md`.
- The release keeps the active logs-family reader coherent in three layers:
  - `carried-forward`: stable identifier, visible identity, and cutover intake remain active family meaning from `0001`
  - `amended`: frontmatter/body boundary clauses are restated so top-level status ownership becomes explicit
  - `introduced`: conclusion-block and current-effective-body clauses are admitted from `S0C-1A`
- The family transition register now also opens at `docs/governance/contracts/workflow/logs/register-DOC-WORKFLOW-LOGS.md` because `0002` becomes the current-primary reader while `0001` remains historical-retained.
- `S0C-1A-R05` remains support-only; template snippets and applied examples are not admitted into primary release-local contract meaning in this opening round.

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: `LOGS-0001` versus next-release `LOGS-0002` boundary fixed
- [x] `P0-C1-S2`: multi-sample lane rule fixed
- [x] `P0-C1-S3`: evidence contract fixed

### P1 (Sample extraction cycles)

- [x] `P1-C1-S1`: first concrete sample fixed as `S0C-1A`
- [x] `P1-C1-S2`: parent-ledger landing surface fixed
- [x] `P1-C1-S1S2`: `S0C-1A` extracted into explicit candidate rule rows in the parent ledger
- [x] `P1-C2-S1`: next sample cycle admitted after `S0C-1A`

### P2 (Boundary test)

- [x] `P2-C1-S1`: admitted sample rows clustered into provisional rule buckets
- [x] `P2-C1-S2`: contract impact verdict fixed explicitly

### P3 (Downstream write-back)

- [x] `P3-C1-S1`: downstream `LOGS-0002` opening packet scaffolded and family register write-back completed
- [x] `P3-C2-S1`: downstream lifecycle release-opening packet scaffolded and family register write-back completed for `S0C-2A`

## Current Status

- `S0G-3G` is now scaffolded as the bounded source-log lane for testing whether repeated modern log body-structure evidence warrants `LOGS-0002` as the next release in the same `DOC-WORKFLOW-LOGS` family.
- `S0C-1A` is now fixed as the first extracted sample: its candidate rule set has been split into conclusion-block, minimum-field, top-level-status, current-effective-body, and supporting-evidence rows inside the source-owned ledger `ledger-S0C-1A-log-extensions.md`.
- `P2-C1` is now fixed for that first sample: `R01`, `R02`, and `R04` sit in the provisional `LOGS-0002` bucket, `R03` sits in the provisional `LOGS-0001 boundary amendment` bucket, and `R05` remains support-only.
- `P3-C1-S1` is now completed: `DOC-WORKFLOW-LOGS-0002` is emitted as the current-primary logs-family release, `DOC-WORKFLOW-LOGS-0001` is retained as the earlier narrower release, and the family register now records that standing explicitly.
- `S0C-2A` is now admitted as the second sample cycle and still resolves as one negative-control packet for the logs family: its extracted rules are about test retirement and replacement coverage rather than reader-facing log body structure, so the lane records `no logs-family impact now` explicitly for `DOC-WORKFLOW-LOGS`.
- `P3-C2-S1` is now also completed: the same packet is routed onward into `DOC-WORKFLOW-LIFECYCLE-0002`, `DOC-WORKFLOW-LIFECYCLE-0001` is retained as the earlier narrower release, and the lifecycle family register now records that standing explicitly.
- The next concrete step is optional post-opening sampling to decide whether the current logs-family or lifecycle-family `0002` releases should later be sharpened, amended, superseded, or split, ideally from one stronger repeated source set rather than from another single adjacent packet.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the governing sample paths, ledger path, and later boundary-decision artifacts.

### P1-C1-S1S2 (S0C-1A selected as first sample and parent-ledger landing fixed | 2026-04-23)

- headSha: `WORKTREE`
- artifacts:
  - `docs/logs/log-S0C-1A-log-extensions.md`
  - `docs/logs/support-only/ledger-S0C-1A-log-extensions.md`
- expected:
  - the lane should start from one concrete modern log sample rather than from abstract body-structure discussion only
  - the ledger landing surface should be fixed before any contract drafting starts
- observed:
  - `S0C-1A` is now the first admitted sample target for this lane
  - the source-owned `S0C-1A` support-only ledger path is now fixed as the accumulation surface for extracted rule rows

### P1-C1-S1S2 (S0C-1A extracted into explicit candidate rows | 2026-04-23)

- headSha: `WORKTREE`
- artifacts:
  - `docs/logs/log-S0C-1A-log-extensions.md`
  - `docs/logs/support-only/ledger-S0C-1A-log-extensions.md`
- expected:
  - the first sample should stop reading as one vague `LOGS-0002` candidate and instead resolve into specific candidate rule rows
  - the ledger should distinguish likely contract clauses from evidence/support-only pattern material
- observed:
  - `S0C-1A` now yields four primary candidate rows: top-level conclusion block, minimum conclusion fields, top-level status ownership, and current-effective body discipline
  - the sample's applied examples and copyable template snippet are now recorded as supporting evidence rather than primary contract meaning
  - all extracted rows remain `first-sample-only`, so `LOGS-0002` still requires corroborating samples before release opening is justified

### P2-C1-S1S2 (S0C-1A provisional split and no-mutation verdict fixed | 2026-04-24)

- headSha: ``
- artifacts:
  - `docs/logs/log-S0G-3G-logs-body-structure-extraction-and-logs-0002-opening-governance.md`
  - `docs/logs/support-only/ledger-S0C-1A-log-extensions.md`
  - `docs/governance/contracts/workflow/logs/DOC-WORKFLOW-LOGS-0001-structured-log-identity-and-front-matter.md`
- expected:
  - cluster the first sample rows into explicit provisional buckets instead of leaving them as one generic `LOGS-0002` candidate set
  - record whether the current evidence supports immediate `LOGS-0001` reconciliation, immediate `LOGS-0002`, or neither
  - close the first-sample packet without pretending that corroboration already exists
- observed:
  - `R01`, `R02`, and `R04` are now recorded as the provisional `LOGS-0002` candidate bucket
  - `R03` is now recorded as the provisional `LOGS-0001` boundary-amendment bucket because it most directly touches frontmatter/body ownership already governed in `0001`
  - `R05` remains support-only
  - the explicit current contract impact verdict is `no-contract-mutation-for-now`, so this first sample is now fully classified without opening `LOGS-0002` yet

### P3-C1-S1 (LOGS-0002 opened directly from the first body-structure sample | 2026-04-24)

- headSha: ``
- artifacts:
  - `docs/governance/contracts/workflow/logs/DOC-WORKFLOW-LOGS-0002-body-structure-and-reader-facing-log-shape.md`
  - `docs/governance/contracts/workflow/logs/register-DOC-WORKFLOW-LOGS.md`
  - `docs/governance/contracts/workflow/logs/DOC-WORKFLOW-LOGS-0001-structured-log-identity-and-front-matter.md`
  - `docs/logs/support-only/ledger-S0C-1A-log-extensions.md`
- expected:
  - open `LOGS-0002` directly instead of waiting for one second corroborating sample
  - keep `0001` readable as an earlier narrower release rather than silently replacing it
  - write the family-standing change back explicitly instead of leaving it implicit across release-local notes only
- observed:
  - `DOC-WORKFLOW-LOGS-0002` is now emitted as the current logs-family release
  - `LOGS-0001` now records reciprocal supersession and remains historical-retained rather than current-primary
  - `register-DOC-WORKFLOW-LOGS.md` now fixes that `0002` is first-open now and `0001` remains one retained earlier release
  - `S0C-1A-R01` through `R04` are now resolved through the direct-opening verdict, while `R05` remains support-only

### P1-C2-S1 (S0C-2A admitted as a structured negative-control sample | 2026-04-24)

- headSha: ``
- artifacts:
  - `docs/logs/log-S0C-2A-legacy-integration-suite-retired.md`
  - `docs/logs/support-only/ledger-S0C-2A-legacy-integration-suite-retired.md`
  - `docs/governance/contracts/workflow/logs/DOC-WORKFLOW-LOGS-0002-body-structure-and-reader-facing-log-shape.md`
  - `docs/governance/contracts/workflow/logs/register-DOC-WORKFLOW-LOGS.md`
- expected:
  - test whether one later structured source should still be rejected by the lane when its extracted rows do not govern reader-facing log body structure
  - record the routing result explicitly instead of leaving the second sample as one unclassified adjacent source
- observed:
  - `S0C-2A` now exposes explicit retirement, skip-message, replacement-coverage, and support-evidence rows under the current source template
  - those rows are useful governance candidates, but none of them contribute reusable `DOC-WORKFLOW-LOGS` body-shape meaning
  - the explicit verdict is `no logs-family impact now`: no `LOGS-0002` amendment, no `LOGS-0001` reconciliation, and no family-register update are required from this sample

### P3-C2-S1 (S0C-2A routed into DOC-WORKFLOW-LIFECYCLE-0002 | 2026-04-24)

- headSha: ``
- artifacts:
  - `docs/governance/contracts/workflow/lifecycle/DOC-WORKFLOW-LIFECYCLE-0002-continuity-test-retirement-and-replacement-coverage.md`
  - `docs/governance/contracts/workflow/lifecycle/register-DOC-WORKFLOW-LIFECYCLE.md`
  - `docs/governance/contracts/workflow/lifecycle/DOC-WORKFLOW-LIFECYCLE-0001-legacy-taxonomy-cutover-and-stub-preservation.md`
  - `docs/logs/support-only/ledger-S0C-2A-legacy-integration-suite-retired.md`
- expected:
  - keep the explicit `no logs-family impact now` verdict intact
  - avoid leaving the reusable `S0C-2A` rows indefinitely below contract level
  - open one later integrated lifecycle release rather than one broad parent stub
- observed:
  - `DOC-WORKFLOW-LIFECYCLE-0002` is now emitted as the current lifecycle-family release
  - `DOC-WORKFLOW-LIFECYCLE-0001` now remains the earlier narrower lifecycle release and the family register records that standing explicitly
  - `S0C-2A-R01` through `R03` are now resolved through the lifecycle-family opening verdict, while `R04` remains retained support-only evidence

## Recent changes

- 2026-04-23: opened `S0G-3G` as the bounded lane for cross-sample log body-structure extraction and candidate `LOGS-0002` same-family release opening.
- 2026-04-23: fixed `S0C-1A` as the first sample and fixed one dedicated parent-ledger landing surface for later sample rows.
- 2026-04-23: completed `P1-C1-S1S2` by extracting `S0C-1A` into explicit candidate rule rows and separating likely `LOGS-0002` clauses from support-only pattern evidence.
- 2026-04-24: completed `P2-C1-S1S2` for the first sample by classifying the `S0C-1A` rows into provisional `LOGS-0002`, provisional `LOGS-0001` boundary-amendment, and support-only buckets, and by fixing the explicit current verdict as `no-contract-mutation-for-now`.
- 2026-04-24: completed `P3-C1-S1` by opening `DOC-WORKFLOW-LOGS-0002` directly from `S0C-1A`, writing the reciprocal `LOGS-0001` supersession note, and creating `register-DOC-WORKFLOW-LOGS.md` so the family now has one explicit current-primary reader.
- 2026-04-24: completed `P1-C2-S1` by admitting `S0C-2A` as one structured negative-control sample, extracting it into a source-owned ledger, and recording the explicit verdict `no logs-family impact now`.
- 2026-04-24: completed `P3-C2-S1` by routing the reusable `S0C-2A` rows into `DOC-WORKFLOW-LIFECYCLE-0002`, reclassifying `DOC-WORKFLOW-LIFECYCLE-0001` as the earlier narrower release, and creating `register-DOC-WORKFLOW-LIFECYCLE.md`.