# log-S0C-2A (Phase 2A: legacy integration suite retired and current-test protection rewrite)

---

**id**: `S0C-2A`
**kind**: `log`
**title**: `testing legacy integration suite retired and current-test protection rewrite v1`
**status**: `stable`
**scope**: `S0C`
**tags**: `EVOLUTION, Testing, Drills, Evidence, epic/s0c, sub/2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: `docs/adr/adr-S2B-legacy-integration-suite-retired.md`
  **runbook**: ``
  **parent_log**: ``
  **previous_log**: ``
  **reference_log_1**: `docs/logs/log-S2B-1A-failure-contract-v1.md`
**issue_keyword**: `evidence`
**issue_top_labels**: ``
**issue_scope_labels**: ``
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: ``
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: ``
**pr_development_issue**: ``
**created**: `2026-02-17`
**updated**: `2026-04-24`
**reviewed**: `pending`
**source_reader_model**: `mixed-source-v1`
**extraction_surface_version**: `extractable-rules-v1`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are artifact-lifecycle fields only.
- This source log records when the retirement packet was authored and later refit; it does not claim to define semantic-effective dates for any later contract or ledger route.
- Any later family-routing or release-effective dates should remain on downstream ledger or contract surfaces rather than being widened into this log frontmatter.

## Decision / Outcome

**Decision**:

- Retire the legacy integration suites `backend/api/app/tests/test_library/test_integration_round_trip.py` and `backend/api/app/tests/test_integration_four_modules.py` by module-level skip instead of forcing the current system to stay compatible with obsolete `modules.*` paths and removed legacy domain APIs.
- Treat the retirement as a current-system protection decision: the active quality gate should move to tests that exercise current use-case, repository, exception-mapping, and domain-invariant behavior rather than preserving obsolete integration narratives as hard gates.
- Keep the retirement reason explicit and auditable through the paired ADR/log references and through one reproducible pytest result that proves coverage moved rather than disappeared.

**Default choices (phase defaults / v1)**:

- When one test suite fails only because it encodes obsolete layout or removed APIs, prefer explicit retirement plus current replacement coverage over compatibility shims that distort the current architecture.
- Strong source structure alone is not enough to make this log one `DOC-WORKFLOW-LOGS` sample: downstream routing still depends on whether the extracted rows express reusable log-body meaning rather than testing-lifecycle or repo-test governance.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

**验证结果（当次证据）**：

- `api/app/tests/test_library` 在退役后达到 `131 passed, 1 skipped`。
- 本批次对齐“保护现在”的测试后，全量 `pytest -q` 达到 `470 passed, 132 skipped`（另有 `12 warnings`）。

## Background

在演进过程中，测试的首要目的不是“保持旧世界可运行”，而是**保护当前系统的行为与契约**。当某些历史测试套件：

- 绑定到已弃用的模块布局（例如 `modules.*`），
- 假设了已被移除/替换的 domain API 与事件模型，

那么它们的失败会持续制造“假阴性”（false negatives），阻塞当前交付与演进，且会诱导团队为了修测试去引入不必要的兼容层。

## Problem / Malfunction

- **症状**：全量/子集 pytest 运行被 `test_integration_round_trip.py` 大量失败阻塞。
- **根因**：该文件不是对当前系统的黑盒/契约测试，而是对早期架构/旧 API 的硬编码“集成叙事脚本”。当前代码与其假设已不可对齐。
- **风险**：若强行对齐（加 shim 或重构 domain 以迎合测试），会引入额外 surface area 与长期维护负担，且可能扭曲当前架构边界。

补充：同类问题也出现在 `test_integration_four_modules.py`（Phase 1.5 的叙事式集成套件），其失败同样不代表当前系统回归。

## What/How to do（落地规则）

### 1) 退役规则：skip 而不是“硬修到绿”

- 对于明确指向 **deprecated module layout / obsolete API** 的 legacy suite：
  - 使用 `pytest.skip(..., allow_module_level=True)` 退役；
  - skip message 必须包含：退役原因、指向 ADR/Log 的链接。

### 2) 替代保护网：写“保护现在”的测试

- **Application layer（优先）**：use case + ports + repository 的契约测试（尤其是异常语义与 DTO 映射）。
- **Infrastructure/Repository（必要）**：关键行为合约（例如 soft-delete 行为、时间戳、过滤规则）。
- **Domain（最小必要）**：不变量与事件发射在仍被系统依赖时才测试；避免为了叙事完整而测试不存在的 API。

本批次落地示例（对齐当前系统语义）：

- `api/app/tests/test_book/test_application_layer.py`：重写为对齐当前 Book UseCase API + Basement（`soft_deleted_at`）语义的最小单测集。
- `api/app/tests/test_block/test_repository.py`：将旧字段/构造参数从 `index/is_deleted/block_id/block_type` 对齐到当前领域模型的 `order/soft_deleted_at/id/type`，并补齐 HEADING 的 `heading_level` 约束。

### 3) 证据链要求（DoD）

- suite 退役不应导致“无人负责的空白”：
  - 必须能指出当前系统对应的测试覆盖位置（文件/目录级即可）；
  - 需要一次可复现的通过结果（pytest 输出）作为证据。

## Extractable Rule Surface

| packet id | source anchor | extraction class | candidate text | downstream owner | split status | shared reason group | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R01` | `Decision / Outcome` bullet 1-3 | `contract-candidate` | Legacy test suites that depend on deprecated module layout or removed APIs should be retired by explicit module-level skip instead of being force-fixed into the current system. | `contract` | `needs-corroboration` | `RG-01` | `docs/adr/adr-S2B-legacy-integration-suite-retired.md` | Stable candidate, but it is not a logs-family body-structure rule. |
| `R02` | `What/How to do -> 1) 退役规则：skip 而不是“硬修到绿”` | `contract-candidate` | Retirement-by-skip should carry one explicit skip message that states the retirement reason and links to the governing ADR/log packet. | `contract` | `needs-corroboration` | `RG-01` | `docs/adr/adr-S2B-legacy-integration-suite-retired.md` | This is a narrow operational rule candidate for future test-lifecycle governance. |
| `R03` | `Decision / Outcome` bullet 4; `What/How to do -> 2) 替代保护网` | `contract-candidate` | Retiring one obsolete suite must be paired with current-system replacement coverage at the application, repository, or still-live domain-invariant layers. | `contract` | `needs-corroboration` | `RG-02` | `api/app/tests/test_book/test_application_layer.py`; `api/app/tests/test_block/test_repository.py` | Stable rule candidate for test-governance routing, but not a logs-body clause. |
| `R04` | `What/How to do -> 3) 证据链要求（DoD）`; `验证结果（当次证据）` | `support-only` | Retirement should keep one reproducible proof that replacement coverage passed after the obsolete suites were removed from the active gate. | `support-only` | `not-for-extraction` | `RG-02` | `api/app/tests/test_library`; `pytest -q` | Evidence requirement is valuable, but the concrete pass counts are support-only rather than primary contract text. |

