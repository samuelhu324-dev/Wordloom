# log-S2B-5A-table-merge-migration-v2（Search closure：cutover + deprecate window）

---

**id**: `S2B-5A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `table merge migration (Phase 2: Search cutover + deprecate window closure)`
**status**: `stable`          # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Search, Projection, TableMerge, epic/s2, sub/5`
**links**: ``
  **adr**: `docs/adr/adr-S2B-projection-table-merge.md`
  **runbook**: `docs/runbook/run-S2B-projection-table-merge.md`
  **sibling_log**: `docs/logs/log-S2B-4A-table-merge-migration.md` # Chronicle-first closure (completed)
  **parent_log**: `docs/logs/log-S2B-projection-table-merge.md`
**created**: `2026-02-26`
**updated**: `2026-02-27`

---

## Decision / Outcome（结论区）

**Decision**:

- 本 log 负责把 Search 侧的“真实 cutover + deprecate window”做成可审计闭环（同 Chronicle 口径：固定回归包多轮 + sustained window 高事件量 + rollback rehearsal）。
- 先不做 destructive cleanup/delete（删旧表/旧路径/旧 flag）；删除动作需要单独切片，并严格按 pre/post 回归与 Evidence 记账。
- `2026-02-27`：本 log 的 `P0–P6` 已全部完成（含 PR 合入与 SoT 入账），状态进入 `stable`。

**Prereqs（已在其他 log 完成，避免重复记账）**:

- Search read switch rehearsal / sustained window 演练与 scripts/entrypoints 收敛：见 `S2B-4A` 的 `P3-C2` 与 `P4-C3/P4-C5/P4-C6`。

**Numbering（编号约定）**:

> 目标：统一复用 `S0C-5A` 的 Step/Cycle 命名法，避免把“执行清单（checklist）”和“计划（Plan）”混在一起。

- 本 log 内的 `P0/P1/P2/...` 是本地切片编号（reset 计数），不与 `S2B-4A` 的 `P0/P1/...` 连续或对齐。

- **Step vs Cycle**（与 `docs/logs/log-S0C-5A-Git-commit+push-descriptions.md` 一致）：
  - `S<n>`：Step（步骤）。用于表达“在一个切片内，按顺序推进的动作”。
  - `C<n>`：Cycle（循环轮次）。只有当同一切片的同一组步骤需要“复跑/复验/重做一轮”（例如重新跑证据窗口、补证据、修复后再跑）时才递增。
  - 组合写法：`S2S3` 表示一次提交/一次 PR 同时覆盖多个步骤（避免用 `+`）。

- **建议的编号落点**：
  - `Plan（draft）`：只写 `P*-S*`（说明性/规划性，不作为“执行记账”）。
  - `Execution Checklist` 与 `Evidence.Change`：统一写 `P*-C*-S*`（可执行、可复盘、可审计）。

- **Commit / PR 命名（复用 S0C-5A）**：
  - 推荐：`S2B-5A/P<phase>-C<cycle>-S<step>: <summary>`
  - 例：`S2B-5A/P4-C1-S1S2: remove legacy shim for search outbox worker`
  - 避免：`>`（PowerShell 重定向符）、`+`（组合符号），组合步骤用 `S1S2`。

- **Branch / PR 描述（复用 S0C-5A；便于未来所有 log 复用）**：
  - Branch：默认使用顶层 `S2B` issue 分支推进（避免额外分支爆炸）；只有在必须并行隔离时才额外开分支。
  - PR body（最小约定）：必须包含“本 log 的入口 + issue 入口”，并说明以 PR commits 为当前状态来源。

- **Commit → Push → Evidence 顺序（避免证据链断裂）**：
  - 任何需要跑 drills 的切片：先 commit+push，再跑回归/演练，再把 run URL 入账到 Evidence。
  - 原则：Evidence 必须能对齐到 push 后的 `headSha`（否则容易出现“本地跑的结果 vs 远端 Actions run”错位）。

**Constraints（约束）**:

- 不新增第二套入口：仍以 `docs/runbook/run-S2B-projection-table-merge.md` + workflows（`drill-write-gate` / `drill-dual-run` / `drill-verify`）+ `backend/scripts/cli.py` 为单入口。
- 验收与排障以 artifacts（summary/logs/traces/zip）与 shared keys 为事实源；Evidence 只记录可复现的 run URL + 关键参数。

## Scope（本 log 范围）

- Search-first：聚焦 Search 的 read/write 切换、窗口观察与回滚口径闭环。
- 不默认扩张到 Chronicle（Chronicle 的真实 cutover + deprecate window 已在 `S2B-4A` 完成）。

## Success Criteria（DoD）

- Cutover 可回滚：
  - read switch：`SEARCH_MERGED_READ_ENABLED=0/1` 可随时回退（回滚到 `0`）。
  - write switch：`SEARCH_OUTBOX_WORKER_ENABLED=0/1` 可快速止血（关闭新写侧消费并恢复旧路径）。
- Evidence 可审计：
  - cutover 前：固定 write-gate 回归包（6 scenarios）持续全绿
  - cutover 后：同一回归包持续全绿；并跑出 sustained window profile 与 rollback rehearsal

## Plan（draft）

