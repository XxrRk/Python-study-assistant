# 发布工具

本目录存放项目级发布工具，不属于 Skill 运行时依赖。

## release_check.py

只读发布预检：

```bash
python tools/release_check.py --version 0.8.0
```

可选参数：

- `--tag v0.8.0`：指定 Tag；默认 `v<version>`。
- `--title "v0.8.0 - ..."`：Release 标题。
- `--skill Skills/python-study-assistant-v0-8`：Skill 目录；默认按版本推断。
- `--notes-file release-notes.md`：写出发布说明；**只有此参数会写文件**。
- `--check-remote`：额外检查 GitHub 上是否已有 Tag/Release。
- `--skip-git-status`：仅用于本地试跑，跳过工作区干净检查。

检查内容：

- 版本号格式；
- Skill `metadata.version`；
- `agents/openai.yaml` 版本标记；
- README、CHANGELOG、RELEASE_CHECKLIST 版本一致；
- 工作区干净（默认）；
- 本地 Tag 不存在；
- 从 CHANGELOG 提取当前版本发布说明。

默认只打印计划和说明，不执行 Git 写操作；发布仍由人工或需要审批的 GitHub Actions 完成。

## release.yml

`.github/workflows/release.yml` 由 `workflow_dispatch` 触发，配置 `environment: release`，应按仓库设置要求人工审批（需要在仓库 Settings → Environments 中配置 required reviewers）。

流程：

1. 校验 v0.8 Skill 与版本一致性；
2. 运行 `release_check.py`；
3. 创建并推送 annotated Tag；
4. 创建 GitHub Release。

不会修改仓库可见性，也不会使用强制推送。
