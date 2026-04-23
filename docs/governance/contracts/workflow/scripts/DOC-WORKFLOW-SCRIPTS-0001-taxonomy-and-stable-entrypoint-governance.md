# DOC-WORKFLOW-SCRIPTS-0001 taxonomy and stable entrypoint governance

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-SCRIPTS
  contract_release: 0001
  contract_id: DOC-WORKFLOW-SCRIPTS-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Open the first workflow scripts family release from the deferred S0B-2A scripts-governance candidate by consuming the directory-taxonomy and stable-entrypoint rows together as one narrow current reader.
  summary: Govern workflow scripts through one explicit lifecycle-and-risk taxonomy plus one stable entrypoint contract that keeps invocation, safety defaults, and legacy reuse readable without collapsing adjacent labs snapshot or migration-support rules into the same family.
  owner_team: docs-governance
  current_steward: delegated:workflow-scripts-contract-maintainer
  approval_state: reviewed-awaiting-approval
  reviewed_by: role:workflow-reviewer
  approved_by: role:docs-governance-approver
  governance_area: workflow scripts taxonomy and stable entrypoint governance
  applies_to: workflow-facing scripts under backend/scripts, their lifecycle-and-risk classification, the stable CLI/router reader surface, safety defaults, and bounded legacy reuse through the stable entrypoint
  enforcement_surface: script
  violation_semantics: warning
  recorded_at: 2026-04-23
  reviewed_at: pending
  effective_from: 2026-02-13
  effective_until: ongoing
  introduced_by: docs/logs/log-S0B-2A-scripts-snapshots-management.md
  last_changed_by: docs/logs/log-S0G-1C-workflow-scripts-family-opening-and-s0b-2a-ledger-consumption.md
  source_refs:
    - docs/logs/log-S0B-2A-scripts-snapshots-management.md
    - docs/logs/log-S0G-1C-workflow-scripts-family-opening-and-s0b-2a-ledger-consumption.md
  cumulative_source_refs:
    - docs/logs/log-S0B-2A-scripts-snapshots-management.md
    - docs/logs/log-S0G-1C-workflow-scripts-family-opening-and-s0b-2a-ledger-consumption.md
  supporting_evidence_refs:
    - docs/logs/support-only/ledger-S0B-2A-tools-scripts-and-snapshots-management.md
    - docs/governance/contracts/workflow/labs/DOC-WORKFLOW-LABS-0002-labs-snapshot-evidence-package-governance.md
  lineage:
    supersedes: []
    superseded_by: []
    split_from: []
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This initial release intentionally consumes only `S0B-2A-R01` and `S0B-2A-R02` as the first scripts-family rule body.
    - The release explicitly excludes the labs-only snapshot-package slice already read through `DOC-WORKFLOW-LABS-0002`.
    - The release also excludes the deferred OPS-side snapshot-root candidate and the support-only cutover/stub slices from the first scripts-family body.
    - This release opens the family without assuming that a family transition register or bridge write-back is already required on day one.
    - `effective_from` is anchored to the decisive source log `S0B-2A` created date rather than to the later 2026-04-23 family-opening write-back date.
