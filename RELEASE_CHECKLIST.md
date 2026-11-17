# Release Checklist

当前版本：`0.7.0`（已发布）
目标 Skill：`Skills/python-study-assistant-v0-7`

## 发布前

1. 确认版本号：`0.7.0`，且 `CHANGELOG.md` 已更新。
2. 运行官方校验：

   ```bash
   python tests/tools/quick_validate.py Skills/python-study-assistant-v0-7
   python tests/tools/quick_validate.py Skills/python-study-assistant-v0-6
   ```

3. 用 `tests/fixtures/v0.7/english_material.md` 做英文输出前向测试，确认标签为英文、代码/包名未翻译。
4. 用 `tests/fixtures/v0.7/anki-profile.yaml` 从 Deck 导出 Anki TSV，确认 Front/Back/tags 符合 profile，且包含 card_id/source_id。
5. 回归 RST/DOCX/长材料输入和 v0.4 Deck 操作；确认 v0.7 仍沿用 Deck Schema `0.4.0`。
6. 运行 `python tools/release_check.py --version 0.7.0`。
7. 确认发布 workflow 的 `release` environment 仍需要人工审批。
8. 校验质量用例（含英文输出 case）、库映射 YAML 和安全扫描。
9. 确认 README、CHANGELOG、SKILL.md、agents/openai.yaml 的 v0.7.0 版本标记一致。
10. 确认 `SKILL.md`、`references/`、`tools/` 和 workflow 没有 TODO 或占位符。

## 发布

1. 提交本版本改动，确认工作区干净，并将 README/CHANGELOG/RELEASE_CHECKLIST 更新为已发布状态。
2. 通过 GitHub Actions 的 `Release Python Study Assistant` 工作流发布：
   - `version=0.7.0`
   - `tag=v0.7.0`
   - Release 标题：`v0.7.0 - Multilingual output, Anki export profiles`
   - 在 `release` environment 中人工批准。
3. 工作流会校验 Skill/版本 → 预检 → 创建 annotated Tag → 推送 Tag → 创建 Release。
4. Release 说明至少包含：输出语言、Anki profile、当前功能、安装方式、验证结果。

## 发布后

1. 确认 Release 非 Draft、非 Pre-release。
2. 确认 `v0.7.0` 标签指向预期提交。
3. 在 README 或 CHANGELOG 中记录发布链接。
4. 归档下个版本的改进方向。

## 版本约定

- `0.x`：规则仍可能调整；修改 Deck/导出契约时提升次版本号。
- 修复不改变输出契约的问题提升补丁版本号。
- 每次发布必须更新 `CHANGELOG.md` 与本文档中的“当前版本”。
