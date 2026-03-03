# log-S5A-3A-backup-sanitization（Phase 3：DB backup + restore drill + sanitization v1）

---

**id**: `S5A-3A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `dev/test recoverable backup + restore drill + sanitization (masking) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S5`
**tags**: `EVOLUTION, Security, Governance, MultiTenant, Backup, Restore, Sanitization, Masking, Postgres, Drills, Evidence, epic/s5, sub/3a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S5A-security-governance.md`
  **previous_log**: `docs/logs/log-S5A-2A-library-membership-roles-policy-audit.md`
**created**: `2026-03-03`
**updated**: `2026-03-03`

---

## Decision / Outcome（结论区）

**Decision**:

- 将“路线 C”里的 **数据备份/脱敏策略** 落为可演练、可证据化的最小闭环（优先 dev/test）：
  - 先跑通“**备份 → 恢复到新库 → 验证**”的恢复演练（recoverability first）。
  - 脱敏优先在“恢复后的副本库”执行（不在主库改写），默认不可逆、低风险。
  - 产出 drills + artifacts 证据链；后续再演进到对象存储（S3/minio）与更严格匿名化。

**Default choices（本 phase 默认决策）**:

- **存储**：本地 `artifacts/`（仅 dev/test / CI 产物）。
- **用途**：开发/测试可重置的副本（不对外提供数据集）。
- **RPO/RTO（工程默认值）**：`RPO=24h`（每日备份）/ `RTO=1h`（1 小时内恢复出可用新库）。

## Definitions（概念定义）

### 什么叫“数据脱敏”（sanitization / masking）？

- 数据脱敏是：对一份真实数据的**拷贝/副本**（通常用于 dev/test/排障/演练）进行处理，把敏感信息替换为“看起来像真数据但无法指向真实个体”的形式，同时尽量保留结构与可测试性。
- 本 phase 的落地方向：**恢复到新库后做 SQL 脱敏**（最小风险），不在源库改写。

### RPO / RTO 是什么意思？

- **RPO（Recovery Point Objective）**：最多允许丢失多少数据（恢复点）。例：RPO=24h 表示最坏丢失 24 小时内的数据变更。
- **RTO（Recovery Time Objective）**：故障到恢复可用的最长允许时间（恢复时长）。例：RTO=1h 表示 1 小时内恢复出可用的新库。

## Constraints（约束）

- **先 recoverability，后 platformization**：先把闭环跑通，不引入对象存储/云权限/生命周期等复杂度。
- **脱敏默认不可逆**：优先替换/置空；避免可逆加密与“部分保留”导致边界不清。
- **证据纪律**：每次 drill 产出 artifacts（JSON），包含输入参数与输出产物路径；不依赖人工截图。
- **多租户意识**：脱敏策略需考虑 `library_id`（tenant）字段与跨租户隔离；至少保证不会引入跨 tenant 的拼接数据。

## Scope（本 log 范围）

- `P0`：contract（默认决策、RPO/RTO、脱敏策略 v1、证据口径）
- `P1`：备份（pg_dump）→ 落地 artifacts
- `P2`：恢复演练（restore 到新库）→ 验证可用性
- `P3`：脱敏（恢复库上执行 SQL sanitization）→ 验证不可逆 + 行为不崩

## Success Criteria（DoD）

- 备份：
  - 能生成可恢复的备份产物（至少 1 个 dump 文件），落在 `artifacts/`。
- 恢复：
  - 能从备份恢复到一个新的数据库（例如 `wordloom_restore_dev`），并通过最小验证（连通性 + 基础查询/表存在）。
- 脱敏：
  - 在恢复库上执行脱敏脚本后：
    - 明显 PII 字段已替换/置空（不可逆）。
    - 自由文本字段（notes/description 等）已清空（降低泄露风险）。
- 证据：
  - 至少 2 个 drills，产出 artifacts（JSON）：
    - backup+restore drill
    - restore+sanitize drill

## P0（Contract｜v1）

### P0-C1-S1（备份 contract｜v1）

- 备份类型：v1 采用逻辑备份（`pg_dump`）。
- 产物位置：`artifacts/_tmp_s5a3a_<step>/`。
- 命名：包含时间戳（便于 evidence 对齐）。

### P0-C1-S2（恢复演练 contract｜v1）

- 恢复目标：恢复到一个 **新库名**（避免覆盖源库）。
- 验证：至少包含一次只读校验（如列出关键表/抽样 row count）。

### P0-C1-S3（脱敏策略 contract｜v1）

- 默认不可逆。
- 覆盖优先级（从易到难）：
  - 替换：email/phone/name → `user_<id>@example.com` / `000000...`
  - 置空：notes/自由文本/地址类字段 → 空字符串或 NULL
  - 重置：token/secret/session → NULL/固定占位

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S5A-3A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P1（Backup）

- P1-C1-S1：新增 `pg_dump` 备份脚本（Windows PS + Linux bash 任选其一，优先兼容 devtest DB）
- P1-C1-S2：把 dump 产物写入 `artifacts/_tmp_s5a3a_p1c1s1/` 并写出 JSON 元数据（drill artifacts）

### P2（Restore drill）

- P2-C1-S1：新增 restore 脚本：从 dump 恢复到新库（例如 `wordloom_restore_dev`）
- P2-C1-S2：新增验证步骤（最小 SQL 校验），结果写入 drill artifacts

### P3（Sanitization）

- P3-C1-S1：新增 SQL 脱敏脚本（在恢复库上执行）
- P3-C1-S2：新增验证步骤：抽样检查关键字段已脱敏；结果写入 drill artifacts

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：备份 contract（类型/产物/命名）
- [x] `P0-C1-S2`：恢复演练 contract（新库 + 验证）
- [x] `P0-C1-S3`：脱敏策略 contract（不可逆 + 覆盖优先级）

### P1（Backup）

- [x] `P1-C1-S1`：实现备份脚本（pg_dump）
- [x] `P1-C1-S2`：backup drill + artifacts

### P2（Restore drill）

- [x] `P2-C1-S1`：实现 restore 脚本（恢复到新库）
- [x] `P2-C1-S2`：restore 验证 + artifacts

### P3（Sanitization）

- [x] `P3-C1-S1`：实现脱敏 SQL 脚本（恢复库上跑）
- [x] `P3-C1-S2`：sanitize 验证 + artifacts

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径。
- 本 phase 完成后，在此追加每次 drill 的记录（含 `DATABASE_URL`/目标库名/产物路径）。

### P1-C1-S2（backup drill｜2026-03-03）

- headSha：`8e471442fd81ef3622c86d27a99c4b5077e869cb`
- artifacts（evidence JSON）：`artifacts/_tmp_s5a3a_p1c1s2/drills_1772527633.json`
- dump（本地文件，不入 git）：`artifacts/_tmp_s5a3a_p1c1s2/wordloom_wordloom_dev_<ts>.dump`
- env（示例）：
  - `docker compose -f docker-compose.devtest-db.yml up -d`
  - service：`db_devtest` / db：`wordloom_dev`

### P2-C1-S2（restore+verify drill｜2026-03-03）

- headSha：`bed34296cc70e554caa17e62b48ee77291825dae`
- artifacts（evidence JSON）：`artifacts/_tmp_s5a3a_p2c1s2/drills_1772528419.json`
- restore target db：`wordloom_restore_dev`
- env（示例）：
  - service：`db_devtest` / source dump：`artifacts/_tmp_s5a3a_p1c1s2/wordloom_wordloom_dev_<ts>.dump`

### P3-C1-S2（restore+sanitize+verify drill｜2026-03-03）

- headSha：`65f8a77d1f2a218b1a3b2312650d46a7a0dda5d8`
- artifacts（evidence JSON）：`artifacts/_tmp_s5a3a_p3c1s2/drills_1772531253.json`
- restore target db：`wordloom_restore_dev`
- sanitize SQL：`scripts/backup/s5a3a_p3c1s1_sanitize_restore_db.sql`
- verify SQL：`scripts/backup/s5a3a_p3c1s2_verify_sanitization.sql`
