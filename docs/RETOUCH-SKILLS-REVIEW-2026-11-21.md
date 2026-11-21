# 2026-11-21 · 人像摄影后期 Skills 核对与整合

公开仓库并不等于拥有复制和二次分发权；仅符合授权要求的 Skill 进入上游镜像 Manifest。集成结构校验不代表修图效果经过实际测试。

| 项目 | 事实与特点 | 处理 | 依赖 |
| --- | --- | --- | --- |
| [robyboy888/photo-retouch-pro](https://github.com/robyboy888/photo-retouch-pro) | MIT；标准 SKILL.md；10 种商业精修模式 | 完整镜像 | 仍需实际编辑后端 |
| [hotcoffeeshake/portrait-retouch-skills-docs](https://github.com/hotcoffeeshake/portrait-retouch-skills-docs) | 人像诊断及漫展精修两 Skill；未找到明确 LICENSE | 两条外部索引，不复制 | 图像编辑工具；部分接口尚未实现 |
| [eachlabs/skills/image-relighting](https://github.com/eachlabs/skills/tree/main/skills/image-relighting) | 三点布光、逆光、环境匹配等 API 型 Skill；未找到明确 LICENSE | 外部索引 | EachLabs API Key、网络与潜在费用 |
| [CSlawyer1985/tuxiuxiu](https://github.com/CSlawyer1985/tuxiuxiu) | 非生成式活动批量调色、修肤和水印；未找到明确项目 LICENSE | 外部索引 | Python、Pillow/NumPy/OpenCV/MediaPipe 与模型 |
| [AInVFX/ainvfx-paintaplate](https://github.com/AInVFX/ainvfx-paintaplate) | Apache-2.0 ComfyUI 视频 VFX 节点，非 SKILL.md | 外部工具索引 | ComfyUI、上游推荐≥32GB 显存 |
| [moskoo/xxg-portrait-rebuild-light](https://github.com/moskoo/xxg-portrait-rebuild-light) | MIT，已有镜像 | 不重复收录 | 图像编辑后端 |
| [x-rush/photo-retouch](https://github.com/x-rush/photo-retouch) | 未找到许可证，之前已索引 | 继续只索引 | 图像编辑后端 |

新增本项目原创 [Atlas Portrait Suite](../skills/atlas-portrait-suite/SKILL.md) 将摄影保真、环境融合、补光与清透调色组织为分阶段 SOP；不复制无许可证项目文字。可在 [五种风格配方](../skills/atlas-portrait-suite/references/presets.md) 按需要选择模式。
