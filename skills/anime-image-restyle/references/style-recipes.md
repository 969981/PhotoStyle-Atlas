# 深度画风配方库

本文件是**风格真源**。每段是一套可原样交付给图像模型的完整英文配方，由 `scripts/render_prompt.py` 提取，
**不得手工缩写、同义改写或与多套配方混配**。

与 `style-registry.md` 的分工：

- `style-registry.md` — 71 个 key 的**一行速查**，用于命中别名、判断该用哪个 key。
- 本文件 — 15 个高频 key 的**完整配方**，命中后从这里取原文。

不在这 15 个里的 key，按 `PROTOCOL.md` 的槽位组装流程走 `prompt-lexicon.md`。

> **验证状态：本文件的配方为「基于画风知识的深度初稿，未经真机出图验证」。**
> 维护者在图生图环境实测后，请把结论与样图补进 `benchmarks/` 并更新本段状态。
> 配方原文一旦被实测修正，**只改本文件**，不要在业务侧另维护第二套画风描述。

---

## cel-tv-clean｜现代TV赛璐璐

> **别名**：动漫风、二次元、日漫风、动画风（兜底默认值）
> **命门**：① 线条等细、闭合、干净，不许毛笔感或抖动；② 阴影只有一层硬边，皮肤绝不能渐变；
> ③ 高饱和清亮，不能灰雾或电影调色；④ 背景简化成有限色块，但保留原场景空间布局。
> **整体判断**：第一眼像现代 TV 动画的一帧——干净、平、亮。若皮肤出现柔和渐变或画面发灰即判不合格。

```text
Render Image 1 as a modern Japanese TV anime cel still.

Linework: crisp, even, thin dark brown-black outlines with consistent weight. Contours are closed and clean. No sketchy, doubled, or tapered brush strokes.

Coloring: flat cel shading. One hard-edged shadow layer per surface, with a hard boundary between light and shadow. At most one additional lighter tone on hair. Small crisp specular highlights on hair and eyes only.

Palette: bright, clean, medium-high saturation. Skin is an even warm tone with a small flat blush. No grayish desaturation, no filmic color grade.

Background: simplify the original scene into a readable painted anime background — a limited number of flat color planes, slightly reduced detail, soft depth separation. Keep the original spatial layout.

Surface: clean digital cel. No canvas grain, no film noise, no photographic texture carried over from the source, no painterly brush marks.

Fail conditions: soft gradient shading on skin; airbrushed blush; semi-realistic painterly rendering; thick visible brush strokes; watercolor bleeding or paper texture; visible pencil construction lines; desaturated muddy palette.
```

---

## cel-90s-film｜90年代胶片赛璐璐

> **别名**：老动画、怀旧番、胶片感
> **命门**：① 线是手绘上墨的，带人抖和出头，比现代数字赛璐璐更重更黑；② 阴影两层且**带色偏**，不能是中性灰；
> ③ 整体蒙暖调、轻微褪色；④ 全画有细胶片颗粒。
> **整体判断**：像一张扫描自胶片的动画赛璐璐。若线条干净利落、阴影纯灰、零颗粒，就是做成了现代赛璐璐，判不合格。

```text
Render Image 1 as a 1990s Japanese cel-animation film frame.

Linework: hand-inked dark outlines of slightly uneven weight with visible human wobble. Corners slightly overshoot. The line is darker and heavier than modern digital cel.

Coloring: flat cel base with two shadow layers. The second layer is slightly softer and tinted toward warm brown or violet rather than pure gray. Shadows are subtly colored, never neutral gray.

Palette: slightly faded and warm-shifted. Highlights drift toward cream yellow, shadows toward warm brown. Overall lower contrast than modern digital cel, with a gentle filmic color cast.

Light and surface: visible fine film grain across the whole frame, very slight blooming on highlights, a hint of chromatic softness at the edges. Think a scanned animation cel photographed on film.

Background: hand-painted on paper, muted, with visible gouache or poster-paint texture and slightly muddy color mixing.

Fail conditions: crisp modern digital linework; pure neutral-gray shadows; zero grain; high-contrast modern palette; plastic clean vector look; heavy digital sharpening.
```

---