```

## Current Governance State

- The current effective governance state of this contract is carried in frontmatter through `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by`.
- Older fields such as `introduced_by`, `last_changed_by`, `source_refs`, and `cumulative_source_refs` remain chronology/source metadata for this release family; they should not be read as current ownership or approval identity.
- This contract therefore acts as the narrow current-state governance surface for the first `DOC-WORKFLOW-SCRIPTS` family release while the parent ledger remains the routing and later consumption-writeback surface for the mixed `S0B-2A` packet.

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-SCRIPTS-0001-GOV-01` | `contribution-event` | `DOC-WORKFLOW-SCRIPTS family` | `unknown` | `family-candidate-contributed` | `2026-02-13` | `docs/logs/log-S0B-2A-scripts-snapshots-management.md` | The mixed `S0B-2A` source introduced the scripts taxonomy and stable entrypoint rule body on 2026-02-13, but it did not by itself resolve whether those rows should open one separate family. |
| `DOC-WORKFLOW-SCRIPTS-0001-GOV-02` | `family-opening-verdict-event` | `DOC-WORKFLOW-SCRIPTS-0001` | `role:packet-reviewer` | `initial-release-opened` | `2026-04-23` | `docs/logs/log-S0G-1C-workflow-scripts-family-opening-and-s0b-2a-ledger-consumption.md` | `S0G-1C` fixed that `R01` and `R02` should travel together and now justifies opening the first scripts-family release on that narrow scope. |

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-SCRIPTS-0001-ST-01` | `Lifecycle-and-risk script classes` | `active` | `introduced` | `S0B-2A-R01` | `DOC-WORKFLOW-SCRIPTS-0001` | `2026-02-13` | `DOC-WORKFLOW-SCRIPTS-0001` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | Workflow-facing scripts should be classified by lifecycle and risk rather than by author memory or ad hoc filenames. | This clause fixes the scripts-family taxonomy boundary as the first family-owned rule. |
| `DOC-WORKFLOW-SCRIPTS-0001-ST-02` | `Named script partitions` | `active` | `introduced` | `S0B-2A-R01` | `DOC-WORKFLOW-SCRIPTS-0001` | `2026-02-13` | `DOC-WORKFLOW-SCRIPTS-0001` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | The governed scripts taxonomy should distinguish at least `ops`, `labs`, `migrations`, `dev`, and `legacy` as reader-facing partitions with different lifecycle and risk expectations. | This preserves the classification vocabulary without importing the separate cutover policy as contract scope. |
| `DOC-WORKFLOW-SCRIPTS-0001-ST-03` | `Governed placement over filename memory` | `active` | `introduced` | `S0B-2A-R01` | `DOC-WORKFLOW-SCRIPTS-0001` | `2026-02-13` | `DOC-WORKFLOW-SCRIPTS-0001` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | New workflow-facing scripts should be placed into one governed partition in that taxonomy instead of relying on personal memory of loose filenames or ad hoc directories. | This keeps the first release focused on stable placement semantics rather than on migration timing. |
| `DOC-WORKFLOW-SCRIPTS-0001-ST-04` | `Stable scripts entrypoint` | `active` | `introduced` | `S0B-2A-R02` | `DOC-WORKFLOW-SCRIPTS-0001` | `2026-02-13` | `DOC-WORKFLOW-SCRIPTS-0001` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | Workflow-facing scripts should expose one stable entrypoint through `backend/scripts/cli.py` rather than making readers remember individual script filenames as the primary invocation surface. | This clause is the first family-owned reader contract for invocation stability. |
| `DOC-WORKFLOW-SCRIPTS-0001-ST-05` | `Shared parameter and safety contract` | `active` | `introduced` | `S0B-2A-R02` | `DOC-WORKFLOW-SCRIPTS-0001` | `2026-02-13` | `DOC-WORKFLOW-SCRIPTS-0001` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | The stable entrypoint should carry one consistent parameter contract and reader-visible safety posture, including safe defaults where operator-facing script classes require them. | This keeps invocation safety in the scripts family without reclassifying the deferred OPS evidence boundary. |
| `DOC-WORKFLOW-SCRIPTS-0001-ST-06` | `Bounded legacy reuse through the stable reader` | `active` | `introduced` | `S0B-2A-R02` | `DOC-WORKFLOW-SCRIPTS-0001` | `2026-02-13` | `DOC-WORKFLOW-SCRIPTS-0001` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | The stable entrypoint may reuse legacy implementations when necessary, but legacy code should remain behind the stable reader surface rather than acting as the governing public entrypoint itself. | This clause preserves the reuse boundary without importing the separate stub-preservation packet. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-SCRIPTS-0001-CH-01` | `DOC-WORKFLOW-SCRIPTS-0001` | `introduced` | `none` | `DOC-WORKFLOW-SCRIPTS-0001-ST-01; DOC-WORKFLOW-SCRIPTS-0001-ST-02; DOC-WORKFLOW-SCRIPTS-0001-ST-03; DOC-WORKFLOW-SCRIPTS-0001-ST-04; DOC-WORKFLOW-SCRIPTS-0001-ST-05; DOC-WORKFLOW-SCRIPTS-0001-ST-06` | `2026-02-13` | `2026-04-23` | The first scripts-family release is opened because `S0G-1C` fixed that `R01` and `R02` together form one narrow, independently judgeable scripts-governance reader. | `S0B-2A-R01; S0B-2A-R02` | The initial release keeps the rule body narrow and leaves labs snapshot, OPS evidence, cutover, and stub support outside the family-opening packet. |