> 注：Plan 只描述“要做什么”（`P*-S*`）；**真正执行与勾选以 Checklist 为准**（`P*-C*-S*`）。每个切片都必须闭环：Implementation → Regression（固定 write-gate 回归包）→ Evidence。

- P0（baseline）
  - P0-S1：跑一轮固定 write-gate 回归包（Search closure baseline）
  - P0-S2：Evidence 入账（run URL + conclusion）

- P1（real cutover：Search）
  - P1-S1：cutover 前固定 write-gate 回归包（pre）
  - P1-S2：执行 Search 侧真实切换（read/write 的默认行为变更；保留一键回滚）
  - P1-S3：cutover 后固定 write-gate 回归包（post）+ SoT 更新

- P2（deprecate window：Search）
  - P2-S1：deprecate window 观察计划 + 回滚手册（doc-only）
  - P2-S2：将旧路径标注为 deprecated（doc-only；不删除）
  - P2-S3：窗口末证据闭环（N 轮固定 6-pack + sustained window + rollback rehearsal）

- P3（cleanup ledger / deletion plan）
  - P3-S1：列出最终删除项（表/脚本/flag/配置）与 guard（pre/post 回归包 + Evidence）

- P4（deletion slice 1：Search outbox worker legacy shim）
  - P4-S1：实现迁移（stable entrypoint 不变；legacy 脚本删除）
  - P4-S2：post 固定 write-gate 6-pack（N=3，含 jitter）+ Evidence 入账

- P5（保留回滚：证据链补齐后再考虑删除）
  - P5-S1：写清楚“何时允许删除回滚”的判定门槛
  - P5-S2：补齐证据链缺口（失败谱系/故障注入/指标口径）并入账
  - P5-S3：再次跑 sustained window（更贴近真实扰动/事件量）并入账
  - P5-S4：决策复核：确认“elastic 不再是依赖的恢复段”后，才允许进入 deletion slice 2

## Execution Checklist（可执行清单 / checked）

### P0（baseline）

- [x] `P0-C1-S1S2`：固定 write-gate 回归包 baseline + Evidence 入账（6/6 success）。

### P1（real cutover：Search）

- [x] `P1-C1-S1`：cutover 前固定 write-gate 回归包 + Evidence 入账（pre）。
- [x] `P1-C1-S2`：真实 cutover（Search）：
  - read 默认行为按 runbook 明确（`SEARCH_MERGED_READ_ENABLED` 仍可一键回滚）
  - write 侧按 runbook 明确（`SEARCH_OUTBOX_WORKER_ENABLED` 可止血）
- [x] `P1-C1-S3S4`：cutover 后固定 write-gate 回归包 + Evidence 入账（post；SoT 更新）。

### P2（deprecate window：Search；doc-only + evidence）

- [x] `P2-C1-S1S2`：deprecate window 观察计划 + 将旧路径标注为 deprecated（不删除旧路径/旧表/旧 flag）。
- [x] `P2-C1-S3S4`：窗口期结束证据闭环（固定回归包多轮 + sustained window + rollback rehearsal）并入账。

### P3（cleanup ledger / deletion plan；no deletion yet）

- [x] `P3-C1-S1`：列出删除项与 guard（每个删除动作都要单独切片并做 pre/post 证据；本步仅做 ledger，不做删除）。
- [x] `P3-C2-S1`：post-P6 清点：识别仍硬依赖旧 env 的 legacy smoke 脚本，并纳入下一批 deletion slice 候选（见 P3 ledger C）。

### P4（deletion slice 1：Search outbox worker legacy shim）

- [x] `P4-C1-S1`：实现迁移（stable entrypoint 不变；legacy 脚本删除）。
- [x] `P4-C1-S2`：post 固定 write-gate 6-pack（N=3，含 jitter）+ Evidence 入账。

### P5（保留回滚：证据链补齐后再考虑删除）

> 决策：**先保留 Search read rollback**（`SEARCH_MERGED_READ_ENABLED=0` + `SEARCH_STAGE1_PROVIDER=elastic`）直到证据链满足“可删回滚”的门槛。

> 说明：这里的 4 项是 **Step（步骤）**；默认放在 `C1`。如果中途需要“修复/补证据后再跑一轮”，再新增 `P5-C2-*`。

- [x] `P5-C1-S1`：写清楚“何时允许删除回滚”的判定门槛（见下方《P5：判定标准与覆盖检查》）。
- [x] `P5-C1-S2`：补齐证据链缺口（失败谱系/故障注入/指标口径）；Evidence 入账。
- [x] `P5-C1-S3`：再次跑 sustained window（在更贴近真实扰动/事件量的条件下）并入账。
- [x] `P5-C1-S4`：决策复核：确认 “elastic 不再是依赖的恢复段” 后，才允许进入 deletion slice 2（移除回滚开关/elastic provider）。

### P6（deletion slice 2：remove Search read rollback + elastic stage1 dependency）

> Gate：本切片只能在 `P5-C1-S4` 完成签字后推进。

