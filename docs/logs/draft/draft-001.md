可以做，而且应该做，但要先把“文档对象模型”改掉，再改单个 contract。你现在要的不是给现有 contract 多补几列，而是把整个治理链从“release/log 驱动的读物”重构成“code-oriented semantics 驱动的审计系统”。我建议把它拆成三层：

Current Contract：只表达“当前生效语义”，是最新语义视图，不按 release 排序。
Semantic Chronology：表达“语义怎么一步步变成现在这样”，按语义生效时间排序，不按 release 排序。
Evidence Intake / Writeback Ledger：表达“这次谁拿了什么证据、准备怎么写回、最终写回了什么”，这是操作层，不应该再冒充语义主表。
你现在 DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md 这份文件，已经有 statement / bridge / coverage / evolution，但本质上还是“release-first contract”。它兼容历史，但不够适合你现在要的“从 code 反推最新语义，再用 chronology sharpen”的方法。核心问题不是它不能记历史，而是它把“当前语义”“历史变更”“证据 intake”混在一起了。

成熟做法
应该把 contract 从“条款集合”升级成“语义面清单 + 证据挂载 + 历史演化”三件事分离：

Contract Face Table
每一行对应 checklist 的一个 face，不再先写 statement，再零散补 bridge/coverage；而是先以 9 面为骨架。
建议 9 行固定下来：
owner boundary
stable entrypoint
application bridge
domain invariants
critical data shape
persistence continuity
observability minimum set
control/fallback boundary
verification surface
每一行至少要有这些字段：

face_id
face_name
semantic_status
semantic_strength
current_semantic_text
code_truth_kind
primary_code_refs
supporting_refs
source_basis
effective_from
effective_until
recorded_at
last_changed_at
actor
change_reason
replacement_rule
notes
这里最关键的是两列：

semantic_status：例如 owned-now / partially-owned / boundary-only / not-owned-here
semantic_strength：替代你现在比较分散的 defended-now / code-anchor-only / bridged-now
我建议把强度统一成一套枚举，避免 statement/coverage/bridge 各说各话：

code-observed
code-anchored
evidence-supported
defended-now
historically-retained
superseded
这样一来，“有代码但还没形成可治理语义”和“已经是 contract 当前承诺”就能明确区分。

Code Evidence Table
这不是 runbook，也不是 contract clause，而是“代码事实挂载表”。每个 face 可以挂多个 code block。
字段建议：
evidence_id
face_id
evidence_kind：entrypoint / domain-flow / config-switch / schema-shape / signal-emission / verification-hook
repo_ref
symbol_or_block
observed_semantic
confidence
observed_at
recorded_at
actor
source_packet_or_ledger
notes
这张表负责解决你说的“不是简单拥有/没有字段，而是和 defended / anchor 有关联”的问题。因为 contract face 是治理结论，code evidence 是事实基础，二者不要混写。

Semantic Chronology Table
这是你现在最缺的。它必须按语义时间排序，不按 release 排序，允许插入中间历史。
字段建议：
chronology_id
face_id
change_type：introduced / clarified / narrowed / widened / split / superseded / backfilled-audit
semantic_before
semantic_after
effective_from
effective_until
observed_at
recorded_at
actor
basis_refs
source_release_rows
source_scenario_rows
source_routing_event_ids
chronology_order_key
notes
这里的 chronology_order_key 不应该依赖 release id。应该是可排序的时间键，比如：

c
h
r
o
n
o
l
o
g
y
_
o
r
d
e
r
_
k
e
y
=
e
f
f
e
c
t
i
v
e
_
f
r
o
m
+
o
b
s
e
r
v
e
d
_
a
t
+
r
e
c
o
r
d
e
d
_
a
t
+
c
h
r
o
n
o
l
o
g
y
_
i
d
chronology_order_key=effective_from+observed_at+recorded_at+chronology_id
这样即使后来发现一个旧语义或中间语义，也能插进去，不破坏当前 contract 的最新视图。

怎么处理“代码变了，contract 怎么跟着变”
成熟做法不是直接改 contract 主文，而是走一条标准写回链：

发现代码语义变化
来源可以是代码 diff、PR、migration、test 改动、lab、incident、runbook drill。

先产出一次 Semantic Intake Packet
它不是旧式“先从日志抽结论”，而是“先从代码和验证材料抽当前语义变化候选”。

Packet 进入 Writeback Ledger
ledger 只记录：

