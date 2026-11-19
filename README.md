# Python Study Assistant

把 Python 学习材料转换成知识卡片的开源 Skill。粘贴文章，或指定本地 Markdown、文本、Python、Notebook、HTML 或目录，即可得到四字段知识卡片，并自动解释材料中出现的每一个库。

当前仓库包含：

- **v0.9.0（已发布，推荐）**：`Skills/python-study-assistant-v0-9`
- **v0.8.0（已发布）**：`Skills/python-study-assistant-v0-8`
- **v0.7.0（已发布）**：`Skills/python-study-assistant-v0-7`
- **v0.6.0（已发布）**：`Skills/python-study-assistant-v0-6`
- **v0.5.0（已发布）**：`Skills/python-study-assistant-v0-5`
- **v0.4.0（已发布）**：`Skills/python-study-assistant-v0-4`
- **v0.3.0（已发布）**：`Skills/python-study-assistant-v0-3`
- **v0.2.0（已发布）**：`Skills/python-study-assistant-v0-2`
- **v0.1.0（已发布）**：`Skills/python-study-assistant`

v0.9.0 在 v0.8.0 基础上增加 Deck 集合与跨库检索；Deck 格式继续沿用 Schema `0.4.0`。

## 项目解决什么问题

Python 学习资料常常散落在文章、笔记、Notebook 和代码文件里：同一知识点反复出现，夹杂着与 Python 无关的内容，读完之后也不方便自测；材料里出现的第三方库往往“只会调用、不知道它是什么”。

这个 Skill 把材料整理成可以直接复习、可以持续维护的知识卡片：

- 每张卡片只保留一个知识点，并给出最小示例和自测问题；
- 自动合并重复表述、过滤非 Python 内容，材料信息不足时不凑数；
- 材料里出现的每个库单独解释，按包去重，并区分标准库、第三方库、本地模块和未确认导入；
- v0.9.0 支持 Deck 集合与跨库检索；Markdown 复习库、多语言、Anki profile、RST/DOCX、长材料、Deck 操作继续保留。

## 主要功能

v0.9.0（`Skills/python-study-assistant-v0-9`）：

- **多来源输入**：对话中粘贴的文本，以及本地 `.md` / `.txt` / `.py` / `.ipynb` / `.html` / `.rst` / `.docx` 文件；也可以递归处理目录。格式规则见 [references/input-formats.md](Skills/python-study-assistant-v0-9/references/input-formats.md)。
- **长材料覆盖**：长文按章节分块，输出已覆盖/跳过章节和原因；规则见 [references/large-materials.md](Skills/python-study-assistant-v0-9/references/large-materials.md)。
- **输出语言/术语**：支持中文/英文/双语输出；代码、包名、API 不翻译；术语表优先。规则见 [references/output-language.md](Skills/python-study-assistant-v0-9/references/output-language.md)。
- **Anki 导出 profile**：可配置 Front/Back 字段顺序、附加 tags、归档包含；仍保留 card_id/source_id。规则见 [references/export-profiles.md](Skills/python-study-assistant-v0-9/references/export-profiles.md)。
- **Markdown 复习库**：导出 Obsidian/Logseq 兼容的 `cards.md` + `index.md`，保留 card_id 锚点、来源和 tags。规则见 [references/markdown-vaults.md](Skills/python-study-assistant-v0-9/references/markdown-vaults.md)。
- **Deck 集合**：把多个 Deck 组织成只读集合，支持跨库搜索和按 Deck 导出；规则见 [references/collections.md](Skills/python-study-assistant-v0-9/references/collections.md)。
- **固定四字段**：每张卡片包含标题、知识点、例子、自测问题。

  | 字段 | 说明 |
  | --- | --- |
  | 标题 | 具体、可检索的知识点名称 |
  | 知识点 | 1–3 句话说明是什么、为什么重要、什么时候用 |
  | 例子 | 最小可运行的示例，展示该知识点的效果 |
  | 自测问题 | 能由本卡片内容回答的问题，不另附答案 |

