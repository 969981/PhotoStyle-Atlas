# 执行协议

> 本文件是 [SKILL.md](SKILL.md) 的详细展开。`SKILL.md` 负责路由（判断用哪个 key），
> 本文件负责执行（怎么定位原图、怎么拆解、怎么出图、怎么验收）。
>
> 风格描述只维护在 `references/style-recipes.md`（深度配方）与 `references/prompt-lexicon.md`（槽位短语），
> 本文件不含画风描述，避免第三处真源。

## 1. 定位原图

按以下顺序找，找到即用，不要问用户：

1. 本轮用户消息里附带的图片路径（`<attached_files>` / 拖入路径）
2. 用户消息里直接写的绝对路径
3. 本会话中用户最近一次提供的图片路径
4. 都找不到 → 才问一句原图在哪

## 2. 解析风格（槽位拆解）

一句话风格是**多个维度的组合**。把用户的话拆到下面这些槽位里，命中几个填几个，没提到的槽留空：

| 槽位 | 管什么 | 用户可能怎么说 |
|---|---|---|
| **媒介/渲染** | 主渲染体系 | 赛璐璐、厚涂、水彩、水墨、3D、像素、黑白 |
| **人设体系** | 人物比例与受众 | 萌系、少女漫、少年漫、剧画、半写实、Q版、三渲二、轻小说封面、Galgame |
| **线稿** | 轮廓处理 | 无描边、极细线、粗描边、铅笔线、墨线、彩线、网点线、机械硬线 |
| **上色** | 明暗塑造方式 | 平涂、双阴影、柔边、半厚涂、厚涂、水彩、网点、蜡笔 |
| **调色** | 色彩倾向 | 糖果色、复古限色、霓虹、哥特低明度、矿物颜料、印刷套色 |
| **光影** | 光线设计 | 逆光、硬光、高键柔光、霓虹混光、烛光月光、黄金时刻 |
| **时代/地域** | 年代与产业 | 昭和、90年代、京阿尼感、中国2D国漫、韩系条漫、美式卡通 |
| **题材美术** | 服装/道具/场景 | 校园、偶像、魔法少女、仙侠、赛博、机甲、废土、美食、治愈 |
| **氛围** | 情绪基调 | 治愈、梦幻、热血、压抑、神圣、诡异、浪漫、史诗 |
| **镜头** | 取景与用途 | 立绘、三视图、近景肖像、全身海报、低机位、广角、分镜、头像 |

**解析顺序**：

1. 先在 `SKILL.md` 的「口语别名表」里精确命中整体说法。
2. 没整体命中 → 逐槽拆解用户的话，每个维度单独匹配。
3. 单个槽位没命中 → 读 `references/style-registry.md` 按 11 大风格家族找最接近的 key。
4. 风格名是英文 key 或别名 → 直接用。
5. 只说「动漫风 / 二次元」→ 默认 `cel-tv-clean`，并在回复末尾提示可从 11 个家族里选。
6. 只给了题材没给画风（如「校园风」）→ 主渲染体系默认 `cel-tv-clean`，题材填 `theme-campus-youth`。
7. 用户提到具体作品/作者 → 提取视觉元素，映射成原创特征描述，**不复述该作品名，不声称复刻**。

**冲突规则**：主渲染体系（赛璐璐 / 厚涂 / 水彩 / 水墨 / 3D / 像素 / 黑白漫画）只能选一个。题材、氛围、年代、镜头类可以叠加在主风格上。用户同时给了两个冲突主风格 → 必须让用户选一个，不要自己混合。

**组合示例**：

- 「90年代手绘赛璐璐，雨夜霓虹街，低机位广角」
  → 渲染 `cel-90s-film` ＋ 题材 `cyber-rain-neon` ＋ 镜头「低机位仰视」（`prompt-lexicon.md` 的 LENS 槽短语 `low-angle looking up, imposing and heroic`）＋ 电影广角（MOTION 槽 `reframe to a wide cinematic composition`）
- 「国风仙侠女主，现代中国2D国漫风，细腻线稿，赛璐璐加半厚涂，清晨逆光，全身立绘」
  → 地域 `cn-2d-donghua` ＋ 题材 `xianxia-ethereal` ＋ 线稿细线 ＋ 上色 `hybrid cel base with painterly rendering` ＋ 光影 `strong backlight` ＋ 镜头 `fullbody-sheet`

## 3. 编译提示词

### 路径 A：命中有深度配方的 15 个 key

