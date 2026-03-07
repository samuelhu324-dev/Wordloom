# log-S5B-security-governance-hard-gates（S5B：Security/Governance hard gates spine）

---

**id**: `S5B-security-governance-hard-gates`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `security & governance hard gates (policy/audit drills, contract enforcement) v1`
**status**: `stable`          # draft | stable | archived
**scope**: `S5`
**tags**: `EVOLUTION, Security, Governance, MultiTenant, Auth, Authorization, Policy, Audit, Drills, Evidence, HardGate, epic/s5, epic/s5b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **roadmap**: `docs/ROADMAP.md`
  **reference_log_1**: `docs/logs/log-S5A-security-governance.md`
  **reference_log_2**: `docs/logs/log-S5A-2A-library-membership-roles-policy-audit.md`
  **reference_log_3**: `docs/logs/log-S6A-4A-hard-gate-evidence-json.md` # hard-gate/evidence discipline baseline
  **phase_log_1**: `docs/logs/log-S5B-1A-policy-audit-hard-gate-drills.md`
  **phase_log_2**: `docs/logs/log-S5B-2A-policy-entrypoint-consolidation.md`
  **phase_log_3**: ``
**created**: `2026-03-06`
**updated**: `2026-03-07`

---

## Decision / Outcome（结论区）

**Decision**:

- 启动 `S5B` 作为 `S5` 下的下一轮 security/governance epic：目标是把 `AuthContext + policy + audit` 从“已落地但覆盖不均匀”推进到“可 hard-gate 的稳定骨架”，并能持续扩展。
- 交付策略：延续你在 S6A/S6A-4A 的做法——把“正确性”产品化为可机械判定的 drills/evidence（PASS/FAIL + artifacts contract），并在每个 phase log 里闭环记账。

**Default choices（默认基线 / v1）**:

- AuthN：JWT Bearer token（dev/test 允许 dev fallback，但必须可配置收紧）。
- Tenant：`tenant_id == library_id`。
- Policy：所有授权规则集中表达（policy functions / check entrypoint），禁止散落 if-else。
- Audit：append-only（只 INSERT），以 `request_id` 作为跨层关联键。
- Deny 语义：优先 404（防存在性泄露），但必须全局一致并可审计（result/reason 低基数）。

**Non-goals（不做什么）**:

- 不引入复杂 ACL/OPA/RLS（先 RBAC-lite + policy 收口）。
- 不把“线上身份接入（IdP/JWKS）”作为本轮必交付（可以作为后置 phase）。
- 不把高基数字段写入 metrics labels（run_id/request_id 只能进 logs/artifacts）。

## Background（背景）

- `S5A` 已经把 AuthContext/policy/audit 的 v1/v2 骨架跑通，并有 drills/evidence 的先例；但仓库中仍存在较多“旧式骨架”（例如 usecase 层仍传 `actor_user_id`、用 `enforce_owner_check` 走散落逻辑），导致：
  - 新增一个链路时容易复制/漂移；
  - deny reason 不可聚合或不可审计；
  - audit 覆盖与 request_id 贯穿不一致。
- `S5B` 的目标是把这件事再推进一轮：让“安全/多租户/审计”变成工程系统的稳定面（像投影/worker 一样可回归、可运营）。

## Constraints（约束）

- 先收口 contract，再做大范围迁移（避免全库扫荡式 refactor）。
- reason taxonomy 必须低基数（白名单），可在 metrics 和 audit 中聚合。
- drills 产物必须满足 artifacts contract（PASS/FAIL 可机械判定；关键输入/输出字段齐备）。
- 入口稳定面优先：如果已有 stable 脚本/路径，迁移用 shim，不随意改名。

## Scope（本 log 范围）

- 本 log 负责：
  - 定义 `S5B` 的默认基线、切片拆分、DoD 与 evidence 纪律。
  - 索引：链接到各 phase log（实现与证据）。
- 本 log 不负责：
  - 每个切片的具体实现细节与 evidence run（落在 phase logs + artifacts）。

## Success Criteria（DoD）

- 结构层面：
  - 读者 30 秒能定位：contract、当前进度、下一步与证据入口。
  - spine log 的 links 能导航到每个 phase log 的 evidence。

- 工程层面：
  - 至少 1 条关键链路（读/写/管理动作）完成：tenant 边界 + policy 收口 + audit 记录点一致化。
  - deny 的 reason 低基数、可聚合、可审计；并在测试/drills 中被验证。

- 证据层面：
  - 每个 phase 至少 1 条可追溯 evidence（headSha + artifacts 路径或 CI run URL）。
  - 至少 1 个 phase 具备 hard-gate 入口（可在 CI 反复运行）。

## Phases（切片）

- `S5B-1A`（Phase 1）：Policy/Audit hard-gate drills v1（把安全骨架变成可机械判定的回归包）
  - 详见：`docs/logs/log-S5B-1A-policy-audit-hard-gate-drills.md`

- `S5B-2A`（Phase 2）：Policy entrypoint consolidation（选 1 条关键链路，把散落 owner check 收口到 policy + tenant filter）
  - 详见：`docs/logs/log-S5B-2A-policy-entrypoint-consolidation.md`

- `S5B-3A`（Phase 3）：Audit coverage expansion + operator workflow（把 deny/allow 的审计覆盖扩展到关键写入，并固化 replay/forensics 流程）
  - 详见：`docs/logs/log-S5B-3A-<TBD>.md`

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`：contract/indexing（action/result/reason 口径；evidence schema；links/index）
- [x] `P1`：Phase 1（drills/evidence hard gate v1）
- [ ] `P2`：Phase 2（关键链路 policy 收口）
- [ ] `P3`：Phase 3（audit 扩展 + 运维可操作）

## Current Status（进展摘要）

- `S5B-1A` 已完成并标记为 stable：P0-P4 drills + verifier + CI hard gate workflow 已闭环。
- 下一步：启动 `S5B-2A`，选定 1 条关键链路把散落 owner check 收口到 policy + tenant filter，并补齐对应 drills/evidence。

## Evidence（S5B 记账）

- `S5B-1A`（Policy/Audit hard-gate drills v1）：
  - headSha：`de39d90e11c7a1479f22352b6b78c72109082695`
  - phase log：`docs/logs/log-S5B-1A-policy-audit-hard-gate-drills.md`
  - CI hard gate workflow：`.github/workflows/hard-gate-s5b1a-policy-audit.yml`

## Notes（落地原则）

- 优先让 drills/evidence “可复跑 + 可机械判定”，再扩大覆盖面。
- 永远不要把高基数字段写进 metrics label；若必须记录，写入结构化日志与 artifacts。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - `S5B` 的默认基线、phase 拆分与证据口径稳定。
  - 至少 `S5B-1A` 已具备可复跑的 hard-gate drills 入口，并且 Evidence 有可追溯记录。

## Recent changes（for traceability，可选）

- 2026-03-06：scaffold S5B spine log + Phase 1 log skeleton.
