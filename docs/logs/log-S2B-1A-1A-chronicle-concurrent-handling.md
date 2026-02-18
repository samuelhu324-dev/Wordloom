# Log-S2B-1A-1A: shadow/chronicle concurrent handling

---

**id**: `S2B-1A-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `shadow/concurrent handling`
**status**: `draft`          # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Chronicle, Projection, sub/2`
**links**: ``
  **issue**: `#56, #57`
  **pr**: ``
  **adr**: ``
  **runbook**: ``
**created**: `2026-02-15`
**updated**: `2026-02-17`

---

## Decision / Outcome（结论区）

**Decision**:

- 在开始 Dual-run（新旧并行）前，先把“并行到底怎么并行”说清楚：新表是什么、在哪里切读、要不要双写、怎么验。
- 默认采用一个最小可落地方案先开工：新 merged 表先做“新 schema/新表”（不立刻替换旧表）；读路径优先在 DAO/Repository 层切；写路径先不双写（先做 shadow read / shadow projection）。
- 用开关把读切换做成可回滚：`MERGED_READ_ENABLED=0/1`。

**Drivers**:

- Dual-run 如果只是一句口号，会出现“跑了半天也不知道谁在读、谁在写、结果怎么验”，无法形成证据与可交接结论。
- 早期让 Grafana/SQL 直接读新表会制造“两套真相”，对不上账且难排障。
- 双写会引入一致性与幂等问题，默认先用 shadow 降低风险。

**Non-goals**:

- 这份 log 不替你一次性拍板最终一定走 Replace（A）还是 Derived（B）；它的目标是让你能先安全开工并保留回滚空间。
- 不在此处展开具体表结构/字段映射细节（那是后续合表设计与迁移脚本的内容）。

**Success criteria（DoD）**:

- Dual-run 前的三件事有明确答案并落到文档/配置：新表类型（A/B/C）、读切换点、写策略（shadow/dual-write）与验证方式。
- `MERGED_READ_ENABLED=0` 时全量测试/冒烟不受影响；开启后能切换到新读且可一键回退。
- shadow 验证能产出对账证据（counts/排序/关键字段/分页稳定性等），并能写入可追溯 artifacts。

**Current status（现状）**:

- ✅ Read switch 已实现且有测试覆盖：通过 `MERGED_READ_ENABLED=0/1` 在 DI 层切换 Chronicle Query Service 的 read-repo。
- ✅ entries 读库已实现为 read-only adapter（避免误用写路径）。
- ✅ shadow verify 已提供最小可重复脚本（count + missing rows，对不上直接非 0 退出）。
- ✅ CI artifacts（GitHub Actions）已接入：每次 drill 生成 `artifacts/summary.json + logs.txt + traces.json` 并统一上传；成功仅上传 summary，失败上传完整 zip。

**Evidence（代码证据）**:

- Read switch（DI 层切读）：`backend/api/app/dependencies_real.py`（`get_chronicle_query_service`）
- Flag → settings：`backend/api/app/config/setting.py`（`merged_read_enabled`）
- Flag wiring test：`backend/api/app/tests/test_chronicle/test_merged_read_flag.py`
- Read-side adapter（entries read-only）：`backend/infra/storage/chronicle_entries_repository_impl.py`
- Shadow verify script：`backend/scripts/labs/lab-S2B-1A-1A.py`
- CI workflow：`.github/workflows/drill-shadow-verify-entries.yml`

Registry:

- `docs/labs/INDEX.md`

## Background

你这张图的意思是：在你开始“Dual-run（新旧并行）”之前，必须先把“并行到底怎么并行”说清楚。不然 Dual-run 会变成一句口号：跑了半天也不知道谁在读、谁在写、结果怎么验。

我把它翻译成“你接下来该怎么操作”的清单（按你现在 Wordloom 的 outbox/projection/合表语境）。

## Problem / Malfunction

- 并行策略不明确会导致：无法定义“新旧结果一致性”的验证口径，最终无法切读/切写。
- 读切换点选错（例如早期让 Grafana/SQL 直连新表）会制造两套真相。
- 双写在没有幂等键/回滚策略/冲突规则时容易翻车。

## What/How to do（落地规则）

### 0) 一个最小可落地的默认方案（不纠结也能开工）

如果你现在只想赶紧推进而不想卡在设计上，默认选：

- 新 merged 表：先做新 schema/新表（不要立刻替换旧表）
- 读路径切换点：先在 DAO/Repository（查询服务）切（API/UI 仍然走同一个 query 接口）
- 写路径：先不双写（只做“新读影子”或“新投影影子”），等验证稳了再谈双写

对应迁移节奏：先影子跑、再切读、最后切写。

### 1) 信息 #1：新 merged 表到底是什么？（A/B/C 三选一）

你要从下面三选一（操作方式完全不同）：

**A. 新表替换旧表（Replace）**

- 含义：旧表将被新表完全取代（最终会删旧表）。
- 怎么做：新建表 → backfill → 双写一段时间 → 切读 → 切写 → 下线旧表。

**B. 新表是“物化/快照表”（Materialized / Derived）**

