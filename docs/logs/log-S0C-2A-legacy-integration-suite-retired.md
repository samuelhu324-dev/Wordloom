# Log-S0C-2A: legacy integration suite retired（测试退役治理）

---

**id**: `S0C-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `testing/legacy integration suite retired`
**status**: `stable`          # draft | stable | archived
**scope**: `S0C`
**tags**: `EVOLOTION, Docs, lab, sub/1`
**links**: ``
  **issue**: `null`
  **pr**: `null`
  **adr**: `docs/adr/adr-S2B-legacy-integration-suite-retired.md`
  **runbook**: `null`
**created**: `2026-02-17`
**updated**: `2026-02-17`

---

## Decision / Outcome（结论区）

- 将 `backend/api/app/tests/test_library/test_integration_round_trip.py` 标记为 **module-level skip**，作为“已退役的 legacy integration suite”，不再作为当前系统的质量门禁。
- 将 `backend/api/app/tests/test_integration_four_modules.py` 标记为 **module-level skip**，作为“已退役的 legacy integration narrative suite”，不再作为当前系统的质量门禁。
- 退役理由明确写入：该套件依赖 `modules.*` 旧导入路径与已不存在的 legacy domain API（如 `Block.create_text` 等），其失败不代表当前系统回归。
- 用“面向当前系统的测试”作为替代保护网：应用层 use case 测试（ports + repo + 异常映射）、关键仓储/基础设施合约测试、必要的 domain 不变量测试。

**验证结果（当次证据）**：

- `api/app/tests/test_library` 在退役后达到 `131 passed, 1 skipped`。
- 本批次对齐“保护现在”的测试后，全量 `pytest -q` 达到 `470 passed, 132 skipped`（另有 `12 warnings`）。

## Background

在演进过程中，测试的首要目的不是“保持旧世界可运行”，而是**保护当前系统的行为与契约**。当某些历史测试套件：

- 绑定到已弃用的模块布局（例如 `modules.*`），
- 假设了已被移除/替换的 domain API 与事件模型，

那么它们的失败会持续制造“假阴性”（false negatives），阻塞当前交付与演进，且会诱导团队为了修测试去引入不必要的兼容层。

## Problem / Malfunction

- **症状**：全量/子集 pytest 运行被 `test_integration_round_trip.py` 大量失败阻塞。
- **根因**：该文件不是对当前系统的黑盒/契约测试，而是对早期架构/旧 API 的硬编码“集成叙事脚本”。当前代码与其假设已不可对齐。
- **风险**：若强行对齐（加 shim 或重构 domain 以迎合测试），会引入额外 surface area 与长期维护负担，且可能扭曲当前架构边界。

补充：同类问题也出现在 `test_integration_four_modules.py`（Phase 1.5 的叙事式集成套件），其失败同样不代表当前系统回归。

## What/How to do（落地规则）

### 1) 退役规则：skip 而不是“硬修到绿”

- 对于明确指向 **deprecated module layout / obsolete API** 的 legacy suite：
  - 使用 `pytest.skip(..., allow_module_level=True)` 退役；
  - skip message 必须包含：退役原因、指向 ADR/Log 的链接。

### 2) 替代保护网：写“保护现在”的测试

- **Application layer（优先）**：use case + ports + repository 的契约测试（尤其是异常语义与 DTO 映射）。
- **Infrastructure/Repository（必要）**：关键行为合约（例如 soft-delete 行为、时间戳、过滤规则）。
- **Domain（最小必要）**：不变量与事件发射在仍被系统依赖时才测试；避免为了叙事完整而测试不存在的 API。

本批次落地示例（对齐当前系统语义）：

- `api/app/tests/test_book/test_application_layer.py`：重写为对齐当前 Book UseCase API + Basement（`soft_deleted_at`）语义的最小单测集。
- `api/app/tests/test_block/test_repository.py`：将旧字段/构造参数从 `index/is_deleted/block_id/block_type` 对齐到当前领域模型的 `order/soft_deleted_at/id/type`，并补齐 HEADING 的 `heading_level` 约束。

### 3) 证据链要求（DoD）

- suite 退役不应导致“无人负责的空白”：
  - 必须能指出当前系统对应的测试覆盖位置（文件/目录级即可）；
  - 需要一次可复现的通过结果（pytest 输出）作为证据。

## Next

- 将“legacy suite 退役治理”沉淀为一个小型规范（何时 skip、skip message 模板、替代测试清单）。
- 继续推进全量 `pytest -q` 从“可运行”到“可维护地全绿”（逐个收敛剩余失败点，避免再被历史测试拖垮）。

## References

- `docs/adr/adr-S2B-legacy-integration-suite-retired.md`
- `backend/api/app/tests/test_library/test_integration_round_trip.py`（已 module-level skip）
- `backend/api/app/tests/test_integration_four_modules.py`（已 module-level skip）
- `docs/logs/log-S2B-1A-failure-contract-v1.md`（结构模板与“稳定契约优先”思路）