**必须调用渲染器**，不要手写：

```bash
python scripts/render_prompt.py --style <key 或中文别名> [选项]
```

| 参数 | 说明 |
|---|---|
| `--style` | 必填。风格 key 或中文别名 |
| `--aspect` | 目标画幅，如 `9:16`。不传则沿用原图比例 |
| `--intensity` | `轻度` / `中度` / `强度`，默认 `中度` |
| `--layer` | 叠加层，可重复：`minimal-bg`（极简背景）、`keep-light`（保留原光线）、`vertical-cover`（竖版封面构图） |
| `--note` | 追加一句用户补充要求，原样附加在配方之后、防劣化后缀之前 |
| `--image` | 原图路径，仅用于 JSON 调用包 |
| `--format` | `text`（默认）或 `json` |
| `--list` | 列出全部深度配方 key |

渲染器输出的 prompt = **保真前缀 + 配方原文 + 防劣化后缀**，直接交给图生图工具。
脚本不可运行时，从 `references/style-recipes.md` 整段照抄对应配方，自己补上前缀后缀。

### 路径 B：其余 key，按槽位组装

读 `references/prompt-lexicon.md` 取英文短语，按下面的模板组装成**英文** prompt。保留用户明确的中文专名、文字内容和颜色要求。

```text
Transform Image 1 into an original [STYLE NAME] anime illustration. Preserve the recognizable identity and facial features of every subject, the exact number of subjects, pose, expression, body proportions, hairstyle silhouette, clothing silhouette, key objects, camera angle, composition, crop, spatial layout, and the original image aspect ratio [OR REQUESTED ASPECT RATIO].

Visual direction: [ERA/REGION]. [CHARACTER BASE]. [LINEWORK]. [COLORING]. [PALETTE]. [LIGHTING]. [THEME]. [MOOD]. [MATERIAL AND TEXTURE]. [BACKGROUND TREATMENT]. [LENS]. [MOTION CUES].

Change only the visual rendering style unless the user explicitly requested content changes. Keep hands anatomically coherent, eyes aligned, facial features consistent, clean silhouettes, and readable object geometry. Preserve any existing text exactly when legible; otherwise omit new text.

**槽位填充纪律**：只填用户点名或风格 key 隐含的槽位，**不要用默认值填满所有槽**。空槽留白比堆砌无关修饰词出图更准。

Do not add extra people, duplicate limbs, alter identity, change ethnicity, change age category, replace important objects, add watermark, add logo, add signature, add random text, make plastic skin, blur the face, or introduce deformed hands.
```

非人物主体（宠物 / 商品 / 建筑 / 风景）时：把身份相关措辞换成物体保真措辞（`preserve the exact product shape, material, label text, and brand markings`），其余结构不变。

## 4. 出图参数

本技能需要一个**支持「图生图」（image-to-image）**的图像生成工具。下表参数名是通用参考名，如果你的工具参数名不同，按语义映射即可，不要因为名字对不上就放弃出图：

| 语义 | 参考参数名 | 取值 |
|---|---|---|
| 原图输入 | `image1` / `image` / `input_image` | 步骤 1 定位到的原图绝对路径 |
| 提示词 | `prompt` | 步骤 3 得到的英文 prompt |
| 画幅 | `size` / `aspect_ratio` | 见下方画幅映射 |
| 保真度 | `input_fidelity` / `strength` | 保真/轻度 → 高；标准/中度 → 中；强度/重构 → 低 |
| 质量 | `quality` | 默认 `high` |
| 输出目录 | `output_dir` | 见下方输出路径规则 |

若工具没有「保真度」参数，用提示词强度代偿：保真 → 在 prompt 开头加重 `Stay as close to Image 1 as possible`；强度 → 加重 `Fully reinterpret in this style`。

**输出路径规则**（不要写死任何本机绝对路径）：

1. 优先 `<当前工作区>/outputs/anime-restyle/<key>-<MMDDHHMM>`；
2. 拿不到工作区时，退回 `~/.anime-restyle/outputs/<key>-<MMDDHHMM>`；
3. 两者都不确定 → 直接问用户想存哪，不要自己猜一个盘符。

**画幅映射**（`size` 只支持三种）：

| 用户要求 | size |
|---|---|
| 1:1、头像 | `1024x1024` |
| 9:16、2:3、3:4、竖版封面 | `1024x1536` |
| 16:9、3:2、横版、动画截图 | `1536x1024` |
| 原比例 / 没说 | 跑一次 `scripts/probe_image.py <原图路径>`，横图→`1536x1024`，竖图→`1024x1536`，方图→`1024x1024` |

