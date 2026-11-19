# 测试材料与不变量

本目录用于验证：

- `Skills/python-study-assistant-v0-2`（v0.2.0，已发布）
- `Skills/python-study-assistant-v0-3`（v0.3.0，已发布）
- `Skills/python-study-assistant-v0-4`（v0.4.0，已发布）
- `Skills/python-study-assistant-v0-5`（v0.5.0，已发布）
- `Skills/python-study-assistant-v0-6`（v0.6.0，已发布）
- `Skills/python-study-assistant-v0-7`（v0.7.0，已发布）
- `Skills/python-study-assistant-v0-8`（v0.8.0，已发布）
- `Skills/python-study-assistant-v0-9`（v0.9.0，本地开发）
- 目录布局：`fixtures/` 输入材料、`fixtures/v0.3/`、`fixtures/v0.4/`、`fixtures/v0.6/`、`fixtures/v0.7/`、`fixtures/v0.8/` 与 `fixtures/v0.9/` 新功能材料、`quality/` 质量用例、`schema/` Schema、`tools/` 官方校验脚本；项目级发布工具在根目录 `tools/`。

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

## v0.5.0 质量与发布

| 资产 | 目的 | 必须满足 |
| --- | --- | --- |
| `tests/quality/cases.schema.json` | 质量用例结构 | 通过 JSON Schema 校验 |
| `tests/quality/cases.json` | 机读质量基线 | 用例 ID 唯一；fixture 存在；min_cards ≤ max_cards |
| `tools/release_check.py` | 发布预检 | 默认只读；版本一致；Tag 不存在；生成说明草稿 |
| `.github/workflows/release.yml` | 发布自动化 | workflow_dispatch；environment: release；只在人工审批后创建 Tag/Release |
| `Skills/python-study-assistant-v0-5/references/library-map.yaml` | 库映射机读化 | 必填字段完整；import_name 唯一；覆盖 16 个别名 |

v0.5 不变量：

- v0.5 沿用 Deck Schema `0.4.0`，不产生新迁移；
- 质量用例只校验结构/路径/范围，不在 CI 调用 LLM；
- 发布预检默认不写文件、不执行 Git 写操作；
- 发布 workflow 不修改仓库可见性，不使用 force push；
- 库映射机读文件与 Markdown 说明保持同步。

## v0.6.0 输入扩展

| Fixture | 目的 | 必须满足 |
| --- | --- | --- |
| `v0.6/article.rst` | RST 输入 | 标题/正文/code-block 能出卡；pathlib 库卡正确 |
| `v0.6/article.docx` | DOCX 输入 | 段落/代码段落能提取；忽略页眉页脚；pathlib 库卡正确 |
| `v0.6/large_material.md` | 长材料覆盖 | 按章节输出覆盖报告；广告章节不进入卡片 |
| `v0.6/batch/` | 目录扩展 | `.rst`/`.docx`/`.md` 递归处理并去重 |

v0.6 不变量：

- RST/DOCX 在 Deck 中按 `kind=markdown` 记录来源，`ref` 保留原扩展名；
- DOCX 不执行宏，不读取页眉页脚/批注/修订；
- 长材料不能只读开头；覆盖报告必须列出读取/跳过章节与原因；
- 不能因为分块而为同一库重复出卡；
- v0.6 仍沿用 Deck Schema `0.4.0`。

## v0.7.0 多语言与导出 profile

| Fixture | 目的 | 必须满足 |
| --- | --- | --- |
| `v0.7/english_material.md` | 英文输出 | 标签为英文；pathlib 库卡正确；代码/包名未翻译 |
| `v0.7/anki-profile.yaml` | Anki profile | Front/Back 字段顺序、附加 tags、include_archived 生效；保留 card_id/source_id |

v0.7 不变量：

- 输出语言一致；不混用中英标签；代码/API 不翻译；
- 双语输出卡片数量和 ID 不变；
- Anki profile 不改变 3 列 TSV 结构，card_id/source_id 缺失时自动补；
- 同一 Deck + profile 重复导出稳定；
- v0.7 仍沿用 Deck Schema `0.4.0`。

## v0.8.0 Markdown 复习库

| Fixture | 目的 | 必须满足 |
| --- | --- | --- |
| `v0.8/review-profile.yaml` | Markdown vault profile | format=markdown；index/frontmatter 开启；split_by=none |
| v0.4 Deck + v0.8 profile | Markdown 导出 | 生成 `cards.md`、`index.md`；锚点/`id::`/index 链接稳定 |

v0.8 不变量：

- Markdown 复习库使用 `card_id` 锚点和 `index.md` 链接；
- frontmatter 含 `deck_id`、`schema_version`、`exported_at`、卡片数；
- 同一 Deck + profile 重复导出时 ID/锚点/文件名稳定；
- 目标目录已有同名文件时先给覆盖计划并等待确认；
- v0.8 仍沿用 Deck Schema `0.4.0`。

## v0.9.0 Deck 集合

| Fixture | 目的 | 必须满足 |
| --- | --- | --- |
| `v0.9/collection.json` | Deck 集合 | collection Schema 通过；两个 Deck 路径/deck_id 正确 |
| v0.9 collection + 跨库检索 | 跨库检索 | 结果带 deck_id/path/card_id；不自动合并同名卡片 |

v0.9 不变量：

- 集合是只读清单，不复制、不修改 Deck；
- 路径必须相对且不越界；`deck_id` 必须与 Deck 一致；
- 跨库同名卡片只报告重复，不静默合并；
- 集合 Markdown 导出按 Deck 分文件，顶层 index 链接；
- v0.9 仍沿用 Deck Schema `0.4.0`。

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

1. 分别运行 `tests/tools/quick_validate.py` 检查 v0.2、v0.3、v0.4、v0.5、v0.6、v0.7、v0.8、v0.9 Skill；
2. 校验 `cards.schema.json`、`deck.schema.json`、`deck-0.4.schema.json`、`collection.schema.json`、`quality/cases.schema.json` 和示例 Deck/集合；
3. 检查 v0.2/v0.3/v0.4/v0.6/v0.7/v0.8/v0.9 fixture、质量用例 fixture 和路径是否齐全；
4. 校验库映射 YAML、发布预检脚本和发布 workflow；
5. 扫描 tests/fixtures，禁止真实 Token 前缀/私钥格式；
6. 检查 README、CHANGELOG、SKILL.md、agents/openai.yaml 的 v0.9.0 版本标记一致；
7. 检查 `SKILL.md` 是否包含 Deck、集合、diff/dry-run、跨 Deck、质量、安全、长材料、语言、导出 profile、Markdown 复习库等关键章节。

行为验证（模型实际出卡、合并、导出）不在 CI 中执行，由人工/独立 Agent 按上表前向测试完成。
