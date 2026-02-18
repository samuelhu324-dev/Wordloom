# Log-S2B-1A: maintainability/failure contract v1

---

**id**: `S2B-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `maintainability/failure contract v1`
**status**: `draft`          # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Chronicle, Projection, Search, epic/s2, sub/1`
**links**: ``
  **issue**: `#56`
  **pr**: ``
  **adr**: ``
  **runbook**: ``
**created**: `2026-02-15`
**updated**: `2026-02-17`

---

## Decision / Outcome（结论区）

**Decision**:

- 将“失败管理/审计/回放”定义为稳定对外接口（Failure Contract v1），把“稳定语义与证据链”从实现细节中抽离出来，合表/合 projection 不得破坏该契约。
- 引入兼容层（Compatibility Shim）：指标/日志/trace 与 runbook/脚本入口保持稳定；内部实现可以替换。
- 采用“语义版本化”（v1/v2…）：版本号属于规则语义与操作入口，而不是仅仅属于 schema。
- 用可回滚的三步走迁移（Dual-run → Read switch → Write switch + retire），降低牵连变更风险。
- 用统一 registry + CLI 门面做 source of truth：文档引用入口与查询模板，不在 runbook 里粘贴易过期细节；旧位置保留 stub。

**Drivers**:

- 大改动不可怕，破坏“稳定接口/稳定证据链”才会让系统到处断。
- 合表/合 projection 会牵动 failure drills / runbook / ADR，需要把“换发动机不换方向盘”工程化。
- 可观测与回放入口（查、降级、replay）必须长期可维护、可交接。

**Non-goals**:

- 不要求一次性重写所有历史 runbook/drill 文档。
- 不承诺 schema/表结构永远不变；只承诺对外语义与证据链尽量稳定。
- 不引入新的文档系统/站点生成器；先用 Markdown + front matter + git 审计。

**Success criteria（DoD）**:

- 同一类失败在外部观察到的语义与证据链保持一致（或通过版本号明确升级）。
- Dashboard / drill 在合表后不需要“全量重写”（最多更新兼容层/门面实现）。
- replay/DLQ/drill 的入口命令与参数稳定（或新旧并存一段时间）。
- 迁移过程具备回滚路径：能对新旧系统做 shadow 对比并产出证据（snapshot/metrics/traces）。

**Current status（现状）**:

- 已落地一条“可回滚读切换（Read switch）”与“影子对账（shadow verify）”最小闭环（以 Chronicle 为样例），可作为 Failure Contract v1 的最小落地样板：
  - 读切换开关：`MERGED_READ_ENABLED=0/1` → `Settings.merged_read_enabled`
  - DI 选择读库（默认 events / 开启 entries），并有测试覆盖
  - 一份可重复运行的 shadow verify 脚本，失败时非 0 退出码

**Evidence（代码证据）**:

- Read switch（DI 层切读）：`backend/api/app/dependencies_real.py`（`get_chronicle_query_service`）
- Flag → settings：`backend/api/app/config/setting.py`（`merged_read_enabled`）
- Flag wiring test：`backend/api/app/tests/test_chronicle/test_merged_read_flag.py`
- Read-side adapter（entries read-only）：`backend/infra/storage/chronicle_entries_repository_impl.py`
- Shadow verify script：`backend/scripts/labs/lab-S2B-1A-1A.py`

## Background

你这个问题已经摸到“成熟团队怎么不把自己搞死”的核心：大改动不可怕，可怕的是把“稳定接口/稳定证据链”也一起改了，然后整个系统像拔河一样到处断。

合表/合 projection 这种变更，确实会牵动 failure drills / runbook / ADR，但成熟做法不是“硬扛着改完”，而是用一套稳定边界 + 适配层 + 版本化的办法，让改动像“换发动机不换方向盘”。

下面给你一套可落地的打法（按你现在的 outbox + worker/daemon + 可观测体系来讲）。

## Problem / Malfunction

- 变更类型：合表/合 projection 属于结构性变更，天然会牵连 runbook、failure drills、可观测看板与历史证据链。
- 典型失败模式：实现细节改变后，外部“同样的失败”看起来变成了不同语义/不同键/不同入口，导致排障、审计、回放不可持续。

## What/How to do（落地规则）

### 1) 先立一个“不许动”的稳定契约：Failure Contract

把“失败管理/审计/回放”当成一个产品接口，而不是实现细节。

**Failure Contract（v1）最小稳定面**建议包含：

- 失败分类：`transient` / `deterministic` / `partial`
- 状态机：`pending → processing/leased → retry_scheduled → failed(DLQ) → replayed`
- 可观测共享键（logs/metrics/traces 统一可关联）：`correlation_id` / `projection` / `outbox_event_id(or event_id)` / `actor` / `tenant/library` 等
- runbook 入口：如何查、如何降级、如何 replay（入口命令与参数尽量稳定）