- **一卡一知识点**：不把多个概念塞进一张卡，也不按原文段落机械切分。
- **去重与不凑数**：同一知识点多次出现时合并；材料只支持 1 张就输出 1 张，没有 Python 知识时说明原因，不编造。
- **库解释**：标准库、第三方库、框架每个库一张卡片，按包去重；给出“导入名 → 安装包名”映射（如 PIL→Pillow、bs4→beautifulsoup4），完整映射与未知导入处理见 [references/library-map.md](Skills/python-study-assistant-v0-9/references/library-map.md)，机读映射见 [references/library-map.yaml](Skills/python-study-assistant-v0-9/references/library-map.yaml)。
- **Deck 卡片库**：v0.9 沿用 `schema_version: "0.4.0"`，卡片带稳定 `card_id`、`created_at`、`source_id`、`source_ref`、可选 `fingerprint` / `archived` / `tags` / `origin_deck_id`；格式见 [references/deck-format.md](Skills/python-study-assistant-v0-9/references/deck-format.md)。
- **Deck 操作台**：
  - 写回前输出 diff，支持 dry-run/预览，不写文件；
  - 按 tag / type / library / source / keyword 筛选；
  - 支持“只导出本次新增卡片”；
  - 跨 Deck 合并、v0.3 Deck 迁移、归档与拆分；
  - 操作规则见 [references/deck-operations.md](Skills/python-study-assistant-v0-9/references/deck-operations.md)。
- **复习导出**：从 Deck 导出 JSONL、CSV、Anki 兼容 TSV；导出保留卡片 ID、来源和 tags，归档卡片默认排除。
- **结构化输出**：支持单次 JSON（`source` + `cards`）；Deck 使用 [tests/schema/deck-0.4.schema.json](tests/schema/deck-0.4.schema.json)，单次 JSON 使用 [tests/schema/cards.schema.json](tests/schema/cards.schema.json)。
- **质量用例**：机读用例见 [tests/quality/cases.json](tests/quality/cases.json)，结构见 [tests/quality/cases.schema.json](tests/quality/cases.schema.json)；评分方法见 [references/quality-eval.md](Skills/python-study-assistant-v0-9/references/quality-eval.md)。
- **发布预检**：`tools/release_check.py` 检查版本一致性、工作区、Tag 冲突并生成发布说明草稿；默认只读。
- **发布工作流**：`.github/workflows/release.yml` 通过 `workflow_dispatch` 和 `environment: release` 人工审批后创建 annotated Tag 和 Release。
- **安全预扫描**：处理前扫描密码、Token、API Key、私钥、Cookie、凭据连接串和个人信息；规则见 [references/security.md](Skills/python-study-assistant-v0-9/references/security.md)。
- **可选模式**：只解释第三方库、库卡片精简、只要库卡片/知识点卡片、指定卡片数量。
- **纯指令 Skill**：Skill 本体只有 `SKILL.md`、`agents/openai.yaml` 和 `references/` 文档，无运行脚本、无第三方依赖。

v0.4.0 提供 Deck 操作、跨 Deck 合并、v0.3 迁移和筛选导出；v0.3.0 提供 Notebook/HTML/目录输入和基础 Deck；v0.2.0 提供单次 JSON/文件导出；v0.1.0 提供最初的卡片生成能力。

## 目录结构

```text
.
├── .github
│   └── workflows
│       ├── skill-validate.yml
│       └── release.yml
├── CHANGELOG.md
├── LICENSE
├── README.md
├── RELEASE_CHECKLIST.md
├── Skills
│   ├── python-study-assistant          # v0.1.0（已发布）
│   ├── python-study-assistant-v0-2     # v0.2.0（已发布）
│   ├── python-study-assistant-v0-3     # v0.3.0（已发布）
│   ├── python-study-assistant-v0-4     # v0.4.0（已发布）
│   ├── python-study-assistant-v0-5     # v0.5.0（已发布）
│   ├── python-study-assistant-v0-6     # v0.6.0（已发布）
│   ├── python-study-assistant-v0-7     # v0.7.0（已发布）
│   ├── python-study-assistant-v0-8     # v0.8.0（已发布）
│   └── python-study-assistant-v0-9     # v0.9.0（已发布，推荐）
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/                 # Deck、集合、导出、语言、Markdown 复习库、质量、安全、库映射
├── tests
│   ├── fixtures/                       # v0.2 / v0.3 / v0.4 / v0.6 / v0.7 / v0.8 / v0.9 测试材料
│   ├── quality/                        # 机读质量用例
│   ├── schema/                         # cards、deck 0.3、deck 0.4、collection Schema
│   └── tools/                          # 官方 quick_validate.py 及许可证
└── tools
    ├── README.md
    └── release_check.py                # 只读发布预检
```

