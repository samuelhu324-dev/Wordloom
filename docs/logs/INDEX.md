# At which level we are handling

## Current Levels & Descriptions
- S0: Knowledge System
- S1: SoT
- S2: Projection
- S3: Observability
- S4: Ops Runtime
- S5: Security & Governance
- S6: Evidence & Drills

- `S0-S6` is the system-level map used by this index; it is not the first-level contract taxonomy.
- Contract-family classification should be treated as a separate axis from these levels, so one contract family may affect more than one `S` level and one `S` level may contain more than one contract family.

### S0: Knowledge System

- Docs-centered management

- "Docs" based on wordloom's knowledge system:  
  1) structured logs;
  2) runbooks;
  3) external tools for workflow (e.g., GitHub);
  4) other docs (e.g., INDEX, README, or demos etc.);

### S1: SoT
- SoT = Source of Truth

- "SoT"s that provide primary layers of businesses' authoritative domain and write path 
  1) Library;
  2) Bookshelf;
  3) Book;
  4) Block;

### S2: Projection
- async/read models derived from "SoT"s

- perfect for modules with write aggregation, async consistency, transactions and constraints
  1) Search;
  2) Chronicle;
  3) Tag;
  4) etc.;

## S3: Observability
- for system's audits, rollbacks, and traceability,

- such as:
  1) triad: structured logs, metrics, tracing
  2) external assistence: Jaegar, Prometheus, Grafana, etc.;

### S4: Ops Runtime
- the operator-facing runtime layer

- covers the runtime contracts and operational paths used to package, start, deploy, verify, roll back, monitor, and recover the system through scripts, environment setup, and controlled gates
  1) damonisation (such as for event-outbox workers/patterns)
  2) deploy / verify / rollback workflows (e.g., failures drills, shadow verify, write-gate, write-readiness, dual-write, ... etc.)
  3) operator-visible gates and release operations (e.g., hard-gates & soft-gates)
  4) backup / recovery and post-change checks

### S5: Security Governance
- about system boundaries, enforceable policy and sensitive actions

- about control layer that protects system boundaries, enforces policy, and keeps sensitive actions auditable.
  1) authentication and identity context
  2) tenant boundary and data isolation
  3) authorization and policy enforcement
  4) audit logs and traceable access decisions
  5) membership, roles, and permission models
  6) backup, sanitization, and sensitive data handling
  7) security hard gates and governance drills

### S6: Evidence & Drills
- the verfication layer

- that turns system changes and scenarios into repeatable drills, structured evidence, and machine-checkable results

  1) drill scenarios and stable entrypoints
  2) structured evidence artifacts and result JSONs
  3) hard-gates and machine-checkable PASS/FAIL rules
  4) failure contracts and reason taxonomies
  5) CI-verifiable drill workflows and exported artifacts
  6) cross-domain evidence pipelines
  7) traceability by headSHA, run ID, scenario ID, and artifact lineage

# what they might contain

## Support-only historical logs

- `docs/logs/` root remains the current-log and parent-spine surface.
- Fully support-only historical logs that no longer need root placement may be relocated under `docs/logs/support-only/` when `S0F-3G` or a later bounded cleanup slice proves discoverability and rewrite safety.
- `docs/logs/support-only/INDEX.md` is the directory entrypoint for relocated support-only logs; mixed-standing or still-reader-facing logs stay at the root until a later bounded round proves they are safe to move.

## S0-related

### current logs
- S0B knowledge/index hygiene
  - docs/logs/log-S0B-2A-scripts-snapshots-management.md
  - docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
- S0C automation/tooling baseline (log extensions, CLI, artifacts, scenarios, git traceability)
  - docs/logs/log-S0C-1A-log-extensions.md
  - docs/logs/log-S0C-2A-legacy-integration-suite-retired.md
  - docs/logs/log-S0C-3A-cli-breakdown.md
  - docs/logs/log-S0C-3A-1A-double-parallel.md
  - docs/logs/log-S0C-3A-2A-artifacts-contract-packing.md
  - docs/logs/log-S0C-3A-3A-dispatch-only-argparse-extraction.md
  - docs/logs/log-S0C-4A-scenarios-taxonomy.md
  - docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md
  - docs/logs/log-S0C-5A-Git-commit+push-descriptions.md