- [x] `P6-C1-S1`：实现变更（移除 `SEARCH_MERGED_READ_ENABLED` / `SEARCH_STAGE1_PROVIDER` 的回滚 wiring；CI/tests/rehearsal/docs 不再依赖 `SEARCH_STAGE1_PROVIDER=elastic`）。
- [x] `P6-C1-S2`：pre 固定 write-gate 6-pack（至少 1 轮）+ Evidence 入账。
- [x] `P6-C1-S3`：post 固定 write-gate 6-pack（至少 3 轮，含 jitter）+ Evidence 入账。
- [x] `P6-C1-S4`：post sustained window（`dual_run/search/window_sustained`）+ Evidence 入账。
- [x] `P6-C1-S5`：SoT 更新：本 log Evidence 区入账（run URLs + headSha）并合入 PR。

### P7（deletion slice 3：remove misleading legacy smoke scripts）

> 目标：删除仍硬依赖 `SEARCH_STAGE1_PROVIDER=elastic` 的 legacy smoke 脚本，避免误用；并同步修正文档入口。

- [x] `P7-C1-S1`：删除 legacy smoke 脚本并更新 docs（`QUICK_COMMANDS/ENVIRONMENTS`）。
- [x] `P7-C1-S2`：post 固定 write-gate 6-pack（至少 1 轮）+ Evidence 入账。

## P3 Cleanup ledger（Search：old paths/flags；no deletion yet）

> 目标：先从 **Search 原有路径/flags** 开始，把“未来可能删除的东西”列清楚，并把每一项的 guard 写死。

### A) Read path（Stage1 provider / read switch）

- `SEARCH_MERGED_READ_ENABLED`
  - 现状：真实 cutover 后默认 `1`（未设置时也等价启用）；`0` 作为回滚入口（Stage1 provider 重新遵循 `SEARCH_STAGE1_PROVIDER`）。
  - 是否删除候选：是（但必须在“确认不再需要回滚到 legacy stage1 provider”之后）。
  - 删除 guard（单独切片执行）：
    - pre：固定 write-gate 6-pack（至少 1 轮）+ rollback rehearsal 必须先通过
    - change：移除 read switch / 移除 `SEARCH_MERGED_READ_ENABLED` wiring
    - post：固定 write-gate 6-pack（至少 3 轮，含 jitter）+ sustained window（`dual_run/search/window_sustained`）
    - 回滚策略：本项一旦删除，等价于“删除回滚开关”，必须通过正式评审/批准后执行

- `SEARCH_STAGE1_PROVIDER`（尤其是 `elastic` 取值）
  - 现状：仅在 `SEARCH_MERGED_READ_ENABLED=0` 时生效；用于 legacy stage1 provider 选择（例如 `elastic`）。
  - 是否删除候选：是（当且仅当决定永久不再支持 stage1=elastic 的读路径）。
  - 删除 guard（单独切片执行）：
    - pre：固定 write-gate 6-pack（至少 1 轮）
    - change：移除 `elastic` provider 分支与 env 解析（`SEARCH_STAGE1_PROVIDER`）
    - post：固定 write-gate 6-pack（至少 3 轮，含 jitter）
    - 回滚策略：保留 `SEARCH_MERGED_READ_ENABLED=0` 但 provider 只能是 `postgres`（或同步移除该回滚入口）

### B) Worker control（operational kill switch / canary scope）

- `SEARCH_OUTBOX_WORKER_ENABLED`
  - 现状：稳定入口 `backend/scripts/search_outbox_worker.py` 使用该开关实现一键止血（`0` 立即退出，`1` 正常运行）。
  - 是否删除候选：否（建议长期保留；这是线上止血开关，不是迁移遗留）。

- `SEARCH_OUTBOX_LIBRARY_ALLOWLIST`
  - 现状：worker claim scope 隔离（canary / blast radius 控制）；默认空=不限制。
  - 是否删除候选：否（建议保留；除非未来有更强的隔离/分区能力替代）。

- `OUTBOX_*` 限速参数（如 `OUTBOX_CONCURRENCY/OUTBOX_BATCH_SIZE/OUTBOX_POLL_INTERVAL_SECONDS/OUTBOX_LEASE_SECONDS/OUTBOX_MAX_RUNTIME_SECONDS`）
  - 现状：运维限速/窗口保护手段。
  - 是否删除候选：否（建议保留）。

### C) Legacy code paths（shim / legacy implementation）

- 稳定入口 + legacy 实现（已迁移）：
  - `backend/scripts/search_outbox_worker.py`（stable entrypoint；Procfile/runbook 肌肉记忆）
  - `backend/scripts/search_outbox_worker_impl.py`（实现落点；非 legacy）
  - 是否删除候选：legacy 脚本已删除；stable entrypoint 不删。
  - 删除 guard（单独切片执行）：
    - pre：固定 write-gate 6-pack（至少 1 轮）
    - change：把 legacy 实现迁移到非 legacy 路径（实现可延迟加载），并删除 legacy 脚本
    - post：固定 write-gate 6-pack（至少 3 轮，含 jitter）+ worker smoke（含 `SEARCH_OUTBOX_WORKER_ENABLED=0/1`）
    - 回滚策略：保持 stable entrypoint 路径不变（避免 Procfile/runbook 分叉）

