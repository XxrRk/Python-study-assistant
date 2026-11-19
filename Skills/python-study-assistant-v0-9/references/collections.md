# Deck 集合与跨库检索（v0.9.0）

集合把多个 Deck 组织成一个只读清单，便于跨库搜索和按 Deck 导出。集合不复制卡片、不改变 Deck，也不替代跨 Deck 合并。

## 集合文件

```json
{
  "schema_version": "1.0",
  "collection_id": "python-study",
  "name": "Python 学习集合",
  "decks": [
    {
      "deck_id": "python-study-demo-v04",
      "path": "decks/pathlib.json",
      "role": "core"
    },
    {
      "deck_id": "python-study-other",
      "path": "decks/other.json",
      "role": "reference"
    }
  ]
}
```

字段：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `schema_version` | 是 | 固定 `"1.0"` |
| `collection_id` | 是 | 集合 ID，小写字母/数字/连字符 |
| `name` | 否 | 展示名称 |
| `decks` | 是 | 至少 1 项 |
| `deck_id` | 是 | 必须与 Deck 内 `deck_id` 一致 |
| `path` | 是 | 相对集合文件的 Deck 路径；禁止绝对路径 |
| `role` | 否 | `core` / `reference` / `archive` |

## 构建与校验

1. 读取集合文件；不存在时根据用户给出的 Deck 路径创建。
2. 校验 JSON、`schema_version`、`collection_id`、`decks`。
3. 解析每个 `path`：必须是相对路径，不能越出用户指定目录。
4. 读取 Deck，校验 `schema_version`（0.3.0/0.4.0）和 `deck_id` 与清单一致。
5. 检查 `deck_id` 重复、路径重复。
6. 只有用户要求时才写集合文件；已有同名文件时先给覆盖计划并等待确认。

## 跨库搜索

支持与单 Deck 相同的筛选：

- `keyword`：标题/知识点/例子/问题；
- `tag`、`type`、`library`、`source`、`archived`；
- `deck_id`：限定某个 Deck。

结果格式：

```text
deck_id: python-study-demo-v04 (core)
path: decks/pathlib.json
card_id: c-000002
title: 用 / 运算符拼接 Path 路径
source_ref: notes/pathlib.md
tags: path
```

规则：

- 结果必须带 `deck_id` 和 Deck 路径；
- 同名 `card_id` 在不同 Deck 中不视为同一张卡，不能用单键合并；
- 跨库重复知识点只报告，不自动去重；
- 结果按 Deck 清单顺序，再按 Deck 内卡片顺序。

## 按 Deck 导出

- JSONL/CSV/Anki：按 Deck 分别生成文件，文件名带 `deck_id`，不把多个 Deck 的 card_id 混在一起；
- Markdown 复习库：顶层 `index.md` 链接到每个 Deck 的 `cards-<deck_id>.md`；每个文件使用 v0.8 的 Markdown vault 规则；
- 每个 Deck 的导出仍使用原来的 card_id/source_id；
- 集合级 index 包含 Deck 名称、路径、卡片数；
- 目标目录已有文件时先列覆盖计划并等待确认。

## 集合级 Markdown 结构

```text
review/
├── index.md
├── cards-python-study-demo-v04.md
└── cards-python-study-other.md
```

`index.md`：

```markdown
# Python 学习集合

- [python-study-demo-v04](cards-python-study-demo-v04.md) — 3 张
- [python-study-other](cards-python-study-other.md) — 2 张
```

## 错误处理

- Deck 缺失/损坏：停止，报告路径；
- `deck_id` 不一致：停止，不自动改 Deck；
- 绝对路径或越界路径：拒绝；
- 集合写入失败：报告原因，不写 fallback 文件；
- 搜索无结果：明确说明，不生成空导出文件。
