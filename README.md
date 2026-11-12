# Python Study Assistant

把 Python 学习材料转换成知识卡片的开源 Skill。粘贴文章，或指定本地 `.md` / `.txt` / `.py` 文件，即可得到一组四字段知识卡片，并自动解释材料中出现的每一个库。

## 项目解决什么问题

Python 学习资料常常散落在文章、笔记和代码文件里：同一知识点反复出现，夹杂着与 Python 无关的内容，读完之后也不方便自测。这个 Skill 把材料整理成可以直接复习的知识卡片：

- 每张卡片只保留一个知识点，并给出最小示例和自测问题；
- 自动合并重复表述、过滤非 Python 内容，材料信息不足时不凑数；
- 材料里出现的每个库都会单独解释，避免“只会调用、不知道它是什么”；
- 输出格式固定，方便复习和检查。

## 主要功能

- **多来源输入**：对话中粘贴的文本，以及本地 `.md` / `.txt` / `.py` 文件，可一次处理多个来源。
- **固定四字段**：每张卡片包含标题、知识点、例子、自测问题。

  | 字段 | 说明 |
  | --- | --- |
  | 标题 | 具体、可检索的知识点名称 |
  | 知识点 | 1–3 句话说明是什么、为什么重要、什么时候用 |
  | 例子 | 最小可运行的示例，展示该知识点的效果 |
  | 自测问题 | 能由本卡片内容回答的问题，不另附答案 |

- **一张卡片一个知识点**：不把多个概念塞进一张卡，也不按原文段落机械切分。
- **去重与不凑数**：同一知识点多次出现时合并；材料只支持 1 张就输出 1 张，没有 Python 知识时说明原因，不编造。
- **库解释**：标准库模块、第三方库、框架每个库一张卡片，按包去重（`PyQt6.QtCore` 和 `PyQt6.QtWidgets` 算同一个 PyQt6）；项目自己的本地模块不算库。库卡片排在知识点卡片之前，并计入总数。
- **知识过滤**：只保留 Python 编程知识，其他语言、通用学习建议、无关内容不进入卡片。
- **纯指令实现**：只有 `SKILL.md` 和 `agents/openai.yaml`，没有脚本，也没有第三方依赖。

## 目录结构

```text
.
├── LICENSE
├── README.md
└── Skills
    └── python-study-assistant
        ├── SKILL.md
        └── agents
            └── openai.yaml
```

## 安装方法

1. 下载或克隆本项目。
2. 把 `Skills/python-study-assistant` 整个目录复制到客户端的 skills 目录，例如：
   - Codex：`~/.codex/skills/`（Windows：`%USERPROFILE%\.codex\skills\`）
   - 其他支持 `SKILL.md` 的客户端：放到其约定的 skills 目录
3. 刷新或重启客户端，让 Skill 被加载。

可选：用 `skill-creator` 自带的官方脚本校验 Skill 结构（把 `quick_validate.py` 换成实际路径）：

```bash
python quick_validate.py Skills/python-study-assistant
```

Windows 中文环境如果遇到 `UnicodeDecodeError`，先执行 `set PYTHONUTF8=1` 再运行。

## 使用方法

显式调用：

```text
$python-study-assistant 把 notes/generators.md 转换成知识卡片
```

也可以直接用自然语言提出请求（客户端支持自动选择时会自动调用）：

```text
帮我把下面这篇文章整理成知识卡片：
（粘贴文章内容）
```

```text
把这几个文件转成复习卡片：demo/decorators.py demo/errors.py
```

支持的输入：对话中粘贴的文本、`.md`、`.txt`、`.py`，可一次提供多个来源。

## 输入输出示例

### 输入（粘贴一段介绍 `requests` 的文章）

~~~markdown
# 用 requests 抓取网页

`requests` 是 Python 中常用的 HTTP 库。用 `requests.get(url)` 可以发送 GET 请求并读取网页内容。

注意请求要设置超时。如果不设置 timeout，服务器一直不响应时程序会一直卡住；设置 `timeout=5` 后，5 秒内没有响应就会抛出 `requests.Timeout` 异常，可以用 try/except 捕获。

```python
import requests

try:
    resp = requests.get("https://example.com", timeout=5)
    print(resp.text)
except requests.Timeout:
    print("请求超时")
```
~~~

### 输出

~~~markdown
共 3 张卡片（来源：粘贴的文本）

### 1. requests：常用的第三方 HTTP 客户端库

- **知识点**：`requests` 是 Python 中常用的第三方 HTTP 库，用简单的函数调用就能发送 HTTP 请求并读取响应；安装名与导入名相同，都是 `requests`（`pip install requests`）。材料里它负责抓取网页：发送 GET 请求并取出页面内容。
- **例子**：
```python
import requests

resp = requests.get("https://example.com", timeout=5)
print(resp.status_code)  # 200
print(resp.text[:15])    # <!doctype html>
```
- **自测问题**：材料用 `requests` 完成什么任务，而用 pip 安装它时写的包名是什么？

### 2. requests.get 发送 GET 请求并返回 Response 对象

- **知识点**：`requests.get(url)` 向 `url` 发送一个 GET 请求，返回一个 `Response` 对象；网页正文通过 `resp.text` 取成字符串，之后就能打印或继续处理。
- **例子**：
```python
import requests

resp = requests.get("https://example.com", timeout=5)
print(type(resp).__name__)  # Response
print(resp.text[:15])       # <!doctype html>
```
- **自测问题**：执行 `resp = requests.get(url)` 之后，要从 `resp` 上取网页的 HTML 文本，应该访问它的哪个属性？

### 3. 请求要设置 timeout，并用 try/except 捕获 requests.Timeout

- **知识点**：`requests.get` 不设置 `timeout` 时，如果服务器一直不响应，程序会一直卡住；写成 `timeout=5` 后，5 秒内没有响应就会抛出 `requests.Timeout` 异常，用 try/except 捕获后就可以自己处理，比如提示“请求超时”。
- **例子**：
```python
import requests

try:
    resp = requests.get("https://example.com", timeout=5)
    print(resp.text[:15])  # <!doctype html>
except requests.Timeout:
    print("请求超时")       # 服务器 5 秒内没响应时走这里
```
- **自测问题**：如果服务器在 5 秒内没有响应，例子中哪一句会抛出哪个异常，又会被哪个分支捕获？
~~~

上面的输入涉及一个库和两个具体知识点，因此输出 3 张卡片：1 张 `requests` 库卡片和 2 张知识点卡片。这份示例就是按 Skill 规则实际处理得到的输出。

## 验证

本项目用 `skill-creator` 的官方校验脚本检查过 Skill 结构，结果为 `Skill is valid!`。此外已用代码文件、技术文章、混合内容、非 Python 内容、粘贴短文等 6 类输入做过前向测试，并对库解释规则单独做了标准库、第三方库、本地模块混用的测试。

## 开源协议

[MIT](LICENSE)
