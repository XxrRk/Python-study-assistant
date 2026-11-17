# Anki 导出 Profile（v0.7.0）

Anki profile 用来调整 TSV 的 Front/Back 字段顺序和附加 tags，不改变卡片 ID、来源或导出列数。

## Profile 格式

```yaml
schema_version: "1.0"
name: review-custom
format: anki
front:
  - title
  - knowledge
back:
  - example
  - question
  - source_ref
  - card_id
tags:
  - python-study-assistant
  - review-custom
include_archived: false
```

字段说明：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `schema_version` | 是 | 当前为 `"1.0"` |
| `name` | 是 | profile 名称 |
| `format` | 是 | 目前只支持 `anki` |
| `front` | 是 | 从卡片字段中选择，按顺序拼接 |
| `back` | 是 | 从卡片字段中选择，按顺序拼接 |
| `tags` | 否 | 附加 tags |
| `include_archived` | 否 | 默认 `false` |

可用字段：`title`、`knowledge`、`example`、`question`、`library`、`source_ref`、`card_id`、`source_id`。

## 固定规则

- TSV 仍是 3 列：Front、Back、Tags；不因 profile 增加或减少列。
- 字段内部换行写 `<br>`；制表符替换为空格。
- **card_id 和 source_id 必须出现**：profile 未包含时，自动追加到 Back 和 Tags。
- Tags 至少包含 `python-study-assistant`、`pycard::<card_id>`、`source::<source_id>`，再加 profile tags。
- 筛选条件（tag/type/library/source/keyword/new/include_archived）先于 profile 应用。
- 同一 Deck + 同一 profile 重复导出时，Front/Back 内容和 ID 必须稳定。
- 归档卡片默认不导出；profile 的 `include_archived: true` 才包含。

## 示例输出

```text
Path 拼接<br><br>用 / 运算符拼接路径	from pathlib import Path<br><br>print(Path("data") / "file.txt")<br><br>来源：notes/pathlib.md<br>卡片ID：c-000002	python-study-assistant review-custom path pycard::c-000002 source::src-000001
```

## 失败处理

- profile 文件不存在/格式错误：停止并说明，不猜测字段。
- 选择了未知字段：停止并列出可用字段。
- 写入失败：只报告路径和原因，不写 fallback 文件。