- S0D spine (docs management v4: log/drills/runbook/UI/packing/roadmap+demo)
  - docs/logs/log-S0D-6A-docs-management-v4.md
  - docs/logs/log-S0D-1A-log-entries-orchestration.md
  - docs/logs/log-S0D-2A-drills-evidence-automation.md
  - docs/logs/log-S0D-3A-runbook-stub.md
  - docs/logs/log-S0D-4A-UI-layered-fix-notes.md
  - docs/logs/log-S0D-5A-drills-evidence-packing-unification.md
  - docs/logs/log-S0D-6A-structured-roadmap-and-demo.md

### old logs

- N/A

## S1-related

### current logs

- No dedicated `log-S1*` spine family yet; S1 is currently expressed mainly through domain modules and higher-level docs rather than a separate log chain.

### old logs

- N/A

## S2-related

### current logs
- S2B spine (projection table merge, failure contract, cutover, unified outbox)
  - docs/logs/log-S2B-projection-table-merge.md
  - docs/logs/log-S2B-1A-failure-contract-v1.md
  - docs/logs/log-S2B-1A-1A-chronicle-concurrent-handling.md
  - docs/logs/log-S2B-1A-2A-search-concurrent-handling.md
  - docs/logs/log-S2B-2A-failure-contract-v2.md
  - docs/logs/log-S2B-2A-1A-shadow-verify-write-gate.md
  - docs/logs/log-S2B-2A-2A-dual-run-cutover-closure.md
  - docs/logs/log-S2B-3A-unified-consumer-framework.md
  - docs/logs/log-S2B-4A-table-merge-migration.md
  - docs/logs/log-S2B-5A-table-merge-migration.md
  - docs/logs/log-S2B-5A-table-merge-migration-v2.md
  - docs/logs/log-S2B-6A-unified-outbox-table-merge.md
- S2C spine (projection framework platformization)
  - docs/logs/log-S2C-projection-framework-platformization.md
  - docs/logs/log-S2C-1A-projection-spec-registry-harness.md
  - docs/logs/log-S2C-2A-projection-writer-template.md
  - docs/logs/log-S2C-3A-projection-rebuild-backfill-template.md
  - docs/logs/log-S2C-4A-projection-drills-template.md
  - docs/logs/log-S2C-5A-projection-backfill-template.md
  - docs/logs/log-S2C-6A-search-harness-migration.md
- S2D spine (projection onboarding hard gates)
  - docs/logs/log-S2D-projection-onboarding-hard-gates.md
  - docs/logs/log-S2D-1A-projection-onboarding-contract-and-sample.md
  - docs/logs/log-S2D-1B-projection-onboarding-skeleton-second-sample.md
  - docs/logs/log-S2D-1C-projection-onboarding-skeleton-third-sample.md
  - docs/logs/log-S2D-1D-projection-onboarding-skeleton-fourth-sample.md
  - docs/logs/log-S2D-2A-onboarding-coverage-and-catalog-rules.md
  - docs/logs/log-S2D-3A-projection-onboarding-hard-gate-entrypoint+CI.md

### old logs

- N/A

## S3-related

### current logs
- S3A chain (observability failure drills, automation, GitHub Actions, dashboard-facing workflow)
  - docs/logs/log-S3A-2A-2B-daemon-ready-worker-migration.md
  - docs/logs/log-S3A-2A-3B-automated-failure-drills.md
  - docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md
  - docs/logs/log-S3A-2A-4B-1A-git-actions.md

### old logs

- N/A

## S4-related

### current logs
- S4A spine (systems/platform operations runtime foundation)
  - docs/logs/log-S4A-systems-platform-operations-runtime-foundation.md
  - docs/logs/log-S4A-1A-ops-scripting-baseline.md
  - docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md
  - docs/logs/log-S4A-3A-backup-recovery-operator-path.md
  - docs/logs/log-S4A-4A-hybrid-runtime-awareness.md
  - docs/logs/log-S4A-5A-operational-visibility-and-post-change-verification.md
- S4B spine (infra as code and runtime packaging)
  - docs/logs/log-S4B-infra-as-code-and-runtime-packaging.md
  - docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md
  - docs/logs/log-S4B-2A-infra-as-code-devtest-db-terraform-skeleton.md
