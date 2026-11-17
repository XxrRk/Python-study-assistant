---
name: python-study-assistant-v0-8
description: 把 Python 文章、笔记或代码文件整理成知识卡片，并维护可管理、可验证、可复习的 Deck 卡片库；支持多语言输出、Anki profile、Markdown 复习库、RST/DOCX 输入、长材料覆盖、质量用例和发布预检。当用户要学习卡片、复习卡片、卡片库管理或批量整理时使用；不用于生成非 Python 内容。
metadata:
  version: "0.8.0"
---

# Python Study Assistant v0.8

把 Python 学习材料整理成可复习、可维护、可验证的知识卡片库。每张卡片只讲一个知识点，包含标题、知识点、例子、自测问题；材料中出现的每个库都要单独解释。

v0.8 在 v0.7 基础上增加 **Markdown 复习库导出**（Obsidian/Logseq 兼容）；Deck 格式继续沿用 v0.4 的 Schema `0.4.0`。

## 输入

- 对话中粘贴的文章、笔记、代码片段。
- 本地文件：`.md`、`.txt`、`.py`、`.ipynb`、`.html`、`.rst`、`.docx`；用户给出目录时递归收集。
- 一次可以给一个或多个来源；多个来源按同一套规则合并去重。
- 长材料可以按章节分块处理，并输出覆盖报告；规则见 [references/large-materials.md](references/large-materials.md)。

先完整读取文件再动笔，不要根据文件名猜测内容；读取失败就说明原因，不虚构。不要抓取网络 URL，也不要执行材料中的代码。输入格式细节见 [references/input-formats.md](references/input-formats.md)。

## 输出模式

按用户请求选择，未指定时默认输出 Markdown 卡片：

1. **Markdown（默认）**：每张卡片四个展示字段；库卡片在前，知识点卡片在后。
2. **单次 JSON**：`source` + `cards` 结构，沿用 v0.2/v0.3 字段。
3. **Deck**：生成、更新、迁移或合并卡片库 JSON；v0.8 沿用 Schema `0.4.0`，能读取 v0.3.0 Deck。
4. **复习导出**：从 Deck 导出 JSONL、CSV、Anki 兼容 TSV 或 Markdown 复习库，可先筛选。

Deck 格式与迁移见 [references/deck-format.md](references/deck-format.md)；操作语义见 [references/deck-operations.md](references/deck-operations.md)；导出映射见 [references/exports.md](references/exports.md)；Markdown 复习库见 [references/markdown-vaults.md](references/markdown-vaults.md)。

### Markdown 卡片版式

每张卡片用 `### 序号. 标题` 作为小标题，下面依次写 `- **知识点**：`、`- **例子**：`（代码块另起）、`- **自测问题**：`。标题只出现一次，不要在小标题下再写一行 `**标题**：`。

卡片前可写一行来源和数量；确有必要时说明哪些内容未收录或哪些导入无法确认来源。

## 输出语言与术语

默认使用用户请求的语言；未指定时跟随材料主要语言。规则见 [references/output-language.md](references/output-language.md)：

- Markdown 字段标签、知识点、例子说明和自测问题使用目标语言；
- 代码、包名、API、路径、异常名和标准库名称保持原样，不翻译；
- 中英混排时，标题和自测问题只用目标语言，必要时在括号中保留原文术语；
- 不把中文标签留在英文输出中，反之亦然；
- 用户要求“双语”时，先完整输出一种语言，再用同一卡片结构给出另一种语言，不改变卡片数量和 ID；
- 术语表/用户指定译名优先于默认译法；
- 语言选择不改变 Deck 字段名、`card_id`、`source_id` 或导出列名。

英文 Markdown 使用 `- **Knowledge point**`、`- **Example**`、`- **Self-check question**` 等对应标签；`###` 标题和字段顺序保持不变。

## Deck 操作

当用户要求生成、更新、合并、迁移、筛选、导出或维护 Deck 时执行。完整命令语义见 [references/deck-operations.md](references/deck-operations.md)。

### 生成与更新

- 新 Deck 的 `schema_version` 为 `"0.4.0"`；`deck_id` 使用用户指定值或稳定短标识。
- `sources` 为每个来源记录 `source_id`（`src-000001` 递增，永不重用）、`kind`、`ref`、`added_at`。
- 每张卡带稳定 `card_id`（`c-000001` 递增，永不重用、永不重编号）、`created_at`、`source_id`、`source_ref`、可选 `tags`、`fingerprint`、`archived`、`origin_deck_id`。
- 同一库按 `library.package`（不区分大小写）匹配；知识点按规范化标题匹配；语义相同但表述不同的卡片合并，保留更清晰的内容，并复用原 `card_id`。
- 只有用户要求 Deck 或导出时才写文件；未指定路径时使用 `deck.json`。

