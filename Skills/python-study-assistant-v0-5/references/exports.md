# 复习导出映射（v0.5.0）

导出只从已有 Deck 读取；同一 Deck 多次导出必须保持 `card_id`、`source_id` 不变。默认只在用户要求时写文件。v0.5 沿用 v0.4 的筛选导出，字段映射保持 v0.3 兼容。

## 导出前筛选

可用条件（取交集，不区分大小写）：

- `tag=<标签>`
- `type=library|knowledge`
- `library=<包名>`
- `source=<source_id 或 ref 子串>`
- `keyword=<文本>`
- `new`（最近一次 diff 新增的卡片）
- `include_archived`（默认排除 `archived: true`）

导出前报告筛选条件和实际选中数量；0 张时不创建空文件。

## JSONL（.jsonl）

一行一个 JSON 对象，UTF-8，不使用 Markdown 围栏。每行字段：

```json
{"schema_version":"0.4.0","deck_id":"python-study-demo","card_id":"c-000001","type":"library","title":"pathlib：面向对象的路径操作（标准库）","knowledge":"pathlib 是 Python 标准库，用 Path 对象表示路径。","example":"from pathlib import Path\n\nprint(Path('data') / 'file.txt')","question":"pathlib 属于标准库还是第三方库？","library":{"name":"pathlib","package":"pathlib","kind":"stdlib"},"source_id":"src-000001","source_ref":"notes/pathlib.md","tags":["stdlib","path"],"created_at":"2026-11-16T09:00:00Z"}
```

规则：

- 保留 Deck 中的卡片顺序；
- 知识点卡片不带 `library`；
- 可选 `tags` 原样输出；
- 每行必须合法 JSON；不输出 Deck 顶层对象或解释行。

## CSV（.csv）

固定表头（顺序不可变）：

```text
schema_version,deck_id,card_id,type,title,knowledge,example,question,library_name,library_package,library_kind,source_id,source_ref,tags,created_at
```

规则：

- 每张卡一行；知识点卡片的 `library_name`、`library_package`、`library_kind` 留空。
- 字段含逗号、双引号或换行时按 RFC 4180 转义。
- `tags` 用 `|` 连接；没有 tags 时留空。
- UTF-8；不要使用 Excel 专有分号格式。

## Anki 兼容 TSV（.tsv）

无表头，3 列，制表符分隔：

1. **Front**：卡片标题 + `<br><br>` + 知识点
2. **Back**：例子 + `<br><br>自测问题：` + 自测问题 + `<br><br>来源：` + `source_ref` + `<br>卡片ID：` + `card_id`
3. **Tags**：空格分隔，至少包含：
   - `python-study-assistant`
   - 卡片原有 tags
   - `pycard::<card_id>`
   - `source::<source_id>`

规则：

- 字段内换行写 `<br>`，制表符替换为空格。
- `card_id`、`source_id`、`source_ref` 必须出现在导出内容中；重复导出不变。
- 原 tag 含空格时改为连字符。

## 文件命名

用户未指定路径时：

- JSONL：`cards.jsonl`
- CSV：`cards.csv`
- Anki TSV：`cards.tsv`

导出后报告路径、筛选条件和卡片数量；写入失败时说明原因，不要假装已保存，也不要自行改写路径或创建 fallback 文件。

## 兼容性

- 字段映射与 v0.3 保持一致，v0.4 Deck 导出不改变列顺序。
- `schema_version` 使用 Deck 的实际版本；迁移后的 Deck 导出为 `0.4.0`，未迁移的 v0.3 Deck 仍导出 `0.3.0`。
- `fingerprint`、`archived`、`origin_deck_id` 不进入导出列；归档卡片默认不导出。
