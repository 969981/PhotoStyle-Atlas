#!/usr/bin/env python3
"""Render a restyle prompt without paraphrasing the style recipe.

The style recipes in `references/style-recipes.md` are the single source of
truth. This script extracts the matching block **verbatim** and only prepends
the identity-preservation preamble and appends the guardrail postscript. The
agent must not hand-abbreviate, paraphrase, or merge recipes — drift in the
wording is exactly what makes restyle output inconsistent between runs.

Usage:
    python scripts/render_prompt.py --style sketch-pencil
    python scripts/render_prompt.py --style 水墨 --aspect 9:16 --intensity 强度
    python scripts/render_prompt.py --style cyber-rain-neon --layer minimal-bg
    python scripts/render_prompt.py --list

Stdlib only. Exit code 0 on success, 2 on a usage or validation error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECIPES_PATH = ROOT / "references" / "style-recipes.md"
REGISTRY_PATH = ROOT / "references" / "style-registry.md"

# Chinese display names, used only inside the preamble sentence.
STYLE_NAMES = {
    "cel-tv-clean": "modern TV cel anime",
    "cel-90s-film": "1990s cel-animation film",
    "anime-watercolor": "anime watercolor",
    "painterly-fantasy": "fantasy oil-painting anime",
    "sketch-pencil": "graphite pencil",
    "line-minimal": "minimal line",
    "xieyi-ink": "Chinese xieyi ink",
    "gongbi-heavy-color": "Chinese gongbi heavy-color",
    "cyber-rain-neon": "cyberpunk neon-rain anime",
    "pixel-16bit": "16-bit pixel-art",
    "manga-bw-screentone": "black-and-white manga screentone",
    "chibi-2head": "two-head-tall chibi",
    "sky-luminous-cinema": "luminous cinematic anime sky",
    "handpainted-nature-fable": "hand-painted nature fable",
    "game-gacha-render": "premium gacha game",
}

ALIASES = {
    "动漫风": "cel-tv-clean", "二次元": "cel-tv-clean", "日漫风": "cel-tv-clean",
    "动画风": "cel-tv-clean",
    "老动画": "cel-90s-film", "怀旧番": "cel-90s-film", "胶片感": "cel-90s-film",
    "水彩": "anime-watercolor", "水彩风": "anime-watercolor", "淡彩": "anime-watercolor",
    "厚涂": "painterly-fantasy", "油画感": "painterly-fantasy",
    "素描": "sketch-pencil", "铅笔素描": "sketch-pencil", "铅笔画": "sketch-pencil",
    "简笔": "line-minimal", "简笔画": "line-minimal", "极简线描": "line-minimal",
    "水墨": "xieyi-ink", "写意": "xieyi-ink", "中国画": "xieyi-ink",
    "工笔": "gongbi-heavy-color", "重彩": "gongbi-heavy-color", "敦煌": "gongbi-heavy-color",
    "赛博朋克": "cyber-rain-neon", "赛博": "cyber-rain-neon", "霓虹雨夜": "cyber-rain-neon",
    "像素": "pixel-16bit", "8bit": "pixel-16bit", "16bit": "pixel-16bit",
    "黑白漫画": "manga-bw-screentone", "网点": "manga-bw-screentone",
    "线稿漫画": "manga-bw-screentone",
    "q版": "chibi-2head", "二头身": "chibi-2head", "萌化": "chibi-2head",
    "新海诚风": "sky-luminous-cinema", "你的名字风": "sky-luminous-cinema",
    "唯美天空": "sky-luminous-cinema",
    "吉卜力风": "handpainted-nature-fable", "宫崎骏风": "handpainted-nature-fable",
    "二游立绘": "game-gacha-render", "抽卡图": "game-gacha-render",
    "游戏宣传图": "game-gacha-render",
}

# Optional add-on layers, extracted from the appendix by Chinese heading.
APPENDIX_LAYERS = {
    "minimal-bg": "极简背景",
    "keep-light": "保留原光线",
    "vertical-cover": "竖版封面构图",
}

PREAMBLE = {
    "轻度": (
        "Apply subtle {name} rendering to Image 1, preserving the original "
        "lighting, fine detail, and background information. Preserve the "
        "recognizable identity and facial features of every subject, the exact "
        "number of subjects, pose, expression, body proportions, hairstyle "
        "silhouette, clothing silhouette, key objects, camera angle, "
        "composition, crop, spatial layout{aspect}."
    ),
    "中度": (
        "Transform Image 1 into an original {name} illustration. Preserve the "
        "recognizable identity and facial features of every subject, the exact "
        "number of subjects, pose, expression, body proportions, hairstyle "
        "silhouette, clothing silhouette, key objects, camera angle, "
        "composition, crop, spatial layout{aspect}."
    ),
    "强度": (
        "Fully reinterpret Image 1 in {name}. Preserve the recognizable "
        "identity and facial features of every subject, the exact number of "
        "subjects, pose, expression, body proportions, and hairstyle "
        "silhouette. Allow the style to rebuild background detail, garment "
        "detail, and surface texture, but keep the composition, camera angle, "
        "and key objects{aspect}."
    ),
}

POSTSCRIPT = (
    "Change only the visual rendering style unless the user explicitly "
    "requested content changes. Keep hands anatomically coherent, eyes "
    "aligned, facial features consistent, clean silhouettes, and readable "
    "object geometry. Preserve any existing text exactly when legible; "
    "otherwise omit new text. Do not add extra people, duplicate limbs, alter "
    "identity, change ethnicity, change age category, replace important "
    "objects, add watermark, add logo, add signature, add random text, make "
    "plastic skin, blur the face, or introduce deformed hands."
)


def canonical_style_id(value: str) -> str:
    return ALIASES.get(value.strip().lower(), value.strip())


def _first_block_after(source: str, pattern: str) -> str:
    match = re.search(
        pattern + r".*?^```(?:\w+)?\s*$\n(.*?)^```\s*$",
        source,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError("配方代码块未找到: %s" % pattern)
    return match.group(1).strip()


def extract_recipe(style_id: str) -> str:
    source = RECIPES_PATH.read_text(encoding="utf-8")
    return _first_block_after(source, r"^## %s[｜\s]" % re.escape(style_id))


def extract_layer(layer: str) -> str:
    heading = APPENDIX_LAYERS[layer]
    source = RECIPES_PATH.read_text(encoding="utf-8")
    return _first_block_after(source, r"^### %s\s*$" % re.escape(heading))


def registry_line(style_id: str) -> str:
    """Fallback for keys without a deep recipe: the one-line registry entry."""
    for line in REGISTRY_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("- `%s`" % style_id):
            parts = line.lstrip("- ").split("｜")
            if len(parts) >= 3:
                return "Render Image 1 in this style. %s" % parts[2].strip()
            return "Render Image 1 in this style. %s" % parts[-1].strip()
    raise ValueError("风格 key 不存在: %s" % style_id)


def build_prompt(style_id: str, aspect: str | None, intensity: str,
                 layers: list[str], note: str | None) -> tuple[str, str]:
    try:
        recipe = extract_recipe(style_id)
        source = "deep-recipe"
    except ValueError:
        recipe = registry_line(style_id)
        source = "registry-fallback"

    name = STYLE_NAMES.get(style_id, style_id)
    aspect_clause = ", and the target aspect ratio is %s" % aspect.strip() if aspect else ""
    preamble = PREAMBLE[intensity].format(name=name, aspect=aspect_clause)

    blocks = [preamble, "", recipe]
    for layer in layers:
        blocks += ["", extract_layer(layer)]
    if note:
        blocks += ["", note.strip()]
    blocks += ["", POSTSCRIPT]
    return "\n".join(blocks), source


def main() -> int:
    parser = argparse.ArgumentParser(
        description="从 style-recipes.md 原样提取配方并拼装改图 prompt。")
    parser.add_argument("--style", help="风格 key 或中文别名")
    parser.add_argument("--aspect", help="目标画幅，例如 9:16；不传则沿用原图比例")
    parser.add_argument("--intensity", choices=("轻度", "中度", "强度"),
                        default="中度", help="风格覆盖程度（默认 中度）")
    parser.add_argument("--layer", action="append", default=[],
                        choices=sorted(APPENDIX_LAYERS),
                        help="叠加层，可重复；选项：%s" % ", ".join(sorted(APPENDIX_LAYERS)))
    parser.add_argument("--note", help="追加一句用户补充要求（原样附加，不改写配方）")
    parser.add_argument("--image", help="原图路径，仅用于 JSON 调用包")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--list", action="store_true", help="列出已有深度配方的 key")
    args = parser.parse_args()

    if args.list:
        for key in STYLE_NAMES:
            print(key)
        return 0

    if not args.style:
        print("render_prompt: 需要 --style，或用 --list 查看可用深度配方", file=sys.stderr)
        return 2

    if args.image and not Path(args.image).is_file():
        print("render_prompt: 原图不存在: %s" % args.image, file=sys.stderr)
        return 2

    try:
        style_id = canonical_style_id(args.style)
        prompt, source = build_prompt(style_id, args.aspect, args.intensity,
                                      args.layer, args.note)
    except ValueError as error:
        print("render_prompt: %s" % error, file=sys.stderr)
        return 2

    if source == "registry-fallback":
        print("render_prompt: 注意 %s 暂无深度配方，已退回一行式注册表描述，"
              "保真度低于深度配方" % style_id, file=sys.stderr)

    if args.format == "json":
        print(json.dumps({
            "style_id": style_id,
            "prompt": prompt,
            "recipe_source": source,
            "intensity": args.intensity,
            "aspect": args.aspect,
            "layers": args.layer,
            "image": args.image,
        }, ensure_ascii=False, indent=2))
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