## anime-watercolor｜水彩动画插画

> **别名**：水彩、水彩风、淡彩
> **命门**：① 颜料在纸上自然扩散，**边缘必须有深色沉积**；② 大面积留白纸，不能涂满；
> ③ 颜色透明叠色，底下透得出来；④ 线是淡彩线或局部色线，绝不是黑粗线。
> **整体判断**：第一眼是"画在纸上"的通透感。若颜色不透明、涂满无留白、出现黑粗轮廓，即判不合格。

```text
Render Image 1 as a Japanese anime watercolor illustration.

Pigment behavior: transparent watercolor washes. Color pools unevenly, with darker pigment sedimentation collecting at the edges of each wash. Overlaps between two washes create a visibly darker secondary tone. Paint does not fully cover what is underneath.

Edges: soft, irregular wash boundaries with characteristic hard pigment deposits at the rim. Some areas bleed outward, some dry short with a broken dry-brush edge.

Palette: light, airy, slightly desaturated but luminous. Skin is a very thin warm wash. Large areas of the paper are left unpainted.

Linework: thin, light colored-line contour — warm brown or a darker version of the local color, never heavy black. Lines may break, skip, and vary in opacity.

Paper: visible cold-press watercolor paper texture throughout, including inside painted areas.

Fail conditions: opaque gouache or acrylic coverage; thick painterly impasto; heavy black outlines; uniform digital airbrush gradients; plastic smooth skin; fully painted background with no paper showing; vector flat cel shading.
```

---

## painterly-fantasy｜奇幻厚涂

> **别名**：厚涂、油画感、奇幻插画
> **命门**：① 笔触与颜料堆积必须看得见；② 体积靠明暗塑造，不是平涂色块；③ 边缘虚实交替，焦点处锐利、其余融进色调；
> ④ 阴影带冷色、高光带暖色，有环境反射光。
> **整体判断**：像一张奇幻游戏封面油画。若出现平涂硬边阴影、或光滑无笔触的喷枪渐变，即判不合格。

```text
Render Image 1 as a fantasy oil-painting style anime illustration.

Paint handling: thick opaque painterly strokes with visible brush direction and impasto build-up. Edges alternate between crisp focal edges and soft lost edges that dissolve into the surrounding tone.

Form: volume is built with light and shadow, not flat color planes. Core shadow, reflected light, and a rim light are all present. Skin shows subtle subsurface warmth.

Palette: rich and saturated, with colored light — shadows lean cool violet or blue, highlights lean warm. Environment reflects colored bounce light onto the subject.

Background: painterly environment with atmospheric depth, softer and less detailed than the subject.

Surface: canvas texture subtly visible under the paint.

Fail conditions: flat cel shading; airbrushed smooth gradients with no brush character; uniform digital soft focus; desaturated gray shadows; photographic skin texture; crisp anime linework dominating the image.
```

---

## sketch-pencil｜铅笔素描

> **别名**：素描、铅笔素描、铅笔画
> **命门**：① **必须有排线方向与疏密变化**，不能是均匀灰面；② 纯黑白灰，出现任何彩色即失败；
> ③ 纸张颗粒贯穿暗部，高光是留出的纸白不是白颜料；④ 轮廓线有轻重和断开，不是等粗细描边。
> **整体判断**：第一眼是"用铅笔画出来的"，能看到手的方向和力度。若像一张去色照片、或灰面均匀无笔触，即判不合格。

```text
Render Image 1 as a graphite pencil drawing on paper.

Tone: monochrome only — black, white, and gray. No color anywhere, including no warm or cool tint.

Mark-making: tone is built from visible graphite hatching and cross-hatching. Stroke direction must change between surfaces — follow the form of the face, hair, and fabric rather than laying one uniform direction. Density varies to describe value, with the darkest accents built from multiple crossing layers.

Linework: contour lines vary in pressure, breaking and overlapping. No uniform-weight outlines. A light under-drawing may show through.

Edges: some edges are defined by a firm line, others are implied by a change in hatch density alone. Not every contour is drawn.

Paper: visible tooth of the paper throughout, including inside dark areas. Highlights are the bare paper left untouched, not white paint.

Eraser: allow soft eraser lifts and smudged transitions in midtones.

Fail conditions: any color, even slight; uniform gray fills with no stroke direction; a photographic or airbrushed smooth gradient masquerading as shading; pure black filled silhouettes; a digital sketch filter with repeated identical strokes; white painted highlights instead of reserved paper; heavy inked comic outlines.
```

