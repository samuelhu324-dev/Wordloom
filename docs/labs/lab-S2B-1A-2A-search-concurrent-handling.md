# Lab-S2B-1A-2A：search concurrent handling

---

**id**: `S2B-1A-2A`
**kind**: `lab`               # log | lab | runbook | adr | note
**title**: `search concurrent handling`
**status**: `draft`           # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Search, Projection, lab, sub/2`
**links**: ``
  **issue**: `#56, #57`
  **pr**: ``
  **adr**: ``
  **runbook**: ``
**created**: `2026-02-18`
**updated**: `2026-02-18`

---

目标：给 Search 链路也补齐“影子验证（shadow verify）→ 证据（_result.json）”的最小闭环，为后续 read switch / provider switch / 合表提供可回滚、可核对的证据链。

本 lab 以 Postgres 侧投影为对账对象：

- SoT：`blocks`/`books`/`tags`（考虑软删除语义）
- 投影：`search_index`
- 观测补充：`search_outbox_events`（仅统计，不做一致性断言）

---

## 0) 前置条件

- 有可用 Postgres（本地/容器均可）
- 已完成 Alembic migrations（保证 `search_index` / `search_outbox_events` 存在）
- Search projector（EventBus handlers）至少跑过一轮
  - 若 SoT 有数据但 `search_index` 为空，本 lab 应该失败（这是预期信号）
- 说明：Search read 已为 merged-only（projection-backed Postgres）；不再提供 `SEARCH_MERGED_READ_ENABLED` / `SEARCH_STAGE1_PROVIDER` 回滚开关。

---

## 1) 执行方式

### 1.1 本地运行（推荐：稳定入口）

- 全量对账：
  - `python backend/scripts/cli.py labs shadow-verify-search-index --database-url "postgresql://..."`
- 限定单个 library：
  - `python backend/scripts/cli.py labs shadow-verify-search-index --database-url "postgresql://..." --library-id <uuid>`

默认输出目录：
- `docs/labs/_snapshot/auto/S2B-1A-2A/shadow_verify_search_index/<run_id>/_result.json`

---

## 2) 结果解释（验收口径）

### 2.1 Block

- `blocks_total`：满足口径的 SoT block 数（`blocks.soft_deleted_at IS NULL` 且其 book 未软删）
- `blocks_index_total`：`search_index` 中 `entity_type='block'` 的行数（library scope 时按 `library_id` 过滤）
- `blocks_missing`：SoT 有，但 `search_index` 缺失
- `blocks_extra`：`search_index` 有，但 SoT 不存在/已软删/其 book 不存在或已软删
- `blocks_mismatched_library_id`：`search_index.library_id` 与 `books.library_id` 不一致

### 2.2 Book

- `books_total`：`books.soft_deleted_at IS NULL`
- `books_index_total`：`search_index` 中 `entity_type='book'` 的行数（library scope 时按 `library_id` 过滤）
- `books_missing / books_extra / books_mismatched_library_id`：同上

### 2.3 Tag

Tags 在当前实现里不做 library 归属：

- `tags_total`：`tags.deleted_at IS NULL`
- `tags_index_total`：`search_index` 中 `entity_type='tag'` 的行数
- `tags_missing / tags_extra`：同上
- `tags_invalid_library_id`：tag 行不应带 `library_id`（应为 NULL）

### 2.4 Outbox（统计项，不参与 ok 判定）

- `outbox_total / outbox_pending / outbox_processing / outbox_done / outbox_failed`

判定：
- `missing/extra/mismatch/invalid` 全为 0 → 通过（exit 0）
- 否则 → 失败（exit 2）

---

## 3) 证据与关联位置

- 稳定 CLI 入口：`backend/scripts/cli.py`（`labs shadow-verify-search-index`）
- 投影写入实现：`backend/infra/search/search_indexer.py`
- 投影表模型：`backend/infra/database/models/search_index_models.py`
- Outbox 表模型：`backend/infra/database/models/search_outbox_models.py`

---

## 4) 常见失败与排查

- `*_missing > 0`：优先检查 projector 是否跑过 / 是否有消费延迟。
- `*_extra > 0`：检查软删除语义是否一致（SoT 已软删但 search_index 未删除）。
- `*_mismatched_library_id > 0`：检查 `search_indexer._get_library_id_for_book()` 与历史数据回填是否一致。
