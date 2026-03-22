# log-S4C-3A (Phase 3: Connect wordloom-v3 runtimes to cloud dev/test infra)

---

**id**: `S4C-3A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `Cloud dev/test wordloom integration（env + smoke drills） v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S4`
**tags**: `EVOLUTION, Cloud, Terraform, Runtime, Drills, Evidence, epic/s4, sub/3a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S4C-cloud-services-and-terraform-epic.md`
  **previous_log**: `docs/logs/log-S4C-2A-cloud-devtest-db-and-storage.md`
  **reference_log_1**: `docs/logs/_template-log-phase-drills-evidence.md`
**created**: `2026-03-22`
**updated**: `2026-03-22`

---

## Decision / Outcome

**Decision**:

- 在 S4C-2A 已经证明 cloud-dev 网络与 Postgres 生命周期可控之后，继续推进到应用侧：让 wordloom-v3 的本机 runtime 能通过一套单独的 cloud-dev env 配置连接到云上的 DB / 存储；
- 重点不是“部署整套应用到云上”，而是先打通“本机 runtime -> 云上 dev/test infra”的稳定开发路径，并留下 smoke evidence。

**Default choices (phase defaults / v1)**:

- 优先采用 `.env.cloud.dev` 或等价配置文件来承接 cloud-dev 连接串，不污染现有本地 dev/test env；
- 先选择最小 smoke path，例如应用启动 + DB 连接检查 + 一条最小读写验证；
- 如需临时公网访问，只作为 drill 手段，成功后应尽快回收或切回更安全的访问路径。

## Constraints

- 本 phase 不要求把完整应用部署到 AWS，只要求本机 runtime 能稳定访问云上 dev/test infra；
- 所有凭证不得写入仓库，应用层配置通过本地 env 或安全参数注入；
- 每次 smoke drill 需要记录 headSha、env 名称、目标 endpoint 类型和结果摘要。

## Scope

- `P0`: contract（cloud-dev env 命名、配置边界、smoke evidence 约定）。
- `P1`: implementation（为 wordloom-v3 增加/整理 cloud-dev env 配置入口）。
- `P2`: drill / verify（运行一次本机 runtime -> 云上 DB/存储的 smoke drill）。
- `P3`: drill / wording（总结 cloud-dev runtime integration 的 narrative，并与 S4C-2A / road-S1 对齐）。

## Success Criteria (DoD)

- 应用层存在清晰的 cloud-dev 配置入口，不与本地默认 env 混淆；
- 至少完成一次本机 runtime 连接云上 DB 的 smoke drill，并记录 evidence；
- 能明确说明：哪些内容属于 infra（Terraform），哪些属于 runtime config（env / app settings）。

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`：cloud-dev env/config contract 固定
- [ ] `P0-C1-S2`：smoke evidence contract 固定

### P1（Implementation）

- [ ] `P1-C1-S1`：cloud-dev env/config 入口建立
- [ ] `P1-C1-S2`：最小 smoke script 或 run path 就绪

### P2（Drill / Verify）

- [ ] `P2-C1-S1`：本机 runtime -> 云上 DB smoke drill 入账

### P3（Drill / Wording）

- [ ] `P3-C1-S1`：integration narrative 写入 docs

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records head SHA, env/config identifiers, and smoke results.

### P0-C1-S1（S4C-3A skeleton created｜2026-03-22）

- headSha: `<TBD-after-first-S4C-3A-commit>`
- artifacts:
  - `docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`
- expected:
  - 为 S4C-3A 定义最小目标：从本机 wordloom-v3 runtime 连接 cloud-dev infra，并形成 smoke/evidence 路径。
- observed:
  - 本 skeleton 已创建，等待后续 contract 与 implementation 落地。