---

## line-minimal｜极简简笔

> **别名**：简笔、简笔画、极简线描
> **命门**：① **一条连贯线勾形**，无填充、无排线、无第二遍描；② 白底或单一纯色底，不画场景；
> ③ 极度简化，不能帮识别主体和动态的一律删掉；④ 线宽基本均匀，不是漫画式粗细变化线。
> **整体判断**：像一笔画成的图标级涂鸦，几根线就认得出是谁。若有任何填充色、排线或背景细节，即判不合格。

```text
Render Image 1 as an extreme minimal line drawing.

Line: a single continuous, confident contour that captures the subject's silhouette and the few essential internal features. Line weight is even, or varies only very slightly. No shading, no hatching, no fill, no second pass.

Reduction: strip everything non-essential. No texture, no small folds, no background detail, no decorative elements. If a detail does not help identify the subject or the pose, omit it.

Background: plain white, or a single flat pale color. No scene, no environment, no gradient.

Color: monochrome line — black or a single ink color — on the plain ground.

Character: the drawing should read instantly despite extreme simplification. Proportion and gesture carry all the information.

Fail conditions: any fill color; hatching or cross-hatching; multiple overlapping sketchy strokes searching for the form; textured or shaded rendering; detailed background; thick comic-style variable-width outlines; a full-tone sketch rather than a true minimal line.
```

---

## xieyi-ink｜写意水墨

> **别名**：水墨、写意、中国画
> **命门**：① **一笔之内要有浓淡变化（墨分五色）**，不能平涂黑块；② 起笔湿渗、收笔飞白枯笔；
> ③ 大面积留白是构图的一部分，不是没画完；④ 线条是书法用笔，有方向和起收，不能描。
> **整体判断**：像一幅写意中国画。若黑块平匀无墨阶、或像铅笔排线、或画满无留白，即判不合格。

```text
Render Image 1 as a Chinese xieyi (freehand) ink painting.

Ink behavior: ink is loaded once and laid down in single decisive strokes that carry a full gradient from wet dark to dry pale within one stroke — the classic five tones of ink. Wet bleeding into absorbent paper at the start, dry broken white streaks as the brush runs out.

Brushwork: broad sweeping strokes for large forms, fine lines only for essential detail. Strokes are calligraphic — they have direction, pressure, and a clear beginning and end. No tentative scratching.

Space: large areas of empty paper are compositionally essential, not unfinished. Empty space and painted space balance each other.

Color: monochrome ink as the main body. If any color appears it is a restrained mineral tint — light indigo or ochre — used sparingly, never filling the whole image.

Seal: a small vermilion red seal stamp in a corner is appropriate.

Paper: absorbent xuan paper with visible fiber and slight irregular bleeding at stroke edges.

Fail conditions: uniform flat black fills with no ink gradation; pencil-like hatching; photographic grayscale; heavy outlined cartoon rendering; fully painted background with no empty space; glossy digital gradients.
```

---

## gongbi-heavy-color｜工笔重彩

> **别名**：工笔、重彩、敦煌
> **命门**：① 极细等粗的墨线勾全部轮廓（铁线描），线是骨架不能断；② 颜色多层罩染，厚重饱和且**看不见笔触**；
> ③ 完全不做光影体积，是平面装饰性的；④ 矿物颜料色 + 精细纹样 + 可描金。
> **整体判断**：像一幅工笔重彩国画。若出现西式明暗、可见笔触、或写意泼墨，即判不合格。

