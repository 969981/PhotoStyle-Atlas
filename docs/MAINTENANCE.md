# 维护与上游同步

## 同步策略

- sources.yaml 声明 GitHub 仓库、ref、需要物理复制的目录和目标 Skill。
- tools/sync.py 将上游文件真正复制到 skills/，并保存 LICENSES/、config/upstream-lock.json、catalog/skills.json、catalog/styles.json。
- 所有原始 Skill 的 SKILL.md、references、scripts、assets、NOTICE 和 LICENSE 按所选来源范围完整复制，不使用 Git submodule、Git subtree、符号链接。
- 定时任务先提交 Pull Request，人工审核后合并。首轮初始化的 push 工作流会直接填充空仓库。
- config/upstream-lock.json 记录上游完整 Commit SHA 和各镜像文件的 SHA-256，避免覆盖手工编辑。不要直接修改 skills/；中文说明请放 catalog/overrides.yaml 或 docs/。
- 上游删除文件时，只删除锁文件记录为自身管理过的文件，不删除非托管的本地文件。

## 本地运行

1. 安装 Python 3.12+ 和依赖：python -m pip install -r requirements.txt
2. 执行：python tools/sync.py
3. 执行：python tools/validate.py
4. 执行：python tools/generate_docs.py
5. 检查 Git diff，并提交 PR。

同步器会下载来自外部 GitHub 的文件；下载来的脚本不会在同步流程中直接执行。

## 权限与素材

- 许可证和署名以原作者文件为准，见 LICENSES/ 与各 skill 内的 NOTICE/LICENSE。
- Wibi Style 的原始提示词与视觉方案受个人非商业许可约束；用户表示已获导入许可，但本仓库不能代替原作者发放商业授权。
- 不要将部分第三方参考图片重新包装为独立图库或商业素材包。
- 任何含可执行脚本、post-install hook、安装指令或网络请求的上游更新，应先安全审查，再合并自动 PR。

## 常见问题

- 定时更新不一定准点，GitHub Actions 的 schedule 可能出现延迟。
- 默认同步 main 的最新提交；如需锁住稳定版本，把 ref 换成固定 tag。
- 若原始 Skill 被作者移动或删除，校验会报错，需修改 config/sources.yaml 或停用该源。
- 若检测到托管文件被手工编辑而与锁文件 SHA 不同，同步拒绝覆盖，需将修改迁移到自定义文档/补丁再重试。