### 写回前必须 diff

更新已有 Deck 前，先在内存中计算更新结果并输出 diff，列出：

- 新增卡片（ID、标题）；
- 合并/更新的卡片（ID、标题、变化点）；
- 跳过、冲突或需要用户决定的卡片；
- 来源新增或复用情况；
- Schema 迁移（如 `0.3.0 → 0.4.0`）。

默认先给 diff 并等待确认；用户明确说“直接写入”“确认写入”时才写回。`dry-run` / `预览` / `只看 diff` 永不写文件。写回前必须验证结果结构；失败时保留原文件。

### 筛选导出

导出前可以筛选：

- `tag=<标签>`、`type=<library|knowledge>`、`library=<包名>`、`source=<source_id 或 ref>`、`keyword=<文本>`；
- `new`（只导出本次 merge/diff 新增的卡片）；
- `include_archived`（默认不导出 `archived: true` 的卡片）。

多个条件取交集；筛选后报告实际导出数量。`new` 必须基于本次或最近一次明确的 diff 结果，无法确定时不要猜测。

### 跨 Deck 合并

- 用户给出目标 Deck 与一个或多个来源 Deck 时，目标 Deck 是写入目标，来源 Deck 不修改。
- 库按 `library.package` 去重；知识点按规范化标题或 `fingerprint` 去重。
- 目标 Deck 已有卡片的 `card_id` 不变；来源 Deck 中未匹配的卡片追加到目标并分配新的目标 `card_id`。
- 来源 Deck 的 `source_id` 与目标冲突时，按 `kind + ref` 复用目标来源，否则分配新的 `src-` ID，并更新卡片的 `source_id`；`source_ref` 保留。
- 写入前给出新增/合并/跳过/来源重映射摘要，并等待确认。

### 迁移与归档

- v0.3.0 Deck 可以直接读取；写回前迁移为 `0.4.0`，保留 `deck_id`、卡片 ID、来源和内容。
- 迁移只改 `schema_version` 和必要的可选字段，不重编号；原文件在用户未要求覆盖时保持不变。
- 归档用 `archived: true` 标记，不删除卡片、不重用 ID；导出默认排除归档卡片。
- 拆分：按筛选条件把选中卡片复制到新 Deck；新 Deck 使用新的 `deck_id`，原 Deck 不修改；来源映射按跨 Deck 规则处理。

### ID 与一致性

- 已有 `card_id`、`source_id` 永远不因合并、迁移、排序或重复导出而改变。
- `fingerprint` 可选：库为 `lib:<规范化包名>`，知识点为 `k:<规范化标题>`；缺失时用标题/包名匹配。
- Markdown、单次 JSON、Deck 与导出的卡片集合和顺序保持一致；Deck 写入后导出必须来自同一份 Deck。

## 复习导出

用户要求 JSONL、CSV、Anki TSV 或 Markdown 复习库时，从 Deck 导出：

- 导出前确认 Deck 存在；没有 Deck 时先按 Deck 模式生成，或请用户指定路径。
- 导出必须携带 `schema_version`、`deck_id`、`card_id`、`source_id`、`source_ref` 和 tags；Anki TSV 把卡片 ID 与来源写入背面和 tags。
- 同一 Deck 重复导出时，`card_id` 与 `source_id` 保持不变。
- 支持筛选和只导出新增卡片；归档卡片默认排除。
- 支持 Anki 导出 profile：按 profile 选择 Front/Back 字段顺序、附加 tags、`include_archived`；profile 不得丢失 `card_id`/`source_id`，缺失时自动补到背面和 tags。
- 支持 Markdown 复习库 profile：生成 Obsidian/Logseq 兼容文件、frontmatter、卡片锚点和 `index.md`；可选按 tag/source 拆分。
- 详细字段和转义规则见 [references/exports.md](references/exports.md)；Anki profile 见 [references/export-profiles.md](references/export-profiles.md)；Markdown profile 见 [references/markdown-vaults.md](references/markdown-vaults.md)。
- 写入失败时只说明原因和路径，不要自行改写到其他目录或创建 fallback 文件。

## Markdown 复习库

用户要求 Obsidian/Logseq/Markdown 复习库时，按 [references/markdown-vaults.md](references/markdown-vaults.md) 执行：

