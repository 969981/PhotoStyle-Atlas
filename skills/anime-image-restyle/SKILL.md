---
name: anime-image-restyle
version: 1.4.0
description: 把用户上传的单张原照片直接转换成指定动漫风格并出图。当用户上传图片后说「转成XX风格」「动漫风」「二次元」「水彩」「国风」「赛博朋克」「Q版」「像素」「厚涂」「吉卜力风」「新海诚风」「素描」「简笔」等时使用。默认保留人物身份、表情、姿势、人数、构图与关键物件，只替换视觉语言；支持保真/标准/重构三档强度，以及画幅、背景、光线控制。内置 11 大风格家族 71 个风格 key，其中 15 个高频 key 配有完整深度配方（由 scripts/render_prompt.py 原样提取，禁止改写），其余走可组合槽位体系（人设体系+线稿+上色+调色+光影+时代地域+题材美术+氛围+镜头）。
---

# 动漫原图风格转换

最小输入 = **一张原图 + 一句风格描述**。用户给到这两项就直接出图，不要再反问确认。

风格描述可以是单一标签（「水彩风」），也可以是任意维度组合（「90年代手绘赛璐璐，雨夜霓虹街，低机位广角」）。两种都要能直接处理。

## 核心原则

默认任务是**封装式风格迁移**：只换画法、材质、色彩、光影、渲染方式；不改主体身份、脸部特征、发型轮廓、人数、姿势、表情、镜头、构图、空间关系、关键物件与文字位置。

只有当用户明确说「重构 / 换场景 / 换服装 / 换姿势」时，才改变内容。

不使用在世艺术家姓名或具体作品名作为风格锚点。用户提到人名或作品名时，提取其视觉特征，映射成原创特征描述，**不声称复刻**。

## 执行流程

1. **定位原图** —— 本轮附件路径 → 用户写的绝对路径 → 本会话最近一次图片 → 都找不到才问。
2. **解析风格** —— 先查下方别名表；没命中再按 [PROTOCOL.md](PROTOCOL.md) 逐槽拆解。
3. **取配方** —— 见下方两条路径，纪律不同，**这是出图质量的关键**。
4. **出图** —— 画幅映射、保真度、输出路径见 [PROTOCOL.md](PROTOCOL.md)。
5. **交付** —— 呈现成品 + 一行摘要 + 记一行 ledger，详见 PROTOCOL.md。

### 取配方：两条路径

#### 路径 A · 深度配方（15 个 key，优先走这条）

`cel-tv-clean` · `cel-90s-film` · `anime-watercolor` · `painterly-fantasy` · `sketch-pencil` · `line-minimal` · `xieyi-ink` · `gongbi-heavy-color` · `cyber-rain-neon` · `pixel-16bit` · `manga-bw-screentone` · `chibi-2head` · `sky-luminous-cinema` · `handpainted-nature-fable` · `game-gacha-render`

命中这 15 个 key 时：

- **能执行脚本就必须调用 `scripts/render_prompt.py`**，不要自己手写 prompt。
- **禁止**手工缩写、同义改写、摘几句、把多套配方揉在一起。配方原文是已固化的资产，改写就是制造风格漂移。
- 只有脚本确实不可运行时，才手工从 `references/style-recipes.md` 取对应段落，且必须**整段照抄**。

```bash
python scripts/render_prompt.py --style sketch-pencil
python scripts/render_prompt.py --style 水墨 --aspect 9:16 --intensity 强度
python scripts/render_prompt.py --style cyber-rain-neon --layer minimal-bg
python scripts/render_prompt.py --list          # 列出全部深度配方 key
```

脚本自动拼好「保真前缀 + 配方原文 + 防劣化后缀」并输出，直接把结果交给图生图工具即可。

#### 路径 B · 槽位组装（其余 56 个 key）

命中其它 key 时，按 [PROTOCOL.md](PROTOCOL.md) 的槽位拆解流程，用 `references/prompt-lexicon.md` 的英文短语组装。

脚本对这类 key 会退回 `style-registry.md` 的一行式描述，并在 stderr 提示「暂无深度配方，保真度低于深度配方」——看到这个提示就知道这批出图稳定性会差一些。

## 口语别名表

高频说法先查这里，命中就直接用，省去读注册表。

