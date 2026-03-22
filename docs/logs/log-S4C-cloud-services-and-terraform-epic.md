# log-S4C（Cloud dev/test infra & Terraform backbone）

---

**id**: `S4C`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `S4C: Cloud dev/test infra & Terraform backbone v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S4`
**tags**: `EVOLUTION, Cloud, Terraform, Infra, epic/s4, sub/1a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-S1-systems-platform-ops-roadmap-v5.md`
  **reference_log_1**: `docs/logs/_template-log-phase-drills-evidence.md`
  **reference_log_2**: ``
  **phase_log_1**: `docs/logs/log-S4C-1A-cloud-devtest-terraform-bootstrap.md`
  **phase_log_2**: `docs/logs/log-S4C-2A-cloud-devtest-db-and-storage.md`
  **phase_log_3**: ``
**created**: `2026-03-22`
**updated**: `2026-03-22`

---

## Decision / Outcome（结论区）

**Decision**:

- 把「cloud services + Terraform minimal path（dev/test-focused）」从 `road-S1-2` 中抽离，收口为 `S4C` 这一条以 Terraform 为主的 infra backbone，后续通过 phase logs 实现和验证。
- 明确边界：`S4C` 只负责 cloud dev/test 级基础设施（网络、托管数据库、对象存储）以及与 wordloom-v3 的连接方式，不直接覆盖生产级多云/安全治理（交由 S5A/S5B 以及将来的 S1 子路来承接）。

**Default choices（默认基线 / v1）**:

- 首选单一云厂商进行练习（AWS 或 Azure 其一），避免在初期分散注意力；必要时通过 notes/roadmap 说明如何迁移到另一个云。
- 所有 Terraform 模块以 "dev/test only" 为前提：小规格、可随时销毁、成本可控，不承载生产数据。
- state 初期可以使用本地后端（local state），等到需要团队协作时再演进到 remote backend。
- 与 wordloom-v3 的连接优先采用「本机 API/worker 连接云上 DB/存储」的混合模式，而不是一开始就部署整个 app 到云上。

**Non-goals（不做什么）**:

- 不在本 epic 中构建生产级多区域/多账号拓扑；
- 不在早期阶段引入 Kubernetes/EKS/AKS 等容器编排（仅在后续 roadmap 中作为扩展方向提及）；
- 不在 Terraform 中混入应用层配置（保持 infra 与 app 配置解耦，应用仍通过 env / config 管理）。

## Background（背景）

- `road-S1` 中 M3/M5 已经提出「IaC & infrastructure primitives（Terraform + dev/test env → 云基础）」的长期目标，但具体练习路径容易和其他内容纠缠在一起。
- 你当前几乎没有云平台实战经验，希望有一条从 0 开始、围绕 wordloom-v3 的最小实践路线：从开账号 > 建网络 > 开托管 Postgres/存储 > 让本机 API 连上云资源。
- 之前的 `road-S1-2` 尝试把这条路线写成子 road，但与 logs/phase 的角色有一定重叠；因此本次改造把它收口成 S4C epic + phase logs，road 只保留高层路线。

## Constraints（约束）

- 预算与安全边界必须在 P0 阶段说明清楚：仅使用免费层或低成本资源，不在云上保存敏感/生产数据；
- 每一个 `apply` 都需要可追溯 evidence（headSha + state 路径 + 控制台截图/CLI 输出要点）；
- Terraform 目录结构和命名需要在 P0 固定下来，以便后续模块扩展不会引入混乱；
- 尽量避免在一个 phase 内同时修改大量资源类型，保持迭代粒度可控。

## Scope（本 log 范围）

- 本 log 负责：
  - 定义 cloud dev/test infra + Terraform 的目标边界、默认基线、切片拆分（1A/2A/3A 等）与里程碑；
  - 作为 wordloom-v3 在云上练习的索引入口，指向具体 phase logs、Terraform 模块与 evidence。
- 本 log 不负责：
  - 具体 Terraform 资源参数的细节（落在各 phase logs 与代码中）；
  - 安全治理/审计/多账号策略（由 S5A/S5B 以及将来专门的安全/治理 epic 承接）。

## Success Criteria（DoD）

- 结构层面：
  - 读者在 30 秒内能理解 S4C 要解决什么问题、目前到哪一步、下一步做什么；
  - 能够通过 links 迅速跳转到对应的 phase log 和 Terraform 模块目录。
