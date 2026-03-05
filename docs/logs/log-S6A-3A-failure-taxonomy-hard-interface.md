# log-S6A-3A-failure-taxonomy-hard-interface（P3：Failure taxonomy hard interface｜reason = contract v1）

---

**id**: `S6A-3A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `failure taxonomy hard interface (reason = contract across DB + metrics + verify) v1`
**status**: `stable`           # draft | stable | archived
**scope**: `S6`
**tags**: `EVOLUTION, Evidence, Drills, FailureContract, ReasonTaxonomy, Metrics, Verification, epic/s6, sub/3a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **previous_log**: `docs/logs/log-S6A-2A-unify-supply-creation.md`
  **reference_log_1**: `docs/logs/log-S2B-3A-unified-consumer-framework.md`
  **reference_log_2**: `docs/logs/log-S2B-2A-failure-contract-v2.md`
  **reference_log_3**: `docs/logs/log-S3A-2A-3B-automated-failure-drills.md`
**created**: `2026-03-05`
**updated**: `2026-03-05`

---

## Decision / Outcome（结论区）

**Decision（v1）**:

- 将 `error_reason`（DB）与 Prometheus metrics 的 `reason` label 视为同一套“硬接口 contract”（低基数、可聚合、可被 verify 断言）。
- drills/verify 不再把 reason 当作“日志字符串”，而是：用一组稳定枚举/族（family）来断言 expected vs observed。

**Default choices（本 phase 默认决策 / v1）**:

- 默认以“reason family”组织断言（例如：transport、timeout、rate_limit、auth、schema、unknown）。
- 禁止把高基数信息（URL/stacktrace/UUID/tenant id/自由文本）写入 reason；高基数信息只存在 logs/artifacts。

## Definitions（概念定义，可选）

- `error_reason`：DB 侧记录失败原因的字段（应低基数，可聚合）。
- `reason`（metrics label）：Prometheus 指标的 reason 维度（应与 DB reason 同源/同族）。
- `reason family`：reason 的上层族/类别，用于 drills/verify 的稳定断言。

## Constraints（约束）

- reason 必须低基数：禁止把高基数字符串写入 DB reason 或 metrics labels。
- verify 必须机器可判定：PASS/FAIL 以 evidence JSON / DB 查询 / metrics delta 为准。
- 变更必须可回滚：reason contract 的引入不能打断既有 drills（允许兼容窗口）。

## Scope（本 log 范围）

- `P0`：contract（reason 命名、family、禁止项、证据口径）
- `P1`：实现/对齐（DB + metrics 产出同源 reason；verify 读取统一口径）
- `P2`：drills：在至少 1 个 `fault/obs_infra/*` 场景中形成闭环（expected reasons vs observed reasons）
- `P3`：hardening：兼容窗口/回滚策略/CI hard gate 的最小实现

## Success Criteria（DoD）

- reason taxonomy v1 可被写入并被 verify 断言：
  - metrics 侧 reason 维度可聚合（低基数）
  - DB 侧 error_reason 可聚合（低基数）
  - drills evidence JSON 能输出 expected vs observed 的 reason 分布（或 family 分布）
- 至少 1 个场景在本地或 CI 跑通并产出可追溯 evidence：headSha + artifacts 路径（或 CI run URL）。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - P0 contract（reason/family/禁止项）已定稿
  - P1–P2 至少 1 个场景形成闭环：DB + metrics + verify 对齐
  - Evidence 区包含可追溯 headSha + artifacts 路径（或 CI run URL）

## P0（Contract｜v1）

### P0-C1-S1（Reason taxonomy｜v1）

- 为 drills/verify 提供一组稳定 reason family（供断言使用）。
- 对外 contract 面：verify 默认使用 family 断言；reason 细分可作为可选输出。

### P0-C1-S2（Low-cardinality rules｜v1）

- reason 中禁止出现：
  - URL / host / path / query
  - stacktrace 片段
  - UUID / request id / tenant id / trace id
  - 自由文本拼接

### P0-C1-S3（Evidence contract｜v1）

- evidence JSON（最小集）应包含：
  - inputs：scenario、run_id、关键 knobs（可选）
  - outputs：artifacts 路径 + `_result.json` 路径
  - expected：预期 reason family（或分布）
  - observed：观测到的 reason family（或分布）
  - pass/fail：机器可判定字段

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S6A-3A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P1（实现：reason 同源 + verify 读取）

- P1-C1-S1：梳理现有 reason 产出点（DB/metrics），收口到同源 mapping
- P1-C1-S2：verify 读取 reason 并输出结构化统计（family 优先）

**P1 implementation notes（落实点 / v1）**:

