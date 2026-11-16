# Release Checklist

当前版本：`0.5.0`（已发布）
目标 Skill：`Skills/python-study-assistant-v0-5`

## 发布前

1. 确认版本号：`0.5.0`，且 `CHANGELOG.md` 已更新。
2. 运行官方校验：

   ```bash
   python tests/tools/quick_validate.py Skills/python-study-assistant-v0-5
   python tests/tools/quick_validate.py Skills/python-study-assistant-v0-4
   ```

3. 运行质量用例静态校验与人工/独立 Agent 前向测试，核对 `tests/quality/README.md`。
4. 运行 `python tools/release_check.py --version 0.5.0`，确认工作区、版本、Tag 和发布说明检查通过。
5. 确认 `.github/workflows/release.yml` 已配置 `environment: release`，发布需要人工审批。
6. 校验 `references/library-map.yaml`：字段完整、import_name 唯一、覆盖 16 个 v0.3 别名。
7. 用 `tests/fixtures/`、`tests/fixtures/v0.3/`、`tests/fixtures/v0.4/` 做回归；确认 v0.5 沿用 Deck 0.4 后没有破坏。
8. 对 `pii_and_secrets.md` 和 `05_secrets.py` 做安全复检：卡片/Deck/导出中不出现真实凭据或个人信息。
9. 确认 README、CHANGELOG、SKILL.md、agents/openai.yaml 的 v0.5.0 版本标记一致。
10. 确认 `SKILL.md`、`references/`、`tools/` 和 workflow 没有 TODO 或占位符。

## 发布

1. 提交本版本改动，确认工作区干净，并将 README/CHANGELOG/RELEASE_CHECKLIST 更新为已发布状态。
2. 优先通过 GitHub Actions 的 `Release Python Study Assistant` 工作流发布：
   - `version=0.5.0`
   - `tag=v0.5.0`
   - 填写 Release 标题
   - 在 `release` environment 中人工批准
3. 工作流会：校验 Skill/版本 → 预检 → 创建 annotated Tag → 推送 Tag → 创建 Release。
4. 若手动发布，使用标题 `v0.5.0 - Quality cases, release automation, machine-readable library map`，并确保 Tag 为 annotated。
5. Release 说明至少包含：质量用例、发布预检、发布 workflow、库映射机读化、当前功能、安装方式、验证结果。

## 发布后

1. 打开 Release 页面，确认非 Draft、非 Pre-release。
2. 确认 `v0.5.0` 标签指向预期提交。
3. 在 README 或 CHANGELOG 中记录发布链接。
4. 归档下个版本的改进方向。

## 版本约定

- `0.x`：规则仍可能调整；修改 Deck/导出契约时提升次版本号。
- 修复不改变输出契约的问题提升补丁版本号。
- 每次发布必须更新 `CHANGELOG.md` 与本文档中的“当前版本”。