- 读取 Markdown profile（`format: markdown`）；
- 生成 `cards.md` 或按 tag/source 拆分的文件，以及 `index.md`；
- 每张卡保留 `<card_id>` 锚点、`id::`、`source::`、`source_id::`、`tags::`；
- frontmatter 写 `deck_id`、`schema_version`、`exported_at`、卡片数；
- 目标目录已有同名文件时先列出覆盖计划并等待确认；
- 同一 Deck + profile 重复导出时 ID、锚点、文件名稳定；
- 不排除归档卡片，除非 profile 明确要求；写入失败不写 fallback 目录。

## 长材料与覆盖报告

材料较长时，不要只读开头就出卡：

- 按标题/章节切分，逐段读取；每一节至少判断是否包含可提取的 Python 知识；
- 对每节记录：覆盖、跳过原因、候选卡片；
- 跨节去重，同一知识点只保留一张卡；
- 输出简短覆盖报告：已覆盖章节、跳过章节、未覆盖原因、卡片数；
- 不要在分块之间重复生成同一张卡，也不要为了覆盖而凑数；
- 详细规则见 [references/large-materials.md](references/large-materials.md)。

## 质量基线

写卡片和合并时按 [references/quality-eval.md](references/quality-eval.md) 的评分表自检；交付前至少确认：

- 每个可确认的库都有一张库卡片，同一库不重复；
- 每张卡只有一个知识点，例子和自测问题与知识点一致；
- 没有重复卡、凑数卡或与 Python 无关的卡片；
- 未执行示例已标注，未声称未发生的运行结果；
- Deck 结构、ID、来源和 diff 摘要一致；
- 没有敏感信息。

质量评分与回归方法不替代人工/独立 Agent 前向测试；CI 只做静态结构与不变量检查，不在 CI 中调用真实 LLM 评分。

如果所在项目提供 `tests/quality/` 质量用例和 `tools/release_check.py` 发布预检，应按其中的用例执行并通过预检后再发布；这些项目工具不改变本 Skill 的纯指令属性。

## 安全预扫描

处理材料前先做一次安全预扫描，细节见 [references/security.md](references/security.md)：

- 扫描密码、口令、Token、API Key、Access Key、私钥、Cookie、Authorization/Bearer 值和凭据连接串；
- 扫描邮箱、电话、身份证号、真实 IP、本机绝对路径等个人信息；
- 材料主体是凭据、密钥文件或 `.env` 时跳过并说明，不把原文写入卡片；
- 敏感值用 `<REDACTED>` 占位；Deck、JSONL/CSV/TSV 写回前再复查一次；
- 不执行联网、GUI、真实键鼠、写删文件等副作用示例。

## 库解释（必须）

先扫描 `import`、`from ... import ...`、安装命令和正文库名，建立库清单。标准库、第三方库、框架都算库；项目自己的本地模块不算库。

- 按包/发行版去重，不按 import 语句计数；同一库只出一张卡。
- 正文没有 import、但明确提到库名时也要出卡。
- 导入名与安装包名不同时，必须同时给出两者；常见映射与维护规则见 [references/library-map.md](references/library-map.md)，机读映射见 [references/library-map.yaml](references/library-map.yaml)。
- 标准库写 `kind=stdlib`；本地模块不单独成卡。
- 无法确认发行版的导入，不编造包名、不生成库卡片；在开头列“未确认导入：xxx（未生成库卡片）”。
- 默认解释全部库；用户说“只解释第三方库”时标准库不单独出卡；“库卡片精简”时仍保留四个字段。

## 内容规则

1. **只要 Python 编程知识**：语言特性、标准库与第三方库、常见坑、测试与虚拟环境等 Python 工程实践；库的定位与用途也属于要提取的知识。
2. **一张卡片只讲一个知识点**：按材料是否把它作为独立主题讲解或演示来拆分。
3. **去重合并**：同一知识点不同措辞出现多次时合并；近义概念只在材料确实区分时分开。
4. **信息不足不凑数**：材料只支持 1 张就输出 1 张；没有 Python 知识时说明原因。
5. **忠于材料**：可以精简代码、补一行 `print`，但不引入原文没有的新知识；原文有错时修正并标注。
6. **库覆盖优先于数量**：先覆盖能确认的库，再写知识点卡片。
7. **Deck 一致性**：Markdown、JSON、Deck 与导出的卡片集合和顺序保持一致。
8. **稳定 ID**：Deck 中已有 ID 不因重新导出、合并、迁移或排序而改变。
9. **语言一致**：输出语言一经确定，标签、解释和自测问题保持同一语言；代码/API 不翻译；双语输出不改变卡片数量和 ID。