## 安装方法

1. 下载或克隆本项目。
2. 把 Skill 目录复制到客户端的 skills 目录：
   - 推荐版本：复制 `Skills/python-study-assistant-v0-9`
   - 使用已发布版本：复制 `Skills/python-study-assistant-v0-8`
   - 更早版本：复制 `Skills/python-study-assistant-v0-7`、`Skills/python-study-assistant-v0-6`、`Skills/python-study-assistant-v0-5`、`Skills/python-study-assistant-v0-4`、`Skills/python-study-assistant-v0-3`、`Skills/python-study-assistant-v0-2` 或 `Skills/python-study-assistant`
   - Codex 的默认位置：`~/.codex/skills/`（Windows：`%USERPROFILE%\.codex\skills\`）
   - 其他支持 `SKILL.md` 的客户端：放到其约定的 skills 目录
3. 刷新或重启客户端，让 Skill 被加载。

可选：用仓库内的官方校验脚本检查 Skill 结构：

```bash
python tests/tools/quick_validate.py Skills/python-study-assistant-v0-9
python tests/tools/quick_validate.py Skills/python-study-assistant-v0-8
python tests/tools/quick_validate.py Skills/python-study-assistant-v0-7
```

Windows 中文环境如果遇到 `UnicodeDecodeError`，先执行 `set PYTHONUTF8=1` 再运行。

## 使用方法

使用 v0.9.0：

```text
$python-study-assistant-v0-9 把 notes/pathlib.md 转换成知识卡片
$python-study-assistant-v0-9 按 tests/fixtures/v0.8/review-profile.yaml 从 deck.json 导出 Markdown 复习库
$python-study-assistant-v0-9 把 tests/fixtures/v0.7/english_material.md 转换成英文知识卡片
$python-study-assistant-v0-9 按 tests/fixtures/v0.9/collection.json 跨库检索 pathlib
```

Deck 操作：

```text
$python-study-assistant-v0-9 把 notes.md 生成 deck.json
$python-study-assistant-v0-9 预览把 notes.md 合并到 deck.json
$python-study-assistant-v0-9 把 notes.md 合并到 deck.json
$python-study-assistant-v0-9 把 deck-other.json 合并到 deck.json
$python-study-assistant-v0-9 把 v0.3 的 deck 迁移到 v0.4
```

筛选与导出：

```text
$python-study-assistant-v0-9 从 deck.json 导出 tag=stdlib 的 CSV
$python-study-assistant-v0-9 在本次合并预览后只导出新增卡片的 JSONL
$python-study-assistant-v0-9 从 deck.json 导出 include_archived 的 Anki TSV
```

发布预检（项目工具，不属于 Skill 运行时）：

```bash
python tools/release_check.py --version 0.9.0
python tools/release_check.py --version 0.9.0 --notes-file /tmp/release-notes.md
```

发布前需要工作区干净；预检默认只读，不执行 Git 写操作。

支持输入：对话中粘贴的文本、`.md`、`.txt`、`.py`、`.ipynb`、`.html` 和目录，可一次提供多个来源。

## 输入输出示例

### 输入（粘贴一段 `pathlib` 学习材料）

~~~markdown
# 用 pathlib 处理路径

Python 的 pathlib 用 Path 对象表示文件路径，比直接拼接字符串更清晰。
`Path("data") / "file.txt"` 会得到 `data/file.txt`；`Path("data/file.txt").parent` 可以取父目录。
~~~

### 输出（v0.7.0 Markdown 模式）

~~~markdown
共 3 张卡片（来源：粘贴的文本）

### 1. pathlib：面向对象的路径操作（标准库）

- **知识点**：`pathlib` 是 Python 标准库，用 `Path` 对象表示路径，支持 `/` 拼接、`.parent` 取父目录、`glob()` 等操作，无需 pip 安装。材料用它替代字符串拼接来处理文件路径。
- **例子**：
```python
from pathlib import Path