```text
Render Image 1 as a Chinese gongbi heavy-color painting.

Linework: extremely fine, even-width ink contour lines — the iron wire line. Every form is first defined by a precise unbroken outline. Line weight barely varies.

Coloring: built from many thin transparent layers washed over each other until the color becomes deep, saturated, and luminous. No visible brush strokes in the final color. No light-and-shadow modeling; form is expressed by the outline and by flat color.

Palette: mineral pigment colors — azurite blue, malachite green, cinnabar red, gamboge yellow, oyster white. Rich, opaque, decorative, with strong complementary contrast.

Detail: pattern and texture are rendered as fine decorative motifs — fabric patterns, cloud scrolls, floral motifs — drawn precisely, not suggested.

Finish: flat, decorative, two-dimensional. Gold outlining or gold leaf accents are appropriate on garment edges and ornament.

Ground: warm aged silk or sized paper tone showing through pale areas.

Fail conditions: visible painterly brush strokes; Western chiaroscuro shading; loose wet ink washes; sketchy broken outlines; photographic texture; airbrushed gradients; modern flat cel anime shading.
```

---

## cyber-rain-neon｜雨夜霓虹赛博

> **别名**：赛博朋克、赛博、霓虹雨夜
> **命门**：① **霓虹是主光源**，多色混光，暗部压得很深；② 湿地面和湿衣物必须有反射与拉长的倒影；
> ③ 必须有雨（雨丝、水珠、光源光晕）；④ 阴影颜色由霓虹决定，不是中性灰。
> **整体判断**：像赛博朋克动画的一帧。若只是给正常曝光的图套个蓝调、地面干燥无反射、没有雨，即判不合格。

```text
Render Image 1 as a cyberpunk neon-rain anime illustration.

Light: the scene is lit almost entirely by neon signage — magenta, cyan, and electric violet — plus practical lights. Multiple colored light sources hit the subject from different directions, producing colored rim light on one side and a complementary colored fill on the other. Ambient light is very dark.

Contrast: deep crushed shadows with bright specular accents. The subject reads as a dark silhouette penetrated by neon rim light.

Wet surfaces: wet ground and wet garments reflect and smear the neon. Reflections are vertically stretched and broken by ripples. Rain is visible — streaks in the air, droplets on surfaces, a faint haze around light sources.

Palette: predominantly dark blue-violet and near-black, punctuated by saturated magenta and cyan. Skin takes on the color of whatever light is nearest.

Rendering: clean anime rendering with cel or semi-painterly shading, but the shading color is dictated by the neon, not by a neutral gray.

Atmosphere: volumetric haze, light bloom, and slight chromatic aberration around bright sources.

Fail conditions: flat evenly-lit daylight look; neutral gray shadows; dry matte ground with no reflections; a simple blue color grade over a normally lit image; no visible rain; washed-out low-contrast neon.
```

---

## pixel-16bit｜16位像素动漫

> **别名**：像素、8bit、16bit
> **命门**：① **硬边方块、零抗锯齿**，不能有模糊边缘；② 有限调色板（约 16–32 色），过渡靠手工抖色；
> ③ 深色 1px 像素线勾边；④ 大胆砍细节，不能试图保留照片的微妙层次。
> **整体判断**：像 SFC/GBA 时代的游戏精灵图。若边缘平滑、颜色成百上千、或只是给原图套了个马赛克滤镜，即判不合格。

```text
Render Image 1 as a 16-bit era Japanese pixel-art illustration.

Pixel grid: every edge is a hard square step on a visible pixel grid. No anti-aliasing anywhere — no soft or blurred edges. Pixels are large enough to read clearly.

Palette: a limited indexed palette, roughly 16 to 32 colors. Colors are reused across the image rather than individually sampled. Transitions between tones use deliberate dithering patterns, not smooth gradients.

Shading: two to three discrete value steps per surface, hard-edged. Highlights are small clusters of brighter pixels.

Linework: dark 1-pixel outlines, often a dark version of the local color rather than pure black.

Detail: small features must be suggested with very few pixels — eyes and face features are reduced to a handful of carefully placed pixels.

Source fidelity: reduce the original image's detail aggressively to fit the pixel budget. Do not attempt to preserve photographic nuance.

Fail conditions: anti-aliased or blurry edges; smooth photographic gradients; a color count in the hundreds; a simple pixelate or mosaic filter applied over a full-color image; smooth vector-style curves; text rendered too small to be legible in pixels.
```

---

## manga-bw-screentone｜黑白网点漫画

