# ledger-S0A-1A-tools-github-issues-projects-and-tags

```yaml
support_only_contract_release_ledger:
  ledger_id: ledger-S0A-1A-tools-github-issues-projects-and-tags
  ledger_kind: support-only-contract-release-ledger
  status: draft
  owner_lane: S0F-7C
  source_id: S0A-1A
  source_ref: GitHub issue S0A-1A (#23) (issue-only source; no local log exists in workspace)
  source_scope: mixed issue-only source covering GitHub Issues as canonical work breakdown, GitHub Projects as execution-time support, issue title grammar, and issue tag naming
  target_reading_goal: show whether the earlier issue-only S0A-1A packet already has sufficient routing recorded through existing contracts or now needs explicit selective ledger backfill for its mixed source boundaries
```

## Decision Frame

- This ledger is a selective-backfill scaffold, not yet a full re-adjudication.
- The current draft default is:
  - keep GitHub Issues mechanism introduction aligned to `DOC-WORKFLOW-GITHUB-ISSUES-0001`
  - keep title grammar aligned to `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001`
  - keep tag naming aligned to `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001`
  - promote GitHub Projects into one first dedicated child contract rather than leaving it implicit beside the issue packet
- The purpose of this scaffold is to make the mixed-source question reviewable rather than assumed solved because contracts already exist.

## Routing And Consumption Table

| row id | source slice | meaning owned here | target family | target release action | contract lineage impact | retained-only action | resolution status | resolved by contract id | consumed scope | resolution notes | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S0A-1A-R01` | `GitHub Issues as canonical breakdown` in issue `S0A-1A (#23)` | introduce GitHub Issues as the canonical work-breakdown surface for timeline queue work | `DOC-WORKFLOW-GITHUB-ISSUES` | `existing-family-review` | `none-source-only` | `keep-in-issue` | `applied` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `full` | consumed by the existing issue-mechanism parent contract, which now serves as the explicit `ISSUES-0001` surface for this packet | This slice already maps cleanly to the existing parent contract; the backfill now makes that ownership explicit. |
| `S0A-1A-R02` | `GitHub Projects as execution-time view support` in issue `S0A-1A (#23)` | use Projects views for ad hoc or priority-insertion management without replacing issue hierarchy | `DOC-WORKFLOW-GITHUB-PROJECTS` | `new-family` | `none-source-only` | `keep-in-issue` | `applied` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `full` | consumed by a new dedicated Projects child contract because the source issue explicitly gave this support surface stable enough rule meaning to own separately | This slice was implicit in the older packet and is now made explicit through selective backfill. |
| `S0A-1A-R03` | `Title name` in issue `S0A-1A (#23)` | issue title key exposes level and category directly in the title itself | `DOC-WORKFLOW-GITHUB-ISSUES-TITLE` | `existing-family-review` | `none-source-only` | `keep-in-issue` | `applied` | `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001` | `full` | consumed by the title child contract, whose frontmatter is now aligned to the release-style template | This slice remains the clearest direct match to the title child contract. |
| `S0A-1A-R04` | `Tag name` in issue `S0A-1A (#23)` | classify issue tags by naming role across top-level, hierarchy, and module/business labels | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS` | `existing-family-review` | `none-source-only` | `keep-in-issue` | `applied` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `full` | consumed by the tag child contract, whose frontmatter is now aligned to the release-style template | This slice remains the clearest direct match to the tag child contract. |

## Row Id Map

- `S0A-1A-R01`: GitHub Issues as canonical breakdown
- `S0A-1A-R02`: GitHub Projects as execution-time view support
- `S0A-1A-R03`: Title name
- `S0A-1A-R04`: Tag name

## New Releases Expected

- `DOC-WORKFLOW-GITHUB-PROJECTS-0001`

## Deferred Slices

- whether later non-log evidence should extend `DOC-WORKFLOW-GITHUB-PROJECTS-0001` into a richer later release with more detailed operating flow

## Reader Notes

- This ledger now confirms that the earlier `S0A-1A` packet needed one explicit Projects child and explicit completed routing state, but not one workflow-level reroute.