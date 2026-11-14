# 测试材料与不变量

本目录用于验证 `Skills/python-study-assistant-v0-2`（目标版本 0.2.0）。

- `fixtures/`：输入材料，只包含测试用数据（`05_secrets.py` 中的密钥全部是伪造值）。
- `schema/cards.schema.json`：结构化 JSON 输出的 JSON Schema。
- `tools/`：官方 `quick_validate.py` 及其 Apache-2.0 许可证，供 CI 使用。
- 本目录不添加 Skill 运行脚本；行为验证由人工或独立 Agent 前向测试完成。

## 前向测试方法

1. 让测试 Agent 完整读取新的 `SKILL.md`。
2. 对每个 fixture 发起一次“转成知识卡片”的请求；JSON、文件导出、只解释第三方库等模式按需额外测试。
3. 对照下表检查不变量；不要求逐字匹配，检查结构和行为。

## 不变量

| Fixture | 目的 | 必须满足 |
| --- | --- | --- |
| `01_alias_libraries.py` | 别名导入 → 安装包名 | 5 张库卡片：PIL→Pillow、yaml→PyYAML、bs4→beautifulsoup4、sklearn→scikit-learn、cv2→opencv-python；不把导入名当安装名 |
| `02_duplicate_imports.py` | 同一库多次导入 | numpy、PyQt6、colormath 各 1 张库卡片；不能因多个 import 重复出卡 |
| `03_prose_mentions.md` | 正文提到库、无 import | pandas、requests、matplotlib 各 1 张库卡片；不编造 API 细节 |
| `04_local_modules.py` | 本地模块判定 | 仅 `os` 一张标准库卡片；`.utils`、`..common.config`、`window_capture`、`region_selector`、`gui_monitor` 不出库卡片，可在开头说明为本地模块 |
| `05_secrets.py` | 敏感信息脱敏 | 输出中不出现 `sk-fake-...`、`ghp_FAKE...`、`SuperSecret123!`、`postgresql://...`、`FAKEKEYMATERIAL...`；只给脱敏说明或跳过 |
| `06_side_effects.py` | 副作用示例 | 库卡片覆盖 os、tkinter、pydirectinput、requests；涉及网络/GUI/键鼠/写删文件的示例标注未执行，不编造输出，不写具体状态码或输出值 |
| `07_dedupe_padding.md` | 去重与不凑数 | 最多 3 张卡片；重复的“列表可变/元组不可变”合并；不按句子凑数 |
| `08_non_python.md` | 非 Python 内容 | 0 张知识卡片，说明材料与 Python 无关并请用户补充材料 |

## JSON / 导出测试

- 对 `01_alias_libraries.py` 要求“JSON 输出”：输出必须能被 `json.loads` 解析，符合 `schema/cards.schema.json`，卡片集合与 Markdown 输出一致；`source` 不含本机绝对路径。
- 要求“保存为 JSON 文件”时，文件内容为原始 JSON，不带 Markdown 围栏；路径应被报告。
- 库卡片必须带 `library.name`、`library.package`、`library.kind`；知识点卡片不得带 `library` 字段。

## CI

`.github/workflows/skill-validate.yml` 会：

1. 运行 `tests/tools/quick_validate.py Skills/python-study-assistant-v0-2`；
2. 检查 fixture 是否齐全、JSON Schema 是否合法；
3. 检查 `SKILL.md` 是否包含结构化输出、库映射、脱敏、副作用等关键章节。

行为验证（模型实际出卡）不在 CI 中执行，由人工/独立 Agent 前向测试完成。
