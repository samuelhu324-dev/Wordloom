# log-S6A-2A-unify-supply-creation（P2：Unify supply creation｜统一供给写入 outbox_events v1）

---

**id**: `S6A-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `unify scenario supply creation to outbox_events (projection-scoped) v1`
**status**: `stable`           # draft | stable | archived
**scope**: `S6`
**tags**: `EVOLUTION, Evidence, Drills, FailureContract, Scenarios, Outbox, Supply, epic/s6, sub/2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: `docs/runbook/run-S6A-evidence-drills-spine.md`
  **parent_log**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_1**: `docs/logs/log-S6A-1A-stable-entry-contract.md`
  **reference_log_2**: `docs/logs/log-S2B-3A-unified-consumer-framework.md`
  **reference_log_3**: `docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md`
**created**: `2026-03-05`
**updated**: `2026-03-05`

---

## Decision / Outcome（结论区）

**Decision（v1）**:

- 所有 drills/scenarios 的“供给创建（seed/insert/trigger）”默认写入 `outbox_events`（带 `projection`），避免出现“触发写旧表、消费读新表/反之”的漂移。
- 场景中仅描述 **要插入什么意图**（projection/entity/op/版本等），供给脚本/ helper 负责选择正确表结构与兼容字段。

## Problem（为什么要做）

- 现状常见风险：
  - 场景触发事件写到 legacy outbox 表，但 worker/consumer 读取的是 unified outbox（或相反），导致 drill 结果不可解释。
  - 迁移窗口中“供给与消费不一致”会让 verify 断言失真（看起来像 worker 坏了，实际上是 supply 打错了地方）。

## Constraints（约束）

- 不在场景里复制粘贴“插入 SQL”；优先提供一个稳定入口（脚本或 helper）统一处理。
- 不写入高基数 trace/log 信息到 DB/metrics 的 reason；供给侧只做最低限度字段。
- 兼容迁移窗口：如果 unified outbox 不存在/不可用，可显式 fallback，但必须写清楚 evidence（写入哪个表、为何 fallback）。

## Scope（本 log 范围）

- `P0`：明确 supply contract（默认写 `outbox_events` + projection）与 evidence 字段
- `P1`：将 `fault/obs_infra/*` 触发脚本与 verify 口径统一到 `outbox_events`
- `P2`：扩展到同类场景（例如 `shadow_verify_*` 中的供给/seed），减少“供给漂移”

## Success Criteria（DoD）

- `fault/obs_infra/*`：触发脚本默认写 `outbox_events`，并在 evidence 中明确：
  - `supply.target_table`、`supply.projection`、`supply.insert_count`
- verify 能在 DB 侧确认：事件确实进入 worker 读取的表（至少抽样校验 id/status）。
- 至少 1 份可追溯 evidence：headSha + 1 次 artifacts 路径（或 CI run URL）。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - 已形成“供给写入 contract v1”（unified-first：`outbox_events` + `projection`；缺表才 fallback legacy）
  - 已将同类场景（`shadow_verify_*`）供给写入收口到 shared helper（不再在场景里直写 INSERT SQL）
  - Evidence 区有可追溯的 headSha + artifacts 路径（本地 stage2 + window）

## P0（Contract｜v1）

### P0-C1-S1（Supply target contract｜v1）

- 默认写入 unified outbox：`outbox_events`
- 必须带 `projection`（例如：`search_index_to_elastic`）
- 仅当 unified 表缺失/不可用时允许 fallback legacy outbox（并在 evidence 中显式记录）

### P0-C1-S2（Evidence fields｜v1）

- `target_table`：实际写入的 outbox 表名
- `projection`：供给事件的 projection
- `insert_count`：本次插入事件数
- `fallback.used` / `fallback.reason`：是否 fallback + 原因
- `outbox_event_ids`：插入的事件 id（用于 verify 抽样或全量校验）

### P0-C1-S3（Supply DB check｜v1）

- verify 侧应能在 DB 中确认：对应 `outbox_event_ids` 确实存在于 worker 读取的 outbox 表
- 最小口径：`expected` vs `found`（例如 expected=200 found=200）并给出 `ok=true/false`

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S6A-2A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（completed）

- `P0`：Supply contract（默认写 outbox_events + projection）与 evidence 字段（已完成）
- `P1`：`fault/obs_infra/*` 触发脚本与 verify 口径对齐到 unified outbox（已完成）
- `P2`：同类场景（`shadow_verify_*`）供给写入统一收口到 shared helper（已完成）

## Execution Checklist（unchecked）

- [x] `P0-C1-S1`：Supply contract（默认写 outbox_events + projection）
- [x] `P0-C1-S2`：Evidence 字段最小集（supply target + 兼容/fallback 说明）
- [x] `P1-C1-S1`：迁移 `fault/obs_infra/*` 的 trigger/seed 逻辑到 unified outbox
- [x] `P1-C1-S2`：verify 对齐（DB 侧校验 supply 与消费一致）
- [x] `P1-C2-S1`：补 1 份可追溯运行态 evidence（本地 run+verify 一次 + artifacts 路径入账）
- [x] `P2-C1-S1`：同类场景（shadow_verify_*）的 seed/supply 统一