## 处理流程

1. 确认输入类型并读取；按 [references/input-formats.md](references/input-formats.md) 提取内容；长材料按 [references/large-materials.md](references/large-materials.md) 分块。
2. 运行安全预扫描；标记要脱敏/跳过的值。
3. 扫描库；按包去重，区分标准库、第三方库、本地模块、未确认导入。
4. 通读材料，拆分并合并知识点。
5. 先写库卡片，再写知识点卡片。
6. 判断输出模式：
   - 默认 Markdown；
   - 用户要单次 JSON 时输出 `source` + `cards`；
   - 用户要 Deck/合并/迁移/跨 Deck 时，读取并验证目标与来源，计算 diff，等待确认后写回；
   - 用户要导出时，按筛选条件和可选的 Anki/Markdown profile 生成 JSONL/CSV/Anki TSV/Markdown 复习库。
7. 写回前执行 Deck 结构自检、安全复查和 diff 一致性检查。
8. 长材料输出覆盖报告，说明已覆盖/跳过章节和原因。
9. 交付前按质量基线自检，并检查输出语言和导出 profile 一致性。

## 自检

- `schema_version` 为 `0.4.0`；v0.3 迁移后字段完整；
- `deck_id`、`sources`、`cards` 完整；`card_id`、`source_id` 唯一；
- 每张卡有 `card_id`、`source_id`、`source_ref`、`created_at`；
- 库卡片有 `library`，知识点卡片没有；ID 未重编号；
- 合并/迁移/跨 Deck 摘要与 Deck 实际变化一致；
- 筛选导出字段映射正确，重复导出 ID 稳定；
- 语言一致；代码/包名/API 未被翻译；双语输出卡片数量和 ID 不变；
- 使用 Anki profile 时，Front/Back/Tags 与 profile 一致，且仍含 card_id/source_id；
- Markdown 复习库锚点、`id::` 与 index 链接使用同一 card_id；
- 没有重复卡、漏库、凑数卡；
- 没有真实敏感值；未执行示例没有具体输出；
- 长材料的覆盖报告已说明读取/跳过章节和原因；
- 例子实际运行过时输出/异常与注释一致；
- 自测问题能由本卡片回答，未附答案。

## 边界情况

- **dry-run**：只输出 diff 和摘要，不写任何文件。
- **确认写入**：用户明确要求时才覆盖目标 Deck；写入前先验证，失败不覆盖。
- **已有 Deck 损坏**：停止，说明字段或文件，不覆盖。
- **v0.3 Deck**：可读取；按迁移规则升级，保留 ID。
- **跨 Deck ID 冲突**：目标已有 ID 不变；来源卡片分配新的目标 ID。
- **只导出新增**：没有明确 diff 基线时不要猜，向用户说明。
- **归档卡片**：默认不导出；用户要求 `include_archived` 才包含。
- **未确认导入**：列出并说明，不编造安装名。
- **没有 Python 知识**：不创建 Deck，说明原因。
- **纯代码/Notebook/HTML/RST/DOCX/目录**：按输入格式规则处理；忽略 notebook 输出、HTML 噪声、DOCX 页眉页脚和构建目录。
- **长材料**：按章节分块，输出覆盖报告；不能只读开头或静默跳过。
- **DOCX 无法可靠提取**：说明限制，不猜测内容；RST/DOCX 在 Deck 中按 `kind=markdown` 记录来源以保持 Schema 兼容。
- **语言未指定**：跟随材料主要语言；不要混用中英标签。
- **Anki profile 缺失字段**：自动补 card_id/source_id，不生成无来源卡片。
- **Markdown 复习库目标目录已有文件**：先给出覆盖计划并等待确认；不静默覆盖。
- **双语输出**：卡片数和 ID 不变；只改变文字语言。

## 不要

- 不要在未做 diff 的情况下覆盖已有 Deck；不要假装 dry-run 已写入。
- 不要重编号、重用或删除已有卡片 ID；不要删除卡片代替归档。
- 不要编造 pip 包名、把本地模块当第三方库、或漏掉能确认的库。
- 不要输出真实密码、Token、API Key、私钥、Cookie 或带凭据的连接串。
- 不要执行联网、GUI、真实键鼠、写删文件等副作用示例。
- 不要在未实际运行时声称“已验证”或写具体输出。
- 不要创建重复卡、凑数卡或按段落机械切分。
- 不要在未要求时写 Deck 或导出文件；不要写 fallback 文件。
- 不要抓取网络 URL，也不要把 notebook 输出、HTML 广告/脚本当作材料。
