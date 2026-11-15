# Python Study Assistant

把 Python 学习材料转换成知识卡片的开源 Skill。粘贴文章，或指定本地 Markdown、文本、Python、Notebook、HTML 或目录，即可得到四字段知识卡片，并自动解释材料中出现的每一个库。

当前仓库包含：

- **v0.3.0（开发版，推荐）**：`Skills/python-study-assistant-v0-3`
- **v0.2.0（已发布）**：`Skills/python-study-assistant-v0-2`
- **v0.1.0（已发布）**：`Skills/python-study-assistant`

v0.3.0 在 v0.2.0 基础上增加了 Deck 卡片库与增量合并、`.ipynb` / `.html` / 目录输入、JSONL / CSV / Anki TSV 导出，以及更完整的测试和 CI。

## 项目解决什么问题

Python 学习资料常常散落在文章、笔记、Notebook 和代码文件里：同一知识点反复出现，夹杂着与 Python 无关的内容，读完之后也不方便自测；材料里出现的第三方库往往“只会调用、不知道它是什么”。

这个 Skill 把材料整理成可以直接复习、可以持续维护的知识卡片：

- 每张卡片只保留一个知识点，并给出最小示例和自测问题；
- 自动合并重复表述、过滤非 Python 内容，材料信息不足时不凑数；
- 材料里出现的每个库单独解释，按包去重，并区分标准库、第三方库、本地模块和未确认导入；
- v0.3.0 支持 Deck 增量合并与多格式导出，便于把多批材料整理成同一个卡片库。

## 主要功能

v0.3.0（`Skills/python-study-assistant-v0-3`）：

- **多来源输入**：对话中粘贴的文本，以及本地 `.md` / `.txt` / `.py` / `.ipynb` / `.html` 文件；也可以递归处理目录。格式规则见 [references/input-formats.md](Skills/python-study-assistant-v0-3/references/input-formats.md)。
- **固定四字段**：每张卡片包含标题、知识点、例子、自测问题。

  | 字段 | 说明 |
  | --- | --- |
  | 标题 | 具体、可检索的知识点名称 |
  | 知识点 | 1–3 句话说明是什么、为什么重要、什么时候用 |
  | 例子 | 最小可运行的示例，展示该知识点的效果 |
  | 自测问题 | 能由本卡片内容回答的问题，不另附答案 |

- **一卡一知识点**：不把多个概念塞进一张卡，也不按原文段落机械切分。
- **去重与不凑数**：同一知识点多次出现时合并；材料只支持 1 张就输出 1 张，没有 Python 知识时说明原因，不编造。
- **库解释**：标准库、第三方库、框架每个库一张卡片，按包去重；给出“导入名 → 安装包名”映射（如 PIL→Pillow、bs4→beautifulsoup4），完整映射与未知导入处理见 [references/library-map.md](Skills/python-study-assistant-v0-3/references/library-map.md)；本地模块不单独成卡，无法确认发行版的导入不会编造包名。
- **Deck 卡片库**：`schema_version`、`deck_id`、`sources`、`cards` 容器；卡片带稳定 `card_id`、`created_at`、`source_id`、`source_ref`、可选 tags；支持把新材料合并到已有 Deck，并输出“新增 / 合并 / 跳过”摘要；格式与合并规则见 [references/deck-format.md](Skills/python-study-assistant-v0-3/references/deck-format.md)。
- **复习导出**：从 Deck 导出 JSONL、CSV、Anki 兼容 TSV；导出保留卡片 ID、来源和 tags。
- **结构化输出**：支持单次 JSON（`source` + `cards`）；Deck 使用 [tests/schema/deck.schema.json](tests/schema/deck.schema.json)，单次 JSON 使用 [tests/schema/cards.schema.json](tests/schema/cards.schema.json)。
- **安全策略**：密码、Token、API Key、私钥等敏感值脱敏；联网、GUI、真实键鼠、写删文件等副作用示例不执行并标注。
- **可选模式**：只解释第三方库、库卡片精简、只要库卡片/知识点卡片、指定卡片数量。
- **纯指令 Skill**：Skill 本体只有 `SKILL.md`、`agents/openai.yaml` 和 `references/` 文档，无运行脚本、无第三方依赖。

v0.2.0 提供四字段卡片、单次 JSON/文件导出和基础安全策略；v0.1.0 提供最初的卡片生成能力。

## 目录结构

```text
.
├── .github
│   └── workflows
│       └── skill-validate.yml
├── CHANGELOG.md
├── LICENSE
├── README.md
├── RELEASE_CHECKLIST.md
├── Skills
│   ├── python-study-assistant          # v0.1.0（已发布）
│   ├── python-study-assistant-v0-2     # v0.2.0（已发布）
│   └── python-study-assistant-v0-3     # v0.3.0（开发版，推荐）
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/                 # Deck、输入格式、导出、库映射
└── tests
    ├── fixtures/                       # v0.2 与 v0.3 测试材料
    ├── schema/                         # cards / deck Schema
    └── tools/                          # 官方 quick_validate.py 及许可证
```