> **别名**：黑白漫画、网点、线稿漫画
> **命门**：① **纯黑白**，灰面只能用网点（screentone）表达，不能有灰阶渐变；② 墨线粗细分明；
> ③ 刻意使用大块纯黑制造重量感；④ 纯白、纯黑、网点三者的分布要清楚。
> **整体判断**：像青年漫画的一格。若是去色照片、或灰面是无点阵的平滑渐变，即判不合格。

```text
Render Image 1 as black-and-white Japanese manga art with screentone.

Monochrome: strictly black and white. No color, no sepia, no gray gradients.

Tone: midtones are expressed with screentone — regular dot patterns at varying density. Different densities for different values. The dot pattern is visibly regular and mechanical, distinct from hatching.

Linework: clean black ink lines with clear thick-and-thin variation. Major contours are solid and confident; interior detail lines are finer.

Contrast: strong black masses are used deliberately for weight and drama — solid black hair, solid black shadows. The composition should have clear areas of pure white, pure black, and tone.

Effects: speed lines, focus lines, or effect tones are appropriate for emphasis.

Background: simplified or replaced with tone, keeping the original spatial layout.

Fail conditions: grayscale airbrushed shading with no dot texture; any color tint; a photographic desaturation filter; uniform thin vector linework with no weight variation; gray mush with no solid blacks or clean whites.
```

---

## chibi-2head｜二头身Q版

> **别名**：Q版、二头身、萌化
> **命门**：① 头身比约 1:2，**头极大**；② 五官压在脸的下半部；③ 四肢短圆，手是小圆球；
> ④ **发型轮廓、发色、瞳色和标志性配件必须保留**——这是"还认得出是谁"的唯一凭据。
> **整体判断**：一眼认出是同一个人，但被萌化了。若换了发型、丢了标志配件、或脸变成了通用路人，即判不合格。

```text
Render Image 1 as a two-head-tall chibi anime character.

Proportions: total height is about two head-lengths. The head is very large relative to the body, the body and limbs are short and rounded. Hands and feet are simplified into small rounded mitts and stubby shapes.

Face: eyes are large and placed low on the face, with the features compressed into the lower half. A small simple mouth and nose. The expression is simplified but must still read as the same person.

Identity: hairstyle silhouette, hair color, eye color, and any signature accessory or garment detail from the original must be clearly preserved — these are what keep the chibi recognizable.

Rendering: clean cel shading, bright saturated palette, simple rounded forms. Minimal interior detail on the body and clothing.

Background: plain or very simple, so the small figure reads clearly.

Fail conditions: realistic proportions; four-head or taller SD proportions; losing the hairstyle or signature accessory that identifies the person; over-detailed clothing; a completely generic face with no likeness; inconsistent eye structure.
```

---

## sky-luminous-cinema｜通透天空电影感

> **别名**：新海诚风、你的名字风、唯美天空
> **命门**：① **天空是主角**，积云要有体积和多层次；② 强逆光 + 光晕 + 光芒，人物有暖色轮廓光；
> ③ 青蓝 × 金橙的互补分割；④ 远景强烈空气透视，往天空色里fade。
> **整体判断**：像现代日本动画电影的天空镜头。若天空是灰平的一层渐变、没有云的形态结构，即判不合格。

```text
Render Image 1 as a luminous cinematic anime landscape in the manner of a modern Japanese animated film sky.

Sky: the sky dominates. Towering cumulus clouds with clearly modeled light and shadow, multiple depth layers, and a luminous gradient from deep blue at the zenith to warm pale near the horizon. Cloud edges catch strong light.

Light: low sun or strong backlight. Visible lens bloom, light streaks, light shafts, and a warm rim on every foreground edge. Highlights bloom gently.

Palette: clean saturated blues against warm golden or orange light. A clear complementary split — cool blue sky and shadow, warm gold sunlight. Colors are saturated but never muddy.

Atmosphere: strong aerial perspective — distant elements fade toward the sky color. Everything feels freshly washed and transparent.

Foreground: the subject is crisply rendered with clean anime linework against the painterly sky. Grass, foliage, and small details are drawn with precision.

Fail conditions: flat gray overcast sky; no visible cloud structure; low-contrast washed-out palette; photographic HDR look; heavy film grain; the sky rendered as a plain gradient with no cloud form.
```

