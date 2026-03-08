# log-<ID>（Phase <n>：<切片标题>）

---

**id**: `<ID>`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `<一句话标题：交付物 + drills/evidence + v1>`
**status**: `draft`           # draft | stable | archived
**scope**: `<Sx>`
**tags**: `EVOLUTION, <domain>, Drills, Evidence, epic/<sx>, sub/<phase>`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-<PARENT>.md`
  **previous_log**: ``
  **reference_log_1**: ``
**created**: `YYYY-MM-DD`
**updated**: `YYYY-MM-DD`

---

## Decision / Outcome（结论区）

**Decision**:

- <本 phase 的核心交付是什么>
- <默认做法/默认语义>

**Default choices（本 phase 默认决策 / v1）**（可选，但建议写）:

- <例如：dev/test 先；不引入生产级复杂度；不入 git 的产物；证据 JSON 字段>

## Definitions（概念定义，可选）

- <关键术语 3~10 条，避免读者猜>

## Constraints（约束）

- <例如：dump 不入 git；最小权限；reason 低基数；证据机器可判定>

## Scope（本 log 范围）

- `P0`：contract（默认决策、命名/字段、证据口径）
- `P1`：<实现/infra/脚本>
- `P2`：<drill/verify>
- `P3`：<drill/verify>
- （可选）`P4`：<单命令 pipeline / hard gate>

## Success Criteria（DoD）

- <列 4~10 条可验收标准，尽量能靠 evidence JSON / SQL / metrics 判定>

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - <P0-Pn 的 contract + 入口脚本 + drills 已跑通>
  - Evidence 区有可追溯的 `headSha` + artifacts 路径（或 CI run URL）

## P0（Contract｜v1）

### P0-C1-S1（<contract 子项 1>）

- <命名/字段/语义/约束>

### P0-C1-S2（<contract 子项 2>）

- <命名/字段/语义/约束>

### P0-C1-S3（证据口径 contract｜v1）

- evidence JSON 必须包含：
  - <输入参数>
  - <输出产物路径>
  - <PASS/FAIL 可判定字段>

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`，即 `...-S1`），也可以是在同一 phase / cycle 下连续的多个 step 合并（如 `1S2`，即 `...-S1S2`）。

**Branch 约定**:

- 对应 scope/index 的 log（例如 `S5B-3A` 隶属于 `S5B`，`S0D-2A` 隶属于 `S0D`）优先在同名前缀的工作分支上推进 P* 的代码与文档变更：
  - 例如：`S5B-3A` 相关改动优先落在 `S5B-...` 系列分支（如 `S5B-security-governance-hard-gates`）；
  - `S0D-2A` 这类 meta/docs/automation 改动优先落在 `S0D-...` 系列分支（如 `S0D-docs-management-v4`）。
- 如果一次 PR 同时涉及多个 scope/index（例如同时修改 `S5B-3A` 和 `S0D-2A`），建议拆成多条 PR：每条 PR 聚焦一个 scope/index 与对应分支，便于后续自动化按 scope 做聚合与回溯。

**Commit 纪律（建议）**:

- 每完成一个 `P*-C*-S*` 的实质内容（无论是合同、实现，还是 drills/evidence），应尽量在对应 scope 的工作分支上及时 `commit/push`：
  - 例如：`S5B-4A` 相关改动默认落在 `S5B-security-governance-hard-gates` 这类 `S5B-*` 顶层分支上；
  - 若某个 phase 体量特别大或多人协作，可在 `S5B-*` 之下再开短生命周期子分支，但默认不必为每个 log 单独起分支。
- 正常节奏是：在对应 scope 分支上按 `P*-C*-S*` 粒度累积 commit → 定期从该分支向 `main` 提交 PR，由人工 Review/合并。

## Plan（draft）

### P1（<实现>）

- P1-C1-S1：...
- P1-C1-S2：...

### P2（<drill/verify>）

- P2-C1-S1：...
- P2-C1-S2：...

## Execution Checklist（unchecked）

### P0（Contract）

- [ ] `P0-C1-S1`：...
- [ ] `P0-C1-S2`：...
- [ ] `P0-C1-S3`：...

### P1（...）

- [ ] `P1-C1-S1`：...
- [ ] `P1-C1-S2`：...

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

### <Pn-Cx-Sy>（<drill 名称>｜YYYY-MM-DD）

- headSha：`<git sha>`
- artifacts：`artifacts/_tmp_<...>/drills_<ts>.json`
- env（示例，可选）：
  - `<ENV>=<...>`
- 期望（expected）：
  - ...
- 观测（observed）：
  - ...

## Recent changes（for traceability，可选）

- YYYY-MM-DD：<发生了什么变更，为什么要记录，如何追溯>