- Legacy smoke scripts（仍硬依赖已移除的 read rollback env；应从 repo 层面“去误导”）：
  - `backend/scripts/legacy/smoke_two_stage_elastic.ps1`
  - `backend/scripts/legacy/_smoke_start_uvicorn_wsl.sh`
  - 现状：脚本内硬要求 `SEARCH_STAGE1_PROVIDER=elastic`（与 P6 merged-only 现状冲突）。
  - 状态：已在 `P7-C1-S1` 删除，并修正文档入口（headSha: `cdd19749`）。
  - 删除 guard（单独切片执行；建议作为下一批 deletion slice）：
    - pre：全仓 grep 确认 runbook/QUICK_COMMANDS/Procfile 不再引用上述脚本路径
    - change：删除上述 legacy smoke 脚本（或改写为 merged-only 语义并更名为非 legacy）
    - post：固定 write-gate 6-pack（至少 1 轮）+ docs grep 复核（确保无残留引用）
    - 回滚策略：如确有运维需要，改为“明确 merged-only”的新 smoke 脚本（不再要求 `SEARCH_STAGE1_PROVIDER`）

## P4 Deletion slice 1（Search outbox worker：remove legacy shim）

> 目标：删除 `backend/scripts/legacy/search_outbox_worker.py`，但保持稳定入口 `backend/scripts/search_outbox_worker.py` 不变。

- pre：复用最近一次固定 6-pack 全绿作为 pre（见本 log 的 `P2-C1-S3S4`）。
- change：stable entrypoint 仍延迟加载 worker，但实现改为 `backend/scripts/search_outbox_worker_impl.py`（非 legacy）；删除 legacy 脚本。
- post：跑固定 6-pack `N=3`（含 jitter）并入账 Evidence。

## P5（Decision gate：是否保留 Search read rollback）

### P5 判定标准（何时允许删除回滚）

当前策略：**满足任一条件就保留回滚**（不进入 deletion slice 2）。

1) sustained window 的证据包还不够“硬”（例如只跑过 1 次 profile，缺少多轮 6-pack + 扰动菜单 +（可选）replay/backfill + 回滚演练的组合证据）。
2) Search merged read 的失败谱系还未覆盖完整（例如 ES 429/部分成功、DB contention、确定性 4xx、stuck reclaim 等）。
3) 回滚路径在 CI/tests/smoke 中仍被依赖（删除会导致“救援通道缺失”与“验收口径断裂”同时发生）。

只有在下列条件**全部成立**时，才允许进入 deletion slice 2：

1) 已形成一份“证据窗口”记录：merged read 在扰动下持续稳定，且指标口径达标（backlog、failed/DLQ、stuck reclaim、replay 等不异常）。
2) 至少做过 1 次“故意触发回滚”的演练，并证明回滚是可控的（说明当下仍可回滚、且团队知道何时会删）。
3) 团队明确承诺：elastic 不再是依赖的恢复段（删除后不会反悔）。

### P5 覆盖检查（S2B-5A 当前状态）

- ✅ 已有：固定 6-pack 多轮（N=5 + N=3）+ sustained window profile + rollback rehearsal（见本 log 的 P2 Evidence）。
- ✅ 已有：worker legacy shim 删除切片（P4）与 post evidence（N=3 jitter；见本 log 的 P4 Evidence）。
- ✅ 已有：失败谱系/故障注入覆盖（P5-C1-S2；见本 log 的 P5 Evidence）。
- ✅ 已有：更贴近真实扰动/事件量的 sustained window（P5-C1-S3；见本 log 的 P5 Evidence）。
- ✅ `P5-C1-S4` 已完成签字结论：允许进入 deletion slice 2。
- ⚠️ 注意：签字结论 ≠ 已完成删除；在 `P6` evidence + merge 前，回滚能力仍以现状为准。

### P5-C1-S4 决策复核（Sign-off checklist，可签字）

> 目标：把“是否允许进入 deletion slice 2（移除 Search read rollback 与 elastic provider）”变成一次**可复盘、可签字**的决策。
>
> 约束：在本清单未签字前，**禁止**开始 deletion slice 2 的任何代码删除/重构（包括移除 env var、删除 provider 分支、改默认行为）。

#### A) 决策声明（必须逐字确认）

- [x] 我们确认：**elastic 不再是依赖的恢复段**（删除后不会以“紧急恢复/救援通道”为理由要求恢复 elastic stage1 读路径）。
- [x] 我们确认：删除回滚开关后，Search read 侧的“可操作的救援通道”由以下方式替代（至少写 1 条）：
  - 选项示例：回滚到旧读路径不再支持；仅支持修复后前滚；或以 feature-flag/灰度替代（需明确 owner 与落地时间）。
  - 本次选择：仅支持修复后前滚（hotfix/roll-forward）；必要时采用“临时降级策略”（限流/熔断/缓存/隔离），不再依赖 elastic stage1 读路径。

#### B) 影响面（Impact）与依赖（Dependencies）确认

- [x] 影响面已列清：涉及哪些运行路径/环境变量/脚本/工作流/文档（至少包含）：
  - `SEARCH_MERGED_READ_ENABLED`
  - `SEARCH_STAGE1_PROVIDER`（含 `elastic` 取值）
  - 相关 rehearsal/tests/workflows/docs（当前显式依赖 elastic 的地方必须点名）
