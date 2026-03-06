我更推荐的推进顺序（为什么）
建议 先深化路线 C，再深化路线 A。

原因很现实：路线 A 想做到“新增投影=填配置/复制模板”，最终一定会要求事件/回放/审计/actor 信息口径稳定；而这些“上下文与边界”的稳定来源，正是路线 C（AuthContext + policy + audit）。你现在如果先猛推 A，后面补 C 时会出现典型返工：投影里已经固化了不完整的 actor/tenant/trace 口径，再统一会很痛。

路线 C：推荐怎么深化（按 P/C/S 给你一条可闭环路线）
目标：把“散落的 owner check / if-else”升级成“统一骨架”，并能像你路线 B 一样用 drills/evidence 验证。

P0（Contract 收敛）：把“Actor/AuthContext/Policy/Audit 的最小字段 + 错误语义 + reason 白名单”固定下来
你已有 AuthContext contract 与 roles 来源（membership SoT + fallback）雏形：security.py
下一步是把“哪些动作必须审计、哪些拒绝必须带 reason、404 vs 403 的全局选择”固化成一份“不可随意漂移”的 contract（参考 log-S5A-1A-authcontext-policy-audit.md 的写法）。
P1（单一入口：Policy 收口）：让 handler/service 只做两件事：load resource（含 tenant filter）+ policy.check(...)
现在 policy 已有样板，但覆盖面不统一；建议选 1 条“最关键写链路”作为示范，把 Bookshelf/Book/Block 这些仍在用 actor_user_id/enforce_owner_check 的链路迁移到 AuthContext + policy（你能从测试里看到它们仍是旧骨架）。
P2（审计产品化）：把 audit 从“到处 try/except best-effort append”变成“统一 helper + 统一 action/result/reason 口径”
repo 已有 append-only 实现：audit_log_repository_impl.py
下一步重点不是加字段，而是：动作命名规范（membership.grant 这类已出现）、result 枚举（success/denied/not_found/error）、reason 低基数（not_member/not_admin/tenant_mismatch 这类）。
P3（像路线 B 一样做 drills/evidence）：做 3 个最小 drills（tenant 越权读 / role 不足写 / audit 完整性）并固定 artifacts 证据入口
这会把路线 C 从“架构设想”变成“可 hard-gate 的工程资产”，后面你做公开服务会非常值钱。
验收标准（你可以照抄成 checklist）：

每个需要权限的关键动作都能拿到 AuthContext（含 tenant_id/roles/request_id）。
所有拒绝都来自 policy（不是散落 if-else），并且 reason 可聚合。
audit 能用 request_id 把一次请求的授权、资源、结果串起来。

路线 A：推荐怎么深化（把“框架存在”变成“新增投影不手搓”）
你现在已经具备平台化的三件套：consumer 内核、projection harness、rebuild/backfill 模板。深化重点是“把 spec 真正用起来 + 把新增投影流程固化”。

P0（统一 event schema / scope key 落地）
outbox payload 的 schema_version 约束已经存在：payload_contract.py
projection spec 也有 scope_keys/payload_schema_version/requires 字段：spec.py
下一步建议：让 harness/adapter 在运行时真正校验这些 contract（比如 scope_keys 对应的列必须填、payload schema_version 必须匹配），这样“新增投影”不会靠人记住规则。
P1（consumer 模板彻底统一：从“每个投影一份 worker”到“一个 harness + 多个 adapter/spec”）
你已经有通用 worker harness：harness.py
也已经有两个 adapter（search/chronicle）：adapters
下一步就是把“新增投影”的动作固定成：写 adapter.apply → 注册 spec（参考 builtins.py）→ 复用 harness 运行。
P2（rebuild/backfill 继续走模板化 + catalog 化）
你已经有模板实现与契约日志：log-S2C-3A-projection-rebuild-backfill-template.md、log-S2C-5A-projection-backfill-template.md
下一步就是：每新增一个 projection，必须同时交付最小 rebuild smoke + backfill smoke（DB-only 先行），并纳入 catalog/CI（这一步会把“平台”变成“可复制”而不是“有一堆脚手架文件”）。
验收标准（路线 A 的“平台化”DoD）：

新增 projection 不需要复制粘贴 worker 主循环；最多新增 adapter + spec 注册。
rebuild/backfill 都能复用模板跑通，且能产出稳定 artifacts（像你路线 B 的 hard gate 一样可验证）。
reason/metrics/shared keys 不爆炸（低基数、可聚合、可排障）。
如果你愿意我给一个更“可执行”的版本：你选一个你接下来最想公开/最怕越权的用户链路（比如 Book 写入 / membership 管理 / search query），我可以把路线 C 的 P0–P3 切成 1～2 周的细颗粒 checklist，并明确每一步应该新增哪 1 个 drill 来做 hard-gate 证据闭环。