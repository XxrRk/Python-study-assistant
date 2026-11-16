# 测试材料与不变量

本目录用于验证：

- `Skills/python-study-assistant-v0-2`（v0.2.0，已发布）
- `Skills/python-study-assistant-v0-3`（v0.3.0，已发布）
- `Skills/python-study-assistant-v0-4`（v0.4.0，本地开发）
- 目录布局：`fixtures/` 输入材料、`fixtures/v0.3/` 与 `fixtures/v0.4/` 新功能材料、`schema/` Schema、`tools/` 官方校验脚本。

本目录不添加 Skill 运行脚本；行为验证由人工或独立 Agent 前向测试完成。

## 安全测试夹具策略

- 所有敏感信息测试值必须是明显的占位符（如 `EXAMPLE_API_KEY_VALUE`），不得使用真实凭据或可用的 Token 格式。
- 不写入 `ghp_`、`sk-` 等真实 Token 前缀，不写可解析的私钥块；避免公开仓库 secret scanning / push protection 误报。
- 不写入真实邮箱、手机号、身份证号、真实 IP、本机绝对路径；测试占位域名/号码（如 `example.invalid`、`000`）除外。
- CI 会扫描 `tests/fixtures/`，出现禁止模式即失败。

## v0.2 回归材料

| Fixture | 目的 | 必须满足 |
| --- | --- | --- |
| `01_alias_libraries.py` | 别名导入 → 安装包名 | PIL→Pillow、yaml→PyYAML、bs4→beautifulsoup4、sklearn→scikit-learn、cv2→opencv-python；不把导入名当安装名 |
| `02_duplicate_imports.py` | 同一库多次导入 | numpy、PyQt6、colormath 各 1 张库卡片 |
| `03_prose_mentions.md` | 正文提到库、无 import | pandas、requests、matplotlib 各 1 张库卡片 |
| `04_local_modules.py` | 本地模块判定 | 仅 `os` 一张标准库卡片；本地模块不出库卡片 |
| `05_secrets.py` | 敏感信息脱敏 | 输出中不出现 `EXAMPLE_*` 占位值；不生成含凭据的卡片 |
| `06_side_effects.py` | 副作用示例 | 联网/GUI/键鼠/写删文件示例标注未执行，不写具体输出 |
| `07_dedupe_padding.md` | 去重与不凑数 | 最多 3 张；重复表述合并 |
| `08_non_python.md` | 非 Python 内容 | 0 张卡片，说明原因 |

## v0.3.0 新材料

| Fixture | 目的 | 必须满足 |
| --- | --- | --- |
| `v0.3/notebook_demo.ipynb` | Notebook 输入 | 读取 markdown/code cell；忽略 outputs/execution_count；`source_ref` 含 `cell-` 序号；输出中不出现 `SHOULD_NOT_APPEAR` |
| `v0.3/article_noise.html` | HTML 输入 | 提取 pathlib 正文与代码块；不出现 `NOISE_*` 与广告/导航/页脚原文内容（可说明已过滤） |
| `v0.3/aliases_v03.py` | 扩展别名映射 | 16 个库的导入名与安装名全部正确；无重复库卡片 |
| `v0.3/unknown_imports.py` | 未知/本地导入 | 仅 `os` 出库卡片；本地模块不出卡；`internal_company_sdk` 列为“未确认导入”，不虚构安装名 |
| `v0.3/batch/` | 目录批量 | 递归收集 `.md/.py/.txt`；跨文件重复知识点合并；批量结果与逐文件一致 |
| `v0.3/deck-existing.json` | 合法 Deck | 通过 `deck.schema.json`；3 张卡、ID 连续、来源完整 |
| `v0.3/merge-material.md` | 增量合并 | 复用现有 `pathlib` 库卡和 `/`、`.parent` 知识点卡；只新增 `Path.glob` 卡片；已有 `card_id` 不变 |
| `v0.3/deck-invalid.json` | 损坏 Deck | 校验失败；不得覆盖原文件 |
| `v0.3/deck-existing.json` | 导出 | 可生成 JSONL/CSV/Anki TSV；字段映射固定；重复导出 ID 稳定 |

## v0.4.0 新材料

