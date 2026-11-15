# Deck 格式与增量合并（v0.3.0）

Deck 是本 Skill 的卡片库容器。它把一次或多次转换得到的卡片、来源信息和稳定 ID 保存在一份 JSON 中，供重复转换、去重和导出使用。

## 顶层结构

```json
{
  "schema_version": "0.3.0",
  "deck_id": "python-study-demo",
  "updated_at": "2026-11-15T10:00:00Z",
  "sources": [
    {
      "source_id": "src-000001",
      "kind": "markdown",
      "ref": "notes/pathlib.md",
      "added_at": "2026-11-15T09:50:00Z"
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
      "tags": ["stdlib", "path"],
      "created_at": "2026-11-15T09:50:00Z"
    }
  ]
}
```

## 字段规则

| 字段 | 规则 |
| --- | --- |
| `schema_version` | 固定为 `"0.3.0"`；升级格式时才修改 |
| `deck_id` | 3–64 个字符，使用小写字母、数字和连字符（如 `python-study-demo`） |
| `sources` | 至少 1 项；每个来源只追加，不删除 |
| `cards` | 至少 1 项；卡片顺序在合并时保留，新卡追加到末尾 |
| `source_id` | `src-000001` 形式的递增值，Deck 内唯一，永不复用 |
| `card_id` | `c-000001` 形式的递增值，Deck 内唯一，永不复用、永不重编号 |
| `created_at` / `added_at` / `updated_at` | ISO 8601 UTC 时间，如 `2026-11-15T09:50:00Z` |

### source 对象

- `source_id`：`src-000001` 递增。
- `kind`：`paste`、`markdown`、`txt`、`py`、`ipynb`、`html`、`directory` 之一。
- `ref`：相对文件名或“对话中粘贴的文本”；不要写本机绝对路径。
- `added_at`：首次加入 Deck 的时间。

### card 对象

- 必须包含 `card_id`、`type`、`title`、`knowledge`、`example`、`question`、`source_id`、`source_ref`、`created_at`。
- `type` 为 `library` 或 `knowledge`。
- `type=library` 时必须带 `library`：`name`（导入名）、`package`（安装名；标准库时与导入名相同）、`kind`（`stdlib` 或 `third-party`）。
- `type=knowledge` 时不得带 `library`。
- `source_ref`：粘贴文本写“对话中粘贴的文本”；文件写相对路径（`.ipynb` 可带 `:cell-N`）。
- `tags`：可选字符串数组，去重；建议包含主题、库名或 `stdlib`/`third-party`。
- `created_at`：首次创建该卡的时间；合并更新时不改。

## ID 分配

- 新 Deck 从 `src-000001`、`c-000001` 开始。
- 合并时取现有编号的最大值 +1；删除卡片留下的空号不复用。
- 已有 `card_id` / `source_id` 永远保持不变，即使标题、例子或标签更新。
- 导出只读取 Deck，不重新编号。

## 增量合并规则

1. **读取并校验**现有 Deck：`schema_version` 必须为 `0.3.0`，`deck_id`、`sources`、`cards` 完整；字段缺失或 JSON 无效时停止，说明原因，不覆盖原文件。
2. **登记来源**：新来源按 `kind + ref` 去重；已有来源复用 `source_id`，新来源分配下一个 `src-` 编号并追加。
3. **匹配卡片**：
   - 库卡片：`library.package` 不区分大小写相等；缺失 package 时比较 `library.name`。
   - 知识点卡片：标题规范化后相等（去掉首尾空白、标点，统一小写，压缩连续空白）。
   - 表述不同但明显是同一知识点的卡片，可合并；拿不准时保留两张并说明，不要为了去重误删不同知识。
4. **处理命中**：
   - 内容与已有卡片一致 → 计入“跳过”，不新增卡片。
   - 新解释/例子/标签更清晰完整 → 保留原 `card_id` 和 `created_at`，更新知识点、例子、标签、来源，计入“合并”。
   - 已有卡片更好 → 也不新增，计入“跳过”。
5. **处理未命中**：分配下一个 `c-` 编号，写入 `created_at`、`source_id`、`source_ref`，追加到 `cards` 末尾，计入“新增”。
6. **更新元数据**：更新 `updated_at`；不要删除旧来源或旧卡片，除非用户明确要求。
7. **写回**：只有结构自检通过后才写回 Deck；默认路径 `deck.json`，用户指定路径时使用指定路径。
8. **输出摘要**：

   ```text
   Deck updated: deck.json
   新增 2 张 / 合并 1 张 / 跳过 3 张
   ```

## 常见操作

- “把 notes.md 生成 Deck” → 新建 Deck，分配 ID，写 `deck.json`。
- “把 notes.md 合并到 deck.json” → 读取、匹配、更新，写回并给摘要。
- “同一材料再合并一次” → 应全部跳过或合并，不新增重复卡。
- “导出 JSONL / CSV / Anki TSV” → 从 Deck 读取，字段映射见 [exports.md](exports.md)。

## 自检

- `schema_version` 为 `0.3.0`，`deck_id` 符合格式；
- `sources` 非空，`source_id` 唯一；
- `cards` 非空，`card_id` 唯一且没有重编号；
- 每张卡都有来源字段和 `created_at`；
- 库卡片有 `library`，知识点卡片没有；
- 合并摘要中的新增/合并/跳过数量与 Deck 变化一致；
- Deck 中不含密码、Token、API Key、私钥或本机绝对路径。
