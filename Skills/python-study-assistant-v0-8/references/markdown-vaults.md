# Markdown 复习库导出（v0.8.0）

把 Deck 导出成 Obsidian/Logseq 可用的 Markdown 文件集合。卡片 ID、来源和 tags 必须保留，便于后续更新和回链。

## Profile 格式

```yaml
schema_version: "1.0"
name: obsidian-review
format: markdown
split_by: none
index: true
frontmatter: true
filename: cards.md
```

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `schema_version` | 是 | 当前 `"1.0"` |
| `name` | 是 | profile 名称 |
| `format` | 是 | 固定 `markdown` |
| `split_by` | 否 | `none`、`tag`、`source`；默认 `none` |
| `index` | 否 | 是否生成 `index.md`，默认 `true` |
| `frontmatter` | 否 | 是否生成 YAML frontmatter，默认 `true` |
| `filename` | 否 | `split_by=none` 时的文件名，默认 `cards.md` |

## 文件结构

### split_by: none

```text
review/
├── cards.md
└── index.md
```

### split_by: tag / source

```text
review/
├── tag-pathlib.md
├── tag-stdlib.md
├── index.md
```

文件名中的非法字符替换为 `-`；tag/source 为空时使用 `untagged` / `unknown`。

## cards.md 格式

```markdown
---
deck_id: python-study-demo
schema_version: "0.4.0"
exported_at: 2026-11-17T12:00:00Z
cards: 3
---

<a id="c-000001"></a>

## pathlib：路径操作（标准库）

id:: c-000001
source:: notes/pathlib.md
source_id:: src-000001
tags:: stdlib, path

- **知识点**：...
- **例子**：
```python
...
```
- **自测问题**：...
```

规则：

- 每张卡都有 HTML 锚点 `<a id="<card_id>"></a>`，便于跨文件链接；
- `id::`、`source::`、`source_id::`、`tags::` 使用 Logseq 属性语法，便于 Logseq 识别；
- 标题下不要重复写 `**标题**`；
- 代码块保持围栏；
- 不导出敏感值；不写本机绝对路径。

## index.md

```markdown
# Python Study Review

- [pathlib：路径操作（标准库）](cards.md#c-000001)
- [用 / 拼接路径](cards.md#c-000002)
- [Path.parent](cards.md#c-000003)
```

- 链接使用 `文件名#card_id`；
- 按 Deck 中的卡片顺序；
- 拆分模式下按文件分组，仍按卡片顺序；
- 不把 `card_id` 当作标题。

## 导出规则

- 先应用筛选（tag/type/library/source/keyword/new/include_archived）；
- profile 先于写文件应用；
- 归档卡片默认不导出；profile 要求时才包含；
- 目标目录不存在时创建；目录已有同名文件时先列出将覆盖的文件并等待确认；
- 同一 Deck + profile 重复导出时，卡片 ID、锚点和文件名稳定；
- 写入失败只报告原因，不写 fallback 目录。

## 兼容性

- 文件使用 UTF-8、LF；
- YAML frontmatter 使用简单键值，避免嵌套结构；
- Obsidian 可直接打开 `cards.md`；Logseq 可读取 `id::` 属性；
- 不引入插件专属语法（除 HTML 锚点）。
