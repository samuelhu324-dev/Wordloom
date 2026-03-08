# log-S5B-4A-search-query-authorization-drills（Phase 4：Search query authorization + tenant isolation v1）

---

**id**: `S5B-4A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `search query authorization + tenant isolation (drills/evidence) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S5`
**tags**: `EVOLUTION, Security, Governance, MultiTenant, Authorization, Policy, Audit, Drills, Evidence, HardGate, Search, Query, epic/s5, epic/s5b, sub/4a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S5B-security-governance-hard-gates.md`
  **previous_log**: `docs/logs/log-S5B-3A-audit-coverage-operator-workflow.md`
  **reference_log_1**: `docs/logs/log-S5B-1A-policy-audit-hard-gate-drills.md`
  **reference_log_2**: `docs/logs/log-S5B-2A-policy-entrypoint-consolidation.md`
  **reference_log_3**: `docs/logs/log-S5B-3A-audit-coverage-operator-workflow.md`
**created**: `2026-03-08`
**updated**: `2026-03-08`

---

## Decision / Outcome（结论区）

**Decision**:

- 选定一条典型的 search 链路（例如「按关键字搜索书/文档」），把 AuthContext/tenant/policy/audit contract 从“隐含约定”收紧为可机械判定的 contract，并配套 drills/evidence。
- 按路线 C 的 P0–P3 做法，把 search 做成第二条完整的「AuthContext + policy + audit + drills + hard gate」示例链路，补上当前系统在公开度/越权风险最高区域的防线。

**Default choices（本 phase 默认决策 / v1）**:

- 仍然以 dev/test 环境为主（本地 API + devtest DB），不直接触碰生产流量。
- search 的授权语义优先沿用 S5B-1A 的 deny 语义与 reason 白名单，避免新增高基数 reason。
- drills/evidence 继续复用 S5B-1A/S5B-3A 的 artifacts contract 与 verifier（schema_version 与 failure taxonomy 一致）。

## Definitions（概念定义，可选）

- **Search query**：面向终端用户的查询接口，例如「按关键字搜索书/文档」，通常表现为 GET /search... 或模块内的 query API。
- **Search authorization**：对 search 结果集合施加 tenant/role 限制，确保用户只能看到自己有权限访问的资源（不出现「别人的书架/文档」）。
- **Search surface**：所有会暴露搜索结果的 API/场景（例如 Web 搜索框、API 客户端、内部运维工具）。
- **Tenant escape via search**：通过搜索结果间接看到其他 tenant 的资源（即使无法直接访问详情页）。

## Constraints（约束）

- search 的 AuthContext 必须至少包含 tenant_id/request_id/actor_user_id/roles，不允许匿名 search 绕过 tenant 边界（除非明确声明为公开索引）。
- deny/过滤逻辑必须集中在 policy/查询构造层，禁止在 handler 内散落 if-else 过滤已返回的结果。
- audit_contract：对于关键 search API，需要有可回溯的 audit 记录（至少记录 request_id/tenant_id/action/result/reason），并可被 drills 机械判定。
- drills 产物必须满足 artifacts contract，且能够在 CI hard gate 中复跑，不依赖生产数据。

## Scope（本 log 范围）

- `P0`：contract（search AuthContext/tenant/policy/audit contract；search action/result/reason 命名与 evidence 口径）
- `P1`：实现（统一 search policy entrypoint + 查询层 tenant filter，收口 search 授权逻辑）
- `P2`：drills（设计并实现 search tenant escape / 覆盖不足的 drills，复用 S5B-1A/S5B-3A 的 artifacts contract）
- `P3`：hard gate & wiring（接 S0D-2A 的 run_dir + hard gate 入口，形成 CI hard gate，或明确记录暂不接入的原因）

## Success Criteria（DoD）

- 至少 1 条代表性的 search 链路满足：
  - 查询语义在 AuthContext/tenant/policy/audit contract 中被明确描述（含公开/非公开、可见资源类型）。
  - tenant 边界在查询层被硬性约束（例如 WHERE tenant_id = :ctx.tenant_id），不存在「先跨 tenant 搜索后再在代码里过滤」的路径。
  - deny/过滤原因（例如 tenant_mismatch/not_member/not_admin）落在低基数白名单中，并写入 audit_log.reason 或可等价回溯。
- 至少 1 组 search drills 可以在 dev/test 环境完整跑通：
  - 包含「本 tenant 正常搜索」「跨 tenant 搜索不应返回结果」「权限不足角色搜索」等基本场景。
  - artifacts 满足 S5B-1A 的 `_recipe.json/_result.json/_logs/_metrics` contract，且 `_result.json.ok` 可作为 hard gate 信号。
- CI 或单命令 hard gate 入口可以重复触发上述 search drills，并将 run_dir 写入 artifacts JSON（例如 `artifacts/s5b4a-runs.json`）。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - `P0-P3` 的 contract + search 授权实现 + drills + hard gate（若接入）已跑通；
  - Evidence 区有至少 1 条可追溯的 `headSha` + search drills run_dir + CI run URL（或本地 run 记录）。

## P0（Contract｜v1）

### P0-C1-S1（Target search chain & action 命名）

- v1 选定的代表性 search 链路：
  - HTTP：`GET /search/blocks/two-stage`
  - Router：`backend/api/app/modules/search/routers/search_router.py::search_blocks_two_stage`
  - 描述：two-stage block search（先 search_index 召回候选，再在 blocks + tag_associations + tags 上做严格过滤并返回 tags）。
- 本 phase 聚焦这条链路的授权/tenant/audit 行为，其它 `/search/*` 端点（包括 `GET /search` 全局搜索）在 v1 中视为 out-of-scope，仅在后续阶段评估是否迁移到同一骨架。
- 为这条链路定义 canonical audit action：
  - 主 action：`search.blocks.two_stage`
  - 可预留后续扩展：`search.blocks`（单 stage blocks search）、`search.global`（全局搜索），但本 phase 的 drills/evidence 仅以 `search.blocks.two_stage` 为硬合同。

### P0-C1-S2（Search authorization & audit contract）

- AuthContext 要求：
  - `search_blocks_two_stage` 必须在 handler 层拿到 `AuthContext`（含 `tenant_id/request_id/actor_user_id/roles`）；
  - `library_id` query 参数与 `AuthContext.tenant_id` 的关系：
    - 若未显式传入 `library_id`，默认取 `library_id = ctx.tenant_id`；
    - 若显式传入 `library_id`，必须等于 `ctx.tenant_id`，否则视为 tenant 越权，按 deny 处理；
    - 匿名请求或缺失 membership 的请求不得绕过上述约束（按 401/403 处理）。
- Deny/过滤语义沿用 S5B-1A 的 contract：
  - `result` 枚举：`success | denied | not_found | error`；
  - 当 search 因 tenant/role/membership 被限制或抛出 403 时：
    - `result=denied`，`reason in {tenant_mismatch, not_member, not_admin}`；
  - 对于「自然无结果」的查询（在合法 tenant/角色下确实没有匹配项）：
    - HTTP 200；`result=success`，`reason=null`；结果集合允许为空，不引入额外 reason。
  - search 内部错误（例如下游 DB/search_index 异常）：
    - `result=error`，`reason in {dependency_error, internal_error}`，具体映射在 P1 实现阶段细化。
- Audit 约束：
  - 两类请求需要写入 audit 行：
    - 「关键管理型搜索」场景（例如管理后台或具备 admin 权限的内容搜索），以及
    - drills 设计覆盖的所有 search tenant escape / 权限不足场景；
  - 审计字段需满足 S5B-1A 的 action/result/reason contract：
    - `action = search.blocks.two_stage`；
    - `result ∈ {success, denied, error}`；
    - `reason` 来自低基数白名单或为 null（仅在 `result=success` 时允许）；
    - 审计记录必须携带 `tenant_id/actor_user_id/request_id`，并推荐补充 `library_id` 及 `q_preview` 等低基数字段到 `meta_json`。

### P0-C1-S3（Evidence & artifacts contract｜v1）

- suite（v1 草案）：
  - `suite_id`：`search_query_authorization`
  - runner 预计为：`python scripts/drills/s5b4a_p2c1s1_drills_runner.py`（后续 P2 实现时补充）。
- artifacts layout：
  - `docs/labs/_snapshot/auto/S5B-4A/<suite_id>/<run_id>/`，复用 S5B-1A/S5B-3A 的目录结构。
- schema_version：
  - `_recipe.json.schema_version = "s5b-1a.recipe.v1"`
  - `_result.json.schema_version = "s5b-1a.result.v1"`
  - `_metrics/*.json.schema_version = "s5b-1a.metrics.v1"`
- verifier：
  - 复用 `python scripts/drills/s5b1a_verify_artifacts.py --run-dir <run_dir>`；
  - hard gate 以 verifier exit code 与 `_result.json.ok` 作为 PASS/FAIL 判定。

### P0-C2-S1（Global search chain & action 命名｜draft）

- C2 目标 search 链路：
  - HTTP：`GET /search`
  - Router：`backend/api/app/modules/search/routers/search_router.py::search_global`
  - 描述：global search（聚合 blocks/books 等实体的结果，按 score 排序）。
- 与 C1 的关系：
  - C1 锁定 `GET /search/blocks/two-stage` 作为「高风险 blocks 内容搜索」主链路；
  - C2 把同一套 AuthContext/tenant/audit 语义延展到 global search 聚合层，避免「全局搜索」成为新的 tenant escape 通道。
- 为 global search 定义 canonical audit action：
  - 主 action：`search.global`
  - 允许在 meta_json 中记录实体类型分布（如 `entity_types={blocks,books,...}`），但 audit.action 本身维持低基数，不按实体类型拆分。

### P0-C2-S2（Global search authorization & audit contract｜draft）

- AuthContext 要求：
  - `search_global` 必须在 handler 层拿到 `AuthContext`（含 `tenant_id/request_id/actor_user_id/roles`），不得以匿名方式跨 tenant 搜索；
  - `library_id` 参数语义与 C1 保持一致：
    - 未显式传入时，默认 `library_id = ctx.tenant_id`；
    - 若显式传入且 `library_id != ctx.tenant_id`，按 tenant 越权处理（deny + 403），不可默默改为本 tenant；
    - 缺失 membership 或角色不足时，按 401/403 处理，不允许「降级为匿名 global search」。
- Deny/过滤语义沿用 S5B-1A 的 contract：
  - `result ∈ {success, denied, not_found, error}`；
  - 因 tenant/role/membership 限制导致拒绝执行（或显式拒绝返回结果）时：
    - `result=denied`，`reason ∈ {tenant_mismatch, not_member, not_admin}`；
  - 自然无结果（合法 tenant/角色下确无匹配项）：
    - HTTP 200；`result=success`，`reason=null`；结果集合允许为空；
  - 内部错误（下游 DB/search_index 异常、聚合逻辑异常等）：
    - `result=error`，`reason ∈ {dependency_error, internal_error}`，具体映射在 P1-C2 实现阶段细化。
- Audit 约束（global search）：
  - 至少覆盖两类请求：
    - drills 涵盖的所有 global search tenant escape / 权限不足场景；
    - 具备 admin/高敏感度视图的 global search 调用（例如运维/后台工具入口）。
  - 审计字段遵循 S5B-1A contract：
    - `action = search.global`；
    - `result ∈ {success, denied, error}`；
    - `reason` 来自低基数白名单或为 null（仅在 `result=success` 时允许）；
    - 必须携带 `tenant_id/actor_user_id/request_id`，推荐在 `meta_json` 中补充：
      - `q_preview`、`library_id`、`limit/offset`；
      - `entity_types`（命中特定实体类型集合）与 `hit_count_total`，便于后续分析。

### P0-C2-S3（Global search evidence & artifacts contract｜draft）

- suite 复用原则：
  - 继续使用 `suite_id = search_query_authorization`，在同一套 drills 中新增 global search 相关 case；
  - 通过 scenario 名称 / case_id 区分 blocks two-stage 与 global search 场景。
- artifacts layout：
  - 仍然落在 `docs/labs/_snapshot/auto/S5B-4A/<suite_id>/<run_id>/` 之下；
  - `_recipe.json` 中新增/调整 scenario 列表以覆盖 global search；
  - `_result.json` 中按 case 维度标记 global search 的 pass/fail。
- schema_version：
  - 继续使用 `s5b-1a.*.v1` 系列，不单独 fork 版本；
  - 若未来 global search 引入额外维度（例如 per-entity-type metrics），优先通过 `_metrics/*.json` 扩展字段而非变更 schema_version。
- verifier：
  - 仍由 `scripts/drills/s5b1a_verify_artifacts.py` 负责校验 artifacts 合同；
  - 要求 verifier 可以识别并报告 global search case 的结果（例如通过 case_id 前缀 `global_`）。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S5B-4A/P<phase>-C<cycle>-S<step>: <summary>`

**Branch 约定**:

- 对应 scope/index 的 log（例如 `S5B-3A` 隶属于 `S5B`，`S0D-2A` 隶属于 `S0D`）优先在同名前缀的工作分支上推进 P* 的代码与文档变更：
  - 例如：`S5B-3A` 相关改动优先落在 `S5B-...` 系列分支（如 `S5B-security-governance-hard-gates`）；
  - `S0D-2A` 这类 meta/docs/automation 改动优先落在 `S0D-...` 系列分支（如 `S0D-docs-management-v4`）。
- 如果一次 PR 同时涉及多个 scope/index（例如同时修改 `S5B-3A` 和 `S0D-2A`），建议拆成多条 PR：每条 PR 聚焦一个 scope/index 与对应分支，便于后续自动化按 scope 做聚合与回溯。

## Plan（draft）

### P1（实现：search 授权收口）

- P1-C1-S1：选定具体 search API（如 `GET /search/books`），梳理当前 call chain 与 tenant/role 过滤位置。
- P1-C1-S2：设计/实现统一的 search policy entrypoint（负责 tenant 边界 + 角色过滤），并改造 handler/usecase 只通过该入口做授权决策。
- P1-C1-S3：补齐/统一 search 相关 audit 写入点，确保 action/result/reason 落在 contract 中。

- P1-C2-S1：梳理 `GET /search` global search 的 call chain（router → SearchService/SearchPort → 各实体 search_*）、现有 tenant/role 过滤与错误处理路径。
- P1-C2-S2：为 global search 接入统一的 search policy entrypoint（可复用/扩展 `search_policy`），统一 `library_id` 与 `AuthContext.tenant_id` 的关系，并在聚合前就做 deny 判定。
- P1-C2-S3：在 global search 的 success/deny/error 出口补齐 audit 写入点（`action=search.global`），确保与 C1 同步满足 S5B-1A 的 action/result/reason 合同。

### P2（drill/verify：search tenant escape & coverage）

- P2-C1-S1：设计并实现 search drills runner `s5b4a_p2c1s1_drills_runner.py`，覆盖：
  - 本 tenant 正常搜索（预期 success，结果集只包含本 tenant 数据）；
  - 跨 tenant 搜索（预期 denied 或空结果，不能看到其他 tenant 资源）；
  - 角色不足的搜索（例如 member 不应看到 admin-only 结果）。
- P2-C1-S2：使用 S5B-1A verifier 验证 artifacts contract，首次跑出可用的 red/green evidence，并在 Evidence 区记录 headSha + run_dir。

- P2-C2-S1：在同一 suite 中新增针对 `GET /search` 的 global search drills case（例如 same-tenant/global、cross-tenant library_id、non-member/global），并扩展 `s5b4a_p2c1s1_drills_runner.py` 以一并产出 artifacts。
- P2-C2-S2：复用 S5B-1A verifier（`s5b1a_verify_artifacts.py`）验证包含 global search case 在内的 artifacts contract，并在 Evidence 区新增对应 headSha + run_dir 记录。

### P3（hard gate & wiring）

- P3-C1-S1：新增 hard gate 入口脚本（例如 `scripts/drills/s5b4a_p3c1s1_hard_gate.py` 或复用 S0D-2A shared hard gate），调用 search drills runner + verifier，并把 run 结果写入 `artifacts/s5b4a-runs.json`。
- P3-C1-S2：接一条 CI workflow（或接入现有 hard gate pipeline），在 search/policy/audit 相关改动时自动运行 search drills，并以 hard gate exit code 作为 CI 成功/失败依据。

## Execution Checklist

### P0（Contract）

- [x] `P0-C1-S1`：选定目标 search 链路 + action 命名
- [x] `P0-C1-S2`：search 授权 + audit contract 固化
- [x] `P0-C1-S3`：evidence/artifacts contract 明确（复用 S5B-1A/S5B-3A）

- [x] `P0-C2-S1`：锁定 global search 链路（GET /search）+ action 命名
- [x] `P0-C2-S2`：global search 授权 + audit contract 固化
- [x] `P0-C2-S3`：global search evidence/artifacts contract 明确（复用 S5B-1A/S5B-3A）

### P1（实现：search 授权收口）

- [x] `P1-C1-S1`：梳理现有 search call chain 与授权/tenant 过滤位置
- [x] `P1-C1-S2`：实现 search policy entrypoint 并改造调用方
- [x] `P1-C1-S3`：对齐 search audit 写入点的 action/result/reason 口径
  
- [x] `P1-C2-S1`：梳理 global search call chain 与授权/tenant 过滤位置
- [x] `P1-C2-S2`：为 GET /search 接入统一 search policy entrypoint
- [x] `P1-C2-S3`：补齐 global search 的 audit 写入点（action/result/reason 对齐）

### P2（drill/verify）

- [x] `P2-C1-S1`：实现 search drills runner 并覆盖关键场景
- [x] `P2-C1-S2`：通过 verifier 并记录首条 evidence（headSha + run_dir）

- [x] `P2-C2-S1`：设计并实现 global search drills（复用现有 runner）
- [x] `P2-C2-S2`：通过 verifier 跑通 global search drills 并记录 evidence

### P3（hard gate & wiring）

- [x] `P3-C1-S1`：实现 search hard gate 入口脚本 + artifacts 记账
- [ ] `P3-C1-S2`：接入 CI workflow 或记录不接入原因

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

### P2-C1-S1（blocks two-stage search drills 扩展矩阵：含未授权搜索 case｜2026-03-08）

- headSha：`03d81e68f2ad48ef4a09b3abb8a39f2e3f53c942`
- run_dir：`docs/labs/_snapshot/auto/S5B-4A/search_query_authorization/2fa7f2b4-5b18-42cf-a193-16be77cd7c09`
- suite：`search_query_authorization`，schema_version：`s5b-1a.result.v1`
- summary：`total=5, passed=4, failed=1, ok=false`
- 说明：在原有 4 个 green case 基础上新增 `unauthorized_missing_token`（缺少 Authorization header，仅携带 X-Library-Id）后，当前实现行为为 HTTP 200 + `search.blocks.two_stage` success 审计，与「匿名/缺 token 搜索不得绕过 AuthContext/tenant/membership 约束」的合同存在偏差；该 run 作为 P2-C1-S1 的扩展矩阵 red evidence 保留，用于后续 P1/P2/P3 收敛。

### P2-C1-S2（blocks two-stage search drills + verifier｜2026-03-08）

- headSha：`6ed7ad608a99793923e1744624e14f3dab6224be`
- run_dir：`docs/labs/_snapshot/auto/S5B-4A/search_query_authorization/ad0ba4d2-e456-4011-a0b9-bcbd388a0327`
- suite：`search_query_authorization`，schema_version：`s5b-1a.result.v1`
- summary：`total=4, passed=4, failed=0, ok=true`
- verifier：`python scripts/drills/s5b1a_verify_artifacts.py --run-dir docs/labs/_snapshot/auto/S5B-4A/search_query_authorization/ad0ba4d2-e456-4011-a0b9-bcbd388a0327`

### P2-C2-S2（blocks two-stage + global search drills（strict-auth）｜2026-03-08）

- headSha：`4ed956b90c09e18be882eac4cbe3888923444331`
- run_dir：`docs/labs/_snapshot/auto/S5B-4A/search_query_authorization/bf3e4f7e-2b17-43b7-be2c-80dd6e58b8ce`
- suite：`search_query_authorization`，schema_version：`s5b-1a.result.v1`
- summary：`total=8, passed=8, failed=0, ok=true`
- 说明：在引入 strict 版 AuthContext（缺少或非法 Authorization bearer token 一律 401，不再 fallback 到 dev user）后，覆盖 blocks two-stage + global search 的 8 个 case（含 missing-token）在 strict-auth API 实例上全部通过；其中 `unauthorized_missing_token` case 观察到 HTTP 401 且无 search 审计（`audit_expected=false`，`audit_rows.count=0`），标记为 P2-C2-S2 的 full green evidence，用于后续 P3 hard gate。


**P1-C1-S1（现状定位：blocks two-stage search 授权与 tenant 行为｜2026-03-08）**

- Call chain（今日形态）：
  - HTTP：`GET /search/blocks/two-stage`
  - Router：`search_router.search_blocks_two_stage`（[backend/api/app/modules/search/routers/search_router.py](backend/api/app/modules/search/routers/search_router.py#L73-L137) 一段及其后续定义）；
  - Infra：`PostgresSearchAdapter.search_block_hits_two_stage` → `TwoStageSearchService.search_block_hits` → search_index + blocks/tags SQL；
  - 数据来源：`SearchIndexModel`（[backend/infra/storage/search_repository_impl.py](backend/infra/storage/search_repository_impl.py#L1-L120)）+ 两阶段 join；
- AuthContext / 授权（缺口）：
  - 当前 router 只接收 `library_id`（可选）和 `book_id`，完全不依赖 `AuthContext` 或 membership/policy 模块；
  - 匿名请求或未认证请求，只要 `enable_search_projection=true` 且 DB 正常，就能对 `search_index` 做全文检索；
  - `library_id` 仅作为裸参数透传到 `SearchQuery.library_id`，没有与 tenant_id 进行任何比对或约束，也没有 role-based 行为差异；
  - search 模块内部没有使用现有的 `policy`/`AuthContext` helper，因此 search 结果的可见性完全由 SQL filter 决定。
- Tenant 行为（当前）：
  - two-stage 流程中，Stage1 依赖 `SearchIndexModel.library_id == query.library_id`（当传入时）；若不传 `library_id`，则不会做 tenant 过滤，而是跨 tenant 检索整个 index；
  - Stage2 中 blocks/tags join 的 SQL 会过滤软删除/已删除资源，但不会重新按 tenant 做强约束（tenant 隔离主要依赖 Stage1 的 library_id 条件）；
  - 这意味着：
    - 若调用方未传 `library_id`，或传入了其他 tenant 的 `library_id`，当前实现可能在 SQL 层返回跨 tenant 的 blocks 搜索结果；
    - 由于 search router 不知道 “当前用户的 tenant_id/roles”，无法在应用层做补救过滤。
- Audit / 可观测性（当前）：
  - router 仅通过 `logger.info` 记录 `event=search.blocks.two_stage.requested/returned` 之类的结构化日志（含 `q_preview/library_id/book_id/limit/candidate_limit/count`），但不写入 `audit_log`；
  - 日志中不包含 `actor_user_id/request_id/tenant_id`，即使从 log pipeline 中也难以可靠地做 per-tenant 或 per-actor 审计；
  - 错误处理路径中，仅在异常时写 `logger.error` 并返回 500 `"Two-stage search failed"`，同样没有审计记录。
- 小结（P1 输入）：
  - 这条 two-stage search 链路在「AuthContext + tenant 边界 + policy + audit」四个维度都几乎是“裸奔”的，仅靠 `library_id` 参数做了部分 SQL 过滤；
  - P1 改造的重点将是：
    - 在 router 层引入 `AuthContext` 并强约束 `library_id == ctx.tenant_id`；
    - 设计 search 专用的 policy entrypoint（决定是否允许执行 two-stage search、对哪些 tenant/角色开放）；
    - 在成功/deny/error 三类出口上写入符合 S5B-1A contract 的 audit 行，为后续 P2 drills 和 P3 hard gate 提供可验证的事实源。

## Recent changes（for traceability，可选）

- 2026-03-08：scaffold S5B-4A phase log（search query authorization + tenant isolation），尚未落地具体 search 链路与 drills。
 - 2026-03-08：补齐 P0 合同并完成 P1-C1-S1 现状梳理，锁定 `GET /search/blocks/two-stage` 作为本 phase 主链路。
 - 2026-03-08：完成 global search 合同与实现（P0-C2/P1-C2），并通过 strict-auth 环境下的 search_query_authorization drills 获得 8/8 绿的 P2-C2-S2 evidence。