变更候选是什么
证据是什么
属于哪个 face
建议动作是什么：no-writeback / clarify / narrow / widen / split-contract / move-to-runbook
审核通过后，改 Current Contract
只改受影响的 face 行，必要时更新 code evidence 行。

同时追加 Semantic Chronology
永远追加，不覆盖。这样当前视图保持干净，历史也不丢。

最后在 ledger 里记录 writeback 完成
这时 ledger 是审计收口，不再承担“当前语义阅读”的职责。

所以你问“这些变化的文字来源根据是什么地方”，成熟答案是三层来源：

primary: 代码与 schema / config / tests / entrypoints
supporting: labs / run results / incidents / operator evidence
governance: packet / ledger / approval notes
文字上应该优先从 primary 归纳，再用 supporting sharpen，不能反过来。

对 OBSERVABILITY-0001 的具体改造建议
如果从 DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md 开始，我建议不要直接在原表上继续堆列，而是做一次 pilot 重排。

第一阶段，只做结构迁移，不扩大语义：

保留现有 frontmatter 的审计字段。
把 Contract Statement Table 重组为 Contract Face Table。
把现有 Code Bridge Table 和 Contract Coverage Table 的内容，拆进：
Current Contract Face Table
Code Evidence Table
新增 Semantic Chronology Table，先把现有 release/evolution 里能还原出的历史搬进去。
现有 Statement Evolution Table、Code Bridge Evolution Table、Coverage Evolution Table 不一定立刻删除，可以先降级为迁移期兼容层。
第二阶段，补 checklist 9 面缺口：
以当前 OBSERVABILITY-0001 看，大概率会是这样：

owner boundary：已有，强
stable entrypoint：已有，强
application bridge：部分有，需要从 worker entry -> impl -> scenario glue 补齐
domain invariants：弱，目前更像“诊断可追”要求，还没把领域不变量说清
critical data shape：弱，需要补 trace_id / claim_batch_id / outbox event id / projection/op 的 shape 和 continuity
persistence continuity：弱，需要明确 DB reason family movement 和 outbox state continuity 的契约位置
observability minimum set：已有，强
control/fallback boundary：有边界，但还是 negative boundary，不够成熟
verification surface：已有 proof path，但还没形成统一 verification face
也就是说，OBSERVABILITY-0001 很适合做 pilot，因为它不是全空白，但也没有成熟到难以重构。

旧 ledger 能不能沿用
不能完全沿用，但也不用推倒重来。我的判断是：

旧 release-ledger 可以保留。
用途改成：
intake
routing
writeback decision
audit closure
旧办法不能继续承担“语义主抽取器”。
因为它天然偏 release-first、packet-first，不适合 code-first semantics。

需要新增至少两类 template：

contract-face extraction ledger
semantic chronology ledger
我建议新模板至少有这三份：

ledger-CONTRACT-FACE-EXTRACTION-xxxx.md
用途：从代码侧抽 face 候选。
输入是 code refs、tests、schema、config、runtime signals。
输出是 face 级候选语义，不直接写 current contract。

ledger-SEMANTIC-CHRONOLOGY-SHARPENING-xxxx.md
用途：把 source logs、旧 release、incident、lab 的历史材料整理成时间序视图。
重点是：

observed_at
recorded_at
effective_from/until
actor
insertion point
supersedes / clarifies / narrows / widens
ledger-CONTRACT-WRITEBACK-xxxx.md
用途：最终决定写回 current contract 哪些 face，怎么改文案，谁审批，何时生效。
这样旧的 SUP -> ledger -> contract/runbook 还能保留，但中间 ledger 的职责要拆细。否则一份 ledger 又抽证据、又排历史、又做 writeback，最后还是会混。

建议的 contract 新版骨架
如果你要的是成熟版，我建议 OBSERVABILITY-0001 未来主文长这样：

frontmatter
保留治理元数据、owner、approval、active window、actor、source refs。

Current Contract Faces
9 行固定表。这里是“今天生效的语义”。

Code Evidence Attachments
按 face 挂代码块和验证钩子。

Semantic Chronology
按时间排序，不按 release 排序。

Current Gaps and Non-Ownership
明确哪些 face 只是 boundary-only 或 not-owned-here。

Writeback Rules
说明以后什么变化必须触发 contract 改写，什么只进 runbook，什么只进 chronology。

这里第 6 节很重要。否则以后代码变了，团队还是不知道什么时候该动 contract。

触发规则我建议写死
比如：