- 同源产出：worker 在同一个异常上生成 `reason`（用于 metrics label）并写入 DB `error_reason`（用于聚合与 verify）。
- family 断言：drills/verify 通过 `reason_family_v1()` 将 reason 映射到稳定 family，再做 expected vs observed 的机器断言。
- evidence 口径：每个场景的 `_result.json` 输出 `reason_contract.expected` 与 `reason_contract.observed`（family 优先）。

### P2（drills：闭环样板）

- P2-C1-S1：选择 1 个 `fault/obs_infra/*` 场景，定义 expected reasons（family）
- P2-C1-S2：跑 1 次 run+verify，输出 evidence JSON 并能 PASS/FAIL
- P2-C2-S1：扩展到第 2 个 `fault/obs_infra/*` 场景（`es_429_inject`），补齐 expected reason family
- P2-C2-S2：修复注入 429 时的异常分类崩溃，保证场景可稳定跑通
- P2-C2-S3：跑 1 次 run+verify，输出第 2 份可追溯 evidence（headSha + artifacts）
- P2-C3-S1：扩展到第 3 个 `fault/obs_infra/*` 场景（`es_write_block_4xx`），覆盖 `client` family
- P2-C3-S2：跑 1 次 run+verify，输出第 3 份可追溯 evidence（headSha + artifacts）

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：Reason taxonomy（family 优先）
- [x] `P0-C1-S2`：Low-cardinality rules（禁止项）
- [x] `P0-C1-S3`：Evidence contract（expected vs observed）

### P1（实现）

- [x] `P1-C1-S1`：reason 同源 mapping
- [x] `P1-C1-S2`：verify 输出 reason 统计（family）

### P2（drills）

- [x] `P2-C1-S1`：选定样板场景 + expected reason family
- [x] `P2-C1-S2`：产出 1 份可追溯 evidence（headSha + artifacts）
- [x] `P2-C2-S1`：扩展第二个样板场景（es_429_inject）+ expected reason family
- [x] `P2-C2-S2`：修复 es_429 注入路径崩溃（exception classification）
- [x] `P2-C2-S3`：产出第 2 份可追溯 evidence（headSha + artifacts）
- [x] `P2-C3-S1`：扩展第三个样板场景（es_write_block_4xx）+ expected reason family
- [x] `P2-C3-S2`：产出第 3 份可追溯 evidence（headSha + artifacts）

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

### P2-C1-S2（fault/obs_infra/es_down_connect｜2026-03-05）

- headSha：`d208c767`（S6A-3A/P2: reason contract evidence v1）
- run_id：`s6a3a-p2c1s1-20260305-142816`
- artifacts：`docs/labs/_snapshot/auto/S3A-2A-3A/es_down_connect/s6a3a-p2c1s1-20260305-142816/`
- expected：
  - metrics reasons ⊆ {`es_connect`, `es_unreachable`}
  - reason family ⊆ {`transport`}
- observed：
  - metrics delta（reason=es_connect|es_unreachable）：
    - retry_scheduled: `+9`
    - failed: `+9`
    - terminal_failed: `+0`
  - DB error_reason（outbox_events）：
    - `es_connect`（family=`transport`）

### P2-C2-S3（fault/obs_infra/es_429_inject｜2026-03-05）

- headSha：`ea407543`（S6A-3A/P2-C2: es_429 reason contract evidence v1）
- run_id：`s6a3a-p2c2s3-20260305-143920`
- artifacts：`docs/labs/_snapshot/auto/S3A-2A-3A/es_429_inject/s6a3a-p2c2s3-20260305-143920/`
- expected：
  - metrics reasons ⊆ {`es_429`}
  - reason family ⊆ {`rate_limit`}
- observed：
  - metrics delta（reason=es_429）：
    - retry_scheduled: `+9`
    - failed: `+9`
    - terminal_failed: `+0`
  - DB error_reason（outbox_events）：
    - `es_429`（family=`rate_limit`）

### P2-C3-S2（fault/obs_infra/es_write_block_4xx｜2026-03-05）

- headSha：`5b03d039`（S6A-3A/P2-C3: es_4xx reason contract evidence v1）
- run_id：`s6a3a-p2c3s2-20260305-144820`
- artifacts：`docs/labs/_snapshot/auto/S3A-2A-3A/es_write_block_4xx/s6a3a-p2c3s2-20260305-144820/`
- expected：
  - metrics reasons ⊆ {`es_4xx`}
  - reason family ⊆ {`client`}
- observed：
  - metrics delta（reason=es_4xx）：
    - failed: `+1`
    - retry_scheduled: `+0`
  - DB error_reason（outbox_events）：
    - `es_4xx`（family=`client`）