- S4C spine (cloud services and terraform backbone)
  - docs/logs/log-S4C-cloud-services-and-terraform-epic.md
  - docs/logs/log-S4C-1A-cloud-devtest-terraform-bootstrap.md
  - docs/logs/log-S4C-2A-cloud-devtest-db-and-storage.md
  - docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md
- S4D spine (cloud runtime deploy / verify / rollback)
  - docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md
  - docs/logs/log-S4D-1A-cloud-runtime-release-path.md
  - docs/logs/log-S4D-2A-post-change-verification-and-operational-checks.md
  - docs/logs/log-S4D-3A-cloud-runtime-rollback-sample.md
  - docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md
  - docs/logs/log-S4D-4B-github-actions-release-dispatch.md
  - docs/logs/log-S4D-4C-408-timeout-eradication.md
  - docs/runbook/run-S4D-cloud-release-gate-map.md
  - docs/runbook/run-S4D-4C-agent-context-navigation.md
- S4E spine (release operating model and governance boundary)
  - docs/logs/log-S4E-release-operating-model-and-governance.md
  - docs/logs/log-S4E-1A-release-trigger-policy-and-governance-boundary.md
  - docs/logs/log-S4E-2A-environment-promotion-and-release-records.md
  - docs/logs/log-S4E-3A-approval-hierarchy-and-rollback-authority.md
  - docs/logs/log-S4E-4A-enforcement-auditability-and-environment-approver-policy.md
  - docs/logs/log-S4E-5A-higher-environment-governance-and-blocking-upgrades.md
  - docs/logs/log-S4E-5B-execution-layer-enforcement-and-controlled-exceptions.md

### old logs

- N/A

## S5-related

### current logs
- S5A spine (security/governance baseline, auth, tenant boundary, audit, backup, sanitization)
  - docs/logs/log-S5A-security-governance.md
  - docs/logs/log-S5A-1A-authcontext-policy-audit.md
  - docs/logs/log-S5A-2A-library-membership-roles-policy-audit.md
  - docs/logs/log-S5A-3A-backup-sanitization.md
  - docs/logs/log-S5A-3B-object-storage-backup.md
- S5B spine (security/governance hard gates)
  - docs/logs/log-S5B-security-governance-hard-gates.md
  - docs/logs/log-S5B-1A-policy-audit-hard-gate-drills.md
  - docs/logs/log-S5B-2A-policy-entrypoint-consolidation.md
  - docs/logs/log-S5B-3A-audit-coverage-operator-workflow.md
  - docs/logs/log-S5B-4A-search-query-authorization-drills.md
  - docs/runbook/run-S5B-security-governance-hard-gates.md

### old logs

- N/A

## S6-related

### current logs
- S6A spine (evidence and drills indexing, stable-entry contracts, hard-gate evidence JSON)
  - docs/logs/log-S6A-evidence-drills-spine.md
  - docs/logs/log-S6A-1A-stable-entry-contract.md
  - docs/logs/log-S6A-2A-unify-supply-creation.md
  - docs/logs/log-S6A-3A-failure-taxonomy-hard-interface.md
  - docs/logs/log-S6A-4A-hard-gate-evidence-json.md
  - docs/runbook/run-S6A-evidence-drills-spine.md

### old logs

- S6 is the only scope that currently keeps an explicit old-logs section, because its current spine was distilled from earlier cross-domain evidence and drills practices rather than being designed as a first-class domain family from the beginning.
- S6A spine (new SoT index)
  - docs/logs/log-S6A-evidence-drills-spine.md

- Artifacts / Evidence contract
  - docs/logs/log-S0C-3A-2A-artifacts-contract-packing.md

- Git discipline for evidence (descriptions / traceability)
  - docs/logs/log-S0C-5A-Git-commit+push-descriptions.md

- Scenarios taxonomy / catalog-driven suites
  - docs/logs/log-S0C-4A-scenarios-taxonomy.md
  - docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md

- Failure Contract (S2B)
  - docs/logs/log-S2B-1A-failure-contract-v1.md
  - docs/logs/log-S2B-2A-failure-contract-v2.md
  - docs/logs/log-S2B-2A-1A-shadow-verify-write-gate.md
  - docs/logs/log-S2B-2A-2A-dual-run-cutover-closure.md

- Unified consumer framework / reasons taxonomy (S2B)
  - docs/logs/log-S2B-3A-unified-consumer-framework.md

