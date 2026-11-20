# TALOS-Lite 全量 9 份脱敏教学样板速查手册

本目录集中展示贯穿 Week 1–6 的全部教学样板文件。所有文件均虚构自 `demo-habit-tracker` 示例项目，单文件严格控制在 **60 行以内**，且受自动化门禁脚本保护，确保零隐私路径与零内部数据泄露。

---

## 按周次索引全量样板

| 周次 | 样板文件名 | 一句话说明它演示什么 | 对应精讲章节 |
| :--- | :--- | :--- | :--- |
| **Week 1** | `state-sample.json` | 精简的项目当前状态档案卡 | [第 1 周精讲](/guide/week-01-data-rules) |
| **Week 1** | `state-schema-sample.json` | 管住上面档案卡怎么填的“填写规范表” | [第 1 周精讲](/guide/week-01-data-rules) |
| **Week 2** | `workspace-binding-sample.json` | 主工作区与草稿分支隔离绑定规则 | [第 2 周精讲](/guide/week-02-git-truth) |
| **Week 2** | `truth-vs-index-sample.json` | 权威事实源 vs 可随时重建派生索引的分级清单 | [第 2 周精讲](/guide/week-02-git-truth) |
| **Week 3** | `port-protocol-sample.py` | Python 插座接口（Protocol）与测试假插头示例 | [第 3 周精讲](/guide/week-03-oop-layers) |
| **Week 4** | `proposal-sample.json` | AI 只能投递的待审提议单（含双版本号与防篡改指纹） | [第 4 周精讲](/guide/week-04-concurrency-guard) |
| **Week 4** | `event-chain-sample.jsonl` | 连续递增且带加密收据的事件流水单 | [第 4 周精讲](/guide/week-04-concurrency-guard) |
| **Week 5** | `ratchet-baseline-sample.json` | 只许减少坏依赖、新增立即报错的架构棘轮基线 | [第 5 周精讲](/guide/week-05-tdd-migration) |
| **Week 6** | `manifest-sample.json` | 插件上架前必交的权限、外呼确认与安全降级身份证 | [第 6 周精讲](/guide/week-06-packaging-boundary) |

---

## 全量样板速览

### 1. 状态档案卡（`state-sample.json`）
<<< ./examples/state-sample.json

### 2. 状态填写规范表（`state-schema-sample.json`）
<<< ./examples/state-schema-sample.json

### 3. 工作区隔离绑定（`workspace-binding-sample.json`）
<<< ./examples/workspace-binding-sample.json

### 4. 真账本 vs 派生索引分级表（`truth-vs-index-sample.json`）
<<< ./examples/truth-vs-index-sample.json

### 5. 插座标准与可替换插头（`port-protocol-sample.py`）
<<< ./examples/port-protocol-sample.py

### 6. AI 待审提议单（`proposal-sample.json`）
<<< ./examples/proposal-sample.json

### 7. 连续加密收据流水（`event-chain-sample.jsonl`）
<<< ./examples/event-chain-sample.jsonl

### 8. 架构棘轮基线（`ratchet-baseline-sample.json`）
<<< ./examples/ratchet-baseline-sample.json

### 9. 能力身份证（`manifest-sample.json`）
<<< ./examples/manifest-sample.json
