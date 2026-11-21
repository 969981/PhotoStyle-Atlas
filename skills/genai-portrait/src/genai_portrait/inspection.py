from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


def contact_sheet(paths: list[Path], output: Path, tile_size: int = 640) -> None:
    if not paths:
        raise ValueError("At least one image is required")
    margin = 24
    label_height = 48
    width = len(paths) * tile_size + (len(paths) + 1) * margin
    height = tile_size + label_height + 2 * margin
    canvas = Image.new("RGB", (width, height), (18, 19, 22))
    draw = ImageDraw.Draw(canvas)
    for index, path in enumerate(paths):
        with Image.open(path) as source:
            tile = ImageOps.contain(source.convert("RGB"), (tile_size, tile_size))
        x = margin + index * (tile_size + margin)
        y = margin + (tile_size - tile.height) // 2
        canvas.paste(tile, (x + (tile_size - tile.width) // 2, y))
        draw.text((x, margin + tile_size + 12), path.name, fill=(230, 232, 236))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, quality=92, optimize=True)
