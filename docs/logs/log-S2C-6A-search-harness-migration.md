# log-S2C-6A-search-harness-migration（Phase 6：Search outbox worker → projection harness）

---

**id**: `S2C-6A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `search harness migration (DB→ES; migrate search worker into projection harness)`
**status**: `draft`           # draft | stable | archived
**scope**: `S2C`
**tags**: `EVOLUTION, Projection, Platform, Framework, Outbox, Worker, Search, ES, epic/s2, sub/6`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S2C-projection-framework-platformization.md`
  **reference_log_1**: `docs/logs/log-S2B-3A-unified-consumer-framework.md` # outbox_core baseline
  **reference_log_2**: `docs/logs/log-S2C-1A-projection-spec-registry-harness.md` # harness core
  **reference_log_3**: `docs/logs/log-S2C-2A-projection-writer-template.md` # writer-template baseline
  **previous_log**: `docs/logs/log-S2C-5A-projection-backfill-template.md`
**created**: `2026-03-01`
**updated**: `2026-03-01`

---

## Decision / Outcome（结论区）

**Decision**:

- 本切片交付 `S2C Phase 6`：将 Search outbox worker（DB→ES）迁移到 projection harness。
- 由于该迁移涉及 ES 依赖与行为边界（bulk/index mapping/最终一致/失败重试策略），必须独立证据链与回滚说明，不与 backfill/rebuild/writer/drills 混交付。

## Constraints（约束）

- 不破坏路线 B 的稳定面：既有 stable entrypoints（scripts/runbooks/workflows）不随意改名；如需迁移，优先 shim。
- artifacts contract 保持不变（`_result.json` / snapshot bundle 为 SoT）。
- 不引入高基数 metrics labels；run_id/worker_id 只进日志与 artifacts。

## Scope（本 log 范围）

- `P0`：迁移 contract（harness 行为边界、ES 依赖、失败语义、回滚策略）
- `P1`：实现 Search projection 的 harness adapter（复用 outbox_core/harness 的 claim/lease/retry/reclaim/sanitize）
- `P2`：保持 stable entrypoint（脚本层 shim：旧 worker 入口继续可用，内部调用 harness）
- `P3`：drills + evidence（至少 N≥3 rounds；ES 环境依赖明确；记录 run URL / artifacts）

## Success Criteria（DoD）

- 代码层面：
  - Search 的消费主循环由 harness 驱动（claim → apply → mark_done/mark_retry/mark_failed）。
  - Search 的 apply 逻辑从脚本实现中抽离为可复用 adapter（并由 ProjectionSpec 注册）。
  - 旧脚本入口可继续运行（shim 或兼容 wrapper）。

- 证据层面：
  - 至少 1 个 ES-involved scenario 进入 catalog（requires.es=true），并产出可审计 artifacts。
  - 若迁移影响 outbox 行为/重试口径：至少 N≥3 rounds（与 S2B 口径一致）。

## P0（Migration contract｜v1）

- Projection: `search_index_to_elastic`
- SoT: `search_index`（DB）
- Sink: Elasticsearch index（ES）
- 失败语义：
  - apply 失败必须落入 outbox_core 的 reason taxonomy（低基数；可聚合）。
  - 可重试失败：按 backoff/retry/attempts；不可重试失败：mark_failed 并保留 error。
- 回滚策略：
  - harness migration 必须支持快速回退到旧 worker（通过 entrypoint shim 选择或 feature toggle）。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S2C-6A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P0（Contract）

- P0-S1：梳理 Search worker 现状（ES bulk、mapping/index lifecycle、失败分类）
- P0-S2：定义 harness migration 的最小 contract 与回滚面

### P1（Harness adapter）

- P1-S1：抽离 Search apply（输入 outbox row → ES side-effect）为 adapter
- P1-S2：将 `search_index_to_elastic` 接入 registry/harness（ProjectionSpec + adapter entrypoint）

### P2（Stable entrypoint shim）

- P2-S1：保留 `backend/scripts/search_outbox_worker_impl.py` 等稳定入口
- P2-S2：将旧入口内部改为调用 harness runner（必要时 subprocess 避免 nested event loop）

### P3（Evidence）

- P3-S1：新增 scenario（requires.es=true）并通过 guardrails
- P3-S2：跑证据入账（N≥3 rounds 或等价证明）

## Execution Checklist（unchecked）

### P0（Contract）

- [ ] `P0-C1-S1`：梳理 Search worker 行为边界与 ES 依赖
- [ ] `P0-C1-S2`：定义最小 contract + 回滚策略

### P1（Harness adapter）

- [ ] `P1-C1-S1`：抽离 Search apply 为 adapter
- [ ] `P1-C1-S2`：接入 ProjectionSpec/registry/harness

### P2（Stable entrypoint shim）

- [ ] `P2-C1-S1`：稳定入口保留（脚本路径不破坏）
- [ ] `P2-C1-S2`：shim 内部调用 harness runner

### P3（Evidence）

- [ ] `P3-C1-S1`：scenario 纳入 catalog + guardrails 校验通过
- [ ] `P3-C1-S2`：最小证据入账（N≥3 或等价证明）

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + run URL（如有）+ 关键参数。
- 本切片完成后，在此追加 Search harness migration 的证据记录。
