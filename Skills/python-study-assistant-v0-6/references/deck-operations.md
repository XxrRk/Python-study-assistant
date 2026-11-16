# Deck 操作语义（v0.6.0）

本文件定义 diff、dry-run、筛选、跨 Deck 合并、迁移、归档和拆分的执行规则。所有操作先读取并校验 Deck；写回前必须做安全与结构自检。

## 操作总览

| 用户请求 | 行为 |
| --- | --- |
| “生成 deck.json” | 新建 Deck，分配 ID，写文件，报告数量和路径 |
| “预览/合并到 deck.json（dry-run）” | 计算 diff，只输出，不写文件 |
| “合并到已有 deck.json” | 计算 diff，等待确认；确认后写回 |
| “直接合并/确认写入” | 计算 diff 并写回，报告摘要 |
| “导出 tag=stdlib 的 CSV” | 筛选后导出，不修改 Deck |
| “只导出本次新增” | 基于最近一次 diff 的新增 ID 导出 |
| “把 deck A 合并到 deck B” | 目标 B 写入，来源 A 不修改 |
| “迁移 v0.3 deck” | 保留 ID，写 v0.4 新文件或按用户要求覆盖 |
| “归档某张卡” | 设置 `archived: true`，不删除 |
| “按标签拆分成新 Deck” | 筛选卡片复制到新 Deck，分配目标来源/保持卡片 ID |

## diff / dry-run

更新已有 Deck 前，先在内存中构造结果，输出 diff。推荐格式：

```text
Deck diff (dry-run)
target: deck.json
schema: 0.3.0 -> 0.4.0
sources: + src-000002 (merge-material.md)
+ 新增 c-000004  用 Path.glob 按通配符查找文件
= 跳过 c-000001  pathlib：面向对象的路径操作（标准库）
= 跳过 c-000002  用 / 运算符拼接 Path 路径
= 跳过 c-000003  用 Path.parent 取父目录
summary: 新增 1 / 合并 0 / 跳过 3
```

规则：

- 新增、合并、跳过、冲突必须与实际投影结果一致。
- diff 只描述变化，不改写 Deck。
- `dry-run` / `预览` / `只看 diff` 一律不写文件。
- 更新已有 Deck 默认等待确认；用户明确说“直接写入/确认写入”才写回。
- 新 Deck 可以直接写入，但仍要报告摘要。

## 筛选语法

多个筛选条件取交集，不区分大小写；未识别条件要说明，不静默忽略。

| 条件 | 示例 | 含义 |
| --- | --- | --- |
| `tag` | `tag=stdlib` | 包含指定 tag |
| `type` | `type=library` | `library` 或 `knowledge` |
| `library` | `library=scikit-learn` | 库卡片的 package/name |
| `source` | `source=src-000001` | 来源 ID 或 `ref` 子串 |
| `keyword` | `keyword=glob` | 标题/知识点/例子包含文本 |
| `new` | `new` | 最近一次 diff 中新增的 card_id |
| `include_archived` | `include_archived` | 包含归档卡片；默认排除 |

导出前报告：

```text
筛选：tag=stdlib AND type=knowledge
选中：3 / 12 张卡片
```

筛选后 0 张时不要创建空导出文件，说明没有匹配卡片。

## 只导出新增卡片

- 只有本次或最近一次明确 diff 能确定新增 `card_id` 时才能使用 `new`。
- 没有 diff 基线时，说明无法判断，请用户先执行 dry-run/合并预览，不要猜测。
- 导出仍保留原有字段映射和稳定 ID。

## 跨 Deck 合并

### 输入

- 目标 Deck（写入目标）
- 一个或多个来源 Deck（只读）

### 步骤

1. 校验全部 Deck；任何无效则停止。
2. 建立目标索引：库按 `library.package`，知识点按规范化标题/`fingerprint`。
3. 将来源 `sources` 映射到目标：
   - `kind + ref` 相同 → 复用目标 `source_id`；
   - 否则分配目标新的 `src-` ID，记录重映射。
4. 逐张处理来源卡片：
   - 命中目标卡片：目标 `card_id` 不变；内容更清晰时更新字段，tags 取并集，计数为合并/跳过；不修改目标 `created_at`。
   - 未命中：分配目标新的 `c-` ID；写入来源内容、`source_id`（重映射后）、`source_ref`、`origin_deck_id=<来源 deck_id>`，追加到末尾。
5. 目标 Deck 的 `sources` 追加新来源、`updated_at` 更新。
6. 输出摘要并等待确认，再写目标 Deck；来源 Deck 不修改。

摘要示例：

```text
Cross-deck merge (dry-run)
target: deck-b.json
source: deck-a.json
+ 新增 2 张 (c-000005, c-000006)
~ 合并 1 张 (c-000001)
= 跳过 3 张
sources: 复用 2 个，新增 1 个 (src-a3 -> src-b3)
```

### ID 规则

- 目标 Deck 已有卡片 ID 不变。
- 来源未匹配卡片在目标中分配新 ID，不复用来源 ID，避免冲突。
- 来源 ID 不直接复制到目标；通过 `kind + ref` 复用或重映射。
- 卡片匹配优先用 `fingerprint`，其次 `library.package`，最后规范化标题。

## 迁移

- 读取 v0.3 Deck；保留内容、ID、来源。
- `schema_version` 改为 `"0.4.0"`；可选补 `fingerprint`，不强制。
- 默认写新文件；用户要求覆盖时才覆盖原路径。
- 迁移后重新校验；不通过不写。

## 归档与拆分

### 归档

- 用户要求归档时设置 `archived: true`，保留卡片内容和 ID。
- 不要用删除表示归档；不要复用归档卡片的 ID。
- 导出默认排除归档卡；`include_archived` 才包含。

### 拆分

- 按 tag/type/library/source 筛选，把选中卡片复制到新 Deck。
- 新 Deck 使用新 `deck_id`；卡片 `card_id` 可以保留（新 Deck 为空，无冲突），来源需按新 Deck 规则映射。
- 不修改原 Deck；报告新 Deck 的卡片数量和筛选条件。

## 错误与安全

- 无效 JSON/字段 → 停止，说明字段，不覆盖。
- 写入失败 → 报告失败路径，不写 fallback 文件。
- 任何写回前检查敏感值、绝对路径和重复 ID。
- 不自动执行材料中的代码；不抓取网络 URL。