### Shared Reason Groups

| reason group | applies to packet ids | reason summary | source refs | notes |
| --- | --- | --- | --- | --- |
| `RG-01` | `R01; R02` | Obsolete integration narratives create false negatives and incentivize compatibility shims that distort the current architecture. | `Problem / Malfunction`; `What/How to do -> 1)` | Shared rationale for explicit retirement and explicit retirement messaging. |
| `RG-02` | `R03; R04` | Retirement is only defensible when current-system behavior remains protected through replacement tests and one reproducible evidence trail. | `Decision / Outcome`; `What/How to do -> 2)`; `What/How to do -> 3)` | Shared rationale for replacement coverage and retained evidence. |

## Source Reader Model / Versioning

| field | value | notes |
| --- | --- | --- |
| current source reader model | `mixed-source-v1` | Decision plus bounded extraction table over one mixed testing-governance packet. |
| extraction surface version | `extractable-rules-v1` | This refit exposes stable retirement and replacement-coverage candidates explicitly. |
| compatibility expectation | `forward-readable` | Older readers can still use the narrative body, while later extractors should prefer the extraction table. |
| migration note | `2026-04-24 refit adds explicit extraction rows without changing the original retirement outcome.` | Source-reader update only; not a release-semantic change. |

## Optional Required Processing Chain