- 工程层面：
  - 至少有 1 套 Terraform 模块可以在 dev/test 账号上成功 `plan/apply/destroy`；
  - wordloom-v3 本机 API 能够在一个独立的 env（例如 `.env.cloud.dev`）下连接到云上的托管 Postgres 或对象存储。
- 证据层面：
  - 每个 phase 至少有 1 条 evidence（headSha + state 路径 + 关键命令输出），并在本 epic 中有索引。

## Phases（切片）

- `S4C-1A`（Phase 1）：Cloud dev/test bootstrap（账号 + CLI + 最小目录结构 + 词汇表）
  - 详见：`docs/logs/log-S4C-1A-cloud-devtest-terraform-bootstrap.md`
- `S4C-2A`（Phase 2）：Network + managed Postgres + storage modules（dev/test only）
  - 详见：`docs/logs/log-S4C-2A-cloud-devtest-db-and-storage.md`（未来创建）
- `S4C-3A`（Phase 3）：Connect wordloom-v3 runtimes to cloud infra（env + drills）
  - 详见：`docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`（未来创建）

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`: S4C contract/indexing 完成（epic + S4C-1A P0/P1/P2/P3）
- [x] `P1`: S4C-1A 完成账号/CLI/目录结构最小落地 + 首次 plan drill
- [ ] `P2`: S4C-2A 最小网络 + DB + 存储模块可 `plan/apply/destroy`
- [ ] `P3`: S4C-3A 完成一次从本机 API 连接云上 DB 的 drill，并写入 Evidence。

## Current Status（进展摘要）

- 当前：S4C-1A 已标记为 `stable`，AWS playground 账号、Terraform toolchain 与最小 S3 示例模块均可正常 `plan`；
- S4C-2A 已创建 phase skeleton 与 `infra/terraform/aws/{network,devtest-db}` 目录，但尚未有真正的网络/DB 资源定义或 `apply`；
- 关键风险：后续 RDS/网络资源需要持续关注成本与清理策略，避免遗留 dev/test 资源长期运行。

## Notes（落地原则，可选）

- 优先选择文档和社区资源丰富的云平台（AWS/Azure 其一）作为首选；
- 所有练习以「可随时销毁、不要留悬挂资源」为原则；
- 若未来需要多云对比，应通过 notes/roadmap 做 narrative，而不是在同一个 Terraform 目录混合多云 provider。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - S4C 的目标边界、phase 拆分与 evidence 口径稳定；
  - 至少 S4C-1A/S4C-2A 已经完成，并有可复用的 Terraform 模板和 drills；
  - 对 wordloom-v3 如何连接云上 dev/test infra 有一条清晰的、可演示的路径。

## Numbering & Commit Naming（编号与提交命名）

- 编号约定：`P<n>` 表示 Phase，`C<n>` 表示 Cycle，`S<n>` 表示 Step。
- Commit / PR 命名：
  - 基础形式：`S4C-<phase>/P<phase>-C<cycle>-S<steps>: <summary>`，例如：
    - `S4C-1A/P0-C1-S1: bootstrap AWS playground account`。
  - `<steps>` 可以是单个 step（`1`，即 `...-S1`），也可以是在同一 phase / cycle 下连续的多个 step 合并（如 `1S2`，即 `...-S1S2`）。

**Branch 约定（建议）**:

- 与本 epic 相关的改动，优先落在以 `S4C-<summary>` 命名的长期工作分支上（本次为 `S4C-cloud-services-and-terraform-minimal-path`）。
- 若一次演进涉及其他 scope/index（例如 S5B 的安全治理），推荐拆分为单独分支/PR，保持证据链清晰。

**Commit 纪律（建议）**:

- 完成每个 `P*-C*-S*` 的关键内容后，应在 `S4C-*` 分支上及时 `commit/push`；
- 仅当某个 phase 体量较大、需要多人协同时，才在该分支之下再建短生命周期子分支，避免碎片化。

## Recent changes（for traceability，可选）

- 2026-03-22：创建 `S4C` epic skeleton，用于承接原 `road-S1-2` 中的 cloud + Terraform 最小路径内容，将详细实践下放到 phase logs 与 Terraform 模块中。