## Release Change

- This release opens the `DOC-WORKFLOW-SCRIPTS` family as one narrow current reader for scripts taxonomy and stable entrypoint governance.
- The release exists because the deferred `S0B-2A` scripts-governance candidate can now be defended as one shared family-opening body rather than two unresolved rows.
- The rule body's semantic start is read from the decisive `S0B-2A` source date `2026-02-13`, while the release record itself entered repo chronology later on `2026-04-23`.
- Relative to the mixed-source parent ledger, this release fixes three points:
  - workflow-facing scripts should be read through one explicit lifecycle-and-risk taxonomy
  - readers should invoke that taxonomy through one stable CLI/router surface rather than through remembered filenames
  - legacy reuse may remain behind the stable reader surface without becoming the family's public governing entrypoint
- This release intentionally does not absorb:
  - the labs-only snapshot-package slice already read through `DOC-WORKFLOW-LABS-0002`
  - the deferred OPS-side snapshot-root distinction
  - the support-only cutover and stub-preservation slices

## Contract Statement

- The table above is the clause registry for this release; the readable statement below preserves the same effective meaning in prose form.
- `DOC-WORKFLOW-SCRIPTS-0001-ST-01`: Workflow-facing scripts should be classified by lifecycle and risk rather than by author memory or ad hoc filenames.
- `DOC-WORKFLOW-SCRIPTS-0001-ST-02`: That taxonomy should distinguish at least `ops`, `labs`, `migrations`, `dev`, and `legacy` as reader-facing script classes.
- `DOC-WORKFLOW-SCRIPTS-0001-ST-03`: New scripts should be placed into one governed class in that taxonomy instead of being discovered through loose directory sprawl.
- `DOC-WORKFLOW-SCRIPTS-0001-ST-04`: Readers should enter the scripts surface through one stable entrypoint, `backend/scripts/cli.py`, rather than by memorizing individual implementation filenames.
- `DOC-WORKFLOW-SCRIPTS-0001-ST-05`: That stable entrypoint should carry one consistent parameter and safety contract, including safe defaults where the script class requires them.
- `DOC-WORKFLOW-SCRIPTS-0001-ST-06`: Legacy code may still be reused behind that stable reader, but legacy implementations should not replace the stable entrypoint as the governing public surface.

## Current Reader Shape

- This file is one narrow current reader for the first scripts-family release, not a broad parent boundary map.
- All clauses here are `introduced` in the same initial release, but they still come from two adjacent source rows that answer one shared reader problem:
  - `R01` fixes how scripts are classified and placed
  - `R02` fixes how that classified surface is invoked safely and consistently
- The contract therefore keeps both rows visible inside one release-local clause registry without importing the adjacent non-scripts slices from the same mixed source.

## Current Reading

- Read this release when the question is `what is the current stable governance reader for workflow script taxonomy and invocation?`
- Read the `S0B-2A` parent ledger when the question is `which parts of the mixed source entered this family and which parts remained deferred or support-only?`
- Read `DOC-WORKFLOW-LABS-0002` when the question is `which snapshot-package clauses were deliberately kept out of the first scripts-family release?`
- Read `S0G-1C` when the question is `why was the family opened now and why were only R01 and R02 admitted into 0001?`

## Reader Notes

- This initial release is intentionally narrow: it proves the scripts family can exist without first solving every adjacent lifecycle, snapshot, or link-preservation concern in the same packet.
- This sample now also shows one explicit three-layer split: source-side rule recording at `2026-02-13`, parent-ledger consumption write-back at `2026-04-23`, and contract effective range `2026-02-13 -> ongoing`.
- The file does not yet claim that a family transition register is needed; that verdict remains a separate write-back question for the lane.
- The file also does not yet claim that any bridge note is required on another current reader surface; that remains a separate follow-up decision rather than an assumed consequence of opening the family.