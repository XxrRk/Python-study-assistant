# Python Study Assistant

把 Python 学习材料转换成知识卡片的开源 Skill。粘贴文章，或指定本地 `.md` / `.txt` / `.py` 文件，即可得到四字段知识卡片，并自动解释材料中出现的每一个库。

当前仓库包含两个版本：

- **v0.2.0（推荐，最新版本）**：`Skills/python-study-assistant-v0-2`
- **v0.1.0（已发布版本）**：`Skills/python-study-assistant`

v0.2.0 在 v0.1.0 的基础上增加了结构化 JSON/文件导出、库别名映射、安全脱敏与副作用策略，并补充了测试与 CI。

## 项目解决什么问题

Python 学习资料常常散落在文章、笔记和代码文件里：同一知识点反复出现，夹杂着与 Python 无关的内容，读完之后也不方便自测；材料里出现的第三方库往往“只会调用、不知道它是什么”。

这个 Skill 把材料整理成可以直接复习的知识卡片：

- 每张卡片只保留一个知识点，并给出最小示例和自测问题；
- 自动合并重复表述、过滤非 Python 内容，材料信息不足时不凑数；
- 材料里出现的每个库单独解释，按包去重，并区分标准库、第三方库和本地模块；
- v0.2.0 支持 JSON 结构化输出、Markdown/JSON 文件导出和安全脱敏，便于复习、自动化处理和二次开发。

## 主要功能

v0.2.0（`Skills/python-study-assistant-v0-2`）：

- **多来源输入**：对话中粘贴的文本，以及本地 `.md` / `.txt` / `.py` 文件，可一次处理多个来源。
- **固定四字段**：每张卡片包含标题、知识点、例子、自测问题。

  | 字段 | 说明 |
  | --- | --- |
  | 标题 | 具体、可检索的知识点名称 |
  | 知识点 | 1–3 句话说明是什么、为什么重要、什么时候用 |
  | 例子 | 最小可运行的示例，展示该知识点的效果 |
  | 自测问题 | 能由本卡片内容回答的问题，不另附答案 |

- **一卡一知识点**：不把多个概念塞进一张卡，也不按原文段落机械切分。
- **去重与不凑数**：同一知识点多次出现时合并；材料只支持 1 张就输出 1 张，没有 Python 知识时说明原因，不编造。
- **库解释**：标准库、第三方库、框架每个库一张卡片，按包去重；给出“导入名 → 安装包名”映射（如 PIL→Pillow、bs4→beautifulsoup4），项目本地模块不单独成卡。
- **结构化输出**：支持 JSON 输出，以及保存为 Markdown/JSON 文件；JSON 卡片带 `type`、`library`、可选 `source_ref`，Schema 见 [tests/schema/cards.schema.json](tests/schema/cards.schema.json)。
- **安全策略**：密码、Token、API Key、私钥等敏感值脱敏；联网、GUI、真实键鼠、写删文件等副作用示例不执行并标注。
- **可选模式**：只解释第三方库、库卡片精简、只要库卡片/知识点卡片、指定卡片数量。
- **纯指令 Skill**：Skill 本体只有 `SKILL.md` 和 `agents/openai.yaml`，无运行脚本、无第三方依赖。

v0.1.0（`Skills/python-study-assistant`）提供基础的四字段卡片、去重、库解释和本地文件输入；不支持 v0.2.0 的 JSON 导出、库别名映射和安全策略。

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
│   └── python-study-assistant-v0-2     # v0.2.0（最新版本，推荐）
└── tests
    ├── fixtures/                       # 前向测试材料
    ├── schema/                         # JSON 输出 Schema
    └── tools/                          # 官方 quick_validate.py 及许可证
```

## 安装方法

1. 下载或克隆本项目。
2. 把 Skill 目录复制到客户端的 skills 目录：
   - 推荐：复制 `Skills/python-study-assistant-v0-2`
   - 使用已发布版本：复制 `Skills/python-study-assistant`
   - Codex 的默认位置：`~/.codex/skills/`（Windows：`%USERPROFILE%\.codex\skills\`）
   - 其他支持 `SKILL.md` 的客户端：放到其约定的 skills 目录
3. 刷新或重启客户端，让 Skill 被加载。

可选：用仓库内的官方校验脚本检查 Skill 结构：

```bash
python tests/tools/quick_validate.py Skills/python-study-assistant-v0-2
python tests/tools/quick_validate.py Skills/python-study-assistant
```

Windows 中文环境如果遇到 `UnicodeDecodeError`，先执行 `set PYTHONUTF8=1` 再运行。

## 使用方法

使用 v0.2.0：

```text
$python-study-assistant-v0-2 把 notes/pathlib.md 转换成知识卡片
```

```text
帮我把下面这篇文章整理成 Python 知识卡片：
（粘贴文章内容）
```

v0.2.0 还支持：

```text
$python-study-assistant-v0-2 把 tests/fixtures/01_alias_libraries.py 转成知识卡片，输出 JSON
$python-study-assistant-v0-2 把 notes.md 转成卡片，保存为 cards.md
$python-study-assistant-v0-2 把这篇文章转成卡片，只解释第三方库
```

使用 v0.1.0：

```text
$python-study-assistant 把 notes/pathlib.md 转换成知识卡片
```

支持的输入：对话中粘贴的文本、`.md`、`.txt`、`.py`，可一次提供多个来源。

## 输入输出示例

### 输入（粘贴一段 `pathlib` 学习材料）

~~~markdown
# 用 pathlib 处理路径

Python 的 pathlib 用 Path 对象表示文件路径，比直接拼接字符串更清晰。
`Path("data") / "file.txt"` 会得到 `data/file.txt`；`Path("data/file.txt").parent` 可以取父目录。
~~~

### 输出（v0.2.0 Markdown 模式）

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

- **知识点**：`Path.parent` 返回当前路径的父目录；对 `Path("data/file.txt")` 来说，父目录是 `Path("data")`，常用于从文件路径回到它所在的目录。
- **例子**：
```python
from pathlib import Path

print(Path("data/file.txt").parent)  # data
```
- **自测问题**：`Path("data/file.txt").parent` 返回哪个路径？
~~~

如果要求“输出 JSON”，同一材料会得到相同卡片，并在每张卡片外层附带 `type`、`library`、可选 `source_ref` 等元数据，结构见 [tests/schema/cards.schema.json](tests/schema/cards.schema.json)。

## 验证

仓库包含 8 份前向测试材料（[tests/fixtures](tests/fixtures)）和 GitHub Actions 校验工作流（[.github/workflows/skill-validate.yml](.github/workflows/skill-validate.yml)）：

- 运行 `quick_validate.py` 校验 Skill 结构；
- 校验 JSON Schema 和测试材料完整性；
- 检查 `SKILL.md` 是否包含结构化输出、库解释、脱敏、副作用等关键章节。

v0.2.0 的本地校验结果为 `Skill is valid!`，JSON 输出已通过 Schema 校验。

> v0.2.0 已发布；v0.1.0 是上一个发布版本。

## 开源协议

[MIT](LICENSE)