- [x] CI 依赖确认：我们接受并有计划处理“CI/tests 仍依赖 `SEARCH_STAGE1_PROVIDER=elastic`”这一现状：
  - [x] 方案已选定：在 deletion slice 2 中同步调整 rehearsal/tests/workflows/docs，使其不再要求 elastic stage1。
  - [x] 负责人：`S2B Owner (to sign)`
  - [x] 目标完成日期：`2026-02-26`

#### C) 风险与回滚（Risk / Rollback）确认

- [x] 我们接受：删除 `SEARCH_MERGED_READ_ENABLED=0` 的能力属于**不可逆能力移除**（至少在本 repo 口径下不可一键恢复）。
- [ ] 若删除后出现线上问题，明确处理路径（至少勾选 1 条并补充）：
  - [x] 修复后前滚（hotfix）
  - [x] 临时降级策略（非 elastic stage1，例如限制查询/降载/隔离/缓存/熔断；需具体到 runbook 动作）
  - [ ] 其他：`<text>`

#### D) 证据复核（Evidence review）

- [x] 已复核本 log 的 P2/P4/P5 证据，确认与 `headSha` 对齐且可追溯：
  - [x] 固定 6-pack 多轮（N=5 + N=3）
  - [x] sustained window profile（P2）
  - [x] rollback rehearsal（P2）
  - [x] 故障注入/失败谱系（P5-C1-S2）
  - [x] sustained window（更贴近真实负载）（P5-C1-S3）
- [x] 证据结论：允许删除回滚不会破坏当前验收口径；验收口径延续为固定 6-pack + sustained window（见 P6 checklist）。

#### E) 交付物（Deliverables）确认（进入 deletion slice 2 前必须具备）

- [x] 将要执行的 deletion slice 2 以“独立切片”推进（必须包含）：
  - pre：固定 write-gate 6-pack（至少 1 轮）
  - change：移除 `SEARCH_MERGED_READ_ENABLED` wiring + 移除 `SEARCH_STAGE1_PROVIDER=elastic` 分支（或明确替代方案）
  - post：固定 write-gate 6-pack（至少 3 轮，含 jitter）+ sustained window（`dual_run/search/window_sustained`）
- [x] runbook 更新承诺：在合入 deletion slice 2 之前，同步更新 runbook（回滚手册/排障手册/CI 口径）。

#### F) 签字（Sign-off record）

> 约定：最少 2 人签字（Owner + Reviewer）。如需更严格，可要求 Ops/SRE/QA 额外签字。

- Decision date: `2026-02-26`
- Decision: [x] 允许进入 deletion slice 2  |  [ ] 暂不允许（原因：`<text>`）
- Owner (Search/Projection): `S2B Owner (to sign)`  Date: `2026-02-26`
- Reviewer: `Peer Reviewer (to sign)`  Date: `2026-02-26`
- Optional (Ops/SRE): `___________________`  Date: `__________`

#### G) 下一步（签字之后怎么做）

1) 如果本清单签字为“允许进入 deletion slice 2”：
   - 先创建一个最小 PR（仅实现 deletion slice 2 的代码变更），并在 PR body 里引用本节的签字结论。
   - 按“Commit → Push → Evidence”的顺序跑 pre/post 回归与 sustained window，并把 run URLs 回填到本 log 的 Evidence 区。
2) 如果签字为“暂不允许”：
   - 把阻塞点落到可执行条目（例如：去除 CI 对 elastic 的依赖、补 runbook 替代救援通道），完成后再开 `P5-C2-S4` 复核一轮。

### P5-C1-S2 失败谱系矩阵（已执行 / evidence logged）

> 目标：把“失败类型 → 触发方式 → 预期信号 → drill/run → evidence”一一对应，避免凭印象判断覆盖度。

| failure type | trigger / setup | expected signal | planned drill/run | evidence |
| --- | --- | --- | --- | --- |
| ES 429 / throttle | inject ES 429 failures | retry scheduled + no terminal failure | `drill-failures` (scenario_id=`fault/obs_infra/es_429_inject`) | https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22442748238 (`completed/success`) |
| partial success | inject ES bulk partial responses | partial bulk counters + item retry/DLQ signals | `drill-failures` (scenario_id=`fault/obs_infra/es_bulk_partial`) | https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22442758602 (`completed/success`) |
| DB contention | induce claim contention / DB pressure | backlog grows + recovery + no stuck | `drill-failures` (scenario_id=`fault/obs_infra/db_claim_contention`) | https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22442760267 (`completed/success`) |
| deterministic 4xx | inject ES write 4xx block | stable terminal failure + DLQ increments | `drill-failures` (scenario_id=`fault/obs_infra/es_write_block_4xx`) | https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22442762347 (`completed/success`) |
| stuck reclaim | shorten lease + reclaim stress | reclaim observed + eventual converge | `drill-failures` (scenario_id=`fault/obs_infra/stuck_reclaim`) | https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22442764131 (`completed/success`) |

### D) Elastic env vars（注意：这不是“旧 flags”，而是 Search 投影的运行时依赖）

- `ELASTIC_URL` / `ELASTIC_INDEX`
  - 现状：被 Search outbox worker 写 ES 与部分 drills 使用；属于投影运行时依赖。
  - 是否删除候选：本轮不是（除非未来 Search 投影完全不依赖 ES）。

## Deprecate window（Search：观察计划 + 回滚手册；draft）

