# Release Checklist

当前版本：`0.2.0`（已提交 main，尚未创建 GitHub Release）
目标 Skill：`Skills/python-study-assistant-v0-2`

## 发布前

1. 确认版本号：`0.2.0`，且 `CHANGELOG.md` 已更新。
2. 运行官方校验：

   ```bash
   python tests/tools/quick_validate.py Skills/python-study-assistant-v0-2
   ```

3. 用 `tests/fixtures/` 做前向测试，逐项核对 `tests/README.md` 的不变量。
4. 对 `01_alias_libraries.py` 额外测试 JSON 输出，确认能被 `json.loads` 解析且符合 `tests/schema/cards.schema.json`。
5. 对 `05_secrets.py` 做敏感信息检查，确认输出没有任何伪造密钥字面量。
6. 对 `06_side_effects.py` 确认没有实际执行联网/GUI/键鼠/写删文件示例，未执行示例没有写具体输出值、状态码或版本号。
7. 确认 `SKILL.md` 与 `agents/openai.yaml` 的描述一致，未包含 TODO 或占位符。
8. 确认没有把 `tests/` 中的伪造凭据当作真实凭据处理。

## 发布

1. 提交本版本改动，确认工作区干净。
2. 创建注解标签：`git tag -a v0.2.0 -m "v0.2.0 - Structured output, library mapping, security policy"`。
3. 推送 `main` 与标签 `v0.2.0`。
4. 使用 `gh release create v0.2.0 --title "v0.2.0 - Structured output and safer cards" --notes-file <发布说明>` 创建 Release。
5. Release 说明至少包含：当前功能、安装方式、验证结果、破坏性变更（如有）。

## 发布后

1. 打开 Release 页面，确认非 Draft、非 Pre-release。
2. 确认 `v0.2.0` 标签指向预期提交。
3. 在 README 或 CHANGELOG 中记录发布链接。
4. 归档下个版本的改进方向。

## 版本约定

- `0.x`：规则仍可能调整；修改输出契约时提升次版本号。
- 修复不改变输出契约的问题提升补丁版本号。
- 每次发布必须更新 `CHANGELOG.md` 与本文档中的“当前版本”。