| 用户说法 | key |
|---|---|
| 动漫风、二次元、日漫风、动画风 | `cel-tv-clean` |
| 吉卜力风、宫崎骏风 | `handpainted-nature-fable` |
| 新海诚风、你的名字风、唯美天空 | `sky-luminous-cinema` |
| 京阿尼风、轻音风、通透日常 | `cel-10s-clear` |
| 少女漫、乙女风 | `shoujo-ethereal` |
| 少年漫、热血漫、战斗番 | `shonen-dynamic` |
| 老动画、怀旧番、胶片感 | `cel-90s-film` |
| 赛博朋克、赛博、霓虹雨夜 | `cyber-rain-neon` |
| 国风、古风、仙气 | `guofeng-cel` |
| 水墨、写意、中国画 | `xieyi-ink` |
| 工笔、重彩、敦煌 | `gongbi-heavy-color` |
| 厚涂、油画感 | `painterly-fantasy` |
| 水彩 | `anime-watercolor` |
| 像素、8bit、16bit | `pixel-16bit` |
| Q版、二头身、萌化 | `chibi-2head` |
| 三渲二、3D 动漫 | `anime-3d-cel` |
| 皮克斯风、迪士尼 3D | `toon-3d-clean` |
| 黑白漫画、网点、线稿漫画 | `manga-bw-screentone` |
| 暗黑、哥特 | `gothic-lace` |
| 二游立绘、抽卡图、游戏宣传图 | `game-gacha-render` |
| 头像 | `icon-avatar`（追加修饰符） |
| 贴纸、抠图 | `sticker-cutout`（追加修饰符） |
| 素描、铅笔素描、铅笔画 | `sketch-pencil` |
| 简笔、简笔画、极简线描 | `line-minimal` |

### 时代与地域

| 用户说法 | key |
|---|---|
| 国漫、中国2D国漫、国产2D | `cn-2d-donghua` |
| 韩漫、条漫、webtoon、韩国漫画 | `kr-webtoon` |
| 韩游、韩国游戏概念图、韩系立绘 | `kr-game-concept` |
| 美式卡通、欧美卡通 | `us-cartoon` |
| 迪士尼风、皮克斯风、美式动画电影 | `us-animation-film` |
| 美漫、超英漫画、超级英雄漫画 | `us-superhero-comic` |
| 欧式绘本、法漫、欧洲漫画 | `fr-european-picturebook` |
| 俄式童话、东欧动画、民俗动画 | `ru-eastern-folktale` |

### 人设体系

| 用户说法 | key |
|---|---|
| galgame、美少女游戏、Galgame立绘 | `galgame-portrait` |

### 题材美术（可叠加）

| 用户说法 | key |
|---|---|
| 校园、青春、校园番、制服 | `theme-campus-youth` |
| 偶像、舞台、演唱会、爱豆 | `theme-idol-stage` |
| 魔法少女、变身、魔法少女番 | `theme-magical-girl` |
| 异世界、转生、轻奇幻、冒险者 | `theme-isekai-fantasy` |
| 和风、日式幻想、神社、妖怪和风 | `theme-japanese-fantasy` |
| 西幻、西方奇幻、史诗奇幻、龙与城堡 | `theme-western-epic` |
| 治愈系、日常番、温馨日常 | `theme-daily-healing` |
| 美食番、料理、食物特写 | `theme-food-anime` |
| 未来都市、极简科幻、白色未来 | `theme-minimal-future` |
| 深夜食堂、居酒屋、市井美食 | `theme-gourmet-night` |

### 镜头与用途

| 用户说法 | key |
|---|---|
| 立绘、角色立绘、全身立绘 | `fullbody-sheet` |
| 主视觉、KV、海报 | `key-visual` |
| 分镜、漫画格、漫画分镜 | `manga-panel` |

## 参考文件

- **[PROTOCOL.md](PROTOCOL.md)** —— 完整执行协议：定位原图、槽位拆解、编译提示词、画幅映射、出图参数、质量红线、迭代修订、渲染器完整参数表
- **[references/style-recipes.md](references/style-recipes.md)** —— **15 套深度配方真源**。风格描述只在这里改，其他任何地方不得复制第二份
- `references/style-registry.md` —— 71 个 key 一行速查，用于命中别名后确认该用哪个 key
- `references/prompt-lexicon.md` —— 英文提示词短语库，12 个槽位，供路径 B 组装
- `scripts/render_prompt.py` —— 原样提取 + 拼装渲染器（路径 A 强制使用）
- `scripts/probe_image.py` —— 纯标准库读原图宽高，判横竖构图