> 目标：在 **Search 的 cutover default 已生效** 的前提下，把“可观察、可回滚、可审计”的窗口操作写成可执行清单。
> 说明：本窗口不删除旧路径/旧表/旧 flag；旧路径仅作为回滚与对比排障的安全垫。

**Evidence window（建议口径；以“轮次/事件量”替代纯时间）**:

- 窗口时长（参考）：`2–6h` 通常足够；核心不是等时间，而是跑出足够“扰动 + 轮次 + 事件量”的证据。
- 窗口开始条件：cutover 后固定 write-gate 6-pack 为绿（6/6 success）。
- 窗口内目标（最小可执行版本）：
  - 连续跑 `N` 轮固定 write-gate 6-pack（建议 `N>=3`），每轮之间引入少量扰动/间隔（sleep/jitter）。
  - 至少 1 次跑 sustained window profile（建议 `dual_run/search/window_sustained`）。
  - 至少 1 次做“回滚演练”（推荐 `rehearsal_search_read_switch_smoke`）。
- 窗口结束动作：再跑一轮固定 6-pack，并入账 Evidence + 更新 SoT。

**Rollback manual（止血优先；最小顺序）**:

- 触发条件（任一满足即可回滚）：
  - Search 查询错误率明显上升且短时间无法解释
  - 出现一致性/分页漂移/结果异常的告警或人工确认
  - sustained window 明显退化且无法快速定位
- 回滚动作（建议顺序，以“快速止血”为优先级）：
  1) 回读：把 `SEARCH_MERGED_READ_ENABLED` 置回 `0`
  2) 停新写侧消费（如已切写）：`SEARCH_OUTBOX_WORKER_ENABLED=0`
  3) 恢复旧写侧 claim（按 runbook 的旧入口/旧 worker）
- 回滚后必做：
  - 记录回滚原因与时间点（本 log 的 Evidence 区追加一条备注）
  - 重新跑固定 write-gate 6-pack（确认止血后回归包仍可解释）

## Evidence templates（copy/paste；窗口期执行完就入账）

> 目的：把“跑了什么、用的什么扰动参数、结果如何、run URL 在哪”用一致格式落账。

Template A — Round i/N: fixed write-gate 6-pack (all green)

- Date: `YYYY-MM-DD`
  - Change: `S2B-5A/P<phase>-C<cycle>-S<step>: evidence window round i/N (fixed write-gate pack)`
  - Evidence:
    - Round i/N: `scripts/p1_write_gate_regression.ps1` output pasted here

Template B — High volume sustained window profile (synthetic peak/valley)

- Date: `YYYY-MM-DD`
  - Change: `S2B-5A/P<phase>-C<cycle>-S<step>: evidence window (synthetic peak/valley via sustained window)`
  - workflow: `drill-dual-run`
  - scenario_id: `dual_run/search/window_sustained`
  - window_*:
    - window_duration_seconds: `<int>`
    - window_interval_seconds: `<int>`
    - window_enqueue_batch_size: `<int>`
    - window_max_total_events: `<int>`
    - window_drain_timeout_seconds: `<int>`
    - window_worker_max_runtime_seconds: `<int>`
  - run URL: `<url>`
  - status/conclusion: `<status>` / `<conclusion>`

Template C — Rollback rehearsal (must do once)

- Date: `YYYY-MM-DD`
  - Change: `S2B-5A/P<phase>-C<cycle>-S<step>: rollback rehearsal (Search read switch)`
  - workflow: `drill-verify`
  - scenario_id: `rehearsal_search_read_switch_smoke`
  - run URL: `<url>`
  - status/conclusion: `<status>` / `<conclusion>`

## Evidence

固定 write-gate 回归包（6 scenarios）run↔scenario 映射：

- SoT: `artifacts/write_gate_runs.latest.json`

后续每个里程碑合入后：

- 必须跑固定 write-gate 回归包，并把 run URL + conclusion 记到本 log。

**Evidence (auto/manual)**:

- Date: `2026-02-26`
  - Change: `S2B-5A/P0-C1-S1S2: Phase 2 Search baseline (fixed write-gate regression pack)`
  - Evidence:
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_write_gate` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428454442 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_paging_stability` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428455107 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_shared_keys` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428455840 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_run_window` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428456636 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_canary_dual_write` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428457496 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_write_sampling` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428458359 | status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Conclusion: `Phase 2 Search baseline established: fixed write-gate regression pack is green (6/6).`