> 注意：图生图场景下画幅**必须**与原图比例一致，否则主体会被拉伸变形。
> 这与某些「文生图配方库」刻意不锁画幅的做法不同——那是为文生图保留画布自由度，本 skill 不适用。

**计费提示**：如果该平台的图像生成按次计费，每个会话第一次出图前用一句话说明单次大致消耗与张数，同一会话后续不再重复提示，直接出。

## 5. 交付

1. 出图后把成品文件呈现给用户（有文件呈现工具就调用，没有就直接报路径）。
2. 回复只写三样：已匹配的风格名（含 key）、一行「保留什么 / 改了什么」摘要、成品图。**不要**把整段英文 prompt 贴出来污染对话，除非用户问。
3. 在输出根目录追加一行到 `ledger.md`：`时间 | 原图文件名 | key | 强度/画幅 | 输出路径`。

## 6. 可选控制项

用户没提就按默认值走，不要主动追问。

| 字段 | 可填值 | 默认 |
|---|---|---|
| mode | 保真 / 标准 / 重构 | 保真 |
| frame | 原比例 / 1:1 / 3:4 / 2:3 / 9:16 / 16:9 | 原比例 |
| scene | 保留背景 / 简化背景 / 换场景描述 | 保留背景 |
| light | 保留光线 / 风格默认光线 / 自定义描述 | 风格默认光线 |
| intensity | 轻度 / 中度 / 强度 | 中度 |

### 强度对模板的影响

- **轻度**：把 `Transform` 改成 `Apply subtle [style] rendering`，保留原图光线、细节与背景信息。
- **中度**：用标准模板；风格覆盖线稿、上色、材质与调色，不动构图。
- **强度**：允许风格重绘背景与服装细节，但仍保留身份、人数、姿势、构图和关键物件。
- **重构**：只保留用户点名的不变项，把新场景/服装/镜头要求写进 `Visual direction` 段落后。

## 7. 迭代修订

用户看完图提修改意见时，**沿用同一张原图重出，不要在原图上叠加二次转换**（会累积失真）。

- 说「再柔和一点 / 线条再细一点 / 颜色再淡一点」→ 只改对应的那个 slot，其余 prompt 原样保留，`output_dir` 后加 `-v2`、`-v3`。
- 说「换个风格」→ 换 key 重来，其余不变。
- 说「给我几个风格对比」→ 同一原图、同一画幅，换 key 连续出 2-4 张，逐张呈现。
- 用户不满意且说不清哪不对 → 回退到 `保真 + 轻度`，再往上加。

**深度配方的修订纪律**：若某套深度配方实测就是出不来效果，
**改 `references/style-recipes.md` 里的配方原文**，不要每次在调用侧临时加补救词。
临时补救词不进真源，下一次调用又会漂回去。

## 8. 质量红线

每次出图后自查，有硬伤就重出一次，并向用户说明改了什么：

- 人脸不像原图 / 换了一张脸 → 提高 `input_fidelity` 到 `high`，prompt 里加重 `preserve the recognizable identity and facial features`。
- 多出一个人 / 少了一个人 / 人脸融合 → prompt 里显式写明人数 `exactly N subjects`。
- 手部畸形 → prompt 加 `hands anatomically coherent, correct finger count`。
- 原图有文字被糊掉或乱码 → 加 `preserve existing text exactly`。
- 皮肤塑料感 → 加 `natural skin texture, avoid plastic skin`。

深度配方自带 `Fail conditions` 段，是每套风格专属的失败判据。出图后**逐条对照**该段检查，
命中任意一条就判不合格并重出——这是深度配方相比一行式描述最大的价值所在，不要跳过。

## 9. 验证状态（务必知悉）

`references/style-recipes.md` 中的 15 套配方是**基于画风知识的深度初稿，尚未经真机出图验证**。

构建时没有可用的图生图环境，因此本仓库目前没有样图与实测结论。
在有图生图能力的宿主中实测后，请：

1. 把样图与结论放进 `benchmarks/`，失败样例也要留（失败图比成功图更能说明问题）；
2. 只针对**已稳定复现**的偏差修改配方原文，不要凭单张满意图就改；
3. 至少验证一个与配方描述同构的场景 + 一个跨主体场景；
4. 更新 `style-recipes.md` 顶部的验证状态说明。