原则：合表、合 projection 可以改内部实现，但要尽量保证同样的失败在外部看起来仍然是同样的语义和证据链（换内脏不换皮肤）。

### 2) 用“适配层”把旧世界先保住：Compatibility Shim

你担心“连根拔起”，本质上就是缺一个兼容层。

**2.1 指标/日志/trace 适配（别让看板和 drill 全部重写）**

- 内部字段改了没关系，但对外输出统一到稳定字段集。
- 例：将 merged 表里的 `job_id` / `task_id` 映射回旧的 `outbox_event_id` 语义（或反向映射，取决于你要保哪一侧）。
- 指标名称和 label 尽量不改；必须改时采用“保留旧指标一段时间 + 新旧并发上报”。

**2.2 Runbook/脚本入口适配（入口稳定，内部换实现）**

把 runbook 的命令入口做成“门面”（Facade）：

- `scripts/cli.py replay --projection search --since ...`
- `scripts/cli.py dlq list --projection chronicle`
- `scripts/cli.py drill run --scenario es_429`

门面背后调用新旧实现都可以。合表后你改的是门面内部，而不是每一份 runbook。

### 3) 版本化不是给 schema 的，是给“规则语义”的

- 合表前：failure 规则 / retry 规则 / DLQ 规则 是 v1
- 合表后：规则语义变化（例如 claim/reclaim 或 batch 粒度变化）则升级为 v2

关键：runbook 用“规则版本”路由，而不是靠人记忆。

示例（写在 runbook 顶部 metadata 或结论区即可）：

- `failure_contract: v1`
- `projection_runtime: merged_outbox_v2`

当 v2 上线时：

- 新建 v2 runbook（或同文件追加 v2 章节），不要把 v1 改到面目全非
- v1 标注 `deprecated but supported`（明确过渡期与支持范围）

### 4) 牵连变更的增量拆解：三步走（可回滚）

**Step A：并行运行（Dual-run/Shadow）**

- 新 merged projection 先跑起来，但不影响旧的。
- drill 对新旧都跑一遍，产出两份证据（snapshot / metrics / traces）。
- 你已有武器：Golden fixtures + Jaeger export + PromQL summary。

**Step B：切换读路径（Read switch）**

- 先让 UI/查询读新表/新 projection。
- 写入仍可保持旧路径或双写（取决于当前架构）。

**Step C：切换写路径 + 回收旧系统（Write switch + retire）**

- 写切到新系统。
- 旧 worker/表/脚本进入 legacy，保留一段时间可回放。
- 到期再删除（用 ADR 记录“何时删除、验证证据是什么”）。

### 5) 让“被迫改动的文件”不需要逐个改：统一 registry + 稳定链接

不要一个个改文档，先让它们不需要改。

做法：建立统一 registry（source of truth）。例如用 `docs/INDEX.md` + `scripts/cli.py list` 给出：

- drill scenarios 列表
- runbook 的入口命令
- 指标/trace 的关键查询模板

runbook 只保留“人类决策与操作”，把查询语句/脚本命令/路径/URL 全部改成引用 registry 或 CLI 输出。

例：runbook 写“运行：`wl drill run es_429`（详见 `wl drill list`）”，不要粘贴一堆易过期命令。

并对外暴露“稳定链接”：旧位置留 stub，stub 指向新位置，避免链接碎裂与“连根拔起”。

### 6) 合表最容易炸的点（提前埋雷）

- `outbox_event_id` 语义变化（tracing 查不到、replay 找错对象）
- claim/reclaim 状态字段变化（stuck 判断失真）
- batch 语义变化（partial success 计数口径变化）
- 指标 label 变多/变乱（Grafana 看板报废）
- runbook 指令依赖旧脚本路径（入口漂移）

优先级原则：把“可观测共享键”和“replay 入口”当成最优先保守的稳定层。

### 7) 一个可复用的原则：文档是“可演化资产”

一句话：runbook 是操作指南；实现细节进 code/registry；历史决策进 ADR；过期内容进 legacy + stub。

这样改实现时：

- runbook 少改（最多改入口或注意事项）
- registry/cli 更新一次，所有引用自动对齐
- ADR 记录“为什么变了”，而不是把 runbook 改成小说续集

## Next

- 在合表之前写一份超短的 Failure Contract v1（半页纸也可）：明确“必须保持不变/允许变化/变更必须升级版本号”。
- 将“最小落地样板（Chronicle）”抽象为其它 projection 也可复用的清单：开关、对账脚本、回滚步骤、产证据格式。

## References

- `docs/logs/log-S0C-1A-log-extensions.md`（log 结构规范）
- `docs/logs/log-S2B-projection-table-merge.md`（合表/合 projection 相关上下文）