## Evidence（预留）

- 以 artifacts 为事实源；记录 headSha + 参数 + artifacts 路径（或 CI run URL）。
- code head: `bb462457`（commit messages 规范化后已重写 history；此为当前 head）
- note: 运行态 evidence 已入账（见下方 P2-C1-S1）。

### P2-C1-S1（shadow_verify_* 供给收口｜已补）

- 迁移点：将 shadow_verify 家族中“场景内直写 outbox SQL”的 enqueue 统一到 shared supply helper（优先 `outbox_events` + `projection`，仅在 unified 表缺失时 fallback legacy）。
- 涉及场景：
  - `shadow_verify_dual_run_stage2`（新增：`_supply.json` + result.meta 里附 `supply`/`supply_db_check`；并在写 unified 时强制 worker `OUTBOX_UNIFIED_READ_ENABLED`）
  - `shadow_verify_dual_run_window`（循环 enqueue 改用 helper；新增：`_supply.json` + result.meta 里附 `supply`/`supply_db_check`；并在写 unified 时强制 worker `OUTBOX_UNIFIED_READ_ENABLED`）
  - `shadow_verify_canary_dual_write`（改为 unified-first；新增：`_supply.json` + `supply_db_check`，且在 cleanup 前采样证据）
  - `shadow_verify_dual_write_sampling`（按 `entity_type` 分组 enqueue；新增：`_supply.json` + `supply_db_check`，且在 cleanup 前采样证据）

#### P2-C1-S1（本地 evidence：shadow_verify_dual_run_stage2｜2026-03-05）

- command：`python backend/scripts/cli.py labs shadow-verify-dual-run-stage2 --database-url postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_dev --es-url http://127.0.0.1:19200 --run-id s6a2a-p2c1s1-20260305-132816 --outdir artifacts/_tmp_s6a2a-p2c1s1-20260305-132816_shadow_verify_dual_run_stage2`
- artifacts：`artifacts/_tmp_s6a2a-p2c1s1-20260305-132816_shadow_verify_dual_run_stage2/`
- observed：
  - result：`ok=true`（strict parity）
  - supply：`target_table=outbox_events`、`projection=search_index_to_elastic`、`insert_count=20`、`fallback.used=false`
  - supply_db_check：`ok=true`（expected=20 found=20）
  - evidence files：`_result.json`、`_supply.json`、`_worker_start.json`、`worker.log`、`traces.json`

#### P2-C1-S1（本地 evidence｜C2：shadow_verify_dual_run_window｜2026-03-05）

- command：`python backend/scripts/cli.py labs shadow-verify-dual-run-window --database-url postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_dev --es-url http://127.0.0.1:19200 --run-id s6a2a-p2c1s1-c2-20260305-133359 --outdir artifacts/_tmp_s6a2a-p2c1s1-c2-20260305-133359_shadow_verify_dual_run_window`
- artifacts：`artifacts/_tmp_s6a2a-p2c1s1-c2-20260305-133359_shadow_verify_dual_run_window/`
- observed：
  - result：`ok=true`（strategy=`strict`）
  - supply：`target_table=outbox_events`、`projection=search_index_to_elastic`、`insert_count=200`、`fallback.used=false`
  - outbox：`enqueued_total=200`、`status_counts.done=200`
  - worker：`ok=true`（exit_code=1 runtime_s≈11.02）
  - parity：`compare.parity_ok=true`（PG vs ES ids）
  - supply_db_check：`ok=true`（expected=200 found=200）
  - evidence files：`_result.json`、`_supply.json`、`_worker_start.json`、`worker.log`

### P1-C2-S1（本地 evidence：跑 1 次 run+verify｜已补）

前置：准备一个可用的 env 文件（建议从 `backend/.env.test.example` 复制为 `.env.test`，并填入真实 `DATABASE_URL`；同时保证 ES/DB/OTLP infra 可用）。

最小命令（任选一个已迁移场景即可，例如 `es_down_connect`）：

- run：`python backend/scripts/cli.py labs run es_down_connect --env-file .env.test --run-id S6A-2A-P1-C2-S1`
- verify：`python backend/scripts/cli.py labs verify es_down_connect --run-id S6A-2A-P1-C2-S1`

入账：

- artifacts 路径：`docs/labs/_snapshot/auto/S3A-2A-3A/es_down_connect/S6A-2A-P1-C2-S1/`
- observed：
  - outbox_event_id：`9b20638b-546d-4e60-b44f-3b1d6aadb6be`
  - supply：`target_table=outbox_events`、`projection=search_index_to_elastic`、`insert_count=1`、`fallback.used=false`
  - verify：`supply_db_check.ok=true`（expected=1 found=1）
  - metrics delta：`retry_scheduled=+8`、`failed=+8`、`terminal_failed=+0`

## Notes（实施提示）

- 建议在 shared helper 或 `backend/scripts/labs/*` 中提供稳定供给入口，场景只调用它。
- 若遇到 schema 差异（列名/必填字段不同），应在供给层做兼容映射，而不是回流到每个 scenario。
- 本次本地 infra（用于 P2-C1-S1/C2）：`docker compose -f docker-compose.infra.yml up -d es`（ES: `http://127.0.0.1:19200`）
