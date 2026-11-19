# 质量用例与回归

本目录把 v0.5 起的质量基线变成可机读的用例清单：

- `cases.schema.json`：用例结构 Schema；
- `cases.json`：对 v0.2/v0.3/v0.4/v0.6/v0.7/v0.8/v0.9 fixture 的期望不变量。

## 用例字段

| 字段 | 含义 |
| --- | --- |
| `id` | 唯一用例 ID，小写连字符 |
| `fixture` | 主测试材料，相对仓库根目录 |
| `secondary_fixture` | 合并/跨 Deck 用例的第二个输入 |
| `operation` | `convert`、`merge`、`cross_merge`、`migrate`、`filter_export`、`security` |
| `min_cards` / `max_cards` | 允许的卡片数量范围 |
| `required_libraries` | 必须出现的库发行版名 |
| `forbidden_text` | 输出/Deck/导出中不得出现的文本 |
| `required_card_fields` | 卡片必须带的字段 |
| `required_source_ref` | 是否要求来源引用 |

CI 只校验用例结构、fixture 路径、ID 唯一性和范围合法性；不调用真实 LLM。实际卡片质量由人工或独立 Agent 前向测试按 `references/quality-eval.md` 评分。

## 前向测试

1. 读取 v0.5 Skill 和对应 fixture；
2. 按 `operation` 执行；
3. 核对卡片数量范围、必需库、禁止文本、必需字段；
4. 记录通过/失败；失败项必须修复后重跑；
5. 不把测试输出或临时 Deck 写入仓库。