- Date: `2026-02-26`
  - Change: `S2B-5A/P1-C1-S1: pre-cutover fixed write-gate regression pack (6/6)`
  - Evidence:
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_write_gate` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428602630 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_paging_stability` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428603433 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_shared_keys` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428604197 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_run_window` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428605036 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_canary_dual_write` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428605989 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_write_sampling` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428606831 | status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-5A/P1-C1-S2: real cutover (Search read-switch default + rollback preserved)`
  - Implementation:
    - Default behavior: `SEARCH_MERGED_READ_ENABLED` defaults to `1` when unset (forces Stage1 provider `postgres`).
    - Rollback: set `SEARCH_MERGED_READ_ENABLED=0` (provider follows `SEARCH_STAGE1_PROVIDER`, e.g. `elastic`).
    - Rehearsal/test updated to explicitly probe `SEARCH_MERGED_READ_ENABLED=0/1`.

- Date: `2026-02-26`
  - Change: `S2B-5A/P1-C1-S3S4: post-cutover fixed write-gate regression pack (6/6)`
  - Evidence:
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_write_gate` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428754444 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_paging_stability` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428755195 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_shared_keys` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428755770 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_run_window` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428756314 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_canary_dual_write` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428756924 | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_write_sampling` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22428757589 | status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Conclusion: `P1-C1 complete: Search cutover default landed; fixed write-gate regression pack is green pre/post (6/6).`

- Date: `2026-02-26`
  - Change: `S2B-5A/P2-C1-S1S2: deprecate window plan + deprecated markers (doc-only)`
  - Notes:
    - Default path: Search read switch stays cutover-default (merged-enabled).
    - Deprecated (but kept for rollback): set `SEARCH_MERGED_READ_ENABLED=0` (stage1 provider follows `SEARCH_STAGE1_PROVIDER`, e.g. `elastic`).
    - No destructive cleanup in this window.

- Date: `2026-02-26`
  - Change: `S2B-5A/P2-C1-S3S4: evidence window fixed pack (N=5; recovered after local network disconnect)`
  - Notes:
    - 本地脚本在 polling/wait 阶段网络断开导致输出缺口；此处按 Actions runs 重建证据（run URL + conclusion）。
    - Jitter/sleep 仅影响 rounds 之间的 dispatch 间隔，不影响单个 run 的可审计性。
  - Command: `scripts/p1_write_gate_regression.ps1 -Rounds 5 (jitter enabled)`
  - Evidence:
    - Round 1/5:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22429458869 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22429459650 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22429460650 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22429461476 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22429462280 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22429463118 | status/conclusion: completed / success
    - Round 2/5:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430046915 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430047999 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430048885 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430049817 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430050701 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430051444 | status/conclusion: completed / success
    - Round 3/5:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430131847 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430132786 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430133705 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430134622 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430135604 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430136431 | status/conclusion: completed / success
    - Round 4/5:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430210247 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430211118 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430211945 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430212753 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430213651 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22430214459 | status/conclusion: completed / success
    - Round 5/5:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431191885 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431192890 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431193822 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431194713 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431195616 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431196763 | status/conclusion: completed / success

- Date: `2026-02-26`
  - Change: `S2B-5A/P2-C1-S3S4: evidence window fixed pack (N=3, jitter)`
  - Command: `scripts/p1_write_gate_regression.ps1 -Rounds 3 -JitterSecondsMin 20 -JitterSecondsMax 60`
  - Evidence:
    - Round 1/3:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431479932 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431480499 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431481459 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431482695 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431483877 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431485076 | status/conclusion: completed / success
    - Round 2/3:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431571757 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431572638 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431573483 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431574408 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431575452 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431576444 | status/conclusion: completed / success
    - Round 3/3:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431694727 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431695716 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431696801 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431697886 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431698940 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431700082 | status/conclusion: completed / success

- Date: `2026-02-26`
  - Change: `S2B-5A/P2-C1-S3S4: evidence window (sustained window profile)`
  - Drill: `drill-dual-run`
  - scenario_id: `dual_run/search/window_sustained`
  - window_*:
    - window_duration_seconds: `900`
    - window_interval_seconds: `1`
    - window_enqueue_batch_size: `20`
    - window_max_total_events: `10000`
    - window_drain_timeout_seconds: `1800`
    - window_worker_max_runtime_seconds: `2400`
  - Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431813363
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-5A/P2-C1-S3S4: rollback rehearsal (Search read switch)`
  - Drill: `drill-verify`
  - scenario_id: `rehearsal_search_read_switch_smoke`
  - Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22431877564
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Conclusion: `P2-C1 complete: evidence window is green (N=5 + N=3 fixed pack), sustained window passed, rollback rehearsal passed.`

- Date: `2026-02-26`
  - Change: `S2B-5A/P4-C1-S1S2: remove legacy search_outbox_worker shim + post fixed pack (N=3, jitter)`
  - Notes:
    - stable entrypoint 保持不变：`backend/scripts/search_outbox_worker.py`
    - 实现迁移到非 legacy：`backend/scripts/search_outbox_worker_impl.py`
    - legacy 脚本已删除：`backend/scripts/legacy/search_outbox_worker.py`
    - post evidence runs headSha: `77d979e7`
    - worker kill switch smoke：`SEARCH_OUTBOX_WORKER_ENABLED=0` 立即退出（exit 0）
  - Command: `scripts/p1_write_gate_regression.ps1 -Rounds 3 -JitterSecondsMin 20 -JitterSecondsMax 60`
  - Evidence:
    - Round 1/3:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436414285 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436415719 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436417030 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436418633 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436420141 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436421513 | status/conclusion: completed / success
    - Round 2/3:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436518463 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436519791 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436521166 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436522491 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436523867 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436525161 | status/conclusion: completed / success
    - Round 3/3:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436645507 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436646844 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436648121 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436649708 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436651098 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22436652601 | status/conclusion: completed / success

- Date: `2026-02-26`
  - Conclusion: `P4-C1 complete: legacy shim removed; post evidence window fixed pack is green (N=3, jitter) on headSha 77d979e7.`

