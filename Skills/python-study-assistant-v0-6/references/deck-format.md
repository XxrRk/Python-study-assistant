# Deck 格式与迁移（v0.6.0，沿用 Schema 0.4.0）

Deck 是卡片库容器。v0.6 沿用 v0.4 的格式：可选的 `fingerprint`、`archived`、`origin_deck_id`，并支持安全迁移。

## 顶层结构

```json
{
  "schema_version": "0.4.0",
  "deck_id": "python-study-demo",
  "description": "pathlib 学习卡片",
  "created_at": "2026-11-16T09:00:00Z",
  "updated_at": "2026-11-16T10:00:00Z",
  "sources": [
    {
      "source_id": "src-000001",
      "kind": "markdown",
      "ref": "notes/pathlib.md",
      "added_at": "2026-11-16T09:00:00Z"
    }
  ],
  "cards": [
    {
      "card_id": "c-000001",
      "type": "library",
      "title": "pathlib：面向对象的路径操作（标准库）",
      "knowledge": "pathlib 是 Python 标准库，用 Path 对象表示路径。",
      "example": "from pathlib import Path\n\nprint(Path('data') / 'file.txt')",
      "question": "pathlib 属于标准库还是第三方库？",
      "library": {
        "name": "pathlib",
        "package": "pathlib",
        "kind": "stdlib"
      },
      "source_id": "src-000001",
      "source_ref": "notes/pathlib.md",
      "fingerprint": "lib:pathlib",
      "archived": false,
      "tags": ["stdlib", "path"],
      "created_at": "2026-11-16T09:00:00Z"
    }
  ]
}
```

## 字段规则

| 字段 | 规则 |
| --- | --- |
| `schema_version` | v0.4 Deck 固定为 `"0.4.0"`；v0.3 为 `"0.3.0"` |
| `deck_id` | 3–64 个字符，小写字母、数字、连字符 |
| `description` | 可选，简短说明 Deck 主题 |
| `sources` | 至少 1 项；只追加，不删除 |
| `cards` | 至少 1 项；合并时保留既有顺序，新卡追加到末尾 |
| `source_id` | `src-000001` 递增，Deck 内唯一，永不复用 |
| `card_id` | `c-000001` 递增，Deck 内唯一，永不复用、永不重编号 |
| `fingerprint` | 可选；跨 Deck 匹配用；库为 `lib:<规范化包名>`，知识点为 `k:<规范化标题>` |
| `archived` | 可选，默认 `false`；归档不删除，导出默认排除 |
| `origin_deck_id` | 可选；跨 Deck 合并时记录来源 Deck |
| `created_at` / `added_at` / `updated_at` | ISO 8601 UTC 时间 |

### source 对象

- `source_id`：`src-000001` 递增。
- `kind`：`paste`、`markdown`、`txt`、`py`、`ipynb`、`html`、`directory`。
- `ref`：相对文件名或“对话中粘贴的文本”；不要写本机绝对路径。
- `added_at`：首次加入 Deck 的时间。

### card 对象

- 必须包含 `card_id`、`type`、`title`、`knowledge`、`example`、`question`、`source_id`、`source_ref`、`created_at`。
- `type=library` 时必须带 `library`：`name`（导入名）、`package`（安装名；标准库时与导入名相同）、`kind`（`stdlib` / `third-party`）。
- `type=knowledge` 时不得带 `library`。
- `source_ref`：粘贴文本写“对话中粘贴的文本”；文件写相对路径；`.ipynb` 可带 `:cell-N`。
- `tags`：可选字符串数组，去重。
- `fingerprint`：可选；用于跨 Deck 去重，不替代 `card_id`。
- `archived`：可选布尔值；归档卡片保留 ID 和内容。

## ID 与指纹

- 新 Deck 从 `src-000001`、`c-000001` 开始。
- 合并/迁移取现有编号最大值 +1；删除/归档留下的空号不复用。
- 已有 `card_id` / `source_id` 永远保持不变，即使标题、例子或标签更新。
- `fingerprint` 生成建议：
  - 库：`lib:<package 小写>`，非字母数字替换为 `-`，如 `lib:scikit-learn`；
  - 知识点：`k:<标题小写、去标点、空白替换为 `-`>`，如 `k:用-path-运算符拼接路径`。
- `fingerprint` 缺失时，用 `library.package` 或规范化标题匹配。

## Schema 版本与迁移

### v0.3.0 → v0.4.0

1. 读取并校验 v0.3 Deck（`schema_version`、`deck_id`、`sources`、`cards`）。
2. 保留 `deck_id`、所有来源、所有卡片 ID、内容、tags 和创建时间。
3. 将 `schema_version` 改为 `"0.4.0"`；按需补充可选 `fingerprint`，不强制。
4. 不重编号、不删除、不改写已有标题/例子。
5. 用户未要求覆盖时，写入新文件（如 `deck.v0.4.json`），原文件不动。
6. 迁移结果必须通过 v0.4 Deck Schema；失败时停止，不写部分结果。

### 兼容性

- v0.4 可以读取 v0.3 Deck；读取后按迁移规则处理。
- 不要求 v0.3 客户端读取 v0.4 Deck；发布新格式时应提示版本。
- 导出的 `schema_version` 来自实际 Deck；迁移前导出仍为 `0.3.0`。

## 写回前自检

- `schema_version` 正确，`deck_id` 格式合法；
- `sources` 非空，`source_id` 唯一；
- `cards` 非空，`card_id` 唯一且未重编号；
- 每张卡有来源字段和 `created_at`；
- 库卡片有 `library`，知识点卡片没有；
- 可选字段类型正确（`archived` 布尔、`fingerprint` 字符串、`origin_deck_id` 字符串）；
- 没有敏感值、本机绝对路径或凭据。