---

## handpainted-nature-fable｜手绘自然童话

> **别名**：吉卜力风、宫崎骏风
> **命门**：① **背景必须是画出来的**，全手绘水粉笔触，绝不是照片虚化；② 植物茂密，叶片成簇、笔触可见；
> ③ 光是暖的，阴影带色（暖褐或绿调），不是中性灰；④ 人物线条简洁圆润，不是时髦插画的锋利比例。
> **整体判断**：像经典手绘动画的自然场景。若背景有照片感、或色彩冷灰、或人物是潮流插画比例，即判不合格。

```text
Render Image 1 as a hand-painted storybook animation illustration in the spirit of a classic Japanese hand-drawn nature fable.

Paint: everything is painted in opaque watercolor and gouache with visible brushwork. Backgrounds are painted, never photographic. Foliage, grass, and clouds are built from distinct brush marks rather than smooth fills.

Nature: vegetation is dense, lush, and slightly overgrown. Leaves and grass are drawn in clusters with varied greens, warm touches, and visible individual strokes.

Light: warm, soft, slightly hazy sunlight. Gentle dappled light through leaves. Shadows are colored — warm brown or green-tinted, never neutral gray.

Characters: simple rounded linework, warm and friendly, with a soft blush and expressive but simple faces. Not sleek or glamorous.

Palette: earthy greens, warm ochres, soft sky blue, brick and terracotta accents. Harmonious and slightly muted, never neon.

Texture: subtle paper grain and paint texture throughout, including on the character.

Fail conditions: photographic background; smooth airbrushed digital gradients; cool blue-gray sterile palette; sleek modern anime character rendering with sharp fashion-illustration proportions; flat vector shapes with no brush character.
```

---

## game-gacha-render｜二游抽卡图

> **别名**：二游立绘、抽卡图、游戏宣传图
> **命门**：① 细节密度极高，发丝、饰品、材质全部画完，不能"暗示"；② 材质分离明确——金属、皮革、布料、蕾丝、玻璃各有各的表面逻辑；
> ③ 背景华丽但虚化、带光效粒子，绝不抢人物；④ 脸精致但**保留皮肤质感，不能塑料**。
> **整体判断**：像手游的 SSR 立绘。若饰品糊掉、材质不分、皮肤像蜡像，即判不合格。

```text
Render Image 1 as a premium Japanese gacha game character illustration.

Detail density: very high. Hair is rendered as many individually defined strands with visible flyaways and inner-hair shading. Garments have fully realized material separation — metal, leather, fabric, lace, and glass each rendered with its own surface logic. Accessories and ornament are drawn completely, not suggested.

Rendering: refined semi-painterly anime rendering. Clean cel base with painterly finish on skin, hair, and materials. Soft gradients on skin only, crisp cel-like edges on hard materials.

Palette: high saturation with strong complementary accents — often a jewel-tone base with a single contrasting accent color.

Light: deliberate cinematic key light with rim light separating the character from the background. Bloom, light particles, and glow accents are appropriate.

Background: an ornate but soft-focus environment or decorative frame with light particles and atmospheric effects, clearly subordinate to the character.

Face: polished and attractive while retaining real skin texture — not plastic. Eyes have detailed iris structure and clean specular highlights.

Fail conditions: plastic waxen skin with no texture; blurry or simplified accessories; flat cel rendering with no material differentiation; muddy desaturated palette; a busy background competing with the character; deformed hands or inconsistent ornament symmetry.
```

---

## 附录 · 叠加层（可选，追加在配方之后）

命中下列需求时，把对应段落**原样追加**在配方末尾，不要改写配方本体：

### 极简背景

```text
Replace the background with a plain flat pale ground or a very simple abstract shape composition. Remove environmental detail while keeping the subject's silhouette and the original framing.
```

### 保留原光线

```text
Keep the original lighting direction, light quality, and highlight placement from the source image. Do not restage the light to the style's default.
```

### 竖版封面构图

```text
Recompose for a vertical book-cover crop: subject placed in the upper two thirds, lower third reserved for negative space, keeping the subject's identity and the style exactly as specified above.
```