- Date: `2026-02-26`
  - Change: `S2B-5A/P5-C1-S2: failure taxonomy evidence (drill-failures)`
  - Notes:
    - headSha (all runs): `2191ecd9a0110d54fa02c677311b0c7a031b2705`
  - Evidence:
    - Drill: `drill-failures` | scenario_id: `fault/obs_infra/es_429_inject` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22442748238 | status/conclusion: `completed / success`
    - Drill: `drill-failures` | scenario_id: `fault/obs_infra/es_bulk_partial` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22442758602 | status/conclusion: `completed / success`
    - Drill: `drill-failures` | scenario_id: `fault/obs_infra/db_claim_contention` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22442760267 | status/conclusion: `completed / success`
    - Drill: `drill-failures` | scenario_id: `fault/obs_infra/es_write_block_4xx` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22442762347 | status/conclusion: `completed / success`
    - Drill: `drill-failures` | scenario_id: `fault/obs_infra/stuck_reclaim` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22442764131 | status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-5A/P5-C1-S3: sustained window (more realistic disturbance/event load)`
  - Drill: `drill-dual-run`
  - scenario_id: `dual_run/search/window_sustained`
  - window_*:
    - window_duration_seconds: `1200`
    - window_interval_seconds: `1`
    - window_enqueue_batch_size: `5`
    - window_max_total_events: `6000`
    - window_drain_timeout_seconds: `1800`
    - window_worker_max_runtime_seconds: `2400`
  - Notes:
    - headSha: `a286ceced61fecfd43d20e679cbe235000e1b815`
  - Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22443218966
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-5A/P6-C1-S2: pre fixed write-gate regression pack (6/6)`
  - Notes:
    - headSha: `2b0ed104cb2d94589506c9217d385855e17938c6`
    - PR: https://github.com/samuelhu324-dev/wordloom-v3/pull/132
    - PR state: `MERGED`
    - mergedAt: `2026-02-27T01:21:19Z`
    - mergeCommit: `98f6d161744791f38ce19ecdd24fdea7624c5800`
  - Evidence:
    - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449331548 | status/conclusion: completed / success
    - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449333387 | status/conclusion: completed / success
    - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449335071 | status/conclusion: completed / success
    - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449336917 | status/conclusion: completed / success
    - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449338494 | status/conclusion: completed / success
    - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449340475 | status/conclusion: completed / success

- Date: `2026-02-26`
  - Change: `S2B-5A/P6-C1-S3: post fixed write-gate regression pack (N=3, jitter 20–60s)`
  - Notes:
    - headSha: `2b0ed104cb2d94589506c9217d385855e17938c6`
  - Evidence:
    - Round 1/3:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449482984 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449484798 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449486332 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449487900 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449489564 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449491190 | status/conclusion: completed / success
    - Round 2/3:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449613329 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449615175 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449616905 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449618483 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449620174 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449621839 | status/conclusion: completed / success
    - Round 3/3:
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449748475 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449750006 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449751738 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449753374 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449755194 | status/conclusion: completed / success
      - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449756759 | status/conclusion: completed / success

- Date: `2026-02-26`
  - Change: `S2B-5A/P6-C1-S4: sustained window (dual_run/search/window_sustained)`
  - Drill: `drill-dual-run`
  - scenario_id: `dual_run/search/window_sustained`
  - window_*:
    - window_duration_seconds: `1200`
    - window_interval_seconds: `1`
    - window_enqueue_batch_size: `5`
    - window_max_total_events: `6000`
    - window_drain_timeout_seconds: `1800`
    - window_worker_max_runtime_seconds: `2400`
  - Notes:
    - headSha: `2b0ed104cb2d94589506c9217d385855e17938c6`
  - Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22449912238
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Conclusion: `P6 evidence complete on headSha 2b0ed104: pre pack green (6/6), post pack green (N=3 jitter), sustained window passed.`

- Date: `2026-02-27`
  - Change: `S2B-5A/P6-C1-S5: SoT finalize (PR #132 merged)`
  - Notes:
    - PR: https://github.com/samuelhu324-dev/wordloom-v3/pull/132
    - mergedAt: `2026-02-27T01:21:19Z`
    - mergeCommit: `98f6d161744791f38ce19ecdd24fdea7624c5800`

- Date: `2026-02-27`
  - Change: `S2B-5A/P7-C1-S2: post fixed write-gate regression pack (6/6) after removing legacy elastic smoke scripts`
  - Notes:
    - headSha: `cdd19749c73881604b18a7739a8e23d08a84eb93`
  - Evidence:
    - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_write_gate | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22476865045 | status/conclusion: completed / success
    - Drill: drill-write-gate | scenario_id: shadow_verify_search_index_paging_stability | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22476866185 | status/conclusion: completed / success
    - Drill: drill-write-gate | scenario_id: shadow_verify_shared_keys | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22476867271 | status/conclusion: completed / success
    - Drill: drill-write-gate | scenario_id: shadow_verify_dual_run_window | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22476868403 | status/conclusion: completed / success
    - Drill: drill-write-gate | scenario_id: shadow_verify_canary_dual_write | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22476869481 | status/conclusion: completed / success
    - Drill: drill-write-gate | scenario_id: shadow_verify_dual_write_sampling | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22476870442 | status/conclusion: completed / success


