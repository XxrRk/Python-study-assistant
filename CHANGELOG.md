# Changelog

本项目使用语义化版本。发布日期均为北京时间。

## [0.5.0] - 2026-11-16

### Added

- 质量用例：`tests/quality/cases.schema.json` 与 `cases.json`，为 v0.2/v0.3/v0.4 fixture 定义卡片数量、必需库、禁止文本和必需字段。
- 发布预检：`tools/release_check.py` 检查版本一致性、工作区、Tag 冲突，并从 CHANGELOG 生成发布说明草稿；默认只读。
- 发布工作流：`.github/workflows/release.yml`，`workflow_dispatch` + `environment: release` 人工审批，校验后创建 annotated Tag 和 Release。
- 库映射机读化：`references/library-map.yaml`，保留 `library-map.md` 作为人工说明。
- v0.5 测试/CI 覆盖质量用例、发布工具、库映射和版本一致性。

### Changed

- v0.5 沿用 v0.4 的 Deck Schema `0.4.0`，不改变四字段卡片和导出字段映射。
- 更新 README、CHANGELOG、RELEASE_CHECKLIST、tests README 和 CI 到 v0.5.0。

## [0.4.0] - 2026-11-16

### Added

- Deck 操作台：写回前 diff、dry-run/预览、确认写入；筛选导出（tag/type/library/source/keyword/new/include_archived）。
- 跨 Deck 合并：目标 Deck 已有 ID 不变，来源卡片分配目标新 ID，来源 ID 按 kind+ref 复用或重映射。
- Deck Schema 0.4.0：可选 `fingerprint`、`archived`、`origin_deck_id`；支持 v0.3.0 Deck 迁移并保留 ID。
- 归档与拆分：归档不删除、不重用 ID；按筛选拆分新 Deck。
- 质量基线与回归：新增质量评分表、回归不变量和前向测试方法。
- 安全预扫描：处理前扫描凭据与个人信息，Deck/导出写回前复查；新增 PII/凭据测试夹具。
- 新增 v0.4 测试材料、Deck 0.4 Schema 和 CI 校验。

### Changed

- README、CHANGELOG、RELEASE_CHECKLIST 同步 v0.4.0 开发状态。
- 导出保持 v0.3 字段映射，新增筛选、只导出新增和归档排除规则。

## [0.3.0] - 2026-11-15

### Added

- Deck 卡片库：`schema_version`、`deck_id`、`sources`、`cards`，卡片带稳定 `card_id`、`created_at`、`source_id`、可选 tags。
- Deck 增量合并：按包匹配库卡片、按规范化标题匹配知识点；同材料重复合并不新增重复卡；输出新增/合并/跳过摘要。
- 输入扩展：`.ipynb`（读取 markdown/code cell，忽略 outputs/execution_count）、`.html`（提取正文/标题/代码块并过滤导航广告脚本）、目录递归批量处理。
- 复习导出：JSONL、CSV、Anki 兼容 TSV；保留卡片 ID、来源和 tags；`references/exports.md` 固定字段映射。
- 新增 `deck.schema.json`、Deck/输入/导出测试材料和不变量。
- 库映射维护：扩充常见别名到独立参考文档，明确标准库判断、废弃包名和未知导入处理（不编造安装名）。
- CI 增加 v0.2/v0.3 结构校验、Deck Schema、版本标记一致性和测试夹具 secret-scanning 策略。

### Changed

- 测试夹具中的伪造凭据改为明显的 `EXAMPLE_*` 占位值，避免公开仓库 secret scanning 误报。
- README、CHANGELOG、RELEASE_CHECKLIST 同步 v0.3.0 开发状态。

## [0.2.0] - 2026-11-14

### Added

- 结构化输出：定义卡片 JSON Schema，支持 JSON 输出以及 Markdown/JSON 文件导出；Markdown 与 JSON 的卡片集合、顺序、内容保持一致。
- 库识别增强：常见“导入名 → 安装包名”映射（如 PIL→Pillow、yaml→PyYAML、bs4→beautifulsoup4、sklearn→scikit-learn、cv2→opencv-python）；支持从正文提到的库名出卡；明确本地模块判定；支持“只解释第三方库”“库卡片精简”等配置。
- 安全策略：材料中的密码、Token、API Key、私钥、凭据连接串一律脱敏，不进入卡片；联网、GUI、真实键鼠、写删文件等副作用示例不执行并标注；未安装依赖的示例标注为推断。
- 可选来源引用：支持 `文件名:行号范围` 或原文短引用。
- 工程化：新增 `tests/` 测试材料与不变量、JSON Schema、GitHub Actions 校验工作流、发布检查清单。

### Changed

- 库卡片明确区分标准库（`stdlib`）与第三方库（`third-party`），`package` 字段给出安装名。
- 本地模块（相对导入、同目录模块、项目内模块）不单独出库卡片。
- 输出版式继续保留四个展示字段；来源引用作为可选引用行，不作为额外字段。

## [0.1.0] - 2026-11-14

### Added

- 首个公开版本：Python 学习材料转四字段知识卡片。
- 一卡一知识点、去重、信息不足不凑数、只保留 Python 知识。
- 每个库一张卡片（标准库、第三方库、框架），按包去重。
- 支持粘贴文本与本地 `.md` / `.txt` / `.py` 文件。
