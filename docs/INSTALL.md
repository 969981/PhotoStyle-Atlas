# 安装和使用

## 直接复制 Skill 实体目录

先克隆 PhotoStyle-Atlas，再把需要的完整目录复制进 Agent Skills 搜索路径。不要只复制 SKILL.md；目录中的 references、scripts、assets 也可能是必需的。

Windows PowerShell (Codex Desktop):
    git clone https://github.com/969981/PhotoStyle-Atlas.git
    New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
    Copy-Item -Recurse -Force ".\PhotoStyle-Atlas\skills\watercolor-travel-card" "$HOME\.codex\skills\"

macOS / Linux (Claude Code):
    git clone https://github.com/969981/PhotoStyle-Atlas.git
    mkdir -p ~/.claude/skills
    cp -R PhotoStyle-Atlas/skills/watercolor-travel-card ~/.claude/skills/

不同版本的 Codex CLI / Desktop 可能采用 .agents/skills 或 .codex/skills，按客户端当前实际说明调整目录。

## 如何选风格

打开 README.md 或 docs/STYLES.md，通过风格缩略图、中文名称和标签找到目标 Skill，再按目标客户端指令调用。例如：

    Use $watercolor-travel-card to transform the attached photo.

对于 image-style-transfer，可以先参考 docs/STYLES.md 中的 80 个预设名称，再调用单一 Skill 并指定编号。

## 使用限制

- 本仓库只是技能文件，不内置图片生成模型、API Key 或免费额度。
- 少数专业摄影后期 Skill 依赖 Lightroom Computer Use、Photoshop、PhotoCraft 或本地脚本，需要额外环境。
- 艺术化重绘可能改动真实细节；请保留原图并核对结果。
- Wibi Style 保留原许可和署名要求，其视觉技能为个人非商业使用条款；用于商业前自行确认授权。