- Automated failure drills (buttons: run/verify/export/clean)
  - docs/logs/log-S3A-2A-3B-automated-failure-drills.md
  - docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md

- Projection drills templates (platformization)
  - docs/logs/log-S2C-4A-projection-drills-template.md
  - docs/logs/log-S2C-projection-framework-platformization.md

- Backup drills as evidence pipelines (S5A)
  - docs/logs/log-S5A-security-governance.md
  - docs/logs/log-S5A-1A-authcontext-policy-audit.md
  - docs/logs/log-S5A-2A-library-membership-roles-policy-audit.md
  - docs/logs/log-S5A-3A-backup-sanitization.md
  - docs/logs/log-S5A-3B-object-storage-backup.md

# Historical Appearance View

- This view is one chronology aid for `docs/logs/log-*.md`, not one unique lineage or family-history truth surface.
- Mechanical sort rule:
  - primary key: `frontmatter.created` ascending
  - tie-breaker inside the same day: root log file name ascending
- `current-template ledger note` marks only the current `support_only_contract_release_ledger` extraction model under `docs/logs/support-only/`; older six-outlet-era exports do not count here.

| created | historical appearance rows | current-template ledger note |
| --- | --- | --- |
| 2026-02-12 | `S0B-3A` | `S0B-3A` -> `ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter` |
| 2026-02-13 | `S0B-2A`, `S3A-2A-2B` | `S0B-2A` -> `ledger-S0B-2A-tools-scripts-and-snapshots-management` |
| 2026-02-14 | `S3A-2A-3B`, `S3A-2A-4B`, `S3A-2A-4B` | none |
| 2026-02-15 | `S0C-1A`, `S2B-1A-1A`, `S2B-1A`, `S2B-projection-table-merge` | `S0C-1A` -> `ledger-S0C-1A-log-extensions` |
| 2026-02-17 | `S0C-2A`, `S2B-1A-2A` | `S0C-2A` -> `ledger-S0C-2A-legacy-integration-suite-retired` |
| 2026-02-18 | `S2B-2A-1A`, `S2B-2A-2A`, `S2B-2A` | none |
| 2026-02-20 | `S0C-3A-1A`, `S0C-3A` | none |
| 2026-02-21 | `S0C-3A-2A` | none |
| 2026-02-22 | `S0C-3A-3A`, `S0C-4A` | none |
| 2026-02-23 | `S0C-4A-1A`, `S0C-5A`, `S2B-3A` | none |
| 2026-02-24 | `S2B-4A` | none |
| 2026-02-26 | `S2B-5A`, `S2B-5A` | none |
| 2026-02-27 | `S2B-6A` | none |
| 2026-02-28 | `S2C-1A`, `S2C-projection-framework-platformization` | none |
| 2026-03-01 | `S2C-2A`, `S2C-3A`, `S2C-4A`, `S2C-5A`, `S2C-6A` | none |
| 2026-03-02 | `S5A-1A`, `S5A-2A`, `S5A-security-governance` | none |
| 2026-03-03 | `S5A-3A`, `S5A-3B` | none |
| 2026-03-04 | `S6A-1A`, `S6A-evidence-drills-spine` | none |
| 2026-03-05 | `S6A-2A`, `S6A-3A`, `S6A-4A` | none |
| 2026-03-06 | `S0D-1A`, `S5B-1A`, `S5B-security-governance-hard-gates` | none |
| 2026-03-07 | `S0D-2A`, `S5B-2A`, `S5B-3A` | none |
| 2026-03-08 | `S2D-1A`, `S2D-projection-onboarding-hard-gates`, `S5B-4A` | none |
| 2026-03-09 | `S2D-3A` | none |
| 2026-03-10 | `S2D-1B`, `S2D-2A` | none |
| 2026-03-11 | `S2D-1C`, `S2D-1D` | none |
| 2026-03-13 | `S0D-3A`, `S0D-4A` | none |
| 2026-03-14 | `S0D-5A` | none |
| 2026-03-20 | `S4A-1A`, `S4A-systems-platform-operations-runtime-foundation` | none |
| 2026-03-21 | `S0D-6A`, `S4A-2A`, `S4A-3A`, `S4A-4A`, `S4A-5A`, `S4B-1A`, `S4B-2A`, `S4B` | none |
| 2026-03-22 | `S0E-1A`, `S0E-1B`, `S4C-1A`, `S4C-2A`, `S4C-3A`, `S4C` | none |
| 2026-03-23 | `S4D-1A`, `S4D` | none |
| 2026-03-24 | `S4D-2A`, `S4D-3A` | none |
| 2026-03-25 | `S4D-4A`, `S4D-4B` | none |
| 2026-03-26 | `S4D-4C` | none |
| 2026-03-27 | `S4E-1A`, `S4E-2A`, `S4E-3A`, `S4E-4A`, `S4E-5A`, `S4E-5B`, `S4E` | none |
| 2026-03-28 | `S0E-2A`, `S0E-2B`, `S0E-2C`, `S0E-docs-management-v5` | none |
| 2026-03-29 | `S0E-2D`, `S0E-2E`, `S0E-3A`, `S0E-4A`, `S0E-4B` | none |
| 2026-03-30 | `S0E-4C`, `S0E-4D`, `S0E-5A`, `S0E-5B`, `S0E-5C` | none |
| 2026-03-31 | `S0E-4E`, `S0E-5D`, `S0E-6A`, `S0E-6B`, `S0E-7A` | none |
| 2026-04-01 | `S0E-6C`, `S0E-6D`, `S0E-6E`, `S0E-7B`, `S0E-7C` | none |
| 2026-04-02 | `S0E-4F`, `S0E-6F`, `S0E-7D` | none |
| 2026-04-03 | `S0E-3B`, `S0E-5E` | none |
| 2026-04-04 | `S0F-1A`, `S0F-1B`, `S0F-1C`, `S0F-1D`, `S0F-docs-management-v6`, `S6B-1A`, `S6B-1B`, `S6B-1C`, `S6B-evidence-drills-taxonomy` | none |
| 2026-04-05 | `S0F-1G`, `S0F-1H`, `S0F-1J`, `S0F-2A`, `S0F-2B` | none |
| 2026-04-06 | `S0F-3A`, `S0F-3B`, `S0F-3C`, `S0F-3D`, `S0F-3E`, `S0F-3F`, `S0F-3G` | none |
| 2026-04-07 | `S0F-1K`, `S0F-3H`, `S0F-4A`, `S0F-4B` | none |
| 2026-04-08 | `S0F-3I`, `S0F-3J`, `S0F-4C`, `S0F-4D`, `S0F-4E`, `S0F-4F`, `S0F-4G`, `S0F-5A` | none |
| 2026-04-09 | `S0F-3K`, `S0F-3L`, `S0F-3M`, `S0F-4H`, `S0F-4I`, `S0F-5B`, `S0F-5C`, `S0F-5D`, `S0F-5E`, `S0F-5F`, `S0F-6A`, `S0F-6B`, `S0F-6C` | none |
| 2026-04-10 | `S0F-5G`, `S0F-5H`, `S0F-5I`, `S0F-5J`, `S0F-7A`, `S0F-7B`, `S0F-7C` | none |
| 2026-04-11 | `S0F-7D`, `S0F-8A` | none |
| 2026-04-12 | `S0F-7E` | none |
| 2026-04-13 | `S0F-7F`, `S0F-7G`, `S0F-7H` | none |
| 2026-04-14 | `S0F-7I`, `S0F-8B` | none |
| 2026-04-15 | `S0F-10A`, `S0F-10B`, `S0F-10C`, `S0F-10D`, `S0F-9A` | none |
| 2026-04-16 | `S0F-9B`, `S0F-9C`, `S0F-9D`, `S0F-9E` | none |
| 2026-04-17 | `S0F-9F`, `S0F-9G` | none |
| 2026-04-19 | `S0F-9H` | none |
| 2026-04-20 | `S0G-1A`, `S0G-2A`, `S0G-docs-management-v7`, `S4F-1A`, `S4F-2A`, `S4F-2B`, `S4F-2C`, `S4F` | none |
| 2026-04-21 | `S0G-2B`, `S0G-3A`, `S0G-3B`, `S0G-3C`, `S0G-3D`, `S0G-3E` | none |
| 2026-04-22 | `S0G-1B`, `S0G-3F`, `S0G-4A` | none |
| 2026-04-23 | `S0G-1C`, `S0G-3G`, `S0G-4B`, `S0G-5A` | none |