- 含义：新表不是主数据，只是为了更快查询/聚合。
- 怎么做：保持旧表为 SoT，新表由 worker/SQL job 生成；切读只影响查询，不影响写。

**C. 新表只是“视图/兼容层”（View / Compatibility）**

- 含义：你不想动太多代码，让新旧统一成一个接口。
- 怎么做：用 SQL VIEW 或 DAO 组合查询把两边包装成一个“看起来像 merged 的表”。

你现在“要合表”通常更像 A 或 B；如果你怕炸，先用 B（衍生表）更安全。

### 2) 信息 #2：读路径切换点在哪里？（从低风险到高风险）

**最推荐（可控）：DAO/Repository 层切**

- 操作：加一个开关 `MERGED_READ_ENABLED`
- `off`：DAO 读旧表
- `on`：DAO 读新表（或读新表优先，缺失回退旧表）
- 优点：API/UI 不动，runbook/观测入口稳定。

**次推荐：查询服务层切（Query Service）**

- 操作：Query Service 按场景选择数据源（旧/新/混合）。
- 优点：规则集中；缺点：如果 Query Service 写得很胖，会变难测。

**不推荐（早期）：直接让 Grafana/SQL 读新表**

- 优点：快；缺点：你会得到“两套真相”，很快对不上账。

### 3) 信息 #3：写路径是否允许双写？（Dual-run 最易翻车点）

双写不是“多写一份”这么简单，它会引入一致性问题。你要先回答：写入事件/事务是否有稳定 idempotency key（幂等键）？例如：

- `outbox_event_id` 稳定唯一
- 处理端 upsert 按 `event_id` 幂等
- 重放不会产生重复副作用

**选择 1：不双写（Shadow read / Shadow projection）**

- 操作：写仍然只有旧链路；新链路在旁边“自己跑”，只用于对比验证。
- 优点：最安全；缺点：覆盖面慢一点。

**选择 2：双写（Dual-write）**

- 操作：同一份输入同时驱动旧表 & 新表。
- 必须具备：幂等键、可回滚策略、清晰的冲突解决（以谁为准）。

你现在已经有 outbox + replay + 幂等 upsert 的思路，所以“可以做双写”，但默认仍建议：先不双写，先影子跑通。

### 4) 把三点落成“你今天就能做的任务”（可直接开工）

**Task 1：写一个 10 行的 Decision Note（放 ADR 或 log）**

- merged 表类型：A/B/C
- 读切换点：DAO / Query Service
- 写策略：shadow / dual-write
- 验证方式：对比哪些字段/哪些指标（你已有 golden fixtures 思路）

**Task 2：加一个读开关（最小代码改动）**

- `MERGED_READ_ENABLED=0/1`
- DAO 里：`if enabled: read_new else: read_old`
- 先让 `enabled=0` 跑全量测试，确保没影响

**Task 3：做“影子验证”而不是全系统切换**

- 新表先 backfill 一份（或者新 projection 重建一份）
- 跑 labs 的验证脚本：条数、排序、关键字段、分页稳定性（你实验 2/4 那套）
- 结果写入 artifacts（你现在 Actions 已经通了）

**Task 4：切读（只切一个入口）**

- 只切一个 query（例如某个 list API）
- 出问题立刻把开关关掉回退

### 5) 一句话总结

这段话不是让你“想很多”，而是要你在 Dual-run 前决定：新表是什么、在哪里切读、要不要双写。决定了，Step A/B/C 才能落到具体文件、模块、脚本和迁移节奏。

你现在最稳的落地路径：新表先做衍生/影子（B）→ DAO 切读 → 不双写 → 用 labs+Actions 做对账 → 稳了再考虑双写/替换（A）。

## Next

- 把 Task 1 的 Decision Note 写出来并固化为“唯一事实源”（后续切读/切写都以此为准）。
- 选定一个最小 read-switch 入口（一个 DAO 方法/一个 list query），实现 `MERGED_READ_ENABLED` 并跑全量测试。
- 选定一套 shadow 对账口径（counts/排序/关键字段/分页稳定性）并接入 Actions artifacts 输出。

## Acceptance checklist（验收清单，可直接勾）

- [ ] `MERGED_READ_ENABLED` 默认关闭时：`ChronicleQueryService` 使用 events repo（见 `test_chronicle_query_service_uses_events_repo_by_default`）。
- [ ] `MERGED_READ_ENABLED=1` 开启时：`ChronicleQueryService` 使用 entries repo（见 `test_chronicle_query_service_uses_entries_repo_when_enabled`）。
- [ ] entries repo 为 read-only（写入会抛出明确异常），避免误把 read-side 当成 SoT。
- [ ] shadow verify 脚本可在本地/容器运行并产生可审计输出：
  - 输出包含 `events_total / entries_total / missing_entries / extra_entries / mismatched_book_id`
  - 任一不为 0 时退出码非 0（当前为 2）

## References

- `docs/logs/log-S2B-1A-failure-contract-v1.md`（Failure Contract v1：稳定对外语义与证据链）
- `docs/logs/log-S2B-projection-table-merge.md`（合表/合 projection 相关上下文）