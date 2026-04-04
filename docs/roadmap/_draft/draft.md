1) 我希望接下来生成一份 S0E-docs-management-v5 的分支并把最近的内容 commit/push 到这上面；
2) 然后我想要按照 template 的结构， scaffold 一份 S0E-2A，具体内容如下：
3) 实现半自动化的 Git issue 创建，内容应该包括如下：

## title

一级固定词
二级自由描述
也就是标题格式改成：

SxY-ZA: <fixed-keyword>/<specific subject>

但是注意：这里的 <specific subject> 和 LOG 部分的 <summary> 是一类东西
比如 log-S4E-5B-execution-layer-enforcement-and-controlled-exceptions.md
生成的是 S4E-5B: governance/execution layer enforcement and controlled exceptions

所以其实自动化照顾到的主要是 <fixed-keyword>，Sxy-ZA 和 <specific subject> 可以用 log 现成的，能算上 "Full-automation"

我建议你长期固定的一级词表
如果你想尽量少，我建议最终只保留这 10 个：

contract
policy
authority
enforcement
records
workflow
automation
runtime
migration
evidence
然后只在少数 parent issue 上允许用：

governance
platform

## label(s)

这里有一个补充问题：我是否需要提前在 Git 里面把这些 Labels 提前创建好？你需要回答我？

给对应的 issue 打上 label，首先对应的是具体的 LOG，必须通过对应 LOG 来判定 Label

如： log-S4E-5B-execution-layer-enforcement-and-controlled-exceptions.md
对应的是 S4E-5B: governance/execution layer enforcement and controlled exceptions

一般 label 分为三类：

1.  顶层 label（全大写）：
比如 EVOLUTION （目前只给 EVOLOTION 分配了顶层 label）
- 假设总的 ISSUE/LOG 上面打了 EVOLUTION ，其他所有的 子ISSUE 全部要打上 EVOLUTION；
- 若 S4E 有 EVOLUTION，那么 S4E-5B 也应打上 EVOLUTION；所有整个系列的 LOGS 都应该持有这个顶层 label；
- 可以做到 "full-automation"

2. 模组 label （开头大写）：
具体到对应模块（比如 Search, Chronicle, Library, Tag 等）
- 只要接下来的改动涉及到相应模块，就应该打上；
- 这里有个问题在于：一般总 LOG 可能会漏打这些 Labels；因为在执行子 LOGS 的过程中很多时候才知道需要改动这些模组；
- 可以认为只能做到 "semi-automation"，后期要手工添加一些内容；

3. 底层/功能 label（全小写）
- 层级：按照 ISSUES 层级分为 sub/0 - sub/1 - sub/2 .. etc（不过经过 docs-management-v4 整改以后基本现在 sub/2 - sub/3 替代为了 log 内的 P* - C* - S* 部分，以防 ID 溢出）
  - 比如：
    sub/0 -> S4E: governance/ release-operating model and governance
    sub/1 -> S4E-5B: governance/execution layer enforcement and controlled exceptions
  - 适合 "Full-automation"
- 层级职能：这里和 title 的 SxY 部分可以对上，比如 S4E 的 S4 则对应的是 s4/ops 这个标签；同样的道理可以适用于别的 ISSUEs/LOGs，同样适合 "Full-automation"
- 优先度：p1 - p2，这里完全不用打，需要人来操作，属于 "zero-automation"
- 功能 labels：目前只有 drills，原因在于底层的标签比如 s6/evidence & drills 表示整个 drills 体系的通用结构层，而 drills 这里表示的是跑 N 次具体的 drills（更多是复用概念，然后具体到运用到本次 issue/log 中）这里也可以几乎做到 "3/4-automation" 判定（因为很多子 logs 都会自带获得 summary.json 和 artifacts 的过程，但是可能主 logs 有时候会在正文中没有关键词，所以偶尔需要后期自己打上去）

## body_template

这个地方是 ISSUE 的通用正文，比如：

## Context
- <placeholder>

## Definition of Done (DoD)
- <placeholder>

## Links:
- `log-xxxx.md`<这里应该填写对应 issue 的 log>

此处实际上应该 scaffold 一套初始化的 ISSUE 内容，实际里面的 Context 和 DoDs 部分应该是人最后手工确认并 check，并且有时候会有 run-xxx-xx 这些内容存在里面，我个人现在打算手工加进去（因为 runbook 不一定每次都有，而且命名可能不同）；
所以这里应该算 "half-automation"

## milestone

这里的 milestone 应该对应到 log 部分的 frontmatter （目前我还没有给 log 的 template 增加这一条目，但是如果我的这个提议被落实，我希望在两份 logs 的 templates 中增加进去）

一般来说，milestone 会在生成 log 的时候就创建，所以这里其实算 structured logs 的一些优化（目的是为了考虑到 Git issues 的创建）

所以这里可以完全做到 "full-automation"

