# 复习导出映射（v0.3.0）

导出只从已有 Deck 读取；同一 Deck 多次导出必须保持 `card_id`、`source_id` 不变。默认只在用户要求时写文件。

## JSONL（.jsonl）

一行一个 JSON 对象，UTF-8 编码，不使用 Markdown 围栏。每行字段：

```json
{"schema_version":"0.3.0","deck_id":"python-study-demo","card_id":"c-000001","type":"library","title":"pathlib：面向对象的路径操作（标准库）","knowledge":"pathlib 是 Python 标准库，用 Path 对象表示路径。","example":"from pathlib import Path\n\nprint(Path('data') / 'file.txt')","question":"pathlib 属于标准库还是第三方库？","library":{"name":"pathlib","package":"pathlib","kind":"stdlib"},"source_id":"src-000001","source_ref":"notes/pathlib.md","tags":["stdlib","path"],"created_at":"2026-11-15T09:50:00Z"}
```

规则：

- 保留 Deck 中的卡片顺序；
- 知识点卡片不带 `library`；
- 可选 `tags` 原样输出；
- 不要输出 Deck 顶层对象或额外解释行；每行都必须是合法 JSON。

## CSV（.csv）

固定表头（顺序不可变）：

```text
schema_version,deck_id,card_id,type,title,knowledge,example,question,library_name,library_package,library_kind,source_id,source_ref,tags,created_at
```

规则：

- 每张卡一行；知识点卡片的 `library_name`、`library_package`、`library_kind` 留空。
- 字段含逗号、双引号或换行时按 RFC 4180 用双引号包裹，内部双引号写成两个双引号。
- `tags` 用 `|` 连接（如 `stdlib|path`）；没有 tags 时留空。
- 使用 UTF-8 编码；不要使用 Excel 专有的分号格式。

## Anki 兼容 TSV（.tsv）

无表头，3 列，以制表符分隔：

1. **Front**：卡片标题 + `<br><br>` + 知识点
2. **Back**：例子 + `<br><br>自测问题：` + 自测问题 + `<br><br>来源：` + `source_ref` + `<br>卡片ID：` + `card_id`
3. **Tags**：空格分隔的标签集合，至少包含：
   - `python-study-assistant`
   - 卡片原有 tags
   - `pycard::<card_id>`
   - `source::<source_id>`

规则：

- 字段内部的换行统一写成 `<br>`，制表符替换为空格，确保一行一条记录。
- `card_id`、`source_id`、`source_ref` 必须出现在导出内容中；同一 Deck 重复导出不变。
- 标签中不能含空格；原 tag 含空格时改为连字符。
- 示例：

```text
pathlib：面向对象的路径操作（标准库）<br><br>pathlib 是 Python 标准库，用 Path 对象表示路径。<br><br>示例代码见卡片。	from pathlib import Path<br><br>print(Path('data') / 'file.txt')<br><br>自测问题：pathlib 属于标准库还是第三方库？<br><br>来源：notes/pathlib.md<br>卡片ID：c-000001	python-study-assistant stdlib path pycard::c-000001 source::src-000001
```

（示例第二列为了可读性省略了示例代码的完整复制；实际导出必须完整写入。）

## Markdown / 单次 JSON

- Markdown 默认四字段卡片格式不变。
- 单次 JSON 指用户只要一次性 `source` + `cards` 的结构，不建立 Deck：沿用 v0.2 字段（`type`、`title`、`knowledge`、`example`、`question`、可选 `library`/`source_ref`）。
- 复习导出只在 Deck 模式下提供；没有 Deck 时先创建 Deck，或请用户指定 Deck 路径。

## 文件命名

用户未指定路径时：

- JSONL：`cards.jsonl`
- CSV：`cards.csv`
- Anki TSV：`cards.tsv`

导出后报告路径和卡片数量；写入失败时说明原因，不要假装已保存，也不要自行改写到其他目录或创建 fallback 文件。
