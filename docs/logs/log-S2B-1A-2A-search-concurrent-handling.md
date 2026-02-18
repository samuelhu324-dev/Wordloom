# Log-S2B-1A-2A: shadow/search concurrent handling

---

**id**: `S2B-1A-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `shadow/concurrent handling`
**status**: `stable`          # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Projection, Search, sub/2`
**links**: ``
  **issue**: `#56, #57`
  **pr**: ``
  **adr**: ``
  **runbook**: ``
**created**: `2026-02-17`
**updated**: `2026-02-18`

---

## Decision / Outcome（结论区）

**Decision**:

- 把 Chronicle 已跑通的“影子验证 → 可回滚切读 → 证据链（artifacts）”模式复制到 Search 链路，先做 shadow verify 和 read switch，最后才进入真正的“合表/替换”。
- Search 的切读开关不复用 Chronicle 的 `MERGED_READ_ENABLED`，避免之后出现“到底切的是哪条链路”的混淆；建议单独引入 `SEARCH_MERGED_READ_ENABLED`（命名仅示意）。
- Search 的 shadow verify 默认先做“最小有用口径”（counts / missing / extra / 关键字段一致性），并允许“部分成功（partial）”的统计，因为 ES bulk/item 级失败是常态。

**Drivers**:

- Search 往往更早遇到“并发/重试/部分失败”的现实，缺少统一验证口径会导致无法安全切读/切写。
- 沿用 Chronicle 的证据链（summary/logs/zip）可以把讨论从“感觉对不对”变成“证据对不对”。

**Non-goals**:

- 不在此 log 内直接决定 Search 一定走 Replace（A）还是 Derived（B）；目标是把“可回滚的影子切换”先建立起来。
- 不在此处展开 ES mapping、索引别名切换、回填/重建策略细节（后续 ADR / runbook 补齐）。

**Success criteria（DoD）**:

- Search 链路具备独立的 read switch（默认 off，on 可回滚），且 `off` 时不影响现有测试/冒烟。
- Search shadow verify 能在本地/CI 重复执行并产出 artifacts（失败时能解释原因并可追溯）。
- 验证口径至少覆盖：counts、missing/extra、关键幂等键（例如 outbox_event_id / entity_id）一致性。

**Current status（现状）**:

- ✅ Chronicle 已完成样板闭环（read switch + shadow verify + Actions artifacts）。
- ✅ Search shadow verify v0 已落地（script + stable CLI，产出 `_result.json`）。
- ✅ Search read switch 已落地（独立 `SEARCH_MERGED_READ_ENABLED`，默认 off，可回滚）。

**Evidence（代码证据 / 参考实现）**:

- Chronicle 样板 log：`docs/logs/log-S2B-1A-1A-chronicle-concurrent-handling.md`
- Chronicle CI workflow（证据链样板）：`.github/workflows/drill-shadow-verify-entries.yml`
- Search worker（现状入口，后续 verify/观测会围绕它）：`backend/scripts/legacy/search_outbox_worker.py`
- Search shadow verify（v0, script）：`backend/scripts/labs/lab-S2B-1A-2A.py`
- Search shadow verify（stable CLI）：`backend/scripts/cli.py`（`labs shadow-verify-search-index`）
- Search lab manual：`docs/labs/lab-S2B-1A-2A-search-concurrent-handling.md`

Registry:

- `docs/labs/INDEX.md`

## Background

Search 的“并发/一致性”问题常见来源包括：

- outbox 重试导致重复投递
- ES bulk 部分失败（item 级失败）
- 索引切换/回填期间读写并发

因此在进入“合表/替换”之前，需要先把 Search 链路也升级到可治理的 Dual-run：先影子、再切读、最后切写。

## Problem / Malfunction

- 缺少统一 shadow verify 口径，会导致无法判断“新链路是否可用”，切读风险不可控。
- 复用同一个开关会造成链路间耦合与排障困难（Chronicle/Search 无法独立推进）。
- ES 的部分失败若不被显式计入验证与证据链，会被误判为“偶发”而长期积累技术债。

## What/How to do（落地规则）

### 0) 默认最小方案（先影子、再切读）

- 写路径：先不双写（避免幂等/回滚复杂度），优先 shadow read / shadow projection
- 读路径：在 DAO/Repository 层切读（最可控，回滚简单）
- 验证：先最小口径（counts/missing/extra/幂等键一致性），再逐步加字段/排序/分页稳定性

### 1) Search read switch（建议）

- 引入独立开关（命名示意）：`SEARCH_MERGED_READ_ENABLED=0/1`
- `off`：读旧路径
- `on`：读新路径（或“新优先、缺失回退旧”）
- 回滚：一键关开关

### 2) Search shadow verify（建议口径）

最小口径（v0）：

- counts：按全量 +（可选）按 book/library 分桶
- missing：source-of-truth 有，但 search view 没有
- extra：search view 有，但 source-of-truth 没有
- 幂等键一致性：以 outbox_event_id / entity_id 为主键的唯一性与对应关系

关于 ES partial：

- verify 输出应显式包含“部分失败”计数（例如 bulk item failure count），避免把问题埋进 logs。

### 3) 证据链（Actions artifacts）

沿用 Chronicle 规则：

- 成功：仅上传 `artifacts/summary.json`
- 失败：上传 `artifacts.zip`（包含 `summary.json/logs.txt/traces.json`）并 fail job

## Next

- 补齐 Search 的 read-only read-side adapter（避免误用写路径）。
- 引入 Search 独立 read flag，并加最小 wiring test。
- 落地 Search shadow verify v0（脚本/CLI 任一形式均可），接入 CI artifacts。

## Acceptance checklist（验收清单，可直接勾）

- [x] Search 有独立读开关（不复用 Chronicle 的 `MERGED_READ_ENABLED`）。
- [x] `SEARCH_MERGED_READ_ENABLED=0` 时：全量测试/冒烟不受影响。
- [x] `SEARCH_MERGED_READ_ENABLED=1` 时：至少一个入口切到新读且可回滚。
- [x] shadow verify 输出至少包含：`counts / missing / extra / key-mismatch(or duplicate)`。
- [x] shadow verify 在 CI 中产出 artifacts，成功仅上传 summary，失败上传 zip 并 fail job。

## References

- `docs/logs/log-S2B-1A-1A-chronicle-concurrent-handling.md`
- `docs/logs/log-S2B-1A-failure-contract-v1.md`