变更 stable entrypoint：必须改 contract face + chronology
变更 owner boundary：必须改 contract face + chronology + approval
变更 minimum signal set：必须改 contract face + code evidence + chronology
新增一个 drill proof path：如果只是验证增强，可只加 evidence；如果改变“当前 defended proof path”，必须改 face
新增 shadow/dual-run/cutover procedure：默认不进 contract，先判定是否属于 control/fallback boundary；否则进 runbook
历史材料只补审计字段、不改当前语义：只进 chronology，不改 current contract
这套规则一旦落地，后面的仓库治理才会稳定。

如果现在就从 OBSERVABILITY-0001 开始，建议这样落地

先不大面积改仓库，先做一个 pilot 模板。
先把 OBSERVABILITY-0001 重构成新骨架，但语义不扩张，只重排。
同时新增一个 code-first extraction ledger 模板。
再新增一个 time-ordered chronology 模板。
用 OBSERVABILITY-0001 跑完整链条，确认：
face 怎么抽
chronology 怎么插中间历史
writeback 怎么收口
跑通后，再回头改 contract template 和 runbook/ledger template。
我的结论很明确：需要新 template，而且不能继续沿用旧的“直接从 release/log 组织 contract”的办法。旧资产还能复用，但要降级成证据来源和审计来源；主语义必须改成 code-oriented current contract，历史则单独做 chronology 视图。

如果你要，我下一步可以直接做两件事之一：

先给你产出一版 OBSERVABILITY-0001 的新 contract 模板骨架，只改结构不改语义。
先给你产出三份新 ledger/template 草案：face extraction、chronology sharpening、contract writeback。

可以，而且这件事必须先定规则，不然后面一定会重新回到“所有变化都往一个 contract 里堆”的状态。

我的判断是：contract 不应该是“永远长一份主文档”，而应该是“同一 contract family 下的一系列 release”。每个 release 表示一个在当时可成立、可审计、可阅读的“当前语义快照”。历史不是靠不断改老 release 维持，而是靠：

老 release 保留不动。
新语义出来时开新 release。
用 chronology 和 supersede 链把它们串起来。
front-door/index 永远指向当前生效 release。
核心原则只有一句话：

新 release 不是“材料变多了”，而是“当前 contract 语义变了”。

先把变化分层
我建议以后所有变化先分成 4 类，再决定要不要开新 release。

Evidence-only
代码没变语义，只是补证据、补时间窗、补 actor、补来源、补旧历史。
这种不应该开新 release。
它应该只进：
chronology
support-only writeback ledger
evidence attachment
Clarification-only
文字更清楚了，但“当前要求/边界/责任/验证面”没有变化。
这种通常也不应该开新 release。
但要严格限制，只能是“不改变 reader 结论”的澄清。

Semantic change
当前 contract 的任何一个 face 的有效语义变了。
这种就应该开新 release。

Boundary restructure
不是单纯语义变化，而是 contract 的归属边界变了，比如 split、merge、换 owner surface、从一个 family 拆成两个 family。
这种一定开新 release，而且通常还要带 lineage 字段：

supersedes
split_from
split_into
absorbed_from
retired_by
什么情况必须开新 release
成熟做法里，我建议把触发条件写死。只要命中任一条，就不要继续往当前 release 里堆。

owner boundary 变了
例如从 search outbox worker 扩到另一条 worker chain，或者 owner team 变了。

stable entrypoint 变了
入口脚本、主调用链、主治理附着点变了。

application bridge 变了
原来 contract 附着在 A->B->C，现在变成 A->D->C，且这会改变语义解释或验证路径。

domain invariants 变了
例如“必须保留哪些 shared pivots”“什么算 diagnosable”发生了变化。

critical data shape 变了
关键字段、关联键、事件形状、状态形状变了，而且 reader 对 contract 的理解会变。

persistence continuity 变了
比如 DB movement、outbox continuity、state transition 的 contract 承诺变了。

observability minimum set 变了
最小指标、trace、日志、pivot 集合变了。

control/fallback boundary 变了
原来不属于 contract 的 fallback / switch / degraded semantics，现在被 contract 正式接管，或者反过来移出。

verification surface 变了
当前 defended proof path 变了，或者“证明 contract 成立”的最小验证面变了。

上面任一项变化，本质上都不是“补材料”，而是“当前 contract 是什么”发生了变化，所以应该开新 release。

什么情况不应该开新 release
这些可以留在当前 release 体系下，用 chronology 或 ledger 收口：