path = Path("data") / "file.txt"
print(path)  # Windows: data\file.txt；Linux/macOS: data/file.txt
```
- **自测问题**：`pathlib` 属于标准库还是第三方库？安装它需要执行 pip 命令吗？

### 2. 用 / 运算符拼接 Path 路径

- **知识点**：`Path` 重载了 `/` 运算符，把路径片段依次连接成一个新的 `Path` 对象，比手写字符串拼接更清晰，也不会因为漏写斜杠而出错。
- **例子**：
```python
from pathlib import Path

print(Path("data") / "file.txt")  # Windows: data\file.txt
```
- **自测问题**：`Path("data") / "file.txt"` 得到的是什么对象，和字符串拼接相比有什么好处？

### 3. 用 Path.parent 取父目录

- **知识点**：`Path.parent` 返回当前路径的父目录；对 `Path("data/file.txt")` 来说，父目录是 `Path("data")`。
- **例子**：
```python
from pathlib import Path

print(Path("data/file.txt").parent)  # data
```
- **自测问题**：`Path("data/file.txt").parent` 返回哪个路径？
~~~

### Deck diff 与导出

更新已有 Deck 前会先给出 diff；`dry-run` 不写文件。例如：

```text
Deck diff (dry-run)
target: deck.json
schema: 0.4.0
sources: + src-000002 (merge-material.md)
+ 新增 c-000004  用 Path.glob 按通配符查找文件
= 跳过 c-000001  pathlib：面向对象的路径操作（标准库）
= 跳过 c-000002  用 / 运算符拼接 Path 路径
= 跳过 c-000003  用 Path.parent 取父目录
summary: 新增 1 / 合并 0 / 跳过 3
```

确认后写回，并可从 Deck 生成 JSONL、CSV 或 Anki TSV；字段映射见 [references/exports.md](Skills/python-study-assistant-v0-9/references/exports.md)。Deck 结构见 [tests/schema/deck-0.4.schema.json](tests/schema/deck-0.4.schema.json)。

## 验证

仓库包含 v0.2 回归材料、v0.3 输入/Deck 材料、v0.4 Deck 操作材料、v0.5 质量用例与发布工具、v0.6 RST/DOCX/长材料材料、v0.7 多语言/Anki profile 材料、v0.8 Markdown 复习库材料、v0.9 Deck 集合材料，以及 GitHub Actions 校验工作流：

- 分别校验 v0.2、v0.3、v0.4、v0.5、v0.6、v0.7、v0.8、v0.9 Skill 结构；
- 校验 cards、deck 0.3、deck 0.4、collection Schema 和示例 Deck/集合；
- 校验质量用例 fixture、RST/DOCX/长材料/多语言/Markdown 复习库/集合 fixture、库映射 YAML、发布预检脚本和发布 workflow；
- 扫描测试材料，禁止真实 Token 前缀、私钥格式和本机路径误入公开仓库；
- 检查 README、CHANGELOG、SKILL.md、agents/openai.yaml 的 v0.9.0 版本标记一致。

v0.9.0 的本地验证已覆盖 Deck 集合、跨库检索、Markdown 复习库、英文输出、Anki profile、RST/DOCX/长材料回归、质量用例、发布预检和 A* Python 代码测试；`quick_validate.py`、Schema 与本地等价的 CI 静态检查均通过。

> v0.9.0 已发布；v0.8.0 是上一个发布版本。

## 开源协议

[MIT](LICENSE)
