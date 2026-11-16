# 输入格式规则（v0.4.0）

## 通用规则

- 先完整读取文件，再提取内容；不要根据文件名猜测内容。
- 不抓取网络 URL，不执行材料中的代码。
- 每个文件或粘贴文本对应一个来源；来源 ID 与 `source_ref` 由 Deck 规则分配。
- 多个来源先分别提取，再统一去重；同一知识点只保留一张卡。
- 不支持的文件类型直接说明跳过，不要伪装成已读取。

## Markdown / TXT

- 直接读取正文；保留标题层级、列表、代码块和链接文字。
- 忽略纯装饰性内容（分隔线、目录锚点、重复页眉页脚）和与 Python 无关的段落。
- `source_ref` 使用相对文件名；需要时可加标题或小节说明。

## Python 代码文件

- 读取完整源码；按代码演示的 Python 概念出卡。
- 忽略 `import` 样板、`if __name__ == "__main__"` 样板和重复注释；导入的库仍按库解释规则出卡。
- 同一概念在多个函数/文件中出现时只出一张卡。

## Jupyter Notebook（.ipynb）

- 按 JSON 的 `cells` 数组顺序读取。
- 只使用两类 cell：
  - `cell_type = "markdown"`：读取 `source` 中的文本；
  - `cell_type = "code"`：读取 `source` 中的代码。
- 忽略 `outputs`、`execution_count`、`metadata` 以及隐藏/删除的 cell；绝不能把 notebook 输出当作材料内容。
- `source_ref` 写成 `文件名.ipynb:cell-<序号>`，序号使用 `cells` 数组的 0-based 下标。
- markdown cell 与 code cell 讲同一知识点时合并为一张卡；不要一个 cell 一张卡。
- 空 cell、纯导入 cell、纯输出 cell 不单独成卡。
- 如果 notebook 里的代码依赖已保存的图片/数据文件，不在示例中声称运行，标注依赖。

## HTML（.html）

- 从未被脚本执行的静态文本中提取：
  - 页面标题、`h1`–`h3` 等标题；
  - 正文段落、列表项；
  - `pre` / `code` 代码块及其语言标记（如有）。
- 过滤：`nav`、`footer`、`aside`、`script`、`style`、`noscript`、广告/推荐/订阅区域、导航链接和无正文的侧栏。
- 保留解释性文字与代码；不要把 HTML 标签、CSS 选择器、脚本变量名当作 Python 知识。
- `source_ref` 使用相对文件名；页面内小节可用标题文字补充。
- 不做网页抓取，也不解析远程 URL；用户只给 URL 时请附上正文或下载为文件。

## 目录批量（directory）

- 递归收集扩展名：`.md`、`.txt`、`.py`、`.ipynb`、`.html`。
- 跳过：
  - 以 `.` 开头的目录和文件；
  - `.git`、`node_modules`、`.venv`、`venv`、`__pycache__`、`.pytest_cache`、`dist`、`build`、`.tox` 等构建/缓存目录；
  - 明显的二进制文件和非支持扩展名。
- 按相对路径排序后处理，保证同一目录的批量结果与逐文件处理一致。
- 目录本身作为一个 `kind=directory` 来源加入 Deck 的 `sources`；卡片的 `source_ref` 仍指向具体文件。
- 不跟随符号链接，避免循环和越界读取。
- 批量去重与单文件去重使用同一套规则：跨文件重复的知识点只保留一张卡，库卡片按包合并。

## 多来源与粘贴文本

- 粘贴文本的来源 `kind=paste`，`ref=对话中粘贴的文本`；多段粘贴可合并为一个来源。
- 多个文件按用户给出顺序或相对路径顺序处理；不因处理顺序改变 `card_id` 的分配规则。
- 只有在 Deck 模式下才需要写 `source_id`；Markdown/单次 JSON 模式可只保留来源说明。