| Fixture | 目的 | 必须满足 |
| --- | --- | --- |
| `v0.4/deck-existing.json` | 合法 v0.4 Deck | 通过 `deck-0.4.schema.json`；3 张卡；含 fingerprint |
| `v0.4/deck-other.json` | 跨 Deck 来源 | 2 张卡；与目标 Deck 有重复 pathlib 库卡；来源 ID 需重映射 |
| `v0.4/deck-v03.json` | v0.3 迁移源 | 通过 v0.3 Schema；迁移后保留 deck_id/card_id/source_id |
| `v0.4/filter-deck.json` | 筛选与归档 | 4 张卡，其中 `c-000003` 为 archived；默认导出排除 |
| `v0.4/merge-material.md` | dry-run/diff/合并 | dry-run 不写文件；只新增 `Path.glob`；已有 ID 不变；diff 与结果一致 |
| `v0.4/pii_and_secrets.md` | 安全预扫描 | 全部为 `EXAMPLE_*` / `example.invalid` 占位值；不进入卡片/Deck/导出 |
| `v0.4/deck-invalid.json` | 损坏 v0.4 Deck | 校验失败；不得覆盖原文件 |

## v0.4 操作不变量

- dry-run / 预览：写入文件数为 0；diff 中的新增/合并/跳过与实际投影一致。
- 更新已有 Deck：目标 `card_id` 不变；来源 `source_id` 按 `kind+ref` 复用或重映射。
- 跨 Deck 合并：重复库/知识点为 0；目标已有 ID 不变；来源未匹配卡片分配新目标 ID。
- v0.3 迁移：`deck_id`、`card_id`、`source_id`、卡片内容保持不变；只改 `schema_version` 和可选字段。
- 筛选：tag/type/library/source/keyword 取交集；`new` 只使用明确 diff 基线；归档默认不导出。
- Schema：v0.4 Deck 通过 `deck-0.4.schema.json`；v0.3 Deck 仍可通过 `deck.schema.json` 读取。
- 质量与安全：按 `references/quality-eval.md` 评分；敏感值/个人信息不出现在任何产物中。

## Deck 不变量

- v0.3 Deck 的 `schema_version` 为 `0.3.0`；v0.4 Deck 为 `0.4.0`。
- `deck_id`、`sources`、`cards` 完整；`source_id`、`card_id` 唯一。
- 同一材料转换两次：卡片数量不增加，结果为跳过或合并。
- 合并两个来源后：库按 `library.package` 去重，知识点按规范化标题去重；已有 ID 不变。
- 摘要中的新增/合并/跳过数量与 Deck 实际变化一致。
- 损坏 Deck 或 JSON 无效时停止，不覆盖原文件。
- 导出携带 `schema_version`、`deck_id`、`card_id`、`source_id`、`source_ref`、tags；重复导出 ID 稳定。
- 导出路径不可写时只报告失败，不写 fallback 文件、不假装成功。

## 导出字段映射

- JSONL：一行一张卡；含 Deck/卡片/来源/标签字段。
- CSV 表头固定：
  `schema_version,deck_id,card_id,type,title,knowledge,example,question,library_name,library_package,library_kind,source_id,source_ref,tags,created_at`
- Anki TSV：Front = 标题 + 知识点；Back = 例子 + 自测问题 + 来源 + 卡片 ID；Tags 含 `pycard::<card_id>`、`source::<source_id>`。
- 字段内换行在 TSV 中用 `<br>`；CSV 按 RFC 4180 转义。

## CI

`.github/workflows/skill-validate.yml` 会：

1. 分别运行 `tests/tools/quick_validate.py` 检查 v0.2、v0.3、v0.4 Skill；
2. 校验 `cards.schema.json`、`deck.schema.json`、`deck-0.4.schema.json` 和示例 Deck；
3. 检查 v0.2/v0.3/v0.4 fixture 是否齐全；
4. 扫描 tests/fixtures，禁止真实 Token 前缀/私钥格式；
5. 检查 README、CHANGELOG、SKILL.md、agents/openai.yaml 的 v0.4.0 版本标记一致；
6. 检查 `SKILL.md` 是否包含 Deck、diff/dry-run、跨 Deck、质量、安全等关键章节。

行为验证（模型实际出卡、合并、导出）不在 CI 中执行，由人工/独立 Agent 按上表前向测试完成。
