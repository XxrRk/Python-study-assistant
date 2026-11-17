# Release Checklist

当前版本：`0.8.0`（已发布）
目标 Skill：`Skills/python-study-assistant-v0-8`

## 发布前

1. 确认版本号：`0.8.0`，且 `CHANGELOG.md` 已更新。
2. 运行官方校验：

   ```bash
   python tests/tools/quick_validate.py Skills/python-study-assistant-v0-8
   python tests/tools/quick_validate.py Skills/python-study-assistant-v0-7
   ```

3. 用 `tests/fixtures/v0.8/review-profile.yaml` 从现有 Deck 导出 Markdown 复习库，确认 `cards.md`、`index.md`、frontmatter、锚点、`id::`、来源和 tags。
4. 回归 v0.7 英文输出、Anki profile，以及 v0.6 RST/DOCX/长材料输入。
5. 运行 `python tools/release_check.py --version 0.8.0`。
6. 确认发布 workflow 的 `release` environment 需要人工审批。
7. 校验质量用例（含 v0.8 Markdown 复习库 case）、库映射 YAML 和安全扫描。
8. 确认 README、CHANGELOG、SKILL.md、agents/openai.yaml 的 v0.8.0 版本标记一致。
9. 确认 `SKILL.md`、`references/`、`tools/` 和 workflow 没有 TODO 或占位符。

## 发布

1. 提交本版本改动，确认工作区干净，并将 README/CHANGELOG/RELEASE_CHECKLIST 更新为已发布状态。
2. 通过 GitHub Actions 的 `Release Python Study Assistant` 工作流发布：
   - `version=0.8.0`
   - `tag=v0.8.0`
   - Release 标题：`v0.8.0 - Markdown review vaults`
   - 在 `release` environment 中人工批准。
3. 工作流会校验 Skill/版本 → 预检 → 创建 annotated Tag → 推送 Tag → 创建 Release。
4. Release 说明至少包含：Markdown 复习库、当前功能、安装方式、验证结果。

## 发布后

1. 确认 Release 非 Draft、非 Pre-release。
2. 确认 `v0.8.0` 标签指向预期提交。
3. 在 README 或 CHANGELOG 中记录发布链接。
4. 归档下个版本的改进方向。

## 版本约定

- `0.x`：规则仍可能调整；修改 Deck/导出契约时提升次版本号。
- 修复不改变输出契约的问题提升补丁版本号。
- 每次发布必须更新 `CHANGELOG.md` 与本文档中的“当前版本”。
