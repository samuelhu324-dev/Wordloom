# log-S5A-3B-object-storage-backup（Phase 4：Object storage backup platformization v1）

---

**id**: `S5A-3B`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `dev/test backup artifacts to object storage (minio/S3) + lifecycle + drill evidence v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S5`
**tags**: `EVOLUTION, Security, Governance, Backup, ObjectStorage, S3, MinIO, Lifecycle, Drills, Evidence, epic/s5, sub/3b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S5A-security-governance.md`
  **previous_log**: `docs/logs/log-S5A-3A-backup-sanitization.md`
**created**: `2026-03-03`
**updated**: `2026-03-03`

---

## Decision / Outcome（结论区）

**Decision**:

- 在 `S5A-3A` 完成“本地 artifacts 可恢复备份 + restore drill + sanitization”后，将备份产物的存储从本地 `artifacts/` 演进为 **对象存储（MinIO/S3 兼容）**，形成可持续的“可备份、可演练、可证据化”的平台化路径。

**Default choices（本 phase 默认决策）**:

- **对象存储实现（dev/test）**：MinIO（S3 兼容）。
- **存储的对象**：dump 文件（不入 git）与 evidence JSON（可入 git）两条线并存：
  - dump：上传到对象存储（bucket + prefix）
  - evidence JSON：仍然写到 `artifacts/_tmp_*` 并可选择性提交（只含元数据/校验值/对象 key，不含 dump）
- **生命周期（lifecycle）**：
  - dump：默认 7 天过期（dev/test）
  - evidence：不在对象存储强制过期（由 git 或 artifacts 目录策略决定）

## Definitions（概念定义）

- **对象存储（S3 兼容）**：以 bucket/object key 方式存储二进制/大文件。
- **Lifecycle**：针对 bucket/prefix 的过期删除（expire）策略，降低 dump 长期留存风险。
- **Manifest / Evidence**：
  - manifest：描述 dump 元数据（size/sha256/created_at/object_key）
  - evidence：drill 输出 JSON，引用 manifest/object_key，作为事实源。

## Constraints（约束）

- **不引入生产级复杂度**：本 phase 仅覆盖 dev/test 的最小闭环；不做 IAM/多账户/跨区域复制。
- **dump 不入 git**：仍保持 dump 不提交仓库，只上传到对象存储。
- **最小权限**：MinIO 使用独立 access key（dev/test），后续再演进到更严格策略。
- **证据纪律**：每次 drill 产出 evidence JSON，包含 bucket/key/sha256/size/restore 验证结果。

## Scope（本 log 范围）

- `P0`：contract（bucket/key 命名、生命周期、证据口径）
- `P1`：infra（MinIO dev/test）+ 上传脚本（dump → object storage）
- `P2`：restore drill（从 object storage 拉取 dump → restore 到新库 → verify）

## Success Criteria（DoD）

- 能在 dev/test 运行 MinIO（本地 docker compose）。
- 能把 dump 上传到对象存储，并记录 sha256/size/object_key。
- 能从对象存储下载 dump 并完成 restore+verify drill。
- 能为上述 drill 产出 evidence JSON，并在本 log 记录 headSha + artifacts 路径。

## P0（Contract｜v1）

### P0-C1-S1（对象存储 contract｜v1）

- bucket：`wordloom-backups-devtest`（dev/test 默认）
- key：`s5a3a/<YYYY-MM-DD>/<db_name>/<timestamp>.dump`
- manifest：`s5a3a/<YYYY-MM-DD>/<db_name>/<timestamp>.manifest.json`

### P0-C1-S2（生命周期 contract｜v1）

- dump：默认 7 天过期（bucket lifecycle rule）
- manifest：默认与 dump 同期（或更短）

### P0-C1-S3（证据口径 contract｜v1）

- evidence JSON 必须包含：
  - bucket + object_key + sha256 + size
  - restore target db + verify 结果摘要
  - 使用的 compose file / service / 时间戳

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S5A-3B/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P1（MinIO + upload）

- P1-C1-S1：在 `docker-compose.infra.yml` 增加 MinIO（dev/test）
- P1-C1-S2：实现 upload 脚本：dump → bucket/key（带 sha256/size/manifest）
- P1-C1-S3：upload drill + artifacts（evidence JSON）

### P2（Restore drill from object storage）

- P2-C1-S1：实现 download 脚本：bucket/key → 本地临时文件
- P2-C1-S2：restore + verify drill（复用 `S5A-3A` restore 逻辑）+ artifacts

## Execution Checklist（unchecked）

### P0（Contract）

- [ ] `P0-C1-S1`：对象存储 contract（bucket/key/manifest）
- [ ] `P0-C1-S2`：生命周期 contract（dump/manifest 过期）
- [ ] `P0-C1-S3`：证据口径 contract（evidence 字段）

### P1（MinIO + upload）

- [ ] `P1-C1-S1`：MinIO dev/test infra（compose）
- [ ] `P1-C1-S2`：upload 脚本（dump → bucket/key + manifest）
- [ ] `P1-C1-S3`：upload drill + artifacts

### P2（Restore drill from object storage）

- [ ] `P2-C1-S1`：download 脚本（bucket/key → 本地）
- [ ] `P2-C1-S2`：restore+verify drill + artifacts

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径。

### P1-C1-S3（upload drill｜YYYY-MM-DD）

- headSha：`__HEAD_SHA_AFTER_COMMIT__`
- artifacts：`artifacts/_tmp_s5a3a_pXcXsX/drills_<ts>.json`
- bucket/key：`s5a3a/<YYYY-MM-DD>/<db_name>/<timestamp>.dump`

### P2-C1-S2（download+restore+verify drill｜YYYY-MM-DD）

- headSha：`__HEAD_SHA_AFTER_COMMIT__`
- artifacts：`artifacts/_tmp_s5a3a_pXcXsX/drills_<ts>.json`
- restore target db：`wordloom_restore_dev`
