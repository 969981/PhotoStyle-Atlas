---
name: atlas-portrait-suite
description: >-
  摄影后期 Agent Skill：真实人像保真精修、局部补光、物理重新布光、人物与环境融合、清透唯美糖水片。
  适用于日系清冷空气感、夏日逆光、窗边奶油、夜间直闪、风景环境人像。
license: MIT
metadata:
  version: 1.0.0
  origin: PhotoStyle-Atlas original
---

# Atlas Portrait Suite · 保真精修与清透人像

**仅是可移植的编辑方法论与操作契约。** 需要图像查看和实际编辑后端才能出图。未连接图像编辑工具时仅提供可执行修图方案，不得声称编辑成功。先阅读 [预设](references/presets.md)、[光学与融合](references/lighting-physics.md)、[身份质检](references/identity-and-qa.md)、[后端适配](references/backends.md)。

## Step 1 · 诊断并锁定

先查看原片分辨率、画幅、曝光、光源方位、色温、焦平面、透视、皮肤纹理、背景干扰和高光溢出。原图始终是身份权威；第二张照片若仅为光影参考，不得继承其五官。默认锁定五官与脸宽、年龄特征、痣疤、发际线、眼镜、眼神表情、人物姿态、服装、背景结构、照片比例。只有用户明确要求的维度可以 UNLOCK。目标为『糖水片』只释放光影、局部肤色影调、对比与色彩，不自动换脸、瘦身、美白或改场景。

记录：`base_image`、`reference_role`、`LOCK`、`UNLOCK`、`requested_edit`、`preset`、`output`。可参考：

```yaml
mode: sweet-portrait
preset: jp-airy
identity_authority: input-1
LOCK: [face_geometry, identity_marks, expression, pose, clothing, composition]
UNLOCK: [face_exposure, tone_curve, background_color, local_skin_tone]
light: {key: observed_daylight, fill: subtle_subject_bounce, rim: existing_only}
output: {preserve_original: true, edit_copy: true}
```

## Step 2 · 场景/背景（按需）

不换景时先用裁切、局部降饱和或真实景深处理杂乱环境，优先保留现场结构。用户明确要求换背景时才执行：几何透视与比例校正 → 分离边缘及发丝 → 统一景深/噪点 → 接触影与投射影 → 环境光包裹和色彩溢出。背景或机位变化应先完成，最后才精修皮肤与锐化。只有显式蒙版回贴原图区域才能承诺未编辑区域逐像素不变；纯生成式重绘不保证。

## Step 3 · 补光与物理重新布光

优先补充已有场景的可解释光线：先确定主光的方位、相对高度、面积、软硬、色温和阴影衰减，再定义环境天空/墙面/地面/辅助闪光灯的弱回填。允许多个真实光源，但每道明显投影都应有对应来源。

控制轴以概念解耦：`L` 光源方向与大小、`E` 高光/中调/阴影/黑点、`S` 肤色低频过渡、`P` 漫反射/高光、`T` 色温、`G` 曲线/HSL、`D` 相机镜头质感、`A` 环境、`Q` 质量与身份。这些不是统一 API 参数。

默认先用 Lightroom/Photoshop 蒙版及曲线做非生成式局部补光。只有原像素不足以完成目标、用户也允许重画时，才使用支持原图输入的 AI 编辑后端。直闪必须匹配鼻影、镜面与背景衰减；逆光不能只造亮发丝而人脸严重欠曝。

## Step 4 · 糖水片与皮肤

从 [五套配方](references/presets.md) 选择一个主风格：`jp-airy`、`summer-backlight`、`indoor-cream`、`night-direct-flash`、`environment-portrait`。不得把所有规则同时堆满。大面积柔光、较低但不死板的反差、柔和高光滚降、弱化无关杂色、轻提人物中间调；肤色保持真实不强行漂白。

皮肤分三层处理：① 低频均匀肤色/明暗但保留立体感；② 受光方向一致的温和反射，不能凭空涂高光；③ 随焦平面变化的低对比真实微纹理，睫毛/瞳孔/发丝保持清晰。不能靠加粗毛孔、暗灰脏纹、油污或全局锐化伪造真实性。

## Step 5 · 原图对照、回滚与交付

对照原片逐项查五官、脸宽、痣疤、眼镜、手指、衣物纹理、文字、建筑线条、发丝边界、接触影、眼神光、景深和色彩；检查发白光晕、假毛孔、皮肤斑驳和 HDR 过锐。若发生身份漂移或多轮画质劣化，从原图或最近合格版本重做，根图仅做身份/几何权威，不把光线参考当成人脸参考。连续两次相同失败时报告限制，不无限试错。

另存结果、不覆盖原片。可用时保留 PSD/XMP 分层母版并核实 JPEG/PNG 的尺寸与颜色空间。未安装后端或未运行修图时，只交付诊断、具体参数范围、蒙版策略和质检项，严禁虚构处理效果。私人人像不上传公开仓库；使用云端 API 前核对费用与隐私许可。

## 优先搭配

- [XXG 重新布光](../xxg-portrait-rebuild-light/SKILL.md)：复杂光场/清洁肤质。
- [AI Portrait Light](../portrait-light/SKILL.md)：光位设计与写实光线提示词。
- [GenAI Portrait](../genai-portrait/SKILL.md)：需要模型与身份核对的场景融合。
- [Roby 十种精修](../roby-photo-retouch-pro/SKILL.md)：去路人、扩图、服装与背景等明确变更模式。