## 安装方法

1. 下载或克隆本项目。
2. 把 Skill 目录复制到客户端的 skills 目录：
   - 推荐：复制 `Skills/python-study-assistant-v0-3`
   - 使用已发布版本：复制 `Skills/python-study-assistant-v0-2`
   - 最早版本：复制 `Skills/python-study-assistant`
   - Codex 的默认位置：`~/.codex/skills/`（Windows：`%USERPROFILE%\.codex\skills\`）
   - 其他支持 `SKILL.md` 的客户端：放到其约定的 skills 目录
3. 刷新或重启客户端，让 Skill 被加载。

可选：用仓库内的官方校验脚本检查 Skill 结构：

```bash
python tests/tools/quick_validate.py Skills/python-study-assistant-v0-3
python tests/tools/quick_validate.py Skills/python-study-assistant-v0-2
python tests/tools/quick_validate.py Skills/python-study-assistant
```

Windows 中文环境如果遇到 `UnicodeDecodeError`，先执行 `set PYTHONUTF8=1` 再运行。

## 使用方法

使用 v0.3.0：

```text
$python-study-assistant-v0-3 把 notes/pathlib.md 转换成知识卡片
```

```text
$python-study-assistant-v0-3 把 tests/fixtures/v0.3/notebook_demo.ipynb 转成知识卡片
$python-study-assistant-v0-3 把 tests/fixtures/v0.3/article_noise.html 转成知识卡片
$python-study-assistant-v0-3 把 tests/fixtures/v0.3/batch 目录批量转成知识卡片
```

Deck 与导出：

```text
$python-study-assistant-v0-3 把 notes.md 生成 deck.json
$python-study-assistant-v0-3 把 notes.md 合并到 deck.json
$python-study-assistant-v0-3 从 deck.json 导出 JSONL
$python-study-assistant-v0-3 从 deck.json 导出 CSV
$python-study-assistant-v0-3 从 deck.json 导出 Anki TSV
```

使用 v0.2.0 / v0.1.0：

```text
$python-study-assistant-v0-2 把 notes/pathlib.md 转换成知识卡片
$python-study-assistant 把 notes/pathlib.md 转换成知识卡片
```

支持的输入：对话中粘贴的文本、`.md`、`.txt`、`.py`、`.ipynb`、`.html` 和目录，可一次提供多个来源。

## 输入输出示例

### 输入（粘贴一段 `pathlib` 学习材料）

~~~markdown
# 用 pathlib 处理路径

Python 的 pathlib 用 Path 对象表示文件路径，比直接拼接字符串更清晰。
`Path("data") / "file.txt"` 会得到 `data/file.txt`；`Path("data/file.txt").parent` 可以取父目录。
~~~

### 输出（v0.3.0 Markdown 模式）

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

### Deck 与导出

同一材料在 Deck 模式下会写入 `deck.json`，卡片带稳定 `card_id`、`source_id`、`created_at`；再次合并同一材料时不会新增重复卡。合并结果会给出摘要，例如：

```text
Deck updated: deck.json
新增 3 张 / 合并 0 张 / 跳过 0 张
```

随后可以从该 Deck 生成 JSONL、CSV 或 Anki TSV；字段映射和转义规则见 [Skills/python-study-assistant-v0-3/references/exports.md](Skills/python-study-assistant-v0-3/references/exports.md)。单次 JSON 结构见 [tests/schema/cards.schema.json](tests/schema/cards.schema.json)，Deck 结构见 [tests/schema/deck.schema.json](tests/schema/deck.schema.json)。

## 验证

仓库包含 v0.2 的 8 份回归材料、v0.3 的 Notebook/HTML/目录/Deck/导出测试材料，以及 GitHub Actions 校验工作流（[.github/workflows/skill-validate.yml](.github/workflows/skill-validate.yml)）：

- 分别校验 v0.2、v0.3 Skill 结构；
- 校验 `cards.schema.json`、`deck.schema.json` 和示例 Deck；
- 检查两代测试材料完整性；
- 扫描测试材料，禁止真实 Token 前缀、私钥格式和本机路径误入公开仓库；
- 检查 README、CHANGELOG、SKILL.md、agents/openai.yaml 的 v0.3.0 版本标记一致。

v0.3.0 的本地测试已覆盖 Notebook、HTML、目录批量、Deck 合并与重复合并、JSONL/CSV/Anki 导出、别名映射和未知导入；`quick_validate.py`、Deck Schema 与 CI 静态检查均通过。

> v0.3.0 已提交 main，尚未创建 GitHub Release；v0.2.0 是已发布版本。

## 开源协议

[MIT](LICENSE)