补旧证据，但不改变当前语义。
给现有 code block 补更精确的定位。
补 actor、recorded_at、effective window。
把旧 source log 插入时间线中间，纯粹 sharpen 历史。
wording cleanup，但不改变当前 reader 的结论。
新 runbook/operator 步骤出现，但 contract 边界没有变。
新实验、lab、incident 只是支持现有结论，没有改变 contract 承诺。
关键边界：不是“代码变了就开 release”，而是“代码语义映射到 contract face 变了才开 release”
这个边界要非常明确。

比如：

代码重构，但 stable entrypoint 和语义不变，不开。
新增内部 helper，不开。
trace 实现细节换了，但 minimum signal set 没变，通常不开。
proof path 从 es_write_block_4xx 改成别的 path，开。
原来 shadow/dual-run 不属于 contract，现在正式纳入 control boundary，开。
所以以后不能用“代码有 diff”来驱动 release，而要用“face-level semantic delta”来驱动。

我建议加一个 release decision gate
以后每次 writeback 前，先做一个很小的判定表，逐 face 看是否发生 semantic delta。

建议就叫 Release Decision Table，每次 packet 都填一次：

face_id
current_release_semantic
candidate_semantic
delta_class
reader_visible_change
contract_action
其中 contract_action 只允许这几种：

no-release
same-release-evidence-writeback
new-release-required
split-family-required
move-to-runbook
retain-in-chronology-only
这样就不会再靠感觉决定。

我更建议 release 不可变
这是重点。我的建议是：

一个 contract release 一旦形成“当前语义快照”，就尽量不要再改它的语义正文。
老 release 最多只允许：
审计字段补全
链接修正
明确标记 superseded
补 chronology backfill
任何当前语义变化，都去开下一个 release。
也就是说，未来不应该把 OBSERVABILITY-0001 一直改成越来越长的大杂烩；而应该在它语义变更时开：

OBSERVABILITY-0002
OBSERVABILITY-0003
然后 index/front-door 指向最新版本。

这样你的“基于现在代码追过去历史”的模型才稳，因为“现在”永远是一个清楚的 release，而不是一份被多年补丁反复改写的文档。

那旧 release 还有什么价值
价值很大。它不是废档，而是：

当时生效的 contract 快照。
chronology 的锚点。
审计和责任的固定切片。
新 release 的 supersedes 依据。
所以仓库里应该形成这样的结构：

contract family
release 0001
release 0002
release 0003
front-door current
semantic chronology cross-release view
前者负责“当时是什么”，后者负责“怎么变成现在”。

对 OBSERVABILITY-0001，我建议用这个策略
如果从它开始治理，我会这样定：

OBSERVABILITY-0001 作为第一代窄边界 release 保留。
先把它重构成你前面说的 code-oriented face 模型，但这次重构尽量定义为“结构迁移，不改变正面语义”。
以后凡是下面这些变化，就直接开 0002：
bounded owner surface 扩大
current defended proof path 改变
minimum signal set 改变
shadow/dual-run 被正式吸入 contract ownership
verification surface 被重定义
如果只是补历史、补时间窗、补 actor、补 source basis，就不要再动 release 编号。
这意味着 0001 不该继续无限增厚，它应该作为“第一代当前 contract”的冻结点存在。

我建议再补一条版本策略
为了避免以后争议，我建议直接约定 3 个 release level：

Audit patch
不变更语义，不升 release，只写 ledger/chronology。

Semantic release
同 family 下新 release，例如 0001 -> 0002。

Lineage release
涉及 split/merge/retire，不只是 0002，还要更新 family 关系。

如果你愿意更严格，还可以加一条：只要 Current Contract Faces 表里任意一行的 current_semantic_text 需要改，默认就是新 release；除非能明确证明只是拼写或等义改写。

这个规则很硬，但长期会省很多事。

结论
这件事不能靠“当前 contract 一直往里补”。成熟做法是：

contract release 代表当前语义快照
chronology 代表时间序历史
ledger 代表证据 intake 和 writeback 决策
front-door 代表当前生效入口
判断是否开新 release，不看材料多少，也不看代码有没有 diff，而看 9 个 face 里有没有 reader-visible semantic delta。

如果你要，我下一步可以直接继续往前推进两种之一：

我先帮你写一份“contract release 判定规则”草案，做成一个可复用模板，专门定义什么叫 new release、什么叫 same-release writeback。
我直接拿 OBSERVABILITY-0001 做样板，给它设计一版 0001 -> 0002 的判定门和 lineage 结构。