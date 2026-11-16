# Release Checklist

当前版本：`0.4.0`（已发布）
目标 Skill：`Skills/python-study-assistant-v0-4`

## 发布前

1. 确认版本号：`0.4.0`，且 `CHANGELOG.md` 已更新。
2. 运行官方校验：

   ```bash
   python tests/tools/quick_validate.py Skills/python-study-assistant-v0-4
   python tests/tools/quick_validate.py Skills/python-study-assistant-v0-3
   python tests/tools/quick_validate.py Skills/python-study-assistant-v0-2
   ```

3. 用 `tests/fixtures/`、`tests/fixtures/v0.3/`、`tests/fixtures/v0.4/` 做前向测试，逐项核对 `tests/README.md` 的不变量。
4. 用 `tests/schema/deck-0.4.schema.json` 校验 v0.4 Deck；确认 `deck-invalid.json` 被拒绝；确认 `deck-v03.json` 可通过 v0.3 Schema 并迁移到 v0.4。
5. 对 `merge-material.md` 做 dry-run，确认不写文件；再执行合并，确认 diff 与实际变化一致、已有 ID 不变。
6. 对 `deck-other.json` 执行跨 Deck 合并，确认重复库/知识点不重复、目标 ID 不变、来源 ID 重映射正确。
7. 对 `filter-deck.json` 测试 tag/type/library/source/keyword/new/include_archived；确认归档默认不导出。
8. 从 v0.4 Deck 导出 JSONL/CSV/Anki TSV，确认字段映射正确、重复导出 ID 稳定、写入失败不写 fallback。
9. 检查 `pii_and_secrets.md` 和 `05_secrets.py`：卡片、Deck、导出中不出现真实凭据或个人信息。
10. 运行 CI 安全扫描或人工安全预扫描；确认测试夹具只使用 `EXAMPLE_*` / `example.invalid` 占位值。
11. 按 `references/quality-eval.md` 做质量评分和前向测试；无 0 分项、总分 ≥ 9。
12. 确认 `README.md`、`CHANGELOG.md`、`SKILL.md`、`agents/openai.yaml` 的 v0.4.0 版本标记一致。
13. 确认 `SKILL.md`、`references/` 与 `agents/openai.yaml` 没有 TODO 或未完成占位符。

## 发布

1. 提交本版本改动，确认工作区干净，并将 README/CHANGELOG/RELEASE_CHECKLIST 更新为已发布状态。
2. 创建注解标签：`git tag -a v0.4.0 -m "v0.4.0 - Deck operations, schema migration, quality baseline"`。
3. 推送 `main` 与标签 `v0.4.0`。
4. 使用 `gh release create v0.4.0 --title "v0.4.0 - Deck operations, schema migration, quality baseline" --notes-file <发布说明>` 创建 Release。
5. Release 说明至少包含：Deck diff/dry-run、筛选导出、跨 Deck 合并、v0.3 迁移、质量基线、安全预扫描、当前功能、安装方式、验证结果。

## 发布后

1. 打开 Release 页面，确认非 Draft、非 Pre-release。
2. 确认 `v0.4.0` 标签指向预期提交。
3. 在 README 或 CHANGELOG 中记录发布链接。
4. 归档下个版本的改进方向。

## 版本约定

- `0.x`：规则仍可能调整；修改 Deck/导出契约时提升次版本号。
- 修复不改变输出契约的问题提升补丁版本号。
- 每次发布必须更新 `CHANGELOG.md` 与本文档中的“当前版本”。