| chain step | required state | primary owner surface | trigger question | completion evidence | notes |
| --- | --- | --- | --- | --- | --- |
| `source extraction` | `required` | `S0C-2A` | `Has the retirement packet been normalized into reusable rule candidates rather than left as mixed narrative only?` | `Extractable Rule Surface rows R01-R04` | Required for later routing review. |
| `SUP` | `not-required` | `n/a` | `Is later evidence needed only to sharpen one already-routed row?` | `explicit no-SUP verdict` | Current packet already carries enough direct evidence for first-pass routing. |
| `parent ledger` | `required` | `source-owned support-only ledger for S0C-2A` | `Does the packet need an explicit routing verdict against S0G-3G and possible downstream families?` | `ledger-S0C-2A-legacy-integration-suite-retired.md` | Required to separate extraction from downstream family choice. |
| `contract impact decision` | `required` | `S0C-2A` | `Is this packet a logs-family sample, a family-mismatch sample, or a future non-logs contract candidate?` | `explicit classified verdict` | Boundary gate for this refit. |
| `contract mutation` | `conditional` | `future family contract or n/a` | `Does this packet change defended current contract meaning now?` | `explicit admitted-or-no-op verdict` | This packet is now admitted into `DOC-WORKFLOW-LIFECYCLE-0002`, while still leaving `DOC-WORKFLOW-LOGS` unchanged. |
| `transition register update` | `conditional` | `affected family register or n/a` | `Did any family-level current-reader standing change?` | `explicit register update or no-register-change verdict` | This packet now changes lifecycle-family release standing, but not logs-family standing. |
| `bridged contract reconciliation` | `not-required` | `n/a` | `Do current readers need redirect or bridge notes because of this packet?` | `explicit no-bridge-impact verdict` | No current bridge write-back is needed in this round. |

## Exported Sections / Outlet Ownership

**Outlet ownership**:

- `contract`: potential future landing for a narrower test-retirement or test-lifecycle family if corroborating source packets appear.
- `runbook`: no-op for now; this packet states policy and evidence more than repeatable operator procedure.
- `view`: no-op for now; no reader-facing summary surface is needed yet.
- `index/front-door`: no-op for now.
- `disposition/placement`: this source remains the retained historical proof of why the legacy suites were removed from the active gate.
- `log-retained core`: the retirement decision, replacement-coverage rule, and bounded evidence summary remain readable here.

## Definitions

- **legacy integration suite**: a test packet that still encodes obsolete layout, import paths, or removed APIs and therefore no longer measures current-system behavior faithfully.
- **replacement coverage**: current-system tests that protect the behavior still worth gating after the obsolete suite is retired.
- **false negative**: a failure produced by outdated assumptions rather than by a regression in the current system.

## Constraints

- Do not treat obsolete integration narratives as required active gates once their assumptions no longer match the current system.
- Do not retire a failing suite without naming the replacement-coverage surface.
- Do not treat this packet as a logs-family body-structure source merely because it now has a well-structured extraction table.

## Current Status

- `S0C-2A` now reads as one explicit retirement-governance packet: obsolete suites were removed from the active gate, replacement coverage was named, and the local evidence trail was preserved.
- Under the current extraction model, the packet yields reusable retirement and replacement-coverage candidates, but those candidates still do not map to `DOC-WORKFLOW-LOGS-0002` clause ownership.
- The packet therefore remains a useful structured sample and a useful negative control for `S0G-3G` on the logs side, while its reusable retirement rows are now admitted into `DOC-WORKFLOW-LIFECYCLE-0002` as one later integrated lifecycle release.

## Evidence

### Retirement And Replacement Coverage (2026-02-17)

- headSha: ``
- artifacts:
  - `docs/adr/adr-S2B-legacy-integration-suite-retired.md`
  - `backend/api/app/tests/test_library/test_integration_round_trip.py`
  - `backend/api/app/tests/test_integration_four_modules.py`
  - `api/app/tests/test_book/test_application_layer.py`
  - `api/app/tests/test_block/test_repository.py`
- expected:
  - obsolete integration narratives should stop blocking current delivery once the repo has clearer current-system protection
  - replacement coverage should be identifiable and one reproducible pytest result should remain attached to the retirement packet
- observed:
  - both legacy integration suites were retired through module-level skip rather than compatibility repair
  - current-system protection was redirected to current application-layer and repository-focused tests
  - the packet retained one reproducible pytest result for the local library scope and one whole-suite result

## Next

- If a second or third source packet expresses the same retirement-by-skip and replacement-coverage rules, decide whether `DOC-WORKFLOW-LIFECYCLE-0002` should remain integrated, be amended, or split into one narrower test-retirement lifecycle release.
- Keep this source as retained proof, keep `DOC-WORKFLOW-LOGS` unchanged, and treat concrete pytest outputs as support-only unless a later evidence model explicitly promotes them.

## References

- `docs/adr/adr-S2B-legacy-integration-suite-retired.md`
- `backend/api/app/tests/test_library/test_integration_round_trip.py`
- `backend/api/app/tests/test_integration_four_modules.py`
- `docs/logs/log-S2B-1A-failure-contract-v1.md`

