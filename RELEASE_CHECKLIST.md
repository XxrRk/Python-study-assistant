# Release Checklist

当前版本：`0.3.0`（已发布）
目标 Skill：`Skills/python-study-assistant-v0-3`

## 发布前

1. 确认版本号：`0.3.0`，且 `CHANGELOG.md` 已更新。
2. 运行官方校验：

   ```bash
   python tests/tools/quick_validate.py Skills/python-study-assistant-v0-3
   python tests/tools/quick_validate.py Skills/python-study-assistant-v0-2
   ```

3. 用 `tests/fixtures/` 与 `tests/fixtures/v0.3/` 做前向测试，逐项核对 `tests/README.md` 的不变量。
4. 用 `tests/schema/deck.schema.json` 校验 `tests/fixtures/v0.3/deck-existing.json`；确认 `deck-invalid.json` 会被拒绝。
5. 对 `merge-material.md` 合并到 `deck-existing.json`：已有 `card_id` 不变，只新增 `Path.glob` 卡片，摘要数量正确。
6. 对 `notebook_demo.ipynb` 确认忽略 outputs/execution_count、`source_ref` 含 cell 序号；对 `article_noise.html` 确认没有导航/广告/脚本噪声。
7. 对 `tests/fixtures/v0.3/batch/` 做目录批量处理，确认结果与逐文件处理一致、跨文件重复知识点已合并。
8. 从 Deck 导出 JSONL、CSV、Anki TSV，确认字段映射正确、重复导出 ID 稳定。
9. 检查测试夹具安全策略：不包含 `ghp_`、`sk-`、可解析私钥格式、真实邮箱或本机路径。
10. 确认 `README.md`、`CHANGELOG.md`、`SKILL.md`、`agents/openai.yaml` 的 v0.3.0 版本标记一致。
11. 确认 `SKILL.md`、`references/` 与 `agents/openai.yaml` 没有 TODO 或未完成的占位符。

## 发布

1. 提交本版本改动，确认工作区干净，并将 README/CHANGELOG/RELEASE_CHECKLIST 更新为已发布状态。
2. 创建注解标签：`git tag -a v0.3.0 -m "v0.3.0 - Deck merge, notebook/HTML input, exports"`。
3. 推送 `main` 与标签 `v0.3.0`。
4. 使用 `gh release create v0.3.0 --title "v0.3.0 - Deck merge, notebook/HTML input, exports" --notes-file <发布说明>` 创建 Release。
5. Release 说明至少包含：Deck/增量合并、输入扩展、复习导出、当前功能、安装方式、验证结果。

## 发布后

1. 打开 Release 页面，确认非 Draft、非 Pre-release。
2. 确认 `v0.3.0` 标签指向预期提交。
3. 在 README 或 CHANGELOG 中记录发布链接。
4. 归档下个版本的改进方向。

## 版本约定

- `0.x`：规则仍可能调整；修改 Deck/导出契约时提升次版本号。
- 修复不改变输出契约的问题提升补丁版本号。
- 每次发布必须更新 `CHANGELOG.md` 与本文档中的“当前版本”。
